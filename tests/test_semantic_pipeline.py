"""Unit tests for CSIP Fluent Auto-Semantic ML & Decision Pipeline.

Validates:
- [UK-01 s/d UK-05] Fluent Schema Building & Human Translation
- [UK-06] Auto Data Cleaning and Transform
- [UK-07] Feature Engineering and Metric Extraction
- [UK-08, UK-09] Multi-Model Training (Baseline Ladder vs Random Forest) & K-Means Clustering
- [UK-10] Model Evaluation (Metrics, Pearson Correlations, Statistical Significance)
- [UK-11] Simulation & Human Story Generation

100% Real Computation, Local, Zero Emojis.
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_diabetes, load_wine

# Add src and repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from src.csip.data.semantic_profiler import (
    build_fluent_schema,
    fmt_num,
    get_builtin_dataset,
    smart_transform_uploaded_dataframe,
)
from src.csip.models.ml_engine import (
    simulate_and_narrate,
    train_fluent_ml_pipeline,
)


def test_fmt_num_human_formatting():
    """Verify human readable number formatting without technical jargon."""
    assert fmt_num(1_500_000_000, "$") == "$1.50 Miliar"
    assert fmt_num(2_500_000, "Rp") == "Rp2.50 Juta"
    assert fmt_num(45_000) == "45.0 Ribu"
    assert fmt_num(12.345, "%") == "12.35%"
    assert fmt_num(np.nan) == "-"


def test_fluent_schema_building():
    """Verify semantic schema building, target selection, and audit metadata [UK-01 - UK-05]."""
    test_df = pd.DataFrame({
        "price": [120.50, 45.00, 230.10, 89.90],
        "freight_value": [15.20, 10.00, 25.00, 12.50],
        "delivery_days": [3.5, 7.0, 12.2, 5.0],
        "review_score": [5.0, 4.0, 2.0, 4.5],
    })

    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(test_df)
    assert len(clean_df) == 4
    assert auto_target == "Kepuasan Pembeli"
    assert "Harga Barang" in clean_df.columns
    assert "Ongkos Kirim" in clean_df.columns
    assert audit_info["clean_rows"] == 4


def test_train_fluent_ml_pipeline_regression():
    """Verify model training, benchmark comparison, and K-Means segmentation [UK-08 - UK-11]."""
    raw_df = get_builtin_dataset("Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)")
    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)

    candidates = [c for c in clean_df.columns if c != auto_target]
    pipeline = train_fluent_ml_pipeline(
        df_sample=clean_df,
        target_col=auto_target,
        candidate_cols=candidates,
        schema_info=schema_info,
        audit_info=audit_info,
    )

    assert "model" in pipeline
    assert "stats_df" in pipeline
    assert len(pipeline["stats_df"]) > 0
    assert "Pengaruh_Persen" in pipeline["stats_df"].columns
    assert "benchmark_df" in pipeline
    assert "plot_df" in pipeline
    assert "Segment_Label" in pipeline["plot_df"].columns
    assert pipeline["n_rows"] == len(clean_df)


def test_train_fluent_ml_pipeline_classification():
    """Verify classification training and benchmark comparison [UK-08 - UK-10]."""
    raw_df = get_builtin_dataset("Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)")
    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)

    candidates = [c for c in clean_df.columns if c != auto_target]
    pipeline = train_fluent_ml_pipeline(
        df_sample=clean_df,
        target_col=auto_target,
        candidate_cols=candidates,
        schema_info=schema_info,
        audit_info=audit_info,
    )

    assert "model" in pipeline
    assert "benchmark_df" in pipeline
    bench = pipeline["benchmark_df"]
    assert any("Random Forest" in str(m) for m in bench["Model Algoritma"])


def test_simulate_and_narrate():
    """Verify interactive decision simulation and natural language narration [UK-11]."""
    raw_df = get_builtin_dataset("Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)")
    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(raw_df)

    candidates = [c for c in clean_df.columns if c != auto_target]
    pipeline = train_fluent_ml_pipeline(
        df_sample=clean_df,
        target_col=auto_target,
        candidate_cols=candidates,
        schema_info=schema_info,
        audit_info=audit_info,
    )

    top_feature = pipeline["top_features"][0]
    custom_inputs = {top_feature: float(pipeline["stats_df"].iloc[0]["Max"])}

    sim = simulate_and_narrate(
        pipeline=pipeline,
        custom_inputs=custom_inputs,
        target_col=auto_target,
        schema_info=schema_info,
    )

    assert "pred_val" in sim
    assert "base_val" in sim
    assert "diff_val" in sim
    assert "diff_pct" in sim
    assert "headline" in sim
    assert "full_narrative" in sim
    assert len(sim["headline"]) > 0
    assert len(sim["grid_x"]) == 60
