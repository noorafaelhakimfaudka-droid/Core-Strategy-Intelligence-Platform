import numpy as np
import plotly.graph_objects as go
from src.csip.data.semantic_profiler import fmt_num


def build_impact_curve_chart(pipeline: dict, sim: dict, target_col: str, schema_info: dict) -> go.Figure:
    top1_row = pipeline["stats_df"].iloc[0]
    top1 = top1_row["Fitur"]
    f1_unit = top1_row["Unit"]
    t_unit = schema_info.get(target_col, {}).get("unit", "")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["base_grid_preds"], mode="lines",
        name="Pola Dasar (Tuas Lain di Posisi Standar)",
        line=dict(color="#38BDF8", width=2, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["grid_preds"], mode="lines",
        name="Hasil Simulasi Tuas Kamu",
        line=dict(color="#F5A623", width=3.5),
        fill="tozeroy", fillcolor="rgba(245, 166, 35, 0.12)",
    ))

    fig.add_vline(x=sim["tipping_x"], line=dict(color="rgba(251, 113, 133, 0.6)", width=1.5, dash="dot"))
    fig.add_annotation(
        x=sim["tipping_x"], y=float(np.min(sim["base_grid_preds"])),
        text=f"Titik Kritis ({fmt_num(sim['tipping_x'], f1_unit)})",
        showarrow=False, yshift=14,
        font=dict(family="JetBrains Mono", size=10, color="#FB7185"),
    )

    fig.add_vline(x=sim["current_x"], line=dict(color="#34D399", width=2.2, dash="dash"))
    fig.add_annotation(
        x=sim["current_x"], y=sim["pred_val"],
        text=f"Tuas ({fmt_num(sim['current_x'], f1_unit)}) → {fmt_num(sim['pred_val'], t_unit)}",
        showarrow=True, arrowhead=2, arrowcolor="#34D399", ax=35, ay=-28,
        font=dict(family="JetBrains Mono", size=11, color="#34D399"),
        bgcolor="rgba(15, 19, 29, 0.92)", bordercolor="#34D399", borderwidth=1, borderpad=5,
    )

    fig.update_layout(
        height=395, margin=dict(l=20, r=20, t=20, b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(title=f"Perubahan {top1} →", showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
        yaxis=dict(title=f"Hasil {target_col} →", showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(color="#CBD5E1")),
    )
    return fig


def build_ranking_chart(pipeline: dict, target_col: str) -> go.Figure:
    """Grafik Peringkat Faktor dengan teks di LUAR ujung batang agar sangat kontras dan tajam."""
    st_df = pipeline["stats_df"].iloc[:7].sort_values("Pengaruh_Persen", ascending=True)
    colors = ["#34D399" if r >= 0 else "#FB7185" for r in st_df["Pearson_r"]]
    max_x = float(st_df["Pengaruh_Persen"].max()) if not st_df.empty else 50.0

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=st_df["Fitur"],
        x=st_df["Pengaruh_Persen"],
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.2)", width=1)),
        text=[f"  {v:.1f}%  •  {a}" for v, a in zip(st_df["Pengaruh_Persen"], st_df["Arah_Singkat"])],
        textposition="outside",
        textfont=dict(family="Inter", size=12, color="#F8FAFC"),
        cliponaxis=False,
        customdata=np.stack([st_df["Arti_Kolom"], st_df["Kalimat_Alami"]], axis=-1),
        hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br><b>%{customdata[1]}</b><extra></extra>",
    ))

    fig.update_layout(
        height=395, margin=dict(l=20, r=90, t=20, b=25),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(
            title=f"Besar Kendali terhadap {target_col} (%) →",
            range=[0, max(100.0, max_x * 1.32)],
            showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8",
        ),
        yaxis=dict(color="#F1F5F9", tickfont=dict(size=12.5)),
    )
    return fig


def build_cluster_map_chart(pipeline: dict, sim: dict, target_col: str, current_inputs: dict, schema_info: dict) -> go.Figure:
    df = pipeline["plot_df"]
    if len(df) > 850:
        df = df.sample(n=850, random_state=42)

    f1 = pipeline["top_features"][0]
    t_unit = schema_info.get(target_col, {}).get("unit", "")
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
            x=sub[f1], y=sub[target_col], mode="markers",
            marker=dict(size=13, color=glow_col, line=dict(width=0)),
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scattergl(
            x=sub[f1], y=sub[target_col], mode="markers", name=label,
            marker=dict(size=6.5, color=solid_col, opacity=0.88, line=dict(width=0.8, color="rgba(255,255,255,0.3)")),
            hovertemplate=f"<b>{label}</b><br>{f1}: %{{x:,.2f}}<br><b>{target_col}: %{{y:,.2f}}</b><extra></extra>",
        ))

    cur_x = current_inputs.get(f1, float(pipeline["X_median"][f1]))
    fig.add_trace(go.Scatter(
        x=[cur_x], y=[sim["pred_val"]], mode="markers+text",
        name="Posisi Skenario Kamu",
        text=[f"  {fmt_num(sim['pred_val'], t_unit)}"],
        textposition="middle right",
        textfont=dict(family="JetBrains Mono", size=11, color="#34D399"),
        marker=dict(size=16, color="#34D399", symbol="diamond", line=dict(width=2.5, color="#FFFFFF")),
    ))

    fig.update_layout(
        height=395, margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13, 17, 26, 0.55)",
        xaxis=dict(title=f"Faktor Utama: {f1} →", showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
        yaxis=dict(title=f"Hasil: {target_col} →", showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10.5, color="#CBD5E1")),
    )
    return fig


# Compatibility aliases for legacy names
build_pdp_response_chart = build_impact_curve_chart
build_feature_importance_chart = build_ranking_chart
build_real_scatter_chart = build_cluster_map_chart

