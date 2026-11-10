"""Canvas Story: Flowing living visual canvases with 0% text walls and <= 15 words titles.

Implements 3 dynamic visual acts:
1. Act 1: Peta Rasi Bintang Perilaku (Scattergl celestial map / clusters).
2. Act 2: Aliran Titik Patah Hati / Tarik-Menarik Faktor (Gold to crimson transition).
3. Act 3: Cermin Dua Dunia (Interactive simulation duel with dynamic sliders).

Strictly NO emojis, NO technical jargon on the primary canvas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.ui_components import NOCTURNAL_PALETTE, nocturnal_plotly_theme
from src.csip.engine.scenario_duel import ScenarioDuelEngine
from src.csip.engine.text_constellation import TextConstellationEngine
from src.csip.engine.universal_csv_xray import UniversalCSVXRay


# ---------------------------------------------------------------------
# BABAK 1: PETA RASI BINTANG PERILAKU
# ---------------------------------------------------------------------
def render_canvas_act1_constellation(
    mode: str,
    parsed_query: Dict[str, Any],
    base_sample_df: pd.DataFrame,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
) -> None:
    """Render Act 1: Celestial Constellation of Human Behavior."""
    st.markdown("<div id='act-1'></div>", unsafe_allow_html=True)

    if mode == "csv" and csv_results:
        title = "Setiap titik adalah satu baris data milikmu yang berkumpul menurut kemiripan sifat."
        clusters = csv_results.get("clusters", {})
        df_clean = csv_results.get("cleaned_dataframe", pd.DataFrame())
        roles = csv_results.get("roles", {})
        target_col = roles.get("target_col")

        labels = clusters.get("labels", [])
        cluster_palette = [NOCTURNAL_PALETTE["gold"], NOCTURNAL_PALETTE["cyan"], NOCTURNAL_PALETTE["amethyst"], NOCTURNAL_PALETTE["crimson"]]
        colors = [cluster_palette[lbl % len(cluster_palette)] for lbl in labels]

        custom_info = []
        for i, row in df_clean.iterrows():
            target_val = f"{row[target_col]}" if target_col and target_col in row else "-"
            custom_info.append([f"Baris {i+1}", f"Kelompok {labels[i % len(labels)] + 1}", target_val])

        fig = go.Figure(
            go.Scattergl(
                x=clusters.get("pca_x", []),
                y=clusters.get("pca_y", []),
                mode="markers",
                marker=dict(size=6, color=colors, opacity=0.88),
                customdata=np.array(custom_info),
                hovertemplate=(
                    "<span style='font-size:13px; font-weight:700; color:#F5B041;'>%{customdata[0]}</span><br>"
                    "<span style='color:#F4F1EA;'>Klasifikasi: <b>%{customdata[1]}</b></span><br>"
                    "<span style='color:#8E95A5;'>Nilai Hasil: %{customdata[2]}</span>"
                    "<extra></extra>"
                ),
            )
        )
    elif mode == "teks" and text_results:
        title = "Peta rasi suara manusia memperlihatkan sebaran rasa puas, bimbang, dan kecewa."
        points = text_results.get("points", [])
        xs = [p["x"] for p in points]
        ys = [p["y"] for p in points]
        colors = [p["color"] for p in points]
        custom_info = [[p["topic"], p["sentiment_label"], p["text"][:60] + "..."] for p in points]

        fig = go.Figure(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="markers",
                marker=dict(size=9, color=colors, opacity=0.92, line=dict(color="#090A0F", width=1.5)),
                customdata=np.array(custom_info),
                hovertemplate=(
                    "<span style='font-size:13px; font-weight:700; color:#F5B041;'>%{customdata[0]}</span><br>"
                    "<span style='color:#F4F1EA;'>Suasana Hati: <b>%{customdata[1]}</b></span><br>"
                    "<span style='color:#8E95A5;'>\"%{customdata[2]}\"</span>"
                    "<extra></extra>"
                ),
            )
        )
    else:
        title = "Di balik seratus ribu transaksi, setiap cahaya adalah manusia yang memilih dan menunggu."
        if not base_sample_df.empty:
            colors = [NOCTURNAL_PALETTE["gold"] if r >= 4 else (NOCTURNAL_PALETTE["cyan"] if r == 3 else NOCTURNAL_PALETTE["crimson"]) for r in base_sample_df["review_score"]]
            custom_info = []
            for _, row in base_sample_df.iterrows():
                custom_info.append([
                    row["customer_state"],
                    f"R$ {row['total_order_value']:,.0f}",
                    "Tepat Waktu" if row["delivery_delay_days"] <= 0 else f"Terlambat {int(round(row['delivery_delay_days']))} Hari",
                ])

            fig = go.Figure(
                go.Scattergl(
                    x=base_sample_df["buyer_lng"],
                    y=base_sample_df["buyer_lat"],
                    mode="markers",
                    marker=dict(size=4.5, color=colors, opacity=0.82),
                    customdata=np.array(custom_info),
                    hovertemplate=(
                        "<span style='font-size:13px; font-weight:700; color:#F5B041;'>Pembeli di %{customdata[0]}</span><br>"
                        "<span style='color:#F4F1EA;'>Nilai Belanja: <b>%{customdata[1]}</b></span><br>"
                        "<span style='color:#38BDF8;'>Kondisi: <b>%{customdata[2]}</b></span>"
                        "<extra></extra>"
                    ),
                )
            )
        else:
            fig = go.Figure()

    fig = nocturnal_plotly_theme(fig, height=540, show_axes=False)

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.8rem;">
        <span style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase; color:#F5B041; font-weight:600;">BABAK 1: RASI BINTANG PERILAKU</span>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-style: italic; color: #F4F1EA; margin-top: 0.2rem;">
            "{title}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass-canvas-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# BABAK 2: ALIRAN TITIK PATAH HATI / TARIK-MENARIK FAKTOR
# ---------------------------------------------------------------------
def render_canvas_act2_breaking_point(
    mode: str,
    parsed_query: Dict[str, Any],
    delay_curve_df: pd.DataFrame,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
) -> None:
    """Render Act 2: Tension curve showing where gold transitions to crimson."""
    st.markdown("<div id='act-2'></div>", unsafe_allow_html=True)

    if mode == "csv" and csv_results:
        title = "Faktor teratas yang paling kuat menggerakkan hasil pada data milikmu."
        factors = csv_results.get("factors", [])
        y_names = [f["faktor"] for f in factors][::-1]
        x_vals = [f["pengaruh_pct"] for f in factors][::-1]

        fig = go.Figure(
            go.Bar(
                x=x_vals,
                y=y_names,
                orientation="h",
                marker=dict(color=NOCTURNAL_PALETTE["gold"], line=dict(color="#FFFFFF", width=1)),
                text=[f"<b>{v:.1f}%</b>" for v in x_vals],
                textposition="auto",
                textfont=dict(family="Plus Jakarta Sans", size=11, color="#090A0F"),
                hovertemplate="<b>%{y}</b><br>Kekuatan Pengaruh: %{x:.1f}%<extra></extra>",
            )
        )
        fig = nocturnal_plotly_theme(fig, height=380, show_axes=True)
    elif mode == "teks" and text_results:
        title = "Porsi sentimen suara pembeli antara apresiasi, keraguan, dan kekecewaan."
        pos = text_results.get("positive_count", 0)
        neg = text_results.get("negative_count", 0)
        total = text_results.get("total_opinions", 1)
        netral = max(0, total - pos - neg)

        fig = go.Figure(
            go.Pie(
                labels=["Puas dan Bahagia", "Bimbang atau Netral", "Kecewa dan Terluka"],
                values=[pos, netral, neg],
                hole=0.64,
                marker=dict(colors=[NOCTURNAL_PALETTE["gold"], NOCTURNAL_PALETTE["cyan"], NOCTURNAL_PALETTE["crimson"]]),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>Jumlah Ungkapan: %{value}<br>Porsi: %{percent}<extra></extra>",
            )
        )
        fig.add_annotation(
            text=f"<b style='font-size:26px; color:#F5B041;'>{pos}/{total}</b><br><span style='font-size:11px; color:#8E95A5;'>Ungkapan Bahagia</span>",
            showarrow=False,
            font=dict(family="Cormorant Garamond, Georgia, serif"),
        )
        fig = nocturnal_plotly_theme(fig, height=420, show_axes=False)
    else:
        title = "Harga murah mudah dilupakan, namun tiga hari keterlambatan memadamkan kesetiaan pembeli."
        fig = go.Figure()

        if not delay_curve_df.empty:
            ontime = delay_curve_df["delay_days"] <= 0
            late = delay_curve_df["delay_days"] >= 0

            # Early/On-Time stream
            fig.add_trace(
                go.Scatter(
                    x=delay_curve_df.loc[ontime, "delay_days"],
                    y=delay_curve_df.loc[ontime, "score_all"],
                    mode="lines+markers",
                    name="Tepat Waktu",
                    line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                    fill="tozeroy",
                    fillcolor="rgba(245, 176, 65, 0.10)",
                    hovertemplate="<b>Tepat Waktu (%{x} Hari)</b><br>Kepuasan: %{y:.2f} / 5.0<extra></extra>",
                )
            )

            # Late stream plunging
            fig.add_trace(
                go.Scatter(
                    x=delay_curve_df.loc[late, "delay_days"],
                    y=delay_curve_df.loc[late, "score_all"],
                    mode="lines+markers",
                    name="Terlambat",
                    line=dict(color=NOCTURNAL_PALETTE["crimson"], width=4),
                    fill="tozeroy",
                    fillcolor="rgba(244, 63, 94, 0.14)",
                    hovertemplate="<b>Terlambat +%{x} Hari</b><br>Kepuasan Hancur: %{y:.2f} / 5.0<extra></extra>",
                )
            )

            # Point of Heartbreak Annotation
            fig.add_annotation(
                x=3,
                y=3.06,
                text="<b>Titik Patah Hati (Hari ke-3 Molor)</b><br><span style='font-size:10px;'>Kepuasan anjlok drastis</span>",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.2,
                arrowcolor=NOCTURNAL_PALETTE["crimson"],
                ax=0,
                ay=-45,
                font=dict(family="Plus Jakarta Sans", size=12, color=NOCTURNAL_PALETTE["ivory"]),
                bgcolor="rgba(20, 25, 38, 0.9)",
                bordercolor=NOCTURNAL_PALETTE["crimson"],
                borderwidth=1,
                borderpad=6,
            )

        fig = nocturnal_plotly_theme(fig, height=500, show_axes=True)
        fig.update_xaxes(title="Selisih dari Hari Janji Tiba (Hari)", range=[-10, 15])
        fig.update_yaxes(title="Tingkat Kepuasan Pembeli (Bintang 1 – 5)", range=[1.2, 5.0])

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.8rem; margin-top: 1.5rem;">
        <span style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase; color:#F5B041; font-weight:600;">BABAK 2: PERTARUNGAN FAKTOR & TITIK PATAH HATI</span>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-style: italic; color: #F4F1EA; margin-top: 0.2rem;">
            "{title}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass-canvas-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# BABAK 3: CERMIN DUA DUNIA (SIMULASI LANGSUNG)
# ---------------------------------------------------------------------
def render_canvas_act3_dual_world(
    mode: str,
    parsed_query: Dict[str, Any],
    duel_engine: ScenarioDuelEngine,
) -> None:
    """Render Act 3: Side-by-side comparative simulation with interactive glass sliders."""
    st.markdown("<div id='act-3'></div>", unsafe_allow_html=True)

    # Glass Interactive Sliders below
    st.markdown("""
    <div style="background: rgba(20, 25, 38, 0.72); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; font-weight: 600; color: #F5B041; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;">
            TUAS PENGENDALI SIMULASI LANGSUNG
        </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        param_subsidy = st.slider(
            "Besaran Pemotongan Biaya Tambahan (% Subsidi):",
            min_value=0.0,
            max_value=50.0,
            value=float(parsed_query.get("parameters", {}).get("subsidy_pct", 20.0)),
            step=5.0,
            key="slider_subsidy",
        )
    with col_s2:
        param_delay = st.slider(
            "Perubahan Waktu Tunggu (Hari Lebih Cepat / Lebih Lambat):",
            min_value=-5.0,
            max_value=5.0,
            value=float(parsed_query.get("parameters", {}).get("delay_days_delta", 0.0)),
            step=0.5,
            key="slider_delay",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if mode == "adu":
        title = "Disiplin waktu kurir menghasilkan efisiensi modal dua koma delapan kali lebih tinggi."
        duel_res = duel_engine.duel_two_options()
        weeks = duel_res["weeks"]

        fig = go.Figure()
        # Option A: Universal Subsidy (Cyan)
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=duel_res["traj_a_volume"],
                mode="lines+markers",
                name="Pilihan A: Subsidi Biaya Rata",
                line=dict(color=NOCTURNAL_PALETTE["cyan"], width=3),
                hovertemplate="<b>Pilihan A (Subsidi Rata)</b><br>Minggu %{x}: %{y:,.0f} Pesanan<extra></extra>",
            )
        )
        # Option B: Logistics SLA (Gold)
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=duel_res["traj_b_volume"],
                mode="lines+markers",
                name="Pilihan B: Disiplin Kurir",
                line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                hovertemplate="<b>Pilihan B (Disiplin Kurir)</b><br>Minggu %{x}: %{y:,.0f} Pesanan<extra></extra>",
            )
        )
        fig = nocturnal_plotly_theme(fig, height=480, show_axes=True)
        fig.update_xaxes(title="Minggu Perjalanan Kebijakan", tickmode="linear", dtick=1)
        fig.update_yaxes(title="Volume Pesanan per Minggu")

    else:
        title = "Pilihan baru diproyeksikan menggeser volume dan kekecewaan di dalam batas aman."
        sim_res = duel_engine.simulate_what_if(subsidy_pct=param_subsidy, delay_days_delta=param_delay)
        weeks = sim_res["weeks"]

        fig = go.Figure()
        # Optimistic upper bound
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=sim_res["optimistic_trajectory"],
                mode="lines",
                line=dict(color="rgba(56, 189, 248, 0.2)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Pessimistic lower bound filled
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=sim_res["pessimistic_trajectory"],
                mode="lines",
                line=dict(color="rgba(56, 189, 248, 0.2)", width=1),
                fill="tonexty",
                fillcolor="rgba(56, 189, 248, 0.08)",
                name="Rentang Kemungkinan (Pesimis - Optimis)",
                hoverinfo="skip",
            )
        )
        # Expected simulated trajectory (Gold)
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=sim_res["expected_trajectory"],
                mode="lines+markers",
                name="Proyeksi Pilihan Baru",
                line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                hovertemplate="<b>Pilihan Baru (Minggu %{x})</b><br>Proyeksi: %{y:,.0f} Pesanan<extra></extra>",
            )
        )
        # Current condition baseline (Cyan dashed)
        base_weekly = [sim_res["current_volume"] / 12.0 for _ in weeks]
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=base_weekly,
                mode="lines",
                name="Kondisi Saat Ini",
                line=dict(color=NOCTURNAL_PALETTE["cyan"], width=2.5, dash="dash"),
                hovertemplate="<b>Kondisi Saat Ini</b><br>Garis Dasar: %{y:,.0f} Pesanan<extra></extra>",
            )
        )
        fig = nocturnal_plotly_theme(fig, height=480, show_axes=True)
        fig.update_xaxes(title="Minggu Proyeksi Masa Depan", tickmode="linear", dtick=1)
        fig.update_yaxes(title="Volume Pesanan Mingguan")

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.8rem; margin-top: 1.5rem;">
        <span style="font-size:0.75rem; letter-spacing:0.2em; text-transform:uppercase; color:#F5B041; font-weight:600;">BABAK 3: CERMIN DUA DUNIA (SIMULASI LANGSUNG)</span>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-style: italic; color: #F4F1EA; margin-top: 0.2rem;">
            "{title}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass-canvas-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

