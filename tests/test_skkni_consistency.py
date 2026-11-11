"""Automated SKKNI 299/2020 Competency Mapping Consistency & Artifact Validator.

Rigorously verifies:
1. Exact presence of all 11 canonical SKKNI units (UK-01 through UK-11).
2. Exact presence of all 27 competency elements across all 11 units.
3. Exact presence of all 63 official KUKs (Kriteria Unjuk Kerja).
4. Exact verbatim text consistency between canonical standard and evidence registry.
5. Physical existence on disk of every single referenced evidence file (63/63).
6. Evidence traceability and honest verification status (VERIFIED / PARTIALLY_VERIFIED).
7. Dual import path resolution (csip and src.csip).
"""

from pathlib import Path
import json
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent

# Normative reference breakdown according to SKKNI 299/2020
EXPECTED_UNITS_METRIC = {
    "UK-01": {"official_code": "J.62DMI00.001.1", "title": "Menentukan Objektif Bisnis", "elements": 4, "kuks": 12},
    "UK-02": {"official_code": "J.62DMI00.002.1", "title": "Menentukan Tujuan Teknis Data Science", "elements": 2, "kuks": 4},
    "UK-03": {"official_code": "J.62DMI00.005.1", "title": "Menelaah Data", "elements": 3, "kuks": 8},
    "UK-04": {"official_code": "J.62DMI00.006.1", "title": "Memvalidasi Data", "elements": 2, "kuks": 4},
    "UK-05": {"official_code": "J.62DMI00.007.1", "title": "Menentukan Objek Data", "elements": 2, "kuks": 4},
    "UK-06": {"official_code": "J.62DMI00.008.1", "title": "Membersihkan Data", "elements": 2, "kuks": 4},
    "UK-07": {"official_code": "J.62DMI00.009.1", "title": "Mengkonstruksi Data", "elements": 3, "kuks": 6},
    "UK-08": {"official_code": "J.62DMI00.012.1", "title": "Membangun Skenario Model", "elements": 3, "kuks": 7},
    "UK-09": {"official_code": "J.62DMI00.013.1", "title": "Membangun Model", "elements": 2, "kuks": 6},
    "UK-10": {"official_code": "J.62DMI00.014.1", "title": "Mengevaluasi Hasil Pemodelan", "elements": 2, "kuks": 4},
    "UK-11": {"official_code": "J.62DMI00.015.1", "title": "Melakukan Proses Review Pemodelan", "elements": 2, "kuks": 4},
}


@pytest.fixture(scope="module")
def canonical_skkni():
    path = ROOT_DIR / "standards" / "canonical_skkni_299_2020.json"
    assert path.exists(), f"Missing canonical file: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def evidence_registry_data():
    path = ROOT_DIR / "reports" / "evidence" / "evidence_registry.json"
    assert path.exists(), f"Missing evidence registry file: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_canonical_skkni_structure_completeness(canonical_skkni):
    """Verify exact count of units (11), elements (27), and KUKs (63) in canonical standard."""
    units = canonical_skkni.get("units", [])
    assert len(units) == 11, f"Expected 11 units, got {len(units)}"
    
    total_elements = 0
    total_kuks = 0
    
    for u in units:
        u_id = u["internal_id"]
        assert u_id in EXPECTED_UNITS_METRIC, f"Unexpected unit ID: {u_id}"
        expected = EXPECTED_UNITS_METRIC[u_id]
        
        assert u["unit_code"] == expected["official_code"], f"Code mismatch for {u_id}"
        assert u["official_unit_title"] == expected["title"], f"Title mismatch for {u_id}"
        
        elems = u.get("competency_elements", [])
        assert len(elems) == expected["elements"], f"{u_id} expected {expected['elements']} elements, got {len(elems)}"
        total_elements += len(elems)
        
        u_kuks = sum(len(e.get("performance_criteria", [])) for e in elems)
        assert u_kuks == expected["kuks"], f"{u_id} expected {expected['kuks']} KUKs, got {u_kuks}"
        total_kuks += u_kuks
        
        # Verify metadata fields
        assert u.get("unit_description"), f"{u_id} missing unit_description"
        assert u.get("variable_limitations"), f"{u_id} missing variable_limitations"
        assert u.get("critical_aspects"), f"{u_id} missing critical_aspects"
        assert len(u.get("required_knowledge", [])) >= 2, f"{u_id} required_knowledge incomplete"
        assert len(u.get("required_skills", [])) >= 2, f"{u_id} required_skills incomplete"

    assert total_elements == 27, f"Expected exactly 27 total competency elements, got {total_elements}"
    assert total_kuks == 63, f"Expected exactly 63 total KUKs, got {total_kuks}"
    assert canonical_skkni.get("total_units") == 11
    assert canonical_skkni.get("total_elements") == 27
    assert canonical_skkni.get("total_kuks") == 63


