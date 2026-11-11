import os
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent

patterns = [
    r"60\s*VERIFIED",
    r"3\s*PARTIALLY_VERIFIED",
    r"60\s*KUK\s*\(95[,.]2%\)",
    r"100%\s*evidence verification",
    r"11\s*units\s*as\s*100%\s*VERIFIED",
]

matches = []

for ext in [".md", ".json", ".csv", ".py", ".txt"]:
    for f in root.rglob(f"*{ext}"):
        # Ignore pycache, .git, and test_evidence_consistency itself
        if ".git" in f.parts or "__pycache__" in f.parts or ".pytest_cache" in f.parts:
            continue
        if f.name in ["test_evidence_consistency.py", "scan_remaining_discrepancies.py", "reconcile_evidence_system.py", "find_inconsistencies.py"]:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in patterns:
            found = re.findall(pat, text, re.IGNORECASE)
            if found:
                matches.append((str(f.relative_to(root)), pat, len(found)))

print(f"Total matching files found: {len(matches)}")
for rel_path, pat, count in matches:
    print(f"- {rel_path} [{pat}] count={count}")

