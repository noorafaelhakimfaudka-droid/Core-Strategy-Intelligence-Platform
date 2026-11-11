"""Stress tests for CSIP Data Engineering & Auto Data Cleaning Pipelines.

Validates robust handling of pathological edge cases:
1. Small datasets (N < 10)
2. Constant / Zero-variance features
3. High-cardinality categorical features
4. Extreme missing values (100% NaN columns, scattered NaNs)
5. Infinite values (+inf, -inf)
6. Duplicate rows and duplicate columns
7. Unseen categories during out-of-sample transform
8. Scikit-Learn transformer contracts (fit, transform, fit_transform)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from csip.cleaning.auto_cleaner import AutoDataCleaner, auto_clean_dataframe
from csip.data.semantic_profiler import build_fluent_schema
from csip.models.ml_engine import train_fluent_ml_pipeline


def test_autocleaner_fit_transform_contract():
    """Verify AutoDataCleaner strictly adheres to Scikit-Learn transformer protocol."""
    train_df = pd.DataFrame({
        "num1": [1.0, 2.0, np.nan, 4.0, 5.0],
        "cat1": ["A", "B", "A", None, "B"],
        "const1": [10.0, 10.0, 10.0, 10.0, 10.0],
    })
    test_df = pd.DataFrame({
        "num1": [np.nan, 6.0],
        "cat1": [None, "C"],  # "C" is an unseen category
        "const1": [10.0, 10.0],
    })

    cleaner = AutoDataCleaner()
    cleaner.fit(train_df)

    assert cleaner.imputed_medians_["num1"] == 3.0
    assert cleaner.imputed_modes_["cat1"] in ("A", "B")
    assert "const1" in cleaner.constant_cols_

    # Transform test set without fitting on test set (strict feature isolation)
    transformed_test = cleaner.transform(test_df)
    assert transformed_test["num1"].iloc[0] == 3.0  # Uses train median
    assert not transformed_test["num1"].isnull().any()
    assert not transformed_test["cat1"].isnull().any()


def test_autocleaner_infinite_and_duplicates():
    """Verify AutoDataCleaner handles infinite values and removes duplicate rows."""
    df_with_inf = pd.DataFrame({
        "val": [1.0, np.inf, -np.inf, 4.0, 1.0],
        "label": ["X", "Y", "Z", "W", "X"],
    })

    cleaned_df, report = auto_clean_dataframe(df_with_inf, drop_duplicates=True)

    # Infinite values replaced with median and duplicates removed
    assert not np.isinf(cleaned_df["val"]).any()
    assert report["inf_values_handled"] == 2
    assert report["duplicates_removed"] == 1
    assert len(cleaned_df) == 4
    assert report["is_clean"] is True


def test_autocleaner_all_nan_column():
    """Verify AutoDataCleaner handles 100% NaN columns gracefully."""
    df_all_nan = pd.DataFrame({
        "all_nan_num": [np.nan, np.nan, np.nan],
        "all_nan_cat": [None, None, None],
        "valid_col": [1, 2, 3],
    })

    cleaner = AutoDataCleaner()
    cleaned = cleaner.fit_transform(df_all_nan)

    assert not cleaned["all_nan_num"].isnull().any()
    assert not cleaned["all_nan_cat"].isnull().any()
    assert (cleaned["all_nan_num"] == 0.0).all()


def test_ml_pipeline_stress_small_dataset():
    """Verify ML pipeline gracefully fits and evaluates on very small datasets (N = 12)."""
    np.random.seed(42)
    small_df = pd.DataFrame({
        "feat_a": np.random.randn(12),
        "feat_b": np.random.randn(12),
        "target": np.random.randn(12) * 10 + 50,
    })

    schema_info = {
        "feat_a": {"unit": "", "phrase": "fitur a"},
        "feat_b": {"unit": "", "phrase": "fitur b"},
        "target": {"unit": "poin", "phrase": "skor target"},
    }

    pipeline = train_fluent_ml_pipeline(
        df_sample=small_df,
        target_col="target",
        candidate_cols=["feat_a", "feat_b"],
        schema_info=schema_info,
        audit_info={},
    )

    assert "model" in pipeline
    assert "benchmark_df" in pipeline
    assert "residuals" in pipeline
    assert pipeline["n_rows"] == 12
    assert pipeline["residuals"]["rmse"] >= 0.0


def test_ml_pipeline_stress_constant_and_collinear_features():
    """Verify ML pipeline automatically detects and drops constant and redundant features."""
    np.random.seed(42)
    n = 100
    x1 = np.random.randn(n)
    df_collinear = pd.DataFrame({
        "useful": x1,
        "constant_col": np.ones(n) * 42.0,
        "perfect_duplicate": x1 * 1.0,  # r = 1.0
        "target": x1 * 3.5 + np.random.randn(n) * 0.1,
    })

    schema_info = {c: {"unit": "", "phrase": c} for c in df_collinear.columns}

    pipeline = train_fluent_ml_pipeline(
        df_sample=df_collinear,
        target_col="target",
        candidate_cols=["useful", "constant_col", "perfect_duplicate"],
        schema_info=schema_info,
        audit_info={},
    )

    # Constant column should be excluded from active features
    assert "constant_col" not in pipeline["feature_cols"]
    # Collinear duplicate should be dropped
    assert "perfect_duplicate" in pipeline["audit_summary"]["dropped_collinear"]
    assert "useful" in pipeline["feature_cols"]


def test_semantic_profiler_stress_mixed_types():
    """Verify build_fluent_schema handles high-cardinality strings, mixed types, and timestamps."""
    dates = pd.date_range("2024-01-01", periods=50, freq="D")
    df_mixed = pd.DataFrame({
        "timestamp": dates,
        "high_cardinality_id": [f"ID_{i:04d}" for i in range(50)],
        "revenue_usd": np.random.uniform(100, 5000, 50),
        "delivery_delay_days": np.random.choice([0, 1, 2, 5, 10], 50),
        "customer_rating": np.random.choice([1, 2, 3, 4, 5], 50),
    })

    clean_df, schema_info, auto_target, audit_info = build_fluent_schema(df_mixed)

    assert auto_target in ("revenue_usd", "customer_rating", "Total Pendapatan", "Penilaian Pembeli")
    raw_names = [meta.get("raw") for meta in schema_info.values()]
    assert "revenue_usd" in raw_names
    assert "delivery_delay_days" in raw_names
    # Check unit detection in schema_info metadata
    rev_meta = next(m for m in schema_info.values() if m.get("raw") == "revenue_usd")
    assert rev_meta["unit"] in ("$", "Rp")
    delay_meta = next(m for m in schema_info.values() if m.get("raw") == "delivery_delay_days")
    assert delay_meta["unit"] == "hari"
    delay_col = next(col for col, meta in schema_info.items() if meta.get("raw") == "delivery_delay_days")
    assert clean_df[delay_col].dtype in (np.float64, np.float32, np.int64)
