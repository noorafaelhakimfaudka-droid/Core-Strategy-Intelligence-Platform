"""Run CSIP Feature Engineering and Build 4 Analytical Datasets."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.features.engineer import FeatureEngineer


def main():
    engineer = FeatureEngineer(
        interim_dir=REPO_ROOT / "data" / "interim",
        processed_dir=REPO_ROOT / "data" / "processed",
        delta_w_days=90,
    )
    datasets = engineer.build_all()

    print("\n--- Analytical Datasets Construction Summary ---")
    for name, df in datasets.items():
        mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        print(f"  {name:20s}: {len(df):,} rows x {len(df.columns)} cols ({mem_mb:.2f} MB)")


if __name__ == "__main__":
    main()
