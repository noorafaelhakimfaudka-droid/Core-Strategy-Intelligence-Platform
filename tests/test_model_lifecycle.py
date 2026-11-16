"""Unit tests for CSIP Model Lifecycle Manager & Champion-Challenger Promotion."""

import pytest
from pathlib import Path
from csip.models.registry import (
    ModelLifecycleManager,
    ModelRegistration,
    ModelRole,
    MaturityStatus,
)


def test_candidate_registration_and_hash(tmp_path: Path):
    model_file = tmp_path / "candidate_model.joblib"
    model_file.write_bytes(b"dummy_model_bytes_123456789")

    manager = ModelLifecycleManager(
        repo_root=tmp_path,
        promotion_log_path=tmp_path / "test_promotion_log.csv",
    )

    reg = manager.register_candidate(
        model_id="test_candidate_1",
        model_name="Test LightGBM Candidate",
        version="1.0.0",
        target_name="negative_review_flag",
        artifact_path=model_file,
        feature_list=["feat_a", "feat_b"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.3250,
        brier_score=0.0750,
    )

    assert reg.role == ModelRole.CANDIDATE
    assert len(reg.artifact_sha256) == 64
    assert reg.primary_metric_value == 0.3250


def test_promotion_safeguards_rejection(tmp_path: Path):
    manager = ModelLifecycleManager(
        repo_root=tmp_path,
        promotion_log_path=tmp_path / "test_promotion_log.csv",
    )

    # 1. Reject RESEARCH_ONLY model
    candidate_research = ModelRegistration(
        model_id="research_model",
        model_name="Research Model",
        version="1.0.0",
        role=ModelRole.CANDIDATE,
        maturity_status=MaturityStatus.RESEARCH_ONLY,
        target_name="target",
        artifact_path="dummy",
        artifact_sha256="abc",
        feature_list=["x"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.4500,
    )

    eligible, reasons = manager.evaluate_promotion(candidate_research, None)
    assert not eligible
    assert "RESEARCH_ONLY" in reasons[0]

    # 2. Reject candidate with inferior metric compared to champion
    champion = ModelRegistration(
        model_id="champ",
        model_name="Champion",
        version="1.0.0",
        role=ModelRole.CHAMPION,
        maturity_status=MaturityStatus.PRODUCTION_APPROVED,
        target_name="target",
        artifact_path="dummy",
        artifact_sha256="abc",
        feature_list=["x"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.3061,
        brier_score=0.0762,
    )

    inferior_candidate = ModelRegistration(
        model_id="inferior",
        model_name="Inferior",
        version="1.0.0",
        role=ModelRole.CANDIDATE,
        maturity_status=MaturityStatus.BENCHMARK_VALIDATED,
        target_name="target",
        artifact_path="dummy",
        artifact_sha256="abc",
        feature_list=["x"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.2900,
        brier_score=0.0800,
    )

    eligible, reasons = manager.evaluate_promotion(inferior_candidate, champion)
    assert not eligible
    assert any("did not exceed champion" in r for r in reasons)


def test_successful_promotion_and_rollback(tmp_path: Path):
    manager = ModelLifecycleManager(
        repo_root=tmp_path,
        promotion_log_path=tmp_path / "test_promotion_log.csv",
    )

    champ_v1 = ModelRegistration(
        model_id="lgbm_review",
        model_name="Negative Review LGBM",
        version="1.0.0",
        role=ModelRole.CHAMPION,
        maturity_status=MaturityStatus.PRODUCTION_APPROVED,
        target_name="negative_review_flag",
        artifact_path="artifacts/models/champ_v1.joblib",
        artifact_sha256="hash1",
        feature_list=["x"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.3061,
        brier_score=0.0762,
    )

    challenger_v2 = ModelRegistration(
        model_id="lgbm_review",
        model_name="Negative Review LGBM",
        version="1.0.0",
        role=ModelRole.CHALLENGER,
        maturity_status=MaturityStatus.BENCHMARK_VALIDATED,
        target_name="negative_review_flag",
        artifact_path="artifacts/models/champ_v2.joblib",
        artifact_sha256="hash2",
        feature_list=["x"],
        primary_metric_name="PR_AUC",
        primary_metric_value=0.3250,  # +6.1% improvement
        brier_score=0.0750,
    )

    # Promote challenger to champion
    success = manager.promote_candidate(
        candidate=challenger_v2,
        current_champion=champ_v1,
        approved_by="Lead ML Engineer",
        reason="Verified out-of-time PR-AUC improvement +6.1%",
    )
    assert success is True
    assert challenger_v2.role == ModelRole.CHAMPION
    assert champ_v1.role == ModelRole.ARCHIVED

    # Rollback champion to v1
    rollback_success = manager.rollback(
        active_model=challenger_v2,
        target_archived_model=champ_v1,
        approved_by="Model Risk Officer",
        reason="Unexpected feature drift observed in shadow deployment",
    )
    assert rollback_success is True
    assert champ_v1.role == ModelRole.CHAMPION
    assert challenger_v2.role == ModelRole.ARCHIVED

