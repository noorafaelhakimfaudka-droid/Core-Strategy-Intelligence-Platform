"""CSIP Universal Interactive Engine Package.

Provides active processing modules:
- omni_router: Free-text natural language parser and intent routing.
- scenario_duel: Simulation engine for trade-offs, what-if scenarios, and strategy duels.
- text_constellation: Fast NLP topic and sentiment constellation generator.
- universal_csv_xray: Instant role detection, cleaning, clustering, and factor discovery for arbitrary CSVs.
"""

from __future__ import annotations

from src.csip.engine.omni_router import OmniRouter, parse_user_query
from src.csip.engine.scenario_duel import ScenarioDuelEngine
from src.csip.engine.text_constellation import TextConstellationEngine
from src.csip.engine.universal_csv_xray import UniversalCSVXRay

__all__ = [
    "OmniRouter",
    "parse_user_query",
    "ScenarioDuelEngine",
    "TextConstellationEngine",
    "UniversalCSVXRay",
]

