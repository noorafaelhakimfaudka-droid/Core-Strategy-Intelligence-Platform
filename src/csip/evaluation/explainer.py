"""CSIP Model Evaluation & Explainability Module (G7 & Competency Lab).

SKKNI Compliance:
- [UK-10 Mengevaluasi Model]: Analisis performa mendalam, kalibrasi probabilitas (Brier score, ECE),
  dan validasi diagnostik out-of-time.
- Modul Kompetensi 16: Model Explainability menggunakan SHAP (SHapley Additive exPlanations)
  dan Reliability Diagrams.

Claim Governance:
- SHAP values & Tree Feature Importances are Level L1 (Predictive) / L2 (Associational).
- They represent model-internal attribution and associative relevance, NOT Level L3 Causal mechanisms.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss

logger = logging.getLogger(__name__)


def compute_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error (ECE)."""
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n_samples = len(y_true)

    for i in range(n_bins):
        bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
        if i == n_bins - 1:
            bin_mask = (y_prob >= bin_edges[i]) & (y_prob <= bin_edges[i + 1])

        bin_count = np.sum(bin_mask)
        if bin_count > 0:
            bin_acc = np.mean(y_true[bin_mask])
            bin_conf = np.mean(y_prob[bin_mask])
            ece += (bin_count / n_samples) * abs(bin_acc - bin_conf)

    return float(ece)


