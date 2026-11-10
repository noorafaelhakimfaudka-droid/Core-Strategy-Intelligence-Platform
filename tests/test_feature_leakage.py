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
