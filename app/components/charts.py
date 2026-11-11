"""CSIP Interactive Plotly Visualizations.

Provides:
- Cluster Scatter Chart (K-Means clusters with user simulation position)
- Partial Dependence Response Curve (Model predictions vs baseline response)
- Feature Importance & Pearson Correlation Ranking Chart

100% Real Computation, Local, Zero Emojis.
"""

from __future__ import annotations

from typing import Any, Dict
import numpy as np
import plotly.graph_objects as go


def build_real_scatter_chart(
    pipeline: Dict[str, Any],
    sim: Dict[str, Any],
    target_col: str,
    current_inputs: Dict[str, float],
) -> go.Figure:
    """Build multi-cluster scatter chart showing empirical distribution and live simulation diamond."""
    df = pipeline["plot_df"]
    if len(df) > 900:
        df = df.sample(n=900, random_state=42)

    f1 = pipeline["top_features"][0]
    f2 = pipeline["top_features"][1] if len(pipeline["top_features"]) > 1 else f1

    fig = go.Figure()
    color_map = {
        "high": ("#F5A623", "rgba(245, 166, 35, 0.16)"),
        "mid": ("#38BDF8", "rgba(56, 189, 248, 0.16)"),
        "low": ("#FB7185", "rgba(251, 113, 133, 0.18)"),
    }

    for g_key, (solid_col, glow_col) in color_map.items():
        sub = df[df["Group_Key"] == g_key]
        if sub.empty:
            continue
        label = sub["Segment_Label"].iloc[0]
        fig.add_trace(go.Scattergl(
            x=sub[f1], y=sub[f2], mode="markers",
            marker=dict(size=14, color=glow_col, line=dict(width=0)),
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scattergl(
            x=sub[f1], y=sub[f2], mode="markers", name=label,
            marker=dict(size=6.5, color=solid_col, opacity=0.88,
                        line=dict(width=0.8, color="rgba(255,255,255,0.3)")),
            customdata=sub[target_col],
            hovertemplate=(
                f"<b>{label}</b><br>"
                f"{f1}: %{{x:,.2f}}<br>"
                f"{f2}: %{{y:,.2f}}<br>"
                f"<b>{target_col}: %{{customdata:,.2f}}</b><extra></extra>"
            ),
        ))

    # Display active user simulation position on top of real empirical data
    cur_x = current_inputs.get(f1, float(pipeline["X_median"][f1]))
    cur_y = current_inputs.get(f2, float(pipeline["X_median"][f2]))
    fig.add_trace(go.Scatter(
        x=[cur_x], y=[cur_y], mode="markers+text",
        name="Posisi Simulasi Kamu Saat Ini",
        text=[f"  Prediksi: {sim['pred_val']:,.2f}"],
        textposition="middle right",
        textfont=dict(family="JetBrains Mono", size=11, color="#34D399"),
        marker=dict(size=16, color="#34D399", symbol="diamond",
                    line=dict(width=2.5, color="#FFFFFF")),
        hovertemplate=f"<b>Skenario Aktif</b><br>{f1}: %{{x:,.2f}}<br>{f2}: %{{y:,.2f}}<br>Prediksi {target_col}: {sim['pred_val']:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        height=410, margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(title=f"Faktor Penggerak #1: {f1}", showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94A3B8"),
        yaxis=dict(title=f"Faktor Penggerak #2: {f2}", showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94A3B8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10.5, color="#CBD5E1")),
    )
    return fig


def build_pdp_response_chart(
    pipeline: Dict[str, Any],
    sim: Dict[str, Any],
    target_col: str,
) -> go.Figure:
    """Build Partial Dependence Curve comparing user scenario response vs population baseline."""
    top1 = pipeline["top_features"][0]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["base_grid_preds"], mode="lines",
        name="Respons Dasar (Variabel Lain di Nilai Tengah)",
        line=dict(color="#38BDF8", width=2, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["grid_preds"], mode="lines",
        name="Kurva Respons Model pada Skenario Kamu",
        line=dict(color="#F5A623", width=3.5),
        fill="tozeroy", fillcolor="rgba(245, 166, 35, 0.10)",
    ))

    fig.add_vline(x=sim["current_x"], line=dict(color="#34D399", width=2, dash="dash"))
    fig.add_annotation(
        x=sim["current_x"], y=sim["pred_val"],
        text=f"POSISI TUAS ({sim['current_x']:,.2f}) -> {sim['pred_val']:,.2f}",
        showarrow=True, arrowhead=2, arrowcolor="#34D399", ax=40, ay=-30,
        font=dict(family="JetBrains Mono", size=10.5, color="#34D399"),
        bgcolor="rgba(15, 19, 29, 0.92)", bordercolor="#34D399", borderwidth=1, borderpad=5,
    )

    fig.update_layout(
        height=410, margin=dict(l=20, r=20, t=20, b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(title=f"Perubahan Nilai {top1} (Data Asli)", showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94A3B8"),
        yaxis=dict(title=f"Prediksi Model untuk {target_col}", showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94A3B8"),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(color="#CBD5E1")),
    )
    return fig


def build_feature_importance_chart(
    pipeline: Dict[str, Any],
    target_col: str,
) -> go.Figure:
    """Build horizontal bar chart of top feature importances and Pearson correlation directions."""
    st_df = pipeline["stats_df"].iloc[:8].sort_values("Importance", ascending=True)
    colors = ["#34D399" if r >= 0 else "#FB7185" for r in st_df["Pearson_r"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=st_df["Fitur"],
        x=st_df["Importance"] * 100.0,
        orientation="h",
        marker=dict(color=colors),
        customdata=np.stack([st_df["Pearson_r"], st_df["p_value"]], axis=-1),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Kontribusi ke Model: %{x:.1f}%<br>"
            "Korelasi Pearson (r): %{customdata[0]:+.3f}<br>"
            "Signifikansi (p-value): %{customdata[1]:.2e}<extra></extra>"
        ),
    ))

    fig.update_layout(
        height=410, margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(title=f"Kekuatan Pengaruh terhadap {target_col} (% Feature Importance)", showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
        yaxis=dict(color="#E2E8F0", tickfont=dict(size=12)),
    )
    return fig
