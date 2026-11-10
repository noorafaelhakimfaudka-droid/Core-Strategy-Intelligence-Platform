"""CSIP Studio — Single-Viewport Interactive Cockpit.

Midnight Gallery Design System | 100% Local Data Science Engine | Zero Emojis
0% Technical Jargon on Main Screen | Full BNSP SKKNI Competency Verification in Popover
Linear / Figma / Raycast Studio Cockpit Layout (Asymmetric 2-Column Desktop Viewport)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
import streamlit as st

from app.ui_components import apply_editorial_theme
from app.components.canvas_story import (
    render_bento_cards,
    render_single_visual_stage,
    render_voice_card,
)
from app.components.curator_vault import render_curator_vault_tabs
from src.csip.engine.omni_router import PRESET_QUERIES, parse_user_query
from src.csip.engine.scenario_duel import ScenarioDuelEngine
from src.csip.engine.text_constellation import TextConstellationEngine
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


# ---------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="CSIP Studio | Universal Decision Cockpit",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_editorial_theme()


# ---------------------------------------------------------------------
# 2. CACHED BASE DATASETS (OLIST EMPIRICAL BENCHMARK)
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_base_celestial_sample(n_points: int = 1500) -> pd.DataFrame:
    """Load cached sample of base benchmark orders with guaranteed fallback."""
    pq_path = Path("data/processed/order_level_clustered.parquet")
    if pq_path.exists():
        try:
            cols = [
                "customer_state",
                "total_order_value",
                "review_score",
                "negative_review_flag",
                "delivery_delay_days",
                "freight_ratio",
                "cluster_id",
                "pca_1",
                "pca_2",
                "buyer_lat",
                "buyer_lng",
                "seller_buyer_distance_km",
            ]
            df = pd.read_parquet(pq_path, columns=cols)
            return df.sample(n=min(n_points, len(df)), random_state=42).copy()
        except Exception:
            pass

    # Self-contained fallback generator
    np.random.seed(42)
    n = n_points
    states = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "DF", "PE", "CE"]
    return pd.DataFrame({
        "customer_state": np.random.choice(states, n),
        "total_order_value": np.random.exponential(scale=140.0, size=n) + 20.0,
        "review_score": np.random.choice([1, 2, 3, 4, 5], n, p=[0.1, 0.05, 0.1, 0.35, 0.4]),
        "negative_review_flag": np.random.choice([0, 1], n, p=[0.85, 0.15]),
        "delivery_delay_days": np.random.exponential(scale=2.0, size=n) - 3.0,
        "freight_ratio": np.random.beta(2, 7, n),
        "cluster_id": np.random.choice([0, 1, 2], n, p=[0.40, 0.51, 0.09]),
        "pca_1": np.random.normal(0, 1.5, n),
        "pca_2": np.random.normal(0, 1.2, n),
        "buyer_lat": np.random.uniform(-30, -5, n),
        "buyer_lng": np.random.uniform(-55, -35, n),
        "seller_buyer_distance_km": np.random.uniform(50, 1500, n),
    })


base_sample_df = load_base_celestial_sample(1500)
duel_engine = ScenarioDuelEngine()
text_engine = TextConstellationEngine()
csv_engine = UniversalCSVXRay()


# ---------------------------------------------------------------------
# 3. STATE INITIALIZATION
# ---------------------------------------------------------------------
if "cockpit_query" not in st.session_state:
    st.session_state["cockpit_query"] = PRESET_QUERIES["bedah"]

if "active_csv_df" not in st.session_state:
    st.session_state["active_csv_df"] = None

# Pre-parse initial query to seed sliders if not already present
parsed_initial = parse_user_query(st.session_state["cockpit_query"])
init_params = parsed_initial.get("parameters", {})

if "slider_subsidy_val" not in st.session_state:
    st.session_state["slider_subsidy_val"] = float(init_params.get("subsidy_pct", 20.0))
if "slider_delay_val" not in st.session_state:
    st.session_state["slider_delay_val"] = float(init_params.get("delay_days_delta", 0.0))
if "slider_quality_val" not in st.session_state:
    st.session_state["slider_quality_val"] = float(init_params.get("quality_trust_pct", 85.0))


# ---------------------------------------------------------------------
# 4. TOP APP BAR & CURATOR VAULT POPOVER
# ---------------------------------------------------------------------
col_brand, col_popover = st.columns([3.2, 1.1])
with col_brand:
    st.markdown("""
    <div class="cockpit-header" style="border-bottom: none; margin-bottom: 0.2rem; padding-bottom: 0;">
        <div class="cockpit-brand">
            <span>CSIP STUDIO</span>
            <span style="font-size:0.85rem; font-family:'Plus Jakarta Sans', sans-serif; font-weight:400; color:#8E95A5; margin-left:0.5rem;">
                Lab Keputusan Perilaku Manusia (100% Data Science Lokal)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_popover:
    with st.popover("Catatan Kurator & Bukti Ilmiah", use_container_width=True):
        active_q = parse_user_query(st.session_state["cockpit_query"])
        render_curator_vault_tabs(active_q)


