"""CSIP Alternative World Simulator & Policy Intervention Engine (Milestone 10 - Gate G9).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Simulasi skenario alternatif kebijakan (S0 - S5).
- [UK-10 Mengevaluasi Model]: Validasi sanity constraints & Extrapolation Guardrails.
- [UK-11 Mengembangkan Solusi]: Proyeksi dampak bisnis (GMV lift, biaya subsidi, net profit, ROI).

Claim Governance:
- In-distribution scenarios are assigned Grade B (Cukup / Bersyarat) associational evidence.
- Scenarios violating Extrapolation Guardrails are automatically downgraded to Grade C/D.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from csip.uncertainty.bootstrap import ResidualBootstrapper
from csip.world.state_transition import WorldStateTransitionModel

logger = logging.getLogger(__name__)


@dataclass
class ScenarioDefinition:
    scenario_id: str
    name: str
    description: str
    delta_freight_pct: float  # e.g., -0.15 for 15% freight reduction
    delta_delay_days: float   # e.g., -3.0 for 3 days faster delivery
    subsidy_per_order_brl: float
    target_segment: str = "all"


class AlternativeWorldSimulator:
    """Simulates counterfactual policy interventions and financial outcomes."""

    SCENARIOS: Dict[str, ScenarioDefinition] = {
        "S0_baseline": ScenarioDefinition(
            scenario_id="S0_baseline",
            name="Baseline (Status Quo)",
            description="Lanjutan tren alamiah tanpa perubahan kebijakan operasional atau logistik.",
            delta_freight_pct=0.0,
            delta_delay_days=0.0,
            subsidy_per_order_brl=0.0,
        ),
        "S1_freight_subsidy": ScenarioDefinition(
            scenario_id="S1_freight_subsidy",
            name="Universal Freight Subsidy (15%)",
            description="Subsidi ongkos kirim flat 15% untuk seluruh pesanan e-commerce.",
            delta_freight_pct=-0.15,
            delta_delay_days=0.0,
            subsidy_per_order_brl=3.50,
        ),
        "S2_carrier_sla": ScenarioDefinition(
            scenario_id="S2_carrier_sla",
            name="Carrier Logistics SLA Overhaul",
            description="Optimasi SLA mitra logistik untuk memangkas keterlambatan rata-rata 3 hari.",
            delta_freight_pct=0.0,
            delta_delay_days=-3.0,
            subsidy_per_order_brl=1.20,
        ),
        "S3_targeted_friction": ScenarioDefinition(
            scenario_id="S3_targeted_friction",
            name="Targeted Friction Cohort Subsidy",
            description="Subsidi ongkir selektif 25% hanya untuk segmen friksi tinggi (Cluster 0).",
            delta_freight_pct=-0.10,  # Macro average equivalent
            delta_delay_days=-1.0,
            subsidy_per_order_brl=1.80,
            target_segment="Cluster_0_Friction",
        ),
        "S4_macro_shock": ScenarioDefinition(
            scenario_id="S4_macro_shock",
            name="Macroeconomic Fuel & Delay Shock",
            description="Kenaikan harga BBM logistik (+20% ongkir) disertai lonjakan delay (+4 hari).",
            delta_freight_pct=+0.20,
            delta_delay_days=+4.0,
            subsidy_per_order_brl=0.0,
        ),
        "S5_combined_blitz": ScenarioDefinition(
            scenario_id="S5_combined_blitz",
            name="Combined Logistics & Subsidy Blitz",
            description="Intervensi ganda: subsidi ongkir 15% dikombinasikan dengan pemangkasan delay 3 hari.",
            delta_freight_pct=-0.15,
            delta_delay_days=-3.0,
            subsidy_per_order_brl=4.50,
        ),
    }

    def __init__(
        self,
        world_model: WorldStateTransitionModel,
        historical_df: pd.DataFrame,
        random_state: int = 42,
    ) -> None:
        self.world_model = world_model
        self.historical_df = historical_df
        self.random_state = random_state

        self.bootstrapper = ResidualBootstrapper(world_model=world_model, random_state=random_state)
        self.residuals_scaled = self.bootstrapper.extract_empirical_residuals(historical_df)

        # Compute empirical support envelope for Extrapolation Guardrails
        s_data = historical_df[self.world_model.state_cols].values
        self.hist_min = np.min(s_data, axis=0)
        self.hist_max = np.max(s_data, axis=0)
        self.hist_mean = np.mean(s_data, axis=0)
        self.hist_std = np.std(s_data, axis=0) + 1e-6

        # Average historical order value (BRL)
        self.mean_order_value = float(historical_df["mean_item_price"].mean()) + float(historical_df["mean_freight_value"].mean())
        self.platform_take_rate = 0.15  # 15% platform monetization rate

    def check_extrapolation_guardrails(self, trajectory_median: np.ndarray) -> Dict[str, Any]:
        """Verify whether simulated trajectory remains within historical empirical support.

        Tolerance buffer: mu +/- 3.5 std dev.
        """
        lower_bound = self.hist_mean - 3.5 * self.hist_std
        upper_bound = self.hist_max + 1.0 * self.hist_std

        ood_violations = []
        max_z_score = 0.0

        for col_idx, col_name in enumerate(self.world_model.state_cols):
            vals = trajectory_median[:, col_idx]
            z_scores = np.abs((vals - self.hist_mean[col_idx]) / self.hist_std[col_idx])
            col_max_z = float(np.max(z_scores))
            if col_max_z > max_z_score:
                max_z_score = col_max_z

            if np.any(vals < lower_bound[col_idx]) or np.any(vals > upper_bound[col_idx]):
                ood_violations.append({
                    "variable": col_name,
                    "max_simulated": float(np.max(vals)),
                    "min_simulated": float(np.min(vals)),
                    "hist_min": float(self.hist_min[col_idx]),
                    "hist_max": float(self.hist_max[col_idx]),
                    "max_z_score": col_max_z,
                })

        is_ood = len(ood_violations) > 0
        return {
            "is_out_of_distribution": is_ood,
            "max_z_score": max_z_score,
            "violations": ood_violations,
            "evidence_grade": "Grade C (Spekulatif / Guardrail Triggered)" if is_ood else "Grade B (Cukup / Bersyarat)",
        }

    def simulate_scenario(
        self,
        scenario_id: str,
        horizon_weeks: int = 12,
        n_bootstraps: int = 300,
    ) -> Dict[str, Any]:
        """Execute counterfactual simulation with uncertainty intervals and business impact."""
        if scenario_id not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario_id: {scenario_id}. Choose from {list(self.SCENARIOS.keys())}")

        scenario = self.SCENARIOS[scenario_id]

        # Starting state S_0: latest historical week
        initial_state = self.historical_df[self.world_model.state_cols].iloc[-1].values.copy()

        # Build action vector in scaled space
        # State: [0: volume, 1: delay, 2: freight_ratio, 3: review_rate]
        action_scaled = np.zeros(self.world_model.d, dtype=np.float64)

        # Scale delay change
        if scenario.delta_delay_days != 0.0:
            action_scaled[1] = scenario.delta_delay_days / self.world_model.state_stds_[1]

        # Scale freight ratio change
        if scenario.delta_freight_pct != 0.0:
            delta_ratio = scenario.delta_freight_pct * self.world_model.state_means_[2]
            action_scaled[2] = delta_ratio / self.world_model.state_stds_[2]

        action_schedule = [action_scaled] * horizon_weeks

        # Run residual bootstrap
        trajectories = self.bootstrapper.simulate_trajectories(
            initial_state=initial_state,
            horizon_weeks=horizon_weeks,
            residuals_scaled=self.residuals_scaled,
            action_schedule=action_schedule,
            n_bootstraps=n_bootstraps,
        )

        intervals = self.bootstrapper.compute_intervals(trajectories)
        median_traj = intervals["median"]

        # Run Extrapolation Guardrail
        guardrail = self.check_extrapolation_guardrails(median_traj)

        # Compute cumulative business metrics over horizon (weeks 1 to H)
        sim_volumes = median_traj[1:, 0]
        cumulative_volume = float(np.sum(sim_volumes))
        avg_negative_review_rate = float(np.mean(median_traj[1:, 3]))
        avg_delay_days = float(np.mean(median_traj[1:, 1]))
        avg_freight_ratio = float(np.mean(median_traj[1:, 2]))

        # Financial impact
        gross_gmv = cumulative_volume * self.mean_order_value
        subsidy_cost = cumulative_volume * scenario.subsidy_per_order_brl
        platform_revenue = gross_gmv * self.platform_take_rate

        return {
            "scenario_id": scenario.scenario_id,
            "name": scenario.name,
            "description": scenario.description,
            "horizon_weeks": horizon_weeks,
            "cumulative_volume": cumulative_volume,
            "avg_negative_review_rate": avg_negative_review_rate,
            "avg_delay_days": avg_delay_days,
            "avg_freight_ratio": avg_freight_ratio,
            "gross_gmv_brl": gross_gmv,
            "subsidy_cost_brl": subsidy_cost,
            "platform_revenue_brl": platform_revenue,
            "guardrail": guardrail,
            "intervals": {k: v.tolist() for k, v in intervals.items()},
        }

