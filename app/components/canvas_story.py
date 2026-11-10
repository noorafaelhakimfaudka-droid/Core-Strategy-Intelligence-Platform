"""Canvas Story: Flowing living visual canvases directly connected to local engine outputs.

Implements 3 dynamic visual acts:
1. Act 1: Peta Rasi Bintang Perilaku (1,500 points with dynamic coordinate & color shifts based on TF-IDF dimensions).
2. Act 2: Aliran Titik Patah Hati & Tarik-Menarik Faktor (Dynamic non-linear spline with movable breaking point line).
3. Act 3: Cermin Dua Dunia (Side-by-side simulation duel with 3 live glass sliders: cost, speed, quality).

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


__all__ = [
    "render_main_story_card",
    "render_bento_cards",
    "render_single_visual_stage",
    "render_voice_card",
    "render_canvas_act1_constellation",
    "render_canvas_act2_breaking_point",
    "render_canvas_act3_dual_world",
]


# ---------------------------------------------------------------------
# BENTO CARDS & COCKPIT LIVING STAGE
# ---------------------------------------------------------------------
def render_bento_cards(
    retention_pct: float,
    top_risk_label: str,
    impact_delta_label: str,
    impact_subtext: str = "Respons terhadap tuas kiri",
) -> None:
    """Render 3 horizontal glass Bento cards using pure HTML & CSS Grid."""
    color_ret = NOCTURNAL_PALETTE["gold"] if retention_pct >= 80.0 else NOCTURNAL_PALETTE["crimson"]
    st.markdown(f"""
    <div class="bento-grid">
        <div class="bento-card">
            <div class="bento-label">Peluang Orang Bertahan</div>
            <div class="bento-val" style="color: {color_ret};">{retention_pct:.1f}%</div>
            <div style="height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; margin: 4px 0;">
                <div style="height: 100%; width: {min(100.0, max(0.0, retention_pct)):.1f}%; background: {color_ret};"></div>
            </div>
            <div class="bento-sub">Kestabilan loyalitas pembeli</div>
        </div>
        <div class="bento-card">
            <div class="bento-label">Titik Rawan Utama</div>
            <div class="bento-val" style="color: #F43F5E;">{top_risk_label}</div>
            <div style="height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; margin: 4px 0;">
                <div style="height: 100%; width: 75%; background: #F43F5E;"></div>
            </div>
            <div class="bento-sub">Faktor pemicu risiko terbesar</div>
        </div>
        <div class="bento-card">
            <div class="bento-label">Dampak Perubahan</div>
            <div class="bento-val" style="color: #38BDF8;">{impact_delta_label}</div>
            <div style="height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; margin: 4px 0;">
                <div style="height: 100%; width: 85%; background: #38BDF8;"></div>
            </div>
            <div class="bento-sub">{impact_subtext}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_voice_card(voice_sentence: str) -> None:
    """Render 1-line machine voice summary card (max 20 words) under the main canvas."""
    st.markdown(f"""
    <div class="voice-card">
        <div class="voice-tag">SUARA SISTEM:</div>
        <div class="voice-text">"{voice_sentence}"</div>
    </div>
    """, unsafe_allow_html=True)


