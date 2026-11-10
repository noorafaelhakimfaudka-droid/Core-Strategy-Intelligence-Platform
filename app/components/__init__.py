"""CSIP Application Components Package.

Provides UI modules for the Universal Interactive Decision Lab:
- omni_input: Multi-mode command canvas with 5 glass capsules and 1-click presets.
- canvas_story: Living Plotly visual canvases with <= 15 words conclusion titles.
- curator_vault: Hidden curator drawer for BNSP assessors containing full technical evidence.
"""

from __future__ import annotations

from app.components.omni_input import render_omni_input
from app.components.canvas_story import (
    render_main_story_card,
    render_bento_cards,
    render_single_visual_stage,
    render_voice_card,
    render_canvas_act1_constellation,
    render_canvas_act2_breaking_point,
    render_canvas_act3_dual_world,
)
from app.components.curator_vault import render_curator_vault

__all__ = [
    "render_omni_input",
    "render_main_story_card",
    "render_bento_cards",
    "render_single_visual_stage",
    "render_voice_card",
    "render_canvas_act1_constellation",
    "render_canvas_act2_breaking_point",
    "render_canvas_act3_dual_world",
    "render_curator_vault",
]
