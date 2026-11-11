"""CSIP Universal Interactive Engine Package.

Provides active processing modules:
- omni_router: Free-text natural language parser and intent routing.
- scenario_duel: Simulation engine for trade-offs, what-if scenarios, and strategy duels.
- text_constellation: Fast NLP topic and sentiment constellation generator.
- universal_csv_xray: Instant role detection, cleaning, clustering, and factor discovery for arbitrary CSVs.
"""

from __future__ import annotations

from .omni_router import OmniRouter, parse_user_query
from .scenario_duel import ScenarioDuelEngine
from .text_constellation import TextConstellationEngine
from .universal_csv_xray import UniversalCSVXRay

__all__ = [
    "OmniRouter",
    "parse_user_query",
    "ScenarioDuelEngine",
    "TextConstellationEngine",
    "UniversalCSVXRay",
]

