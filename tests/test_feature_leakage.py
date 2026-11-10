"""Unit tests for Anti-Leakage Governance and Point-in-Time Correctness.

SKKNI Compliance:
- [UK-07 Mengkonstruksi Data]
- [UK-08 Membangun Skenario Model]
"""

import sys
from pathlib import Path
import pytest

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.data.loader import load_yaml_config


def test_checkout_stage_restricted_features():
    """Verify that checkout-time prediction feature sets contain no fulfillment or review leakage."""
    cfg = load_yaml_config(REPO_ROOT / "config" / "features.yaml")
    restricted_cols = set(
        cfg["anti_leakage_rules"]["checkout_stage_restricted_features"]
    )

    # Required restricted features
    assert "order_delivered_customer_date" in restricted_cols
    assert "delivery_delay_days" in restricted_cols
    assert "review_score" in restricted_cols
    assert "review_comment_message" in restricted_cols

    # Simulated candidate checkout feature list
    checkout_features = [
        "total_item_price",
        "total_freight",
        "freight_ratio",
        "item_count",
        "payment_installments_max",
        "seller_buyer_distance_km",
        "approval_lag_hours",
    ]

    # Verify zero intersection with post-delivery restricted features
    leakage_cols = set(checkout_features).intersection(restricted_cols)
    assert len(leakage_cols) == 0, f"Checkout feature set has data leakage: {leakage_cols}"


def test_first_order_repeat_prediction_prohibited_aggregates():
    """Verify that lifetime aggregates are prohibited when predicting repeat purchase."""
    cfg = load_yaml_config(REPO_ROOT / "config" / "features.yaml")
    prohibited_cols = set(
        cfg["anti_leakage_rules"]["first_order_repeat_prediction_rule"]["prohibited_sources"]
    )

    # Prohibited columns
    assert "lifetime_order_count" in prohibited_cols
    assert "lifetime_total_spend" in prohibited_cols
    assert "lifetime_avg_review" in prohibited_cols

    # Valid first-order features
    valid_first_order_features = [
        "first_order_price",
        "first_order_freight",
        "first_order_freight_ratio",
        "first_order_delivery_delay",
        "first_order_review_score",
        "first_order_item_count",
    ]

    for col in valid_first_order_features:
        assert col not in prohibited_cols


def test_split_before_transform_policy():
    """Verify that transformers requiring split-before-transform are explicitly specified."""
    cfg = load_yaml_config(REPO_ROOT / "config" / "features.yaml")
    training_only_fit = cfg["anti_leakage_rules"]["split_before_transform_enforcement"]["training_only_fit"]

    assert "StandardScaler" in training_only_fit
    assert "MinMaxScaler" in training_only_fit
    assert "SimpleImputer" in training_only_fit
    assert "TfidfVectorizer" in training_only_fit


def test_processed_customer_cohort_zero_leakage():
    """Verify that actual customer_cohort.parquet has zero lifetime aggregate columns."""
    cohort_path = REPO_ROOT / "data" / "processed" / "customer_cohort.parquet"
    if not cohort_path.exists():
        pytest.skip("customer_cohort.parquet not yet generated.")

    import pandas as pd
    cohort_df = pd.read_parquet(cohort_path)

    # 1. Zero prohibited lifetime columns
    prohibited = ["lifetime_order_count", "lifetime_total_spend", "lifetime_avg_review"]
    for col in prohibited:
        assert col not in cohort_df.columns, f"LEAKAGE: {col} present in customer_cohort!"

    # 2. Key uniqueness
    assert cohort_df["customer_unique_id"].is_unique, "customer_unique_id not unique in cohort!"

    # 3. Valid target values
    assert set(cohort_df["repeat_purchase_flag"].unique()).issubset({0, 1})

    # 4. Positive rate is sensible (~2-3% after right-censoring exclusion)
    repeat_rate = cohort_df["repeat_purchase_flag"].mean()
    assert 0.01 <= repeat_rate <= 0.05, f"Unexpected repeat rate: {repeat_rate}"


def test_processed_order_level_engineered_features():
    """Verify order_level.parquet contains all engineered features and valid types."""
    order_path = REPO_ROOT / "data" / "processed" / "order_level.parquet"
    if not order_path.exists():
        pytest.skip("order_level.parquet not yet generated.")

    import pandas as pd
    order_df = pd.read_parquet(order_path)

    # Engineered columns presence
    required_cols = [
        "total_order_value",
        "freight_ratio",
        "delivery_lead_time_days",
        "delivery_delay_days",
        "seller_buyer_distance_km",
        "delay_x_freight_ratio",
        "distance_x_weight",
        "high_value_late_flag",
        "is_late",
        "negative_review_flag",
    ]
    for col in required_cols:
        assert col in order_df.columns, f"Missing engineered column: {col}"

    # Non-negative checks
    assert (order_df["total_order_value"] > 0).all()
    assert (order_df["freight_ratio"] >= 0).all()
    assert (order_df["seller_buyer_distance_km"] >= 0).all()


