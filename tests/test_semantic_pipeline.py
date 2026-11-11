"""Unit tests for CSIP Auto-Semantic ML & Decision Pipeline.

Validates:
- [UK-01 s/d UK-05] Data Profiling, Semantic Schema, and Ingestion
- [UK-06] Auto Data Cleaning (Infinities, Duplicates, Imputation)
- [UK-07] Feature Engineering & Interaction Building
- [UK-08, UK-09] Multi-Model Training (Baseline Ladder vs Random Forest) & K-Means Clustering
- [UK-10] Model Evaluation (Metrics, Pearson Correlations, Statistical Significance)
- [UK-11] What-If Scenario Prediction & Partial Dependence Curve Generation

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

from csip.cleaning.auto_cleaner import AutoDataCleaner, auto_clean_dataframe
from csip.data.semantic_profiler import (
    build_semantic_schema,
    get_builtin_dataset,
    interpret_column_meaning,
)
from csip.features.builder import AutoFeatureBuilder, build_interaction_features
from csip.models.ml_engine import train_semantic_ml_pipeline
from csip.scenarios.what_if import predict_what_if


def test_semantic_schema_profiling():
    """Verify automatic column semantic profiling and schema generation [UK-01 - UK-05]."""
    test_df = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
        "price": [120.50, 45.00, 230.10, 89.90],
        "freight_value": [15.20, 10.00, 25.00, 12.50],
        "delivery_days": [3.5, 7.0, 12.2, 5.0],
        "review_score": [5.0, 4.0, 2.0, 4.5],
        "category_name": ["elektronik", "buku", "elektronik", "fashion"],
    })

    schema = build_semantic_schema(test_df)
    assert schema["n_rows"] == 4
    assert schema["n_cols"] == 6
    assert "price" in schema["numeric_columns"]
    assert "category_name" in schema["categorical_columns"]

    # Verify column interpretation rules
    meaning_price = interpret_column_meaning("price")
    assert meaning_price["semantic_category"] == "price_value"
    assert "Moneter" in meaning_price["human_label"] or "Finansial" in meaning_price["human_label"]

    meaning_freight = interpret_column_meaning("freight_value")
    assert meaning_freight["semantic_category"] == "freight_cost"

    meaning_score = interpret_column_meaning("review_score")
    assert meaning_score["semantic_category"] == "target"


def test_auto_clean_dataframe():
    """Verify automated data cleaning handling infinities, duplicates, and imputation [UK-06]."""
    dirty_df = pd.DataFrame({
        "feature_a": [10.0, 20.0, np.inf, 40.0, 20.0],
        "feature_b": [1.0, np.nan, 3.0, 4.0, np.nan],
        "category": ["A", "B", None, "A", "B"],
    })

    clean_df, report = auto_clean_dataframe(dirty_df)
    assert not np.isinf(clean_df["feature_a"]).any()
    assert clean_df["feature_b"].isna().sum() == 0
    assert report["cleaned_rows"] > 0
    assert report["numeric_nulls_imputed"] >= 1
    assert report["is_clean"] is True


def test_feature_interactions():
    """Verify automated interaction feature construction [UK-07]."""
    df = pd.DataFrame({
        "Harga_Produk": [100.0, 200.0, 50.0],
        "Ongkos_Kirim": [10.0, 40.0, 25.0],
        "Lama_Pengiriman_Hari": [3.0, 5.0, 8.0],
    })

    feat_df, new_cols = build_interaction_features(df)
    assert len(new_cols) > 0
    assert any("Rasio" in c for c in new_cols)
    assert "Rasio_Harga_Prod_Per_Ongkos_Kir" in feat_df.columns


def test_train_semantic_ml_pipeline_regression():
    """Verify regression training, metrics, Pearson significance, and clustering [UK-08 - UK-11]."""
    raw = load_diabetes(as_frame=True)
    df = raw.frame.copy()
    target_col = "target"
    feature_cols = [c for c in df.columns if c != target_col][:5]

    pipeline = train_semantic_ml_pipeline(
        df=df,
        target_col=target_col,
        feature_cols=feature_cols,
        df_hash=123,
    )

    assert not pipeline["is_classification"]
    assert "RandomForestRegressor" in str(type(pipeline["model"]))
    assert "Ridge" in str(type(pipeline["baseline_model"]))
    assert pipeline["primary_metric_name"] == "Variansi Terjelaskan (R²)"
    assert len(pipeline["top_features"]) == len(feature_cols)

    # Check Pearson statistics table
    stats_df = pipeline["stats_df"]
    assert len(stats_df) == len(feature_cols)
    assert "Pearson_r" in stats_df.columns
    assert "p_value" in stats_df.columns
    assert "Importance" in stats_df.columns

    # Check K-Means clustering output
    plot_df = pipeline["plot_df"]
    assert "Cluster_ID" in plot_df.columns
    assert "Segment_Label" in plot_df.columns
    assert "Group_Key" in plot_df.columns
    assert set(plot_df["Group_Key"].unique()).issubset({"high", "mid", "low"})


def test_train_semantic_ml_pipeline_classification():
    """Verify classification training, accuracy, and F1-macro evaluation [UK-08 - UK-10]."""
    raw = load_wine(as_frame=True)
    df = raw.frame.copy()
    target_col = "target"
    feature_cols = [c for c in df.columns if c != target_col][:4]

    pipeline = train_semantic_ml_pipeline(
        df=df,
        target_col=target_col,
        feature_cols=feature_cols,
        df_hash=456,
    )

    assert pipeline["is_classification"]
    assert "RandomForestClassifier" in str(type(pipeline["model"]))
    assert "LogisticRegression" in str(type(pipeline["baseline_model"]))
    assert pipeline["primary_metric_name"] == "Akurasi Model (Test Set)"
    assert pipeline["primary_metric_val"] >= 50.0


def test_predict_what_if_and_pdp():
    """Verify what-if simulation inference and partial dependence curves [UK-08, UK-11]."""
    raw = load_diabetes(as_frame=True)
    df = raw.frame.copy()
    target_col = "target"
    feature_cols = ["bmi", "bp", "s1", "s2"]

    pipeline = train_semantic_ml_pipeline(
        df=df,
        target_col=target_col,
        feature_cols=feature_cols,
    )

    top_feature = pipeline["top_features"][0]
    custom_val = float(pipeline["stats_df"].iloc[0]["Max"])
    sim = predict_what_if(pipeline, {top_feature: custom_val})

    assert "pred_val" in sim
    assert "base_val" in sim
    assert "diff_val" in sim
    assert "diff_pct" in sim
    assert len(sim["grid_x"]) == 60
    assert len(sim["grid_preds"]) == 60
    assert len(sim["base_grid_preds"]) == 60
    assert isinstance(sim["pred_val"], float)
