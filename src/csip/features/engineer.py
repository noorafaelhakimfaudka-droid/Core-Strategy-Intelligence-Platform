"""CSIP Feature Engineering, Multi-Grain Construction & Anti-Leakage Module.

SKKNI Compliance:
- [UK-05 Menentukan Objek Data]: Konstruksi 4 Objek Data Analitik.
- [UK-07 Mengkonstruksi Data]: Rekayasa fitur ekonomi, pengalaman, as-of histori,
  interaksi non-linear, dan isolasi first-order bebas leakage.

Optimized for 8 GB RAM laptop execution with vectorized operations and Parquet storage.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd

from csip.data.loader import downcast_dataframe

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [CSIP-FEATURES] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def haversine_np(
    lat1: np.ndarray,
    lon1: np.ndarray,
    lat2: np.ndarray,
    lon2: np.ndarray,
) -> np.ndarray:
    """Vectorized Haversine distance in kilometers between two coordinate arrays."""
    # Earth radius in kilometers
    r = 6371.0

    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    # Clip for floating point safety
    a = np.clip(a, 0.0, 1.0)
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return (r * c).astype(np.float32)


class FeatureEngineer:
    """End-to-End Feature Constructor for CSIP Multi-Grain Analytical Datasets.

    Fulfills SKKNI [UK-07 Mengkonstruksi Data].
    """

    def __init__(
        self,
        interim_dir: Union[str, Path] = "data/interim",
        processed_dir: Union[str, Path] = "data/processed",
        delta_w_days: int = 90,
    ) -> None:
        self.interim_dir = Path(interim_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.delta_w_days = delta_w_days

    def build_order_level(self) -> pd.DataFrame:
        """Construct Objek Data 1: Order-Level Analytical Table.

        Grain: order_id
        Output: data/processed/order_level.parquet
        """
        logger.info("Building Order-Level Analytical Dataset...")

        # Load clean interim tables
        orders = pd.read_parquet(self.interim_dir / "clean_orders.parquet")
        items = pd.read_parquet(self.interim_dir / "clean_order_items.parquet")
        payments = pd.read_parquet(self.interim_dir / "clean_order_payments.parquet")
        reviews = pd.read_parquet(self.interim_dir / "clean_order_reviews.parquet")
        customers = pd.read_parquet(self.interim_dir / "clean_customers.parquet")
        sellers = pd.read_parquet(self.interim_dir / "clean_sellers.parquet")
        products = pd.read_parquet(self.interim_dir / "clean_products.parquet")
        geo = pd.read_parquet(self.interim_dir / "clean_geolocation_dedup.parquet")

        # 1. Aggregate Items to Order Grain
        # Join product category and weight to items first
        items_with_prod = items.merge(
            products[["product_id", "product_category_name_english", "product_weight_g"]],
            on="product_id",
            how="left"
        )

        def mode_or_first(s: pd.Series) -> str:
            m = s.mode()
            return str(m[0]) if not m.empty else "unknown"

        items_agg = (
            items_with_prod.groupby("order_id", observed=True)
            .agg(
                total_item_price=("price", "sum"),
                total_freight=("freight_value", "sum"),
                item_count=("order_item_id", "count"),
                seller_id=("seller_id", mode_or_first),
                product_category=("product_category_name_english", mode_or_first),
                mean_product_weight_g=("product_weight_g", "mean"),
            )
            .reset_index()
        )

        # 2. Aggregate Payments to Order Grain
        payments_agg = (
            payments.groupby("order_id", observed=True)
            .agg(
                total_payment_value=("payment_value", "sum"),
                payment_installments_max=("payment_installments", "max"),
                payment_type_primary=("payment_type", mode_or_first),
            )
            .reset_index()
        )

        # 3. Base Merge: Orders + Items + Payments
        df = orders.merge(items_agg, on="order_id", how="inner")
        df = df.merge(payments_agg, on="order_id", how="left")
        df = df.merge(
            customers[["customer_id", "customer_unique_id", "customer_state", "customer_zip_code_prefix"]],
            on="customer_id",
            how="left"
        )
        df = df.merge(
            sellers[["seller_id", "seller_state", "seller_zip_code_prefix"]],
            on="seller_id",
            how="left"
        )

        # 4. Geolocation Spatial Distance
        # Merge buyer coordinates
        df = df.merge(
            geo.rename(columns={
                "geolocation_zip_code_prefix": "customer_zip_code_prefix",
                "geolocation_lat": "buyer_lat",
                "geolocation_lng": "buyer_lng",
            })[["customer_zip_code_prefix", "buyer_lat", "buyer_lng"]],
            on="customer_zip_code_prefix",
            how="left"
        )
        # Merge seller coordinates
        df = df.merge(
            geo.rename(columns={
                "geolocation_zip_code_prefix": "seller_zip_code_prefix",
                "geolocation_lat": "seller_lat",
                "geolocation_lng": "seller_lng",
            })[["seller_zip_code_prefix", "seller_lat", "seller_lng"]],
            on="seller_zip_code_prefix",
            how="left"
        )

        # Default fallback coordinates for missing zip codes (São Paulo centroid)
        df["buyer_lat"] = df["buyer_lat"].fillna(-23.5505)
        df["buyer_lng"] = df["buyer_lng"].fillna(-46.6333)
        df["seller_lat"] = df["seller_lat"].fillna(-23.5505)
        df["seller_lng"] = df["seller_lng"].fillna(-46.6333)

        df["seller_buyer_distance_km"] = haversine_np(
            df["seller_lat"].values,
            df["seller_lng"].values,
            df["buyer_lat"].values,
            df["buyer_lng"].values,
        )

        # 5. Economic & Fulfillment Experience Features
        df["total_order_value"] = (df["total_item_price"] + df["total_freight"]).astype(np.float32)
        df["freight_ratio"] = (df["total_freight"] / (df["total_item_price"] + 1e-5)).astype(np.float32)

        df["delivery_lead_time_days"] = (
            (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.total_seconds() / 86400.0
        ).astype(np.float32)

        df["estimated_lead_time_days"] = (
            (df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]).dt.total_seconds() / 86400.0
        ).astype(np.float32)

        df["delivery_delay_days"] = (
            (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.total_seconds() / 86400.0
        ).astype(np.float32)

        df["is_late"] = (df["delivery_delay_days"] > 0).astype(np.int8)

        df["approval_lag_hours"] = (
            (df["order_approved_at"] - df["order_purchase_timestamp"]).dt.total_seconds() / 3600.0
        ).fillna(0.0).astype(np.float32)

        # 6. Merge Reviews & Satisfaction Target (Zero Target Contamination)
        df = df.merge(
            reviews[["order_id", "review_score", "has_review_comment"]],
            on="order_id",
            how="left"
        )
        # Separate unobserved feedback from observed ratings
        df["has_observed_review"] = df["review_score"].notnull().astype(np.int8)
        # Ground truth target: 1 if rating <= 2, 0 if rating >= 3, NaN if unobserved
        df["negative_review_flag"] = np.where(
            df["review_score"].notnull(),
            (df["review_score"] <= 2).astype(np.float32),
            np.nan
        )
        df["has_review_comment"] = df["has_review_comment"].fillna(0).astype(np.int8)

        # 7. Non-linear Interaction Terms
        df["delay_x_freight_ratio"] = (
            np.maximum(0.0, df["delivery_delay_days"]) * df["freight_ratio"]
        ).astype(np.float32)

        df["distance_x_weight"] = (
            df["seller_buyer_distance_km"] * np.log1p(df["mean_product_weight_g"].fillna(500.0))
        ).astype(np.float32)

        q75_val = float(df["total_order_value"].quantile(0.75))
        df["high_value_late_flag"] = (
            (df["total_order_value"] > q75_val).astype(np.int8) * df["is_late"]
        ).astype(np.int8)

        # 8. As-Of Point-in-Time Behavioral History (Prior Orders)
        df = df.sort_values(by=["customer_unique_id", "order_purchase_timestamp"]).reset_index(drop=True)
        df["prior_order_count"] = df.groupby("customer_unique_id").cumcount().astype(np.int16)

        # Downcast and save
        df_opt, _, _ = downcast_dataframe(df)
        out_path = self.processed_dir / "order_level.parquet"
        df_opt.to_parquet(out_path, index=False)
        logger.info("Saved 'order_level.parquet': %d rows, %d columns", len(df_opt), len(df_opt.columns))
        return df_opt

    def build_customer_cohort(self, order_level_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Construct Objek Data 2: Customer Cohort Retention Dataset.

        Enforces System Specification Section 6.3:
        1. Strict First-Order Isolation: Predictors use Order 1 features ONLY.
        2. Right-Censoring Mitigation: Excludes customers whose Order 1 occurred
           within delta_w_days of dataset maximum date.

        Grain: customer_unique_id
        Output: data/processed/customer_cohort.parquet
        """
        logger.info("Building Customer-Cohort Retention Dataset (with Zero Leakage & Censoring Mitigation)...")

        if order_level_df is None:
            order_level_df = pd.read_parquet(self.processed_dir / "order_level.parquet")

        # Sort chronologically per customer
        df_sorted = order_level_df.sort_values(
            by=["customer_unique_id", "order_purchase_timestamp"]
        ).reset_index(drop=True)

        # Identify Order 1 (first transaction)
        order_1 = df_sorted.groupby("customer_unique_id").first().reset_index()

        # Compute transaction counts and repeat status within delta_w_days
        # Order 2 timestamp calculation
        order_2 = df_sorted.groupby("customer_unique_id").nth(1).reset_index()
        order_2_times = dict(zip(order_2["customer_unique_id"], order_2["order_purchase_timestamp"]))

        # Calculate time between order 1 and order 2
        order_1["second_order_timestamp"] = order_1["customer_unique_id"].map(order_2_times)
        order_1["days_to_repeat"] = (
            (order_1["second_order_timestamp"] - order_1["order_purchase_timestamp"]).dt.total_seconds() / 86400.0
        )

        # Label: Repeat purchase within delta_w_days
        order_1["repeat_purchase_flag"] = (
            order_1["days_to_repeat"].notnull()
            & (order_1["days_to_repeat"] <= float(self.delta_w_days))
        ).astype(np.int8)

        # Right-Censoring Buffer:
        t_max = df_sorted["order_purchase_timestamp"].max()
        cutoff_date = t_max - pd.Timedelta(days=self.delta_w_days)

        order_1["is_censored"] = (order_1["order_purchase_timestamp"] > cutoff_date).astype(np.int8)
        cohort_clean = order_1[order_1["is_censored"] == 0].copy()

        # Select strictly FIRST-ORDER predictor columns (Zero Data Leakage Guarantee)
        first_order_features = [
            "customer_unique_id",
            "order_id",
            "order_purchase_timestamp",
            "total_item_price",
            "total_freight",
            "total_order_value",
            "freight_ratio",
            "item_count",
            "product_category",
            "payment_installments_max",
            "payment_type_primary",
            "customer_state",
            "seller_buyer_distance_km",
            "delivery_lead_time_days",
            "estimated_lead_time_days",
            "delivery_delay_days",
            "is_late",
            "review_score",
            "has_review_comment",
            "delay_x_freight_ratio",
            "high_value_late_flag",
            # Targets & Metadata
            "repeat_purchase_flag",
            "days_to_repeat",
        ]

        cohort_clean = cohort_clean[first_order_features].copy()
        cohort_opt, _, _ = downcast_dataframe(cohort_clean)

        out_path = self.processed_dir / "customer_cohort.parquet"
        cohort_opt.to_parquet(out_path, index=False)

        repeat_rate = (cohort_opt["repeat_purchase_flag"].mean()) * 100
        logger.info(
            "Saved 'customer_cohort.parquet': %d customers (after %d censored excluded), Repeat Rate: %.2f%%",
            len(cohort_opt),
            int(order_1["is_censored"].sum()),
            repeat_rate,
        )
        return cohort_opt

    def build_review_corpus(self) -> pd.DataFrame:
        """Construct Objek Data 3: Review Text Corpus for NLP & Sequence Deep Learning.

        Grain: review_id
        Output: data/processed/review_corpus.parquet
        """
        logger.info("Building Review Text Corpus Dataset...")
        reviews = pd.read_parquet(self.interim_dir / "clean_order_reviews.parquet")

        df = pd.DataFrame({
            "review_id": reviews["review_id"],
            "order_id": reviews["order_id"],
            "review_score": reviews["review_score"].astype(np.int8),
            "negative_review_flag": (reviews["review_score"] <= 2).astype(np.int8),
            "review_comment_message": reviews["review_comment_message"],
            "has_review_comment": reviews["has_review_comment"].astype(np.int8),
            "char_length": reviews["review_comment_message"].str.len().astype(np.int16),
            "word_count": reviews["review_comment_message"].apply(lambda t: len(t.split())).astype(np.int16),
            "review_creation_date": reviews["review_creation_date"],
        })

        out_path = self.processed_dir / "review_corpus.parquet"
        df.to_parquet(out_path, index=False)
        logger.info("Saved 'review_corpus.parquet': %d reviews", len(df))
        return df

    def build_weekly_system_state(self, order_level_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Construct Objek Data 4: Weekly System State Panel for World Model.

        Grain: year_week
        Output: data/processed/weekly_system_state.parquet
        """
        logger.info("Building Weekly System State Panel for World Model...")

        if order_level_df is None:
            order_level_df = pd.read_parquet(self.processed_dir / "order_level.parquet")

        df = order_level_df.copy()
        df["year_week"] = df["order_purchase_timestamp"].dt.to_period("W").astype(str)

        # Aggregate metrics per week
        weekly = (
            df.groupby("year_week", observed=True)
            .agg(
                weekly_order_volume=("order_id", "count"),
                mean_item_price=("total_item_price", "mean"),
                mean_freight_value=("total_freight", "mean"),
                mean_freight_ratio=("freight_ratio", "mean"),
                mean_delivery_days=("delivery_lead_time_days", "mean"),
                mean_delivery_delay=("delivery_delay_days", "mean"),
                delay_rate=("is_late", "mean"),
                negative_review_rate=("negative_review_flag", "mean"),
                mean_review_score=("review_score", "mean"),
            )
            .reset_index()
        )

        # Filter complete weekly panel (2017-01 onwards)
        weekly = weekly[weekly["year_week"] >= "2017-01"].sort_values("year_week").reset_index(drop=True)
        weekly_opt, _, _ = downcast_dataframe(weekly)

        out_path = self.processed_dir / "weekly_system_state.parquet"
        weekly_opt.to_parquet(out_path, index=False)
        logger.info("Saved 'weekly_system_state.parquet': %d weeks", len(weekly_opt))
        return weekly_opt

    def build_all(self) -> Dict[str, pd.DataFrame]:
        """Execute full feature engineering and multi-grain construction."""
        order_level = self.build_order_level()
        cohort = self.build_customer_cohort(order_level)
        corpus = self.build_review_corpus()
        weekly = self.build_weekly_system_state(order_level)
        return {
            "order_level": order_level,
            "customer_cohort": cohort,
            "review_corpus": corpus,
            "weekly_system_state": weekly,
        }

