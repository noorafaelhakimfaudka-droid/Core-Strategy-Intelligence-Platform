import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.csip.data.semantic_profiler import fmt_num


def train_fluent_ml_pipeline(
    df_sample: pd.DataFrame,
    target_col: str,
    candidate_cols: list[str],
    schema_info: dict,
    audit_info: dict,
) -> dict:
    """
    [UK-06, UK-08, UK-09, UK-10, UK-11]
    Membersihkan data, menyaring multikolinearitas, melatih Baseline vs Random Forest,
    mengelompokkan K-Means, dan menghitung statistik setiap variabel.
    """
    work_df = df_sample[candidate_cols + [target_col]].copy()
    work_df = work_df.replace([np.inf, -np.inf], np.nan).dropna(subset=[target_col])

    if len(work_df) > 3500:
        work_df = work_df.sample(n=3500, random_state=42).reset_index(drop=True)

    imputer = SimpleImputer(strategy="median")
    X_full = pd.DataFrame(imputer.fit_transform(work_df[candidate_cols]), columns=candidate_cols)
    y = work_df[target_col].values

    # Filter Anti-Redundan (Mencegah dua kolom kembar >94% masuk bersamaan)
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
    unique_y = np.unique(y)
    is_classification = (len(unique_y) <= 8) and np.all(np.mod(unique_y, 1) == 0)

    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.25, random_state=42)
    t_unit = schema_info.get(target_col, {}).get("unit", "")

    # UK-08 & UK-10: Adu Skenario Model (Baseline Linear/Logistic vs Random Forest)
    if is_classification:
        base_model = LogisticRegression(max_iter=500, random_state=42)
        base_model.fit(X_train, y_train)
        base_preds = base_model.predict(X_test)
        base_acc = accuracy_score(y_test, base_preds) * 100.0
        base_f1 = f1_score(y_test, base_preds, average="macro")

        model = RandomForestClassifier(n_estimators=90, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds) * 100.0
        rf_f1 = f1_score(y_test, preds, average="macro")

        model_quality_label = f"Ketepatan Uji {acc:.1f}%"
        benchmark_df = pd.DataFrame([
            {"Model Algoritma": "Random Forest Classifier (Utama)", "Akurasi / R²": f"{acc:.1f}%", "Metrik Error / F1": f"F1: {rf_f1:.3f}", "Status": "Model Terpilih"},
            {"Model Algoritma": "Logistic Regression (Baseline)", "Akurasi / R²": f"{base_acc:.1f}%", "Metrik Error / F1": f"F1: {base_f1:.3f}", "Status": "Pembanding Dasar"},
        ])
    else:
        base_model = Ridge(alpha=1.0, random_state=42)
        base_model.fit(X_train, y_train)
        base_preds = base_model.predict(X_test)
        base_r2 = max(0.0, r2_score(y_test, base_preds) * 100.0)
        base_mae = mean_absolute_error(y_test, base_preds)

        model = RandomForestRegressor(n_estimators=90, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rf_r2 = max(0.0, r2_score(y_test, preds) * 100.0)
        mae = mean_absolute_error(y_test, preds)

        model_quality_label = f"Toleransi Meleset ±{fmt_num(mae, t_unit)}"
        benchmark_df = pd.DataFrame([
            {"Model Algoritma": "Random Forest Regressor (Utama)", "Variansi R²": f"{rf_r2:.1f}%", "Rata-rata Meleset (MAE)": fmt_num(mae, t_unit), "Status": "Model Terpilih"},
            {"Model Algoritma": "Ridge Linear Regression (Baseline)", "Variansi R²": f"{base_r2:.1f}%", "Rata-rata Meleset (MAE)": fmt_num(base_mae, t_unit), "Status": "Pembanding Dasar"},
        ])

    importances = pd.Series(model.feature_importances_, index=filtered_features).sort_values(ascending=False)
    top_features = importances.index.tolist()

    t_meta = schema_info.get(target_col, {})
    t_phrase = t_meta.get("phrase", target_col.lower())
    t_up = t_meta.get("verb_up", "meningkat")
    t_down = t_meta.get("verb_down", "menurun")

    corr_records = []
    for col in filtered_features:
        r_val, p_val = stats.pearsonr(X_raw[col], y) if (X_raw[col].std() > 1e-9 and np.std(y) > 1e-9) else (0.0, 1.0)
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
            "Min": float(X_raw[col].quantile(0.02)),
            "Median": float(X_raw[col].median()),
            "Max": float(X_raw[col].quantile(0.98)),
        })
    stats_df = pd.DataFrame(corr_records).sort_values("Pengaruh_Persen", ascending=False).reset_index(drop=True)

    # K-Means Clustering
    scaler = StandardScaler()
    km = KMeans(n_clusters=3, n_init=10, random_state=42)
    clusters = km.fit_predict(scaler.fit_transform(X_raw))

    plot_df = X_raw.copy()
    plot_df[target_col] = y
    plot_df["Cluster_ID"] = clusters

    # Gunakan Median klaster untuk penamaan yang tahan terhadap outlier ekstrem
    c_medians = plot_df.groupby("Cluster_ID")[target_col].median().sort_values(ascending=False)
    rank_labels = {
        c_medians.index[0]: f"Kelompok Tinggi (~{fmt_num(c_medians.iloc[0], t_unit)})",
        c_medians.index[1]: f"Kelompok Menengah (~{fmt_num(c_medians.iloc[1], t_unit)})",
        c_medians.index[2]: f"Kelompok Rendah (~{fmt_num(c_medians.iloc[2], t_unit)})",
    }
    rank_keys = {c_medians.index[0]: "high", c_medians.index[1]: "mid", c_medians.index[2]: "low"}
    plot_df["Segment_Label"] = plot_df["Cluster_ID"].map(rank_labels)
    plot_df["Group_Key"] = plot_df["Cluster_ID"].map(rank_keys)

    # KUNCI PERBAIKAN: Gunakan prediksi pada titik Tengah (Median) sebagai baseline normal
    # supaya data miring (seperti Volume Kripto) tidak menghasilkan selisih palsu -72.7%!
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
        "plot_df": plot_df,
        "X_median": X_raw.median(),
        "y_baseline": baseline_normal_val,
        "y_population_median": float(np.median(y)),
        "model_quality_label": model_quality_label,
        "n_rows": len(work_df),
    }


