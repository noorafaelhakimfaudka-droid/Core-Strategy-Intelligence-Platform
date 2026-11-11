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


def compute_classification_bootstrap_ci(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bootstraps: int = 1000,
    alpha: float = 0.05,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Compute 95% bootstrap confidence intervals for classification metrics on test evaluation.

    Metrics computed:
    - ROC-AUC: 95% CI, point estimate, lift over chance (0.50), spans chance flag
    - PR-AUC: 95% CI, point estimate, lift over base rate, spans baseline flag
    - Brier score: 95% CI, point estimate, naive Brier baseline
    - Overall statistical distinguishability from random/naive baseline
    """
    from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

    y_true = np.asarray(y_true).astype(int)
    y_prob = np.clip(np.asarray(y_prob, dtype=np.float64), 0.0, 1.0)
    n = len(y_true)
    if n == 0 or len(np.unique(y_true)) < 2:
        return {}

    rng = np.random.default_rng(random_state)
    base_rate = float(np.mean(y_true))

    # Point estimates
    roc_point = float(roc_auc_score(y_true, y_prob))
    pr_point = float(average_precision_score(y_true, y_prob))
    brier_point = float(brier_score_loss(y_true, y_prob))

    # Naive Brier baseline (predicting constant base rate)
    brier_naive = float(brier_score_loss(y_true, np.full_like(y_prob, base_rate)))

    boot_roc = []
    boot_pr = []
    boot_brier = []

    for _ in range(n_bootstraps):
        idx = rng.integers(0, n, size=n)
        y_b = y_true[idx]
        if len(np.unique(y_b)) < 2:
            continue
        p_b = y_prob[idx]
        boot_roc.append(roc_auc_score(y_b, p_b))
        boot_pr.append(average_precision_score(y_b, p_b))
        boot_brier.append(brier_score_loss(y_b, p_b))

    low_p = (alpha / 2.0) * 100
    high_p = (1.0 - alpha / 2.0) * 100

    roc_ci = [round(float(np.percentile(boot_roc, low_p)), 4), round(float(np.percentile(boot_roc, high_p)), 4)]
    pr_ci = [round(float(np.percentile(boot_pr, low_p)), 4), round(float(np.percentile(boot_pr, high_p)), 4)]
    brier_ci = [round(float(np.percentile(boot_brier, low_p)), 4), round(float(np.percentile(boot_brier, high_p)), 4)]

    # Statistical significance checks
    roc_spans_chance = bool(roc_ci[0] <= 0.50 <= roc_ci[1])
    pr_spans_baseline = bool(pr_ci[0] <= base_rate <= pr_ci[1])

    roc_lift = round(roc_point - 0.50, 4)
    pr_lift = round(pr_point - base_rate, 4)
    relative_pr_lift_pct = round(((pr_point - base_rate) / (base_rate + 1e-9)) * 100, 2)

    statistically_distinguishable = not (roc_spans_chance or pr_spans_baseline)

    return {
        "base_rate": round(base_rate, 4),
        "roc_auc": {
            "point": round(roc_point, 4),
            "ci_95": roc_ci,
            "spans_chance": roc_spans_chance,
            "lift_over_chance": roc_lift,
        },
        "pr_auc": {
            "point": round(pr_point, 4),
            "ci_95": pr_ci,
            "spans_baseline": pr_spans_baseline,
            "lift_over_base_rate": pr_lift,
            "relative_lift_pct": relative_pr_lift_pct,
        },
        "brier_score": {
            "point": round(brier_point, 4),
            "ci_95": brier_ci,
            "naive_baseline": round(brier_naive, 4),
        },
        "statistically_distinguishable_from_baseline": statistically_distinguishable,
    }