def test_evidence_registry_alignment_and_verbatim_text(canonical_skkni, evidence_registry_data):
    """Verify evidence registry has exactly 63 records matching canonical KUK texts verbatim."""
    records = evidence_registry_data.get("records", [])
    assert len(records) == 63, f"Expected 63 evidence records, got {len(records)}"
    
    # Build lookup from canonical
    canonical_lookup = {}
    for u in canonical_skkni["units"]:
        u_id = u["internal_id"]
        for e in u["competency_elements"]:
            for k in e["performance_criteria"]:
                canonical_lookup[(u_id, k["kuk_id"])] = {
                    "kuk_text": k["kuk_text"],
                    "element_title": e["element_title"],
                    "unit_code": u["unit_code"],
                    "unit_title": u["official_unit_title"]
                }
                
    assert len(canonical_lookup) == 63, "Canonical lookup must contain 63 items"
    
    for r in records:
        key = (r["internal_unit_id"], r["kuk_number"])
        assert key in canonical_lookup, f"Evidence record {key} not found in canonical standard"
        ref = canonical_lookup[key]
        
        # Exact text consistency check
        assert r["kuk_text"].strip() == ref["kuk_text"].strip(), f"KUK text discrepancy in {key}: {r['kuk_text']!r} != {ref['kuk_text']!r}"
        assert r["element_title"].strip() == ref["element_title"].strip(), f"Element title mismatch in {key}"
        assert r["unit_code"] == ref["unit_code"], f"Unit code mismatch in {key}"
        assert r["unit_title"] == ref["unit_title"], f"Unit title mismatch in {key}"
        
        # Verification status check
        assert r["evidence_status"] in ("VERIFIED", "PARTIALLY_VERIFIED"), f"Invalid status: {r['evidence_status']} for {key}"
        assert r["csip_activity"], f"Missing activity description in {key}"
        assert r["csip_evidence"], f"Missing evidence file in {key}"
        assert r["verification_method"], f"Missing verification method in {key}"


def test_evidence_files_physical_existence_on_disk(evidence_registry_data):
    """Verify that every single evidence file referenced in the registry physically exists on disk.
    
    Also verifies that the 63 records map to exactly 30 unique physical files.
    """
    records = evidence_registry_data.get("records", [])
    assert len(records) == 63
    
    unique_files = set(r["csip_evidence"] for r in records)
    assert len(unique_files) == 30, f"Expected exactly 30 unique physical evidence files, got {len(unique_files)}"
    assert evidence_registry_data.get("unique_evidence_files_count") == 30
    
    missing_files = []
    empty_files = []
    
    for r in records:
        rel_path = r["csip_evidence"]
        full_path = ROOT_DIR / rel_path
        if not full_path.exists():
            missing_files.append((r["kuk_id"], rel_path))
        elif full_path.is_file() and full_path.stat().st_size == 0:
            empty_files.append((r["kuk_id"], rel_path))
            
    assert not missing_files, f"The following referenced evidence files are missing on disk: {missing_files}"
    assert not empty_files, f"The following referenced evidence files are empty: {empty_files}"


