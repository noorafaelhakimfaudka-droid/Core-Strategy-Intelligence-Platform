"""CSIP — Universal Data Science & Decision Studio.

Interactive Single-Viewport Desktop Cockpit for Empirical Machine Learning,
Causal Factor Discovery, and What-If Decision Simulation.

Implements BNSP SKKNI 11 Core Competencies:
[UK-01] s/d [UK-11] across data ingestion, profiling, cleaning, modeling, and evaluation.
100% Local Execution, Zero Emojis, Zero External API Calls.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ and repo root are in python search path
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd
import streamlit as st

from app.components.charts import (
    build_feature_importance_chart,
    build_pdp_response_chart,
    build_real_scatter_chart,
)
from app.components.theme import (
    apply_theme,
    render_bento_cards,
    render_diagnosis_box,
)
from csip.data.semantic_profiler import get_builtin_dataset
from csip.models.ml_engine import train_semantic_ml_pipeline
from csip.scenarios.what_if import predict_what_if

# ==============================================================================
# 1. PAGE SETUP & DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="CSIP — Universal Data Science & Decision Studio",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()


# ==============================================================================
# 2. CACHED ENGINE ADAPTERS
# ==============================================================================
@st.cache_data
def cached_load_dataset(name: str) -> pd.DataFrame:
    """[UK-01, UK-02] Ingest and load reference or empirical dataset."""
    return get_builtin_dataset(name)


@st.cache_resource
def cached_train_pipeline(
    df_hash: int,
    df_sample: pd.DataFrame,
    target_col: str,
    feature_cols: list[str],
):
    """[UK-08, UK-09, UK-10, UK-11] Train multi-model comparison, compute metrics, and segment clusters."""
    return train_semantic_ml_pipeline(
        df=df_sample,
        target_col=target_col,
        feature_cols=feature_cols,
        df_hash=df_hash,
    )


# ==============================================================================
# 3. TOP NAVIGATION & CURATOR VAULT
# ==============================================================================
top_l, top_r = st.columns([3.0, 1.2], vertical_alignment="center")
with top_l:
    st.markdown(
        """
        <div class="studio-topbar">
            <div class="brand-wrap">
                <span class="brand-mark">CSIP Studio</span>
                <span class="brand-badge">100% Real-Data ML Engine</span>
                <span class="brand-sub">Auto-Data Scientist, Penemu Pola & Simulator Keputusan untuk Dataset Apa Saja</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.07); margin: 0.4rem 0 1.0rem 0;'>", unsafe_allow_html=True)


# ==============================================================================
# 4. MAIN COCKPIT WORKSPACE (TWO ASYMMETRIC COLUMNS)
# ==============================================================================
col_left, col_right = st.columns([1.12, 2.28], gap="large")

