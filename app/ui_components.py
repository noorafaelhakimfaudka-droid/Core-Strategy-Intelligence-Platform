"""CSIP UI Components & The Nocturnal Gallery Design System.

Living Canvas, Scrollytelling, and Midnight Museum aesthetics for CSIP.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import plotly.graph_objects as go
import streamlit as st

logger = logging.getLogger(__name__)

# --- NOCTURNAL GALLERY PALETTE (MIDNIGHT OBSIDIAN & BIOLUMINESCENCE) ---
NOCTURNAL_PALETTE = {
    "obsidian": "#090A0F",
    "velvet": "#121521",
    "glass": "rgba(22, 27, 41, 0.72)",
    "ivory": "#F4F1EA",
    "stardust": "#8E95A5",
    "gold": "#F5B041",       # Luminous Gold: Kepuasan & Kesetiaan
    "cyan": "#38BDF8",       # Cyan Nebula: Aliran Pesanan & Nilai
    "crimson": "#F43F5E",    # Crimson Ember: Keterlambatan & Kecewa
    "amethyst": "#A855F7",   # Amethyst Glow: Friksi Ongkir & Keraguan
    "dim_star": "rgba(142, 149, 165, 0.18)",
}

# Editorial legacy palette for backwards compatibility
PALETTE = {
    "terracotta": "#F43F5E",
    "forest_sage": "#F5B041",
    "indigo_ink": "#38BDF8",
    "warm_amber": "#D9822B",
    "crimson_clay": "#F43F5E",
    "muted_stone": "#8E95A5",
    "canvas": "#090A0F",
    "card_bg": "rgba(22, 27, 41, 0.72)",
    "charcoal": "#F4F1EA",
    "subtle_text": "#8E95A5",
}

NOCTURNAL_COLORWAY = [
    NOCTURNAL_PALETTE["gold"],
    NOCTURNAL_PALETTE["cyan"],
    NOCTURNAL_PALETTE["amethyst"],
    NOCTURNAL_PALETTE["crimson"],
]


def apply_editorial_theme() -> None:
    """Inject Midnight Museum / Nocturnal Gallery custom CSS into Streamlit."""
    css_path = Path(__file__).resolve().parent / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        logger.warning(f"style.css not found at {css_path}")


def apply_nocturnal_theme() -> None:
    """Alias for apply_editorial_theme."""
    apply_editorial_theme()


def nocturnal_plotly_theme(
    fig: go.Figure,
    height: int = 580,
    show_axes: bool = False,
) -> go.Figure:
    """Format Plotly figure into a living canvas painting of light in a dark space."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=NOCTURNAL_COLORWAY,
        font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=NOCTURNAL_PALETTE["ivory"]),
        height=height,
        margin=dict(l=15, r=15, t=20, b=20),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="rgba(18, 21, 33, 0.95)",
            bordercolor="rgba(255, 255, 255, 0.15)",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=NOCTURNAL_PALETTE["ivory"]),
        ),
    )

    if not show_axes:
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            visible=False,
        )
        fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            visible=False,
        )
    else:
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="rgba(255,255,255,0.1)",
            tickfont=dict(size=11, color=NOCTURNAL_PALETTE["stardust"]),
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
            showline=False,
            tickfont=dict(size=11, color=NOCTURNAL_PALETTE["stardust"]),
        )

    return fig


def editorial_plotly_theme(
    fig: go.Figure,
    title: str = "",
    subtitle: str = "",
    x_title: str = "",
    y_title: str = "",
    height: int = 440,
) -> go.Figure:
    """Backwards compatible dark editorial theme."""
    full_title = f"<b>{title}</b>"
    if subtitle:
        full_title += f"<br><span style='font-size:12px; font-weight:normal; color:#8E95A5;'>{subtitle}</span>"

    fig.update_layout(
        title={
            "text": full_title,
            "y": 0.94,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"family": "Cormorant Garamond, Georgia, serif", "size": 20, "color": NOCTURNAL_PALETTE["ivory"]},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=NOCTURNAL_COLORWAY,
        font={"family": "Plus Jakarta Sans, sans-serif", "size": 12, "color": NOCTURNAL_PALETTE["ivory"]},
        height=height,
        margin={"l": 30, "r": 30, "t": 75, "b": 40},
        showlegend=True,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
            "font": {"size": 11, "color": NOCTURNAL_PALETTE["stardust"]},
        },
    )

    fig.update_xaxes(
        title={"text": x_title, "font": {"size": 12, "color": NOCTURNAL_PALETTE["stardust"]}},
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.06)",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor="rgba(255, 255, 255, 0.12)",
        tickfont={"size": 10, "color": NOCTURNAL_PALETTE["stardust"]},
    )

    fig.update_yaxes(
        title={"text": y_title, "font": {"size": 12, "color": NOCTURNAL_PALETTE["stardust"]}},
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.06)",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont={"size": 10, "color": NOCTURNAL_PALETTE["stardust"]},
    )

    return fig