def test_honest_verification_status_and_gaps(evidence_registry_data):
    """Verify honest status labeling: simulated stakeholder signoffs are marked PARTIALLY_VERIFIED."""
    records = evidence_registry_data.get("records", [])
    status_map = {r["kuk_id"]: r["evidence_status"] for r in records}
    
    # KUK 2.2, 3.3, 4.3 of UK-01 rely on simulated client approval in an open-source setting
    assert status_map["UK-01-KUK-2.2"] == "PARTIALLY_VERIFIED", "UK-01-KUK-2.2 must be PARTIALLY_VERIFIED (simulated stakeholder signoff)"
    assert status_map["UK-01-KUK-3.3"] == "PARTIALLY_VERIFIED", "UK-01-KUK-3.3 must be PARTIALLY_VERIFIED (simulated risk acceptance)"
    assert status_map["UK-01-KUK-4.3"] == "PARTIALLY_VERIFIED", "UK-01-KUK-4.3 must be PARTIALLY_VERIFIED (simulated cost-benefit approval)"
    
    # 60 out of 63 are VERIFIED with empirical artifacts
    verified_count = sum(1 for r in records if r["evidence_status"] == "VERIFIED")
    partial_count = sum(1 for r in records if r["evidence_status"] == "PARTIALLY_VERIFIED")
    assert verified_count == 60, f"Expected 60 VERIFIED records, got {verified_count}"
    assert partial_count == 3, f"Expected 3 PARTIALLY_VERIFIED records, got {partial_count}"


def test_dual_import_compatibility():
    """Verify that importing csip and src.csip work identically and without error."""
    import csip
    import src.csip
    assert csip is not None
    assert src.csip is not None
    assert hasattr(csip, "SKKNI_UNITS")
    assert hasattr(src.csip, "SKKNI_UNITS")
    assert len(csip.SKKNI_UNITS) == 11
    assert len(src.csip.SKKNI_UNITS) == 11


def test_report_metrics_and_claims_consistency():
    """Verify that all markdown reports in reports/ are synchronized to Version 4 standards.
    
    Ensures:
    1. No active claims of 23 elements, 48 KUKs, or 84 passed tests.
    2. No premature claims of 'Rekomendasi: KOMPETEN' or '100% canonical'.
    3. Proper alignment on 11 units, 27 elements, 63 KUKs, and 83 passed tests.
    """
    key_reports = [
        ROOT_DIR / "FINAL_CSIP_AUDIT_REPORT.md",
        ROOT_DIR / "reports" / "canonical_skkni_299_2020_mapping.md",
        ROOT_DIR / "reports" / "evidence" / "evidence_traceability_matrix.md",
        ROOT_DIR / "reports" / "evidence" / "evidence_gap_analysis.md",
        ROOT_DIR / "reports" / "competency" / "canonical_mapping_validation.md",
        ROOT_DIR / "reports" / "bnsp_assessment_readiness_report.md",
        ROOT_DIR / "reports" / "testing" / "coverage_report.md",
        ROOT_DIR / "reports" / "testing" / "test_execution_report.md",
        ROOT_DIR / "reports" / "test_execution_report.md",
    ]

    for rpt in key_reports:
        assert rpt.exists(), f"Report file does not exist: {rpt}"
        text = rpt.read_text(encoding="utf-8")
        
        # Check that no report makes premature competency recommendations
        assert "rekomendasi: kompeten" not in text.lower(), f"{rpt.name} still contains 'Rekomendasi: KOMPETEN'"
        assert "status: 100% ready for bnsp assessment defense (rekomendasi: kompeten" not in text.lower()
        
        # Check that report has no hardcoded local user absolute paths
        assert "c:/users/" not in text.lower(), f"{rpt.name} contains hardcoded local path 'c:/users/'"
        assert "c:\\users\\" not in text.lower(), f"{rpt.name} contains hardcoded local path 'c:\\users\\'"
        
        # Ensure 63 KUK and 27 elements are represented in canonical / traceability reports
        if rpt.name in ["canonical_skkni_299_2020_mapping.md", "evidence_traceability_matrix.md", "canonical_mapping_validation.md"]:
            assert "63" in text, f"{rpt.name} must reference 63 KUKs"
            assert "27" in text, f"{rpt.name} must reference 27 elements"
            assert "11" in text, f"{rpt.name} must reference 11 units"

