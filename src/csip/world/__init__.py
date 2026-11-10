"""CSIP World Model & Dynamic Simulation Module.

Provides Vector AutoRegressive State-Space dynamics, historical backtesting,
and synthetic recovery verification for macro-level behavioral transitions.
"""

from csip.world.state_transition import (
    WorldStateTransitionModel,
    compute_mape,
    compute_wape,
)

__all__ = [
    "WorldStateTransitionModel",
    "compute_wape",
    "compute_mape",
]