class ModelExplainer:
    """Generates SHAP attributions and probability calibration diagnostics."""

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state

    def explain_tree_pipeline(
        self,
        pipeline: Any,
        x_data: pd.DataFrame,
        sample_size: int = 800,
        output_fig_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Compute SHAP values using TreeExplainer on a trained scikit-learn Pipeline.

        Parameters
        ----------
        pipeline : sklearn.pipeline.Pipeline
            Fitted pipeline containing a preprocessor and a tree model (e.g. LightGBM).
        x_data : pd.DataFrame
            Feature matrix to sample from for explanation.
        sample_size : int
            Number of samples to explain (kept <= 1000 for sub-second execution on 8 GB RAM).
        output_fig_path : str or Path, optional
            Path to save the summary plot figure.
        """
        # Sample data
        if len(x_data) > sample_size:
            x_sample = x_data.sample(n=sample_size, random_state=self.random_state)
        else:
            x_sample = x_data.copy()

        # Extract preprocessor and model from pipeline
        if hasattr(pipeline, "named_steps"):
            if "preprocessor" in pipeline.named_steps:
                preprocessor = pipeline.named_steps["preprocessor"]
                x_trans = preprocessor.transform(x_sample)
                if hasattr(x_trans, "toarray"):
                    x_trans = x_trans.toarray()
                if hasattr(preprocessor, "get_feature_names_out"):
                    feature_names = [f.split("__")[-1] for f in preprocessor.get_feature_names_out()]
                else:
                    feature_names = [f"f_{i}" for i in range(x_trans.shape[1])]
            else:
                x_trans = np.asarray(x_sample)
                feature_names = list(x_sample.columns) if hasattr(x_sample, "columns") else [f"f_{i}" for i in range(x_trans.shape[1])]

            # Find estimator (last step or named 'clf' / 'model')
            if "clf" in pipeline.named_steps:
                model = pipeline.named_steps["clf"]
            elif "model" in pipeline.named_steps:
                model = pipeline.named_steps["model"]
            else:
                model = list(pipeline.named_steps.values())[-1]
        else:
            model = pipeline
            x_trans = np.asarray(x_sample)
            feature_names = list(x_sample.columns) if hasattr(x_sample, "columns") else [f"f_{i}" for i in range(x_trans.shape[1])]

        # SHAP TreeExplainer
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(x_trans)

        # For binary classification, TreeExplainer might return a list of 2 arrays or a single array
        if isinstance(shap_values, list):
            # Binary classification positive class
            shap_matrix = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
            shap_matrix = shap_values[:, :, 1]
        else:
            shap_matrix = shap_values

        # Mean absolute SHAP values per feature
        mean_abs_shap = np.mean(np.abs(shap_matrix), axis=0)
        sorted_indices = np.argsort(mean_abs_shap)[::-1]

        rankings = []
        for rank, idx in enumerate(sorted_indices, start=1):
            rankings.append({
                "rank": rank,
                "feature": feature_names[idx],
                "mean_abs_shap": float(mean_abs_shap[idx]),
            })

        # Generate and save figure if requested
        if output_fig_path is not None:
            fig_path = Path(output_fig_path)
            fig_path.parent.mkdir(parents=True, exist_ok=True)

            plt.figure(figsize=(10, 6))
            shap.summary_plot(
                shap_matrix,
                x_trans,
                feature_names=feature_names,
                max_display=12,
                show=False,
            )
            plt.title("SHAP Feature Attribution (TreeExplainer) - Level L1/L2 Associational Evidence", fontsize=12, pad=15)
            plt.tight_layout()
            plt.savefig(fig_path, dpi=150)
            plt.close()
            logger.info(f"Saved SHAP summary plot to {fig_path}")

        return {
            "num_samples_explained": len(x_sample),
            "top_features": rankings[:15],
            "evidence_grade": "Grade A",
            "claim_level": "Level L1 (Predictive) / L2 (Associational)",
        }

    def evaluate_and_calibrate(
        self,
        y_val_true: np.ndarray,
        y_val_prob: np.ndarray,
        y_test_true: np.ndarray,
        y_test_prob: np.ndarray,
        output_fig_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Perform probability calibration analysis (Platt scaling & reliability diagram).

        Evaluates raw uncalibrated probabilities against calibrated probabilities on locked test set.
        """
        # Fit Platt scaler (logistic regression on log-odds or probabilities)
        from sklearn.linear_model import LogisticRegression

        # Train calibrator on validation predictions
        # Using log-odds (logit) to avoid saturation
        eps = 1e-6
        clipped_val_prob = np.clip(y_val_prob, eps, 1.0 - eps)
        val_logits = np.log(clipped_val_prob / (1.0 - clipped_val_prob)).reshape(-1, 1)

        calibrator = LogisticRegression(C=1.0, solver="lbfgs")
        calibrator.fit(val_logits, y_val_true)

        # Transform locked test set
        clipped_test_prob = np.clip(y_test_prob, eps, 1.0 - eps)
        test_logits = np.log(clipped_test_prob / (1.0 - clipped_test_prob)).reshape(-1, 1)
        y_test_prob_calibrated = calibrator.predict_proba(test_logits)[:, 1]

        # Calculate metrics
        uncal_brier = float(brier_score_loss(y_test_true, y_test_prob))
        cal_brier = float(brier_score_loss(y_test_true, y_test_prob_calibrated))
        uncal_ece = compute_ece(y_test_true, y_test_prob, n_bins=10)
        cal_ece = compute_ece(y_test_true, y_test_prob_calibrated, n_bins=10)

        brier_improvement_pct = float(((uncal_brier - cal_brier) / uncal_brier) * 100)
        ece_improvement_pct = float(((uncal_ece - cal_ece) / uncal_ece) * 100) if uncal_ece > 0 else 0.0

        # Compute calibration curves
        prob_true_uncal, prob_pred_uncal = calibration_curve(y_test_true, y_test_prob, n_bins=10)
        prob_true_cal, prob_pred_cal = calibration_curve(y_test_true, y_test_prob_calibrated, n_bins=10)

        # Generate plot
        if output_fig_path is not None:
            fig_path = Path(output_fig_path)
            fig_path.parent.mkdir(parents=True, exist_ok=True)

            plt.figure(figsize=(8, 6))
            plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
            plt.plot(
                prob_pred_uncal,
                prob_true_uncal,
                "s-",
                color="#e74c3c",
                label=f"Raw Model (Brier={uncal_brier:.4f}, ECE={uncal_ece:.4f})",
            )
            plt.plot(
                prob_pred_cal,
                prob_true_cal,
                "o-",
                color="#2ecc71",
                label=f"Platt Calibrated (Brier={cal_brier:.4f}, ECE={cal_ece:.4f})",
            )
            plt.xlabel("Predicted Probability")
            plt.ylabel("Observed Frequency")
            plt.title("Reliability Diagram: Out-of-Time Test Set Calibration", fontsize=12)
            plt.legend(loc="upper left")
            plt.grid(True, linestyle=":", alpha=0.6)
            plt.tight_layout()
            plt.savefig(fig_path, dpi=150)
            plt.close()
            logger.info(f"Saved calibration curve plot to {fig_path}")

        return {
            "uncalibrated_brier": uncal_brier,
            "calibrated_brier": cal_brier,
            "brier_improvement_pct": brier_improvement_pct,
            "uncalibrated_ece": uncal_ece,
            "calibrated_ece": cal_ece,
            "ece_improvement_pct": ece_improvement_pct,
            "calibrator_params": {
                "coef": float(calibrator.coef_[0][0]),
                "intercept": float(calibrator.intercept_[0]),
            },
        }
