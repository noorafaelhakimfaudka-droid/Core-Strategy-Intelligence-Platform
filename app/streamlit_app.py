import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy import stats
from scipy.ndimage import gaussian_filter1d
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.csip.data.semantic_profiler import build_fluent_schema, fmt_num, get_builtin_dataset

st.set_page_config(
    page_title="CSIP Studio — Ilmuwan Data Otomatis & Simulator Keputusan",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==============================================================================
# 1. CONTINUOUS ML & SIMULATION ENGINE (CROSS-DEVICE SAFE)
# ==============================================================================
def preprocess_intuitive_scales(df: pd.DataFrame, schema_info: dict) -> tuple[pd.DataFrame, dict]:
    work = df.copy()
    info = {k: dict(v) for k, v in schema_info.items()}

    for col in work.columns:
        if col not in info:
            continue
        c_low = col.lower()
        if any(w in c_low for w in ["rating", "skor", "score", "star", "kepuasan", "grade"]) and work[col].max() <= 5.2 and work[col].min() >= 0.8:
            work[col] = (work[col] * 20.0).round(1)
            info[col]["unit"] = "skala 100"
            if not info[col].get("description") or "1 sampai 5" in info[col].get("description", ""):
                info[col]["description"] = "skor yang distandardisasi ke skala 0-100 agar mudah diperbandingkan secara intuitif."
        elif work[col].min() < 0 and any(w in c_low for w in ["delay", "telat", "keterlambatan"]):
            work[col] = np.maximum(0.0, work[col]).round(1)

        if not info[col].get("description") or info[col].get("description") == "-":
            c_min = work[col].min()
            c_max = work[col].max()
            c_med = work[col].median()
            u_str = f" {info[col].get('unit', '')}".rstrip()
            info[col]["description"] = (
                f"variabel data dengan sebaran nilai dari {fmt_num(c_min)}{u_str} hingga {fmt_num(c_max)}{u_str} "
                f"(median {fmt_num(c_med)}{u_str})."
            )

    return work, info


@st.cache_resource
def run_studio_ml_engine(
    df_sig: int,
    df_sample: pd.DataFrame,
    target_col: str,
    candidate_cols: list[str],
    schema_info: dict,
    audit_info: dict,
) -> dict:
    work_df = df_sample[candidate_cols + [target_col]].copy()
    work_df = work_df.replace([np.inf, -np.inf], np.nan).dropna(subset=[target_col])

    if len(work_df) > 3500:
        work_df = work_df.sample(n=3500, random_state=42).reset_index(drop=True)

    imputer = SimpleImputer(strategy="median")
    X_full = pd.DataFrame(imputer.fit_transform(work_df[candidate_cols]), columns=candidate_cols)
    y = work_df[target_col].astype(float).values

    filtered_features = []
    dropped_collinear = []
    for col in candidate_cols:
        if X_full[col].std() <= 1e-9:
            continue
        r_with_target = abs(stats.pearsonr(X_full[col], y)[0]) if np.std(y) > 1e-9 else 0.0
        if r_with_target > 0.992 and len(candidate_cols) > 2:
            dropped_collinear.append(col)
            continue
        if any(abs(stats.pearsonr(X_full[col], X_full[k])[0]) > 0.94 for k in filtered_features):
            dropped_collinear.append(col)
            continue
        filtered_features.append(col)

    if len(filtered_features) < 2:
        filtered_features = candidate_cols[: max(2, len(candidate_cols))]

    X_raw = X_full[filtered_features].copy()
    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.25, random_state=42)
    t_unit = schema_info.get(target_col, {}).get("unit", "")
    short_unit = "poin" if "100" in t_unit else t_unit

    base_model = Ridge(alpha=1.0, random_state=42)
    base_model.fit(X_train, y_train)
    base_preds = base_model.predict(X_test)
    base_r2 = max(0.0, r2_score(y_test, base_preds) * 100.0)
    base_mae = mean_absolute_error(y_test, base_preds)

    # Gunakan n_jobs=1 agar tidak pernah crash multiprocessing di komputer/server dengan limit CPU ketat
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=1,
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rf_r2 = max(0.0, r2_score(y_test, preds) * 100.0)
    mae = mean_absolute_error(y_test, preds)

    model_quality_label = f"±{mae:.1f} {short_unit}".strip()
    benchmark_df = pd.DataFrame([
        {"Model Algoritma": "Random Forest Regressor (Utama)", "Variansi R²": f"{rf_r2:.1f}%", "Rata-rata Meleset (MAE)": f"±{mae:.2f}", "Status": "Model Terpilih"},
        {"Model Algoritma": "Ridge Linear Regression (Baseline)", "Variansi R²": f"{base_r2:.1f}%", "Rata-rata Meleset (MAE)": f"±{base_mae:.2f}", "Status": "Pembanding Dasar"},
    ])

    importances = pd.Series(model.feature_importances_, index=filtered_features).sort_values(ascending=False)
    top_features = importances.index.tolist()

    t_meta = schema_info.get(target_col, {})
    t_phrase = t_meta.get("phrase", target_col.lower())
    t_up = t_meta.get("verb_up", "meningkat")
    t_down = t_meta.get("verb_down", "merosot")

    corr_records = []
    for col in filtered_features:
        r_val, p_val = stats.pearsonr(X_raw[col], y) if (X_raw[col].std() > 1e-9 and np.std(y) > 1e-9) else (0.0, 1.0)
        f_meta = schema_info.get(col, {})
        f_phrase = f_meta.get("phrase", col.lower())
        f_up = f_meta.get("verb_up", "meningkat")
        f_unit = f_meta.get("unit", "")

        if r_val <= -0.05:
            natural_hint = f"Saat {f_phrase} {f_up}, {t_phrase} cenderung {t_down}."
            short_dir = "Berlawanan (-)"
        elif r_val >= 0.05:
            natural_hint = f"Saat {f_phrase} {f_up}, {t_phrase} ikut {t_up}."
            short_dir = "Searah (+)"
        else:
            natural_hint = f"Memengaruhi {t_phrase} ketika melewati titik batas tertentu."
            short_dir = "Titik Ambang"

        q_min = float(X_raw[col].quantile(0.02))
        q_med = float(X_raw[col].median())
        q_max = float(X_raw[col].quantile(0.98))
        if q_max <= q_min:
            q_min, q_max = float(X_raw[col].min()), float(X_raw[col].max()) + 1.0

        corr_records.append({
            "Fitur": col,
            "Frasa": f_phrase,
            "Verb_Up": f_up,
            "Verb_Down": f_meta.get("verb_down", "menurun"),
            "Unit": f_unit,
            "Arti_Kolom": f_meta.get("description", ""),
            "Kalimat_Alami": natural_hint,
            "Arah_Singkat": short_dir,
            "Pengaruh_Persen": float(importances[col] * 100.0),
            "Pearson_r": float(r_val),
            "p_value": float(p_val),
            "Min": q_min,
            "Median": q_med,
            "Max": q_max,
        })
    stats_df = pd.DataFrame(corr_records).sort_values("Pengaruh_Persen", ascending=False).reset_index(drop=True)

    top1_col = stats_df.iloc[0]["Fitur"]
    f1_unit = stats_df.iloc[0]["Unit"]
    f1_vals = X_raw[top1_col]

    if f1_vals.min() == 0 and (f1_vals == 0).mean() > 0.25:
        pos_vals = f1_vals[f1_vals > 0]
        cut_mid = float(pos_vals.median()) if len(pos_vals) > 0 else float(f1_vals.quantile(0.75))
        m1 = f1_vals <= 0.001
        m2 = (f1_vals > 0.001) & (f1_vals <= cut_mid)
        m3 = f1_vals > cut_mid
        g_meta = [
            {"tier": "Tingkat Nol / Nihil", "range": f"{top1_col} = 0", "mask": m1},
            {"tier": "Tingkat Rendah", "range": f"> 0 – {fmt_num(cut_mid, f1_unit)}", "mask": m2},
            {"tier": "Tingkat Tinggi", "range": f"> {fmt_num(cut_mid, f1_unit)}", "mask": m3},
        ]
    else:
        q33, q66 = float(f1_vals.quantile(0.33)), float(f1_vals.quantile(0.67))
        m1 = f1_vals <= q33
        m2 = (f1_vals > q33) & (f1_vals <= q66)
        m3 = f1_vals > q66
        g_meta = [
            {"tier": "Kelompok Bawah", "range": f"≤ {fmt_num(q33, f1_unit)}", "mask": m1},
            {"tier": "Kelompok Menengah", "range": f"{fmt_num(q33)} – {fmt_num(q66, f1_unit)}", "mask": m2},
            {"tier": "Kelompok Atas", "range": f"> {fmt_num(q66, f1_unit)}", "mask": m3},
        ]

    raw_groups = []
    for item in g_meta:
        mask = item["mask"]
        sub_y = y[mask]
        if len(sub_y) < 5:
            sub_y = y
        raw_groups.append({
            "tier": item["tier"],
            "range": item["range"],
            "title": f"{top1_col} {item['tier'].lower()} ({item['range']})",
            "count": int(np.sum(mask)) if np.sum(mask) > 0 else len(sub_y),
            "median": float(np.median(sub_y)),
            "mean": float(np.mean(sub_y)),
            "std": max(float(np.std(sub_y)), (float(np.max(y) - np.min(y)) * 0.06)),
        })
    ridge_groups = sorted(raw_groups, key=lambda d: d["median"], reverse=True)

    median_df = pd.DataFrame([X_raw.median()[filtered_features]])
    baseline_normal_val = float(model.predict(median_df)[0])

    audit_summary = dict(audit_info)
    audit_summary["dropped_collinear"] = dropped_collinear if dropped_collinear else ["Tidak ada kolom redundan"]

    return {
        "model": model,
        "feature_cols": filtered_features,
        "top_features": top_features,
        "stats_df": stats_df,
        "benchmark_df": benchmark_df,
        "audit_summary": audit_summary,
        "ridge_groups": ridge_groups,
        "X_median": X_raw.median(),
        "y_min": float(np.percentile(y, 2)),
        "y_max": float(np.percentile(y, 98)),
        "y_baseline": baseline_normal_val,
        "model_quality_label": model_quality_label,
        "n_rows": len(work_df),
    }


