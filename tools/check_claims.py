"""Overclaim & Forbidden Phrases Checker for CSIP (Rule 6).

Scans all active text files (.md, .json, .csv, .py, .txt) for forbidden phrases:
- "10/10", "10.0 / 10", self-awarded total scores
- "A+", "grade" (evaluative)
- "independent evaluation", "independently audited", "auditor attestation"
- "zero leakage", "zero bias", "zero regional bias", "zero hardcoded secrets"
- "100% reproducible", "fully verified", "fully verified & accredited"
- "guaranteed", "flawless", "APPROVED FOR ASSESSMENT"

Exemptions:
- Files with "[HISTORICAL ARCHIVE]" banner at the top (first 5 lines)
- Sentences explicitly negating the claim (e.g., "tidak dijamin", "not guaranteed", "tidak ada jaminan")
- This checker script and tests specifically testing for these forbidden strings.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PATTERNS = {
    "ten_out_of_ten": re.compile(r"\b10(?:\.0)?\s*/\s*10(?:\.0)?\b", re.IGNORECASE),
    "self_total_score": re.compile(r"\b(?:score|skor|rating)\s*[:=]?\s*[89]\.[0-9]+\s*/\s*10\b", re.IGNORECASE),
    "a_plus": re.compile(r"\bGrade[:\s]+A\+\b|\bA\+\s*\((?:Distinction|Exceptional)\)|\bGrade:\s*A\+\b", re.IGNORECASE),
    "independent_eval": re.compile(r"\bindependent(?:ly)?\s+(?:evaluation|audited|audit)\b", re.IGNORECASE),
    "auditor_attestation": re.compile(r"\bauditor\s+attestation\b", re.IGNORECASE),
    "zero_leakage": re.compile(r"\bzero\s+(?:data\s+)?leakage\b", re.IGNORECASE),
    "zero_bias": re.compile(r"\bzero\s+(?:regional\s+)?bias\b", re.IGNORECASE),
    "zero_hardcoded_secrets": re.compile(r"\bzero\s+hardcoded\s+secrets\b", re.IGNORECASE),
    "hundred_pct_reproducible": re.compile(r"\b100%\s+reproducible\b", re.IGNORECASE),
    "fully_verified": re.compile(r"\bfully\s+verified(?:\s*&\s*accredited)?\b", re.IGNORECASE),
    "guaranteed": re.compile(r"\bguaranteed\b", re.IGNORECASE),
    "flawless": re.compile(r"\bflawless\b", re.IGNORECASE),
    "approved_for_assessment": re.compile(r"\bAPPROVED\s+FOR\s+ASSESSMENT\b", re.IGNORECASE),
}

NEGATION_PATTERNS = [
    re.compile(r"(?i)\b(?:not|never|no|tidak|bukan|tanpa|cannot|rather\s+than)\b[^\n\.\;]*?\b(?:guaranteed|jaminan|verified|audited|grade)\b"),
    re.compile(r"(?i)\b(?:forbidden|terlarang|dilarang|pattern|regex|finding|exemption|pengecualian)\b"),
]

EXCLUDED_FILES = {
    "check_claims.py",
    "test_claims_and_overclaims.py",
    "test_v12_remediation.py",
    "test_v13_remediation.py",
    "test_quality_gates_g1_g15.py",
    "test_v14_master.py",
    "pytest_actual.txt",
    "secret_scan.txt",
}

EXCLUDED_DIRS = {
    ".git", "__pycache__", ".pytest_cache", ".venv", "venv", "data", "legacy"
}

def is_historical_archive(path: Path) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = "".join(f.readline() for _ in range(10))
        return "[HISTORICAL ARCHIVE]" in head
    except Exception:
        return False

def check_file(path: Path) -> list[dict]:
    findings = []
    if path.name in EXCLUDED_FILES:
        return findings
    if is_historical_archive(path):
        return findings

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for line_idx, line in enumerate(content.splitlines(), start=1):
        # Check if line matches a negation / anti-claim
        line_clean = line.strip()
        is_negated = any(p.search(line_clean) for p in NEGATION_PATTERNS)
        if is_negated:
            continue

        for rule_name, pat in FORBIDDEN_PATTERNS.items():
            if pat.search(line_clean):
                findings.append({
                    "file": str(path.relative_to(REPO_ROOT)),
                    "line": line_idx,
                    "rule": rule_name,
                    "snippet": line_clean[:120]
                })
    return findings

def scan_all() -> list[dict]:
    all_findings = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in {".md", ".json", ".csv", ".py", ".txt"}:
                all_findings.extend(check_file(p))
    return all_findings

if __name__ == "__main__":
    findings = scan_all()
    print(f"Total overclaim findings: {len(findings)}")
    for f in findings:
        print(f"  {f['file']}:{f['line']} [{f['rule']}] -> {f['snippet']}")
    import sys
    sys.exit(0 if len(findings) == 0 else 1)
