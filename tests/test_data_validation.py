"""Unit tests for data validation, memory downsizing, and schema sanity.

SKKNI Compliance:
- [UK-03 Menelaah Data]
- [UK-04 Memvalidasi Data]
- [UK-06 Membersihkan Data]
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.data.loader import downcast_dataframe, OlistDataLoader, ValidationResult


def test_downcast_dataframe_numeric_and_categories():
    """Verify that 64-bit numerics are successfully downcast and strings become categories."""
    n_rows = 1000
    df = pd.DataFrame({
        "int_small": np.random.randint(-100, 100, size=n_rows, dtype=np.int64),
        "int_medium": np.random.randint(-50000, 50000, size=n_rows, dtype=np.int64),
        "float_val": np.random.randn(n_rows).astype(np.float64),
        "cat_str": np.random.choice(["SP", "RJ", "MG", "RS"], size=n_rows),
        "date_str": ["2018-01-01 10:00:00"] * n_rows,
    })

    df_opt, mem_init, mem_opt = downcast_dataframe(
        df,
        date_columns=["date_str"],
        categorical_columns=["cat_str"],
        max_categorical_cardinality=10,
    )

    # Assert downcasting occurred
    assert df_opt["int_small"].dtype == np.int16
    assert df_opt["int_medium"].dtype == np.int32
    assert df_opt["float_val"].dtype == np.float32
    assert str(df_opt["cat_str"].dtype) == "category"
    assert pd.api.types.is_datetime64_any_dtype(df_opt["date_str"])

    # Assert memory reduction
    assert mem_opt < mem_init
    reduction_pct = ((mem_init - mem_opt) / mem_init) * 100
    assert reduction_pct > 30.0, f"Expected >30% reduction, got {reduction_pct:.1f}%"


def test_order_timestamp_sanity_detection():
    """Verify that timestamp chronological violations are caught."""
    loader = OlistDataLoader(config_path=REPO_ROOT / "config" / "data.yaml")

    # Synthetic orders dataframe with 1 chronological violation
    orders_df = pd.DataFrame({
        "order_id": ["order_1", "order_2"],
        "customer_id": ["cust_1", "cust_2"],
        "order_status": ["delivered", "delivered"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-10", "2018-01-15"]),
        "order_delivered_customer_date": pd.to_datetime(["2018-01-12", "2018-01-10"]),  # order_2 delivered before purchase!
        "order_delivered_carrier_date": pd.to_datetime(["2018-01-11", "2018-01-11"]),
    })

    warnings = []
    violations = loader._check_order_timestamp_sanity(orders_df, warnings)
    assert violations >= 1
    assert any("delivered BEFORE" in w for w in warnings)


def test_validation_result_metrics():
    """Verify ValidationResult computes memory reduction percentage correctly."""
    res = ValidationResult(
        table_name="test_table",
        passed=True,
        total_rows=5000,
        memory_initial_mb=10.0,
        memory_downsized_mb=4.0,
    )
    assert res.passed is True
    assert pytest.approx(res.memory_reduction_pct, rel=1e-2) == 60.0


def test_real_raw_csv_files_present():
    """Verify all 9 raw Olist CSV files exist on disk in data/raw."""
    loader = OlistDataLoader(config_path=REPO_ROOT / "config" / "data.yaml")
    for tbl in loader.tables_config:
        file_path = loader.get_table_path(tbl)
        assert file_path.exists(), f"Raw CSV missing for table: {tbl} at {file_path}"


def test_real_orders_referential_integrity():
    """Verify referential integrity on real Olist data (zero orphan records)."""
    loader = OlistDataLoader(config_path=REPO_ROOT / "config" / "data.yaml")
    orders_df = loader.load_table("orders")
    customers_df = loader.load_table("customers")

    assert len(orders_df) == 99441
    assert orders_df["order_id"].nunique() == 99441  # 100% unique PK

    # Check zero orphan orders
    order_cust_ids = set(orders_df["customer_id"].dropna())
    customer_cust_ids = set(customers_df["customer_id"].dropna())
    orphan_orders = order_cust_ids - customer_cust_ids
    assert len(orphan_orders) == 0, f"Found {len(orphan_orders)} orphan orders!"