def simulate_and_narrate(pipeline: dict, custom_inputs: dict, target_col: str, schema_info: dict) -> dict:
    """Menjalankan simulasi interaktif dan merakit narasi bahasa Indonesia yang luwes."""
    row = pipeline["X_median"].copy()
    for col, val in custom_inputs.items():
        if col in row.index:
            row[col] = val

    X_in = pd.DataFrame([row[pipeline["feature_cols"]]])
    pred_val = float(pipeline["model"].predict(X_in)[0])

    # Bandingkan dengan kondisi normal (saat semua tuas di nilai tengah/median)
    base_val = pipeline["y_baseline"]
    diff_val = pred_val - base_val
    diff_pct = (diff_val / (abs(base_val) + 1e-9)) * 100.0

    top1_row = pipeline["stats_df"].iloc[0]
    top2_row = pipeline["stats_df"].iloc[1] if len(pipeline["stats_df"]) > 1 else top1_row
    top1 = top1_row["Fitur"]

    grid_x = np.linspace(top1_row["Min"], top1_row["Max"], 60)
    grid_df = pd.DataFrame([row[pipeline["feature_cols"]]] * 60)
    grid_df[top1] = grid_x
    grid_preds = pipeline["model"].predict(grid_df)

    base_grid_df = pd.DataFrame([pipeline["X_median"][pipeline["feature_cols"]]] * 60)
    base_grid_df[top1] = grid_x
    base_grid_preds = pipeline["model"].predict(base_grid_df)

    diffs = np.abs(np.diff(base_grid_preds))
    tipping_idx = int(np.argmax(diffs)) if len(diffs) > 0 else 30
    tipping_x = float(grid_x[tipping_idx])
    low_end_y = float(base_grid_preds[5])
    high_end_y = float(base_grid_preds[-6])

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
            f"(<b>+{ abs(diff_pct):.1f}%</b> di atas kondisi standar {fmt_num(base_val, t_unit)})."
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


# Compatibility aliases for legacy interfaces
train_fluent_pipeline = train_fluent_ml_pipeline
train_semantic_ml_pipeline = train_fluent_ml_pipeline
train_real_ml_pipeline = train_fluent_ml_pipeline

