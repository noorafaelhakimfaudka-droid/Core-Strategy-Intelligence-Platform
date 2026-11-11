import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_FILES = {
    "AUDIT/SHA256SUMS.txt",
    "AUDIT/HASH_VERIFICATION_REPORT.json",
    "AUDIT/HASH_VERIFICATION_REPORT.md",
    "RELEASE_SHA256_MANIFEST.txt",
    "SHA256SUMS_FINAL.txt",
    "SHA256SUMS_V16.txt",
    "SHA256SUMS.txt",
    "reports/final/final_documentation_validation_report.json",
    "reports/final/FINAL_DOCUMENTATION_VALIDATION_REPORT.md",
    "reports/quality/DOCUMENTATION_CONSISTENCY_REPORT.md",
    "reports/final/FINAL_QUALITY_GATES_REPORT.md",
}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
}

def is_excluded(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    if normalized in EXCLUDED_FILES:
        return True
    parts = normalized.split("/")
    for p in parts:
        if p in EXCLUDED_DIRS or p.endswith(".pyc"):
            return True
    return False

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest():
    print(f"Scanning repository root: {ROOT}")
    file_hashes = {}
    
    for p in sorted(ROOT.rglob("*")):
        if p.is_file():
            rel_path = str(p.relative_to(ROOT)).replace("\\", "/")
            if not is_excluded(rel_path):
                sha = compute_sha256(p)
                file_hashes[rel_path] = sha

    print(f"Computed SHA-256 for {len(file_hashes)} physical files.")

    # 1. Write AUDIT/SHA256SUMS.txt, SHA256SUMS_FINAL.txt, and SHA256SUMS_V16.txt
    sums_file = ROOT / "AUDIT" / "SHA256SUMS.txt"
    sums_file_final = ROOT / "SHA256SUMS_FINAL.txt"
    sums_file_v16 = ROOT / "SHA256SUMS_V16.txt"
    sums_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(sums_file, "w", encoding="utf-8") as f:
        for rel_path, sha in file_hashes.items():
            f.write(f"{sha}  {rel_path}\n")
    print(f"Saved {sums_file}")

    with open(sums_file_final, "w", encoding="utf-8") as f:
        for rel_path, sha in file_hashes.items():
            f.write(f"{sha}  {rel_path}\n")
    print(f"Saved {sums_file_final}")

    with open(sums_file_v16, "w", encoding="utf-8") as f:
        for rel_path, sha in file_hashes.items():
            f.write(f"{sha}  {rel_path}\n")
    print(f"Saved {sums_file_v16}")

    # 2. Write AUDIT/HASH_VERIFICATION_REPORT.json
    report_json = ROOT / "AUDIT" / "HASH_VERIFICATION_REPORT.json"
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "release_version": "1.0.0",
        "total_files": len(file_hashes),
        "excluded_files": sorted(list(EXCLUDED_FILES)),
        "files": file_hashes
    }
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {report_json}")

    # 3. Write AUDIT/HASH_VERIFICATION_REPORT.md
    report_md = ROOT / "AUDIT" / "HASH_VERIFICATION_REPORT.md"
    md_content = f"""# CSIP FINAL 1.0.0 SHA-256 Release Hash Verification Report
## Release Integrity & Cryptographic Checksum Audit — Version 1.0.0

**Generated At**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Release Version**: 1.0.0  
**Algorithm**: SHA-256 (Bitwise Cryptographic Hash)  
**Total Tracked Files**: {len(file_hashes)}  
**Manifest Files**: `AUDIT/SHA256SUMS.txt` and `SHA256SUMS_FINAL.txt`  

---

### 1. Integrity Verification Policy

To prevent circular hash corruption, self-referential files are explicitly excluded from the checksum manifest:
- `AUDIT/SHA256SUMS.txt`
- `AUDIT/HASH_VERIFICATION_REPORT.json`
- `AUDIT/HASH_VERIFICATION_REPORT.md`
- `RELEASE_SHA256_MANIFEST.txt`

All cache files (`__pycache__`, `.pytest_cache`, `.pyc`) and version control files (`.git`) are also excluded.

### 2. Verification Procedure

To independently verify the bitwise integrity of this release in any terminal:
```bash
# In Linux / macOS / Git Bash:
sha256sum -c AUDIT/SHA256SUMS.txt

# Or using Python verification script:
python scripts/generate_sha256sums.py --verify
```

Expected result: Every single file must report `OK` with zero mismatches, zero missing files, and zero duplicate paths.

---

### 3. File Inventory Summary by Directory

| Directory | File Count |
| :--- | :---: |
"""
    # Group by top-level folder
    dir_counts = {}
    for rel_path in file_hashes:
        top = rel_path.split("/")[0] if "/" in rel_path else "(root)"
        dir_counts[top] = dir_counts.get(top, 0) + 1

    for d, cnt in sorted(dir_counts.items()):
        md_content += f"| `{d}` | {cnt} |\n"

    md_content += f"| **TOTAL** | **{len(file_hashes)}** |\n"

    report_md.write_text(md_content, encoding="utf-8")
    print(f"Saved {report_md}")

def verify_manifest():
    sums_file = ROOT / "AUDIT" / "SHA256SUMS.txt"
    assert sums_file.exists(), f"Manifest missing: {sums_file}"

    lines = sums_file.read_text(encoding="utf-8").splitlines()
    mismatches = []
    missing = []
    verified = 0

    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split("  ", 1)
        if len(parts) != 2:
            continue
        expected_sha, rel_path = parts
        fp = ROOT / rel_path
        if not fp.exists():
            missing.append(rel_path)
            continue
        actual_sha = compute_sha256(fp)
        if actual_sha != expected_sha:
            mismatches.append((rel_path, actual_sha, expected_sha))
        else:
            verified += 1

    print(f"Verified {verified} files.")
    if missing:
        print(f"MISSING files ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
    if mismatches:
        print(f"MISMATCHED files ({len(mismatches)}):")
        for rel_path, act, exp in mismatches:
            print(f"  - {rel_path}: actual {act} != expected {exp}")

    if not missing and not mismatches:
        print("ALL FILES VERIFIED 100% BITWISE IDENTICAL!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(verify_manifest())
    else:
        generate_manifest()