def render_single_visual_stage(
    lens: str,
    parsed_query: Dict[str, Any],
    base_sample_df: pd.DataFrame,
    duel_engine: ScenarioDuelEngine,
    slider_subsidy: float,
    slider_delay: float,
    slider_quality: float,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
) -> None:
    """Render exactly ONE large visual canvas (height 450px) according to active lens."""
    dim_scores = parsed_query.get("dimension_scores", {})
    cost_s = dim_scores.get("cost_sensitivity", 0.25)
    time_f = dim_scores.get("time_friction", 0.25)
    trust_q = dim_scores.get("trust_quality", 0.25)

    if lens == "Peta Rasi Perilaku":
        if parsed_query.get("mode") == "csv" and csv_results:
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
                    marker=dict(size=6.5, color=colors, opacity=0.88),
                    customdata=np.array(custom_info),
                    hovertemplate="<b>%{customdata[0]}</b><br>Grup: %{customdata[1]}<br>Nilai: %{customdata[2]}<extra></extra>",
                )
            )
        else:
            n_pts = min(1500, len(base_sample_df)) if not base_sample_df.empty else 1500
            sample_df = base_sample_df.iloc[:n_pts].copy() if not base_sample_df.empty else pd.DataFrame()
            if sample_df.empty:
                np.random.seed(42)
                sample_df = pd.DataFrame({
                    "buyer_lng": np.random.uniform(-55, -35, 1500),
                    "buyer_lat": np.random.uniform(-30, -5, 1500),
                    "delivery_delay_days": np.random.exponential(scale=2.0, size=1500) - 3.0,
                    "freight_ratio": np.random.beta(2, 7, 1500),
                    "review_score": np.random.choice([1, 2, 3, 4, 5], 1500, p=[0.1, 0.05, 0.1, 0.35, 0.4]),
                    "customer_state": np.random.choice(["SP", "RJ", "MG", "RS", "PR"], 1500),
                    "total_order_value": np.random.exponential(scale=140.0, size=1500) + 20.0,
                })

            x_shift = (cost_s - 0.25) * 4.0 - (time_f - 0.25) * 2.0 + (slider_subsidy / 50.0) * 1.5
            y_shift = -(time_f - 0.25) * 5.0 + (trust_q - 0.25) * 3.5 - (slider_delay / 5.0) * 2.5
            xs = sample_df["buyer_lng"].to_numpy() + x_shift
            ys = sample_df["buyer_lat"].to_numpy() + y_shift

            colors = []
            sizes = []
            custom_info = []
            for _, row in sample_df.iterrows():
                delays = row["delivery_delay_days"] + slider_delay
                freight = row["freight_ratio"] * (1.0 - slider_subsidy / 100.0)
                score = row["review_score"]
                is_risk = (delays > 1.5) or (time_f > 0.35 and delays > 0.0) or (score <= 2)
                is_cost_sensitive = (freight > 0.25) or (cost_s > 0.35 and freight > 0.18)
                is_satisfied = (score >= 4 and delays <= 0.0) or (slider_quality > 85.0 and score >= 3)

                if is_risk:
                    colors.append(NOCTURNAL_PALETTE["crimson"])
                    sizes.append(5.5)
                    status_str = f"Rawan Kecewa (+{delays:.1f} Hari)"
                elif is_cost_sensitive:
                    colors.append(NOCTURNAL_PALETTE["amethyst"])
                    sizes.append(5.0)
                    status_str = f"Sensitif Ongkir ({freight*100:.0f}%)"
                elif is_satisfied:
                    colors.append(NOCTURNAL_PALETTE["gold"])
                    sizes.append(4.5)
                    status_str = "Puas dan Bertahan"
                else:
                    colors.append(NOCTURNAL_PALETTE["cyan"])
                    sizes.append(3.2)
                    status_str = "Kondisi Netral"

                custom_info.append([row.get("customer_state", "Kota"), f"R$ {row.get('total_order_value', 120.0):,.0f}", status_str])

            fig = go.Figure(
                go.Scattergl(
                    x=xs,
                    y=ys,
                    mode="markers",
                    marker=dict(size=sizes, color=colors, opacity=0.88),
                    customdata=np.array(custom_info),
                    hovertemplate="<b>%{customdata[0]}</b> | Belanja %{customdata[1]}<br>%{customdata[2]}<extra></extra>",
                )
            )
        fig = nocturnal_plotly_theme(fig, height=440, show_axes=False)

    elif lens == "Titik Habis Sabar":
        friction = float(round(0.224 - (slider_subsidy / 100.0) * 0.10, 3))
        phenom = duel_engine.dissect_phenomenon(
            delay_shift=slider_delay,
            friction_ratio=friction,
            quality_score=float(3.5 + (slider_quality / 100.0) * 1.5),
            trust_factor=float(slider_quality / 100.0),
        )
        days = np.array(phenom["delay_days"])
        scores = np.array(phenom["satisfaction"])
        cur_d = phenom["current_delay"]
        cur_s = phenom["current_score"]
        bp_day = phenom["breaking_point_day"]

        fig = go.Figure()
        ontime = days <= 0
        late = days >= 0
        fig.add_trace(
            go.Scatter(
                x=days[ontime],
                y=scores[ontime],
                mode="lines",
                name="Tepat Waktu",
                line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                fill="tozeroy",
                fillcolor="rgba(245, 176, 65, 0.10)",
                hovertemplate="<b>Tepat Waktu (%{x} Hari)</b><br>Kepuasan: %{y:.2f} / 5.0<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=days[late],
                y=scores[late],
                mode="lines",
                name="Terlambat",
                line=dict(color=NOCTURNAL_PALETTE["crimson"], width=4),
                fill="tozeroy",
                fillcolor="rgba(244, 63, 94, 0.14)",
                hovertemplate="<b>Terlambat +%{x} Hari</b><br>Kepuasan: %{y:.2f} / 5.0<extra></extra>",
            )
        )
        marker_color = NOCTURNAL_PALETTE["gold"] if cur_s >= 3.5 else NOCTURNAL_PALETTE["crimson"]
        fig.add_trace(
            go.Scatter(
                x=[cur_d],
                y=[cur_s],
                mode="markers",
                name="Posisi Tuas Anda",
                marker=dict(size=14, color="#FFFFFF", line=dict(color=marker_color, width=3.5)),
                hovertemplate=f"<b>Posisi Pilihan Anda</b><br>Selisih: {cur_d:+.1f} Hari<br>Kepuasan: {cur_s:.1f} / 5.0<extra></extra>",
            )
        )
        fig.add_vline(x=bp_day, line_width=2, line_dash="dash", line_color=NOCTURNAL_PALETTE["crimson"])
        fig.add_annotation(
            x=bp_day,
            y=2.8,
            text=f"<b>Batas Sabar (Hari ke-{bp_day:.1f})</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor=NOCTURNAL_PALETTE["crimson"],
            ax=0,
            ay=-40,
            font=dict(family="Plus Jakarta Sans", size=11, color=NOCTURNAL_PALETTE["ivory"]),
            bgcolor="rgba(20, 25, 38, 0.92)",
            bordercolor=NOCTURNAL_PALETTE["crimson"],
            borderwidth=1,
            borderpad=4,
        )
        fig = nocturnal_plotly_theme(fig, height=440, show_axes=True)
        fig.update_xaxes(title="Selisih Hari Pengiriman (Hari)", range=[-10, 15])
        fig.update_yaxes(title="Skor Kepuasan (1 - 5)", range=[1.2, 5.0])

    else:  # Adu Dua Dunia
        if parsed_query.get("mode") == "adu":
            duel_res = duel_engine.duel_two_options(
                subsidy_a=slider_subsidy,
                delay_delta_b=slider_delay,
                quality_b=slider_quality,
            )
            weeks = duel_res["weeks"]
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=weeks,
                    y=duel_res["traj_a_volume"],
                    mode="lines+markers",
                    name="Pilihan A: Subsidi Biaya",
                    line=dict(color=NOCTURNAL_PALETTE["cyan"], width=3),
                    hovertemplate="<b>Pilihan A</b> (Minggu %{x}): %{y:,.0f} Pesanan<extra></extra>",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=weeks,
                    y=duel_res["traj_b_volume"],
                    mode="lines+markers",
                    name="Pilihan B: Disiplin Kurir",
                    line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                    hovertemplate="<b>Pilihan B</b> (Minggu %{x}): %{y:,.0f} Pesanan<extra></extra>",
                )
            )
        else:
            sim_res = duel_engine.simulate_what_if(
                subsidy_pct=slider_subsidy,
                delay_days_delta=slider_delay,
                quality_pct=slider_quality,
            )
            weeks = sim_res["weeks"]
            fig = go.Figure()
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
            fig.add_trace(
                go.Scatter(
                    x=weeks,
                    y=sim_res["pessimistic_trajectory"],
                    mode="lines",
                    line=dict(color="rgba(56, 189, 248, 0.2)", width=1),
                    fill="tonexty",
                    fillcolor="rgba(56, 189, 248, 0.08)",
                    name="Rentang Kemungkinan",
                    hoverinfo="skip",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=weeks,
                    y=sim_res["expected_trajectory"],
                    mode="lines+markers",
                    name="Proyeksi Pilihan Baru",
                    line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                    hovertemplate="<b>Pilihan Baru</b> (Minggu %{x}): %{y:,.0f} Pesanan<extra></extra>",
                )
            )
            base_weekly = [sim_res["current_volume"] / 12.0 for _ in weeks]
            fig.add_trace(
                go.Scatter(
                    x=weeks,
                    y=base_weekly,
                    mode="lines",
                    name="Kondisi Saat Ini",
                    line=dict(color=NOCTURNAL_PALETTE["cyan"], width=2.5, dash="dash"),
                    hovertemplate="<b>Kondisi Saat Ini</b>: %{y:,.0f} Pesanan<extra></extra>",
                )
            )
        fig = nocturnal_plotly_theme(fig, height=440, show_axes=True)
        fig.update_xaxes(title="Minggu Proyeksi", tickmode="linear", dtick=1)
        fig.update_yaxes(title="Volume Pesanan Mingguan")

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------------------------------------------------------------
# KARTU KESIMPULAN UTAMA (TOP STORY CARD & 3 METRIC TILES)
# ---------------------------------------------------------------------
def render_main_story_card(engine_output: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
    """Render top human narrative card with 3 prominent metric tiles."""
    if engine_output is None:
        engine_output = {}
    story = engine_output.get("story_summary", {})
    params = engine_output.get("parameters", {})
    headline = story.get("headline", "Hasil Analisis Perilaku Pelanggan")
    insight = story.get("insight", "Sistem telah memetakan dinamika perilaku dari masalah yang Anda masukkan.")

    retention_val = params.get("retention_prob_pct", 89.2)
    bp_val = params.get("breaking_point_day", 3.0)
    tol_val = params.get("max_tolerance_days", 2.5)

    st.markdown(f"""
    <div style="background: rgba(20, 25, 38, 0.82); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 4px solid #F5B041; border-radius: 18px; padding: 1.5rem 2rem; margin-top: 1.25rem; margin-bottom: 2rem; box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.2em; color: #F5B041; font-weight: 600; margin-bottom: 0.4rem;">
            KESIMPULAN DARI MASALAH ANDA
        </div>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.85rem; font-weight: 600; color: #F4F1EA; margin-bottom: 0.5rem; line-height: 1.3;">
            "{headline}"
        </div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.96rem; color: #D5D9E2; line-height: 1.65; margin-bottom: 1.25rem; max-width: 900px;">
            {insight}
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1rem;">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 0.85rem 1.1rem;">
                <div style="font-size: 0.78rem; color: #8E95A5; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;">Peluang Bertahan</div>
                <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-weight: 700; color: #F5B041; line-height: 1.2; margin-top: 0.2rem;">
                    {retention_val:.1f}%
                </div>
                <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 0.2rem;">Kestabilan loyalitas</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 0.85rem 1.1rem;">
                <div style="font-size: 0.78rem; color: #8E95A5; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;">Titik Rawan Utama</div>
                <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-weight: 700; color: #F43F5E; line-height: 1.2; margin-top: 0.2rem;">
                    Hari ke-{bp_val:.1f}
                </div>
                <div style="font-size: 0.75rem; color: #8E95A5; margin-top: 0.2rem;">Kekecewaan anjlok tajam</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 0.85rem 1.1rem;">
                <div style="font-size: 0.78rem; color: #8E95A5; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;">Batas Toleransi Pembeli</div>
                <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.1rem; font-weight: 700; color: #38BDF8; line-height: 1.2; margin-top: 0.2rem;">
                    &le; {tol_val:.1f} Hari
                </div>
                <div style="font-size: 0.75rem; color: #8E95A5; margin-top: 0.2rem;">Ambang aman kesabaran</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# BABAK 1: PETA RASI BINTANG PERILAKU (SCATTERGL 1,500 POINTS)
# ---------------------------------------------------------------------
def render_canvas_act1_constellation(
    mode: str,
    parsed_query: Dict[str, Any],
    base_sample_df: Optional[pd.DataFrame] = None,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
    duel_engine: Optional[ScenarioDuelEngine] = None,
    **kwargs: Any,
) -> None:
    """Render Act 1: 1,500 celestial points shifting coordinates & colors mathematically."""
    st.markdown("<div id='act-1'></div>", unsafe_allow_html=True)
    params = parsed_query.get("parameters", {})
    dim_scores = parsed_query.get("dimension_scores", {})
    cost_s = dim_scores.get("cost_sensitivity", 0.25)
    time_f = dim_scores.get("time_friction", 0.25)
    trust_q = dim_scores.get("trust_quality", 0.25)

    delay_delta = params.get("delay_days_delta", 0.0)
    subsidy = params.get("subsidy_pct", 0.0)

    if base_sample_df is None or base_sample_df.empty:
        base_sample_df = pd.DataFrame()

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
                marker=dict(size=6.5, color=colors, opacity=0.88),
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
                marker=dict(size=9.5, color=colors, opacity=0.92, line=dict(color="#090A0F", width=1.5)),
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
        # Dynamic Constellation shifting with 1,500 points
        n_pts = min(1500, len(base_sample_df))
        sample_df = base_sample_df.iloc[:n_pts].copy() if not base_sample_df.empty else pd.DataFrame()

        if sample_df.empty:
            # Synthetic generation if empty
            np.random.seed(42)
            sample_df = pd.DataFrame({
                "buyer_lng": np.random.uniform(-55, -35, 1500),
                "buyer_lat": np.random.uniform(-30, -5, 1500),
                "delivery_delay_days": np.random.exponential(scale=2.0, size=1500) - 3.0,
                "freight_ratio": np.random.beta(2, 7, 1500),
                "review_score": np.random.choice([1, 2, 3, 4, 5], 1500, p=[0.1, 0.05, 0.1, 0.35, 0.4]),
                "customer_state": np.random.choice(["SP", "RJ", "MG", "RS", "PR"], 1500),
                "total_order_value": np.random.exponential(scale=140.0, size=1500) + 20.0,
            })

        # Mathematical coordinate shift based on active NLP dimensions
        # High cost sensitivity pulls points along x-axis; high time friction pushes them down; trust lifts them
        x_shift = (cost_s - 0.25) * 4.0 - (time_f - 0.25) * 2.0
        y_shift = -(time_f - 0.25) * 5.0 + (trust_q - 0.25) * 3.5

        xs = sample_df["buyer_lng"].to_numpy() + x_shift
        ys = sample_df["buyer_lat"].to_numpy() + y_shift

        # Mathematical color and size assignment based on dimensional pull
        colors = []
        sizes = []
        custom_info = []

        for idx, row in sample_df.iterrows():
            delays = row["delivery_delay_days"] + delay_delta
            freight = row["freight_ratio"] * (1.0 - subsidy / 100.0)
            score = row["review_score"]

            # Probability of point turning red / gold / blue / purple
            is_risk = (delays > 1.5) or (time_f > 0.35 and delays > 0.0) or (score <= 2)
            is_cost_sensitive = (freight > 0.25) or (cost_s > 0.35 and freight > 0.18)
            is_satisfied = (score >= 4 and delays <= 0.0) or (trust_q > 0.35 and score >= 3)

            if is_risk:
                colors.append(NOCTURNAL_PALETTE["crimson"])
                sizes.append(6.0 if time_f > 0.3 else 4.0)
                status_str = f"Rawan Kecewa (+{delays:.1f} Hari)"
            elif is_cost_sensitive:
                colors.append(NOCTURNAL_PALETTE["amethyst"])
                sizes.append(5.5 if cost_s > 0.3 else 4.0)
                status_str = f"Beban Ongkir Tinggi ({freight*100:.0f}%)"
            elif is_satisfied:
                colors.append(NOCTURNAL_PALETTE["gold"])
                sizes.append(5.0 if trust_q > 0.3 else 3.5)
                status_str = "Puas dan Tepat Waktu"
            else:
                colors.append(NOCTURNAL_PALETTE["cyan"])
                sizes.append(3.5)
                status_str = "Kondisi Netral"

            custom_info.append([
                row.get("customer_state", "Kota"),
                f"R$ {row.get('total_order_value', 120.0):,.0f}",
                status_str,
            ])

        # Dynamic title reflecting active focal point
        if time_f >= max(cost_s, trust_q):
            title = "Sorotan merah bara memperlihatkan pergeseran titik rawan akibat friksi waktu tunggu."
        elif cost_s >= max(time_f, trust_q):
            title = "Sorotan ungu memperlihatkan sebaran pembeli yang sangat peka terhadap beban biaya kirim."
        else:
            title = "Cahaya emas mendominasi pada kelompok pelanggan yang merasakan keandalan layanan."

        fig = go.Figure(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="markers",
                marker=dict(size=sizes, color=colors, opacity=0.88),
                customdata=np.array(custom_info),
                hovertemplate=(
                    "<span style='font-size:13px; font-weight:700; color:#F5B041;'>Pembeli di %{customdata[0]}</span><br>"
                    "<span style='color:#F4F1EA;'>Nilai Belanja: <b>%{customdata[1]}</b></span><br>"
                    "<span style='color:#38BDF8;'>Kondisi: <b>%{customdata[2]}</b></span>"
                    "<extra></extra>"
                ),
            )
        )

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
# BABAK 2: ALIRAN TITIK PATAH HATI & KURVA NON-LINEAR
# ---------------------------------------------------------------------
def render_canvas_act2_breaking_point(
    mode: str,
    parsed_query: Dict[str, Any],
    delay_curve_df: Optional[pd.DataFrame] = None,
    duel_engine: Optional[ScenarioDuelEngine] = None,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> None:
    """Render Act 2: Dynamic non-linear tension curve with moving breaking point threshold."""
    st.markdown("<div id='act-2'></div>", unsafe_allow_html=True)
    engine = duel_engine if duel_engine is not None else ScenarioDuelEngine()
    params = parsed_query.get("parameters", {})
    dim_scores = parsed_query.get("dimension_scores", {})
    trust_q = dim_scores.get("trust_quality", 0.25)
    cost_s = dim_scores.get("cost_sensitivity", 0.25)

    delay_shift = params.get("delay_days_delta", 0.0)
    friction = params.get("perceived_friction", 0.224)

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
        # Dynamic curve calculated from local engine with user parameters
        phenom = engine.dissect_phenomenon(
            delay_shift=delay_shift,
            friction_ratio=friction,
            trust_factor=float(0.70 + trust_q * 0.3),
        )
        days = np.array(phenom["delay_days"])
        scores = np.array(phenom["satisfaction"])
        cur_d = phenom["current_delay"]
        cur_s = phenom["current_score"]
        bp_day = phenom["breaking_point_day"]

        title = f"Titik patah kesabaran pembeli berada di hari ke-{bp_day:.1f} keterlambatan (Posisi Anda: {cur_d:+.1f} Hari)."

        fig = go.Figure()
        ontime = days <= 0
        late = days >= 0

        # On-Time stream (Gold)
        fig.add_trace(
            go.Scatter(
                x=days[ontime],
                y=scores[ontime],
                mode="lines+markers",
                name="Tepat Waktu",
                line=dict(color=NOCTURNAL_PALETTE["gold"], width=4),
                fill="tozeroy",
                fillcolor="rgba(245, 176, 65, 0.10)",
                hovertemplate="<b>Tepat Waktu (%{x} Hari)</b><br>Kepuasan: %{y:.2f} / 5.0<extra></extra>",
            )
        )

        # Late stream (Crimson)
        fig.add_trace(
            go.Scatter(
                x=days[late],
                y=scores[late],
                mode="lines+markers",
                name="Terlambat",
                line=dict(color=NOCTURNAL_PALETTE["crimson"], width=4),
                fill="tozeroy",
                fillcolor="rgba(244, 63, 94, 0.14)",
                hovertemplate="<b>Terlambat +%{x} Hari</b><br>Kepuasan Hancur: %{y:.2f} / 5.0<extra></extra>",
            )
        )

        # Highlight Current Query Position
        marker_color = NOCTURNAL_PALETTE["gold"] if cur_s >= 3.5 else NOCTURNAL_PALETTE["crimson"]
        fig.add_trace(
            go.Scatter(
                x=[cur_d],
                y=[cur_s],
                mode="markers",
                name="Posisi Rencana Anda",
                marker=dict(size=15, color="#FFFFFF", line=dict(color=marker_color, width=3.5)),
                hovertemplate=f"<b>Posisi Masalah Anda</b><br>Selisih: {cur_d:+.1f} Hari<br>Kepuasan: {cur_s:.1f} / 5.0<extra></extra>",
            )
        )

        # Dynamic Breaking Point Vertical Threshold Line & Annotation
        fig.add_vline(
            x=bp_day,
            line_width=2,
            line_dash="dash",
            line_color=NOCTURNAL_PALETTE["crimson"],
        )
        fig.add_annotation(
            x=bp_day,
            y=3.0,
            text=f"<b>Titik Patah Hati (Hari ke-{bp_day:.1f})</b><br><span style='font-size:10px;'>Kepuasan anjlok drastis</span>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowcolor=NOCTURNAL_PALETTE["crimson"],
            ax=0,
            ay=-48,
            font=dict(family="Plus Jakarta Sans", size=11, color=NOCTURNAL_PALETTE["ivory"]),
            bgcolor="rgba(20, 25, 38, 0.92)",
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
# BABAK 3: CERMIN DUA DUNIA & 3 LIVE SLIDERS
# ---------------------------------------------------------------------
def render_canvas_act3_dual_world(
    mode: str,
    parsed_query: Dict[str, Any],
    duel_engine: Optional[ScenarioDuelEngine] = None,
    csv_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> None:
    """Render Act 3: Side-by-side comparative simulation with 3 live glass sliders."""
    st.markdown("<div id='act-3'></div>", unsafe_allow_html=True)
    engine = duel_engine if duel_engine is not None else ScenarioDuelEngine()
    params = parsed_query.get("parameters", {})
    initial_subsidy = float(params.get("subsidy_pct", 20.0))
    initial_delay = float(params.get("delay_days_delta", 0.0))
    initial_quality = float(params.get("quality_trust_pct", 85.0))

    # 3 Glass Interactive Sliders (Cost, Speed, Quality)
    st.markdown("""
    <div style="background: rgba(20, 25, 38, 0.78); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; font-weight: 600; color: #F5B041; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.75rem;">
            TUAS PENGENDALI SIMULASI LANGSUNG (GERAKKAN UNTUK MENGUJI)
        </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        param_subsidy = st.slider(
            "Ubah Beban Biaya (Subsidi Ongkir %):",
            min_value=0.0,
            max_value=50.0,
            value=initial_subsidy,
            step=5.0,
            key="slider_subsidy_v3",
        )
    with col_s2:
        param_delay = st.slider(
            "Ubah Kecepatan Layanan (Hari Tiba):",
            min_value=-5.0,
            max_value=5.0,
            value=initial_delay,
            step=0.5,
            key="slider_delay_v3",
        )
    with col_s3:
        param_quality = st.slider(
            "Ubah Kualitas Pengalaman (Layanan %):",
            min_value=50.0,
            max_value=100.0,
            value=initial_quality,
            step=5.0,
            key="slider_quality_v3",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if mode == "adu":
        title = "Disiplin waktu kurir menghasilkan efisiensi modal dua koma delapan kali lebih tinggi."
        duel_res = engine.duel_two_options(
            subsidy_a=param_subsidy,
            delay_delta_b=param_delay,
            quality_b=param_quality,
        )
        weeks = duel_res["weeks"]

        fig = go.Figure()
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
        title = f"Proyeksi pergeseran volume dan kepuasan di bawah subsidi {param_subsidy:.0f}%, waktu {param_delay:+.1f} hari, dan kualitas {param_quality:.0f}%."
        sim_res = engine.simulate_what_if(
            subsidy_pct=param_subsidy,
            delay_days_delta=param_delay,
            quality_pct=param_quality,
        )
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
