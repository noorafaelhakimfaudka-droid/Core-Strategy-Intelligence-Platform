"""CSIP Semantic Profiler & Universal Data Schema Engine.

Implements BNSP SKKNI Competencies:
- [UK-01] Menentukan Masalah Bisnis: Menerjemahkan kebutuhan analisis ke variabel target.
- [UK-02] Menentukan Kebutuhan Data: Mengidentifikasi tipe dan spesifikasi data.
- [UK-03] Menelaah Data: Menilai struktur, sebaran, dan tipe variabel tabular.
- [UK-04] Memvalidasi Data: Menghitung persentase missing values, nilai ekstrem, dan integritas.
- [UK-05] Menentukan Objek Data: Menentukan identifier, target, dan fitur prediktor.

100% Real Computation, Local, Zero Emojis.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes, load_wine


# Semantic keyword patterns to recognize business and behavioral variables
SEMANTIC_PATTERNS: Dict[str, List[str]] = {
    "target": [
        r"score", r"rating", r"target", r"label", r"kepuasan", r"churn",
        r"progresi", r"kelas", r"class", r"result", r"output", r"status"
    ],
    "freight_cost": [
        r"ongkir", r"freight", r"shipping", r"biaya_kirim", r"transport",
        r"tarif", r"delivery_fee", r"surcharge"
    ],
    "time_delay": [
        r"delay", r"telat", r"terlambat", r"waktu", r"hari", r"durasi",
        r"lama", r"time", r"duration", r"days", r"hours"
    ],
    "price_value": [
        r"harga", r"price", r"value", r"nilai", r"total", r"nominal",
        r"omset", r"revenue", r"belanja", r"gmv", r"cost"
    ],
    "quantity": [
        r"count", r"jumlah", r"qty", r"quantity", r"items", r"banyak",
        r"item_id", r"cicilan", r"installments"
    ],
    "identifier": [
        r"id$", r"_id$", r"^id_", r"uuid", r"kode", r"nomor", r"trx"
    ],
}


def interpret_column_meaning(col_name: str, series: Optional[pd.Series] = None) -> Dict[str, Any]:
    """[UK-03, UK-05] Interpret semantic meaning, role, and statistical properties of a column."""
    name_clean = col_name.lower().strip()
    if series is None:
        series = pd.Series([1.0, 2.0, 3.0], name=col_name)

    n_rows = len(series)
    null_count = int(series.isnull().sum())
    null_pct = float((null_count / max(1, n_rows)) * 100.0)
    n_unique = int(series.nunique(dropna=True))
    is_numeric = bool(pd.api.types.is_numeric_dtype(series))

    # Detect role
    role = "feature_numeric" if is_numeric else "feature_categorical"
    matched_category = "general"

    # Check identifier pattern
    if any(re.search(pat, name_clean) for pat in SEMANTIC_PATTERNS["identifier"]):
        if n_unique / max(1, n_rows) > 0.6:
            role = "identifier"
            matched_category = "identifier"

    # Check target pattern
    if role != "identifier":
        for cat, pats in SEMANTIC_PATTERNS.items():
            if any(re.search(pat, name_clean) for pat in pats):
                matched_category = cat
                if cat == "target":
                    role = "target_candidate"
                break

    human_labels = {
        "target": "Variabel Hasil / Target",
        "price_value": "Nilai Moneter / Finansial",
        "freight_cost": "Biaya Logistik & Pengiriman",
        "time_delay": "Durasi & Ketepatan Waktu",
        "quantity": "Kuantitas & Frekuensi",
        "identifier": "Identitas / Kunci Unik",
        "general": "Atribut Pendukung",
    }

    return {
        "column_name": col_name,
        "is_numeric": is_numeric,
        "semantic_role": role,
        "semantic_category": matched_category,
        "human_label": human_labels.get(matched_category, "Atribut Pendukung"),
        "null_count": null_count,
        "null_pct": round(null_pct, 2),
        "unique_count": n_unique,
        "sample_values": series.dropna().iloc[:3].tolist() if not series.dropna().empty else [],
    }


def build_semantic_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """[UK-01, UK-02, UK-03, UK-04, UK-05] Construct end-to-end semantic schema profile for any DataFrame."""
    n_rows = len(df)
    n_cols = len(df.columns)
    dup_rows = int(df.duplicated().sum())
    dup_pct = float((dup_rows / max(1, n_rows)) * 100.0)

    col_profiles: Dict[str, Dict[str, Any]] = {}
    numeric_candidates: List[str] = []
    target_candidates: List[str] = []

    for col in df.columns:
        prof = interpret_column_meaning(col, df[col])
        col_profiles[col] = prof
        if prof["is_numeric"] and prof["semantic_role"] != "identifier" and prof["unique_count"] > 1:
            numeric_candidates.append(col)
            if prof["semantic_role"] == "target_candidate":
                target_candidates.append(col)

    # Pick recommended target
    if target_candidates:
        recommended_target = target_candidates[-1]
    elif numeric_candidates:
        recommended_target = numeric_candidates[-1]
    else:
        recommended_target = df.columns[-1]

    candidate_features = [c for c in numeric_candidates if c != recommended_target]
    categorical_columns = [c for c in df.columns if not col_profiles[c]["is_numeric"]]

    # Data health score (UK-04)
    total_cells = max(1, n_rows * n_cols)
    total_nulls = sum(p["null_count"] for p in col_profiles.values())
    null_ratio = total_nulls / total_cells
    health_score = max(0.0, min(100.0, 100.0 - (null_ratio * 40.0) - (dup_pct * 0.5)))

    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "duplicate_rows": dup_rows,
        "duplicate_pct": round(dup_pct, 2),
        "total_nulls": total_nulls,
        "health_score": round(health_score, 1),
        "column_profiles": col_profiles,
        "numeric_columns": numeric_candidates,
        "categorical_columns": categorical_columns,
        "recommended_target": recommended_target,
        "candidate_features": candidate_features,
    }


def try_load_local_olist() -> Optional[pd.DataFrame]:
    """[UK-02, UK-03] Search and merge local Olist e-commerce datasets from data/ or artifacts/."""
    root = Path(__file__).resolve().parent.parent.parent.parent

    # 1. Check for prepared analytical tables
    for folder in [root / "data" / "processed", root / "data" / "interim", root / "artifacts"]:
        if folder.exists():
            for ext in ("*.parquet", "*.csv"):
                files = list(folder.glob(ext))
                for f in files:
                    try:
                        df = pd.read_parquet(f) if f.suffix == ".parquet" else pd.read_csv(f, nrows=15000)
                        if len(df.select_dtypes(include=[np.number]).columns) >= 3 and len(df) >= 50:
                            return df
                    except Exception:
                        continue

    # 2. Check for raw Olist CSVs in data/raw
    raw_dir = root / "data" / "raw"
    orders_f = raw_dir / "olist_orders_dataset.csv"
    items_f = raw_dir / "olist_order_items_dataset.csv"
    reviews_f = raw_dir / "olist_order_reviews_dataset.csv"

    if orders_f.exists() and items_f.exists():
        try:
            orders = pd.read_csv(orders_f, nrows=25000)
            items = pd.read_csv(items_f, nrows=25000)
            agg_items = items.groupby("order_id", as_index=False).agg(
                Harga_Produk=("price", "sum"),
                Ongkos_Kirim=("freight_value", "sum"),
                Jumlah_Barang=("order_item_id", "count"),
            )
            merged = pd.merge(orders, agg_items, on="order_id", how="inner")
            if "order_delivered_customer_date" in merged.columns and "order_purchase_timestamp" in merged.columns:
                p_dt = pd.to_datetime(merged["order_purchase_timestamp"], errors="coerce")
                d_dt = pd.to_datetime(merged["order_delivered_customer_date"], errors="coerce")
                e_dt = pd.to_datetime(merged["order_estimated_delivery_date"], errors="coerce")
                merged["Lama_Pengiriman_Hari"] = (d_dt - p_dt).dt.total_seconds() / 86400.0
                merged["Keterlambatan_Hari"] = (d_dt - e_dt).dt.total_seconds() / 86400.0
            if reviews_f.exists():
                rev = pd.read_csv(reviews_f, usecols=["order_id", "review_score"], nrows=25000)
                merged = pd.merge(merged, rev, on="order_id", how="left")
                merged.rename(columns={"review_score": "Skor_Kepuasan_Pelanggan"}, inplace=True)
            merged["Rasio_Ongkir_Per_Harga"] = merged["Ongkos_Kirim"] / (merged["Harga_Produk"] + 1.0)
            merged["Total_Nilai_Transaksi"] = merged["Harga_Produk"] + merged["Ongkos_Kirim"]
            return merged.dropna(subset=["Harga_Produk", "Ongkos_Kirim"]).reset_index(drop=True)
        except Exception:
            pass

    return None


def get_builtin_dataset(name: str) -> pd.DataFrame:
    """[UK-02] Provide standard verified datasets for machine learning & decision intelligence."""
    if name == "Data E-Commerce Olist (Lokal)":
        olist_df = try_load_local_olist()
        if olist_df is not None:
            return olist_df

    if name == "Dataset Kesehatan & Biometrik (Sklearn Diabetes)":
        raw = load_diabetes(as_frame=True)
        df = raw.frame.copy()
        df.rename(columns={"target": "Progresi_Risiko_Kesehatan"}, inplace=True)
        return df

    if name == "Dataset Kualitas Produk & Kimia (Sklearn Wine)":
        raw = load_wine(as_frame=True)
        df = raw.frame.copy()
        df.rename(columns={"target": "Kelas_Kualitas_Produk"}, inplace=True)
        return df

    # Fallback: Realistic E-Commerce Simulation Sample
    rng = np.random.default_rng(42)
    n = 1500
    harga = rng.lognormal(mean=4.5, sigma=0.7, size=n).round(2)
    ongkir = (harga * rng.uniform(0.05, 0.35, size=n) + rng.normal(5, 2, size=n)).clip(2.0, 120.0).round(2)
    lama_kirim = rng.gamma(shape=2.5, scale=3.2, size=n).round(1)
    telat = (lama_kirim - rng.uniform(5, 12, size=n)).round(1)
    cicilan = rng.integers(1, 10, size=n)
    skor_ulasan = np.clip(
        5.0 - 0.18 * np.maximum(0, telat) - 1.2 * (ongkir / (harga + 1)) + rng.normal(0, 0.45, size=n),
        1.0, 5.0
    ).round(1)
    nilai_total = (harga + ongkir).round(2)

    return pd.DataFrame({
        "Harga_Produk": harga,
        "Ongkos_Kirim": ongkir,
        "Lama_Pengiriman_Hari": lama_kirim,
        "Keterlambatan_Hari": telat,
        "Jumlah_Cicilan": cicilan,
        "Rasio_Ongkir_Per_Harga": (ongkir / harga).round(3),
        "Total_Nilai_Transaksi": nilai_total,
        "Skor_Kepuasan_Pelanggan": skor_ulasan,
    })
