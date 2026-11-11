"""
Tests for Data Contracts & Schema Validation Engine.
Verifies contract validation on clean, invalid, and anomalous inputs.
"""

import pytest
import pandas as pd
import numpy as np
from csip.data.contracts import (
    DataContract,
    CleanOrderLevelContract,
    CustomerCohortContract,
    WeeklySystemStateContract,
    ValidationReport
)


def test_empty_dataframe_contract():
    df_empty = pd.DataFrame()
    report = CleanOrderLevelContract.validate(df_empty)
    assert not report.is_valid
    assert len(report.fatal_errors) > 0
    assert "Dataset is empty" in report.fatal_errors[0]


def test_missing_required_column_contract():
    df_missing = pd.DataFrame({
        "order_id": ["order_1", "order_2"],
        "customer_id": ["cust_1", "cust_2"]
        # Missing total_payment_value, negative_review_flag, etc.
    })
    report = CleanOrderLevelContract.validate(df_missing)
    assert not report.is_valid
    assert any("Missing required columns" in err for err in report.fatal_errors)


def test_clean_order_level_contract_on_real_data():
    df = pd.read_parquet("data/processed/order_level.parquet")
    report = CleanOrderLevelContract.validate(df)
    assert report.is_valid, f"Contract validation failed: {report.fatal_errors}"
    assert report.total_rows == 96470
    assert report.metrics["duplicate_rows"] == 0


def test_customer_cohort_contract_on_real_data():
    df = pd.read_parquet("data/processed/customer_cohort.parquet")
    report = CustomerCohortContract.validate(df)
    assert report.is_valid, f"Contract validation failed: {report.fatal_errors}"
    assert report.total_rows == 75318


def test_weekly_system_state_contract_on_real_data():
    df = pd.read_parquet("data/processed/weekly_system_state.parquet")
    report = WeeklySystemStateContract.validate(df)
    assert report.is_valid, f"Contract validation failed: {report.fatal_errors}"
    assert report.total_rows == 87

