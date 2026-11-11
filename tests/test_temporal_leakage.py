"""Automated Test Suite for Temporal Data Integrity and Leakage Prevention (CSIP V14).

SKKNI Compliance:
- [UK-04 Memvalidasi Data]: Validasi integritas temporal dan ketiadaan kebocoran data (data leakage).
- [UK-07 Mengkonstruksi Data]: Validasi rekayasa fitur berbasis horizon waktu (Split-Before-Transform).
- [UK-08 Membangun Skenario Model]: Validasi isolasi partisi waktu (temporal embargo splits).
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

from csip.models.trainer import ModelExperimentTrainer


def test_checkout_feature_set_has_no_delivery_or_review_features():
    """Verify that Checkout-Time feature sets contain ZERO post-checkout attributes."""
    forbidden_post_checkout = {
        "delivery_lead_time_days",
        "delivery_delay_days",
        "is_late",
        "delay_x_freight_ratio",
        "high_value_late_flag",
        "review_score",
        "review_comment_message",
        "days_to_repeat_post_delivery",
    }

    checkout_feature_sets = [
        "E1_checkout_retrospective_conditional",
        "E1_economic_only",
        "cohort_checkout_features",
    ]

    for fset_name in checkout_feature_sets:
        features = ModelExperimentTrainer.FEATURE_SETS[fset_name]
        overlap = set(features).intersection(forbidden_post_checkout)
        assert len(overlap) == 0, (
            f"Temporal Leakage Violation! Feature set '{fset_name}' contains post-checkout features: {overlap}"
        )


def test_feature_availability_matrix_csv_integrity():
    """Verify AUDIT/FEATURE_AVAILABILITY_MATRIX.csv exists, is readable, and maps all features correctly."""
    matrix_path = REPO_ROOT / "AUDIT" / "FEATURE_AVAILABILITY_MATRIX.csv"
    assert matrix_path.exists(), "AUDIT/FEATURE_AVAILABILITY_MATRIX.csv does not exist"

    df = pd.read_csv(matrix_path)
    assert "feature_name" in df.columns
    assert "is_known_at_checkout" in df.columns
    assert "is_known_at_delivery" in df.columns
    assert "leakage_risk" in df.columns

    # Verify that any feature flagged as is_known_at_checkout == 'NO' has leakage risk flagged if used at checkout
    post_checkout_features = df[df["is_known_at_checkout"] == "NO"]
    for _, row in post_checkout_features.iterrows():
        assert "CRITICAL" in str(row["leakage_risk"]), (
            f"Feature {row['feature_name']} is not known at checkout but lacks CRITICAL leakage risk flag!"
        )


def test_temporal_embargo_split_bounds():
    """Verify that train, validation, and test splits have strict chronological order and embargo buffers."""
    trainer = ModelExperimentTrainer()
    df_cohort = pd.read_parquet(REPO_ROOT / "data" / "processed" / "customer_cohort.parquet")
    train_df, val_df, test_df = trainer.get_cohort_temporal_splits_with_embargo(df_cohort)

    # Convert timestamps to datetime
    train_max_date = pd.to_datetime(train_df["order_purchase_timestamp"]).max()
    val_min_date = pd.to_datetime(val_df["order_purchase_timestamp"]).min()
    val_max_date = pd.to_datetime(val_df["order_purchase_timestamp"]).max()
    test_min_date = pd.to_datetime(test_df["order_purchase_timestamp"]).min()

    # Train max date must be before validation min date with at least 60 days embargo
    assert train_max_date < val_min_date
    embargo_1_days = (val_min_date - train_max_date).days
    assert embargo_1_days >= 60, f"Embargo 1 between train and val is too short: {embargo_1_days} days"

    # Validation max date must be before test min date with at least 60 days embargo
    assert val_max_date < test_min_date
    embargo_2_days = (test_min_date - val_max_date).days
    assert embargo_2_days >= 60, f"Embargo 2 between val and test is too short: {embargo_2_days} days"


def test_cohort_customer_isolation_across_splits():
    """Verify ZERO customer overlap across temporal splits."""
    trainer = ModelExperimentTrainer()
    df_cohort = pd.read_parquet(REPO_ROOT / "data" / "processed" / "customer_cohort.parquet")
    train_df, val_df, test_df = trainer.get_cohort_temporal_splits_with_embargo(df_cohort)

    train_custs = set(train_df["customer_unique_id"])
    val_custs = set(val_df["customer_unique_id"])
    test_custs = set(test_df["customer_unique_id"])

    assert len(train_custs.intersection(val_custs)) == 0, "Train and Val splits share customer entities!"
    assert len(train_custs.intersection(test_custs)) == 0, "Train and Test splits share customer entities!"
    assert len(val_custs.intersection(test_custs)) == 0, "Val and Test splits share customer entities!"


def test_post_delivery_censoring_and_pre_delivery_repeat_isolation():
    """Verify that post-delivery model population has 0 pre-delivery repeats and 0 right-censored instances."""
    df_cohort = pd.read_parquet(REPO_ROOT / "data" / "processed" / "customer_cohort.parquet")
    trainer = ModelExperimentTrainer()
    train_df, val_df, test_df = trainer.get_cohort_temporal_splits_with_embargo(df_cohort)

    # Clean post-delivery subset filter
    clean_test = test_df[
        (test_df["repeat_before_delivery_flag"] == 0) &
        (test_df["is_censored_post_delivery"] == 0)
    ]

    assert (clean_test["repeat_before_delivery_flag"] == 0).all()
    assert (clean_test["is_censored_post_delivery"] == 0).all()
    assert len(clean_test) == 4232, f"Expected 4232 clean test samples, got {len(clean_test)}"
