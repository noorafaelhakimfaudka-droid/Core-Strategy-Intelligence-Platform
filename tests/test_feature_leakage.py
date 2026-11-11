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
    """Verify that actual early-warning checkout feature set contains zero fulfillment or review leakage."""
    from csip.models.trainer import ModelExperimentTrainer

    cfg = load_yaml_config(REPO_ROOT / "config" / "features.yaml")
    restricted_cols = set(
        cfg["anti_leakage_rules"]["checkout_stage_restricted_features"]
    )

    # Required restricted features
    assert "approval_lag_hours" in restricted_cols
    assert "order_approved_at" in restricted_cols
    assert "order_delivered_customer_date" in restricted_cols
    assert "delivery_delay_days" in restricted_cols
    assert "review_score" in restricted_cols
    assert "review_comment_message" in restricted_cols

    # Inspect REAL feature set from ModelExperimentTrainer
    actual_early_warning_features = ModelExperimentTrainer.FEATURE_SETS["E1_checkout_retrospective_conditional"]

    # Verify zero intersection with post-delivery restricted features
    leakage_cols = set(actual_early_warning_features).intersection(restricted_cols)
    assert len(leakage_cols) == 0, f"REAL Early-Warning feature set has data leakage: {leakage_cols}"
    assert "approval_lag_hours" not in actual_early_warning_features


def test_target_label_integrity_and_zero_contamination():
    """Verify ground truth review target has zero contamination from unobserved reviews."""
    import pandas as pd
    order_path = REPO_ROOT / "data" / "processed" / "order_level.parquet"
    if not order_path.exists():
        pytest.skip("order_level.parquet not yet generated.")

    df = pd.read_parquet(order_path)
    assert "has_observed_review" in df.columns, "Missing has_observed_review flag!"
    
    # 646 orders have missing reviews (must NOT be imputed as neutral score 3)
    n_missing = int(df["negative_review_flag"].isnull().sum())
    assert n_missing == 646, f"Expected 646 missing reviews, got {n_missing}"
    
    # 95,824 orders have observed reviews
    n_observed = int(df["has_observed_review"].sum())
    assert n_observed == 95824, f"Expected 95,824 observed reviews, got {n_observed}"
    
    # Observed negative prevalence must be ~12.81%
    obs_df = df[df["has_observed_review"] == 1]
    prevalence = float(obs_df["negative_review_flag"].mean())
    assert 0.125 <= prevalence <= 0.130, f"Observed prevalence {prevalence:.4f} outside [0.125, 0.130]"


def test_review_target_exact_mapping_values():
    """Verify that review_score maps strictly to binary detractor ground truth:
    1 -> 1.0, 2 -> 1.0, 3 -> 0.0, 4 -> 0.0, 5 -> 0.0, and NaN -> NaN.
    """
    import numpy as np
    import pandas as pd
    order_path = REPO_ROOT / "data" / "processed" / "order_level.parquet"
    if not order_path.exists():
        pytest.skip("order_level.parquet not yet generated.")

    df = pd.read_parquet(order_path)
    
    # 1. Rating 1 must have 100% negative_review_flag == 1.0
    r1 = df[df["review_score"] == 1.0]
    assert len(r1) > 0
    assert (r1["negative_review_flag"] == 1.0).all()

    # 2. Rating 2 must have 100% negative_review_flag == 1.0
    r2 = df[df["review_score"] == 2.0]
    assert len(r2) > 0
    assert (r2["negative_review_flag"] == 1.0).all()

    # 3. Rating 3 must have 100% negative_review_flag == 0.0 (Non-Detractor)
    r3 = df[df["review_score"] == 3.0]
    assert len(r3) > 0
    assert (r3["negative_review_flag"] == 0.0).all()

    # 4. Rating 4 must have 100% negative_review_flag == 0.0
    r4 = df[df["review_score"] == 4.0]
    assert len(r4) > 0
    assert (r4["negative_review_flag"] == 0.0).all()

    # 5. Rating 5 must have 100% negative_review_flag == 0.0
    r5 = df[df["review_score"] == 5.0]
    assert len(r5) > 0
    assert (r5["negative_review_flag"] == 0.0).all()

    # 6. Missing review_score must be strictly NaN
    r_null = df[df["review_score"].isnull()]
    assert len(r_null) == 646
    assert r_null["negative_review_flag"].isnull().all()


