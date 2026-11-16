"""CSIP Business Impact Evaluation Framework.

Translates statistical metrics into operational trade-offs:
- Capacity-constrained triage (Precision@K, Recall@K)
- False positive review burden vs False negative churn exposure
- Delivery delay error distribution and triage windows
- Customer behavioral segment implications
Strictly avoids fabricated monetary savings and maintains clear boundaries
between observational findings, simulated scenarios, and causal proof.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


@dataclass
class ClassificationCapacityImpact:
    """Operational trade-offs for classification triage under capacity limits."""
    total_orders: int
    capacity_pct: float
    flagged_orders_count: int
    threshold_used: float
    precision_at_capacity: float
    recall_at_capacity: float
    true_positives: int
    false_positives: int
    false_positive_burden_desc: str
    false_negative_exposure_count: int
    false_negative_desc: str
    methodological_caveat: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DeliveryDelayOperationalImpact:
    """Error distribution and triage opportunities for delivery delay regressor."""
    total_evaluated: int
    mae_days: float
    rmse_days: float
    p50_absolute_error_days: float
    p90_absolute_error_days: float
    p99_absolute_error_days: float
    within_1_day_pct: float
    within_3_days_pct: float
    severe_error_over_7_days_pct: float
    triage_opportunity_desc: str
    population_limitation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BusinessImpactEvaluator:
    """Computes realistic operational and capacity-constrained business impacts."""

    @classmethod
    def evaluate_classification_capacity(
        cls,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        capacity_pcts: Optional[List[float]] = None,
    ) -> List[ClassificationCapacityImpact]:
        """
        Evaluates precision and recall at defined operational handling capacities
        (e.g., top 1%, 5%, 10% of total order volume).
        """
        if capacity_pcts is None:
            capacity_pcts = [0.01, 0.05, 0.10, 0.20]

        n = len(y_true)
        if n == 0:
            return []

        # Sort descending by predicted probability
        order = np.argsort(y_prob)[::-1]
        y_true_sorted = y_true[order]
        y_prob_sorted = y_prob[order]
        total_positives = int(np.sum(y_true))

        impacts: List[ClassificationCapacityImpact] = []
        for cap in capacity_pcts:
            k = max(1, int(round(n * cap)))
            top_k_labels = y_true_sorted[:k]
            threshold = float(y_prob_sorted[k - 1])

            tp = int(np.sum(top_k_labels == 1))
            fp = k - tp
            fn = total_positives - tp

            precision = float(tp / k) if k > 0 else 0.0
            recall = float(tp / total_positives) if total_positives > 0 else 0.0

            fp_desc = (
                f"{fp:,} orders ({fp/k:.1%} of triage capacity) are non-dissatisfied orders. "
                "Operational cost: Agent time reviewing orders that would not have complained."
            )
            fn_desc = (
                f"{fn:,} dissatisfied orders ({fn/max(total_positives,1):.1%} of all negative reviews) "
                "remain unfurled below the capacity boundary."
            )
            caveat = (
                "Observational ranking metric. Operational interventions (e.g. outreach, re-routing) "
                "require randomized holdout evaluation to verify causal churn reduction."
            )

            impacts.append(
                ClassificationCapacityImpact(
                    total_orders=n,
                    capacity_pct=cap,
                    flagged_orders_count=k,
                    threshold_used=round(threshold, 4),
                    precision_at_capacity=round(precision, 4),
                    recall_at_capacity=round(recall, 4),
                    true_positives=tp,
                    false_positives=fp,
                    false_positive_burden_desc=fp_desc,
                    false_negative_exposure_count=fn,
                    false_negative_desc=fn_desc,
                    methodological_caveat=caveat,
                )
            )

        return impacts

    @classmethod
    def evaluate_delivery_operational_impact(
        cls,
        y_true_days: np.ndarray,
        y_pred_days: np.ndarray,
    ) -> DeliveryDelayOperationalImpact:
        """Evaluates delivery delay error distribution and triage capabilities."""
        n = len(y_true_days)
        if n == 0:
            return DeliveryDelayOperationalImpact(
                total_evaluated=0,
                mae_days=0.0,
                rmse_days=0.0,
                p50_absolute_error_days=0.0,
                p90_absolute_error_days=0.0,
                p99_absolute_error_days=0.0,
                within_1_day_pct=0.0,
                within_3_days_pct=0.0,
                severe_error_over_7_days_pct=0.0,
                triage_opportunity_desc="No data",
                population_limitation="Empty evaluation set",
            )

        errors = y_true_days - y_pred_days
        abs_errors = np.abs(errors)

        mae = float(np.mean(abs_errors))
        rmse = float(np.sqrt(np.mean(errors ** 2)))
        p50 = float(np.percentile(abs_errors, 50))
        p90 = float(np.percentile(abs_errors, 90))
        p99 = float(np.percentile(abs_errors, 99))

        within_1 = float(np.mean(abs_errors <= 1.0) * 100.0)
        within_3 = float(np.mean(abs_errors <= 3.0) * 100.0)
        severe_7 = float(np.mean(abs_errors > 7.0) * 100.0)

        triage_desc = (
            f"{within_3:.1f}% of order deliveries are predicted within +-3 days of truth. "
            "Enables supply chain operations to preemptively notify logistics partners "
            "for shipments predicted to experience delays exceeding 4 business days."
        )
        limitation = (
            "Model is calibrated on historical carrier scans (2016-2018). "
            "Extreme logistics tail errors (>7 days) correlate with regional courier stockouts "
            "or severe weather disruptions uncaptured in static origin-destination features."
        )

        return DeliveryDelayOperationalImpact(
            total_evaluated=n,
            mae_days=round(mae, 2),
            rmse_days=round(rmse, 2),
            p50_absolute_error_days=round(p50, 2),
            p90_absolute_error_days=round(p90, 2),
            p99_absolute_error_days=round(p99, 2),
            within_1_day_pct=round(within_1, 1),
            within_3_days_pct=round(within_3, 1),
            severe_error_over_7_days_pct=round(severe_7, 1),
            triage_opportunity_desc=triage_desc,
            population_limitation=limitation,
        )

