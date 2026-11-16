"""CSIP Business Decision Engine.

High-level interface coordinating predictive inference, decision rule evaluation,
business capacity triage, and outcome measurement planning.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from csip.decision_engine.rules import DecisionRuleEvaluator
from csip.decision_engine.schemas import (
    DecisionPriority,
    DecisionRecommendation,
    DecisionRuleConfig,
    OperationalFunction,
)

logger = logging.getLogger(__name__)


class BusinessDecisionEngine:
    """Coordinates the end-to-end Decision Intelligence workflow for CSIP."""

    def __init__(self, config: Optional[DecisionRuleConfig] = None):
        self.config = config or DecisionRuleConfig()
        self.evaluator = DecisionRuleEvaluator(config=self.config)

    def generate_recommendations(
        self,
        orders_df: pd.DataFrame,
        delay_predictions: Optional[np.ndarray] = None,
        negative_review_probabilities: Optional[np.ndarray] = None,
        is_early_warning: bool = True,
    ) -> List[DecisionRecommendation]:
        """Evaluates batch of orders and produces prioritized decision recommendations."""
        n_orders = len(orders_df)
        if n_orders == 0:
            return []

        if delay_predictions is None:
            delay_predictions = np.zeros(n_orders)
        if negative_review_probabilities is None:
            negative_review_probabilities = np.zeros(n_orders)

        recommendations: List[DecisionRecommendation] = []
        for i in range(n_orders):
            row_dict = orders_df.iloc[i].to_dict()
            rec = self.evaluator.evaluate_order(
                order_data=row_dict,
                predicted_delay_days=float(delay_predictions[i]),
                predicted_negative_prob=float(negative_review_probabilities[i]),
                is_early_warning=is_early_warning,
            )
            if rec is not None:
                recommendations.append(rec)

        # Priority ordering: CRITICAL > HIGH > MEDIUM > LOW
        priority_order = {
            DecisionPriority.CRITICAL: 0,
            DecisionPriority.HIGH: 1,
            DecisionPriority.MEDIUM: 2,
            DecisionPriority.LOW: 3,
        }
        recommendations.sort(key=lambda r: priority_order.get(r.priority_level, 99))

        # Capacity enforcement
        if len(recommendations) > self.config.capacity_max_actions_per_batch:
            recommendations = recommendations[: self.config.capacity_max_actions_per_batch]

        return recommendations

    def summarize_recommendations(
        self, recommendations: List[DecisionRecommendation]
    ) -> Dict[str, Any]:
        """Provides an executive breakdown of generated recommendations."""
        priority_counts = {p.value: 0 for p in DecisionPriority}
        function_counts = {f.value: 0 for f in OperationalFunction}
        cost_tier_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        for r in recommendations:
            priority_counts[r.priority_level.value] += 1
            function_counts[r.responsible_function.value] += 1
            cost_tier_counts[r.estimated_cost_tier] = (
                cost_tier_counts.get(r.estimated_cost_tier, 0) + 1
            )

        return {
            "total_recommendations": len(recommendations),
            "priority_breakdown": priority_counts,
            "functional_ownership": function_counts,
            "cost_tier_breakdown": cost_tier_counts,
            "critical_action_count": priority_counts[DecisionPriority.CRITICAL.value],
            "high_action_count": priority_counts[DecisionPriority.HIGH.value],
        }

    def calibrate_thresholds_from_capacity(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        max_alert_rate: float = 0.10,
        min_precision: Optional[float] = None,
        apply: bool = False,
    ) -> Dict[str, Any]:
        """Derive empirical risk thresholds from validation predictions & capacity.

        Computes precision, recall, and lift at the capacity-constrained alert rate
        (or minimum precision constraint) so thresholds are grounded in observed
        model ranking performance rather than arbitrary constants.
        """
        y_t = np.asarray(y_true, dtype=int)
        y_p = np.asarray(y_prob, dtype=float)
        if len(y_t) == 0 or len(y_t) != len(y_p):
            raise ValueError("y_true and y_prob must be non-empty arrays of equal length.")
        if not (0.0 < max_alert_rate <= 1.0):
            raise ValueError("max_alert_rate must be in (0, 1].")

        base_rate = float(np.mean(y_t))
        risk_threshold = float(np.quantile(y_p, 1.0 - max_alert_rate))
        critical_rate = max(0.01, max_alert_rate / 3.0)
        critical_threshold = float(np.quantile(y_p, 1.0 - critical_rate))

        if min_precision is not None:
            # Evaluate candidate thresholds on sorted unique probabilities
            candidates = np.unique(np.round(y_p, 4))
            for thr in candidates:
                mask = y_p >= thr
                if np.sum(mask) == 0:
                    continue
                prec = float(np.mean(y_t[mask]))
                alert_r = float(np.mean(mask))
                if prec >= min_precision and alert_r <= max_alert_rate:
                    risk_threshold = float(thr)
                    break

        flagged = y_p >= risk_threshold
        n_flagged = int(np.sum(flagged))
        precision = float(np.mean(y_t[flagged])) if n_flagged > 0 else 0.0
        total_pos = int(np.sum(y_t))
        recall = float(np.sum(y_t[flagged]) / total_pos) if total_pos > 0 else 0.0
        alert_rate = float(n_flagged / len(y_t))
        lift = float(precision / base_rate) if base_rate > 0 else 0.0

        if apply:
            self.config.risk_probability_threshold = round(risk_threshold, 4)
            self.config.critical_risk_probability_threshold = round(max(critical_threshold, risk_threshold), 4)

        return {
            "recommended_risk_threshold": round(risk_threshold, 4),
            "recommended_critical_threshold": round(max(critical_threshold, risk_threshold), 4),
            "empirical_precision": round(precision, 4),
            "empirical_recall": round(recall, 4),
            "empirical_alert_rate": round(alert_rate, 4),
            "baseline_rate": round(base_rate, 4),
            "lift_over_baseline": round(lift, 3),
            "n_evaluated": int(len(y_t)),
            "applied_to_config": apply,
        }

    def design_ab_holdout_plan(
        self,
        recommendations: List[DecisionRecommendation],
        holdout_fraction: float = 0.20,
        random_seed: int = 42,
    ) -> Dict[str, Any]:
        """Partition prioritized recommendations into Treatment vs Control Holdout.

        Enables empirical causal evaluation of operational interventions instead of
        assuming recommendation impact without a counterfactual control group.
        """
        if not (0.0 < holdout_fraction < 1.0):
            raise ValueError("holdout_fraction must be between 0 and 1.")

        n_total = len(recommendations)
        if n_total == 0:
            return {
                "n_total": 0,
                "n_treatment": 0,
                "n_control_holdout": 0,
                "holdout_fraction": holdout_fraction,
                "treatment_decision_ids": [],
                "control_decision_ids": [],
                "primary_endpoint": "negative_review_flag",
                "secondary_endpoint": "delivery_delay_days",
                "evaluation_note": "No recommendations to partition.",
            }

        rng = np.random.default_rng(random_seed)
        indices = np.arange(n_total)
        rng.shuffle(indices)
        n_control = max(1, int(round(n_total * holdout_fraction))) if n_total >= 2 else 0
        control_idx = set(indices[:n_control].tolist())

        treatment_ids = [r.decision_id for i, r in enumerate(recommendations) if i not in control_idx]
        control_ids = [r.decision_id for i, r in enumerate(recommendations) if i in control_idx]

        return {
            "n_total": n_total,
            "n_treatment": len(treatment_ids),
            "n_control_holdout": len(control_ids),
            "holdout_fraction": holdout_fraction,
            "treatment_decision_ids": treatment_ids,
            "control_decision_ids": control_ids,
            "primary_endpoint": "negative_review_flag",
            "secondary_endpoint": "delivery_delay_days",
            "evaluation_note": (
                "Randomized holdout design: withhold proactive intervention on control_decision_ids "
                "and compare primary/secondary endpoints via two-proportion z-test or Mann-Whitney U."
            ),
        }

