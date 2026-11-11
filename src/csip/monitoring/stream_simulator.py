"""Chronological Time-Lapse Stream Simulator & Shock Injector.

Replays Olist transactions sequentially across historical weeks (including the real
November 2017 Black Friday volume surge) and injects operational shocks for stress testing:
1. Logistics Strike (+5.0 days delay in SP / RJ).
2. Freight Inflation (+40% freight cost ratio).
3. Consumer Harshness Shift (Concept Drift: 3★ flipped to 1★ for minor delays).

Zero external message brokers required (CPU & 8GB RAM optimized).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd


class StreamSimulator:
    """Chronological replay and operational shock injection engine."""

    BLACK_FRIDAY_WEEK = "2017-W47"
    DEFAULT_REFERENCE_END_DATE = "2018-03-31"

    def __init__(self, data_path: Optional[Union[str, Path]] = None) -> None:
        if data_path is None:
            repo_root = Path(__file__).resolve().parent.parent.parent.parent
            data_path = repo_root / "data" / "processed" / "order_level.parquet"

        self.data_path = Path(data_path)
        if not self.data_path.exists():
            raise FileNotFoundError(f"Processed order dataset not found at: {self.data_path}")

        self.df = pd.read_parquet(self.data_path)
        self.df["order_purchase_timestamp"] = pd.to_datetime(self.df["order_purchase_timestamp"])
        self.df = self.df.sort_values("order_purchase_timestamp").reset_index(drop=True)

        # Build weekly period identifiers
        self.df["week_period"] = self.df["order_purchase_timestamp"].dt.to_period("W")
        self.df["week_str"] = self.df["order_purchase_timestamp"].dt.strftime("%Y-W%U")

        # Reference split (training period up to 2018-03-31)
        ref_mask = self.df["order_purchase_timestamp"] <= self.DEFAULT_REFERENCE_END_DATE
        self.reference_df = self.df[ref_mask].copy().reset_index(drop=True)

        # Pre-compute available week windows
        self._build_week_index()

    def _build_week_index(self) -> None:
        """Index weekly chronological slices with metadata."""
        self.weeks_meta: List[Dict[str, Any]] = []
        grouped = self.df.groupby("week_period", sort=True)

        for period, group in grouped:
            start_date = group["order_purchase_timestamp"].min().strftime("%Y-%m-%d")
            end_date = group["order_purchase_timestamp"].max().strftime("%Y-%m-%d")
            week_str = f"{period.year}-W{period.week:02d}"
            is_bf = (period.year == 2017 and period.week == 47) or (week_str == self.BLACK_FRIDAY_WEEK)
            
            self.weeks_meta.append({
                "period": period,
                "week_str": week_str,
                "start_date": start_date,
                "end_date": end_date,
                "count": len(group),
                "is_black_friday": is_bf,
                "label": f"{week_str} ({start_date} to {end_date}) [N={len(group)}]{' ⚡ BLACK FRIDAY' if is_bf else ''}",
            })

    def get_available_weeks(self) -> List[Dict[str, Any]]:
        """Return the sorted chronological list of weekly stream windows."""
        return self.weeks_meta

    def get_reference_data(self) -> pd.DataFrame:
        """Return the locked training reference slice (orders <= 2018-03-31)."""
        return self.reference_df.copy()

    def get_batch(self, week_str: str) -> pd.DataFrame:
        """Fetch transactions for a specific week identifier."""
        matched = self.df[self.df["week_str"] == week_str]
        if matched.empty:
            # Fallback check against period string
            for w in self.weeks_meta:
                if w["week_str"] == week_str:
                    matched = self.df[self.df["week_period"] == w["period"]]
                    break
        return matched.copy().reset_index(drop=True)

    def get_batch_by_index(self, index: int) -> pd.DataFrame:
        """Fetch transaction batch by chronological week index."""
        if index < 0 or index >= len(self.weeks_meta):
            raise IndexError(f"Week index {index} out of range [0, {len(self.weeks_meta)-1}]")
        period = self.weeks_meta[index]["period"]
        return self.df[self.df["week_period"] == period].copy().reset_index(drop=True)

    def inject_shocks(
        self,
        df: pd.DataFrame,
        strike: bool = False,
        inflation: bool = False,
        harshness: bool = False,
    ) -> pd.DataFrame:
        """Inject synthetic operational shocks into transaction stream for stress-testing.
        
        Args:
            df: Raw stream batch DataFrame.
            strike: Adds +5.0 days delay/lead time in SP and RJ.
            inflation: Shifts total_freight up by +40% and updates freight_ratio.
            harshness: Shifts consumer sensitivity by flipping borderline 3-star reviews to 1-star.
        """
        shocked = df.copy()

        # 1. Logistics Strike Shock
        if strike:
            strike_mask = shocked["customer_state"].isin(["SP", "RJ"])
            if strike_mask.any():
                if "delivery_delay_days" in shocked.columns:
                    shocked.loc[strike_mask, "delivery_delay_days"] = (
                        shocked.loc[strike_mask, "delivery_delay_days"] + 5.0
                    )
                if "delivery_lead_time_days" in shocked.columns:
                    shocked.loc[strike_mask, "delivery_lead_time_days"] = (
                        shocked.loc[strike_mask, "delivery_lead_time_days"] + 5.0
                    )
                if "is_late" in shocked.columns and "delivery_delay_days" in shocked.columns:
                    target_dtype = shocked["is_late"].dtype
                    shocked.loc[strike_mask, "is_late"] = (
                        (shocked.loc[strike_mask, "delivery_delay_days"] > 0).astype(target_dtype)
                    )

        # 2. Freight Inflation Shock (+40%)
        if inflation:
            if "total_freight" in shocked.columns:
                shocked["total_freight"] = shocked["total_freight"] * 1.40
            if "freight_ratio" in shocked.columns and "total_order_value" in shocked.columns:
                shocked["freight_ratio"] = (
                    shocked["total_freight"] / (shocked["total_order_value"] + 1e-4)
                )

        # Recompute interactions if features changed
        if (strike or inflation) and "delay_x_freight_ratio" in shocked.columns:
            shocked["delay_x_freight_ratio"] = (
                shocked["delivery_delay_days"] * shocked["freight_ratio"]
            )
        if strike and "high_value_late_flag" in shocked.columns:
            target_flag_dtype = shocked["high_value_late_flag"].dtype
            shocked.loc[strike_mask, "high_value_late_flag"] = (
                ((shocked.loc[strike_mask, "total_order_value"] > 150) & 
                 (shocked.loc[strike_mask, "delivery_delay_days"] > 0)).astype(target_flag_dtype)
            )

        # 3. Consumer Harshness Shift (Concept Drift)
        if harshness:
            harsh_mask = pd.Series(False, index=shocked.index)
            if "delivery_delay_days" in shocked.columns:
                harsh_mask = harsh_mask | (shocked["delivery_delay_days"] >= 1.0)
            if "review_score" in shocked.columns:
                harsh_mask = harsh_mask | (shocked["review_score"] <= 3.0)

            if "negative_review_flag" in shocked.columns:
                neg_dtype = shocked["negative_review_flag"].dtype
                shocked.loc[harsh_mask, "negative_review_flag"] = (
                    pd.Series(1, index=shocked.index[harsh_mask], dtype=neg_dtype)
                )
            if "review_score" in shocked.columns:
                score_dtype = shocked["review_score"].dtype
                shocked.loc[harsh_mask, "review_score"] = (
                    pd.Series(1.0, index=shocked.index[harsh_mask], dtype=score_dtype)
                )

        return shocked
