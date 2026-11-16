"""CSIP Features Module.

Provides feature construction routines, spatial Haversine calculation,
and zero-leakage multi-grain analytical builders.
"""

from csip.features.builder import AutoFeatureBuilder, build_interaction_features
from csip.features.engineer import FeatureEngineer, haversine_np

__all__ = [
    "FeatureEngineer",
    "haversine_np",
    "AutoFeatureBuilder",
    "build_interaction_features",
]
