"""Verify or obtain raw Olist e-commerce CSV files for full pipeline reproduction.

The clean distribution archive (<100 MB) excludes ``data/raw/*.csv`` (120+ MB)
while retaining processed Parquet datasets and trained model artifacts.
Run this script to check which raw Olist CSV files are present in ``data/raw/``
and optionally download them via Kaggle CLI if configured.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def check_raw_files() -> tuple[list[str], list[str]]:
    present, missing = [], []
    for fname in EXPECTED_FILES:
        p = RAW_DIR / fname
        if p.exists() and p.stat().st_size > 0:
            present.append(fname)
        else:
            missing.append(fname)
    return present, missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or fetch raw Olist CSV files.")
    parser.add_argument("--download", action="store_true", help="Attempt download via Kaggle CLI.")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    present, missing = check_raw_files()

    print(f"Raw directory: {RAW_DIR}")
    print(f"Present: {len(present)}/{len(EXPECTED_FILES)}")
    for fname in present:
        p = RAW_DIR / fname
        print(f"  [OK] {fname} ({p.stat().st_size / 1048576:.2f} MB) sha256={sha256_file(p)[:12]}...")

    if missing:
        print(f"Missing ({len(missing)}):")
        for fname in missing:
            print(f"  [MISSING] {fname}")

        if args.download:
            print("\nAttempting download via Kaggle CLI (olistbr/brazilian-ecommerce)...")
            cmd = [
                "kaggle", "datasets", "download",
                "-d", "olistbr/brazilian-ecommerce",
                "-p", str(RAW_DIR), "--unzip",
            ]
            res = subprocess.run(cmd, check=False)
            if res.returncode != 0:
                print(
                    "\nKaggle CLI download failed. Ensure `kaggle` is installed and "
                    "~/.kaggle/kaggle.json is configured, or download manually from:\n"
                    "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
                )
                return 1
            _, still_missing = check_raw_files()
            return 0 if not still_missing else 1
        return 1

    print("\nAll expected raw Olist CSV files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

