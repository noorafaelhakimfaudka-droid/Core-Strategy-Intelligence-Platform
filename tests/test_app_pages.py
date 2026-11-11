"""Tests for Dashboard Pages using streamlit.testing.v1.AppTest (Phase 8).

Validates:
1. Every page in app/pages/ renders without uncaught exceptions.
2. Metrics displayed in the dashboard match the source artifact files (no hardcoding).
3. Explicit methodological limitation badge ('RETROSPEKTIF (Pasca-Delivery)') is visible on the review risk page.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

from app.data_provider import get_model_explainability

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO_ROOT / "app" / "pages"


@pytest.mark.parametrize(
    "page_name",
    [
        "1_Executive_Overview.py",
        "2_Data_Observatory.py",
        "3_Behavioral_Discovery_Lab.py",
        "4_Hypothesis_Laboratory.py",
        "5_Predictive_Intelligence.py",
        "6_World_Model.py",
        "7_Alternative_World_Simulator.py",
        "8_Decision_Studio.py",
        "9_Evidence_Registry_Review.py",
    ],
)
def test_every_page_loads(page_name: str) -> None:
    """Verifies that all 9 dashboard pages execute cleanly without exceptions."""
    page_path = PAGES_DIR / page_name
    assert page_path.exists(), f"Page file {page_name} does not exist"

    at = AppTest.from_file(str(page_path), default_timeout=25)
    at.run(timeout=25)

    if at.exception:
        pytest.fail(f"Page {page_name} raised uncaught exception: {at.exception[0]}")


def test_app_numbers_match_artifacts() -> None:
    """Verifies that Page 5 metrics correspond directly to artifacts/reports/model_explainability.json."""
    page_path = PAGES_DIR / "5_Predictive_Intelligence.py"
    at = AppTest.from_file(str(page_path), default_timeout=25)
    at.run(timeout=25)

    assert not at.exception, f"Page 5 failed with exception: {at.exception}"

    # Load ground truth artifact
    explainability = get_model_explainability()
    assert "calibration" in explainability
    cal_info = explainability["calibration"]
    brier_imp = cal_info.get("brier_improvement_pct", 0.0)

    # Check that the markdown or content displays the actual improvement percentage
    # Search in markdown elements
    page_text = " ".join([m.value for m in at.markdown])
    expected_brier_str = f"-{brier_imp:.2f}%"
    assert expected_brier_str in page_text, f"Expected {expected_brier_str} in page text"


def test_limitations_visible_on_predictive_page() -> None:
    """Verifies that the explicit 'RETROSPEKTIF (Pasca-Delivery)' warning is rendered."""
    page_path = PAGES_DIR / "5_Predictive_Intelligence.py"
    at = AppTest.from_file(str(page_path), default_timeout=25)
    at.run(timeout=25)

    assert not at.exception
    warning_texts = [w.value for w in at.warning]
    assert len(warning_texts) > 0, "Expected at least one st.warning banner on Page 5"
    full_warning_content = " ".join(warning_texts)
    assert "RETROSPEKTIF" in full_warning_content
    assert "Pasca-Delivery" in full_warning_content
    assert "CHECKOUT_RISK_FEASIBILITY.md" in full_warning_content

