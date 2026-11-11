"""
CSIP Data Contracts & Schema Validation Engine
Defines declarative contracts for data ingestion, cleaning, and feature pipelines.
Categorizes validation findings into INVALID (fatal), SUSPICIOUS (out-of-bound/warning),
and VALID_ANOMALOUS (extreme but plausible business observations).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
import pandas as pd
import numpy as np


@dataclass
class ValidationReport:
    contract_name: str
    total_rows: int
    is_valid: bool
    fatal_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suspicious_row_indices: List[int] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contract_name": self.contract_name,
            "total_rows": self.total_rows,
            "is_valid": self.is_valid,
            "fatal_errors_count": len(self.fatal_errors),
            "fatal_errors": self.fatal_errors,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings,
            "suspicious_rows_count": len(self.suspicious_row_indices),
            "metrics": self.metrics,
        }


class DataContract:
    """Base class for CSIP dataset contracts."""
    contract_name: str = "BaseContract"
    required_columns: Dict[str, str] = {}  # col_name -> type_category ('numeric', 'string', 'datetime')
    unique_columns: List[str] = []
    non_null_columns: List[str] = []
    value_ranges: Dict[str, Tuple[Optional[float], Optional[float]]] = {}
    allowed_categories: Dict[str, Set[str]] = {}

    @classmethod
    def validate(cls, df: pd.DataFrame) -> ValidationReport:
        fatal_errors = []
        warnings = []
        suspicious_indices = set()
        metrics = {}

        total_rows = len(df)
        if total_rows == 0:
            return ValidationReport(
                contract_name=cls.contract_name,
                total_rows=0,
                is_valid=False,
                fatal_errors=["Dataset is empty (0 rows)."]
            )

        # 1. Required Columns Check
        missing_cols = [c for c in cls.required_columns if c not in df.columns]
        if missing_cols:
            fatal_errors.append(f"Missing required columns: {missing_cols}")

        # 2. Type & Category Checks
        for col, expected_type in cls.required_columns.items():
            if col in df.columns:
                if expected_type == "numeric":
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        try:
                            pd.to_numeric(df[col].dropna())
                            warnings.append(f"Column '{col}' is object dtype but coercible to numeric.")
                        except Exception:
                            fatal_errors.append(f"Column '{col}' must be numeric, got {df[col].dtype}.")
                elif expected_type == "datetime":
                    if not pd.api.types.is_datetime64_any_dtype(df[col]):
                        try:
                            pd.to_datetime(df[col].dropna().iloc[:10])
                            warnings.append(f"Column '{col}' is stored as string/object; should be parsed to datetime.")
                        except Exception:
                            fatal_errors.append(f"Column '{col}' cannot be parsed as datetime.")

        # 3. Non-Null Constraints
        for col in cls.non_null_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    null_pct = (null_count / total_rows) * 100
                    fatal_errors.append(f"Non-null constraint violated: '{col}' has {null_count:,} nulls ({null_pct:.2f}%).")

        # 4. Uniqueness Constraints
        for col in cls.unique_columns:
            if col in df.columns:
                dup_count = df[col].duplicated().sum()
                if dup_count > 0:
                    fatal_errors.append(f"Uniqueness constraint violated: '{col}' has {dup_count:,} duplicate values.")

        # 5. Value Ranges & Suspicious Bounds
        for col, (min_val, max_val) in cls.value_ranges.items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                vals = df[col].dropna()
                if min_val is not None:
                    viol = vals[vals < min_val]
                    if len(viol) > 0:
                        warnings.append(f"Column '{col}' has {len(viol):,} values below minimum ({min_val}).")
                        suspicious_indices.update(viol.index.tolist())
                if max_val is not None:
                    viol = vals[vals > max_val]
                    if len(viol) > 0:
                        warnings.append(f"Column '{col}' has {len(viol):,} values above maximum ({max_val}).")
                        suspicious_indices.update(viol.index.tolist())

        # 6. Categorical Allowed Sets
        for col, allowed_set in cls.allowed_categories.items():
            if col in df.columns:
                actual_cats = set(df[col].dropna().astype(str).unique())
                unrecognized = actual_cats - allowed_set
                if unrecognized:
                    warnings.append(f"Column '{col}' contains unrecognized categories: {list(unrecognized)[:5]}")

        metrics["column_count"] = len(df.columns)
        metrics["total_memory_mb"] = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        metrics["duplicate_rows"] = int(df.duplicated().sum())

        is_valid = len(fatal_errors) == 0

        return ValidationReport(
            contract_name=cls.contract_name,
            total_rows=total_rows,
            is_valid=is_valid,
            fatal_errors=fatal_errors,
            warnings=warnings,
            suspicious_row_indices=sorted(list(suspicious_indices)),
            metrics=metrics,
        )


class RawOlistOrdersContract(DataContract):
    contract_name = "RawOlistOrdersContract"
    required_columns = {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "string",
        "order_purchase_timestamp": "datetime",
    }
    unique_columns = ["order_id"]
    non_null_columns = ["order_id", "customer_id", "order_status", "order_purchase_timestamp"]
    allowed_categories = {
        "order_status": {"delivered", "shipped", "canceled", "invoiced", "processing", "unavailable", "created", "approved"}
    }


class RawOlistReviewsContract(DataContract):
    contract_name = "RawOlistReviewsContract"
    required_columns = {
        "review_id": "string",
        "order_id": "string",
        "review_score": "numeric",
        "review_creation_date": "datetime",
    }
    non_null_columns = ["review_id", "order_id", "review_score"]
    value_ranges = {
        "review_score": (1.0, 5.0)
    }


class CleanOrderLevelContract(DataContract):
    contract_name = "CleanOrderLevelContract"
    required_columns = {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "string",
        "order_purchase_timestamp": "datetime",
        "total_payment_value": "numeric",
        "total_freight": "numeric",
        "total_item_price": "numeric",
        "delivery_delay_days": "numeric",
        "negative_review_flag": "numeric",
    }
    unique_columns = ["order_id"]
    non_null_columns = ["order_id", "customer_id", "order_status"]
    value_ranges = {
        "negative_review_flag": (0.0, 1.0),
        "total_payment_value": (0.0, 100000.0),
        "delivery_delay_days": (-60.0, 200.0),
    }


class CustomerCohortContract(DataContract):
    contract_name = "CustomerCohortContract"
    required_columns = {
        "customer_unique_id": "string",
        "order_id": "string",
        "repeat_purchase_flag": "numeric",
        "repeat_purchase_post_delivery_flag": "numeric",
        "total_order_value": "numeric",
    }
    non_null_columns = ["customer_unique_id", "order_id", "repeat_purchase_flag"]
    value_ranges = {
        "repeat_purchase_flag": (0.0, 1.0),
        "repeat_purchase_post_delivery_flag": (0.0, 1.0),
        "total_order_value": (0.0, 100000.0),
    }


class WeeklySystemStateContract(DataContract):
    contract_name = "WeeklySystemStateContract"
    required_columns = {
        "year_week": "string",
        "weekly_order_volume": "numeric",
        "mean_delivery_delay": "numeric",
        "negative_review_rate": "numeric",
    }
    non_null_columns = ["year_week", "weekly_order_volume"]
    value_ranges = {
        "weekly_order_volume": (1.0, 50000.0),
        "negative_review_rate": (0.0, 1.0),
    }
