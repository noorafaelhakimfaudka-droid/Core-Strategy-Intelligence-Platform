"""Credential & Secret Pattern Scanner for CSIP.

Scans the repository for common secret patterns (API keys, private keys,
passwords, bearer tokens, AWS/GCP tokens) across text files.
Outputs measured findings to reports/security/secret_scan.txt.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP)?\s*PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "aws_secret_key": re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"][A-Za-z0-9/+=]{40}['\"]"),
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}\b"),
    "bearer_token": re.compile(r"(?i)bearer\s+[A-Za-z0-9\-_\.]{32,}"),
    "generic_api_key": re.compile(r"(?i)(?:api_key|apikey|secret_key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"),
    "hardcoded_password": re.compile(r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
}

EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", ".idea", ".vscode"}
EXCLUDED_EXTENSIONS = {
    ".joblib", ".pt", ".parquet", ".png", ".jpg", ".jpeg", ".ico",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".zip", ".tar", ".gz",
    ".npy", ".npz", ".pickle", ".pkl"
}

def scan_repository() -> tuple[list[dict], dict]:
    findings = []
    scanned_files = 0
    scanned_bytes = 0
    scanned_extensions: dict[str, int] = {}

    for root, dirs, files in os.walk(REPO_ROOT):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for fname in files:
            p = Path(root) / fname
            suffix = p.suffix.lower()
            if suffix in EXCLUDED_EXTENSIONS:
                continue

            # Don't scan the output file itself
            if fname == "secret_scan.txt":
                continue

            try:
                st = p.stat()
                scanned_bytes += st.st_size
                scanned_files += 1
                scanned_extensions[suffix or "(no ext)"] = scanned_extensions.get(suffix or "(no ext)", 0) + 1

                content = p.read_text(encoding="utf-8", errors="ignore")
                for line_idx, line in enumerate(content.splitlines(), start=1):
                    # Skip common false positives (e.g., placeholder in documentation)
                    if any(dummy in line.lower() for dummy in ["your_api_key", "your_secret", "example", "<api_key>", "dummy"]):
                        continue
                    for pat_name, pat in SECRET_PATTERNS.items():
                        if pat.search(line):
                            findings.append({
                                "file": str(p.relative_to(REPO_ROOT)),
                                "line": line_idx,
                                "pattern": pat_name,
                                "snippet": line.strip()[:100]
                            })
            except Exception:
                continue

    summary = {
        "scanned_files": scanned_files,
        "scanned_bytes": scanned_bytes,
        "scanned_extensions": scanned_extensions,
        "patterns_applied": list(SECRET_PATTERNS.keys())
    }
    return findings, summary

def main() -> int:
    findings, summary = scan_repository()
    out_dir = REPO_ROOT / "reports" / "security"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "secret_scan.txt"

    lines = [
        "================================================================================",
        "CSIP CREDENTIAL & SECRET SCAN REPORT",
        "================================================================================",
        f"Scan Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Repository Root: . (Workspace Root)",
        f"Total Files Scanned: {summary['scanned_files']:,}",
        f"Total Bytes Analyzed: {summary['scanned_bytes']:,} bytes ({summary['scanned_bytes'] / (1024*1024):.2f} MB)",
        f"Detection Patterns Applied: {len(summary['patterns_applied'])} ({', '.join(summary['patterns_applied'])})",
        "",
        "--- Scanned File Types Distribution ---",
    ]
    for ext, count in sorted(summary["scanned_extensions"].items(), key=lambda x: -x[1]):
        lines.append(f"  {ext:15s}: {count:4d} files")

    lines.extend([
        "",
        "--- Findings Summary ---",
        f"Total Potential Credential Findings: {len(findings)}",
    ])

    if findings:
        lines.append("")
        lines.append("Detected Items:")
        for f in findings:
            lines.append(f"  - [{f['pattern']}] {f['file']}:{f['line']} -> {f['snippet']}")
    else:
        lines.append("")
        lines.append("No hardcoded credentials, active API keys, or private key blocks detected.")

    lines.extend([
        "",
        "--- Examination Scope & Limitations ---",
        "1. Inclusions: All text files (.py, .md, .json, .csv, .yaml, .yml, .toml, .ini, .txt, .sh, .html, .css).",
        "2. Exclusions: Binary artifacts (.joblib, .pt, .parquet), compiled caches (__pycache__, .pytest_cache), and git metadata.",
        "3. Verification: Pattern-based heuristic scan; does not substitute external runtime secret management.",
        "================================================================================",
    ])

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Scan complete. Analyzed {summary['scanned_files']} files ({summary['scanned_bytes']:,} bytes). Findings: {len(findings)}.")
    print(f"Report written to: {out_file.relative_to(REPO_ROOT)}")
    return 0 if len(findings) == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

