"""CSIP Model Evaluation & Explainability Module.

Provides SHAP feature attribution, reliability diagrams, Expected Calibration Error (ECE),
and probability calibration tools complying with SKKNI [UK-10 Mengevaluasi Model].
"""

from csip.evaluation.explainer import ModelExplainer, compute_ece

__all__ = [
    "ModelExplainer",
    "compute_ece",
]
