"""CSIP Uncertainty Quantification Module: Multi-Trajectory Residual Bootstrapping.

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Kuantifikasi ketidakpastian proyeksi simulasi.
- [UK-10 Mengevaluasi Model]: Estimasi Prediction Intervals (50%, 90%, 95%) berbasis empirical residuals.

Methodology:
Generates B recursive state-space rollout trajectories by sampling empirical innovation residuals
with replacement from the historical training transitions, preserving cross-variable correlation.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from csip.world.state_transition import WorldStateTransitionModel

logger = logging.getLogger(__name__)


class ResidualBootstrapper:
    """Non-parametric residual bootstrapping for dynamic state-space trajectories."""

    def __init__(
        self,
        world_model: WorldStateTransitionModel,
        random_state: int = 42,
    ) -> None:
        if not world_model.is_fitted:
            raise ValueError("WorldStateTransitionModel must be fitted before bootstrapping.")
        self.world_model = world_model
        self.random_state = random_state
        self.rng = np.random.default_rng(random_state)

    def extract_empirical_residuals(self, df: pd.DataFrame) -> np.ndarray:
        """Compute empirical 1-step prediction residual matrix on historical panel."""
        x_lag, y_next = self.world_model._prepare_panel(df)
        x_scaled = (x_lag - self.world_model.state_means_) / self.world_model.state_stds_
        y_scaled = (y_next - self.world_model.state_means_) / self.world_model.state_stds_

        y_pred_scaled = self.world_model.regressor.predict(x_scaled)
        residuals_scaled = y_scaled - y_pred_scaled
        return residuals_scaled

    def simulate_trajectories(
        self,
        initial_state: np.ndarray,
        horizon_weeks: int,
        residuals_scaled: np.ndarray,
        action_schedule: Optional[List[Optional[np.ndarray]]] = None,
        n_bootstraps: int = 300,
    ) -> np.ndarray:
        """Run B recursive simulation trajectories with empirical residual innovations.

        Returns
        -------
        trajectories : np.ndarray
            Array of shape (n_bootstraps, horizon_weeks + 1, d) containing all simulated paths.
        """
        d = self.world_model.d
        n_res = len(residuals_scaled)
        all_trajectories = np.zeros((n_bootstraps, horizon_weeks + 1, d), dtype=np.float64)

        for b in range(n_bootstraps):
            traj = np.zeros((horizon_weeks + 1, d), dtype=np.float64)
            traj[0] = initial_state
            curr = initial_state.copy()

            for t in range(horizon_weeks):
                # Scale current state
                s_scaled = (curr - self.world_model.state_means_) / self.world_model.state_stds_

                # Deterministic transition: S_{t+1} = C + Phi * S_t
                next_scaled = self.world_model.intercept_ + self.world_model.phi_matrix_ @ s_scaled

                # Apply action offset if any
                if action_schedule and t < len(action_schedule) and action_schedule[t] is not None:
                    next_scaled += action_schedule[t]

                # Sample empirical residual vector
                res_idx = self.rng.integers(0, n_res)
                innovation = residuals_scaled[res_idx]
                next_scaled += innovation

                # Unscale back to natural units
                curr = next_scaled * self.world_model.state_stds_ + self.world_model.state_means_

                # Enforce physical bounds
                curr[0] = max(0.0, curr[0])
                curr[2] = max(0.0, min(1.0, curr[2]))
                curr[3] = max(0.0, min(1.0, curr[3]))

                traj[t + 1] = curr

            all_trajectories[b] = traj

        return all_trajectories

    def compute_intervals(
        self,
        trajectories: np.ndarray,
    ) -> Dict[str, np.ndarray]:
        """Compute quantile summaries across bootstrap trajectories."""
        # Quantiles along bootstrap axis (axis 0)
        q025 = np.quantile(trajectories, 0.025, axis=0)
        q05 = np.quantile(trajectories, 0.05, axis=0)
        q50 = np.quantile(trajectories, 0.50, axis=0)  # Median
        q95 = np.quantile(trajectories, 0.95, axis=0)
        q975 = np.quantile(trajectories, 0.975, axis=0)

        mean_traj = np.mean(trajectories, axis=0)
        std_traj = np.std(trajectories, axis=0)

        return {
            "p025": q025,
            "p050": q05,
            "median": q50,
            "p950": q95,
            "p975": q975,
            "mean": mean_traj,
            "std": std_traj,
        }

