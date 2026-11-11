"""CSIP Model Experiment Trainer & Leaderboard Generator.

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Matriks eksperimen E0-E6 & temporal split.
- [UK-09 Membangun Model]: Pelatihan model supervised learning B0-B3.
- [UK-10 Mengevaluasi Hasil Pemodelan]: Evaluasi PR-AUC, ROC-AUC, Brier score, MAE, RMSE.

Strictly enforces Split-Before-Transform and Zero Data Leakage.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    auc,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    f1_score,
    mean_absolute_error,
    precision_recall_curve,
    r2_score,
    roc_auc_score,
    root_mean_squared_error,
)

from csip.models.classic import get_model_pipeline

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [CSIP-TRAINER] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class ModelEvaluationRecord:
    """Standardized performance metrics container for a trained model."""
    experiment_id: str
    model_name: str
    target_name: str
    feature_set_name: str
    split_name: str  # "validation" or "test"
    metrics: Dict[str, float]
    train_samples: int
    eval_samples: int


class ModelExperimentTrainer:
    """Orchestrates Supervised ML Experiments across Baseline Ladder B0 - B3."""

    FEATURE_SETS = {
        "E1_early_warning_checkout": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "seller_buyer_distance_km",
            "estimated_lead_time_days",
            "distance_x_weight",
            "prior_order_count",
        ],
        "E1_economic_only": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
        ],
        "E2_experience_only": [
            "delivery_lead_time_days",
            "estimated_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "approval_lag_hours",
            "seller_buyer_distance_km",
        ],
        "E2_post_delivery_diagnostic": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "seller_buyer_distance_km",
            "estimated_lead_time_days",
            "distance_x_weight",
            "approval_lag_hours",
            "prior_order_count",
            "delivery_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "delay_x_freight_ratio",
            "high_value_late_flag",
        ],
        "E3_combined_interactions": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "delivery_lead_time_days",
            "estimated_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "approval_lag_hours",
            "seller_buyer_distance_km",
            "delay_x_freight_ratio",
            "distance_x_weight",
            "high_value_late_flag",
        ],
    }

    def __init__(
        self,
        order_level_path: Union[str, Path] = "data/processed/order_level_clustered.parquet",
        customer_cohort_path: Union[str, Path] = "data/processed/customer_cohort.parquet",
        artifacts_dir: Union[str, Path] = "artifacts/models",
        reports_dir: Union[str, Path] = "artifacts/reports",
        random_state: int = 42,
    ) -> None:
        self.order_level_path = Path(order_level_path)
        self.customer_cohort_path = Path(customer_cohort_path)
        self.artifacts_dir = Path(artifacts_dir)
        self.reports_dir = Path(reports_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.random_state = random_state

        self.leaderboard: List[ModelEvaluationRecord] = []
        self.trained_models: Dict[str, Any] = {}

    def get_temporal_splits(
        self,
        df: pd.DataFrame,
        train_end: str = "2018-03-31",
        val_end: str = "2018-06-30",
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split DataFrame strictly by order_purchase_timestamp into Train, Val, and Locked Test."""
        train_mask = df["order_purchase_timestamp"] <= train_end
        val_mask = (df["order_purchase_timestamp"] > train_end) & (
            df["order_purchase_timestamp"] <= val_end
        )
        test_mask = df["order_purchase_timestamp"] > val_end

        return df[train_mask].copy(), df[val_mask].copy(), df[test_mask].copy()

    def train_evaluate_classifier(
        self,
        model_key: str,
        features: List[str],
        train_df: pd.DataFrame,
        eval_df: pd.DataFrame,
        target_col: str,
        experiment_id: str,
        feature_set_name: str,
        split_name: str = "validation",
    ) -> ModelEvaluationRecord:
        """Fit a classification model and compute comprehensive evaluation metrics."""
        X_train = train_df[features].fillna(0).values
        y_train = train_df[target_col].values

        X_eval = eval_df[features].fillna(0).values
        y_eval = eval_df[target_col].values

        pipeline = get_model_pipeline(
            model_key=model_key,
            problem_type="classification",
            random_state=self.random_state,
        )

        pipeline.fit(X_train, y_train)

        # Predictions & Probabilities
        preds = pipeline.predict(X_eval)
        probs = pipeline.predict_proba(X_eval)[:, 1] if hasattr(pipeline, "predict_proba") else preds.astype(float)

        # Clip probabilities for Brier score safety
        probs = np.clip(probs, 0.0, 1.0)

        # Compute Metrics (Standard Average Precision & ROC-AUC)
        roc = float(roc_auc_score(y_eval, probs)) if len(np.unique(y_eval)) > 1 else 0.5
        pr_auc = float(average_precision_score(y_eval, probs)) if len(np.unique(y_eval)) > 1 else 0.0
        f1 = float(f1_score(y_eval, preds, zero_division=0))
        brier = float(brier_score_loss(y_eval, probs))
        bal_acc = float(balanced_accuracy_score(y_eval, preds))

        rec_obj = ModelEvaluationRecord(
            experiment_id=experiment_id,
            model_name=model_key,
            target_name=target_col,
            feature_set_name=feature_set_name,
            split_name=split_name,
            metrics={
                "pr_auc": round(pr_auc, 4),
                "roc_auc": round(roc, 4),
                "f1_score": round(f1, 4),
                "brier_score": round(brier, 4),
                "balanced_accuracy": round(bal_acc, 4),
            },
            train_samples=len(X_train),
            eval_samples=len(X_eval),
        )

        self.leaderboard.append(rec_obj)
        model_save_key = f"{target_col}_{model_key}_{feature_set_name}"
        self.trained_models[model_save_key] = pipeline

        return rec_obj

    def train_evaluate_regressor(
        self,
        model_key: str,
        features: List[str],
        train_df: pd.DataFrame,
        eval_df: pd.DataFrame,
        target_col: str,
        experiment_id: str,
        feature_set_name: str,
        split_name: str = "validation",
    ) -> ModelEvaluationRecord:
        """Fit a regression model and compute MAE, RMSE, and R2."""
        X_train = train_df[features].fillna(0).values
        y_train = train_df[target_col].values

        X_eval = eval_df[features].fillna(0).values
        y_eval = eval_df[target_col].values

        pipeline = get_model_pipeline(
            model_key=model_key,
            problem_type="regression",
            random_state=self.random_state,
        )

        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_eval)

        mae = float(mean_absolute_error(y_eval, preds))
        rmse = float(root_mean_squared_error(y_eval, preds))
        r2 = float(r2_score(y_eval, preds))

        rec_obj = ModelEvaluationRecord(
            experiment_id=experiment_id,
            model_name=model_key,
            target_name=target_col,
            feature_set_name=feature_set_name,
            split_name=split_name,
            metrics={
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
                "r2": round(r2, 4),
            },
            train_samples=len(X_train),
            eval_samples=len(X_eval),
        )

        self.leaderboard.append(rec_obj)
        model_save_key = f"{target_col}_{model_key}_{feature_set_name}"
        self.trained_models[model_save_key] = pipeline

        return rec_obj

    def run_all_experiments(self) -> pd.DataFrame:
        """Execute full matrix of experiments across classification and regression targets."""
        logger.info("Executing Full Supervised ML & Competency Lab Experiments (B0 - B3)...")

        orders_df = pd.read_parquet(self.order_level_path)
        cohort_df = pd.read_parquet(self.customer_cohort_path)

        train_ord, val_ord, test_ord = self.get_temporal_splits(
            orders_df, train_end="2018-03-31", val_end="2018-06-30"
        )
        train_coh, val_coh, test_coh = self.get_temporal_splits(
            cohort_df, train_end="2017-12-31", val_end="2018-03-31"
        )

        logger.info(
            "Temporal Splits Orders: Train=%d, Val=%d, Test=%d",
            len(train_ord),
            len(val_ord),
            len(test_ord),
        )

        # -------------------------------------------------------------
        # 1. Target: Negative Review Risk (Order-Level)
        # -------------------------------------------------------------
        target_review = "negative_review_flag"
        
        # Target Population Clean Filtering (Finding F-02: Zero Target Contamination)
        # Supervised review learning strictly requires observed review labels
        if "has_observed_review" in train_ord.columns:
            train_rev = train_ord[train_ord["has_observed_review"] == 1].copy()
            val_rev = val_ord[val_ord["has_observed_review"] == 1].copy()
            test_rev = test_ord[test_ord["has_observed_review"] == 1].copy()
        else:
            train_rev = train_ord.dropna(subset=[target_review]).copy()
            val_rev = val_ord.dropna(subset=[target_review]).copy()
            test_rev = test_ord.dropna(subset=[target_review]).copy()

        train_rev[target_review] = train_rev[target_review].astype(int)
        val_rev[target_review] = val_rev[target_review].astype(int)
        test_rev[target_review] = test_rev[target_review].astype(int)

        clf_models = [
            "B0_naive_majority",
            "B0_naive_heuristic",
            "B1_logistic",
            "B2_decision_tree",
            "B2_knn",
            "B2_naive_bayes",
            "B3_random_forest",
            "B3_lightgbm",
        ]

        # E0 - Naive Baselines
        self.train_evaluate_classifier(
            "B0_naive_majority",
            ["total_order_value"],
            train_rev,
            val_rev,
            target_review,
            "E0",
            "naive",
        )
        self.train_evaluate_classifier(
            "B0_naive_heuristic",
            ["delivery_delay_days"],
            train_rev,
            val_rev,
            target_review,
            "E0",
            "heuristic_delay",
        )

        # Task A: Early-Warning Pre-Fulfillment Models (Zero Post-Outcome Leakage)
        self.train_evaluate_classifier(
            "B1_logistic",
            self.FEATURE_SETS["E1_early_warning_checkout"],
            train_rev,
            val_rev,
            target_review,
            "E1_early_warning",
            "E1_early_warning_checkout",
            split_name="validation",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E1_early_warning_checkout"],
            train_rev,
            val_rev,
            target_review,
            "E1_early_warning",
            "E1_early_warning_checkout",
            split_name="validation",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E1_early_warning_checkout"],
            train_rev,
            test_rev,
            target_review,
            "E1_early_warning",
            "E1_early_warning_checkout",
            split_name="test",
        )

        # E1 - Economic Only (LogReg & LightGBM)
        self.train_evaluate_classifier(
            "B1_logistic",
            self.FEATURE_SETS["E1_economic_only"],
            train_rev,
            val_rev,
            target_review,
            "E1",
            "E1_economic_only",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E1_economic_only"],
            train_rev,
            val_rev,
            target_review,
            "E1",
            "E1_economic_only",
        )

        # E2 - Experience Only
        self.train_evaluate_classifier(
            "B1_logistic",
            self.FEATURE_SETS["E2_experience_only"],
            train_rev,
            val_rev,
            target_review,
            "E2",
            "E2_experience_only",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E2_experience_only"],
            train_rev,
            val_rev,
            target_review,
            "E2",
            "E2_experience_only",
        )

        # Task B: Post-Delivery Fulfillment & Experience Diagnostic Modeling
        # Combined + Competency Lab (All B1 - B3) on Validation & Locked Holdout Test Set
        for m_key in [
            "B1_logistic",
            "B2_decision_tree",
            "B2_knn",
            "B2_naive_bayes",
            "B3_random_forest",
            "B3_lightgbm",
        ]:
            exp_id = "E6" if "B2" in m_key else "E3"
            self.train_evaluate_classifier(
                m_key,
                self.FEATURE_SETS["E3_combined_interactions"],
                train_rev,
                val_rev,
                target_review,
                exp_id,
                "E3_combined_interactions",
                split_name="validation",
            )
            # Evaluate on Locked Holdout Test Set
            self.train_evaluate_classifier(
                m_key,
                self.FEATURE_SETS["E3_combined_interactions"],
                train_rev,
                test_rev,
                target_review,
                exp_id,
                "E3_combined_interactions",
                split_name="test",
            )

        # -------------------------------------------------------------
        # 2. Target: Repeat Purchase Prediction (Customer Cohort)
        # -------------------------------------------------------------
        target_repeat = "repeat_purchase_flag"
        cohort_features = [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "seller_buyer_distance_km",
            "delivery_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "review_score",
            "has_review_comment",
        ]

        self.train_evaluate_classifier(
            "B0_naive_majority",
            ["total_order_value"],
            train_coh,
            val_coh,
            target_repeat,
            "E0",
            "naive",
        )
        self.train_evaluate_classifier(
            "B1_logistic",
            cohort_features,
            train_coh,
            val_coh,
            target_repeat,
            "E3",
            "first_order_features",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            cohort_features,
            train_coh,
            val_coh,
            target_repeat,
            "E3",
            "first_order_features",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            cohort_features,
            train_coh,
            test_coh,
            target_repeat,
            "E3",
            "first_order_features",
            split_name="test",
        )

        # -------------------------------------------------------------
        # 3. Target: Delivery Delay Estimation (Regression)
        # -------------------------------------------------------------
        target_delay = "delivery_delay_days"
        reg_features = [
            "total_order_value",
            "freight_ratio",
            "estimated_lead_time_days",
            "seller_buyer_distance_km",
            "approval_lag_hours",
        ]

        reg_models = [
            "B0_naive_mean",
            "B1_ridge",
            "B2_decision_tree",
            "B3_random_forest",
            "B3_lightgbm",
        ]
        for r_key in reg_models:
            self.train_evaluate_regressor(
                r_key,
                reg_features,
                train_ord,
                val_ord,
                target_delay,
                "E3",
                "logistics_features",
                split_name="validation",
            )
            if r_key in ["B1_ridge", "B3_lightgbm"]:
                self.train_evaluate_regressor(
                    r_key,
                    reg_features,
                    train_ord,
                    test_ord,
                    target_delay,
                    "E3",
                    "logistics_features",
                    split_name="test",
                )

        # Compile Leaderboard DataFrame
        records = []
        for r in self.leaderboard:
            row = asdict(r)
            m = row.pop("metrics")
            row.update(m)
            records.append(row)

        leaderboard_df = pd.DataFrame(records)

        # Save artifacts
        self.save_artifacts(leaderboard_df)
        return leaderboard_df

    def save_artifacts(self, leaderboard_df: pd.DataFrame) -> None:
        """Persist leaderboard JSON and top production model pipelines."""
        board_path = self.reports_dir / "ml_leaderboard.json"
        with open(board_path, "w", encoding="utf-8") as f:
            json.dump(leaderboard_df.to_dict(orient="records"), f, indent=2)

        # Save primary production models (LightGBM champions)
        best_early_warning = self.trained_models.get(
            "negative_review_flag_B3_lightgbm_E1_early_warning_checkout"
        )
        if best_early_warning:
            joblib.dump(
                best_early_warning,
                self.artifacts_dir / "best_early_warning_review_lightgbm.joblib",
            )

        best_review_model = self.trained_models.get(
            "negative_review_flag_B3_lightgbm_E3_combined_interactions"
        )
        if best_review_model:
            joblib.dump(
                best_review_model,
                self.artifacts_dir / "best_negative_review_lightgbm.joblib",
            )

        best_repeat_model = self.trained_models.get(
            "repeat_purchase_flag_B3_lightgbm_first_order_features"
        )
        if best_repeat_model:
            joblib.dump(
                best_repeat_model,
                self.artifacts_dir / "best_repeat_purchase_lightgbm.joblib",
            )

        best_delay_model = self.trained_models.get(
            "delivery_delay_days_B3_lightgbm_logistics_features"
        )
        if best_delay_model:
            joblib.dump(
                best_delay_model,
                self.artifacts_dir / "best_delivery_delay_lightgbm.joblib",
            )

        logger.info("Saved ML Leaderboard to %s and Champion models to %s", board_path, self.artifacts_dir)
