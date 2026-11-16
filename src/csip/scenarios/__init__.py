"""CSIP Scenarios & Alternative World Simulation Module.

Provides counterfactual policy simulations (S0 - S5), extrapolation guardrails,
and business impact projections
and.
"""

from csip.scenarios.simulator import (
    AlternativeWorldSimulator,
    ScenarioDefinition,
)
from csip.scenarios.what_if import predict_what_if

__all__ = [
    "AlternativeWorldSimulator",
    "ScenarioDefinition",
    "predict_what_if",
]

