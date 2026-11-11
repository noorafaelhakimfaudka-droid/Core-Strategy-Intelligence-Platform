"""CSIP Models Module.

Provides Baseline Ladder (B0 - B4), classical and ensemble ML algorithms,
deep learning neural architectures (Tabular MLP and Text Bi-LSTM),
and standardized temporal experiment trainers.
Complies with SKKNI [UK-08 Membangun Skenario Model] and [UK-09 Membangun Model].
"""

from csip.models.classic import (
    DelayHeuristicClassifier,
    MajorityClassClassifier,
    MeanRegressor,
    get_model_pipeline,
)
from csip.models.ml_engine import (
    train_real_ml_pipeline,
    train_semantic_ml_pipeline,
)
from csip.models.trainer import ModelExperimentTrainer


def __getattr__(name: str):
    """Lazy import for deep learning models and tokenizers (Finding F-04 / P-03)."""
    if name in ("TabularEmbeddingMLP", "TabularMLPClassifier"):
        import csip.models.deep_tabular as dt
        return getattr(dt, name)
    if name in ("SimpleTokenizer", "TextBiLSTM", "TextBiLSTMClassifier"):
        import csip.models.deep_seq as ds
        return getattr(ds, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "DelayHeuristicClassifier",
    "MajorityClassClassifier",
    "MeanRegressor",
    "get_model_pipeline",
    "ModelExperimentTrainer",
    "SimpleTokenizer",
    "TextBiLSTM",
    "TextBiLSTMClassifier",
    "TabularEmbeddingMLP",
    "TabularMLPClassifier",
    "train_real_ml_pipeline",
    "train_semantic_ml_pipeline",
]
