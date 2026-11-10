"""Unit tests for Evidence Registry, Claim Level governance, and Failure Register.

SKKNI Compliance:
- [UK-01 Objektif Bisnis]
- [UK-10 Mengevaluasi Hasil Pemodelan]
- [UK-11 Melakukan Proses Review Pemodelan]
"""

import sys
from pathlib import Path
import pytest

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.evidence.registry import (
    EvidenceRegistry,
    DiscoveryEntry,
    HypothesisRecord,
    FailureRecord,
    ClaimLevel,
    EvidenceGrade,
    HypothesisStatus,
)


def test_evidence_registry_initialization(tmp_path):
    """Verify registry initializes with default 11 SKKNI units."""
    reg = EvidenceRegistry(registry_dir=tmp_path)
    assert len(reg.skkni_matrix) == 11

    # Check that unit 1 and 11 are present
    assert "UK-01" in reg.skkni_matrix
    assert "UK-11" in reg.skkni_matrix


def test_register_discovery_and_export(tmp_path):
    """Verify discovery pattern registration and DataFrame export."""
    reg = EvidenceRegistry(registry_dir=tmp_path)
    entry = DiscoveryEntry(
        discovery_id="DISC-01",
        title="Asymmetric Delay Penalty",
        description="Delivery delay beyond SLA drops review score 2.4x faster than early arrival gains.",
        discovered_at="2026-11-10",
        grain="order_id",
        key_metrics={"delay_slope": -0.15, "early_slope": 0.02},
        claim_level=ClaimLevel.L2_ASSOCIATIONAL.value,
        evidence_grade=EvidenceGrade.GRADE_A.value,
    )
    reg.register_discovery(entry)
    assert "DISC-01" in reg.discoveries

    df_disc = reg.export_discoveries_df()
    assert len(df_disc) == 1
    assert df_disc.iloc[0]["discovery_id"] == "DISC-01"
    assert df_disc.iloc[0]["claim_level"] == ClaimLevel.L2_ASSOCIATIONAL.value


def test_register_hypothesis_and_export(tmp_path):
    """Verify hypothesis record tracking, p-values, 95% CIs, and status."""
    reg = EvidenceRegistry(registry_dir=tmp_path)
    h_rec = HypothesisRecord(
        hypothesis_id="H1",
        statement="Freight ratio negatively correlates with review score.",
        analysis_type="OLS Regression",
        test_statistic_name="t-stat",
        test_statistic_value=-4.82,
        p_value=1.4e-6,
        p_value_adjusted=1.4e-6,
        effect_size=-0.21,
        confidence_interval_95=[-0.29, -0.13],
        status=HypothesisStatus.SUPPORTED.value,
        claim_level=ClaimLevel.L2_ASSOCIATIONAL.value,
        evidence_grade=EvidenceGrade.GRADE_A.value,
    )
    reg.register_hypothesis(h_rec)
    assert "H1" in reg.hypotheses

    df_hyp = reg.export_hypotheses_df()
    assert len(df_hyp) == 1
    assert df_hyp.iloc[0]["status"] == HypothesisStatus.SUPPORTED.value
    assert df_hyp.iloc[0]["p_value"] < 0.05


def test_record_failure_in_register(tmp_path):
    """Verify Failure Register records rejected hypotheses and model limitations."""
    reg = EvidenceRegistry(registry_dir=tmp_path)
    failure = FailureRecord(
        failure_id="FAIL-01",
        component_type="model",
        description="KNN classifier (k=5) failed to outperform naive baseline on repeat purchase PR-AUC.",
        root_cause="High dimensionality and sparse customer repeat transaction frequency.",
        impact_assessment="Cannot use KNN for production repeat purchase targeting.",
        mitigation_action="Retain KNN in Competency Lab only; deploy LightGBM with class weights for production.",
    )
    reg.record_failure(failure)
    assert len(reg.failures) == 1

    df_fail = reg.export_failures_df()
    assert len(df_fail) == 1
    assert df_fail.iloc[0]["failure_id"] == "FAIL-01"


def test_save_registry_snapshot(tmp_path):
    """Verify full registry state can be saved to JSON and contains all sections."""
    reg = EvidenceRegistry(registry_dir=tmp_path)
    snapshot_path = reg.save_registry_snapshot(filename="test_snapshot.json")
    assert snapshot_path.exists()

    with open(snapshot_path, "r", encoding="utf-8") as f:
        import json
        data = json.load(f)

    assert "skkni_matrix" in data
    assert "hypotheses" in data
    assert "discoveries" in data
    assert "failures" in data