def test_repeat_purchase_dual_contract_feature_partition():
    """Verify that cohort_checkout_features contains ZERO post-order fulfillment or review leakage,
    and cohort_post_delivery_features isolates review survey feedback (Finding F-01).
    """
    from csip.models.trainer import ModelExperimentTrainer

    checkout_feats = set(ModelExperimentTrainer.FEATURE_SETS["cohort_checkout_features"])
    post_delivery_feats = set(ModelExperimentTrainer.FEATURE_SETS["cohort_post_delivery_features"])
    survey_feats = set(ModelExperimentTrainer.FEATURE_SETS.get("cohort_post_survey_features", []))

    fulfillment_features = {
        "delivery_lead_time_days",
        "delivery_delay_days",
        "is_late",
    }
    review_survey_features = {
        "review_score",
        "has_review_comment",
    }

    # 1. Primary checkout contract MUST have zero overlap with fulfillment OR review leakage
    all_post_leakage = fulfillment_features.union(review_survey_features)
    leakage_in_checkout = checkout_feats.intersection(all_post_leakage)
    assert len(leakage_in_checkout) == 0, f"Cohort checkout features contain leakage: {leakage_in_checkout}"

    # 2. Post-delivery contract incorporates fulfillment realization at delivery time (t = t_delivered)
    assert fulfillment_features.issubset(post_delivery_feats), "Fulfillment features missing from post-delivery contract"

    # 3. Post-delivery contract STRICTLY EXCLUDES post-delivery review survey feedback (Finding F-01)
    review_leakage_in_delivery = post_delivery_feats.intersection(review_survey_features)
    assert len(review_leakage_in_delivery) == 0, f"Post-delivery features contain review survey leakage: {review_leakage_in_delivery}"

    # 4. Survey contract incorporates review feedback
    assert review_survey_features.issubset(survey_feats), "Survey features missing from post-survey contract"


def test_model_leaderboard_metric_unbiasedness():
    """Verify that PR-AUC metric in ml_leaderboard uses unbiased Average Precision."""
    import json
    board_path = REPO_ROOT / "artifacts" / "reports" / "ml_leaderboard.json"
    if not board_path.exists():
        pytest.skip("ml_leaderboard.json not yet generated.")

    data = json.load(open(board_path, encoding="utf-8"))
    
    # Check naive baseline PR-AUC
    naive_records = [
        d for d in data 
        if d.get("model_name") == "B0_naive_majority" and d.get("split_name") == "validation"
    ]
    assert len(naive_records) > 0, "Missing B0 naive majority validation record!"
    naive_pr_auc = naive_records[0]["pr_auc"]
    
    # Unbiased AP should equal positive prevalence (~0.109 - 0.128), NOT the flawed trapezoidal 0.5545!
    assert naive_pr_auc < 0.15, f"Naive PR-AUC {naive_pr_auc} is inflated! Must be < 0.15 (Average Precision)."


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


def test_first_order_cohort_null_bleeding_regression(tmp_path):
    """Verify that build_customer_cohort does NOT bleed non-null values from Order 2 into Order 1 (P0-3 bug)."""
    import numpy as np
    import pandas as pd
    from csip.features.engineer import FeatureEngineer

    # Create synthetic dataset with a customer having 2 orders plus an anchor order to satisfy 90d censoring buffer:
    # Order 1 has review_score = NaN (unobserved)
    # Order 2 has review_score = 5.0 (at Day 31)
    # Anchor order at Day 150 ensures dataset span > 90 days so Order 1 is not right-censored
    synth_data = pd.DataFrame([
        {
            "customer_unique_id": "cust_bleed_test",
            "order_id": "order_1_first",
            "order_purchase_timestamp": pd.Timestamp("2017-01-01 10:00:00"),
            "total_item_price": 50.0,
            "total_freight": 15.0,
            "total_order_value": 65.0,
            "freight_ratio": 0.30,
            "item_count": 1,
            "product_category": "telefonia",
            "payment_installments_max": 1,
            "payment_type_primary": "credit_card",
            "customer_state": "SP",
            "seller_buyer_distance_km": 25.0,
            "delivery_lead_time_days": 5.0,
            "estimated_lead_time_days": 10.0,
            "delivery_delay_days": -5.0,
            "is_late": 0,
            "review_score": np.nan,  # Order 1 had missing review
            "has_review_comment": 0,
            "delay_x_freight_ratio": 0.0,
            "high_value_late_flag": 0,
        },
        {
            "customer_unique_id": "cust_bleed_test",
            "order_id": "order_2_second",
            "order_purchase_timestamp": pd.Timestamp("2017-02-01 10:00:00"),
            "total_item_price": 200.0,
            "total_freight": 40.0,
            "total_order_value": 240.0,
            "freight_ratio": 0.20,
            "item_count": 2,
            "product_category": "beleza_saude",
            "payment_installments_max": 3,
            "payment_type_primary": "credit_card",
            "customer_state": "SP",
            "seller_buyer_distance_km": 150.0,
            "delivery_lead_time_days": 12.0,
            "estimated_lead_time_days": 15.0,
            "delivery_delay_days": -3.0,
            "is_late": 0,
            "review_score": 5.0,  # Order 2 had 5-star review
            "has_review_comment": 1,
            "delay_x_freight_ratio": 0.0,
            "high_value_late_flag": 0,
        },
        {
            "customer_unique_id": "anchor_cust",
            "order_id": "order_anchor",
            "order_purchase_timestamp": pd.Timestamp("2017-06-01 10:00:00"),
            "total_item_price": 100.0,
            "total_freight": 20.0,
            "total_order_value": 120.0,
            "freight_ratio": 0.20,
            "item_count": 1,
            "product_category": "telefonia",
            "payment_installments_max": 1,
            "payment_type_primary": "credit_card",
            "customer_state": "SP",
            "seller_buyer_distance_km": 50.0,
            "delivery_lead_time_days": 5.0,
            "estimated_lead_time_days": 10.0,
            "delivery_delay_days": -5.0,
            "is_late": 0,
            "review_score": 4.0,
            "has_review_comment": 0,
            "delay_x_freight_ratio": 0.0,
            "high_value_late_flag": 0,
        },
    ])

    fe = FeatureEngineer(processed_dir=tmp_path, delta_w_days=90)
    cohort = fe.build_customer_cohort(synth_data)

    target_rows = cohort[cohort["customer_unique_id"] == "cust_bleed_test"]
    assert len(target_rows) == 1
    row = target_rows.iloc[0]
    assert row["order_id"] == "order_1_first"
    assert row["total_item_price"] == 50.0
    # CRITICAL: review_score of Order 1 MUST remain NaN, NOT bled from Order 2 (5.0)!
    assert pd.isna(row["review_score"]), "REGRESSION DETECTED: Order 2 review_score bled into Order 1!"
    assert row["repeat_purchase_flag"] == 1
    assert row["days_to_repeat"] == 31.0


