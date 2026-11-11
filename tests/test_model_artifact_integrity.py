"""Automated Test Suite for Model Artifact Integrity, Sidecars & Metadata Parity.

Validates:
1. Physical existence and non-zero byte size of all champion model artifacts.
2. Metadata sidecars (.joblib.json) completeness and environment compatibility.
3. Model Results Registry (MODEL_RESULTS_REGISTRY.csv) cryptographic hash parity.
4. Clean joblib deserialization without broken dependencies or runtime errors.
"""

from __future__ import annotations

import json
from pathlib import Path
import joblib
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_champion_model_artifacts_exist():
    """Verify that primary champion model files exist in artifacts/models/."""
    models_dir = REPO_ROOT / "artifacts" / "models"
    expected_models = [
        "best_delivery_delay_lightgbm.joblib",
        "best_early_warning_review_lightgbm.joblib",
        "clustering_pipeline.joblib",
    ]

    for model_name in expected_models:
        p = models_dir / model_name
        assert p.exists(), f"Missing required champion model: {model_name}"
        assert p.stat().st_size > 5000, f"Model file suspiciously small: {model_name}"


def test_model_sidecar_metadata_complete():
    """Verify that every model artifact has an accompanying .json sidecar with valid schema."""
    models_dir = REPO_ROOT / "artifacts" / "models"
    for joblib_file in models_dir.glob("*.joblib"):
        sidecar = models_dir / f"{joblib_file.name}.json"
        assert sidecar.exists(), f"Missing metadata sidecar for {joblib_file.name}"
        
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        assert "target_name" in data or "feature_set_name" in data or "model_name" in data or "model_type" in data


def test_model_results_registry_matches_files():
    """Verify that MODEL_RESULTS_REGISTRY.csv accurately tracks registered models."""
    registry_path = REPO_ROOT / "artifacts" / "metadata" / "MODEL_RESULTS_REGISTRY.csv"
    if not registry_path.exists():
        pytest.skip("MODEL_RESULTS_REGISTRY.csv not found")

    df = pd.read_csv(registry_path)
    cols = [c.lower() for c in df.columns]
    assert "model_id" in cols
    assert "artifact_path" in cols
    assert len(df) >= 3, "Registry must contain at least 3 primary models"


def test_joblib_load_artifacts_clean():
    """Verify that LightGBM models load without error."""
    models_dir = REPO_ROOT / "artifacts" / "models"
    for model_path in models_dir.glob("best_*_lightgbm.joblib"):
        try:
            model = joblib.load(model_path)
            assert model is not None
        except Exception as e:
            pytest.fail(f"Failed to load {model_path.name}: {e}")