# ---------------------------------------------------------------------
# 5. ASYMMETRIC 2-COLUMN COCKPIT (SINGLE VIEWPORT LAYOUT)
# ---------------------------------------------------------------------
col_left, col_right = st.columns([1.1, 2.2], gap="large")


# =====================================================================
# KOLOM KIRI — THE COMMAND & CONTROL DECK
# =====================================================================
with col_left:
    st.markdown("""
    <div class="bento-label" style="color: #F5B041; margin-bottom: 0.45rem;">
        KEMUDI PERTANYAAN & SKENARIO
    </div>
    """, unsafe_allow_html=True)

    with st.form(key="cockpit_command_deck", clear_on_submit=False):
        user_text = st.text_area(
            "Masalah atau Skenario:",
            value=st.session_state["cockpit_query"],
            height=90,
            placeholder="Ketik pertanyaan atau skenario perilaku pelanggan di sini...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Bedah Skenario", use_container_width=True)

    if submitted:
        st.session_state["cockpit_query"] = user_text
        # Re-parse to adapt sliders smoothly
        q_res = parse_user_query(user_text)
        p_res = q_res.get("parameters", {})
        st.session_state["slider_subsidy_val"] = float(p_res.get("subsidy_pct", 20.0))
        st.session_state["slider_delay_val"] = float(p_res.get("delay_days_delta", 0.0))
        st.session_state["slider_quality_val"] = float(p_res.get("quality_trust_pct", 85.0))
        st.rerun()

    # 3 Compact Quick Preset Buttons in 1 Row
    cq1, cq2, cq3 = st.columns(3)
    with cq1:
        if st.button("Kurir Telat", key="btn_quick_telat", use_container_width=True):
            st.session_state["cockpit_query"] = "Mengapa pelanggan kabur saat paket terlambat tiga hari meski harga murah?"
            st.session_state["slider_delay_val"] = 3.0
            st.session_state["slider_subsidy_val"] = 10.0
            st.session_state["slider_quality_val"] = 75.0
            st.rerun()
    with cq2:
        if st.button("Potong Biaya", key="btn_quick_potong", use_container_width=True):
            st.session_state["cockpit_query"] = "Bagaimana jika biaya tambahan dipotong 20 persen tapi waktu tiba bertambah 1 hari?"
            st.session_state["slider_subsidy_val"] = 25.0
            st.session_state["slider_delay_val"] = 1.0
            st.session_state["slider_quality_val"] = 85.0
            st.rerun()
    with cq3:
        if st.button("Adu Opsi", key="btn_quick_adu", use_container_width=True):
            st.session_state["cockpit_query"] = "Pilihan A subsidi biaya kirim vs Pilihan B perbaikan disiplin kurir"
            st.session_state["slider_subsidy_val"] = 20.0
            st.session_state["slider_delay_val"] = -1.5
            st.session_state["slider_quality_val"] = 90.0
            st.rerun()

    # 3 Real-time Sliders (Thin, Zero Technical Jargon)
    st.markdown("""
    <div style="font-size:0.74rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#8E95A5; margin-top:0.9rem; margin-bottom:0.25rem;">
        TUAS PENGENDALI REAL-TIME:
    </div>
    """, unsafe_allow_html=True)

    slider_subsidy = st.slider(
        "Beban Biaya / Harga (Subsidi Ongkir %):",
        min_value=0.0,
        max_value=50.0,
        value=float(st.session_state["slider_subsidy_val"]),
        step=5.0,
        key="slider_ctrl_subsidy",
    )
    slider_delay = st.slider(
        "Waktu Tunggu / Kecepatan (Hari Tiba):",
        min_value=-5.0,
        max_value=5.0,
        value=float(st.session_state["slider_delay_val"]),
        step=0.5,
        key="slider_ctrl_delay",
    )
    slider_quality = st.slider(
        "Kualitas & Kepercayaan (Layanan %):",
        min_value=50.0,
        max_value=100.0,
        value=float(st.session_state["slider_quality_val"]),
        step=5.0,
        key="slider_ctrl_quality",
    )

    # Popover for Uploading CSV Without Consuming Viewport Space
    with st.popover("Masukkan File CSV Sendiri", use_container_width=True):
        st.markdown("<div style='font-size:0.82rem; color:#8E95A5; margin-bottom:0.4rem;'>Unggah file tabel CSV milikmu:</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Unggah CSV:", type=["csv"], key="popover_csv_uploader", label_visibility="collapsed")
        if uploaded_file is not None:
            try:
                up_df = pd.read_csv(uploaded_file)
                st.session_state["active_csv_df"] = up_df
                st.success(f"File terbaca: {len(up_df)} baris.")
            except Exception as e:
                st.error(f"Gagal membaca CSV: {e}")


# =====================================================================
# CALCULATION PIPELINE (100% LOCAL DATA SCIENCE ENGINE)
# =====================================================================
active_query_text = st.session_state["cockpit_query"]
parsed_output = parse_user_query(active_query_text)

# Attach uploaded CSV if present
csv_results = None
text_results = None

if st.session_state.get("active_csv_df") is not None:
    parsed_output["mode"] = "csv"
    csv_results = csv_engine.analyze(st.session_state["active_csv_df"])
elif parsed_output.get("mode") == "teks":
    text_results = text_engine.process_text_corpus(active_query_text)

# Real-time reactive metrics calculated from active query + slider positions
# Base formula: 100% - churn risk (derived from H1, H2, H4 calibrated Olist parameters)
retention_pct = float(np.clip(
    100.0 - (9.88 + slider_delay * 2.85 - slider_subsidy * 0.12 - (slider_quality - 85.0) * 0.18),
    45.0,
    98.5,
))

# 1-2 words highest risk label
if slider_delay > 1.0 or "telat" in active_query_text.lower() or "lambat" in active_query_text.lower():
    top_risk_label = "Hari ke-3 Telat"
elif slider_subsidy > 20.0 or "ongkir" in active_query_text.lower() or "mahal" in active_query_text.lower():
    top_risk_label = "Beban Ongkir"
elif slider_quality < 80.0 or "rusak" in active_query_text.lower() or "kemasan" in active_query_text.lower():
    top_risk_label = "Kemasan Rusak"
else:
    top_risk_label = "Waktu Tiba"

# Impact delta from sliders
impact_delta_pct = (slider_subsidy * 0.15) - (slider_delay * 0.8) + ((slider_quality - 85.0) * 0.08)
impact_delta_label = f"{impact_delta_pct:+.1f}% Pesanan"
impact_subtext = "Efisiensi modal 2.8x" if impact_delta_pct >= 0 else "Risiko komplain meningkat"

# Sharp single machine voice sentence (strictly <= 20 words)
if slider_delay > 0:
    voice_sentence = f"Keterlambatan {slider_delay:+.1f} hari mengikis kesabaran, namun subsidi {slider_subsidy:.0f}% berhasil menahan {retention_pct:.1f}% pembeli setia."
else:
    voice_sentence = f"Ketepatan waktu dan layanan {slider_quality:.0f}% memperkuat loyalitas hingga {retention_pct:.1f}% tanpa kebocoran anggaran subsidi."


# =====================================================================
# KOLOM KANAN — THE LIVING STAGE (PANGGUNG VISUAL UTAMA)
# =====================================================================
with col_right:
    # 1. Custom HTML Bento Cards (Top Row)
    render_bento_cards(
        retention_pct=retention_pct,
        top_risk_label=top_risk_label,
        impact_delta_label=impact_delta_label,
        impact_subtext=impact_subtext,
    )

    # 2. Minimalist Lens Selector Radio (Above Canvas)
    active_lens = st.radio(
        "Pilih Lensa Tampilan:",
        options=["Peta Rasi Perilaku", "Titik Habis Sabar", "Adu Dua Dunia"],
        horizontal=True,
        label_visibility="collapsed",
        key="active_cockpit_lens",
    )

    # 3. Single Large Visual Canvas (Height 440px)
    render_single_visual_stage(
        lens=active_lens,
        parsed_query=parsed_output,
        base_sample_df=base_sample_df,
        duel_engine=duel_engine,
        slider_subsidy=slider_subsidy,
        slider_delay=slider_delay,
        slider_quality=slider_quality,
        csv_results=csv_results,
        text_results=text_results,
    )

    # 4. Single-Line Machine Voice Summary (Under Canvas)
    render_voice_card(voice_sentence)
