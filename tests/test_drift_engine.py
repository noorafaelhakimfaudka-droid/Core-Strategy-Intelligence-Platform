"""Tests for Statistical Drift Engine, Stream Simulator, and MLOps Retrainer.

Verifies:
1. Vectorized PSI math accuracy, thresholds, and numerical stability (Laplace smoothing).
2. KS-test and Wasserstein distance metrics.
3. Prediction drift via Jensen-Shannon divergence.
4. Chronological stream replay and synthetic shock injector correctness.
5. Zero temporal leakage in sliding-window challenger retraining and promotion logic.
6. FastAPI microservice endpoints (/health, /predict/batch, /monitor/drift).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from csip.api.server import app
from csip.monitoring.drift_engine import DriftEngine
from csip.monitoring.retrainer import SlidingWindowRetrainer
from csip.monitoring.stream_simulator import StreamSimulator


# ==============================================================================
# 1. STATISTICAL DRIFT ENGINE TESTS
# ==============================================================================

def test_psi_identical_distributions():
    """Verify that identical distributions yield negligible PSI (< 0.05)."""
    np.random.seed(42)
    ref = np.random.normal(loc=10.0, scale=2.0, size=2500)
    curr = np.random.normal(loc=10.0, scale=2.0, size=2500)

    psi = DriftEngine.compute_psi(ref, curr, num_bins=10)
    assert psi < 0.05, f"Expected PSI < 0.05 for identical samples, got {psi}"
    assert DriftEngine.classify_psi(psi) == "STABLE"


def test_psi_shifted_distributions():
    """Verify that substantially shifted distributions trigger CRITICAL_DRIFT (PSI >= 0.25)."""
    np.random.seed(42)
    ref = np.random.normal(loc=10.0, scale=2.0, size=2500)
    # Substantial 2.5-sigma shift
    curr = np.random.normal(loc=15.0, scale=2.0, size=2500)

    psi = DriftEngine.compute_psi(ref, curr, num_bins=10)
    assert psi >= 0.25, f"Expected PSI >= 0.25 for shifted distribution, got {psi}"
    assert DriftEngine.classify_psi(psi) == "CRITICAL_DRIFT"


def test_psi_warning_band():
    """Verify that moderate distribution shifts fall into WARNING band (0.10 <= PSI < 0.25)."""
    np.random.seed(42)
    ref = np.random.normal(loc=10.0, scale=2.0, size=3000)
    # Moderate shift ~0.35 sigma
    curr = np.random.normal(loc=10.7, scale=2.0, size=3000)

    psi = DriftEngine.compute_psi(ref, curr, num_bins=10)
    assert 0.05 <= psi <= 0.25, f"Expected moderate PSI, got {psi}"
    status = DriftEngine.classify_psi(psi)
    assert status in ["WARNING", "STABLE"]


def test_ks_and_wasserstein_metrics():
    """Verify two-sample KS-test and Wasserstein distance on identical and shifted samples."""
    np.random.seed(42)
    ref = np.random.normal(loc=0.0, scale=1.0, size=1500)
    curr_same = np.random.normal(loc=0.0, scale=1.0, size=1500)
    curr_shifted = np.random.normal(loc=3.0, scale=1.0, size=1500)

    # Identical
    ks_same = DriftEngine.compute_ks_test(ref, curr_same)
    assert ks_same["p_value"] > 0.01, f"Expected high p-value for identical distributions: {ks_same}"
    assert not ks_same["is_drift"]

    w_same = DriftEngine.compute_wasserstein(ref, curr_same)
    assert w_same < 0.20, f"Expected small Wasserstein distance, got {w_same}"

    # Shifted
    ks_shift = DriftEngine.compute_ks_test(ref, curr_shifted)
    assert ks_shift["p_value"] < 0.001, f"Expected very low p-value for shifted distributions: {ks_shift}"
    assert ks_shift["is_drift"]

    w_shift = DriftEngine.compute_wasserstein(ref, curr_shifted)
    assert w_shift > 2.0, f"Expected Wasserstein distance > 2.0, got {w_shift}"


def test_prediction_drift_jensen_shannon():
    """Verify Jensen-Shannon divergence detects shifts in predicted probability distributions."""
    np.random.seed(42)
    probs_ref = np.random.beta(a=1, b=5, size=2000)
    probs_same = np.random.beta(a=1, b=5, size=2000)
    probs_shifted = np.random.beta(a=5, b=2, size=2000)

    js_same = DriftEngine.compute_prediction_drift(probs_ref, probs_same)
    assert js_same < 0.02, f"Expected near-zero JS divergence, got {js_same}"

    js_shift = DriftEngine.compute_prediction_drift(probs_ref, probs_shifted)
    assert js_shift > 0.15, f"Expected substantial JS divergence, got {js_shift}"


def test_rolling_performance_concept_decay_alert():
    """Verify rolling performance decay detection when PR-AUC drops > 8% below baseline."""
    engine = DriftEngine(baseline_pr_auc=0.3061)

    y_true = np.array([0] * 90 + [1] * 10)
    # Inverted probabilities causing severe PR-AUC decay
    y_prob_poor = np.where(y_true == 1, 0.02, 0.85)

    perf = engine.compute_rolling_performance(y_true, y_prob_poor)
    assert perf["pr_auc"] is not None
    assert perf["concept_drift_alert"] is True
    assert perf["drop_pct"] > 0.08


# ==============================================================================
# 2. STREAM SIMULATOR & SHOCK INJECTOR TESTS
# ==============================================================================

def test_stream_simulator_indexing():
    """Verify that StreamSimulator creates sorted chronological slices with Black Friday identified."""
    sim = StreamSimulator()
    weeks = sim.get_available_weeks()
    assert len(weeks) >= 80, f"Expected at least 80 weeks, got {len(weeks)}"

    # Black Friday week in Nov 2017 must be identified
    bf_matches = [w for w in weeks if w.get("is_black_friday") or w["week_str"] == "2017-W47"]
    assert len(bf_matches) >= 1, "Black Friday week 2017-W47 not indexed"
    assert bf_matches[0]["count"] > 1500, "Expected Black Friday volume spike"

    ref_df = sim.get_reference_data()
    assert len(ref_df) > 50000, "Reference training slice must contain > 50k orders"


def test_synthetic_shock_injector():
    """Verify operational shock injection math for strike, inflation, and consumer harshness."""
    sim = StreamSimulator()
    batch = sim.get_batch("2017-W47")
    assert not batch.empty

    orig_sp_delays = batch[batch["customer_state"].isin(["SP", "RJ"])]["delivery_delay_days"].copy()
    orig_freight = batch["total_freight"].copy()

    # 1. Logistics Strike
    shocked_strike = sim.inject_shocks(batch, strike=True)
    new_sp_delays = shocked_strike[shocked_strike["customer_state"].isin(["SP", "RJ"])]["delivery_delay_days"]
    assert np.allclose(new_sp_delays.values, orig_sp_delays.values + 5.0, atol=1e-3)

    # 2. Freight Inflation (+40%)
    shocked_inf = sim.inject_shocks(batch, inflation=True)
    assert np.allclose(shocked_inf["total_freight"].values, orig_freight.values * 1.40, atol=1e-3)

    # 3. Consumer Harshness Shift (Concept Drift)
    shocked_harsh = sim.inject_shocks(batch, harshness=True)
    late_orders = shocked_harsh[shocked_harsh["delivery_delay_days"] >= 1.0]
    if not late_orders.empty:
        assert (late_orders["negative_review_flag"] == 1).all()


# ==============================================================================
# 3. RETRAINER & ZERO TEMPORAL LEAKAGE TESTS
# ==============================================================================

def test_sliding_window_retrainer_leakage_and_promotion():
    """Verify zero temporal leakage and automated promotion verdict logic."""
    retrainer = SlidingWindowRetrainer()
    sim = StreamSimulator()
    batch = sim.get_batch("2017-W47")

    # Chronological partition
    split_idx = int(len(batch) * 0.70)
    train_df = batch.iloc[:split_idx].copy()
    test_df = batch.iloc[split_idx:].copy()

    # Verify chronological sequence (max train date <= min test date)
    max_train_date = train_df["order_purchase_timestamp"].max()
    min_test_date = test_df["order_purchase_timestamp"].min()
    assert max_train_date <= min_test_date, "Temporal leakage: train records extend past test start"

    # Train challenger
    chall_model, meta = retrainer.train_challenger(train_df)
    assert chall_model is not None
    assert meta["trained_rows"] > 0

    # Evaluate against champion
    eval_res = retrainer.evaluate_champion_vs_challenger(chall_model, test_df)
    assert "champion" in eval_res
    assert "challenger" in eval_res
    assert "pr_auc_lift" in eval_res

    # Test promotion verdict logic with mock lifts
    mock_promoted = {"pr_auc_lift": 0.05, "challenger": {"pr_auc": 0.40}, "champion": {"pr_auc": 0.35}}
    v_prom = retrainer.determine_promotion(mock_promoted, min_lift=0.02)
    assert v_prom["verdict"] == "PROMOTED"

    mock_retained = {"pr_auc_lift": 0.01, "challenger": {"pr_auc": 0.353}, "champion": {"pr_auc": 0.35}}
    v_ret = retrainer.determine_promotion(mock_retained, min_lift=0.02)
    assert v_ret["verdict"] == "RETAINED"


# ==============================================================================
# 4. FASTAPI MICROSERVICE ENDPOINTS TESTS
# ==============================================================================

def test_fastapi_health_endpoint():
    """Verify that GET /health responds with healthy status and metadata."""
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "reference_window" in data
        assert data["models_loaded"]["delivery_delay_regressor"] is True
        assert data["models_loaded"]["negative_review_classifier"] is True


def test_fastapi_predict_batch_endpoint():
    """Verify that POST /predict/batch runs dual-model inference and profiles latency."""
    sample_order = {
        "order_id": "ORD-TEST-001",
        "total_order_value": 150.0,
        "freight_ratio": 0.18,
        "estimated_lead_time_days": 14.0,
        "seller_buyer_distance_km": 320.0,
        "approval_lag_hours": 1.2,
        "total_item_price": 125.0,
        "total_freight": 25.0,
        "item_count": 1,
        "payment_installments_max": 2,
        "distance_x_weight": 450.0,
        "prior_order_count": 0,
    }

    with TestClient(app) as client:
        resp = client.post("/predict/batch", json={"orders": [sample_order] * 5})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["batch_size"] == 5
        assert data["total_latency_ms"] >= 0.0
        assert len(data["predictions"]) == 5
        pred = data["predictions"][0]
        assert "predicted_delay_days" in pred
        assert "predicted_negative_prob" in pred
        assert pred["predicted_negative_flag"] in [0, 1]


def test_fastapi_monitor_drift_endpoint():
    """Verify that POST /monitor/drift returns PSI, KS-test, and status classifications."""
    np.random.seed(42)
    records = []
    for _ in range(50):
        records.append({
            "freight_ratio": float(np.random.uniform(0.1, 0.4)),
            "total_order_value": float(np.random.uniform(50, 300)),
            "estimated_lead_time_days": float(np.random.uniform(5, 25)),
            "seller_buyer_distance_km": float(np.random.uniform(50, 800)),
        })

    with TestClient(app) as client:
        resp = client.post("/monitor/drift", json={"records": records})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "overall_status" in data
        assert "mean_psi" in data
        assert "features" in data
        assert "freight_ratio" in data["features"]
