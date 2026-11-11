import numpy as np
import plotly.graph_objects as go
from src.csip.data.semantic_profiler import fmt_num


def build_impact_curve_chart(pipeline: dict, sim: dict, target_col: str, schema_info: dict) -> go.Figure:
    """Lensa 1: Kurva Simulasi dan Titik Kritis dengan estetika Warm Editorial Paper & Deep Teal."""
    top1_row = pipeline["stats_df"].iloc[0]
    top1 = top1_row["Fitur"]
    f1_unit = top1_row["Unit"]
    t_unit = schema_info.get(target_col, {}).get("unit", "")

    x_min, x_max = float(np.min(sim["grid_x"])), float(np.max(sim["grid_x"]))
    y_all = np.concatenate([sim["grid_preds"], sim["base_grid_preds"]])
    y_min, y_max = float(np.min(y_all)), float(np.max(y_all))
    y_pad = max((y_max - y_min) * 0.18, 0.5)

    fig = go.Figure()

    # Zona perhatian (amber lembut) setelah titik kritis
    if top1_row["Pearson_r"] <= 0:
        z_x0, z_x1 = sim["tipping_x"], x_max
    else:
        z_x0, z_x1 = x_min, sim["tipping_x"]

    fig.add_vrect(
        x0=z_x0, x1=z_x1,
        fillcolor="rgba(232, 162, 59, 0.10)",
        layer="below", line_width=0,
    )

    # Garis Median Standar
    fig.add_hline(
        y=sim["base_val"],
        line=dict(color="#7A756A", width=1.4, dash="dash"),
        annotation_text=f"Standar {fmt_num(sim['base_val'], t_unit)}",
        annotation_position="top right",
        annotation_font=dict(family="Inter", size=12, color="#5A554B"),
    )

    # Garis Titik Kritis (Amber)
    fig.add_vline(
        x=sim["tipping_x"],
        line=dict(color="#E8A23B", width=1.8, dash="dash"),
    )
    fig.add_annotation(
        x=sim["tipping_x"], y=y_max + y_pad * 0.45,
        text=f"<b>Titik kritis: {fmt_num(sim['tipping_x'], f1_unit)}</b>",
        showarrow=False,
        font=dict(family="Inter", size=12, color="#8A5A0C"),
        bgcolor="#FFF6E6", bordercolor="rgba(183, 121, 31, 0.38)", borderwidth=1, borderpad=6,
    )

    # Kurva Pola Dasar (Abu-abu hangat putus-putus)
    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["base_grid_preds"], mode="lines",
        name="Pola Dasar (Standar)",
        line=dict(color="rgba(90, 85, 75, 0.45)", width=2, dash="dot"),
        hovertemplate=f"{top1}: %{{x:,.2f}}<br>Standar {target_col}: %{{y:,.2f}}<extra></extra>",
    ))

    # Kurva Utama Simulasi (Deep Teal dengan area fill lembut)
    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["grid_preds"], mode="lines",
        name="Prediksi Simulasi",
        line=dict(color="#0E6B63", width=3.5),
        fill="tozeroy", fillcolor="rgba(23, 163, 148, 0.14)",
        hovertemplate=f"<b>{top1}: %{{x:,.2f}}</b><br>Prediksi {target_col}: %{{y:,.2f}}<extra></extra>",
    ))

    # Garis vertikal & Titik Posisi Tuas Saat Ini
    fig.add_vline(
        x=sim["current_x"],
        line=dict(color="rgba(14, 107, 99, 0.45)", width=1.2, dash="dot"),
    )
    fig.add_trace(go.Scatter(
        x=[sim["current_x"]], y=[sim["pred_val"]],
        mode="markers",
        name="Posisi Tuas",
        marker=dict(
            size=14, color="#FFFFFF",
            line=dict(width=3.2, color="#0E6B63"),
        ),
        hovertemplate=f"<b>Posisi Tuas Saat Ini</b><br>{top1}: {fmt_num(sim['current_x'], f1_unit)}<br>Hasil: {fmt_num(sim['pred_val'], t_unit)}<extra></extra>",
    ))

    # Kotak Tooltip Gelap ala Prototipe pada Posisi Tuas
    ax_offset = -55 if sim["current_x"] > (x_min + x_max) * 0.65 else 55
    fig.add_annotation(
        x=sim["current_x"], y=sim["pred_val"],
        text=f"Posisi tuas: <b>{fmt_num(sim['current_x'], f1_unit)}</b> → <b>{fmt_num(sim['pred_val'], t_unit)}</b>",
        showarrow=True, arrowhead=2, arrowcolor="#1D1B17", ax=ax_offset, ay=-34,
        font=dict(family="Inter", size=12, color="#FFFFFF"),
        bgcolor="#1D1B17", bordercolor="#0E6B63", borderwidth=1, borderpad=7,
    )

    fig.update_layout(
        height=350, margin=dict(l=18, r=18, t=28, b=24),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title=dict(text=f"{top1} ({f1_unit})" if f1_unit else top1, font=dict(family="Inter", size=13, color="#5A554B")),
            showgrid=False, zeroline=False,
            linecolor="rgba(34, 30, 24, 0.18)", tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        yaxis=dict(
            title=dict(text=target_col, font=dict(family="Inter", size=13, color="#5A554B")),
            range=[y_min - y_pad * 0.4, y_max + y_pad * 0.85],
            showgrid=True, gridcolor="rgba(34, 30, 24, 0.07)", zeroline=False,
            tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(family="Inter", size=12, color="#5A554B"), bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


def build_ranking_html(pipeline: dict) -> str:
    """Lensa 2: Merender Peringkat Faktor Penentu menggunakan HTML/CSS murni persis seperti prototipe."""
    st_df = pipeline["stats_df"].iloc[:5].copy()
    max_share = max(float(st_df["Pengaruh_Persen"].max()), 1.0)

    rows_html = []
    for idx, row in st_df.iterrows():
        top_cls = "top" if idx == 0 else ""
        pct = float(row["Pengaruh_Persen"])
        width_pct = max(6.0, min(96.0, (pct / max_share) * 78.0))
        r_val = float(row["Pearson_r"])

        if r_val <= -0.06:
            sub_tag = "Menekan hasil"
            dir_note = f"makin tinggi, hasil cenderung turun (r={r_val:+.2f})"
        elif r_val >= 0.06:
            sub_tag = "Mendorong hasil"
            dir_note = f"makin tinggi, hasil ikut naik (r={r_val:+.2f})"
        else:
            sub_tag = "Pengaruh ambang batas"
            dir_note = "bekerja pada titik keseimbangan tertentu"

        rows_html.append(
            f'<div class="rk {top_cls}" style="--w:{width_pct:.1f}%">'
            f'  <div class="rk-name">{row["Fitur"]}<small>{sub_tag} • {row["Arti_Kolom"][:60]}</small></div>'
            f'  <div class="rk-track">'
            f'    <div class="rk-bar"></div>'
            f'    <div class="rk-num">{pct:.1f}%<em>{dir_note}</em></div>'
            f'  </div>'
            f'</div>'
        )

    return '<div class="rank-list">' + "".join(rows_html) + "</div>"


def build_ranking_chart(pipeline: dict, target_col: str) -> go.Figure:
    """Fallback Plotly chart jika dipanggil secara eksternal."""
    st_df = pipeline["stats_df"].iloc[:6].sort_values("Pengaruh_Persen", ascending=True)
    colors = ["#0E6B63" if i == len(st_df) - 1 else "#17A394" for i in range(len(st_df))]
    max_x = float(st_df["Pengaruh_Persen"].max()) if not st_df.empty else 50.0

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=st_df["Fitur"], x=st_df["Pengaruh_Persen"], orientation="h",
        marker=dict(color=colors),
        text=[f"  {v:.1f}% ({a})" for v, a in zip(st_df["Pengaruh_Persen"], st_df["Arah_Singkat"])],
        textposition="outside",
        textfont=dict(family="Inter", size=12.5, color="#1A1814"),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=350, margin=dict(l=18, r=95, t=15, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, max(100.0, max_x * 1.35)], showgrid=True, gridcolor="rgba(34,30,24,0.07)", tickfont=dict(color="#5A554B")),
        yaxis=dict(tickfont=dict(family="Inter", size=12.5, color="#1A1814")),
    )
    return fig


