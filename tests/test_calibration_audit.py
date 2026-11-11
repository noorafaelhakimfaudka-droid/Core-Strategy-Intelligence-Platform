"""Automated Test Suite for Model Calibration and Brier Score Verification (CSIP V14).

SKKNI Compliance:
- [UK-10 Mengevaluasi Hasil Pemodelan]: Evaluasi diagnostik kurva kalibrasi, ECE, dan Brier score.
- Modul Kompetensi 16: Model Diagnostics & Probability Calibration.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_calibration_metadata_and_brier_improvement():
    """Verify that Platt scaling significantly reduces Brier score and Expected Calibration Error (ECE)."""
    meta_path = REPO_ROOT / "artifacts" / "reports" / "model_explainability.json"
    assert meta_path.exists(), "model_explainability.json missing"

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    assert "calibration" in data, "Calibration metadata missing from model_explainability.json"
    calib = data["calibration"]

    uncal_brier = calib["uncalibrated_brier"]
    cal_brier = calib["calibrated_brier"]
    uncal_ece = calib["uncalibrated_ece"]
    cal_ece = calib["calibrated_ece"]

    # Calibrated Brier score must be strictly lower than uncalibrated Brier score
    assert cal_brier < uncal_brier, f"Calibrated Brier ({cal_brier}) not lower than uncalibrated ({uncal_brier})"

    # Calibrated Brier must beat naive baseline (~0.0985)
    assert cal_brier < 0.090, f"Calibrated Brier ({cal_brier}) must outperform naive majority baseline (0.0985)"

    # ECE must drop significantly (calibrated ECE < 0.05)
    assert cal_ece < 0.02, f"Calibrated ECE ({cal_ece}) is too high (should be < 0.02)"
    assert cal_ece < uncal_ece


def test_calibration_curve_figure_exists():
    """Verify that reliability diagram (calibration curves plot) is generated and valid."""
    fig_path = REPO_ROOT / "artifacts" / "reports" / "figures" / "calibration_curves.png"
    assert fig_path.exists(), "artifacts/reports/figures/calibration_curves.png does not exist"
    assert fig_path.stat().st_size > 5000, "calibration_curves.png is suspiciously small"


def test_shap_summary_plot_exists():
    """Verify that SHAP TreeExplainer summary plot is generated and valid."""
    fig_path = REPO_ROOT / "artifacts" / "reports" / "figures" / "shap_summary_plot.png"
    assert fig_path.exists(), "artifacts/reports/figures/shap_summary_plot.png does not exist"
    assert fig_path.stat().st_size > 5000, "shap_summary_plot.png is suspiciously small"