def simulate_studio(pipeline: dict, custom_inputs: dict, target_col: str, schema_info: dict) -> dict:
    row = pipeline["X_median"].copy()
    for col, val in custom_inputs.items():
        if col in row.index:
            row[col] = val

    X_in = pd.DataFrame([row[pipeline["feature_cols"]]])
    pred_val = float(pipeline["model"].predict(X_in)[0])
    base_val = pipeline["y_baseline"]

    top1_row = pipeline["stats_df"].iloc[0]
    top2_row = pipeline["stats_df"].iloc[1] if len(pipeline["stats_df"]) > 1 else top1_row
    top1 = top1_row["Fitur"]

    grid_x = np.linspace(top1_row["Min"], top1_row["Max"], 70)
    grid_df = pd.DataFrame([row[pipeline["feature_cols"]]] * 70)
    grid_df[top1] = grid_x
    grid_preds = gaussian_filter1d(pipeline["model"].predict(grid_df), sigma=2.5)

    base_grid_df = pd.DataFrame([pipeline["X_median"][pipeline["feature_cols"]]] * 70)
    base_grid_df[top1] = grid_x
    base_grid_preds = gaussian_filter1d(pipeline["model"].predict(base_grid_df), sigma=2.5)

    cur_f1_val = float(row[top1])
    smooth_pred = float(np.interp(cur_f1_val, grid_x, grid_preds))
    pred_val = 0.65 * smooth_pred + 0.35 * pred_val
    base_val = float(np.interp(float(pipeline["X_median"][top1]), grid_x, base_grid_preds))

    diff_val = pred_val - base_val
    diff_pct = (diff_val / (abs(base_val) + 1e-9)) * 100.0

    diffs = np.abs(np.diff(base_grid_preds))
    tipping_idx = int(np.argmax(diffs)) if len(diffs) > 0 else 35
    tipping_x = float(grid_x[tipping_idx])

    t_meta = schema_info.get(target_col, {})
    t_phrase = t_meta.get("phrase", target_col.lower())
    t_unit = t_meta.get("unit", "")
    short_unit = "poin" if "100" in t_unit else t_unit

    f1_phrase = top1_row["Frasa"]
    f1_unit = top1_row["Unit"]
    f1_share = top1_row["Pengaruh_Persen"]
    f2_phrase = top2_row["Frasa"]
    f2_share = top2_row["Pengaruh_Persen"]

    if top1_row["Pearson_r"] <= -0.05:
        headline_main = f"Kendalikan {top1.lower()} di bawah {fmt_num(tipping_x, f1_unit)}, agar"
        headline_em = f"{t_phrase} tetap stabil."
        act_1 = f"Prioritaskan kendali {top1.lower()}"
        act_2 = f"Cegah lewati batas {fmt_num(tipping_x, f1_unit)}"
    else:
        headline_main = f"Dorong {top1.lower()} mendekati {fmt_num(tipping_x, f1_unit)}, untuk"
        headline_em = f"mengoptimalkan {t_phrase}."
        act_1 = f"Optimalkan {top1.lower()} di atas {fmt_num(tipping_x, f1_unit)}"
        act_2 = f"Perkuat faktor #{2}: {top2_row['Fitur'].lower()}"

    dir_word = "lebih rendah" if diff_val < -0.05 else ("lebih tinggi" if diff_val > 0.05 else "relatif setara")
    delta_txt = f"{fmt_num(abs(diff_val))} {short_unit}".strip()

    narrative_body = (
        f"{top1} memegang <b>{f1_share:.0f}%</b> pengaruh terhadap {t_phrase}, lebih dominan daripada {f2_phrase} (<b>{f2_share:.0f}%</b>). "
        f"Pola perubahan data menunjukkan pergeseran nyata di sekitar titik kritis <b>{fmt_num(tipping_x, f1_unit)}</b>; pada posisi tuas "
        f"<b>{fmt_num(cur_f1_val, f1_unit)}</b> saat ini, estimasi model menghasilkan nilai yang {dir_word} "
        f"<b>{delta_txt}</b> ({diff_pct:+.1f}%) dibandingkan nilai acuan standar (<b>{fmt_num(base_val, short_unit)}</b>). "
        f"Menyesuaikan tuas <b>{top1.lower()}</b> memberikan respons terbesar pada {t_phrase}."
    )

    return {
        "pred_val": pred_val,
        "base_val": base_val,
        "diff_val": diff_val,
        "diff_pct": diff_pct,
        "grid_x": grid_x,
        "grid_preds": grid_preds,
        "base_grid_preds": base_grid_preds,
        "current_x": cur_f1_val,
        "tipping_x": tipping_x,
        "headline_main": headline_main,
        "headline_em": headline_em,
        "narrative_body": narrative_body,
        "act_1": act_1,
        "act_2": act_2,
    }


