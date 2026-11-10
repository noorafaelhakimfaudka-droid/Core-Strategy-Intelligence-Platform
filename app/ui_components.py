"""CSIP UI Components & Warm Art Gallery Design System Helper.

Provides:
- Editorial CSS injection
- Plotly painting theme formatter (0% visual noise, story-driven annotations)
- High-level HTML components for human-first storytelling
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import plotly.graph_objects as go
import streamlit as st

logger = logging.getLogger(__name__)

# Editorial Painting Palette
PALETTE = {
    "terracotta": "#C85A32",
    "forest_sage": "#2E6F40",
    "indigo_ink": "#2B4C7E",
    "warm_amber": "#D9822B",
    "crimson_clay": "#B83A2E",
    "muted_stone": "#A8A29E",
    "canvas": "#FAF7F2",
    "card_bg": "#FFFFFF",
    "charcoal": "#1C1917",
    "subtle_text": "#655E57",
}

PLOTLY_COLORWAY = [
    PALETTE["terracotta"],
    PALETTE["forest_sage"],
    PALETTE["indigo_ink"],
    PALETTE["warm_amber"],
    PALETTE["crimson_clay"],
    PALETTE["muted_stone"],
]


def apply_editorial_theme() -> None:
    """Inject warm art gallery custom CSS into Streamlit."""
    css_path = Path(__file__).resolve().parent / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        logger.warning(f"style.css not found at {css_path}")


def editorial_plotly_theme(
    fig: go.Figure,
    title: str = "",
    subtitle: str = "",
    x_title: str = "",
    y_title: str = "",
    height: int = 420,
) -> go.Figure:
    """Format Plotly figure to look like a clean, publication-grade editorial chart."""
    full_title = f"<b>{title}</b>"
    if subtitle:
        full_title += f"<br><span style='font-size:12px; font-weight:normal; color:#655E57;'>{subtitle}</span>"

    fig.update_layout(
        title={
            "text": full_title,
            "y": 0.94,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"family": "Newsreader, Playfair Display, Georgia, serif", "size": 18, "color": PALETTE["charcoal"]},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=PLOTLY_COLORWAY,
        font={"family": "Plus Jakarta Sans, sans-serif", "size": 12, "color": PALETTE["charcoal"]},
        height=height,
        margin={"l": 40, "r": 30, "t": 75, "b": 50},
        showlegend=True,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
            "font": {"size": 11, "color": PALETTE["subtle_text"]},
        },
    )

    fig.update_xaxes(
        title={"text": x_title, "font": {"size": 12, "color": PALETTE["subtle_text"]}},
        showgrid=True,
        gridcolor="rgba(101, 94, 87, 0.1)",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor="rgba(101, 94, 87, 0.2)",
        tickfont={"size": 10, "color": PALETTE["subtle_text"]},
    )

    fig.update_yaxes(
        title={"text": y_title, "font": {"size": 12, "color": PALETTE["subtle_text"]}},
        showgrid=True,
        gridcolor="rgba(101, 94, 87, 0.1)",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont={"size": 10, "color": PALETTE["subtle_text"]},
    )

    return fig


def render_hero(title: str, subtitle: str, tag: str = "Cerita di Balik 100.000 Pesanan E-Commerce") -> None:
    """Render high-impact editorial hero header box."""
    html = f"""
    <div class="hero-box">
        <span class="card-tag">{tag}</span>
        <div class="editorial-serif" style="font-size: 2.2rem; font-weight: 700; color: #1C1917; line-height: 1.2; margin-bottom: 0.6rem;">
            {title}
        </div>
        <div style="font-size: 1.05rem; color: #655E57; line-height: 1.6; max-width: 850px;">
            {subtitle}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_story_card(title: str, body: str, tag: Optional[str] = None, tag_class: str = "") -> None:
    """Render a clean editorial story card with subtle border and elevation."""
    tag_html = f'<span class="card-tag {tag_class}">{tag}</span><br>' if tag else ""
    html = f"""
    <div class="editorial-card">
        {tag_html}
        <div class="editorial-serif" style="font-size: 1.35rem; font-weight: 600; color: #1C1917; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="font-size: 0.95rem; color: #44403C; line-height: 1.6;">
            {body}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_qa_box(question: str, myth: str, reality: str, verdict_tag: str = "Fakta di Lapangan") -> None:
    """Render interactive myth-buster card."""
    html = f"""
    <div class="qa-box">
        <span class="card-tag amber">{verdict_tag}</span>
        <div class="editorial-serif" style="font-size: 1.25rem; font-weight: 700; color: #1C1917; margin-bottom: 0.75rem;">
            ❓ {question}
        </div>
        <div style="background-color: #FDFBF7; border-left: 3px solid #D9822B; padding: 0.6rem 0.9rem; border-radius: 6px; margin-bottom: 0.75rem; font-size: 0.9rem; color: #78350F;">
            <b>Mitos Umum:</b> <i>"{myth}"</i>
        </div>
        <div style="background-color: #F0FDF4; border-left: 3px solid #2E6F40; padding: 0.6rem 0.9rem; border-radius: 6px; font-size: 0.92rem; color: #14532D; line-height: 1.5;">
            <b>Temuan Nyata Data:</b> {reality}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_persona_card(
    name: str,
    share_pct: str,
    avatar_emoji: str,
    tag: str,
    habits: str,
    likes: str,
    dislikes: str,
) -> None:
    """Render a humanized persona profile card."""
    html = f"""
    <div class="persona-card">
        <div class="persona-header">
            <div class="persona-avatar">{avatar_emoji}</div>
            <div>
                <span class="card-tag sage">{tag}</span>
                <div class="editorial-serif" style="font-size: 1.3rem; font-weight: 700; color: #1C1917; margin-top: 0.2rem;">
                    {name}
                </div>
                <div style="font-size: 0.85rem; color: #655E57;">Porsi Populasi: <b>{share_pct}</b></div>
            </div>
        </div>
        <div style="font-size: 0.92rem; color: #332F2B; line-height: 1.6; margin-bottom: 0.75rem;">
            <b>🛍️ Kebiasaan Belanja:</b> {habits}
        </div>
        <div style="font-size: 0.88rem; color: #2E6F40; margin-bottom: 0.35rem;">
            <b>💚 Yang Mereka Sukai:</b> {likes}
        </div>
        <div style="font-size: 0.88rem; color: #B83A2E;">
            <b>💔 Yang Bikin Mereka Kapok:</b> {dislikes}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_before_after(
    current_label: str,
    current_val: str,
    simulated_label: str,
    simulated_val: str,
    verdict_summary: str,
    is_favorable: bool = True,
) -> None:
    """Render before-and-after comparison block."""
    color = PALETTE["forest_sage"] if is_favorable else PALETTE["crimson_clay"]
    icon = "✨" if is_favorable else "⚠️"
    html = f"""
    <div class="comparison-container">
        <div class="comparison-pane before">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #655E57; font-weight: 600;">Kondisi Saat Ini</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #1C1917; margin: 0.3rem 0;">{current_val}</div>
            <div style="font-size: 0.82rem; color: #655E57;">{current_label}</div>
        </div>
        <div class="comparison-pane after" style="border-top-color: {color};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: {color}; font-weight: 700;">Jika Kebijakan Diterapkan</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: {color}; margin: 0.3rem 0;">{simulated_val}</div>
            <div style="font-size: 0.82rem; color: #655E57;">{simulated_label}</div>
        </div>
    </div>
    <div style="background-color: #FFFFFF; border: 1px solid #EAE4DC; border-radius: 10px; padding: 0.8rem 1rem; margin-top: 0.75rem; font-size: 0.88rem; color: #1C1917;">
        <b>{icon} Kesimpulan Keputusan:</b> {verdict_summary}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

