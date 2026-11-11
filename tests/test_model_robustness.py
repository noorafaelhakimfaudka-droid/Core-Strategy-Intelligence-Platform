"""
Tests for Model Robustness & Subgroup Slice Evaluation Engine.
Verifies subgroup error analysis across geographical and order value segments.
"""

from pathlib import Path
from csip.evaluation.robustness import run_full_slice_analysis

ROOT = Path(__file__).resolve().parent.parent


def test_model_slice_analysis_execution():
    results = run_full_slice_analysis()
    assert results is not None
    assert "negative_review_model" in results
    assert "delivery_delay_model" in results
    assert results["total_holdout_orders"] > 10000


def test_negative_review_slices():
    results = run_full_slice_analysis()
    neg = results["negative_review_model"]
    assert "overall" in neg
    assert neg["overall"]["roc_auc"] >= 0.65
    assert "geographic_slices" in neg
    assert len(neg["geographic_slices"]) >= 3
    # Check top states SP, RJ, MG
    for state in ["SP", "RJ", "MG"]:
        assert state in neg["geographic_slices"]
        assert neg["geographic_slices"][state]["sample_size"] > 500


def test_delivery_delay_slices():
    results = run_full_slice_analysis()
    delay = results["delivery_delay_model"]
    assert "overall" in delay
    assert delay["overall"]["mae_days"] < 6.0
    assert "geographic_slices" in delay
    assert len(delay["geographic_slices"]) >= 3


def test_slice_analysis_reports_exist():
    json_path = ROOT / "artifacts" / "reports" / "model_slice_analysis.json"
    md_path = ROOT / "reports" / "models" / "MODEL_ROBUSTNESS_AND_SLICE_ANALYSIS.md"
    assert json_path.exists()
    assert md_path.exists()
    assert md_path.stat().st_size > 500

