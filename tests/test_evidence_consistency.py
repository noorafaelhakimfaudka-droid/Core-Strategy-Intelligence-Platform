"""Automated Regression Suite for Competency Evidence Consistency (CSIP V15).

Verifies Critical Finding F01:
1. CANONICAL_EVIDENCE_REGISTRY.csv exists with exactly 63 rows.
2. Canonical counts strictly match:
   - 35 VERIFIED
   - 13 CANDIDATE_DEMONSTRATION_REQUIRED
   - 12 ARTIFACT_ONLY
   - 3 EXTERNAL_CONFIRMATION_REQUIRED
   - 0 PARTIALLY_VERIFIED
   - 0 MISSING
3. All referenced evidence files physically exist on disk and match SHA-256.
4. MASTER_COMPETENCY_MATRIX.csv, EVIDENCE_REGISTRY.csv, and evidence_registry.json match.
5. No contradictory "60 VERIFIED" or "100% VERIFIED" claims in active documentation.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_COUNTS = {
    "VERIFIED": 35,
    "CANDIDATE_DEMONSTRATION_REQUIRED": 13,
    "ARTIFACT_ONLY": 12,
    "EXTERNAL_CONFIRMATION_REQUIRED": 3,
    "PARTIALLY_VERIFIED": 0,
    "MISSING": 0,
}


def test_canonical_registry_existence_and_row_count():
    """Verify CANONICAL_EVIDENCE_REGISTRY.csv exists with exactly 63 KUK rows."""
    canon_path = REPO_ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
    assert canon_path.exists(), "CANONICAL_EVIDENCE_REGISTRY.csv does not exist"

    with open(canon_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 63, f"Expected 63 KUK rows, got {len(rows)}"

    # Check status counts
    counts = {k: 0 for k in CANONICAL_COUNTS}
    for r in rows:
        st = r["verification_result"]
        assert st in counts, f"Invalid verification_result: {st}"
        counts[st] += 1

    assert counts == CANONICAL_COUNTS, f"Status count mismatch: {counts} != {CANONICAL_COUNTS}"


def test_all_referenced_evidence_files_exist_and_sha256_match():
    """Verify that every evidence file declared in CANONICAL_EVIDENCE_REGISTRY.csv physically exists and matches SHA-256."""
    canon_path = REPO_ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
    with open(canon_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        rel_loc = r["exact_location"]
        full_path = REPO_ROOT / rel_loc
        assert full_path.exists(), f"Evidence file missing on disk: {rel_loc} (for KUK {r['kuk_number']})"
        assert full_path.stat().st_size > 0, f"Evidence file is empty: {rel_loc}"

        actual_sha = hashlib.sha256(full_path.read_bytes()).hexdigest()
        declared_sha = r["sha256"]
        assert actual_sha == declared_sha, (
            f"SHA-256 mismatch for {rel_loc}: actual {actual_sha} != declared {declared_sha}"
        )


def test_cross_registry_synchronization():
    """Verify that MASTER_COMPETENCY_MATRIX.csv, EVIDENCE_REGISTRY.csv, and JSON match canonical counts."""
    matrix_path = REPO_ROOT / "competency" / "MASTER_COMPETENCY_MATRIX.csv"
    reg_path = REPO_ROOT / "competency" / "EVIDENCE_REGISTRY.csv"
    json_path = REPO_ROOT / "reports" / "evidence" / "evidence_registry.json"

    assert matrix_path.exists()
    assert reg_path.exists()
    assert json_path.exists()

    with open(matrix_path, "r", encoding="utf-8") as f:
        matrix_rows = list(csv.DictReader(f))
    with open(reg_path, "r", encoding="utf-8") as f:
        reg_rows = list(csv.DictReader(f))
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    assert len(matrix_rows) == 63
    assert len(reg_rows) == 63
    assert len(json_data["records"]) == 63

    matrix_counts = {k: 0 for k in CANONICAL_COUNTS}
    for r in matrix_rows:
        matrix_counts[r["verification_result"]] += 1
    assert matrix_counts == CANONICAL_COUNTS, f"Matrix counts mismatch: {matrix_counts}"

    assert json_data["canonical_status_breakdown"] == CANONICAL_COUNTS


def test_no_contradictory_evidence_claims_in_active_docs():
    """Verify that active documentation files contain NO contradictory claims (e.g. '60 VERIFIED')."""
    active_docs = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "FINAL_CSIP_AUDIT_REPORT.md",
        REPO_ROOT / "CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md",
        REPO_ROOT / "CHANGELOG_V14.md",
        REPO_ROOT / "competency" / "ASSESSMENT_READINESS_REPORT.md",
        REPO_ROOT / "competency" / "EVIDENCE_RECONCILIATION_REPORT.md",
        REPO_ROOT / "competency" / "EVIDENCE_STATUS_DEFINITIONS.md",
        REPO_ROOT / "AUDIT" / "INDEPENDENT_FINAL_AUDIT.md",
    ]

    forbidden_patterns = [
        r"60\s*VERIFIED",
        r"60\s*KUK\s*\(95[,.]2%\)",
        r"100%\s*evidence verification",
        r"11\s*units\s*as\s*100%\s*VERIFIED",
    ]

    violations = []
    for doc in active_docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for pat in forbidden_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                violations.append(f"{doc.name} matched '{pat}': {matches}")

    assert not violations, f"Contradictory claims found:\n" + "\n".join(violations)

