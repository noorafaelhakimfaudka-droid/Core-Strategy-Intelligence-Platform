"""Unit tests for CSIP World Model & State Transition Engine (Milestone 9 - Gate G8).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Verifikasi formulasi state transition & rollout.
- [UK-09 Membangun Model]: Verifikasi estimasi parameter state-space.
- [UK-10 Mengevaluasi Model]: Verifikasi pengujian identifiabilitas & metrik evaluasi (WAPE, MAPE).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from csip.world.state_transition import (
    WorldStateTransitionModel,
    compute_mape,
    compute_wape,
)


def test_wape_and_mape_calculation():
    """Verify WAPE and MAPE exact numerical computation."""
    actual = np.array([100.0, 200.0, 300.0])
    pred = np.array([110.0, 190.0, 315.0])

    # sum_diff = 10 + 10 + 15 = 35; sum_actual = 600; wape = 35 / 600 = 0.05833
    wape = compute_wape(actual, pred)
    assert wape == pytest.approx(35.0 / 600.0, rel=1e-4)
    assert wape >= 0.0

    # mape = mean([10/100, 10/200, 15/300]) = mean([0.1, 0.05, 0.05]) = 0.06666
    mape = compute_mape(actual, pred)
    assert mape == pytest.approx(0.066666, rel=1e-3)


def test_synthetic_recovery_test():
    """Verify that World Model recovers known ground-truth transition matrix Phi*."""
    model = WorldStateTransitionModel(random_state=42)
    res = model.synthetic_recovery_test(n_steps=600, noise_std=0.01, tolerance=0.15)

    assert res["recovered"] is True
    assert res["max_rel_error"] <= 0.15
    assert res["mean_rel_error"] < 0.05


def test_world_model_fit_step_bounds():
    """Verify World Model fitting, 1-step prediction, and physical constraints."""
    np.random.seed(42)
    n_weeks = 30
    df = pd.DataFrame({
        "year_week": [f"2017-W{i:02d}" for i in range(1, n_weeks + 1)],
        "weekly_order_volume": np.random.uniform(500, 2000, n_weeks).astype(np.float32),
        "mean_delivery_delay": np.random.uniform(-10, 5, n_weeks).astype(np.float32),
        "mean_freight_ratio": np.random.uniform(0.1, 0.4, n_weeks).astype(np.float32),
        "negative_review_rate": np.random.uniform(0.15, 0.35, n_weeks).astype(np.float32),
    })

    model = WorldStateTransitionModel(alpha=0.1)
    model.fit(df)
    assert model.is_fitted is True
    assert model.phi_matrix_.shape == (4, 4)

    # Step test
    s0 = np.array([1000.0, 0.0, 0.25, 0.20])
    s1 = model.step(s0, add_noise=False)

    assert len(s1) == 4
    assert s1[0] >= 0.0  # volume non-negative
    assert 0.0 <= s1[2] <= 1.0  # freight ratio bound
    assert 0.0 <= s1[3] <= 1.0  # review rate bound


def test_world_model_rollout_and_save_load():
    """Verify multi-step forward rollout and save/load integrity."""
    df = pd.read_parquet("data/processed/weekly_system_state.parquet")
    model = WorldStateTransitionModel(alpha=0.05)
    model.fit(df)

    # Rollout 8 weeks
    s0 = df[model.state_cols].iloc[0].values
    traj = model.rollout(s0, horizon_weeks=8, stochastic=False)

    assert traj.shape == (9, 4)
    np.testing.assert_allclose(traj[0], s0)

    # Save and Load
    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = Path(tmpdir) / "world_model.joblib"
        model.save(save_path)
        assert save_path.exists()

        loaded = WorldStateTransitionModel.load(save_path)
        assert loaded.is_fitted is True
        s1_orig = model.step(s0)
        s1_loaded = loaded.step(s0)
        np.testing.assert_allclose(s1_orig, s1_loaded, atol=1e-5)