# ==============================================================================
# 2. THREE VISUAL LENSES
# ==============================================================================
def build_lens1_curve(pipeline: dict, sim: dict, target_col: str, schema_info: dict) -> go.Figure:
    top1_row = pipeline["stats_df"].iloc[0]
    top1 = top1_row["Fitur"]
    f1_unit = top1_row["Unit"]
    t_unit = schema_info.get(target_col, {}).get("unit", "")
    short_unit = "poin" if "100" in t_unit else t_unit

    x_min, x_max = float(np.min(sim["grid_x"])), float(np.max(sim["grid_x"]))
    y_all = np.concatenate([sim["grid_preds"], sim["base_grid_preds"], [sim["pred_val"], sim["base_val"]]])
    y_min, y_max = float(np.min(y_all)), float(np.max(y_all))
    y_span = max(y_max - y_min, 2.0)
    y_pad = y_span * 0.24

    fig = go.Figure()

    z_x0, z_x1 = (sim["tipping_x"], x_max) if top1_row["Pearson_r"] <= 0 else (x_min, sim["tipping_x"])
    fig.add_vrect(x0=z_x0, x1=z_x1, fillcolor="rgba(232, 162, 59, 0.10)", layer="below", line_width=0)

    fig.add_hline(
        y=sim["base_val"],
        line=dict(color="#7A756A", width=1.3, dash="dash"),
        annotation_text=f"Median {sim['base_val']:.1f}",
        annotation_position="top right",
        annotation_font=dict(family="Inter", size=12.5, color="#5A554B"),
    )

    fig.add_vline(x=sim["tipping_x"], line=dict(color="#E8A23B", width=1.6, dash="dash"))
    fig.add_annotation(
        x=sim["tipping_x"], y=y_max + y_pad * 0.55,
        text=f"<b>Titik kritis: {fmt_num(sim['tipping_x'], f1_unit)}</b>",
        showarrow=False,
        font=dict(family="Inter", size=12.5, color="#8A5A0C"),
        bgcolor="#FFF6E6", bordercolor="rgba(183, 121, 31, 0.35)", borderwidth=1, borderpad=6,
    )

    fig.add_trace(go.Scatter(
        x=sim["grid_x"], y=sim["grid_preds"], mode="lines",
        name="Prediksi skor",
        line=dict(color="#0E6B63", width=3.5, shape="spline"),
        fill="tozeroy", fillcolor="rgba(23, 163, 148, 0.15)",
        hovertemplate=f"<b>{top1}: %{{x:,.1f}} {f1_unit}</b><br>Prediksi: %{{y:,.1f}} {short_unit}<extra></extra>",
    ))

    fig.add_vline(x=sim["current_x"], line=dict(color="rgba(14, 107, 99, 0.45)", width=1.2, dash="dot"))
    fig.add_trace(go.Scatter(
        x=[sim["current_x"]], y=[sim["pred_val"]],
        mode="markers", name="Posisi tuas",
        marker=dict(size=14, color="#FFFFFF", line=dict(width=3.2, color="#0E6B63")),
        hoverinfo="skip",
    ))

    ax_offset = -75 if sim["current_x"] > (x_min + x_max) * 0.62 else 75
    fig.add_annotation(
        x=sim["current_x"], y=sim["pred_val"],
        text=f"Posisi tuas<br><b>{fmt_num(sim['current_x'], f1_unit)}, hasil {sim['pred_val']:.1f}</b>",
        showarrow=True, arrowhead=2, arrowcolor="#1D1B17", ax=ax_offset, ay=-26,
        align="left",
        font=dict(family="Inter", size=12.5, color="#FFFFFF"),
        bgcolor="#1D1B17", bordercolor="#1D1B17", borderwidth=1, borderpad=8,
    )

    fig.update_layout(
        height=345, margin=dict(l=18, r=18, t=26, b=22),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title=dict(text=f"{top1} ({f1_unit})" if f1_unit else top1, font=dict(family="Inter", size=13, color="#5A554B")),
            showgrid=False, zeroline=False,
            linecolor="rgba(34, 30, 24, 0.18)", tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        yaxis=dict(
            range=[y_min - y_pad * 0.35, y_max + y_pad * 0.9],
            showgrid=True, gridcolor="rgba(34, 30, 24, 0.07)", zeroline=False,
            tickfont=dict(family="Inter", size=12, color="#6A655A"),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(family="Inter", size=12, color="#5A554B"), bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


def build_lens2_ranking_html(pipeline: dict, target_col: str = "") -> str:
    st_df = pipeline["stats_df"].iloc[:5].copy()
    max_share = max(float(st_df["Pengaruh_Persen"].max()), 1.0)
    tgt_name = target_col.lower() if target_col else "target"

    rows_html = []
    for idx, row in st_df.iterrows():
        top_cls = "top" if idx == 0 else ""
        pct = float(row["Pengaruh_Persen"])
        width_pct = max(6.0, min(92.0, (pct / max_share) * 76.0))
        r_val = float(row["Pearson_r"])

        if r_val <= -0.05:
            sub_tag = f"Menurunkan {tgt_name}"
            dir_note = "makin tinggi, nilai turun"
        elif r_val >= 0.05:
            sub_tag = f"Menaikkan {tgt_name}"
            dir_note = "makin tinggi, nilai naik"
        else:
            sub_tag = "Pengaruh seimbang"
            dir_note = "cenderung netral"

        rows_html.append(
            f'<div class="rk {top_cls}" style="--w:{width_pct:.1f}%">'
            f'<div class="rk-name">{row["Fitur"]}<small>{sub_tag}</small></div>'
            f'<div class="rk-track"><div class="rk-bar"></div><div class="rk-num">{pct:.0f}%<em>{dir_note}</em></div></div>'
            f'</div>'
        )
    return '<div class="rank-list">' + "".join(rows_html) + "</div>"


def build_lens3_ridgeline_svg(pipeline: dict, sim: dict, target_col: str) -> str:
    groups = pipeline["ridge_groups"]
    y_min = pipeline["y_min"]
    y_max = pipeline["y_max"]
    span = max(y_max - y_min, 1.0)
    pad = span * 0.12
    dom_min = y_min - pad
    dom_max = y_max + pad
    dom_span = max(dom_max - dom_min, 1.0)

    # Pemisahan area gambar secara ketat agar label di kiri TIDAK AKAN PERNAH nabrak kurva/garis
    plot_left = 270.0
    plot_right = 835.0
    plot_width = plot_right - plot_left

    def to_svg_x(val: float) -> float:
        ratio = float(np.clip((val - dom_min) / dom_span, 0.0, 1.0))
        return plot_left + ratio * plot_width

    ticks = np.linspace(dom_min, dom_max, 5)
    grid_lines = "".join(
        f'<line x1="{to_svg_x(t):.1f}" x2="{to_svg_x(t):.1f}" y1="16" y2="295"/>' for t in ticks
    )
    tick_texts = "".join(
        f'<text x="{to_svg_x(t):.1f}" y="318">{fmt_num(t)}</text>' for t in ticks
    )

    baselines = [95, 192, 288]
    grad_ids = ["gA", "gB", "gC"]
    strokes = ["#17A394", "#E8A23B", "#B5432F"]

    labels_svg = []
    curves_svg = []

    for idx, g in enumerate(groups[:3]):
        by = baselines[idx]
        gid = grad_ids[idx]
        st_col = strokes[idx]

        tier_title = str(g.get("tier", f"Kelompok #{idx+1}"))
        range_cond = str(g.get("range", ""))
        count_num = g.get("count", 0)
        med_num = g.get("median", 0.0)

        # 1. Kolom Label di sisi kiri (X: 18 s.d. 245) - Aman dan tidak terpotong kurva
        labels_svg.append(
            f'<g transform="translate(18, {by})">'
            f'<circle cx="8" cy="-36" r="5" fill="{st_col}"/>'
            f'<text x="22" y="-32" font-size="13.5" font-weight="700" fill="#1A1814">{tier_title}</text>'
            f'<text x="22" y="-17" font-size="11.5" fill="#5A554B">{range_cond}</text>'
            f'<text x="22" y="-3" class="ax" font-size="10.5">{count_num:,} data • med. {fmt_num(med_num)}</text>'
            f'</g>'
        )

        # 2. Area Grafik di sisi kanan (X: 270 s.d. 835)
        cx = to_svg_x(med_num)
        half_w = float(np.clip((g["std"] / dom_span) * plot_width * 1.35, 55.0, 145.0))
        x0 = max(plot_left, cx - half_w)
        x1 = min(plot_right, cx + half_w)
        cx = (x0 + x1) / 2.0
        peak_y = by - 65.0
        c1 = x0 + (cx - x0) * 0.5
        c2 = cx + (x1 - cx) * 0.5

        path_d = f"M{x0:.1f},{by} C{c1:.1f},{by} {c1:.1f},{peak_y:.1f} {cx:.1f},{peak_y:.1f} C{c2:.1f},{peak_y:.1f} {c2:.1f},{by} {x1:.1f},{by} Z"
        curves_svg.append(
            f'<line x1="{plot_left}" x2="{plot_right}" y1="{by}" y2="{by}" stroke="rgba(34,30,24,.14)"/>'
            f'<path d="{path_d}" fill="url(#{gid})" stroke="{st_col}" stroke-width="1.8"/>'
        )

    sim_x = to_svg_x(sim["pred_val"])
    pill_x = float(np.clip(sim_x, plot_left + 64.0, plot_right - 64.0))

    svg_html = (
        '<div class="view3-wrap">'
        '<svg viewBox="0 0 860 348" preserveAspectRatio="xMidYMid meet" role="img" style="width:100%; height:auto; max-height:345px; display:block;">'
        '<defs>'
        '<linearGradient id="gA" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#17A394" stop-opacity=".55"/><stop offset="1" stop-color="#17A394" stop-opacity=".08"/></linearGradient>'
        '<linearGradient id="gB" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#E8A23B" stop-opacity=".55"/><stop offset="1" stop-color="#E8A23B" stop-opacity=".08"/></linearGradient>'
        '<linearGradient id="gC" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#B5432F" stop-opacity=".50"/><stop offset="1" stop-color="#B5432F" stop-opacity=".07"/></linearGradient>'
        '</defs>'
        f'<g stroke="rgba(34,30,24,.07)">{grid_lines}</g>'
        f'<g class="ax ax-mono" text-anchor="middle">{tick_texts}</g>'
        f'<line x1="250" x2="250" y1="16" y2="295" stroke="rgba(34,30,24,.10)" stroke-dasharray="3 3"/>'
        f'<text class="ax" x="{(plot_left + plot_right) / 2:.1f}" y="338" text-anchor="middle" font-weight="500">{target_col}</text>'
        + "".join(labels_svg)
        + "".join(curves_svg)
        + f'<g transform="translate({sim_x:.1f},0)">'
        '<line x1="0" x2="0" y1="18" y2="295" stroke="#1D1B17" stroke-width="1.4" stroke-dasharray="3 4"/>'
        '</g>'
        f'<g transform="translate({pill_x:.1f},16)">'
        '<rect x="-62" y="-12" width="124" height="24" rx="12" fill="#1D1B17"/>'
        f'<text x="0" y="4" text-anchor="middle" font-size="11.5" font-weight="600" fill="#fff">Simulasi {fmt_num(sim["pred_val"])}</text>'
        '</g></svg></div>'
    )
    return svg_html


# ==============================================================================
# 3. CROSS-DEVICE RESPONSIVE CSS & DEEP TEAL CONTRAST FIX
# ==============================================================================
PROTOTYPE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Inter:wght@400;450;500;600;700&display=swap');

:root {
  color-scheme: light only !important;
  --bg:            #F5F2EC;
  --bg-deep:       #EDE9E1;
  --surface:       #FFFFFF;
  --surface-soft:  #FBFAF7;
  --surface-tint:  #F1F6F3;
  --line:          rgba(34, 30, 24, .08);
  --line-strong:   rgba(34, 30, 24, .14);
  --ink:           #1A1814;
  --ink-2:         #3A362F;
  --ink-3:         #5A554B;
  --ink-4:         #6A655A;
  --accent:        #0E6B63;
  --accent-2:      #17A394;
  --accent-soft:   rgba(14, 107, 99, .10);
  --accent-ring:   rgba(14, 107, 99, .22);
  --good:          #25694A;
  --good-soft:     rgba(47, 125, 91, .12);
  --warn:          #8A5A0C;
  --warn-2:        #E8A23B;
  --warn-soft:     rgba(232, 162, 59, .16);
  --bad:           #B5432F;
  --bad-soft:      rgba(181, 67, 47, .10);
  --font-display:  "Fraunces", "Iowan Old Style", Georgia, serif;
  --font-ui:       "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}

#MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
  display: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  font-family: var(--font-ui) !important;
  color: var(--ink) !important;
  background: linear-gradient(155deg, #F8F4EC 0%, #F2EEE5 38%, #E8F0EB 72%, #F4EBDC 100%) !important;
  font-variant-numeric: tabular-nums;
}

.aurora-bg { position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }
.aurora-bg i { position: absolute; border-radius: 50%; filter: blur(90px); }
.aurora-bg i:nth-child(1) { width: 680px; height: 680px; right: -150px; top: -240px; opacity: .52; background: radial-gradient(circle at 35% 35%, #4FD1C0 0%, rgba(23,163,148,0) 68%); }
.aurora-bg i:nth-child(2) { width: 620px; height: 620px; left: -180px; bottom: -260px; opacity: .50; background: radial-gradient(circle at 55% 45%, #F7C46C 0%, rgba(232,162,59,0) 68%); }
.aurora-bg i:nth-child(3) { width: 520px; height: 520px; left: 34%; top: 26%; opacity: .28; background: radial-gradient(circle, #BDA8F2 0%, rgba(150,125,230,0) 70%); }

.block-container {
  position: relative; z-index: 1;
  padding-top: 0.65rem !important;
  padding-bottom: 1.0rem !important;
  padding-left: clamp(0.8rem, 2vw, 1.6rem) !important;
  padding-right: clamp(0.8rem, 2vw, 1.6rem) !important;
  max-width: 1620px !important;
}

.brand { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.logo-box {
  width: 26px; height: 26px; border-radius: 8px;
  background: linear-gradient(145deg, var(--accent-2), var(--accent) 70%);
  box-shadow: 0 1px 0 rgba(255,255,255,.4) inset, 0 0 16px rgba(23,163,148,.55), 0 4px 10px -3px rgba(14,107,99,.5);
  display: grid; place-items: center;
}
.brand-name { font-weight: 600; font-size: 16px; color: var(--ink); }
.badge-status {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12.5px; font-weight: 500; color: var(--accent);
  padding: 2px 10px 2px 8px; border-radius: 999px;
  background: var(--accent-soft); border: 1px solid var(--accent-ring);
}
.badge-status i { width: 6px; height: 6px; border-radius: 50%; background: var(--accent-2); box-shadow: 0 0 0 3px rgba(23,163,148,.22); }
.brand-sub { color: var(--ink-3); font-size: 13.5px; padding-left: 12px; border-left: 1px solid var(--line-strong); }

div[data-testid="stPopover"] > button,
div.stButton > button {
  background: rgba(255,255,255,.88) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: 10px !important;
  color: var(--ink-2) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  height: 34px !important;
  box-shadow: 0 1px 0 rgba(255,255,255,.9) inset, 0 1px 2px rgba(34,30,24,.05) !important;
}
div.stButton > button { border-radius: 999px !important; height: 28px !important; min-height: 28px !important; padding: 0 11px !important; }
div[data-testid="stPopover"] > button:hover,
div.stButton > button:hover {
  border-color: rgba(23,163,148,.5) !important;
  color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-ring) !important;
}

/* =========================================================
   1. KARTU KACA STANDAR (UNTUK KARTU YANG BUKAN DEEP TEAL)
   Ditaruh DI ATAS aturan Deep Teal agar tidak menimpa kartu pertama!
   ========================================================= */
div[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.step-source-teal-anchor)) {
  background: linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,255,255,.68)) !important;
  backdrop-filter: blur(20px) saturate(1.35) !important;
  border: 1px solid rgba(255,255,255,.84) !important;
  border-radius: 20px !important;
  padding: 15px 16px 16px !important;
  box-shadow: 0 0 0 1px rgba(34,30,24,.055), 0 1px 0 rgba(255,255,255,.95) inset, 0 20px 44px -26px rgba(12,70,64,.28) !important;
}

/* =========================================================
   2. KARTU SUMBER DATA DEEP TEAL (DITARUH DI BAWAH AGAR MENANG 100%!)
   ========================================================= */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) {
  position: relative !important;
  overflow: hidden !important;
  border-radius: 20px !important;
  padding: 16px 16px 18px !important;
  background:
    radial-gradient(320px 170px at 100% 0%, rgba(232,162,59,.28), transparent 70%),
    radial-gradient(300px 200px at 0% 100%, rgba(23,163,148,.38), transparent 70%),
    radial-gradient(rgba(255,255,255,.07) 1px, transparent 1.3px) 0 0 / 18px 18px,
    linear-gradient(160deg, #0F5A52 0%, #0A3F3A 55%, #072C29 100%) !important;
  border: 1px solid rgba(143,233,218,.28) !important;
  box-shadow:
    0 1px 0 rgba(255,255,255,.14) inset,
    0 0 0 1px rgba(6,40,38,.5),
    0 0 44px -10px rgba(23,163,148,.45),
    0 26px 50px -24px rgba(6,40,38,.75) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) div[data-testid="stWidgetLabel"] p {
  color: #D6F3EE !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) [data-testid="stFileUploaderDropzone"] {
  border: 1.5px dashed rgba(143,233,218,.55) !important;
  background: rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px !important;
  padding: 12px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) [data-testid="stFileUploaderDropzone"] * {
  color: #F4FBF9 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) [data-testid="stFileUploaderDropzone"] button {
  background: rgba(127,227,211,.24) !important;
  border: 1px solid rgba(143,233,218,.5) !important;
  color: #FFFFFF !important;
  border-radius: 8px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) div[data-baseweb="select"] > div {
  background: rgba(255,255,255,.10) !important;
  border: 1px solid rgba(191,237,230,.32) !important;
  border-radius: 10px !important;
  color: #FFFFFF !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.step-source-teal-anchor) div[data-baseweb="select"] * {
  color: #FFFFFF !important;
}

/* Header Langkah 1: Diberi Latar Kapsul Hijau Tua Mandiri supaya walau dibuka di browser jadul tetap 100% Terbaca Tajam! */
.step-head-teal {
  display: flex; align-items: center; gap: 10px; margin-bottom: 12px;
  padding: 8px 12px; border-radius: 12px;
  background: linear-gradient(90deg, rgba(7, 44, 41, 0.92), rgba(15, 90, 82, 0.85));
  border: 1px solid rgba(143, 233, 218, 0.28);
}
.step-no-teal {
  font-size: 12.5px; font-weight: 600; color: #BFEDE6;
  width: 22px; height: 22px; border-radius: 50%;
  background: rgba(255,255,255,.12); border: 1px solid rgba(191,237,230,.4);
  display: grid; place-items: center;
}
.step-title-teal { font-weight: 600; font-size: 14.5px; color: #FFFFFF !important; }
.step-hint-teal { margin-left: auto; font-size: 12px; color: #BFEDE6 !important; }

/* Kotak "Artinya begini": Diberi Latar Gelap Hangat Mandiri agar teks putihnya 100% Kontras di Semua Browser! */
.explain-amber {
  margin-top: 10px; padding: 12px 14px 13px; border-radius: 14px;
  background: linear-gradient(135deg, #164A44 0%, #2C3A2E 100%);
  border: 1px solid rgba(246,199,122,.45);
  box-shadow: 0 8px 20px -10px rgba(7, 44, 41, 0.5);
}
.explain-tag-amber { display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 600; color: #F6C77A !important; }
.explain-tag-amber::before { content: ""; width: 14px; height: 2px; background: #E8A23B; }
.explain-amber p { margin-top: 6px; font-size: 13.5px; line-height: 1.56; color: #F4FBF9 !important; }
.explain-amber b { color: #FFE099 !important; font-weight: 600; }

.step-head-light { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.step-no-light {
  font-size: 12.5px; font-weight: 600; color: var(--ink-3);
  width: 22px; height: 22px; border-radius: 50%;
  border: 1px solid var(--line-strong); display: grid; place-items: center;
  background: var(--surface-soft);
}
.step-title-light { font-weight: 600; font-size: 15px; color: var(--ink); }

/* Tuas Simulasi */
.lv-card-head { display: flex; align-items: center; gap: 11px; padding: 8px 4px 4px; margin-top: 4px; }
.lv-1 { --c1:#5FD8C6; --c2:#17A394; --ct:#0E6B63; --soft:rgba(23,163,148,.14); }
.lv-2 { --c1:#F6C77A; --c2:#E8A23B; --ct:#9A6317; --soft:rgba(232,162,59,.17); }
.lv-3 { --c1:#C9B8F5; --c2:#8F78E6; --ct:#5B43B5; --soft:rgba(143,120,230,.15); }

.lv-ico {
  flex: none; width: 35px; height: 35px; border-radius: 11px;
  display: grid; place-items: center; color: var(--ct);
  background: linear-gradient(145deg, #FFFFFF, var(--soft));
  box-shadow: 0 0 0 1px rgba(34,30,24,.06);
}
.lv-title { min-width: 0; flex: 1; }
.lv-name { display: block; font-weight: 600; font-size: 14.2px; color: var(--ink); line-height: 1.25; }
.lv-meta { display: flex; align-items: center; gap: 6px; margin-top: 3px; }
.lv-rank { font-size: 11.5px; color: var(--ink-3); padding: 1px 6px; border-radius: 6px; background: var(--bg); border: 1px solid var(--line); }
.lv-weight { font-size: 12px; font-weight: 500; color: var(--ct); background: var(--soft); padding: 1px 8px; border-radius: 999px; }
.lv-val { display: flex; align-items: baseline; gap: 4px; flex: none; font-family: var(--font-display); color: var(--ct); }
.lv-val b { font-weight: 500; font-size: clamp(20px, 1.8vw, 27px); line-height: 1; letter-spacing: -.01em; }
.lv-val small { font-family: var(--font-ui); font-size: 12.5px; color: var(--ink-3); }

.ticks-bar {
  height: 5px; margin: -8px 8px 0;
  background:
    linear-gradient(rgba(34,30,24,.20), rgba(34,30,24,.20)) right / 1px 100% no-repeat,
    repeating-linear-gradient(90deg, rgba(34,30,24,.18) 0 1px, transparent 1px 10%);
}
.scale-row {
  display: flex; justify-content: space-between;
  font-size: 11.5px; color: var(--ink-4); margin: 2px 4px 6px;
}
.lv-note {
  margin-top: 4px; margin-bottom: 10px; padding: 7px 10px 7px 12px;
  border-radius: 10px; font-size: 13px; line-height: 1.45; color: var(--ink-2);
  background: linear-gradient(90deg, var(--soft), rgba(255,255,255,0) 90%);
  border-left: 2.5px solid var(--c2);
}

div[data-baseweb="slider"] > div > div { height: 9px !important; border-radius: 999px !important; }
div[data-baseweb="slider"] div[role="slider"] {
  width: 22px !important; height: 22px !important;
  background: radial-gradient(circle at center, #17A394 0 4px, #fff 5px) !important;
  border: 2px solid #17A394 !important;
  box-shadow: 0 3px 8px rgba(34,30,24,.25), 0 0 0 5px rgba(23,163,148,.14) !important;
}
div[data-baseweb="slider"] div[role="slider"] * { display: none !important; }
div[data-testid="stThumbValue"], div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] { display: none !important; }

/* Segmented Control Pills */
div[data-testid="stRadio"] > div[role="radiogroup"] {
  background: rgba(237, 233, 225, 0.85) !important;
  padding: 3px !important; border-radius: 999px !important;
  border: 1px solid var(--line) !important;
  display: inline-flex !important; gap: 2px !important; flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] {
  background: transparent !important; border: none !important;
  padding: 6px 12px !important; border-radius: 999px !important;
  margin: 0 !important; cursor: pointer !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
div[data-testid="stRadio"] label[data-baseweb="radio"] p {
  font-size: 12.8px !important; font-weight: 500 !important; color: var(--ink-3) !important; white-space: nowrap !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
  background: linear-gradient(180deg, #FFFFFF, #EAF6F2) !important;
  box-shadow: 0 0 0 1px rgba(14,107,99,.25), 0 6px 18px -6px rgba(23,163,148,.55) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
  color: var(--accent) !important; font-weight: 600 !important;
}

/* Bento Cards Responsif Lintas Layar */
@property --ang { syntax:"<angle>"; inherits:false; initial-value:0deg; }
@keyframes spin { to { --ang:360deg; } }

.bento { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-bottom: 14px; }
.bento-card {
  position: relative; overflow: hidden; border-radius: 20px; padding: 14px 16px 14px;
  border: 1px solid rgba(255,255,255,.85);
  box-shadow: 0 0 0 1px rgba(34,30,24,.055), 0 1px 0 rgba(255,255,255,.95) inset, 0 20px 44px -26px rgba(12,70,64,.28);
}
.bento-card.c1 { background: radial-gradient(300px 150px at 100% 0%, var(--tint, rgba(232,162,59,.28)), transparent 72%), linear-gradient(180deg, rgba(255,255,255,.90), rgba(255,255,255,.68)); }
.bento-card.c1::before {
  content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.5px; pointer-events: none;
  background: conic-gradient(from var(--ang), rgba(23,163,148,0) 0deg, #17A394 70deg, #E8A23B 140deg, rgba(232,162,59,0) 220deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  animation: spin 7s linear infinite; opacity: .9;
}
.bento-card.c2 { background: radial-gradient(300px 150px at 100% 0%, rgba(23,163,148,.28), transparent 72%), linear-gradient(180deg, rgba(255,255,255,.90), rgba(255,255,255,.68)); }
.bento-card.c3 { background: radial-gradient(300px 150px at 100% 0%, var(--tint, rgba(232,162,59,.28)), transparent 72%), linear-gradient(180deg, rgba(255,255,255,.90), rgba(255,255,255,.68)); }

.card-label { display: flex; align-items: center; justify-content: space-between; font-size: 13px; font-weight: 500; color: var(--ink-3); gap: 8px; flex-wrap: wrap; }
.pill { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 500; padding: 2px 9px; border-radius: 999px; white-space: nowrap; }
.pill i { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.pill.good { color: var(--good); background: var(--good-soft); }
.pill.warn { color: var(--warn); background: var(--warn-soft); }
.pill.bad  { color: var(--bad);  background: var(--bad-soft); }

.big {
  display: flex; align-items: baseline; gap: 8px; margin-top: 8px; flex-wrap: wrap;
  font-family: var(--font-display); font-weight: 500; letter-spacing: -.02em;
  font-size: clamp(28px, 2.6vw, 42px); line-height: 1.05;
  background: linear-gradient(100deg, #1D1B17 0%, #0E6B63 45%, #17A394 70%, #1D1B17 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
}
.big small { font-family: var(--font-ui); font-size: 13px; font-weight: 400; -webkit-text-fill-color: var(--ink-3); color: var(--ink-3); letter-spacing: 0; }
.big.sm { font-size: clamp(19px, 1.6vw, 24px); letter-spacing: -.01em; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }
.big.pos { background-image: linear-gradient(100deg, #2F7D5B, #17A394 55%, #2F7D5B); }
.big.neg { background-image: linear-gradient(100deg, #B5432F, #E0763A 55%, #B5432F); }

.meter { height: 5px; border-radius: 999px; background: rgba(34,30,24,.08); overflow: hidden; margin-top: 10px; }
.meter i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--accent-2), var(--accent)); box-shadow: 0 0 12px rgba(23,163,148,.55); }
.tol { position: relative; height: 5px; border-radius: 999px; background: rgba(34,30,24,.08); margin-top: 10px; }
.tol i { position: absolute; top: 0; bottom: 0; left: 36%; width: 28%; border-radius: 999px; background: var(--warn-2); box-shadow: 0 0 12px rgba(232,162,59,.65); }
.tol em { position: absolute; top: -3px; left: 50%; width: 2px; height: 11px; margin-left: -1px; background: var(--ink); border-radius: 2px; }

.card-foot { margin-top: 9px; font-size: 12.8px; color: var(--ink-3); display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.card-foot b { color: var(--ink-2); font-weight: 600; }

.eyebrow { font-size: 12.5px; font-weight: 600; color: var(--ink-3); }
.chart-headline { margin-top: 2px; font-family: var(--font-display); font-weight: 500; font-size: clamp(17px, 1.5vw, 21px); letter-spacing: -.01em; line-height: 1.28; color: var(--ink); }

.rank-list { display: flex; flex-direction: column; justify-content: center; gap: 14px; padding: 18px 8px 14px; min-height: 340px; }
.rk { display: grid; grid-template-columns: minmax(140px, 210px) 1fr; align-items: center; gap: 14px; }
.rk-name { font-size: 14px; font-weight: 500; color: var(--ink-2); line-height: 1.25; }
.rk-name small { display: block; font-size: 12px; font-weight: 400; color: var(--ink-3); margin-top: 2px; }
.rk-track { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.rk-bar { height: 22px; border-radius: 6px; width: var(--w, 40%); background: linear-gradient(90deg, rgba(14,107,99,.75), rgba(23,163,148,.45)); box-shadow: 0 8px 18px -10px rgba(14,107,99,.5); }
.rk.top .rk-bar { background: linear-gradient(90deg, #0E6B63, #17A394 60%, #5FD8C6); box-shadow: 0 0 0 1px rgba(23,163,148,.25), 0 0 22px rgba(23,163,148,.5), 0 10px 22px -8px rgba(23,163,148,.55); }
.rk-num { font-size: 14px; font-weight: 500; color: var(--ink); white-space: nowrap; }
.rk.top .rk-num { color: var(--accent); }
.rk-num em { font-style: normal; font-size: 12.5px; color: var(--ink-3); font-weight: 400; margin-left: 8px; }

.ax { font-family: var(--font-ui); font-size: 13px; fill: #5A554B; }
.ax-mono { font-size: 12.5px; fill: #6A655A; }

/* Kartu Narasi Nara Responsif */
.narrative-card {
  margin-top: 14px;
  display: grid; grid-template-columns: auto minmax(200px, .92fr) minmax(240px, 1.15fr); gap: 20px; align-items: center;
  padding: 16px 20px; border-radius: 20px;
  background:
    radial-gradient(540px 210px at 0% 0%, rgba(232,162,59,.28), transparent 70%),
    radial-gradient(540px 230px at 100% 100%, rgba(23,163,148,.20), transparent 70%),
    linear-gradient(180deg, rgba(255,255,255,.90), rgba(255,255,255,.70));
  border: 1px solid rgba(255,255,255,.86);
  box-shadow: 0 0 0 1px rgba(232,162,59,.24), 0 1px 0 rgba(255,255,255,.95) inset, 0 0 42px -10px rgba(232,162,59,.34), 0 22px 44px -26px rgba(12,70,64,.28);
}
.persona { position: relative; width: 104px; display: grid; justify-items: center; gap: 6px; }
.avatar-svg { width: 84px; height: 84px; filter: drop-shadow(0 8px 16px rgba(14,107,99,.42)); }
.nametag { display: flex; flex-direction: column; align-items: center; line-height: 1.15; text-align: center; }
.nametag b { font-family: var(--font-display); font-weight: 500; font-size: 16px; color: var(--ink); }
.nametag span { font-size: 12px; color: var(--ink-3); margin-top: 2px; }
.glyph {
  position: absolute; z-index: 2; font-size: 12px; font-weight: 600; line-height: 1;
  color: var(--accent); background: rgba(255,255,255,.92);
  border: 1px solid rgba(14,107,99,.28); border-radius: 7px; padding: 3px 5px;
  box-shadow: 0 0 12px rgba(23,163,148,.4);
}
.glyph.g1 { top: 0; left: -2px; }
.glyph.g2 { top: 24px; right: -4px; color: var(--warn); border-color: rgba(183,121,31,.35); }
.glyph.g3 { bottom: 36px; left: -4px; }

.narr-tag { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 12.5px; font-weight: 600; color: var(--warn); }
.narr-tag::before { content: ""; width: 16px; height: 1.5px; background: var(--warn-2); }
.headline { font-family: var(--font-display); font-weight: 500; font-size: clamp(20px, 1.8vw, 25px); line-height: 1.2; letter-spacing: -.01em; color: var(--ink); }
.headline em {
  font-style: normal; font-weight: 600;
  background: linear-gradient(90deg, #0E6B63, #17A394, #D98A2B);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
}
.narr-body { font-size: 13.5px; line-height: 1.62; color: var(--ink-2); border-left: 1px solid var(--line-strong); padding-left: 18px; }
.narr-body b { font-weight: 600; color: var(--ink); }
.act-pills { display: flex; gap: 8px; margin-top: 9px; flex-wrap: wrap; }
.act-pills span {
  font-size: 12px; font-weight: 500; padding: 3px 10px; border-radius: 999px;
  background: var(--accent-soft); color: var(--accent); border: 1px solid var(--accent-ring);
}

/* Media Queries Lintas Device (Laptop 13", Tablet, High-DPI Scaling) */
@media (max-width: 1250px) {
  .bento { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)) !important; }
  .narrative-card { grid-template-columns: auto 1fr !important; gap: 14px !important; }
  .narr-body { grid-column: 1 / -1 !important; border-left: 0 !important; padding-left: 0 !important; border-top: 1px solid var(--line) !important; padding-top: 10px !important; }
  .brand-sub { display: none !important; }
}
@media (max-width: 768px) {
  .bento { grid-template-columns: 1fr !important; }
  .narrative-card { grid-template-columns: 1fr !important; text-align: center !important; }
  .persona { justify-self: center !important; }
  .act-pills { justify-content: center !important; }
  .rk { grid-template-columns: 1fr !important; gap: 6px !important; }
}
</style>
<div class="aurora-bg" aria-hidden="true"><i></i><i></i><i></i></div>
"""
st.markdown(PROTOTYPE_CSS, unsafe_allow_html=True)

NARA_AVATAR_SVG = (
    '<div class="persona">'
    '<span class="glyph g1">&Sigma;</span>'
    '<span class="glyph g2">&pi;</span>'
    '<span class="glyph g3">&Delta;</span>'
    '<svg class="avatar-svg" viewBox="0 0 120 120" role="img" aria-label="Avatar Nara">'
    '<defs>'
    '<radialGradient id="avBg" cx="35%" cy="25%" r="90%"><stop offset="0" stop-color="#1B7C71"/><stop offset=".55" stop-color="#0B4540"/><stop offset="1" stop-color="#072725"/></radialGradient>'
    '<linearGradient id="avCoat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E5A53"/><stop offset="1" stop-color="#0A2F2C"/></linearGradient>'
    '<linearGradient id="avSkin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F5D0AC"/><stop offset="1" stop-color="#DDA27A"/></linearGradient>'
    '<linearGradient id="avRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7FE3D3"/><stop offset=".55" stop-color="#17A394"/><stop offset="1" stop-color="#E8A23B"/></linearGradient>'
    '<clipPath id="avClip"><circle cx="60" cy="60" r="55"/></clipPath>'
    '</defs>'
    '<circle cx="60" cy="60" r="56" fill="url(#avBg)"/>'
    '<g clip-path="url(#avClip)">'
    '<circle cx="60" cy="52" r="34" fill="rgba(127,227,211,.16)"/>'
    '<path d="M10 124 C12 96 32 85 60 85 C88 85 108 96 110 124 Z" fill="url(#avCoat)"/>'
    '<path d="M47 86 L60 110 L73 86 Z" fill="#F5F2EC"/>'
    '<path d="M60 93 L51 88 L51 98 Z M60 93 L69 88 L69 98 Z" fill="#E8A23B"/>'
    '<circle cx="60" cy="93" r="2.8" fill="#F6C77A"/>'
    '<path d="M51 72 L51 87 Q60 94 69 87 L69 72 Z" fill="#D69A72"/>'
    '<ellipse cx="60" cy="58" rx="21" ry="24" fill="url(#avSkin)"/>'
    '<path d="M38 58 C33 37 46 25 62 26 C80 27 89 42 82 58 C80 50 76 44 70 42 C62 48 48 46 38 58 Z" fill="#2B2420"/>'
    '<path d="M45 52 Q51.5 49 57 52 M63 52 Q68.5 49 75 52" stroke="#2B2420" stroke-width="1.7" fill="none" stroke-linecap="round"/>'
    '<circle cx="52" cy="60" r="1.6" fill="#1D1B17"/><circle cx="68" cy="60" r="1.6" fill="#1D1B17"/>'
    '<g fill="rgba(200,240,235,.22)" stroke="#1D1B17" stroke-width="2"><circle cx="52" cy="60" r="7.8"/><circle cx="68" cy="60" r="7.8"/></g>'
    '<path d="M59.8 59 Q60 57.4 60.2 59" stroke="#1D1B17" stroke-width="1.8" fill="none"/>'
    '<path d="M53.5 75 Q60 79.5 66.5 75" stroke="#A5593F" stroke-width="1.7" fill="none" stroke-linecap="round"/>'
    '</g>'
    '<circle cx="60" cy="60" r="55" fill="none" stroke="url(#avRing)" stroke-width="2.2"/>'
    '</svg>'
    '<div class="nametag"><b>Nara</b><span>Penasihat strategi</span></div>'
    '</div>'
)

LEVER_ICONS = [
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 5.5h9v7h-9z"/><path d="M11.5 8h3.2l2.3 2.5v2h-5.5z"/><circle cx="6" cy="14.5" r="1.6"/><circle cx="14" cy="14.5" r="1.6"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4.5h14v9H9.5L6 16.5v-3H3z"/><path d="M6.5 8h7M6.5 10.5h4"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h7l7 7-7 7-7-7z"/><circle cx="7" cy="7" r="1.2"/></svg>',
]


# ==============================================================================
# 4. TOP BAR & COCKPIT LAYOUT
# ==============================================================================
top_l = st.container()
with top_l:
    st.markdown(
        '<div class="brand">'
        '<div class="logo-box" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 10 L5 6 L8 8.5 L12 3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
        '<span class="brand-name">CSIP Studio</span>'
        '<span class="badge-status"><i></i>Core Strategy & Intelligence Platform</span>'
        '<span class="brand-sub">Ilmuwan data otomatis dan simulator keputusan</span>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1px; background:linear-gradient(90deg, transparent, rgba(23,163,148,.55) 30%, rgba(232,162,59,.55) 70%, transparent); margin: 8px 0 14px 0;"></div>', unsafe_allow_html=True)

col_deck, col_stage = st.columns([1.05, 2.22], gap="medium")

with col_deck:
    with st.container(border=True):
        header_slot = st.empty()

        uploaded_csv = st.file_uploader(
            "Tarik berkas CSV ke sini, atau pilih dari komputer",
            type=["csv"],
        )

        preset_choice = st.selectbox(
            "Atau pakai dataset bawaan",
            options=[
                "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)",
                "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)",
                "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)",
            ],
        )

        if uploaded_csv is not None:
            raw_df = pd.read_csv(uploaded_csv)
            dataset_title = f"Berkas: {uploaded_csv.name}"
        else:
            raw_df = get_builtin_dataset(preset_choice)
            dataset_title = preset_choice

        active_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)
        active_df, schema_info = preprocess_intuitive_scales(active_df, schema_info)
        human_cols = list(schema_info.keys())

        if len(human_cols) < 2:
            st.error("Berkas CSV membutuhkan minimal 2 kolom angka untuk dibedah.")
            st.stop()

        header_slot.markdown(
            f'<div class="step-head-teal step-source-teal-anchor">'
            f'<span class="step-no-teal">1</span>'
            f'<span class="step-title-teal">Sumber data dan fokus</span>'
            f'<span class="step-hint-teal">{len(active_df):,} baris terbaca</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        target_idx = human_cols.index(auto_target) if auto_target in human_cols else len(human_cols) - 1
        target_col = st.selectbox(
            "Yang ingin dioptimalkan",
            options=human_cols,
            index=target_idx,
            key=f"target_select_{dataset_title}",
        )

        t_meta = schema_info[target_col]
        st.markdown(
            f'<div class="explain-amber">'
            f'<span class="explain-tag-amber">Artinya begini</span>'
            f'<p><b>{target_col}</b> adalah {t_meta["description"]}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    candidate_features = [c for c in human_cols if c != target_col]
    df_signature = hash((dataset_title, target_col, tuple(candidate_features), len(active_df)))
    pipeline = run_studio_ml_engine(df_signature, active_df, target_col, candidate_features, schema_info, audit_info)

    with st.container(border=True):
        head_c1, head_c2 = st.columns([2.1, 1.1], vertical_alignment="center")
        with head_c1:
            st.markdown(
                '<div class="step-head-light"><span class="step-no-light">2</span><span class="step-title-light">Tuas simulasi</span></div>',
                unsafe_allow_html=True,
            )
        with head_c2:
            reset_clicked = st.button("Setel ulang", use_container_width=True)

        custom_inputs = {}
        top_3_rows = pipeline["stats_df"].iloc[:3]

        for idx, (_, row_meta) in enumerate(top_3_rows.iterrows()):
            f_name = str(row_meta["Fitur"])
            f_min = float(row_meta["Min"])
            f_max = float(row_meta["Max"])
            f_med = float(row_meta["Median"])
            f_unit = str(row_meta["Unit"])
            if f_max <= f_min:
                f_max = f_min + 1.0
            step_val = round((f_max - f_min) / 100.0, 4) or 0.1

            default_start = f_med

            s_key = f"slider_v2_{dataset_title}_{target_col}_{idx}"
            if reset_clicked:
                st.session_state[s_key] = f_med
            elif s_key not in st.session_state:
                st.session_state[s_key] = default_start

            cur_v = float(np.clip(float(st.session_state[s_key]), f_min, f_max))
            st.session_state[s_key] = cur_v
            lv_cls = f"lv-{min(idx + 1, 3)}"
            ico_svg = LEVER_ICONS[min(idx, 2)]

            st.markdown(
                f'<div class="lv-card-head {lv_cls}">'
                f'<span class="lv-ico">{ico_svg}</span>'
                f'<div class="lv-title"><span class="lv-name">{f_name}</span>'
                f'<span class="lv-meta"><span class="lv-rank">#{idx+1}</span><span class="lv-weight">Bobot {row_meta["Pengaruh_Persen"]:.0f}%</span></span></div>'
                f'<div class="lv-val"><b>{fmt_num(cur_v)}</b><small>{f_unit}</small></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            val = st.slider(
                f_name,
                min_value=f_min,
                max_value=f_max,
                step=step_val,
                key=s_key,
                label_visibility="collapsed",
            )
            custom_inputs[f_name] = float(val)

            mid_scale = (f_min + f_max) / 2.0
            st.markdown(
                f'<div class="ticks-bar" aria-hidden="true"></div>'
                f'<div class="scale-row"><span>{fmt_num(f_min)}</span><span>{fmt_num(mid_scale)}</span><span>{fmt_num(f_max, f_unit)}</span></div>'
                f'<div class="lv-note {lv_cls}">{row_meta["Kalimat_Alami"]}</div>',
                unsafe_allow_html=True,
            )


sim = simulate_studio(pipeline, custom_inputs, target_col, schema_info)
top1_row = pipeline["stats_df"].iloc[0]
t_unit = schema_info[target_col]["unit"]
short_unit = "poin" if "100" in t_unit else t_unit



with col_stage:
    if sim["diff_pct"] >= 0.5:
        tone_cls = "good"
        pill_label = "Di atas standar"
        delta_cls = "pos"
        tint_rgba = "rgba(47,125,91,.28)"
    elif sim["diff_pct"] <= -8.0:
        tone_cls = "bad"
        pill_label = "Perlu perhatian"
        delta_cls = "neg"
        tint_rgba = "rgba(181,67,47,.26)"
    else:
        tone_cls = "warn"
        pill_label = "Di bawah standar" if sim["diff_val"] < -0.1 else "Setara standar"
        delta_cls = "neg" if sim["diff_val"] < -0.1 else "pos"
        tint_rgba = "rgba(232,162,59,.28)"

    f1_name_low = top1_row["Fitur"].lower()
    tgt_name_low = target_col.lower()
    if top1_row["Pearson_r"] < -0.05:
        dir_short_text = f"Makin tinggi, {tgt_name_low} turun"
    elif top1_row["Pearson_r"] > 0.05:
        dir_short_text = f"Makin tinggi, {tgt_name_low} naik"
    else:
        dir_short_text = "Pengaruh seimbang"

    bento_html = (
        f'<div class="bento">'
        f'<article class="bento-card c1" style="--tint:{tint_rgba};">'
        f'<div class="card-label">Estimasi {target_col} <span class="pill {tone_cls}"><i></i><span>{pill_label}</span></span></div>'
        f'<div class="big"><span>{fmt_num(sim["pred_val"])}</span> <small>{short_unit}</small></div>'
        f'<div class="card-foot">Nilai acuan standar <b>{fmt_num(sim["base_val"], short_unit)}</b></div>'
        f'</article>'
        f'<article class="bento-card c2">'
        f'<div class="card-label">Faktor penentu terkuat</div>'
        f'<div class="big sm" title="{top1_row["Fitur"]}">{top1_row["Fitur"]}</div>'
        f'<div class="meter"><i style="width:{min(100.0, top1_row["Pengaruh_Persen"]):.0f}%"></i></div>'
        f'<div class="card-foot"><b>{top1_row["Pengaruh_Persen"]:.0f}% pengaruh</b> <span>{dir_short_text}</span></div>'
        f'</article>'
        f'<article class="bento-card c3" style="--tint:{tint_rgba};">'
        f'<div class="card-label">Selisih dari standar</div>'
        f'<div class="big {delta_cls}"><span>{sim["diff_val"]:+.1f}</span> <small>{short_unit} ({sim["diff_pct"]:+.1f}%)</small></div>'
        f'<div class="tol" aria-hidden="true"><i></i><em></em></div>'
        f'<div class="card-foot">Toleransi estimasi sekitar <b>{pipeline["model_quality_label"]}</b></div>'
        f'</article>'
        f'</div>'
    )
    st.markdown(bento_html, unsafe_allow_html=True)

    with st.container(border=True):
        ch_l, ch_r = st.columns([1.05, 1.65], vertical_alignment="center")

        with ch_r:
            active_lens = st.radio(
                "Lensa tampilan",
                options=[
                    "1. Kurva Simulasi dan Titik Kritis",
                    "2. Peringkat Faktor Penentu",
                    "3. Sebaran Kelompok Data",
                ],
                horizontal=True,
                label_visibility="collapsed",
            )

        if active_lens == "1. Kurva Simulasi dan Titik Kritis":
            dynamic_chart_title = f"{target_col} mulai bergeser di sekitar {top1_row['Fitur'].lower()} {fmt_num(sim['tipping_x'], top1_row['Unit'])}"
        elif active_lens == "2. Peringkat Faktor Penentu":
            dynamic_chart_title = f"{top1_row['Fitur']} menyumbang {top1_row['Pengaruh_Persen']:.0f}% pengaruh terhadap {target_col.lower()}"
        else:
            dynamic_chart_title = f"Perbedaan sebaran {target_col.lower()} pada tiap tingkatan {top1_row['Fitur'].lower()}"

        with ch_l:
            st.markdown(
                f'<div><div class="eyebrow">Lensa tampilan</div><div class="chart-headline">{dynamic_chart_title}</div></div>',
                unsafe_allow_html=True,
            )

        if active_lens == "1. Kurva Simulasi dan Titik Kritis":
            fig = build_lens1_curve(pipeline, sim, target_col, schema_info)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        elif active_lens == "2. Peringkat Faktor Penentu":
            st.markdown(build_lens2_ranking_html(pipeline, target_col), unsafe_allow_html=True)
        else:
            st.markdown(build_lens3_ridgeline_svg(pipeline, sim, target_col), unsafe_allow_html=True)

    narrative_html = (
        f'<article class="narrative-card">'
        f'{NARA_AVATAR_SVG}'
        f'<div><div class="narr-tag">Kesimpulan untuk posisi tuas saat ini</div>'
        f'<h3 class="headline">{sim["headline_main"]} <em>{sim["headline_em"]}</em></h3></div>'
        f'<div class="narr-body">{sim["narrative_body"]}'
        f'<div class="act-pills"><span>{sim["act_1"]}</span><span>{sim["act_2"]}</span></div>'
        f'</div></article>'
    )
    st.markdown(narrative_html, unsafe_allow_html=True)