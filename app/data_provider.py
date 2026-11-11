"""CSIP Streamlit Data Provider Layer.

Single Source of Truth for Dashboard Data:
Strictly reads pre-computed and audited artifacts from artifacts/ (json, csv, parquet).
No hardcoded metrics, no fabricated figures.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
REPORTS_DIR = ARTIFACTS_DIR / "reports"
MODELS_DIR = ARTIFACTS_DIR / "models"
METADATA_DIR = ARTIFACTS_DIR / "metadata"


def _read_json_safe(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def get_model_explainability() -> Dict[str, Any]:
    """Loads SHAP attribution and calibration metrics from model_explainability.json."""
    return _read_json_safe(REPORTS_DIR / "model_explainability.json")


@st.cache_data
def get_ml_leaderboard() -> pd.DataFrame:
    """Loads audited ML model leaderboard."""
    csv_path = REPORTS_DIR / "ml_leaderboard.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    json_path = REPORTS_DIR / "ml_leaderboard.json"
    if json_path.exists():
        data = _read_json_safe(json_path)
        return pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame()
    return pd.DataFrame()


@st.cache_data
def get_clustering_evaluation() -> Dict[str, Any]:
    """Loads behavioral clustering evaluation and personas."""
    return _read_json_safe(REPORTS_DIR / "clustering_evaluation.json")


@st.cache_data
def get_hypothesis_evaluation() -> Dict[str, Any]:
    """Loads statistical hypothesis test results (H1-H6) with FDR adjustments."""
    return _read_json_safe(REPORTS_DIR / "hypothesis_evaluation.json")


@st.cache_data
def get_scenario_simulation_results() -> Dict[str, Any]:
    """Loads policy intervention scenarios and counterfactual simulation results."""
    return _read_json_safe(REPORTS_DIR / "scenario_simulation_results.json")


@st.cache_data
def get_world_model_evaluation() -> Dict[str, Any]:
    """Loads system dynamics transition matrix and Markov chain evaluation."""
    return _read_json_safe(REPORTS_DIR / "world_model_evaluation.json")


@st.cache_data
def get_raw_data_profile() -> Dict[str, Any]:
    """Loads raw dataset audit profile and lineage."""
    return _read_json_safe(REPORTS_DIR / "raw_data_profile.json")


@st.cache_data
def get_data_lineage() -> Dict[str, Any]:
    """Loads data lineage graph metadata."""
    return _read_json_safe(METADATA_DIR / "DATA_LINEAGE.json")


@st.cache_data
def get_model_sidecars() -> Dict[str, Dict[str, Any]]:
    """Loads all model sidecar metadata files."""
    sidecars = {}
    if MODELS_DIR.exists():
        for f in MODELS_DIR.glob("*.json"):
            sidecars[f.stem] = _read_json_safe(f)
    return sidecars

