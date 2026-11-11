"""Artifact parity tests verifying end-to-end deliverables for CSIP (Milestone 12 - Gate G11).

SKKNI Compliance:
- [UK-11 Mengembangkan Solusi]: Verifikasi ketersediaan dan integritas seluruh artefak, model, laporan, dan dashboard.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest


def test_processed_datasets_parity():
    """Verify all 4 core analytical grains and enriched datasets exist with non-zero size."""
    expected_files = [
        "data/processed/order_level.parquet",
        "data/processed/order_level_clustered.parquet",
        "data/processed/customer_cohort.parquet",
        "data/processed/review_corpus.parquet",
        "data/processed/weekly_system_state.parquet",
    ]
    for rel_path in expected_files:
        p = Path(rel_path)
        assert p.exists(), f"Missing processed dataset: {rel_path}"
        assert p.stat().st_size > 1000, f"File too small: {rel_path}"


def test_trained_models_parity():
    """Verify all trained classical, deep learning, and world model checkpoints exist."""
    expected_models = [
        "artifacts/models/clustering_pipeline.joblib",
        "artifacts/models/best_early_warning_review_lightgbm.joblib",
        "artifacts/models/best_negative_review_lightgbm.joblib",
        "artifacts/models/best_repeat_purchase_lightgbm.joblib",
        "artifacts/models/best_repeat_purchase_post_delivery_lightgbm.joblib",
        "artifacts/models/best_delivery_delay_lightgbm.joblib",
        "artifacts/models/tabular_mlp_negative_review.pt",
        "artifacts/models/text_bilstm_review_sentiment.pt",
        "artifacts/models/world_model_state_transition.joblib",
    ]
    for rel_path in expected_models:
        p = Path(rel_path)
        assert p.exists(), f"Missing trained model artifact: {rel_path}"
        assert p.stat().st_size > 500, f"Model file too small: {rel_path}"


def test_precomputed_reports_parity():
    """Verify all precomputed JSON reports exist and contain valid structures."""
    expected_reports = [
        "artifacts/reports/clustering_evaluation.json",
        "artifacts/reports/hypothesis_evaluation.json",
        "artifacts/reports/ml_leaderboard.json",
        "artifacts/reports/model_explainability.json",
        "artifacts/reports/world_model_evaluation.json",
        "artifacts/reports/scenario_simulation_results.json",
        "artifacts/reports/evidence_registry_snapshot.json",
    ]
    for rel_path in expected_reports:
        p = Path(rel_path)
        assert p.exists(), f"Missing JSON report: {rel_path}"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) > 0, f"Empty JSON report: {rel_path}"


def test_figures_parity():
    """Verify all 9 high-resolution diagnostic figures exist."""
    expected_figures = [
        "artifacts/reports/figures/eda_delay_vs_satisfaction.png",
        "artifacts/reports/figures/eda_weekly_order_trend.png",
        "artifacts/reports/figures/clustering_pca_clusters.png",
        "artifacts/reports/figures/hypothesis_forest_plot.png",
        "artifacts/reports/figures/ml_model_comparison_curves.png",
        "artifacts/reports/figures/shap_summary_plot.png",
        "artifacts/reports/figures/calibration_curves.png",
        "artifacts/reports/figures/world_model_historical_replay.png",
        "artifacts/reports/figures/scenario_simulations.png",
    ]
    for rel_path in expected_figures:
        p = Path(rel_path)
        assert p.exists(), f"Missing visualization figure: {rel_path}"
        assert p.stat().st_size > 5000, f"Figure file suspiciously small: {rel_path}"


def test_written_reports_parity():
    """Verify all 7 comprehensive markdown research reports exist."""
    expected_md = [
        "reports/data_quality_report.md",
        "reports/discovery_report.md",
        "reports/hypothesis_report.md",
        "reports/model_evaluation_and_review_report.md",
        "reports/scenario_simulation_report.md",
        "reports/evidence_and_failure_register.md",
        "reports/research_traceability_matrix.md",
    ]
    for rel_path in expected_md:
        p = Path(rel_path)
        assert p.exists(), f"Missing markdown report: {rel_path}"
        assert p.stat().st_size > 1000, f"Markdown report too short: {rel_path}"


def test_notebooks_suite_parity():
    """Verify complete suite of 14 Jupyter Notebooks (01 to 14) exists."""
    for i in range(1, 15):
        pattern = f"notebooks/{i:02d}_*.ipynb"
        matches = list(Path("notebooks").glob(f"{i:02d}_*.ipynb"))
        assert len(matches) == 1, f"Missing or duplicate notebook for module {i:02d}: {matches}"


def test_streamlit_pages_parity():
    """Verify Streamlit app entrypoint and all 9 pages exist."""
    assert Path("app/streamlit_app.py").exists()
    for i in range(1, 10):
        matches = list(Path("app/pages").glob(f"{i}_*.py"))
        assert len(matches) == 1, f"Missing Streamlit page {i}: {matches}"

