"""CSIP Universal Machine Learning & Decision Intelligence Engine.

Implements BNSP SKKNI Competencies:
- [UK-08] Membangun Skenario Model: Menetapkan data training/testing dan split validasi.
- [UK-09] Membangun Model: Melatih model Baseline (Ridge/Logistic) dan Ensemble (Random Forest).
- [UK-10] Mengevaluasi Hasil Pemodelan: Mengukur akurasi, F1, R-squared, MAE, dan signifikansi Pearson.
- [UK-11] Mengembangkan Solusi: Segmentasi klaster K-Means dan penyiapan inferensi interaktif.

100% Real Computation, Local, Zero Emojis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union
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


def train_semantic_ml_pipeline(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: List[str],
    df_hash: Optional[int] = None,
) -> Dict[str, Any]:
    """[UK-08, UK-09, UK-10, UK-11] Train multi-model comparison pipeline and K-Means segmentation."""
    work_df = df[feature_cols + [target_col]].copy()
    work_df = work_df.replace([np.inf, -np.inf], np.nan).dropna(subset=[target_col])

    if len(work_df) > 4000:
        work_df = work_df.sample(n=4000, random_state=42).reset_index(drop=True)

    imputer = SimpleImputer(strategy="median")
    X_raw = pd.DataFrame(imputer.fit_transform(work_df[feature_cols]), columns=feature_cols)
    y = work_df[target_col].values

    # Auto-detect Classification vs Regression
    unique_y = np.unique(y)
    is_classification = bool((len(unique_y) <= 10) and np.all(np.mod(unique_y, 1) == 0))

    X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.25, random_state=42)

    # Train Baseline & Ensemble Models
    if is_classification:
        baseline_model = LogisticRegression(max_iter=500, random_state=42)
        baseline_model.fit(X_train, y_train)
        b_preds = baseline_model.predict(X_test)
        base_acc = float(accuracy_score(y_test, b_preds) * 100.0)

        model = RandomForestClassifier(n_estimators=80, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        primary_metric_val = float(accuracy_score(y_test, preds) * 100.0)
        primary_metric_name = "Akurasi Model (Test Set)"
        f1_m = float(f1_score(y_test, preds, average="macro"))
        secondary_metric_str = f"F1-Macro: {f1_m:.3f} (Baseline: {base_acc:.1f}%)"
    else:
        baseline_model = Ridge(alpha=1.0, random_state=42)
        baseline_model.fit(X_train, y_train)
        b_preds = baseline_model.predict(X_test)
        base_r2 = float(max(0.0, r2_score(y_test, b_preds) * 100.0))

        model = RandomForestRegressor(n_estimators=80, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        r2 = float(r2_score(y_test, preds))
        mae = float(mean_absolute_error(y_test, preds))
        primary_metric_val = float(max(0.0, r2 * 100.0))
        primary_metric_name = "Variansi Terjelaskan (R²)"
        secondary_metric_str = f"MAE: {mae:.3f} (Baseline R²: {base_r2:.1f}%)"

    # Feature Importances directly from model
    importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    top_features = importances.index.tolist()

    # Real Pearson Correlation & p-values
    corr_records = []
    for col in feature_cols:
        if X_raw[col].std() > 1e-9 and np.std(y) > 1e-9:
            r_val, p_val = stats.pearsonr(X_raw[col], y)
        else:
            r_val, p_val = 0.0, 1.0
        corr_records.append({
            "Fitur": col,
            "Importance": float(importances[col]),
            "Pearson_r": float(r_val),
            "p_value": float(p_val),
            "Min": float(X_raw[col].quantile(0.02)),
            "Median": float(X_raw[col].median()),
            "Mean": float(X_raw[col].mean()),
            "Max": float(X_raw[col].quantile(0.98)),
            "Std": float(X_raw[col].std()),
        })
    stats_df = pd.DataFrame(corr_records).sort_values("Importance", ascending=False).reset_index(drop=True)

    # Real K-Means Clustering for Behavioral Segmentation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    n_cl = 3 if len(X_raw) >= 3 else 1
    km = KMeans(n_clusters=n_cl, n_init=10, random_state=42)
    clusters = km.fit_predict(X_scaled)

    plot_df = X_raw.copy()
    plot_df[target_col] = y
    plot_df["Cluster_ID"] = clusters

    cluster_means = plot_df.groupby("Cluster_ID")[target_col].mean().sort_values(ascending=False)
    rank_labels = {
        cluster_means.index[0]: f"Klaster Tinggi (Rata-rata {target_col}: {cluster_means.iloc[0]:.2f})",
        cluster_means.index[min(1, len(cluster_means)-1)]: f"Klaster Menengah (Rata-rata {target_col}: {cluster_means.iloc[min(1, len(cluster_means)-1)]:.2f})",
        cluster_means.index[-1]: f"Klaster Rendah (Rata-rata {target_col}: {cluster_means.iloc[-1]:.2f})",
    }
    rank_keys = {
        cluster_means.index[0]: "high",
        cluster_means.index[min(1, len(cluster_means)-1)]: "mid",
        cluster_means.index[-1]: "low",
    }
    plot_df["Segment_Label"] = plot_df["Cluster_ID"].map(rank_labels)
    plot_df["Group_Key"] = plot_df["Cluster_ID"].map(rank_keys)

    return {
        "model": model,
        "baseline_model": baseline_model,
        "is_classification": is_classification,
        "feature_cols": feature_cols,
        "top_features": top_features,
        "stats_df": stats_df,
        "plot_df": plot_df,
        "X_median": X_raw.median(),
        "y_mean": float(np.mean(y)),
        "y_std": float(np.std(y)),
        "primary_metric_val": primary_metric_val,
        "primary_metric_name": primary_metric_name,
        "secondary_metric_str": secondary_metric_str,
        "n_rows": len(work_df),
        "inertia": float(km.inertia_),
    }


# Backwards compatibility alias
train_real_ml_pipeline = train_semantic_ml_pipeline
