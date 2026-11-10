"""CSIP Scenarios & Alternative World Simulation Module.

Provides counterfactual policy simulations (S0 - S5), extrapolation guardrails,
and business impact projections complying with SKKNI [UK-08 Membangun Skenario Model]
and [UK-11 Mengembangkan Solusi].
"""

from csip.scenarios.simulator import (
    AlternativeWorldSimulator,
    ScenarioDefinition,
)

__all__ = [
    "AlternativeWorldSimulator",
    "ScenarioDefinition",
]

