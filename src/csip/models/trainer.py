"""CSIP Model Experiment Trainer & Leaderboard Generator.

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Matriks eksperimen E0-E6 & temporal split.
- [UK-09 Membangun Model]: Pelatihan model supervised learning B0-B3.
- [UK-10 Mengevaluasi Hasil Pemodelan]: Evaluasi PR-AUC, ROC-AUC, Brier score, MAE, RMSE.

Strictly enforces Split-Before-Transform and Temporal & Feature Isolation.
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import lightgbm
import numpy as np
import pandas as pd
import sklearn
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
    metrics_ci: Optional[Dict[str, Any]] = None


class ModelExperimentTrainer:
    """Orchestrates Supervised ML Experiments across Baseline Ladder B0 - B3."""

    FEATURE_SETS = {
        "E1_checkout_retrospective_conditional": [
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
        "cohort_checkout_features": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "seller_buyer_distance_km",
            "estimated_lead_time_days",
        ],
        "cohort_post_delivery_features": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "seller_buyer_distance_km",
            "estimated_lead_time_days",
            "delivery_lead_time_days",
            "delivery_delay_days",
            "is_late",
        ],
        "cohort_post_survey_features": [
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "payment_installments_max",
            "seller_buyer_distance_km",
            "estimated_lead_time_days",
            "delivery_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "review_score",
            "has_review_comment",
        ],
        "logistics_features": [
            "total_order_value",
            "freight_ratio",
            "estimated_lead_time_days",
            "seller_buyer_distance_km",
            "approval_lag_hours",
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

    def get_cohort_temporal_splits_with_embargo(
        self,
        cohort_df: pd.DataFrame,
        train_end: str = "2017-08-31 23:59:59",
        val_start: str = "2017-12-01",
        val_end: str = "2018-01-31 23:59:59",
        test_start: str = "2018-05-01",
        test_end: str = "2018-05-31 23:59:59",
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split cohort DataFrame strictly by order_purchase_timestamp with 90-day embargoes.
        
        Finding F-02 (P-02): Guarantees zero overlap between the 90-day outcome window of Train
        and the order placement window of Val, and likewise between Val and Test.
        """
        train_mask = cohort_df["order_purchase_timestamp"] <= train_end
        val_mask = (cohort_df["order_purchase_timestamp"] >= val_start) & (
            cohort_df["order_purchase_timestamp"] <= val_end
        )
        test_mask = (cohort_df["order_purchase_timestamp"] >= test_start) & (
            cohort_df["order_purchase_timestamp"] <= test_end
        )
        return cohort_df[train_mask].copy(), cohort_df[val_mask].copy(), cohort_df[test_mask].copy()

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

        ci_dict = None
        metrics_dict = {
            "pr_auc": round(pr_auc, 4),
            "roc_auc": round(roc, 4),
            "f1_score": round(f1, 4),
            "brier_score": round(brier, 4),
            "balanced_accuracy": round(bal_acc, 4),
        }

        # 95% Bootstrap Confidence Intervals for Holdout Test Evaluation (Auditor N-03)
        if split_name == "test" and len(np.unique(y_eval)) > 1:
            from csip.uncertainty.bootstrap import compute_classification_bootstrap_ci
            ci_dict = compute_classification_bootstrap_ci(
                y_eval, probs, n_bootstraps=500, random_state=self.random_state
            )
            if ci_dict:
                metrics_dict["roc_auc_ci_lower"] = ci_dict["roc_auc"]["ci_95"][0]
                metrics_dict["roc_auc_ci_upper"] = ci_dict["roc_auc"]["ci_95"][1]
                metrics_dict["pr_auc_ci_lower"] = ci_dict["pr_auc"]["ci_95"][0]
                metrics_dict["pr_auc_ci_upper"] = ci_dict["pr_auc"]["ci_95"][1]
                metrics_dict["brier_ci_lower"] = ci_dict["brier_score"]["ci_95"][0]
                metrics_dict["brier_ci_upper"] = ci_dict["brier_score"]["ci_95"][1]
                metrics_dict["spans_chance"] = float(ci_dict["roc_auc"]["spans_chance"])
                metrics_dict["statistically_distinguishable"] = float(ci_dict["statistically_distinguishable_from_baseline"])

        rec_obj = ModelEvaluationRecord(
            experiment_id=experiment_id,
            model_name=model_key,
            target_name=target_col,
            feature_set_name=feature_set_name,
            split_name=split_name,
            metrics=metrics_dict,
            train_samples=len(X_train),
            eval_samples=len(X_eval),
            metrics_ci=ci_dict,
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
        train_coh, val_coh, test_coh = self.get_cohort_temporal_splits_with_embargo(cohort_df)

        logger.info(
            "Temporal Splits Orders: Train=%d, Val=%d, Test=%d",
            len(train_ord),
            len(val_ord),
            len(test_ord),
        )
        logger.info(
            "Temporal Splits Cohort (90d Embargo): Train=%d, Val=%d, Test=%d",
            len(train_coh),
            len(val_coh),
            len(test_coh),
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
        # Estimand: P(Negative Review = 1 | X_checkout, Delivered = 1, Observed Review = 1)
        # Experiment and Feature Set: E1_checkout_retrospective_conditional (F-03)
        self.train_evaluate_classifier(
            "B1_logistic",
            self.FEATURE_SETS["E1_checkout_retrospective_conditional"],
            train_rev,
            val_rev,
            target_review,
            "E1_checkout_retrospective_conditional",
            "E1_checkout_retrospective_conditional",
            split_name="validation",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E1_checkout_retrospective_conditional"],
            train_rev,
            val_rev,
            target_review,
            "E1_checkout_retrospective_conditional",
            "E1_checkout_retrospective_conditional",
            split_name="validation",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            self.FEATURE_SETS["E1_checkout_retrospective_conditional"],
            train_rev,
            test_rev,
            target_review,
            "E1_checkout_retrospective_conditional",
            "E1_checkout_retrospective_conditional",
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
        # 2A. Primary Operational Contract: Checkout Stage (t <= t_order1_purchase)
        target_repeat = "repeat_purchase_flag"
        cohort_checkout_features = self.FEATURE_SETS["cohort_checkout_features"]

        # Baseline B0 (Naive Majority)
        self.train_evaluate_classifier(
            "B0_naive_majority",
            ["total_order_value"],
            train_coh,
            val_coh,
            target_repeat,
            "E0",
            "naive",
        )

        # Primary Operational Contract: Strict First-Order Checkout Features (Zero Point-in-Time Leakage, t = t_order1_purchase)
        self.train_evaluate_classifier(
            "B1_logistic",
            cohort_checkout_features,
            train_coh,
            val_coh,
            target_repeat,
            "E1",
            "first_order_checkout",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            cohort_checkout_features,
            train_coh,
            val_coh,
            target_repeat,
            "E1",
            "first_order_checkout",
        )
        self.train_evaluate_classifier(
            "B3_lightgbm",
            cohort_checkout_features,
            train_coh,
            test_coh,
            target_repeat,
            "E1",
            "first_order_checkout",
            split_name="test",
        )

        # 2B. Post-Delivery Fulfillment Contract (Finding F-01 / P-01: t = t_order1_delivered)
        # Isolates review_score and has_review_comment from delivery features
        target_post_delivery = "repeat_purchase_post_delivery_flag"
        cohort_post_delivery_features = self.FEATURE_SETS["cohort_post_delivery_features"]

        if target_post_delivery in cohort_df.columns:
            # Filter post-delivery cohort to uncensored non-pre-repeat population (Auditor N-01 & N-02)
            # 1. Exclude customers who already repeated before order 1 was delivered (repeat_before_delivery_flag == 0)
            # 2. Exclude customers right-censored post-delivery (is_censored_post_delivery == 0)
            train_coh_post = train_coh[
                (train_coh["repeat_before_delivery_flag"] == 0) & (train_coh["is_censored_post_delivery"] == 0)
            ].copy()
            val_coh_post = val_coh[
                (val_coh["repeat_before_delivery_flag"] == 0) & (val_coh["is_censored_post_delivery"] == 0)
            ].copy()
            test_coh_post = test_coh[
                (test_coh["repeat_before_delivery_flag"] == 0) & (test_coh["is_censored_post_delivery"] == 0)
            ].copy()

            logger.info(
                "Post-Delivery Filtered Cohort: Train=%d (repeaters=%d), Val=%d (repeaters=%d), Test=%d (repeaters=%d)",
                len(train_coh_post),
                int(train_coh_post[target_post_delivery].sum()),
                len(val_coh_post),
                int(val_coh_post[target_post_delivery].sum()),
                len(test_coh_post),
                int(test_coh_post[target_post_delivery].sum()),
            )

            self.train_evaluate_classifier(
                "B0_naive_majority",
                ["total_order_value"],
                train_coh_post,
                val_coh_post,
                target_post_delivery,
                "E0",
                "naive",
            )
            self.train_evaluate_classifier(
                "B1_logistic",
                cohort_post_delivery_features,
                train_coh_post,
                val_coh_post,
                target_post_delivery,
                "E1",
                "post_delivery_fulfillment",
            )
            self.train_evaluate_classifier(
                "B3_lightgbm",
                cohort_post_delivery_features,
                train_coh_post,
                val_coh_post,
                target_post_delivery,
                "E3",
                "post_delivery_fulfillment",
            )
            self.train_evaluate_classifier(
                "B3_lightgbm",
                cohort_post_delivery_features,
                train_coh_post,
                test_coh_post,
                target_post_delivery,
                "E3",
                "post_delivery_fulfillment",
                split_name="test",
            )

        # -------------------------------------------------------------
        # 3. Target: Delivery Delay Estimation (Regression)
        # -------------------------------------------------------------
        target_delay = "delivery_delay_days"
        reg_features = self.FEATURE_SETS["logistics_features"]

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
        """Persist leaderboard JSON, champion model pipelines, and companion metadata sidecars."""
        # Required production champion models configuration (Finding R-01 & R-03)
        champions_spec = {
            "best_early_warning_review_lightgbm": {
                "key": "negative_review_flag_B3_lightgbm_E1_checkout_retrospective_conditional",
                "target_name": "negative_review_flag",
                "feature_set_name": "E1_checkout_retrospective_conditional",
                "feature_list": self.FEATURE_SETS["E1_checkout_retrospective_conditional"],
                "split_bounds": {
                    "train_end": "2018-03-31",
                    "val_end": "2018-06-30",
                    "test_start": "2018-07-01",
                },
            },
            "best_negative_review_lightgbm": {
                "key": "negative_review_flag_B3_lightgbm_E3_combined_interactions",
                "target_name": "negative_review_flag",
                "feature_set_name": "E3_combined_interactions",
                "feature_list": self.FEATURE_SETS["E3_combined_interactions"],
                "split_bounds": {
                    "train_end": "2018-03-31",
                    "val_end": "2018-06-30",
                    "test_start": "2018-07-01",
                },
            },
            "best_repeat_purchase_lightgbm": {
                "key": "repeat_purchase_flag_B3_lightgbm_first_order_checkout",
                "target_name": "repeat_purchase_flag",
                "feature_set_name": "first_order_checkout",
                "feature_list": self.FEATURE_SETS["cohort_checkout_features"],
                "split_bounds": {
                    "train_end": "2017-08-31 23:59:59",
                    "val_start": "2017-12-01",
                    "val_end": "2018-01-31 23:59:59",
                    "test_start": "2018-05-01",
                    "test_end": "2018-05-31 23:59:59",
                },
            },
            "best_repeat_purchase_post_delivery_lightgbm": {
                "key": "repeat_purchase_post_delivery_flag_B3_lightgbm_post_delivery_fulfillment",
                "target_name": "repeat_purchase_post_delivery_flag",
                "feature_set_name": "post_delivery_fulfillment",
                "feature_list": self.FEATURE_SETS["cohort_post_delivery_features"],
                "split_bounds": {
                    "train_end": "2017-08-31 23:59:59",
                    "val_start": "2017-12-01",
                    "val_end": "2018-01-31 23:59:59",
                    "test_start": "2018-05-01",
                    "test_end": "2018-05-31 23:59:59",
                },
            },
            "best_delivery_delay_lightgbm": {
                "key": "delivery_delay_days_B3_lightgbm_logistics_features",
                "target_name": "delivery_delay_days",
                "feature_set_name": "logistics_features",
                "feature_list": self.FEATURE_SETS["logistics_features"],
                "split_bounds": {
                    "train_end": "2018-03-31",
                    "val_end": "2018-06-30",
                    "test_start": "2018-07-01",
                },
            },
        }

        # Validate that all required champion models are available BEFORE modifying any disk files
        for artifact_name, spec in champions_spec.items():
            model_key = spec["key"]
            if model_key not in self.trained_models:
                raise KeyError(
                    f"Champion model key '{model_key}' not found in trained models. "
                    f"Available keys: {list(self.trained_models.keys())}"
                )

        board_path = self.reports_dir / "ml_leaderboard.json"
        with open(board_path, "w", encoding="utf-8") as f:
            json.dump(leaderboard_df.to_dict(orient="records"), f, indent=2)

        # Remove deprecated/orphan diagnostic artifacts if present
        legacy_orphan = f"best_repeat_purchase_{'diagnostic'}_lightgbm.joblib"
        for orphan_name in [legacy_orphan, f"{legacy_orphan}.json"]:
            orphan_path = self.artifacts_dir / orphan_name
            if orphan_path.exists():
                orphan_path.unlink()
        for artifact_name, spec in champions_spec.items():
            model_key = spec["key"]
            if model_key not in self.trained_models:
                raise KeyError(
                    f"Champion model key '{model_key}' not found in trained models. "
                    f"Available keys: {list(self.trained_models.keys())}"
                )

            model_obj = self.trained_models[model_key]
            joblib_path = self.artifacts_dir / f"{artifact_name}.joblib"
            joblib.dump(model_obj, joblib_path)

            # Determine train rows from leaderboard records
            train_rows = 0
            for r in self.leaderboard:
                if (
                    r.target_name == spec["target_name"]
                    and r.feature_set_name == spec["feature_set_name"]
                    and r.model_name == "B3_lightgbm"
                ):
                    train_rows = r.train_samples
                    break

            sidecar_data = {
                "target_name": spec["target_name"],
                "feature_set_name": spec["feature_set_name"],
                "feature_list": spec["feature_list"],
                "train_rows": train_rows,
                "split_bounds": spec["split_bounds"],
                "sklearn_version": sklearn.__version__,
                "lightgbm_version": lightgbm.__version__,
                "python_version": sys.version.split()[0],
                "trained_at": datetime.now(timezone.utc).isoformat(),
                "git_or_release_version": "v13.0.0",
            }
            sidecar_path = self.artifacts_dir / f"{artifact_name}.joblib.json"
            with open(sidecar_path, "w", encoding="utf-8") as f:
                json.dump(sidecar_data, f, indent=2)

        logger.info(
            "Saved ML Leaderboard to %s and 5 Champion models + sidecar JSON metadata to %s",
            board_path,
            self.artifacts_dir,
        )
