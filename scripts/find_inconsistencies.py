"""Search for inconsistent competency phrases in markdown files."""

from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
patterns = [
    r"60\s*VERIFIED",
    r"3\s*PARTIALLY_VERIFIED",
    r"100%\s*VERIFIED",
    r"100%\s*evidence verification",
    r"95[,.]2%",
]

matches = []
for p in root.rglob("*.md"):
    if any(part in p.parts for part in [".git", "__pycache__", ".pytest_cache"]):
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    for pat in patterns:
        m = re.findall(pat, text, re.IGNORECASE)
        if m:
            matches.append((str(p.relative_to(root)), pat, len(m)))

print(f"Total occurrences found: {len(matches)}")
for file_path, pat, count in matches:
    print(f"{file_path}: pattern '{pat}' matched {count} times")