def test_future_perturbation_invariance(tmp_path):
    """Verify that perturbing future order data leaves first-order cohort features invariant."""
    import pandas as pd
    from csip.features.engineer import FeatureEngineer

    def make_orders(order_2_price, order_2_delay):
        return pd.DataFrame([
            {
                "customer_unique_id": "cust_invar_test",
                "order_id": "order_1",
                "order_purchase_timestamp": pd.Timestamp("2017-01-01 10:00:00"),
                "total_item_price": 80.0,
                "total_freight": 20.0,
                "total_order_value": 100.0,
                "freight_ratio": 0.25,
                "item_count": 1,
                "product_category": "informatica",
                "payment_installments_max": 2,
                "payment_type_primary": "credit_card",
                "customer_state": "RJ",
                "seller_buyer_distance_km": 80.0,
                "delivery_lead_time_days": 6.0,
                "estimated_lead_time_days": 12.0,
                "delivery_delay_days": -6.0,
                "is_late": 0,
                "review_score": 4.0,
                "has_review_comment": 0,
                "delay_x_freight_ratio": 0.0,
                "high_value_late_flag": 0,
            },
            {
                "customer_unique_id": "cust_invar_test",
                "order_id": "order_2",
                "order_purchase_timestamp": pd.Timestamp("2017-02-15 10:00:00"),
                "total_item_price": order_2_price,
                "total_freight": 50.0,
                "total_order_value": order_2_price + 50.0,
                "freight_ratio": 0.10,
                "item_count": 5,
                "product_category": "eletronicos",
                "payment_installments_max": 10,
                "payment_type_primary": "boleto",
                "customer_state": "RJ",
                "seller_buyer_distance_km": 500.0,
                "delivery_lead_time_days": 25.0,
                "estimated_lead_time_days": 10.0,
                "delivery_delay_days": order_2_delay,
                "is_late": 1 if order_2_delay > 0 else 0,
                "review_score": 1.0,
                "has_review_comment": 1,
                "delay_x_freight_ratio": 1.5,
                "high_value_late_flag": 1,
            },
            {
                "customer_unique_id": "anchor_cust",
                "order_id": "order_anchor",
                "order_purchase_timestamp": pd.Timestamp("2017-06-01 10:00:00"),
                "total_item_price": 100.0,
                "total_freight": 20.0,
                "total_order_value": 120.0,
                "freight_ratio": 0.20,
                "item_count": 1,
                "product_category": "telefonia",
                "payment_installments_max": 1,
                "payment_type_primary": "credit_card",
                "customer_state": "SP",
                "seller_buyer_distance_km": 50.0,
                "delivery_lead_time_days": 5.0,
                "estimated_lead_time_days": 10.0,
                "delivery_delay_days": -5.0,
                "is_late": 0,
                "review_score": 4.0,
                "has_review_comment": 0,
                "delay_x_freight_ratio": 0.0,
                "high_value_late_flag": 0,
            },
        ])

    fe = FeatureEngineer(processed_dir=tmp_path, delta_w_days=90)
    cohort_normal = fe.build_customer_cohort(make_orders(150.0, -2.0))
    cohort_perturbed = fe.build_customer_cohort(make_orders(99999.0, 45.0))

    row_norm = cohort_normal[cohort_normal["customer_unique_id"] == "cust_invar_test"].iloc[0]
    row_pert = cohort_perturbed[cohort_perturbed["customer_unique_id"] == "cust_invar_test"].iloc[0]

    # All Order 1 predictor features must be bitwise identical despite massive future Order 2 changes
    feature_cols = [
        "total_item_price", "total_freight", "total_order_value", "freight_ratio",
        "item_count", "seller_buyer_distance_km", "delivery_lead_time_days", "review_score"
    ]
    for col in feature_cols:
        assert row_norm[col] == row_pert[col], f"Feature {col} leaked future data!"