with col_left:
    st.markdown('<span class="section-tag">01 / Sumber Data & Target Analisis</span>', unsafe_allow_html=True)

    uploaded_csv = st.file_uploader(
        "Unggah File CSV Kamu Sendiri (Opsional)",
        type=["csv"],
        help="Unggah CSV apa saja (penjualan, operasional, logistik). Jika kosong, gunakan dataset bawaan di bawah.",
    )

    if uploaded_csv is not None:
        active_df = pd.read_csv(uploaded_csv)
        dataset_title = f"CSV Pengguna: {uploaded_csv.name}"
    else:
        preset_choice = st.selectbox(
            "Atau Pilih Dataset Bawaan",
            options=[
                "Data E-Commerce Olist (Lokal)",
                "Dataset Kesehatan & Biometrik (Sklearn Diabetes)",
                "Dataset Kualitas Produk & Kimia (Sklearn Wine)",
            ],
            label_visibility="collapsed",
        )
        active_df = cached_load_dataset(preset_choice)
        dataset_title = preset_choice

    # Detect valid numeric features for empirical modeling
    numeric_cols = [
        c for c in active_df.select_dtypes(include=[np.number]).columns
        if active_df[c].nunique() > 1 and not c.lower().endswith("_id")
    ]

    if len(numeric_cols) < 2:
        st.error("File CSV membutuhkan minimal 2 kolom berisi angka (numerik) untuk dianalisis oleh model.")
        st.stop()

    default_target_idx = len(numeric_cols) - 1
    target_col = st.selectbox(
        "Pilih Variabel Hasil (Target) yang Ingin Dioptimalkan / Diprediksi:",
        options=numeric_cols,
        index=default_target_idx,
    )

    candidate_features = [c for c in numeric_cols if c != target_col]
    selected_features = st.multiselect(
        "Faktor Penyebab / Penggerak (Otomatis Memilih Semua):",
        options=candidate_features,
        default=candidate_features[:8],
    )

    if not selected_features:
        st.warning("Pilih minimal 1 kolom faktor penggerak.")
        st.stop()

    # Train empirical model pipeline on active data
    df_signature = hash((dataset_title, target_col, tuple(selected_features), len(active_df)))
    pipeline = cached_train_pipeline(df_signature, active_df, target_col, selected_features)

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    st.markdown('<span class="section-tag">02 / Simulator Tuas Faktor Terkuat (Dari Data Asli)</span>', unsafe_allow_html=True)

    # Dynamic interactive sliders for the top 3 influential features
    custom_inputs = {}
    top_3_rows = pipeline["stats_df"].iloc[:3]
    for _, row_meta in top_3_rows.iterrows():
        f_name = row_meta["Fitur"]
        f_min = float(row_meta["Min"])
        f_max = float(row_meta["Max"])
        f_med = float(row_meta["Median"])
        if f_max <= f_min:
            f_max = f_min + 1.0
        step_val = (f_max - f_min) / 100.0
        r_sign = "Searah (+)" if row_meta["Pearson_r"] >= 0 else "Berlawanan (-)"

        custom_inputs[f_name] = st.slider(
            f"{f_name} [Korelasi r={row_meta['Pearson_r']:+.2f} {r_sign}]",
            min_value=f_min,
            max_value=f_max,
            value=f_med,
            step=step_val,
        )

    filter_query = st.text_input(
        "Cari Kata Kunci / Fokus Variabel di Tabel:",
        placeholder="Ketik nama kolom untuk menyorot korelasinya...",
    )


# ==============================================================================
# 5. RIGHT STAGE: METRICS, CHARTS & FINDINGS
# ==============================================================================
sim = predict_what_if(pipeline, custom_inputs)
top1_row = pipeline["stats_df"].iloc[0]

with top_r:
    with st.popover("Bukti Statistik & 11 Unit SKKNI", use_container_width=True):
        st.markdown(f"##### Tabel Evaluasi Faktor pada `{dataset_title}` ({pipeline['n_rows']:,} Baris)")
        st.dataframe(pipeline["stats_df"].round(4), use_container_width=True, hide_index=True)
        st.caption(
            f"Seluruh 11 Unit Kompetensi SKKNI (Menelaah, Memvalidasi, Membersihkan, Mengkonstruksi, "
            f"Memodelkan Random Forest & K-Means, serta Evaluasi {pipeline['secondary_metric_str']}) "
            f"dieksekusi secara langsung pada tabel aktif."
        )

with col_right:
    # 1. Glass Bento Metric Cards
    render_bento_cards(sim=sim, pipeline=pipeline, target_col=target_col)

    # 2. Section Header & Lens Selector
    hdr_l, hdr_r = st.columns([1.3, 1.7], vertical_alignment="center")
    with hdr_l:
        st.markdown(
            f"""
            <div>
                <div class="stage-title">Rontgen Data: {dataset_title}</div>
                <div class="stage-caption">Menampilkan {pipeline['n_rows']:,} sampel nyata yang dikelompokkan oleh K-Means & diprediksi oleh Random Forest</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hdr_r:
        active_lens = st.radio(
            "Pilih Visualisasi Data Asli",
            options=[
                "Peta Klaster Data Asli",
                "Kurva Respons Variabel #1",
                "Peringkat Faktor Penyebab",
            ],
            horizontal=True,
            label_visibility="collapsed",
        )

    # 3. Interactive Plotly Charts
    if active_lens == "Peta Klaster Data Asli":
        fig = build_real_scatter_chart(pipeline, sim, target_col, custom_inputs)
    elif active_lens == "Kurva Respons Variabel #1":
        fig = build_pdp_response_chart(pipeline, sim, target_col)
    else:
        fig = build_feature_importance_chart(pipeline, target_col)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # 4. Human-First Finding Diagnosis Box
    render_diagnosis_box(
        dataset_title=dataset_title,
        target_col=target_col,
        pipeline=pipeline,
        sim=sim,
        filter_query=filter_query,
    )
