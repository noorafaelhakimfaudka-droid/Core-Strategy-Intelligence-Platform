# CSIP FINAL 1.1.0 SHA-256 Release Hash Verification Report
## Release Integrity & Cryptographic Checksum Audit — Version 1.1.0

**Generated At**: 2026-11-16 11:46:38 UTC  
**Release Version**: 1.1.0  
**Algorithm**: SHA-256 (Bitwise Cryptographic Hash)  
**Total Tracked Files**: 330  
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
| `(root)` | 26 |
| `.github` | 1 |
| `.streamlit` | 1 |
| `AUDIT` | 2 |
| `app` | 7 |
| `artifacts` | 42 |
| `competency` | 12 |
| `config` | 6 |
| `data` | 25 |
| `docs` | 25 |
| `notebooks` | 15 |
| `reports` | 39 |
| `scripts` | 22 |
| `src` | 61 |
| `standards` | 2 |
| `tests` | 40 |
| `tools` | 4 |
| **TOTAL** | **330** |
