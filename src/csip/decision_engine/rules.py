"""CSIP Operational Decision Rules and Logic Engine.

Maps predictive and analytical patterns to concrete operational actions.
Enforces that recommendations explicitly include contributing factors,
responsible functions, measurable objectives, and methodological limitations.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from csip.decision_engine.schemas import (
    DecisionPriority,
    DecisionRecommendation,
    DecisionRuleConfig,
    EvidenceType,
    OperationalFunction,
    RecommendationStatus,
)


class DecisionRuleEvaluator:
    """Evaluates orders and generates actionable business recommendations."""

    def __init__(self, config: Optional[DecisionRuleConfig] = None):
        self.config = config or DecisionRuleConfig()

    def evaluate_order(
        self,
        order_data: Dict[str, Any],
        predicted_delay_days: Optional[float] = None,
        predicted_negative_prob: Optional[float] = None,
        is_early_warning: bool = True,
    ) -> Optional[DecisionRecommendation]:
        """Evaluates a single order record and returns a recommendation if thresholds trigger."""
        order_id = str(order_data.get("order_id", "UNKNOWN_ORDER"))
        order_value = float(order_data.get("total_order_value", order_data.get("total_item_price", 0.0)))
        freight_ratio = float(order_data.get("freight_ratio", 0.0))
        distance_km = float(order_data.get("seller_buyer_distance_km", 0.0))
        lead_time = float(order_data.get("estimated_lead_time_days", 0.0))
        delay = predicted_delay_days if predicted_delay_days is not None else 0.0
        neg_prob = predicted_negative_prob if predicted_negative_prob is not None else 0.0

        contributing_factors = []
        if neg_prob >= self.config.risk_probability_threshold:
            contributing_factors.append({
                "factor": "Predicted Dissatisfaction Risk",
                "value": f"{neg_prob:.1%}",
                "threshold": f">= {self.config.risk_probability_threshold:.1%}",
                "direction": "RISK_INCREASING"
            })
        if delay >= self.config.delay_days_threshold:
            contributing_factors.append({
                "factor": "Predicted Delivery Delay",
                "value": f"+{delay:.1f} days",
                "threshold": f">= +{self.config.delay_days_threshold:.1f} days",
                "direction": "RISK_INCREASING"
            })
        if freight_ratio >= self.config.freight_ratio_threshold:
            contributing_factors.append({
                "factor": "Freight-to-Price Burden",
                "value": f"{freight_ratio:.1%}",
                "threshold": f">= {self.config.freight_ratio_threshold:.1%}",
                "direction": "COST_FRICTION"
            })
        if distance_km >= self.config.long_distance_km_threshold:
            contributing_factors.append({
                "factor": "Inter-Regional Transit Distance",
                "value": f"{distance_km:.0f} km",
                "threshold": f">= {self.config.long_distance_km_threshold:.0f} km",
                "direction": "TRANSIT_EXPOSURE"
            })

        # Decision Rule 1: CRITICAL Delivery Crisis on High-Value Order
        if (delay >= self.config.critical_delay_days_threshold or neg_prob >= self.config.critical_risk_probability_threshold) and (order_value >= self.config.high_order_value_threshold):
            return DecisionRecommendation(
                decision_id=f"DEC-CRIT-{order_id[-6:]}",
                business_problem="Severe delivery delay risk on high-value basket threatening customer lifetime value",
                relevant_entity=f"Order {order_id} (Basket: BRL {order_value:.2f})",
                prediction_or_evidence={
                    "predicted_delay_days": round(delay, 2),
                    "predicted_negative_prob": round(neg_prob, 4),
                    "order_value_brl": round(order_value, 2),
                    "model_source": "early_warning_lightgbm" if is_early_warning else "post_fulfillment_lightgbm",
                },
                priority_level=DecisionPriority.CRITICAL,
                contributing_factors=contributing_factors,
                recommended_action=(
                    "Immediate Tier-1 escalation: Re-route via expedited express courier, "
                    "flag dedicated customer care agent to provide real-time WhatsApp/SMS tracking, "
                    "and issue a pre-emptive BRL 25 delivery guarantee voucher."
                ),
                responsible_function=OperationalFunction.LOGISTICS_FULFILLMENT,
                expected_operational_objective=(
                    "Mitigate negative review risk by at least 40% through proactive transparency "
                    "and preserve high-value customer retention."
                ),
                measurement_criteria=[
                    "Final delivery lead time vs estimated",
                    "Customer review score (1-5 scale) within 14 days of delivery",
                    "Repeat purchase occurrence within 90 days",
                ],
                limitations_and_uncertainty=(
                    "Observational estimate derived from historical correlation. "
                    "Expedited re-routing incurs operational surcharge (~BRL 15-22). "
                    "Uplift should be monitored against an unassisted holdout cohort."
                ),
                recommendation_status=RecommendationStatus.PROPOSED,
                evidence_type=EvidenceType.OBSERVATIONAL_PREDICTIVE,
                estimated_cost_tier="HIGH",
            )

        # Decision Rule 2: Logistics Transit Friction (High distance + High delay)
        if delay >= self.config.delay_days_threshold:
            return DecisionRecommendation(
                decision_id=f"DEC-DEL-{order_id[-6:]}",
                business_problem="Predicted fulfillment bottleneck exceeding acceptable transit SLA",
                relevant_entity=f"Order {order_id} (Route: {distance_km:.0f} km)",
                prediction_or_evidence={
                    "predicted_delay_days": round(delay, 2),
                    "predicted_negative_prob": round(neg_prob, 4),
                    "seller_buyer_distance_km": round(distance_km, 1),
                },
                priority_level=DecisionPriority.HIGH if delay >= 5.0 else DecisionPriority.MEDIUM,
                contributing_factors=contributing_factors,
                recommended_action=(
                    "Prioritize package sorting at regional distribution hub; "
                    "send automated proactive ETA update to customer before estimated date lapses."
                ),
                responsible_function=OperationalFunction.LOGISTICS_FULFILLMENT,
                expected_operational_objective="Prevent inbound 'Where Is My Order?' (WISMO) support ticket volume.",
                measurement_criteria=[
                    "WISMO ticket contact rate per 100 delayed orders",
                    "Net Promoter Score / Review sentiment distribution",
                ],
                limitations_and_uncertainty=(
                    "Model predicts delay from logistics origin-destination features; "
                    "does not account for real-time weather or highway disruptions."
                ),
                recommendation_status=RecommendationStatus.PROPOSED,
                evidence_type=EvidenceType.OBSERVATIONAL_PREDICTIVE,
                estimated_cost_tier="LOW",
            )

        # Decision Rule 3: Economic Friction at Early Warning (High Freight Ratio)
        if is_early_warning and neg_prob >= self.config.risk_probability_threshold and freight_ratio >= self.config.freight_ratio_threshold:
            return DecisionRecommendation(
                decision_id=f"DEC-EW-{order_id[-6:]}",
                business_problem="Customer price sensitivity friction due to disproportionate shipping cost",
                relevant_entity=f"Order {order_id} (Freight Burden: {freight_ratio:.1%})",
                prediction_or_evidence={
                    "predicted_negative_prob": round(neg_prob, 4),
                    "freight_ratio": round(freight_ratio, 3),
                    "total_freight_brl": round(float(order_data.get("total_freight", 0.0)), 2),
                },
                priority_level=DecisionPriority.MEDIUM,
                contributing_factors=contributing_factors,
                recommended_action=(
                    "Deploy post-purchase satisfaction survey with dynamic BRL 10 shipping discount coupon "
                    "for next order to offset delivery fee sensitivity."
                ),
                responsible_function=OperationalFunction.CUSTOMER_EXPERIENCE,
                expected_operational_objective="Buffer negative post-purchase sentiment driven by high shipping burden.",
                measurement_criteria=[
                    "Coupon redemption rate within 30 days",
                    "Customer satisfaction rating",
                ],
                limitations_and_uncertainty=(
                    "Simulated sensitivity suggests freight ratio is a top contributor; "
                    "causal validation requires randomized coupon A/B test."
                ),
                recommendation_status=RecommendationStatus.PROPOSED,
                evidence_type=EvidenceType.OBSERVATIONAL_PREDICTIVE,
                estimated_cost_tier="MEDIUM",
            )

        # Decision Rule 4: General Customer Experience Watchlist
        if neg_prob >= self.config.risk_probability_threshold:
            return DecisionRecommendation(
                decision_id=f"DEC-CX-{order_id[-6:]}",
                business_problem="Elevated baseline probability of customer complaint / 1-star review",
                relevant_entity=f"Order {order_id}",
                prediction_or_evidence={
                    "predicted_negative_prob": round(neg_prob, 4),
                    "lead_time_days": round(lead_time, 1),
                },
                priority_level=DecisionPriority.LOW,
                contributing_factors=contributing_factors,
                recommended_action=(
                    "Log order into Customer Care observation queue; "
                    "trigger automated post-delivery check-in email 2 hours after recorded delivery."
                ),
                responsible_function=OperationalFunction.CUSTOMER_EXPERIENCE,
                expected_operational_objective="Capture dissatisfaction internally before public negative review is posted.",
                measurement_criteria=[
                    "Internal feedback capture rate vs public negative review rate",
                ],
                limitations_and_uncertainty=(
                    "Model precision at threshold 0.35 has an estimated false-positive rate of ~30%. "
                    "Automated emails should maintain neutral, helpful tone to avoid creating false alarms."
                ),
                recommendation_status=RecommendationStatus.PROPOSED,
                evidence_type=EvidenceType.OBSERVATIONAL_PREDICTIVE,
                estimated_cost_tier="LOW",
            )

        return None

