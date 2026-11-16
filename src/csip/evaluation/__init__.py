"""CSIP Model Evaluation & Explainability Module.

Provides SHAP feature attribution, reliability diagrams, Expected Calibration Error (ECE),
and probability calibration tools complying with SKKNI [UK-10 Mengevaluasi Model].
"""

from csip.evaluation.business_impact import (
    BusinessImpactEvaluator,
    ClassificationCapacityImpact,
    DeliveryDelayOperationalImpact,
)
from csip.evaluation.explainer import ModelExplainer, compute_ece

__all__ = [
    "BusinessImpactEvaluator",
    "ClassificationCapacityImpact",
    "DeliveryDelayOperationalImpact",
    "ModelExplainer",
    "compute_ece",
]

