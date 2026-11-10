"""Unit tests for CSIP Simulation Sanity & Uncertainty Invariants (Milestone 10 - Gate G9).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Verifikasi invariant simulasi kebijakan skenario.
- [UK-10 Mengevaluasi Model]: Uji batas invariant ketidakpastian & Extrapolation Guardrails.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from csip.scenarios.simulator import AlternativeWorldSimulator
from csip.world.state_transition import WorldStateTransitionModel


@pytest.fixture(scope="module")
def simulator():
    world_model = WorldStateTransitionModel.load("artifacts/models/world_model_state_transition.joblib")
    weekly_df = pd.read_parquet("data/processed/weekly_system_state.parquet")
    return AlternativeWorldSimulator(world_model=world_model, historical_df=weekly_df, random_state=42)


def test_s0_baseline_invariant(simulator):
    """Verify S0 baseline runs without policy action and produces consistent trajectories."""
    res = simulator.simulate_scenario("S0_baseline", horizon_weeks=6, n_bootstraps=50)

    assert res["scenario_id"] == "S0_baseline"
    assert res["cumulative_volume"] > 0
    assert res["subsidy_cost_brl"] == 0.0
    assert res["guardrail"]["is_out_of_distribution"] is False


def test_s1_freight_subsidy_reduces_freight_ratio(simulator):
    """Verify S1 policy intervention strictly decreases average freight ratio vs S0."""
    res_s0 = simulator.simulate_scenario("S0_baseline", horizon_weeks=6, n_bootstraps=50)
    res_s1 = simulator.simulate_scenario("S1_freight_subsidy", horizon_weeks=6, n_bootstraps=50)

    assert res_s1["avg_freight_ratio"] < res_s0["avg_freight_ratio"]
    assert res_s1["subsidy_cost_brl"] > 0.0


def test_prediction_interval_monotonicity(simulator):
    """Verify non-parametric bootstrap prediction intervals satisfy strict monotonic quantile ordering."""
    res = simulator.simulate_scenario("S2_carrier_sla", horizon_weeks=6, n_bootstraps=100)
    intv = res["intervals"]

    p025 = np.array(intv["p025"])
    p050 = np.array(intv["p050"])
    med = np.array(intv["median"])
    p950 = np.array(intv["p950"])
    p975 = np.array(intv["p975"])

    # Test across all horizon steps and state dimensions
    assert np.all(p025 <= med + 1e-5)
    assert np.all(p050 <= med + 1e-5)
    assert np.all(med <= p950 + 1e-5)
    assert np.all(med <= p975 + 1e-5)


def test_extrapolation_guardrail_detection(simulator):
    """Verify that extrapolation guardrail correctly detects out-of-distribution states."""
    # Synthetic out of distribution trajectory
    ood_traj = np.tile(simulator.hist_mean, (6, 1))
    ood_traj[:, 0] = simulator.hist_max[0] * 5.0  # 5x maximum order volume

    guard = simulator.check_extrapolation_guardrails(ood_traj)
    assert guard["is_out_of_distribution"] is True
    assert "Grade C" in guard["evidence_grade"]
    assert len(guard["violations"]) > 0


def test_simulation_results_artifact_parity():
    """Verify simulation JSON artifact exists and contains valid metrics."""
    res_path = Path("artifacts/reports/scenario_simulation_results.json")
    assert res_path.exists()

    with open(res_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for sid in ["S0_baseline", "S1_freight_subsidy", "S2_carrier_sla", "S4_macro_shock"]:
        assert sid in data
        assert "cumulative_volume" in data[sid]
        assert "comparison_to_s0" in data[sid]

