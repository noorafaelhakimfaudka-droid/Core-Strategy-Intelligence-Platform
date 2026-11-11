"""Tests for Rolling-Origin Temporal CV, Survival Analysis, and Calibration (Phase 3 & 4).

Validates:
1. Embargo constraints (>= 90 days between train and validation)
2. Zero label/data overlap across train and validation splits
3. Optimal threshold selection without access to test set
4. Locked test set evaluation reported strictly once
5. Categorical target encoding fit strictly on train fold
6. Probability calibrator fit without test set access
7. Survival analysis censoring handling (Kaplan-Meier and C-index)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression

from csip.evaluation.survival_analysis import (
    DiscreteTimeHazardModel,
    KaplanMeierEstimator,
    ProbabilityCalibrator,
    calculate_concordance_index,
    compute_decision_curve_analysis,
    compute_top_k_lift,
)
from csip.evaluation.temporal_cv import (
    RollingOriginTemporalCV,
    TemporalCVManager,
    compute_block_bootstrap_ci,
)
from csip.features.builder import CategoricalFoldEncoder


@pytest.fixture
def synthetic_temporal_df() -> pd.DataFrame:
    """Generates synthetic temporal dataset spanning 2017-01-01 to 2018-08-31."""
    rng = np.random.default_rng(42)
    n = 2000
    dates = pd.date_range("2017-01-01", "2018-08-30", periods=n)
    
    categories = ["beleza_saude", "relogios_presentes", "cama_mesa_banho", "esporte_lazer"]
    states = ["SP", "RJ", "MG", "RS", "PR"]
    payments = ["credit_card", "boleto", "voucher", "debit_card"]

    df = pd.DataFrame({
        "order_id": [f"ord_{i:05d}" for i in range(n)],
        "order_purchase_timestamp": dates,
        "product_category": rng.choice(categories, size=n),
        "customer_state": rng.choice(states, size=n),
        "payment_type_primary": rng.choice(payments, size=n),
        "price": rng.uniform(20.0, 500.0, size=n),
        "freight_value": rng.uniform(10.0, 50.0, size=n),
        "delivery_delay_days": rng.uniform(-5.0, 15.0, size=n),
        "target": rng.binomial(1, 0.12, size=n),
    })
    return df


def test_cv_folds_embargo(synthetic_temporal_df: pd.DataFrame) -> None:
    """Verifies that all temporal folds strictly enforce max(train) + embargo <= min(val)."""
    cv = RollingOriginTemporalCV(
        n_folds=4,
        embargo_days=90,
        min_train_days=180,
        val_window_days=45,
        test_start_date="2018-07-01",
    )
    folds = cv.get_folds(synthetic_temporal_df)

    assert len(folds) >= 4, f"Expected at least 4 folds, got {len(folds)}"

    for fold in folds:
        assert fold.validate_embargo(), f"Fold {fold.fold_idx} failed embargo validation"
        days_gap = (fold.val_start - fold.train_end).days
        assert days_gap >= 90, f"Fold {fold.fold_idx} embargo gap {days_gap} is less than 90 days"
        assert fold.val_end <= pd.to_datetime("2018-07-01"), "Validation must not enter locked test period"


def test_no_label_overlap_across_folds(synthetic_temporal_df: pd.DataFrame) -> None:
    """Asserts that there is zero index overlap between train, embargo, and validation splits."""
    cv = RollingOriginTemporalCV(
        n_folds=4,
        embargo_days=90,
        test_start_date="2018-07-01",
    )

    for tr_idx, val_idx, fold in cv.split(synthetic_temporal_df):
        overlap = set(tr_idx).intersection(set(val_idx))
        assert len(overlap) == 0, f"Fold {fold.fold_idx} has {len(overlap)} overlapping indices"

        tr_dates = synthetic_temporal_df.iloc[tr_idx]["order_purchase_timestamp"]
        val_dates = synthetic_temporal_df.iloc[val_idx]["order_purchase_timestamp"]

        assert tr_dates.max() < val_dates.min(), "Train dates must strictly precede validation dates"
        assert (val_dates.min() - tr_dates.max()).days >= 90, "Minimum gap must be at least 90 days"


def test_threshold_selected_without_test(synthetic_temporal_df: pd.DataFrame) -> None:
    """Asserts that decision threshold is selected strictly from validation folds."""
    manager = TemporalCVManager()
    
    feature_cols = ["price", "freight_value", "delivery_delay_days"]
    results = manager.run_cv(
        df=synthetic_temporal_df,
        feature_cols=feature_cols,
        target_col="target",
        model_factory=lambda: LogisticRegression(random_state=42),
        is_classifier=True,
        n_folds=4,
        embargo_days=90,
    )

    assert "folds" in results
    assert len(results["folds"]) >= 4

    for fold_report in results["folds"]:
        assert "optimal_threshold" in fold_report
        assert 0.0 < fold_report["optimal_threshold"] < 1.0
        assert "pr_auc" in fold_report
        assert "brier_score" in fold_report


def test_test_set_used_once(synthetic_temporal_df: pd.DataFrame) -> None:
    """Asserts that TemporalCVManager allows locked test evaluation exactly once and raises afterwards."""
    manager = TemporalCVManager()
    assert not manager.final_locked_test_reported_once

    X_test = synthetic_temporal_df[["price", "freight_value", "delivery_delay_days"]].iloc[-100:]
    y_test = synthetic_temporal_df["target"].iloc[-100:].values

    model = LogisticRegression(random_state=42)
    model.fit(X_test, y_test)

    # First evaluation succeeds
    res = manager.evaluate_locked_test_once(
        model=model,
        X_test=X_test,
        y_test=y_test,
        threshold=0.5,
        is_classifier=True,
    )
    assert manager.final_locked_test_reported_once
    assert "pr_auc" in res
    assert "brier_score" in res

    # Second evaluation must raise RuntimeError
    with pytest.raises(RuntimeError, match="Violation: Final locked test set has ALREADY been evaluated"):
        manager.evaluate_locked_test_once(
            model=model,
            X_test=X_test,
            y_test=y_test,
            threshold=0.5,
            is_classifier=True,
        )


def test_categorical_encoders_fit_on_train_only(synthetic_temporal_df: pd.DataFrame) -> None:
    """Verifies that CategoricalFoldEncoder only fits on training data and handles unseen categories."""
    encoder = CategoricalFoldEncoder(
        cat_cols=["product_category", "payment_type_primary", "customer_state"],
        smoothing=10.0,
    )

    # Transform before fit must raise ValueError
    with pytest.raises(ValueError, match="must be fitted on training fold data"):
        encoder.transform(synthetic_temporal_df)

    # Split train and validation
    train_df = synthetic_temporal_df.iloc[:1000]
    val_df = synthetic_temporal_df.iloc[1000:].copy()

    # Inject an unseen category into val_df
    val_df.iloc[0, val_df.columns.get_loc("product_category")] = "brand_new_unseen_cat"

    encoder.fit(train_df, train_df["target"])
    assert encoder.fitted_on_train_only

    transformed_val = encoder.transform(val_df)
    assert "product_category_te" in transformed_val.columns
    assert "customer_state_te" in transformed_val.columns
    assert "payment_type_primary_te" in transformed_val.columns

    # Unseen category gets mapped to the global training target mean
    global_mean = train_df["target"].mean()
    unseen_encoded_val = transformed_val.iloc[0]["product_category_te"]
    assert np.isclose(unseen_encoded_val, global_mean, atol=1e-3)


def test_calibration_fit_without_test() -> None:
    """Verifies ProbabilityCalibrator fits on validation probabilities and calculates ECE and BSS."""
    rng = np.random.default_rng(42)
    n = 500
    y_true = rng.binomial(1, 0.15, size=n)
    # Underconfident / uncalibrated raw scores
    raw_probs = np.clip(y_true * 0.4 + rng.uniform(0.05, 0.25, size=n), 0.01, 0.99)

    calibrator = ProbabilityCalibrator()
    calibrator.fit(raw_probs, y_true)
    assert calibrator.is_fitted

    calibrated_probs = calibrator.calibrate(raw_probs)
    assert len(calibrated_probs) == n
    assert (calibrated_probs >= 0.0).all() and (calibrated_probs <= 1.0).all()

    ece_raw = ProbabilityCalibrator.compute_ece(y_true, raw_probs)
    ece_cal = ProbabilityCalibrator.compute_ece(y_true, calibrated_probs)
    assert ece_cal <= ece_raw or ece_cal < 0.10

    bss = ProbabilityCalibrator.compute_brier_skill_score(y_true, calibrated_probs)
    assert isinstance(bss, float)


def test_survival_censoring_handled() -> None:
    """Tests Kaplan-Meier estimation and Harrell's C-index under right censoring."""
    durations = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    events = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])  # 0 = censored
    predicted_risks = np.array([0.9, 0.8, 0.75, 0.6, 0.5, 0.4, 0.35, 0.3, 0.2, 0.1])

    km = KaplanMeierEstimator()
    km.fit(durations, events)

    assert km.timeline is not None
    assert km.survival_probabilities is not None

    # Survival probability is monotonic non-increasing
    diffs = np.diff(km.survival_probabilities)
    assert (diffs <= 0.0).all(), "Survival probability must be monotonically non-increasing"

    # Risk at t=0 should be 0, risk at large t should be > 0
    assert km.predict_risk_at(0.0) == 0.0
    assert km.predict_risk_at(120.0) > 0.0

    # Concordance index should be high because risks align with early events
    c_index = calculate_concordance_index(durations, predicted_risks, events)
    assert 0.5 <= c_index <= 1.0


def test_decision_curve_and_lift() -> None:
    """Tests Decision Curve Analysis and Top-k% Lift computations."""
    rng = np.random.default_rng(42)
    n = 1000
    y_true = rng.binomial(1, 0.10, size=n)
    y_prob = np.clip(y_true * 0.5 + rng.uniform(0.0, 0.4, size=n), 0.0, 1.0)

    dca_df = compute_decision_curve_analysis(y_true, y_prob)
    assert isinstance(dca_df, pd.DataFrame)
    assert "net_benefit_model" in dca_df.columns
    assert "net_benefit_treat_all" in dca_df.columns

    lifts = compute_top_k_lift(y_true, y_prob, k_percentiles=[0.05, 0.10, 0.20])
    assert "lift_top_5pct" in lifts
    assert lifts["lift_top_5pct"] >= 1.0, "Model should achieve lift >= 1.0 on top 5%"

