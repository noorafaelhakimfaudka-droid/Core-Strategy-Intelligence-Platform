"""CSIP Decision Engine Schemas and Data Models.

Defines the core data contracts for the Business Decision Intelligence layer.
Separates model probability, business priority, recommended action,
and explicitly categorizes evidence types (observational, simulated, causal).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class DecisionPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class OperationalFunction(str, Enum):
    LOGISTICS_FULFILLMENT = "Logistics & Fulfillment"
    CUSTOMER_EXPERIENCE = "Customer Experience & Retention"
    MERCHANT_MANAGEMENT = "Merchant Operations"
    PAYMENT_OPERATIONS = "Payment Operations"
    EXECUTIVE_PLANNING = "Executive Strategy"


class EvidenceType(str, Enum):
    OBSERVATIONAL_PREDICTIVE = "OBSERVATIONAL_PREDICTIVE"
    SIMULATED_SCENARIO = "SIMULATED_SCENARIO"
    HISTORICAL_OBSERVATION = "HISTORICAL_OBSERVATION"
    CAUSAL_INTERVENTION = "CAUSAL_INTERVENTION"


class RecommendationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACTIVE = "ACTIVE"
    EVALUATED = "EVALUATED"
    REJECTED = "REJECTED"


@dataclass
class DecisionRuleConfig:
    """Configurable prioritization parameters aligned with operational capacity.

    Note: Default values are conservative fallback baselines. For production
    calibration, use ``BusinessDecisionEngine.calibrate_thresholds_from_capacity``
    with out-of-time validation predictions and daily operational capacity.
    """
    risk_probability_threshold: float = 0.35
    critical_risk_probability_threshold: float = 0.60
    delay_days_threshold: float = 3.0
    critical_delay_days_threshold: float = 7.0
    high_order_value_threshold: float = 150.0
    freight_ratio_threshold: float = 0.28
    long_distance_km_threshold: float = 1200.0
    capacity_max_actions_per_batch: int = 100


@dataclass
class DecisionRecommendation:
    """Standardized decision intelligence recommendation structure."""
    decision_id: str
    business_problem: str
    relevant_entity: str
    prediction_or_evidence: Dict[str, Any]
    priority_level: DecisionPriority
    contributing_factors: List[Dict[str, Any]]
    recommended_action: str
    responsible_function: OperationalFunction
    expected_operational_objective: str
    measurement_criteria: List[str]
    limitations_and_uncertainty: str
    recommendation_status: RecommendationStatus = RecommendationStatus.PROPOSED
    evidence_type: EvidenceType = EvidenceType.OBSERVATIONAL_PREDICTIVE
    estimated_cost_tier: str = "LOW"  # LOW, MEDIUM, HIGH
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["priority_level"] = self.priority_level.value
        data["responsible_function"] = self.responsible_function.value
        data["recommendation_status"] = self.recommendation_status.value
        data["evidence_type"] = self.evidence_type.value
        return data

