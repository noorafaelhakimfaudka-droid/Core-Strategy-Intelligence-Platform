"""CSIP Release Packaging Utility.

Packages clean distribution zip csip_v1.1.0.zip excluding transient cache files.
"""

from __future__ import annotations

import os
from pathlib import Path
import zipfile

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    ".mypy_cache",
    ".ruff_cache",
    "csip.egg-info",
    "raw",
}

EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".zip",
    ".tmp",
    ".log",
}

EXCLUDED_FILENAMES = {
    "PROMPT_BUKU_PANDUAN_LENGKAP.txt",
    "PROMPT_PRESENTASI_CSIP_MEGA.md",
    "PROMPT_EKSPANSI_BUKU_100HAL.md",
    "csip_v1.0.0.zip",
    "csip_v1.1.0.zip",
}


def should_exclude(rel_path: Path) -> bool:
    if rel_path.name in EXCLUDED_FILENAMES:
        return True
    if rel_path.name.startswith("PROMPT_"):
        return True
    for part in rel_path.parts:
        if part in EXCLUDED_DIRS:
            return True
    if rel_path.suffix.lower() in EXCLUDED_EXTENSIONS:
        return True
    return False


def build_release_zip(output_name: str = "csip_v1.1.0.zip") -> Path:
    out_path = REPO_ROOT / output_name
    if out_path.exists():
        out_path.unlink()

    print(f"Packaging {output_name} from {REPO_ROOT}...")
    file_count = 0
    total_bytes = 0

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk(REPO_ROOT):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for f in files:
                full_path = Path(root) / f
                rel_path = full_path.relative_to(REPO_ROOT)
                if should_exclude(rel_path):
                    continue

                zf.write(full_path, arcname=str(rel_path))
                file_count += 1
                total_bytes += full_path.stat().st_size

    archive_size = out_path.stat().st_size
    print(f"Packaged {file_count} files ({total_bytes:,} raw bytes) into {output_name} ({archive_size:,} bytes).")
    return out_path


if __name__ == "__main__":
    build_release_zip()

