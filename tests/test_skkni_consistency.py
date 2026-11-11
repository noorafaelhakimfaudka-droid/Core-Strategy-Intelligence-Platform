"""Automated SKKNI 299/2020 Competency Mapping Consistency & Artifact Validator.

Verifies:
1. Exact presence of all 11 canonical SKKNI units (UK-01 through UK-11).
2. Exact match of official Kemnaker codes (J.62DMI00.xxx.1) and titles.
3. Every referenced source code file, notebook, and report exists on disk.
4. Completeness of 4-dimensional evidence (Process, Result, Validation, Explanation).
5. Cross-document consistency between EvidenceRegistry and markdown matrices.
"""

from pathlib import Path
import pytest
from src.csip.evidence.registry import EvidenceRegistry

ROOT_DIR = Path(__file__).resolve().parent.parent

CANONICAL_UNITS = {
    "UK-01": {"official_code": "J.62DMI00.001.1", "title": "Menentukan Objektif Bisnis"},
    "UK-02": {"official_code": "J.62DMI00.002.1", "title": "Menentukan Tujuan Teknis Data Science"},
    "UK-03": {"official_code": "J.62DMI00.005.1", "title": "Menelaah Data"},
    "UK-04": {"official_code": "J.62DMI00.006.1", "title": "Memvalidasi Data"},
    "UK-05": {"official_code": "J.62DMI00.007.1", "title": "Menentukan Objek Data"},
    "UK-06": {"official_code": "J.62DMI00.008.1", "title": "Membersihkan Data"},
    "UK-07": {"official_code": "J.62DMI00.009.1", "title": "Mengkonstruksi Data"},
    "UK-08": {"official_code": "J.62DMI00.012.1", "title": "Membangun Skenario Model"},
    "UK-09": {"official_code": "J.62DMI00.013.1", "title": "Membangun Model"},
    "UK-10": {"official_code": "J.62DMI00.014.1", "title": "Mengevaluasi Hasil Pemodelan"},
    "UK-11": {"official_code": "J.62DMI00.015.1", "title": "Melakukan Proses Review Pemodelan"},
}


@pytest.fixture
def registry():
    return EvidenceRegistry()


def test_skkni_unit_count_and_codes(registry):
    """Verify exactly 11 canonical SKKNI units exist with correct official codes."""
    assert len(registry.skkni_matrix) == 11, f"Expected exactly 11 units, got {len(registry.skkni_matrix)}"
    for unit_id, expected in CANONICAL_UNITS.items():
        assert unit_id in registry.skkni_matrix, f"Missing unit: {unit_id}"
        item = registry.skkni_matrix[unit_id]
        assert item.unit_title == expected["title"], f"Title mismatch for {unit_id}: {item.unit_title} vs {expected['title']}"
        assert item.official_code == expected["official_code"], f"Official code mismatch for {unit_id}"
        assert item.status in ("VERIFIED", "IMPLEMENTED", "TESTED")


def test_skkni_four_dimensional_evidence_populated(registry):
    """Verify each unit has complete Process, Result, Validation, and Explanation evidence."""
    for unit_id, item in registry.skkni_matrix.items():
        assert item.evidence_process, f"{unit_id} missing evidence_process"
        assert item.evidence_result, f"{unit_id} missing evidence_result"
        assert item.evidence_validation, f"{unit_id} missing evidence_validation"
        assert item.evidence_explanation, f"{unit_id} missing evidence_explanation"
        assert item.verification_method, f"{unit_id} missing verification_method"


def test_skkni_code_locations_exist_on_disk(registry):
    """Verify all referenced code files or directories exist on disk."""
    for unit_id, item in registry.skkni_matrix.items():
        for loc in item.code_locations:
            path = ROOT_DIR / loc
            assert path.exists(), f"For {unit_id}, referenced code path does not exist: {loc}"


def test_skkni_notebook_locations_exist_on_disk(registry):
    """Verify all referenced notebooks exist on disk."""
    for unit_id, item in registry.skkni_matrix.items():
        for nb in item.notebook_locations:
            path = ROOT_DIR / nb
            assert path.exists(), f"For {unit_id}, referenced notebook does not exist: {nb}"


def test_skkni_report_artifacts_exist_on_disk(registry):
    """Verify all referenced report artifacts exist on disk."""
    for unit_id, item in registry.skkni_matrix.items():
        for rpt in item.report_artifacts:
            path = ROOT_DIR / rpt
            assert path.exists(), f"For {unit_id}, referenced report does not exist: {rpt}"


def test_skkni_cross_markdown_consistency():
    """Verify markdown matrix and canonical mapping contain all 11 unit codes and titles."""
    canonical_file = ROOT_DIR / "reports" / "canonical_skkni_299_2020_mapping.md"
    matrix_file = ROOT_DIR / "reports" / "research_traceability_matrix.md"

    assert canonical_file.exists(), "Canonical mapping markdown does not exist"
    assert matrix_file.exists(), "Traceability matrix markdown does not exist"

    canonical_text = canonical_file.read_text(encoding="utf-8")
    matrix_text = matrix_file.read_text(encoding="utf-8")

    for unit_id, expected in CANONICAL_UNITS.items():
        assert unit_id in canonical_text, f"{unit_id} missing in canonical mapping"
        assert expected["official_code"] in canonical_text, f"{expected['official_code']} missing in canonical mapping"
        assert expected["title"] in canonical_text, f"{expected['title']} missing in canonical mapping"

        assert unit_id in matrix_text, f"{unit_id} missing in traceability matrix"
        assert expected["official_code"] in matrix_text, f"{expected['official_code']} missing in traceability matrix"
        assert expected["title"] in matrix_text, f"{expected['title']} missing in traceability matrix"
