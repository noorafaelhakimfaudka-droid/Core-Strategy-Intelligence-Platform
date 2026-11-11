"""Statistical Drift & Concept Decay Monitoring Engine.

Provides vectorized NumPy and SciPy statistical algorithms for:
1. Feature Covariate Shift (Population Stability Index / PSI, Kolmogorov-Smirnov Test, Wasserstein Distance).
2. Prediction Drift (Jensen-Shannon Divergence).
3. Concept Drift & Rolling Performance Decay (PR-AUC, F1-Score, Brier Calibration Score).

Hardware-efficient, CPU-only, memory friendly (<= 8GB RAM).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, wasserstein_distance
from sklearn.metrics import auc, brier_score_loss, f1_score, precision_recall_curve


class DriftEngine:
    """Statistical Drift and Concept Decay Analysis Engine."""

    PSI_THRESHOLD_STABLE = 0.10
    PSI_THRESHOLD_WARNING = 0.25
    DEFAULT_BASELINE_PR_AUC = 0.3061

    def __init__(self, baseline_pr_auc: float = DEFAULT_BASELINE_PR_AUC) -> None:
        self.baseline_pr_auc = float(baseline_pr_auc)

    @staticmethod
    def classify_psi(psi_value: float) -> str:
        """Classify PSI into traffic-light operational status."""
        if psi_value < DriftEngine.PSI_THRESHOLD_STABLE:
            return "STABLE"
        elif psi_value < DriftEngine.PSI_THRESHOLD_WARNING:
            return "WARNING"
        return "CRITICAL_DRIFT"

    @staticmethod
    def compute_psi(
        reference: Union[np.ndarray, pd.Series, List[float]],
        current: Union[np.ndarray, pd.Series, List[float]],
        num_bins: int = 10,
        epsilon: float = 1e-4,
    ) -> float:
        """Calculate Population Stability Index (PSI) with Laplace smoothing.
        
        PSI = sum((Actual% - Expected%) * ln(Actual% / Expected%))
        """
        ref = np.asarray(reference, dtype=float)
        curr = np.asarray(current, dtype=float)
        ref = ref[np.isfinite(ref)]
        curr = curr[np.isfinite(curr)]

        if len(ref) < 2 or len(curr) < 2:
            return 0.0

        # Create quantile-based bins from reference distribution
        quantiles = np.linspace(0, 100, num_bins + 1)
        bins = np.percentile(ref, quantiles)
        bins = np.unique(bins)

        if len(bins) < 2:
            # Degenerate reference distribution (single constant value)
            return 0.0

        # Replace extreme edges with -inf and +inf to capture all current values
        bins[0] = -np.inf
        bins[-1] = np.inf

        ref_counts, _ = np.histogram(ref, bins=bins)
        curr_counts, _ = np.histogram(curr, bins=bins)

        # Proportions with Laplace smoothing to prevent division/log by zero
        ref_pct = (ref_counts + epsilon) / (len(ref) + epsilon * len(ref_counts))
        curr_pct = (curr_counts + epsilon) / (len(curr) + epsilon * len(curr_counts))

        # Re-normalize to ensure sum equals exactly 1.0
        ref_pct = ref_pct / np.sum(ref_pct)
        curr_pct = curr_pct / np.sum(curr_pct)

        psi_val = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
        return float(np.round(np.clip(psi_val, 0.0, None), 4))

    @staticmethod
    def compute_ks_test(
        reference: Union[np.ndarray, pd.Series, List[float]],
        current: Union[np.ndarray, pd.Series, List[float]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        """Compute two-sample Kolmogorov-Smirnov test."""
        ref = np.asarray(reference, dtype=float)
        curr = np.asarray(current, dtype=float)
        ref = ref[np.isfinite(ref)]
        curr = curr[np.isfinite(curr)]

        if len(ref) < 2 or len(curr) < 2:
            return {"statistic": 0.0, "p_value": 1.0, "is_drift": False}

        res = ks_2samp(ref, curr)
        stat = float(np.round(res.statistic, 4))
        p_val = float(np.round(res.pvalue, 6))
        return {
            "statistic": stat,
            "p_value": p_val,
            "is_drift": bool(p_val < alpha),
        }

    @staticmethod
    def compute_wasserstein(
        reference: Union[np.ndarray, pd.Series, List[float]],
        current: Union[np.ndarray, pd.Series, List[float]],
    ) -> float:
        """Compute first Wasserstein distance (Earth Mover's Distance)."""
        ref = np.asarray(reference, dtype=float)
        curr = np.asarray(current, dtype=float)
        ref = ref[np.isfinite(ref)]
        curr = curr[np.isfinite(curr)]

        if len(ref) < 2 or len(curr) < 2:
            return 0.0

        dist = wasserstein_distance(ref, curr)
        return float(np.round(dist, 4))

    @staticmethod
    def compute_prediction_drift(
        reference_probs: Union[np.ndarray, pd.Series, List[float]],
        current_probs: Union[np.ndarray, pd.Series, List[float]],
        num_bins: int = 10,
        epsilon: float = 1e-4,
    ) -> float:
        """Calculate Jensen-Shannon Divergence on predicted probabilities."""
        ref = np.asarray(reference_probs, dtype=float)
        curr = np.asarray(current_probs, dtype=float)
        ref = ref[np.isfinite(ref)]
        curr = curr[np.isfinite(curr)]

        if len(ref) < 2 or len(curr) < 2:
            return 0.0

        bins = np.linspace(0.0, 1.0, num_bins + 1)
        ref_counts, _ = np.histogram(ref, bins=bins)
        curr_counts, _ = np.histogram(curr, bins=bins)

        p = (ref_counts + epsilon) / (len(ref) + epsilon * len(ref_counts))
        q = (curr_counts + epsilon) / (len(curr) + epsilon * len(curr_counts))
        p = p / np.sum(p)
        q = q / np.sum(q)

        # JS distance is square root of JS divergence; squaring gives JS divergence
        js_div = float(jensenshannon(p, q, base=2) ** 2)
        return float(np.round(js_div, 4))

    def evaluate_feature_drift(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame,
        features: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Evaluate covariate drift across a specified set of numerical features."""
        if features is None:
            # Default to top numerical and interaction features
            candidates = [
                "freight_ratio",
                "total_order_value",
                "estimated_lead_time_days",
                "seller_buyer_distance_km",
                "distance_x_weight",
                "total_freight",
                "approval_lag_hours",
                "delivery_delay_days",
            ]
            features = [
                f for f in candidates if f in reference_df.columns and f in current_df.columns
            ]

        results: Dict[str, Any] = {}
        psi_scores = []
        statuses = []

        for feat in features:
            ref_vals = reference_df[feat].dropna().values
            curr_vals = current_df[feat].dropna().values

            if len(ref_vals) < 2 or len(curr_vals) < 2:
                continue

            psi = self.compute_psi(ref_vals, curr_vals)
            ks_res = self.compute_ks_test(ref_vals, curr_vals)
            w_dist = self.compute_wasserstein(ref_vals, curr_vals)
            status = self.classify_psi(psi)

            results[feat] = {
                "psi": psi,
                "status": status,
                "ks_statistic": ks_res["statistic"],
                "ks_p_value": ks_res["p_value"],
                "ks_is_drift": ks_res["is_drift"],
                "wasserstein_distance": w_dist,
                "ref_mean": float(np.round(np.mean(ref_vals), 4)),
                "curr_mean": float(np.round(np.mean(curr_vals), 4)),
                "ref_std": float(np.round(np.std(ref_vals), 4)),
                "curr_std": float(np.round(np.std(curr_vals), 4)),
            }
            psi_scores.append(psi)
            statuses.append(status)

        # Aggregate summary
        mean_psi = float(np.round(np.mean(psi_scores), 4)) if psi_scores else 0.0
        max_psi = float(np.round(np.max(psi_scores), 4)) if psi_scores else 0.0
        worst_feature = (
            max(results.keys(), key=lambda k: results[k]["psi"]) if results else None
        )

        overall_status = "STABLE"
        if "CRITICAL_DRIFT" in statuses:
            overall_status = "CRITICAL_DRIFT"
        elif "WARNING" in statuses:
            overall_status = "WARNING"

        return {
            "features": results,
            "summary": {
                "mean_psi": mean_psi,
                "max_psi": max_psi,
                "worst_feature": worst_feature,
                "overall_status": overall_status,
                "drifted_features_count": sum(1 for s in statuses if s != "STABLE"),
                "total_features_evaluated": len(results),
            },
        }

    def compute_rolling_performance(
        self,
        y_true: Union[np.ndarray, pd.Series, List[int]],
        y_prob: Union[np.ndarray, pd.Series, List[float]],
        baseline_pr_auc: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Compute rolling classification performance and detect concept decay."""
        baseline = baseline_pr_auc if baseline_pr_auc is not None else self.baseline_pr_auc
        yt = np.asarray(y_true, dtype=int)
        yp = np.asarray(y_prob, dtype=float)

        mask = np.isfinite(yt) & np.isfinite(yp)
        yt = yt[mask]
        yp = yp[mask]

        if len(yt) < 10 or len(np.unique(yt)) < 2:
            return {
                "pr_auc": None,
                "roc_auc": None,
                "f1_score": None,
                "brier_score": None,
                "baseline_pr_auc": baseline,
                "drop_pct": 0.0,
                "concept_drift_alert": False,
                "sample_size": len(yt),
                "reason": "Insufficient sample size or single-class window",
            }

        # Compute PR-AUC
        precision, recall, _ = precision_recall_curve(yt, yp)
        curr_pr_auc = float(np.round(auc(recall, precision), 4))

        # Binary predictions at standard 0.5 threshold
        y_pred = (yp >= 0.5).astype(int)
        curr_f1 = float(np.round(f1_score(yt, y_pred, zero_division=0), 4))

        # Brier Score (lower is better calibrated)
        brier = float(np.round(brier_score_loss(yt, yp), 4))

        # Relative drop from baseline
        drop_pct = float(np.round((baseline - curr_pr_auc) / (baseline + 1e-6), 4))
        # Alert triggers if performance decays by > 8%
        alert = bool(drop_pct > 0.08)

        return {
            "pr_auc": curr_pr_auc,
            "f1_score": curr_f1,
            "brier_score": brier,
            "baseline_pr_auc": baseline,
            "drop_pct": drop_pct,
            "concept_drift_alert": alert,
            "sample_size": len(yt),
            "positive_class_rate": float(np.round(np.mean(yt), 4)),
        }
