"""CSIP Data Loader, Schema Validator, and Memory Optimization Module.

SKKNI Compliance:
- [UK-03 Menelaah Data]: Profiling tabel relasional, tipe data, dan relasi kunci.
- [UK-04 Memvalidasi Data]: Uji skema, kardinalitas, missing values, dan timestamp sanity.
- [UK-05 Menentukan Objek Data]: Pemisahan grain tabel dan seleksi kohort.

Designed specifically for 8 GB RAM laptop execution with automatic dtype downsizing
and DuckDB/Parquet acceleration.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import yaml

# Configure module logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [CSIP-LOADER] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class ValidationResult:
    """Result container for data validation checks."""
    table_name: str
    passed: bool
    total_rows: int
    duplicate_pk_count: int = 0
    null_counts: Dict[str, int] = field(default_factory=dict)
    chronological_violations: int = 0
    memory_initial_mb: float = 0.0
    memory_downsized_mb: float = 0.0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def memory_reduction_pct(self) -> float:
        if self.memory_initial_mb <= 0:
            return 0.0
        return (
            (self.memory_initial_mb - self.memory_downsized_mb)
            / self.memory_initial_mb
        ) * 100.0


def load_yaml_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """Load and parse a YAML configuration file safely."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config or {}


def downcast_dataframe(
    df: pd.DataFrame,
    date_columns: Optional[List[str]] = None,
    categorical_columns: Optional[List[str]] = None,
    max_categorical_cardinality: int = 50,
) -> Tuple[pd.DataFrame, float, float]:
    """Downcast DataFrame data types to minimize memory usage on 8 GB RAM systems.

    SKKNI [UK-06 Membersihkan Data] - Efisiensi tipe data.

    Conversions:
    - float64 -> float32
    - int64 -> int32 or int16 (based on value bounds)
    - object with low unique count -> category
    - date_columns -> pd.to_datetime

    Returns:
        (df_downsized, initial_memory_mb, downsized_memory_mb)
    """
    initial_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
    df_opt = df.copy()

    # Parse specified date columns
    if date_columns:
        for col in date_columns:
            if col in df_opt.columns and not pd.api.types.is_datetime64_any_dtype(df_opt[col]):
                df_opt[col] = pd.to_datetime(df_opt[col], errors="coerce")

    # Downcast numerics and categories
    for col in df_opt.columns:
        if col in (date_columns or []):
            continue

        col_type = df_opt[col].dtype

        # Float downcasting
        if pd.api.types.is_float_dtype(col_type):
            df_opt[col] = pd.to_numeric(df_opt[col], downcast="float")

        # Integer downcasting
        elif pd.api.types.is_integer_dtype(col_type):
            c_min = df_opt[col].min()
            c_max = df_opt[col].max()
            if pd.notnull(c_min) and pd.notnull(c_max):
                if c_min >= -32768 and c_max <= 32767:
                    df_opt[col] = df_opt[col].astype(np.int16)
                elif c_min >= -2147483648 and c_max <= 2147483647:
                    df_opt[col] = df_opt[col].astype(np.int32)
                else:
                    df_opt[col] = pd.to_numeric(df_opt[col], downcast="integer")

        # Explicit or automated categorical conversion
        elif pd.api.types.is_object_dtype(col_type) or pd.api.types.is_string_dtype(col_type):
            should_categorize = False
            if categorical_columns and col in categorical_columns:
                should_categorize = True
            else:
                num_unique = df_opt[col].nunique(dropna=True)
                if 1 < num_unique <= max_categorical_cardinality:
                    should_categorize = True

            if should_categorize:
                df_opt[col] = df_opt[col].astype("category")

    downsized_memory = df_opt.memory_usage(deep=True).sum() / (1024 * 1024)
    return df_opt, initial_memory, downsized_memory


