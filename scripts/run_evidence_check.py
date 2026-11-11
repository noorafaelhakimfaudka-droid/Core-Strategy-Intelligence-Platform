"""CSIP Automated Competency Evidence Verification Runner.

Phase 10 (b):
Executes verification procedures across all 63 SKKNI KUKs defined in
competency/CANONICAL_EVIDENCE_REGISTRY.csv and outputs reports/competency/evidence_run.json.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_evidence_verification() -> Dict[str, Any]:
    canon_file = REPO_ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
    if not canon_file.exists():
        raise FileNotFoundError(f"Missing canonical evidence registry at {canon_file}")

    with open(canon_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total_kuks = len(rows)
    verified_items: List[Dict[str, Any]] = []
    missing_files: List[str] = []
    hash_mismatches: List[str] = []

    status_counts = {}

    for r in rows:
        kuk = r["kuk_number"]
        unit_code = r["unit_code"]
        loc = r["exact_location"]
        declared_sha = r["sha256"]
        v_res = r["verification_result"]

        status_counts[v_res] = status_counts.get(v_res, 0) + 1

        p = REPO_ROOT / loc
        file_exists = p.exists()
        actual_sha = hashlib.sha256(p.read_bytes()).hexdigest() if file_exists else "MISSING"

        sha_matches = (file_exists and actual_sha == declared_sha)
        if not file_exists:
            missing_files.append(f"{unit_code} KUK {kuk}: {loc}")
        elif not sha_matches:
            hash_mismatches.append(f"{unit_code} KUK {kuk}: {loc} (actual {actual_sha} != declared {declared_sha})")

        verified_items.append({
            "unit_code": unit_code,
            "unit_title": r["unit_title"],
            "kuk_number": kuk,
            "artifact_location": loc,
            "file_exists": file_exists,
            "sha256_match": sha_matches,
            "declared_sha256": declared_sha,
            "actual_sha256": actual_sha,
            "verification_status": v_res,
            "verification_procedure": r["verification_procedure"],
            "demonstration_task": r["demonstration_task"],
        })

    report = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "total_kuks_checked": total_kuks,
        "status_distribution": status_counts,
        "files_checked": len(verified_items),
        "missing_files_count": len(missing_files),
        "hash_mismatches_count": len(hash_mismatches),
        "all_files_present": len(missing_files) == 0,
        "all_hashes_intact": len(hash_mismatches) == 0,
        "missing_files": missing_files,
        "hash_mismatches": hash_mismatches,
        "items": verified_items,
    }

    out_path = REPO_ROOT / "reports" / "competency" / "evidence_run.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Evidence verification complete. Checked {total_kuks} KUKs.")
    print(f"Status distribution: {status_counts}")
    print(f"Missing files: {len(missing_files)}, Hash mismatches: {len(hash_mismatches)}")
    print(f"Saved run report to {out_path}")
    return report


if __name__ == "__main__":
    run_evidence_verification()

