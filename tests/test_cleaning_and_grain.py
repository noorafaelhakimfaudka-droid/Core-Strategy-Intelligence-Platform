"""Unit tests for Grain selection, Cohort Filtering, and Right-Censoring mitigation.

SKKNI Compliance:
- [UK-05 Menentukan Objek Data]
- [UK-06 Membersihkan Data]
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import pytest

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.data.loader import load_yaml_config


def test_grain_specifications_in_config():
    """Verify that all 4 analytical grains have distinct keys and units."""
    cfg = load_yaml_config(REPO_ROOT / "config" / "data.yaml")
    grains = cfg.get("analytical_grains", {})

    assert grains["grain_1_order_level"]["key"] == "order_id"
    assert grains["grain_2_customer_cohort"]["key"] == "customer_unique_id"
    assert grains["grain_3_review_text"]["key"] == "review_id"
    assert grains["grain_4_weekly_system_state"]["key"] == "year_week"


def test_customer_unique_id_vs_customer_id_distinction():
    """Verify that customer entity logic distinguishes customer_id from customer_unique_id.

    PRD Section 5.3: customer_id is per-order session, customer_unique_id identifies repeat buyer.
    """
    # Synthetic transactions where 1 real customer makes 2 orders
    records = [
        {"customer_id": "session_A1", "customer_unique_id": "buyer_ALPHA", "order_id": "ord_101"},
        {"customer_id": "session_A2", "customer_unique_id": "buyer_ALPHA", "order_id": "ord_102"},
        {"customer_id": "session_B1", "customer_unique_id": "buyer_BETA", "order_id": "ord_103"},
    ]
    df = pd.DataFrame(records)

    # If grouped by customer_id, count is 3 (repeat rate = 0%)
    assert df["customer_id"].nunique() == 3

    # If grouped by customer_unique_id, count is 2 (repeat rate = 50%)
    assert df["customer_unique_id"].nunique() == 2

    repeat_counts = df.groupby("customer_unique_id")["order_id"].count()
    repeat_customers = repeat_counts[repeat_counts > 1]
    assert len(repeat_customers) == 1
    assert repeat_customers.index[0] == "buyer_ALPHA"


def test_right_censoring_exclusion_logic():
    """Verify that customers with first purchase inside delta_w buffer are censored out."""
    cfg = load_yaml_config(REPO_ROOT / "config" / "analysis_plan.yaml")
    delta_w_days = cfg["observation_windows"]["primary_window_days"]
    assert delta_w_days == 90

    t_max = datetime(2018, 10, 17)
    cutoff_date = t_max - timedelta(days=delta_w_days)

    sample_cohort = pd.DataFrame({
        "customer_unique_id": ["cust_old_1", "cust_old_2", "cust_censored_3"],
        "first_purchase_date": [
            datetime(2017, 5, 10),
            datetime(2018, 1, 15),
            datetime(2018, 9, 20),  # After cutoff date (inside 90-day censoring buffer!)
        ]
    })

    # Apply right-censoring exclusion rule
    valid_evaluation_cohort = sample_cohort[
        sample_cohort["first_purchase_date"] <= cutoff_date
    ]

    assert len(valid_evaluation_cohort) == 2
    assert "cust_censored_3" not in valid_evaluation_cohort["customer_unique_id"].values