def render_poetic_header(act_tag: str, poetic_title: str) -> None:
    """Render single poetic title (strictly <= 15 words) for living canvas act."""
    html = f"""
    <div class="poetic-section">
        <span class="poetic-act-tag">{act_tag}</span>
        <div class="poetic-title">
            "{poetic_title}"
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_floating_navigation() -> None:
    """Render top floating glass capsule bar and right-edge floating dots."""
    html = """
    <div class="nocturnal-nav">
        <div class="nocturnal-nav-logo">CSIP NOCTURNE</div>
        <a href="#act-1">Rasi Bintang</a>
        <a href="#act-2">Titik Patah</a>
        <a href="#act-3">Cermin Dunia</a>
        <a href="#curator-vault" style="color: #F5B041;">Catatan Kurator</a>
    </div>
    <div class="floating-dots">
        <a href="#act-1" class="floating-dot" title="Babak 1: Rasi Bintang"></a>
        <a href="#act-2" class="floating-dot" title="Babak 2: Titik Patah"></a>
        <a href="#act-3" class="floating-dot" title="Babak 3: Cermin Dunia"></a>
        <a href="#curator-vault" class="floating-dot" style="background: #F5B041;" title="Catatan Kurator"></a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# Backwards compatibility helpers
def render_hero(title: str, subtitle: str, tag: str = "Cerita di Balik 100.000 Pesanan E-Commerce") -> None:
    render_poetic_header(tag, title)


def render_story_card(title: str, body: str, tag: Optional[str] = None, tag_class: str = "") -> None:
    tag_html = f'<span class="poetic-act-tag">{tag}</span><br>' if tag else ""
    html = f"""
    <div class="glass-canvas-container" style="padding: 1.25rem; margin-bottom: 1.25rem;">
        {tag_html}
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.35rem; font-weight: 600; color: #F4F1EA; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="font-size: 0.92rem; color: #8E95A5; line-height: 1.6;">
            {body}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_qa_box(question: str, myth: str, reality: str, verdict_tag: str = "Fakta di Lapangan") -> None:
    html = f"""
    <div class="glass-canvas-container" style="padding: 1.25rem; margin-bottom: 1.25rem;">
        <span class="poetic-act-tag">{verdict_tag}</span>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.35rem; font-weight: 600; color: #F4F1EA; margin-bottom: 0.75rem;">
            {question}
        </div>
        <div style="background: rgba(245, 176, 65, 0.08); border-left: 3px solid #F5B041; padding: 0.6rem 0.9rem; border-radius: 6px; margin-bottom: 0.75rem; font-size: 0.9rem; color: #F5B041;">
            <b>Mitos:</b> <i>"{myth}"</i>
        </div>
        <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38BDF8; padding: 0.6rem 0.9rem; border-radius: 6px; font-size: 0.92rem; color: #F4F1EA; line-height: 1.5;">
            <b>Temuan Data:</b> {reality}
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
    html = f"""
    <div class="glass-canvas-container" style="padding: 1.25rem; margin-bottom: 1.25rem;">
        <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 0.75rem;">
            <div style="font-size: 2rem;">{avatar_emoji}</div>
            <div>
                <span class="poetic-act-tag">{tag}</span>
                <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.4rem; font-weight: 600; color: #F4F1EA;">
                    {name}
                </div>
                <div style="font-size: 0.85rem; color: #8E95A5;">Porsi: <b>{share_pct}</b></div>
            </div>
        </div>
        <div style="font-size: 0.9rem; color: #F4F1EA; line-height: 1.6; margin-bottom: 0.5rem;">
            <b>Kebiasaan:</b> {habits}
        </div>
        <div style="font-size: 0.88rem; color: #F5B041; margin-bottom: 0.35rem;">
            <b>Disukai:</b> {likes}
        </div>
        <div style="font-size: 0.88rem; color: #F43F5E;">
            <b>Dihindari:</b> {dislikes}
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
    color = NOCTURNAL_PALETTE["gold"] if is_favorable else NOCTURNAL_PALETTE["crimson"]
    html = f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.75rem;">
        <div class="glass-canvas-container" style="padding: 1rem; margin-bottom: 0;">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #8E95A5;">Kondisi Saat Ini</div>
            <div style="font-size: 1.35rem; font-weight: 700; color: #F4F1EA; margin: 0.3rem 0;">{current_val}</div>
            <div style="font-size: 0.82rem; color: #8E95A5;">{current_label}</div>
        </div>
        <div class="glass-canvas-container" style="padding: 1rem; margin-bottom: 0; border-top: 3px solid {color};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: {color};">Dengan Kebijakan</div>
            <div style="font-size: 1.35rem; font-weight: 700; color: {color}; margin: 0.3rem 0;">{simulated_val}</div>
            <div style="font-size: 0.82rem; color: #8E95A5;">{simulated_label}</div>
        </div>
    </div>
    <div class="glass-canvas-container" style="padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.88rem; color: #F4F1EA;">
        <b>Kesimpulan:</b> {verdict_summary}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
