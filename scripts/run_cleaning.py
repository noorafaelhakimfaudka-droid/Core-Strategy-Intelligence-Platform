"""Execute full cleaning pipeline and print audit metrics."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.data.loader import OlistDataLoader
from csip.cleaning.cleaner import OlistDataCleaner


def main():
    loader = OlistDataLoader(
        config_path=REPO_ROOT / "config" / "data.yaml",
        raw_data_dir=REPO_ROOT / "data" / "raw",
    )
    cleaner = OlistDataCleaner(
        loader=loader,
        interim_dir=REPO_ROOT / "data" / "interim",
    )
    audit = cleaner.run_full_pipeline()
    print("\n--- Cleaning Pipeline Audit Results ---")
    for k, v in audit.items():
        print(f"  {k:15s}: {v['rows_initial']:,} -> {v['rows_cleaned']:,} ({v['dropped_pct']:.2f}% dropped)")


if __name__ == "__main__":
    main()

