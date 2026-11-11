"""CSIP Application Components Package.

Provides UI modules for the Universal Interactive Decision Lab:
- theme: Midnight Obsidian design system CSS, Bento cards, diagnostic finding box.
- charts: Plotly charts (real scatter clusters, PDP response curves, feature ranking).
- omni_input: Multi-mode command canvas with glass capsules and 1-click presets.
- canvas_story: Visual narrative stages and living canvases.
- curator_vault: Hidden curator drawer for BNSP assessors containing full technical evidence.
"""

from __future__ import annotations

from app.components.charts import (
    build_cluster_map_chart,
    build_feature_importance_chart,
    build_impact_curve_chart,
    build_pdp_response_chart,
    build_ranking_chart,
    build_real_scatter_chart,
)
from app.components.theme import (
    CUSTOM_CSS,
    apply_theme,
    render_bento_cards,
    render_diagnosis_box,
)
from app.components.omni_input import render_omni_input
from app.components.curator_vault import render_curator_vault

__all__ = [
    "CUSTOM_CSS",
    "apply_theme",
    "render_bento_cards",
    "render_diagnosis_box",
    "build_cluster_map_chart",
    "build_impact_curve_chart",
    "build_ranking_chart",
    "build_real_scatter_chart",
    "build_pdp_response_chart",
    "build_feature_importance_chart",
    "render_omni_input",
    "render_curator_vault",
]
