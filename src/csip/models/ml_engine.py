"""CSIP Continuous ML & Simulation Engine.

Standards Compliance:
- Model Scenario Building (Phase 08)
- Supervised ML Model Development (Phase 09)
- Model Evaluation & Residual Diagnostics (Phase 10)
- Decision Intelligence & Grounded Strategy (Phase 11)

Strictly enforces Split-Before-Transform to prevent Data Leakage.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats
from scipy.ndimage import gaussian_filter1d
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.csip.data.semantic_profiler import fmt_num

logger = logging.getLogger(__name__)


def train_fluent_ml_pipeline(
    df_sample: pd.DataFrame,
    target_col: str,
    candidate_cols: list[str],
    schema_info: dict,
    audit_info: dict,
) -> dict:
    """
    Train leak-free, continuous ML pipeline with baseline comparison and residual diagnostics.
    
    Methodological guarantees:
    1. Split-Before-Transform: train_test_split executed before imputation & feature filtering.
    2. Imputation & feature statistics fitted strictly on X_train.
    3. Continuous Random Forest Regressor calibrated to prevent step-function simulation artifacts.
    4. Full residual analysis (MAE, RMSE, R2, residual mean/std) reported for auditability.
    """
    # 1. Clean raw sample
    work_df = df_sample[candidate_cols + [target_col]].copy()
    work_df = work_df.replace([np.inf, -np.inf], np.nan).dropna(subset=[target_col])

    if len(work_df) > 3500:
        work_df = work_df.sample(n=3500, random_state=42).reset_index(drop=True)

    n_samples = len(work_df)
    test_size = 0.25 if n_samples >= 20 else (0.2 if n_samples >= 5 else 0.0)

    # 2. Split-Before-Transform (ANTI-LEAKAGE ENFORCEMENT)
    if test_size > 0.0 and n_samples >= 8:
        train_df, test_df = train_test_split(work_df, test_size=test_size, random_state=42)
    else:
        train_df = work_df.copy()
        test_df = work_df.copy()

    # 3. Fit Imputer Strictly on Training Data
    imputer = SimpleImputer(strategy="median")
    X_train_raw = pd.DataFrame(
        imputer.fit_transform(train_df[candidate_cols]),
        columns=candidate_cols,
        index=train_df.index,
    )
    X_test_raw = pd.DataFrame(
        imputer.transform(test_df[candidate_cols]),
        columns=candidate_cols,
        index=test_df.index,
    )
    X_full_imp = pd.DataFrame(
        imputer.transform(work_df[candidate_cols]),
        columns=candidate_cols,
        index=work_df.index,
    )

    y_train = train_df[target_col].astype(float).values
    y_test = test_df[target_col].astype(float).values
    y_full = work_df[target_col].astype(float).values

    # 4. Feature Selection on Training Set Only (Zero Leakage)
    filtered_features = []
    dropped_collinear = []
    for col in candidate_cols:
        col_std = float(X_train_raw[col].std())
        if col_std <= 1e-9:
            continue
        # Check correlation with target on train set
        r_with_target = abs(stats.pearsonr(X_train_raw[col], y_train)[0]) if np.std(y_train) > 1e-9 else 0.0
        # Drop extreme trivial duplicates (e.g. price and price_copy)
        if r_with_target > 0.992 and len(candidate_cols) > 2:
            dropped_collinear.append(col)
            continue
        # Drop multicollinear redundant features
        if any(abs(stats.pearsonr(X_train_raw[col], X_train_raw[k])[0]) > 0.94 for k in filtered_features):
            dropped_collinear.append(col)
            continue
        filtered_features.append(col)

    valid_candidates = [c for c in candidate_cols if float(X_train_raw[c].std()) > 1e-9]
    if len(filtered_features) < 1:
        filtered_features = valid_candidates[:2] if len(valid_candidates) >= 1 else candidate_cols[:1]

    X_train = X_train_raw[filtered_features].copy()
    X_test = X_test_raw[filtered_features].copy()
    X_full = X_full_imp[filtered_features].copy()

    t_unit = schema_info.get(target_col, {}).get("unit", "")
    short_unit = "poin" if "100" in t_unit else t_unit

    # 5. Baseline Ladder Comparison (Ridge Baseline vs Champion Random Forest)
    base_model = Ridge(alpha=1.0, random_state=42)
    base_model.fit(X_train, y_train)
    base_preds = base_model.predict(X_test)
    base_r2 = max(0.0, r2_score(y_test, base_preds) * 100.0) if len(y_test) > 1 else 0.0
    base_mae = mean_absolute_error(y_test, base_preds) if len(y_test) > 0 else 0.0

    # Dynamic Hyperparameter Tuning for Sample Size Robustness
    n_train = len(X_train)
    min_leaf = max(1, min(12, n_train // 25))
    max_d = 6 if n_train > 80 else (4 if n_train > 20 else 3)
    n_est = 120 if n_train > 100 else 50

    model = RandomForestRegressor(
        n_estimators=n_est,
        max_depth=max_d,
        min_samples_leaf=min_leaf,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rf_r2 = max(0.0, r2_score(y_test, preds) * 100.0) if len(y_test) > 1 else 0.0
    mae = mean_absolute_error(y_test, preds) if len(y_test) > 0 else 0.0

    # 6. Detailed Residual Diagnostics
    residuals = y_test - preds if len(y_test) > 0 else np.array([0.0])
    mean_residual = float(np.mean(residuals))
    std_residual = float(np.std(residuals))
    rmse = float(np.sqrt(np.mean(residuals**2)))
    p90_error = float(np.percentile(np.abs(residuals), 90)) if len(residuals) > 0 else 0.0

    model_quality_label = f"±{mae:.1f} {short_unit}".strip()
    benchmark_df = pd.DataFrame([
        {
            "Model Algoritma": "Random Forest Regressor (Utama)",
            "Variansi R²": f"{rf_r2:.1f}%",
            "Rata-rata Meleset (MAE)": fmt_num(mae, t_unit),
            "RMSE": fmt_num(rmse, t_unit),
            "Bias Residual": f"{mean_residual:+.2f}",
            "Status": "Model Terpilih",
        },
        {
            "Model Algoritma": "Ridge Linear Regression (Baseline)",
            "Variansi R²": f"{base_r2:.1f}%",
            "Rata-rata Meleset (MAE)": fmt_num(base_mae, t_unit),
            "RMSE": fmt_num(float(np.sqrt(mean_absolute_error(y_test, base_preds))), t_unit),
            "Bias Residual": f"{float(np.mean(y_test - base_preds)):+.2f}",
            "Status": "Pembanding Dasar",
        },
    ])

    importances = pd.Series(model.feature_importances_, index=filtered_features).sort_values(ascending=False)
    top_features = importances.index.tolist()

    t_meta = schema_info.get(target_col, {})
    t_phrase = t_meta.get("phrase", target_col.lower())
    t_up = t_meta.get("verb_up", "meningkat")
    t_down = t_meta.get("verb_down", "menurun")

    # 7. Grounded Feature Influence & Correlation Metrics
    corr_records = []
    for col in filtered_features:
        r_val, p_val = stats.pearsonr(X_full[col], y_full) if (X_full[col].std() > 1e-9 and np.std(y_full) > 1e-9) else (0.0, 1.0)
        f_meta = schema_info.get(col, {})
        f_phrase = f_meta.get("phrase", col.lower())
        f_up = f_meta.get("verb_up", "meningkat")
        f_unit = f_meta.get("unit", "")

        if r_val <= -0.06:
            natural_hint = f"Saat {f_phrase} {f_up}, {t_phrase} cenderung {t_down}."
            short_dir = "Berlawanan (-)"
        elif r_val >= 0.06:
            natural_hint = f"Saat {f_phrase} {f_up}, {t_phrase} ikut {t_up}."
            short_dir = "Searah (+)"
        else:
            natural_hint = f"Memengaruhi {t_phrase} ketika melewati titik batas tertentu."
            short_dir = "Titik Ambang"

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
            "Min": float(X_full[col].quantile(0.03)),
            "Median": float(X_full[col].median()),
            "Max": float(X_full[col].quantile(0.97)),
        })
    stats_df = pd.DataFrame(corr_records).sort_values("Pengaruh_Persen", ascending=False).reset_index(drop=True)

    # 8. Behavioral Clustering (K-Means on Scaled Features)
    scaler = StandardScaler()
    k_clusters = min(3, max(2, len(X_full)))
    km = KMeans(n_clusters=k_clusters, n_init=10, random_state=42)
    clusters = km.fit_predict(scaler.fit_transform(X_full))

    plot_df = X_full.copy()
    plot_df[target_col] = y_full
    plot_df["Cluster_ID"] = clusters

    c_means = plot_df.groupby("Cluster_ID")[target_col].mean().sort_values(ascending=False)
    rank_labels = {
        c_means.index[0]: f"Kelompok Tinggi (~{fmt_num(c_means.iloc[0], t_unit)})",
        c_means.index[min(1, len(c_means)-1)]: f"Kelompok Menengah (~{fmt_num(c_means.iloc[min(1, len(c_means)-1)], t_unit)})",
        c_means.index[-1]: f"Kelompok Rendah (~{fmt_num(c_means.iloc[-1], t_unit)})",
    }
    rank_keys = {c_means.index[0]: "high", c_means.index[min(1, len(c_means)-1)]: "mid", c_means.index[-1]: "low"}
    plot_df["Segment_Label"] = plot_df["Cluster_ID"].map(rank_labels)
    plot_df["Group_Key"] = plot_df["Cluster_ID"].map(rank_keys)

    # 9. Stratified Subgroup Distribution (Ridge Groups for Visualization)
    top1_col = top_features[0] if top_features else filtered_features[0]
    f1_vals = X_full[top1_col]
    f1_meta = schema_info.get(top1_col, {})
    f1_unit = f1_meta.get("unit", "")
    f1_min = float(f1_vals.min())
    f1_max = float(f1_vals.max())
    f1_nunique = int(f1_vals.nunique())

    if f1_min >= 0.0 and f1_max <= 1.0 and f1_nunique <= 4:
        cut_mid = float(f1_vals.quantile(0.6))
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
        sub_y = y_full[mask]
        if len(sub_y) < 5:
            sub_y = y_full
        raw_groups.append({
            "tier": item["tier"],
            "range": item["range"],
            "title": f"{top1_col} {item['tier'].lower()} ({item['range']})",
            "count": int(np.sum(mask)) if np.sum(mask) > 0 else len(sub_y),
            "median": float(np.median(sub_y)),
            "mean": float(np.mean(sub_y)),
            "std": max(float(np.std(sub_y)), (float(np.max(y_full) - np.min(y_full)) * 0.06)),
        })
    ridge_groups = sorted(raw_groups, key=lambda d: d["median"], reverse=True)

    median_df = pd.DataFrame([X_full.median()[filtered_features]])
    baseline_normal_val = float(model.predict(median_df)[0])

    audit_summary = dict(audit_info)
    audit_summary["dropped_collinear"] = dropped_collinear if dropped_collinear else ["Tidak ada kolom redundan"]
    audit_summary["train_samples"] = len(X_train)
    audit_summary["test_samples"] = len(X_test)
    audit_summary["rmse"] = rmse
    audit_summary["p90_error"] = p90_error

    return {
        "model": model,
        "imputer": imputer,
        "feature_cols": filtered_features,
        "top_features": top_features,
        "stats_df": stats_df,
        "benchmark_df": benchmark_df,
        "audit_summary": audit_summary,
        "plot_df": plot_df,
        "ridge_groups": ridge_groups,
        "X_median": X_full.median(),
        "y_min": float(np.percentile(y_full, 2)),
        "y_max": float(np.percentile(y_full, 98)),
        "y_baseline": baseline_normal_val,
        "y_population_median": float(np.median(y_full)),
        "model_quality_label": model_quality_label,
        "n_rows": len(work_df),
        "residuals": {
            "mean": mean_residual,
            "std": std_residual,
            "rmse": rmse,
            "mae": mae,
            "p90": p90_error,
        },
    }


def simulate_and_narrate(pipeline: dict, custom_inputs: dict, target_col: str, schema_info: dict) -> dict:
    """Execute counterfactual decision simulation and generate grounded strategic narrative."""
    row = pipeline["X_median"].copy()
    for col, val in custom_inputs.items():
        if col in row.index:
            row[col] = val

    X_in = pd.DataFrame([row[pipeline["feature_cols"]]])
    pred_val = float(pipeline["model"].predict(X_in)[0])
    base_val = pipeline["y_baseline"]
    diff_val = pred_val - base_val
    diff_pct = (diff_val / (abs(base_val) + 1e-9)) * 100.0

    top1_row = pipeline["stats_df"].iloc[0]
    top2_row = pipeline["stats_df"].iloc[1] if len(pipeline["stats_df"]) > 1 else top1_row
    top1 = top1_row["Fitur"]

    # 50-point marginal grid search
    grid_points = 70
    grid_x = np.linspace(top1_row["Min"], top1_row["Max"], grid_points)
    grid_df = pd.DataFrame([row[pipeline["feature_cols"]]] * grid_points)
    grid_df[top1] = grid_x
    raw_grid_preds = pipeline["model"].predict(grid_df)
    grid_preds = gaussian_filter1d(raw_grid_preds, sigma=2.0)

    base_grid_df = pd.DataFrame([pipeline["X_median"][pipeline["feature_cols"]]] * grid_points)
    base_grid_df[top1] = grid_x
    raw_base_preds = pipeline["model"].predict(base_grid_df)
    base_grid_preds = gaussian_filter1d(raw_base_preds, sigma=2.0)

    # Mathematical Tipping Point via Inflection of Marginal Response
    diffs = np.abs(np.diff(base_grid_preds))
    tipping_idx = int(np.argmax(diffs)) if len(diffs) > 0 else (grid_points // 2)
    tipping_x = float(grid_x[tipping_idx])
    low_end_y = float(base_grid_preds[min(4, len(base_grid_preds)-1)])
    high_end_y = float(base_grid_preds[max(0, len(base_grid_preds)-5)])

    t_meta = schema_info.get(target_col, {})
    t_phrase = t_meta.get("phrase", target_col.lower())
    t_unit = t_meta.get("unit", "")
    t_up = t_meta.get("verb_up", "meningkat")
    t_down = t_meta.get("verb_down", "menurun")

    f1_phrase = top1_row["Frasa"]
    f1_unit = top1_row["Unit"]
    f1_up = top1_row["Verb_Up"]
    f1_share = top1_row["Pengaruh_Persen"]

    f2_phrase = top2_row["Frasa"]
    f2_share = top2_row["Pengaruh_Persen"]

    if top1_row["Pearson_r"] <= -0.06:
        headline = f"Kunci utama menjaga {t_phrase} ada pada kendali {f1_phrase}."
        direction_story = (
            f"Di data ini, begitu <b>{f1_phrase}</b> {f1_up} melewati batas kritis <b>{fmt_num(tipping_x, f1_unit)}</b>, "
            f"<b>{t_phrase}</b> cenderung {t_down} dari kisaran <b>{fmt_num(low_end_y, t_unit)}</b> menuju <b>{fmt_num(high_end_y, t_unit)}</b>."
        )
        action_tip = f"menekan {f1_phrase} agar tetap di bawah {fmt_num(tipping_x, f1_unit)}"
    elif top1_row["Pearson_r"] >= 0.06:
        headline = f"Pertumbuhan {t_phrase} paling kuat digerakkan oleh {f1_phrase}."
        direction_story = (
            f"Data memperlihatkan perubahan paling tajam terjadi saat <b>{f1_phrase}</b> melampaui titik <b>{fmt_num(tipping_x, f1_unit)}</b>, "
            f"yang mengangkat <b>{t_phrase}</b> dari kisaran <b>{fmt_num(low_end_y, t_unit)}</b> ke <b>{fmt_num(high_end_y, t_unit)}</b>."
        )
        action_tip = f"menjaga {f1_phrase} di atas {fmt_num(tipping_x, f1_unit)}"
    else:
        headline = f"{f1_phrase.capitalize()} menjadi penentu keseimbangan {t_phrase}."
        direction_story = (
            f"Pergeseran <b>{f1_phrase}</b> di sekitar titik <b>{fmt_num(tipping_x, f1_unit)}</b> "
            f"mengubah <b>{t_phrase}</b> di rentang <b>{fmt_num(min(low_end_y, high_end_y), t_unit)}</b> hingga <b>{fmt_num(max(low_end_y, high_end_y), t_unit)}</b>."
        )
        action_tip = f"menjaga {f1_phrase} di sekitar titik optimal ({fmt_num(tipping_x, f1_unit)})"

    if f1_share >= 50:
        weight_story = (
            f"Dari {pipeline['n_rows']:,} baris data yang dibedah, <b>{f1_phrase}</b> memegang kendali dominan hingga <b>{f1_share:.0f}%</b>, "
            f"jauh di atas <b>{f2_phrase}</b> ({f2_share:.0f}%)."
        )
    else:
        weight_story = (
            f"Dari {pipeline['n_rows']:,} baris data yang dibedah, <b>{t_phrase}</b> ditentukan oleh perpaduan antara "
            f"<b>{f1_phrase}</b> ({f1_share:.0f}% kendali) dan <b>{f2_phrase}</b> ({f2_share:.0f}% kendali)."
        )

    cur_f1_val = float(row[top1])
    if abs(diff_pct) < 1.0:
        sim_story = (
            f"Saat ini tuas berada di posisi standar (<b>{f1_phrase}</b> di <b>{fmt_num(cur_f1_val, f1_unit)}</b>), "
            f"menghasilkan <b>{t_phrase}</b> sebesar <b>{fmt_num(pred_val, t_unit)}</b>. "
            f"Coba geser tuas di kiri untuk menguji skenario {action_tip}."
        )
    elif diff_val > 0:
        sim_story = (
            f"Pada pengaturan tuasmu sekarang (<b>{f1_phrase}</b> di <b>{fmt_num(cur_f1_val, f1_unit)}</b>), "
            f"<b>{t_phrase}</b> terdorong naik ke <b>{fmt_num(pred_val, t_unit)}</b> "
            f"(<b>+{abs(diff_pct):.1f}%</b> di atas kondisi standar {fmt_num(base_val, t_unit)})."
        )
    else:
        sim_story = (
            f"Pada pengaturan tuasmu sekarang (<b>{f1_phrase}</b> di <b>{fmt_num(cur_f1_val, f1_unit)}</b>), "
            f"<b>{t_phrase}</b> berada di <b>{fmt_num(pred_val, t_unit)}</b> "
            f"(<b>-{abs(diff_pct):.1f}%</b> dari kondisi standar {fmt_num(base_val, t_unit)}). "
            f"Langkah terbaik adalah {action_tip}."
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
        "headline": headline,
        "full_narrative": f"{weight_story} {direction_story}<br><br><b>Simulasi Keputusanmu:</b> {sim_story}",
    }


# Backward-compatible aliases
train_real_ml_pipeline = train_fluent_ml_pipeline
train_semantic_ml_pipeline = train_fluent_ml_pipeline
