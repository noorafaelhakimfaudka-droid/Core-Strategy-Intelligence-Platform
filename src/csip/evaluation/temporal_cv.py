"""Rolling-Origin Temporal Cross-Validation & Out-of-Time Evaluation Engine.

Provides:
1. RollingOriginTemporalCV: Expanding-window time-series CV with mandatory embargo (>= 90 days).
   Enforces: max(ts_train) + embargo_days < min(ts_val).
2. TemporalFoldEvaluator: Evaluates classification and regression models across folds.
   Extracts metrics per fold, aggregated mean/std, and block bootstrap confidence intervals.
3. Locked Test Set Protection: Tracks final_locked_test_reported_once flag to ensure
   locked test evaluation is reported exactly once for final reporting without leakage.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    mean_absolute_error,
    precision_recall_curve,
    roc_auc_score,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@dataclass
class TemporalFold:
    fold_idx: int
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    embargo_days: int
    val_start: pd.Timestamp
    val_end: pd.Timestamp
    n_train: int = 0
    n_val: int = 0

    def validate_embargo(self) -> bool:
        """Assert that validation period strictly starts after train_end + embargo_days."""
        min_allowed_val = self.train_end + pd.Timedelta(days=self.embargo_days)
        return self.val_start >= min_allowed_val


class RollingOriginTemporalCV:
    """Expanding-window rolling-origin cross-validation with temporal embargo."""

    def __init__(
        self,
        n_folds: int = 4,
        embargo_days: int = 90,
        min_train_days: int = 180,
        val_window_days: int = 45,
        test_start_date: str = "2018-07-01",
        time_col: str = "order_purchase_timestamp",
    ):
        self.n_folds = max(4, n_folds)
        self.embargo_days = max(90, embargo_days)
        self.min_train_days = min_train_days
        self.val_window_days = val_window_days
        self.test_start_date = pd.to_datetime(test_start_date)
        self.time_col = time_col

    def get_folds(self, df: pd.DataFrame) -> List[TemporalFold]:
        """Generate expanding-window temporal folds."""
        ts = pd.to_datetime(df[self.time_col])
        t_min = ts.min()
        t_max_cv = self.test_start_date

        available_cv_days = (t_max_cv - t_min).days
        required_minimum = self.min_train_days + self.embargo_days + self.val_window_days
        if available_cv_days < required_minimum:
            raise ValueError(
                f"Insufficient temporal span for CV: available {available_cv_days} days, "
                f"need at least {required_minimum} days."
            )

        # Distribute train expansions
        # Last fold validation ends at t_max_cv
        # Fold k val_end = t_max_cv - (n_folds - 1 - k) * step_days
        last_val_end = t_max_cv
        last_val_start = last_val_end - pd.Timedelta(days=self.val_window_days)
        last_train_end = last_val_start - pd.Timedelta(days=self.embargo_days + 1)
        
        first_train_end = t_min + pd.Timedelta(days=self.min_train_days)
        
        train_endpoints = pd.date_range(first_train_end, last_train_end, periods=self.n_folds)

        folds = []
        for i, tr_end in enumerate(train_endpoints):
            val_start = tr_end + pd.Timedelta(days=self.embargo_days + 1)
            val_end = val_start + pd.Timedelta(days=self.val_window_days)
            if val_end > self.test_start_date:
                val_end = self.test_start_date

            train_mask = (ts >= t_min) & (ts <= tr_end)
            val_mask = (ts >= val_start) & (ts <= val_end)

            fold = TemporalFold(
                fold_idx=i + 1,
                train_start=t_min,
                train_end=tr_end,
                embargo_days=self.embargo_days,
                val_start=val_start,
                val_end=val_end,
                n_train=int(train_mask.sum()),
                n_val=int(val_mask.sum()),
            )
            assert fold.validate_embargo(), f"Fold {i+1} violates embargo constraint!"
            folds.append(fold)

        return folds

    def split(
        self, df: pd.DataFrame
    ) -> Generator[Tuple[np.ndarray, np.ndarray, TemporalFold], None, None]:
        """Yields (train_indices, val_indices, fold) for each temporal fold."""
        ts = pd.to_datetime(df[self.time_col]).values
        folds = self.get_folds(df)

        for fold in folds:
            train_idx = np.where((ts >= fold.train_start) & (ts <= fold.train_end))[0]
            val_idx = np.where((ts >= fold.val_start) & (ts <= fold.val_end))[0]
            yield train_idx, val_idx, fold


def compute_block_bootstrap_ci(
    values: np.ndarray,
    n_bootstraps: int = 1000,
    block_size: int = 5,
    ci_level: float = 0.95,
    seed: int = 42,
) -> Tuple[float, float]:
    """Computes moving-block bootstrap confidence intervals for temporal metric sequences."""
    rng = np.random.default_rng(seed)
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    if n < block_size:
        block_size = max(1, n // 2)

    boot_means = []
    n_blocks = int(np.ceil(n / block_size))
    for _ in range(n_bootstraps):
        start_indices = rng.integers(0, max(1, n - block_size + 1), size=n_blocks)
        sample = np.concatenate([values[s : s + block_size] for s in start_indices])[:n]
        boot_means.append(np.mean(sample))

    alpha = (1.0 - ci_level) / 2.0
    lower = float(np.percentile(boot_means, alpha * 100))
    upper = float(np.percentile(boot_means, (1.0 - alpha) * 100))
    return lower, upper


class TemporalCVManager:
    """Manages full temporal cross-validation, selection, and single locked test evaluation."""

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.config_path = Path(config_path or REPO_ROOT / "config" / "analysis_plan.yaml")
        self.final_locked_test_reported_once: bool = False
        self.locked_test_results: Optional[Dict[str, Any]] = None

    def run_cv(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        target_col: str,
        model_factory: Callable[[], Any],
        is_classifier: bool = True,
        time_col: str = "order_purchase_timestamp",
        n_folds: int = 4,
        embargo_days: int = 90,
    ) -> Dict[str, Any]:
        """Runs rolling-origin temporal CV across all folds without touching locked test set."""
        cv = RollingOriginTemporalCV(
            n_folds=n_folds,
            embargo_days=embargo_days,
            time_col=time_col,
        )

        fold_reports = []
        val_predictions = []
        all_metrics = {"pr_auc": [], "roc_auc": [], "brier": [], "mae": []}

        for tr_idx, val_idx, fold in cv.split(df):
            X_tr = df.iloc[tr_idx][feature_cols]
            y_tr = df.iloc[tr_idx][target_col].values
            X_val = df.iloc[val_idx][feature_cols]
            y_val = df.iloc[val_idx][target_col].values

            # Fit model strictly on train fold
            model = model_factory()
            model.fit(X_tr, y_tr)

            fold_metric = {
                "fold": fold.fold_idx,
                "train_span": f"{fold.train_start.date()} to {fold.train_end.date()}",
                "val_span": f"{fold.val_start.date()} to {fold.val_end.date()}",
                "embargo_days": fold.embargo_days,
                "n_train": len(tr_idx),
                "n_val": len(val_idx),
            }

            if is_classifier:
                y_prob = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_val)
                pr_auc = float(average_precision_score(y_val, y_prob)) if len(np.unique(y_val)) > 1 else 0.0
                roc_auc = float(roc_auc_score(y_val, y_prob)) if len(np.unique(y_val)) > 1 else 0.5
                brier = float(brier_score_loss(y_val, y_prob))
                base_rate = float(np.mean(y_val))

                # Optimal threshold strictly from validation PR curve (Youden or F1 max)
                precisions, recalls, thresholds = precision_recall_curve(y_val, y_prob)
                f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
                best_idx = np.argmax(f1_scores[:-1]) if len(f1_scores) > 1 else 0
                optimal_threshold = float(thresholds[best_idx]) if len(thresholds) > 0 else 0.5

                fold_metric.update({
                    "pr_auc": round(pr_auc, 4),
                    "roc_auc": round(roc_auc, 4),
                    "brier_score": round(brier, 4),
                    "base_rate": round(base_rate, 4),
                    "optimal_threshold": round(optimal_threshold, 4),
                })
                all_metrics["pr_auc"].append(pr_auc)
                all_metrics["roc_auc"].append(roc_auc)
                all_metrics["brier"].append(brier)
            else:
                preds = model.predict(X_val)
                mae = float(mean_absolute_error(y_val, preds))
                fold_metric.update({"mae": round(mae, 4)})
                all_metrics["mae"].append(mae)

            fold_reports.append(fold_metric)

        # Aggregate summary with Block Bootstrap
        summary = {
            "n_folds": len(fold_reports),
            "folds": fold_reports,
        }
        if is_classifier:
            pr_array = np.array(all_metrics["pr_auc"])
            pr_ci_low, pr_ci_high = compute_block_bootstrap_ci(pr_array)
            summary["mean_pr_auc"] = round(float(np.mean(pr_array)), 4)
            summary["std_pr_auc"] = round(float(np.std(pr_array)), 4)
            summary["pr_auc_95_ci"] = [round(pr_ci_low, 4), round(pr_ci_high, 4)]

            roc_array = np.array(all_metrics["roc_auc"])
            roc_ci_low, roc_ci_high = compute_block_bootstrap_ci(roc_array)
            summary["mean_roc_auc"] = round(float(np.mean(roc_array)), 4)
            summary["roc_auc_95_ci"] = [round(roc_ci_low, 4), round(roc_ci_high, 4)]
        else:
            mae_array = np.array(all_metrics["mae"])
            mae_ci_low, mae_ci_high = compute_block_bootstrap_ci(mae_array)
            summary["mean_mae"] = round(float(np.mean(mae_array)), 4)
            summary["mae_95_ci"] = [round(mae_ci_low, 4), round(mae_ci_high, 4)]

        return summary

    def evaluate_locked_test_once(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        threshold: float = 0.5,
        is_classifier: bool = True,
    ) -> Dict[str, Any]:
        """Evaluates model on locked test set exactly once, raising error if attempted again."""
        if self.final_locked_test_reported_once:
            raise RuntimeError(
                "Violation: Final locked test set has ALREADY been evaluated and reported! "
                "Per Phase 3 rule, the locked test set cannot be evaluated iteratively."
            )

        results = {
            "evaluated_at": datetime.utcnow().isoformat(),
            "n_test": len(y_test),
            "threshold": threshold,
        }

        if is_classifier:
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_test)
            pr_auc = float(average_precision_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else 0.0
            roc_auc = float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else 0.5
            brier = float(brier_score_loss(y_test, y_prob))
            base_rate = float(np.mean(y_test))

            # Bootstrap CIs on test set
            boot_prs = []
            rng = np.random.default_rng(42)
            n_samples = len(y_test)
            for _ in range(1000):
                b_idx = rng.integers(0, n_samples, size=n_samples)
                if len(np.unique(y_test[b_idx])) > 1:
                    boot_prs.append(average_precision_score(y_test[b_idx], y_prob[b_idx]))

            pr_low = float(np.percentile(boot_prs, 2.5)) if boot_prs else pr_auc
            pr_high = float(np.percentile(boot_prs, 97.5)) if boot_prs else pr_auc

            results.update({
                "pr_auc": round(pr_auc, 4),
                "pr_auc_95_ci": [round(pr_low, 4), round(pr_high, 4)],
                "roc_auc": round(roc_auc, 4),
                "brier_score": round(brier, 4),
                "base_rate": round(base_rate, 4),
            })
        else:
            preds = model.predict(X_test)
            mae = float(mean_absolute_error(y_test, preds))
            results.update({"mae": round(mae, 4)})

        self.final_locked_test_reported_once = True
        self.locked_test_results = results
        return results

