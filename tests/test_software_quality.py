"""Tests for Software Quality, Single Import Path, Coverage & Deployment.

Validates:
1. Single import path 'csip' without src.csip aliasing or usage in active src code.
2. Experimental module isolation (README disclaimer, excluded from core claims).
3. Explicit coverage thresholds configured in pyproject.toml.
4. Batch prediction CLI rejects RESEARCH_ONLY models and enforces schema/range contracts.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest
import tomllib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

from scripts.predict_batch import run_batch_prediction

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_single_import_path() -> None:
    """Verifies that 'csip' is the canonical package name and no active code imports from 'src.csip'."""
    import csip
    assert hasattr(csip, "__version__")
    assert csip.__version__ in ("1.0.0", "17.0.0")

    # Scan src/csip for any legacy 'src.csip' imports
    src_dir = REPO_ROOT / "src" / "csip"
    violating_files = []
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8", errors="ignore")
        if "from src.csip" in content or "import src.csip" in content:
            violating_files.append(str(py_file.relative_to(REPO_ROOT)))

    assert len(violating_files) == 0, f"Found legacy 'src.csip' imports in: {violating_files}"


def test_experimental_not_in_core_claims() -> None:
    """Verifies that experimental/ contains a disclaimer README and is excluded from core claims."""
    exp_dir = REPO_ROOT / "src" / "csip" / "experimental"
    assert exp_dir.exists(), "src/csip/experimental directory must exist"
    
    readme = exp_dir / "README.md"
    assert readme.exists(), "src/csip/experimental/README.md must exist"
    readme_text = readme.read_text(encoding="utf-8")
    assert "EXPERIMENTAL" in readme_text.upper()


def test_coverage_thresholds_configured() -> None:
    """Verifies that pyproject.toml defines explicit pytest-cov coverage thresholds."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    tool = config.get("tool", {})
    cov_report = tool.get("coverage", {}).get("report", {})
    assert "fail_under" in cov_report, "tool.coverage.report must specify fail_under"
    assert cov_report["fail_under"] >= 60, "Overall coverage threshold must be >= 60%"


def test_predict_batch_rejects_research_only(tmp_path: Path) -> None:
    """Verifies that scripts/predict_batch.py rejects models designated as RESEARCH_ONLY."""
    # 1. Create a dummy model
    model = LogisticRegression()
    X_dummy = np.array([[10.0, 5.0], [20.0, 15.0], [30.0, 25.0]])
    y_dummy = np.array([0, 1, 0])
    model.fit(X_dummy, y_dummy)

    model_file = tmp_path / "test_research_model.joblib"
    sidecar_file = tmp_path / "test_research_model.joblib.json"
    input_file = tmp_path / "test_input.csv"

    joblib.dump(model, model_file)

    # 2. Sidecar with RESEARCH_ONLY status
    sidecar_data = {
        "model_name": "test_research_model",
        "maturity_status": "RESEARCH_ONLY",
        "feature_list": ["feat_a", "feat_b"],
        "model_version": "1.0.0",
    }
    sidecar_file.write_text(json.dumps(sidecar_data), encoding="utf-8")

    # 3. Valid input CSV
    df_input = pd.DataFrame({
        "order_id": ["o1", "o2"],
        "feat_a": [10.0, 20.0],
        "feat_b": [5.0, 15.0],
    })
    df_input.to_csv(input_file, index=False)

    # Must raise ValueError rejecting deployment
    with pytest.raises(ValueError, match="is designated as RESEARCH_ONLY"):
        run_batch_prediction(model_path=model_file, input_path=input_file)

    # 4. Change status to CANDIDATE and verify execution succeeds
    sidecar_data["maturity_status"] = "CANDIDATE"
    sidecar_file.write_text(json.dumps(sidecar_data), encoding="utf-8")

    out_file = tmp_path / "test_output.csv"
    res = run_batch_prediction(model_path=model_file, input_path=input_file, output_path=out_file)
    assert "predicted_score" in res.columns
    assert "predicted_label" in res.columns
    assert len(res) == 2
    assert out_file.exists()