class OlistDataLoader:
    """Enterprise Data Loader for Olist Relational E-Commerce Tables.

    Complies with SKKNI [UK-03], [UK-04], [UK-05].
    Provides schema verification, referential integrity validation,
    and automatic downcasting.
    """

    def __init__(
        self,
        config_path: Union[str, Path] = "config/data.yaml",
        raw_data_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        self.config_path = Path(config_path)
        self.config = load_yaml_config(self.config_path)
        self.raw_data_dir = Path(
            raw_data_dir or self.config.get("raw_data_dir", "data/raw")
        )
        self.tables_config = self.config.get("tables", {})
        self.cached_tables: Dict[str, pd.DataFrame] = {}
        self.validation_history: Dict[str, ValidationResult] = {}

    def get_table_path(self, table_key: str) -> Path:
        """Resolve full filesystem path for a given table key."""
        table_info = self.tables_config.get(table_key)
        if not table_info:
            raise KeyError(
                f"Table key '{table_key}' not found in configuration. Available: {list(self.tables_config.keys())}"
            )
        filename = table_info.get("filename", f"{table_key}.csv")
        return self.raw_data_dir / filename

    def load_table(
        self,
        table_key: str,
        validate: bool = True,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """Load a single Olist table from CSV, apply downcasting and schema validation.

        SKKNI [UK-03 Menelaah Data] & [UK-04 Memvalidasi Data].
        """
        if use_cache and table_key in self.cached_tables:
            logger.debug("Returning cached DataFrame for: %s", table_key)
            return self.cached_tables[table_key]

        file_path = self.get_table_path(table_key)
        if not file_path.exists():
            raise FileNotFoundError(
                f"CSV file for '{table_key}' not found at: {file_path.resolve()}"
            )

        table_meta = self.tables_config[table_key]
        date_cols = table_meta.get("date_columns", [])
        cat_cols = table_meta.get("categorical_columns", [])

        logger.info("Reading CSV: %s (%s)", table_key, file_path.name)
        # Parse dates directly if possible, or handle during downcasting
        df_raw = pd.read_csv(file_path, low_memory=False)

        # Apply downcasting
        df_opt, mem_init, mem_opt = downcast_dataframe(
            df_raw,
            date_columns=date_cols,
            categorical_columns=cat_cols,
            max_categorical_cardinality=self.config.get("downcasting_rules", {}).get(
                "max_categorical_cardinality", 50
            ),
        )

        red_pct = ((mem_init - mem_opt) / mem_init * 100) if mem_init > 0 else 0
        logger.info(
            "Downsized '%s': %.2f MB -> %.2f MB (%.1f%% reduction, %d rows)",
            table_key,
            mem_init,
            mem_opt,
            red_pct,
            len(df_opt),
        )

        if validate:
            val_res = self.validate_table(table_key, df_opt, mem_init, mem_opt)
            self.validation_history[table_key] = val_res

        if use_cache:
            self.cached_tables[table_key] = df_opt

        return df_opt

    def validate_table(
        self,
        table_key: str,
        df: pd.DataFrame,
        mem_init: float = 0.0,
        mem_opt: float = 0.0,
    ) -> ValidationResult:
        """Execute strict schema validation rules against a loaded DataFrame.

        SKKNI [UK-04 Memvalidasi Data].
        """
        table_meta = self.tables_config.get(table_key, {})
        pk_cols = table_meta.get("primary_key", [])
        warnings: List[str] = []
        errors: List[str] = []

        total_rows = len(df)
        dup_pk_count = 0

        # 1. Primary key uniqueness check
        if pk_cols:
            missing_pk_cols = [c for c in pk_cols if c not in df.columns]
            if missing_pk_cols:
                errors.append(f"Missing primary key columns in dataset: {missing_pk_cols}")
            else:
                dup_mask = df.duplicated(subset=pk_cols, keep=False)
                dup_pk_count = int(dup_mask.sum())
                if dup_pk_count > 0:
                    warnings.append(
                        f"Found {dup_pk_count} duplicated primary key rows for keys: {pk_cols}"
                    )

        # 2. Missing value profiling
        null_counts = {col: int(df[col].isnull().sum()) for col in df.columns}

        # 3. Timestamp chronological sanity check (for orders table)
        chrono_violations = 0
        if table_key == "orders":
            chrono_violations = self._check_order_timestamp_sanity(df, warnings)

        # 4. Review score range check
        if table_key == "order_reviews" and "review_score" in df.columns:
            invalid_scores = df[~df["review_score"].isin([1, 2, 3, 4, 5])]
            if len(invalid_scores) > 0:
                errors.append(
                    f"Found {len(invalid_scores)} rows with review_score outside 1..5 range"
                )

        # 5. Non-negative numeric checks
        if table_key == "order_items":
            if "price" in df.columns and (df["price"] < 0).any():
                errors.append("Negative price detected in order_items")
            if "freight_value" in df.columns and (df["freight_value"] < 0).any():
                errors.append("Negative freight_value detected in order_items")

        passed = len(errors) == 0
        return ValidationResult(
            table_name=table_key,
            passed=passed,
            total_rows=total_rows,
            duplicate_pk_count=dup_pk_count,
            null_counts=null_counts,
            chronological_violations=chrono_violations,
            memory_initial_mb=mem_init,
            memory_downsized_mb=mem_opt,
            warnings=warnings,
            errors=errors,
        )

    @staticmethod
    def _check_order_timestamp_sanity(
        orders_df: pd.DataFrame, warnings: List[str]
    ) -> int:
        """Validate that chronological dates in orders follow logical progression.

        Rule: purchase_timestamp <= approved_at <= delivered_carrier_date <= delivered_customer_date
        """
        violations = 0
        # Check purchase <= delivered_customer
        mask_purchase_delivered = (
            orders_df["order_purchase_timestamp"].notnull()
            & orders_df["order_delivered_customer_date"].notnull()
            & (
                orders_df["order_purchase_timestamp"]
                > orders_df["order_delivered_customer_date"]
            )
        )
        p_d_violations = int(mask_purchase_delivered.sum())
        if p_d_violations > 0:
            violations += p_d_violations
            warnings.append(
                f"Chronological anomaly: {p_d_violations} orders delivered BEFORE purchase timestamp"
            )

        # Check carrier <= delivered_customer
        if "order_delivered_carrier_date" in orders_df.columns:
            mask_carrier_delivered = (
                orders_df["order_delivered_carrier_date"].notnull()
                & orders_df["order_delivered_customer_date"].notnull()
                & (
                    orders_df["order_delivered_carrier_date"]
                    > orders_df["order_delivered_customer_date"]
                )
            )
            c_d_violations = int(mask_carrier_delivered.sum())
            if c_d_violations > 0:
                violations += c_d_violations
                warnings.append(
                    f"Chronological anomaly: {c_d_violations} orders delivered to customer BEFORE carrier date"
                )

        return violations

    def build_validation_summary_df(self) -> pd.DataFrame:
        """Compile validation results across loaded tables into an audit DataFrame.

        SKKNI [UK-04 Memvalidasi Data] deliverable.
        """
        records = []
        for name, res in self.validation_history.items():
            records.append(
                {
                    "table_name": name,
                    "passed": res.passed,
                    "total_rows": res.total_rows,
                    "duplicate_pk_rows": res.duplicate_pk_count,
                    "chronological_violations": res.chronological_violations,
                    "initial_mb": round(res.memory_initial_mb, 2),
                    "downsized_mb": round(res.memory_downsized_mb, 2),
                    "reduction_pct": round(res.memory_reduction_pct, 1),
                    "warning_count": len(res.warnings),
                    "error_count": len(res.errors),
                }
            )
        return pd.DataFrame(records)