def build_cluster_map_chart(pipeline: dict, sim: dict, target_col: str, current_inputs: dict, schema_info: dict) -> go.Figure:
    """Lensa 3: Sebaran Kelompok Data (K-Means) dengan palet Teal (#17A394), Amber (#E8A23B), dan Terracotta (#B5432F)."""
    df = pipeline["plot_df"]
    if len(df) > 850:
        df = df.sample(n=850, random_state=42)

    f1 = pipeline["top_features"][0]
    t_unit = schema_info.get(target_col, {}).get("unit", "")
    fig = go.Figure()

    color_map = {
        "high": ("#0E6B63", "rgba(23, 163, 148, 0.18)"),
        "mid": ("#D98A2B", "rgba(232, 162, 59, 0.20)"),
        "low": ("#B5432F", "rgba(181, 67, 47, 0.18)"),
    }

    for g_key, (solid_col, glow_col) in color_map.items():
        sub = df[df["Group_Key"] == g_key]
        if sub.empty:
            continue
        label = sub["Segment_Label"].iloc[0]
        fig.add_trace(go.Scattergl(
            x=sub[f1], y=sub[target_col], mode="markers",
            marker=dict(size=14, color=glow_col, line=dict(width=0)),
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scattergl(
            x=sub[f1], y=sub[target_col], mode="markers", name=label,
            marker=dict(size=7, color=solid_col, opacity=0.86, line=dict(width=1, color="#FFFFFF")),
            hovertemplate=f"<b>{label}</b><br>{f1}: %{{x:,.2f}}<br><b>{target_col}: %{{y:,.2f}}</b><extra></extra>",
        ))

    cur_x = current_inputs.get(f1, float(pipeline["X_median"][f1]))
    fig.add_trace(go.Scatter(
        x=[cur_x], y=[sim["pred_val"]], mode="markers+text",
        name="Posisi Simulasi Anda",
        text=[f"  Simulasi: {fmt_num(sim['pred_val'], t_unit)}"],
        textposition="middle right",
        textfont=dict(family="Inter", size=12, color="#1A1814"),
        marker=dict(size=15, color="#1D1B17", symbol="diamond", line=dict(width=2.5, color="#FFFFFF")),
    ))

    fig.update_layout(
        height=350, margin=dict(l=18, r=18, t=24, b=24),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title=dict(text=f"Faktor Penentu Utama: {f1}", font=dict(family="Inter", size=13, color="#5A554B")),
            showgrid=True, gridcolor="rgba(34, 30, 24, 0.07)", zeroline=False,
            tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        yaxis=dict(
            title=dict(text=target_col, font=dict(family="Inter", size=13, color="#5A554B")),
            showgrid=True, gridcolor="rgba(34, 30, 24, 0.07)", zeroline=False,
            tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(family="Inter", size=12, color="#5A554B"), bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig
