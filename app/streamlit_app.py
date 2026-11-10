"""CSIP — Universal Interactive Decision Lab.

Midnight Gallery Design System | Active Processing Engines | Zero Emojis
0% Technical Jargon on Main Screen | Full BNSP SKKNI Competency Verification
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from app.ui_components import (
    apply_editorial_theme,
    render_floating_navigation,
)
from app.components.omni_input import render_omni_input
from app.components.canvas_story import (
    render_canvas_act1_constellation,
    render_canvas_act2_breaking_point,
    render_canvas_act3_dual_world,
)
from app.components.curator_vault import render_curator_vault
from src.csip.engine.scenario_duel import ScenarioDuelEngine
from src.csip.engine.text_constellation import TextConstellationEngine
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


# ---------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="CSIP | Universal Interactive Decision Lab",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_editorial_theme()
render_floating_navigation()


# ---------------------------------------------------------------------
# 2. DATA CACHING (BASE BENCHMARK MEMORY)
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_base_celestial_sample(n_points: int = 2500) -> pd.DataFrame:
    """Load cached sample of base benchmark orders."""
    pq_path = Path("data/processed/order_level_clustered.parquet")
    if not pq_path.exists():
        return pd.DataFrame()

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


@st.cache_data(show_spinner=False)
def load_base_delay_curve() -> pd.DataFrame:
    """Load base delivery delay vs review score curve."""
    pq_path = Path("data/processed/order_level.parquet")
    if not pq_path.exists():
        return pd.DataFrame()

    df = pd.read_parquet(pq_path, columns=["delivery_delay_days", "review_score", "freight_ratio"])
    df["delay_bin"] = df["delivery_delay_days"].clip(-10, 15).round()
    df["high_freight"] = df["freight_ratio"] > 0.25

    grp_all = df.groupby("delay_bin")["review_score"].mean().reset_index()
    grp_all.columns = ["delay_days", "score_all"]

    grp_hf = df[df["high_freight"]].groupby("delay_bin")["review_score"].mean().reset_index()
    grp_hf.columns = ["delay_days", "score_high_freight"]

    merged = pd.merge(grp_all, grp_hf, on="delay_days", how="left")
    return merged.sort_values("delay_days").reset_index(drop=True)


base_sample_df = load_base_celestial_sample(2500)
base_delay_df = load_base_delay_curve()

# Initialize engines
duel_engine = ScenarioDuelEngine()
text_engine = TextConstellationEngine()
csv_engine = UniversalCSVXRay()


# ---------------------------------------------------------------------
# 3. KOTAK INPUT SERBAGUNA (THE COMMAND CANVAS)
# ---------------------------------------------------------------------
parsed_input = render_omni_input()
active_mode = parsed_input["mode"]

# Execute active engine calculations
csv_results = None
text_results = None

if active_mode == "csv":
    df_to_xray = parsed_input.get("uploaded_df")
    if df_to_xray is None or df_to_xray.empty:
        df_to_xray = UniversalCSVXRay.generate_sample_csv(350)
    csv_results = csv_engine.analyze(df_to_xray)

elif active_mode == "teks":
    raw_corpus = parsed_input.get("raw_text", "")
    text_results = text_engine.process_text_corpus(raw_corpus)


# ---------------------------------------------------------------------
# 4. KANVAS VISUAL MENGALIR (3 BABAK VISUAL)
# ---------------------------------------------------------------------

# Babak 1: Rasi Bintang Perilaku
render_canvas_act1_constellation(
    mode=active_mode,
    parsed_query=parsed_input,
    base_sample_df=base_sample_df,
    csv_results=csv_results,
    text_results=text_results,
)

# Babak 2: Aliran Titik Patah Hati & Tarik-Menarik Faktor
render_canvas_act2_breaking_point(
    mode=active_mode,
    parsed_query=parsed_input,
    delay_curve_df=base_delay_df,
    csv_results=csv_results,
    text_results=text_results,
)

# Babak 3: Cermin Dua Dunia (Simulasi Langsung)
render_canvas_act3_dual_world(
    mode=active_mode,
    parsed_query=parsed_input,
    duel_engine=duel_engine,
)


# ---------------------------------------------------------------------
# 5. LACI CATATAN KURATOR (KHUSUS PENGUJI BNSP)
# ---------------------------------------------------------------------
render_curator_vault()
