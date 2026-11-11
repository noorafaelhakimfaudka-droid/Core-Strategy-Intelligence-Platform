"""Execute Supervised ML & Competency Lab Experiments (B0 - B3).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]
- [UK-09 Membangun Model]
- [UK-10 Mengevaluasi Hasil Pemodelan]
"""

import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.models.trainer import ModelExperimentTrainer
from csip.evidence.registry import EvidenceRegistry


def main():
    print("Starting Supervised ML & Competency Lab Training...")
    trainer = ModelExperimentTrainer(
        order_level_path=REPO_ROOT / "data" / "processed" / "order_level_clustered.parquet",
        customer_cohort_path=REPO_ROOT / "data" / "processed" / "customer_cohort.parquet",
        artifacts_dir=REPO_ROOT / "artifacts" / "models",
        reports_dir=REPO_ROOT / "artifacts" / "reports",
        random_state=42,
    )
    leaderboard_df = trainer.run_all_experiments()

    print("\n--- ML Leaderboard Summary (Test Split Negative Review Risk) ---")
    test_reviews = leaderboard_df[
        (leaderboard_df["target_name"] == "negative_review_flag") &
        (leaderboard_df["split_name"] == "test")
    ].sort_values(by="pr_auc", ascending=False)
    print(test_reviews[["model_name", "pr_auc", "roc_auc", "f1_score", "brier_score"]])

    # Generate Model Comparison Chart
    fig_dir = REPO_ROOT / "artifacts" / "reports" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
    bars = ax.barh(
        test_reviews["model_name"],
        test_reviews["pr_auc"],
        color="#2b5c8f",
        edgecolor="black",
        alpha=0.85,
    )

    ax.set_title("Baseline Ladder B0 - B3: PR-AUC on Locked Temporal Test Set", fontsize=13, fontweight="bold")
    ax.set_xlabel("PR-AUC (Precision-Recall Area Under Curve)", fontsize=11)
    ax.set_xlim(0.0, max(test_reviews["pr_auc"]) * 1.25)
    ax.grid(axis="x", linestyle=":", alpha=0.6)
    ax.invert_yaxis()

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.01, bar.get_y() + bar.get_height() / 2, f"{w:.4f}", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart_path = fig_dir / "ml_model_comparison_curves.png"
    plt.savefig(chart_path)
    plt.close()
    print(f"Comparison chart saved: {chart_path}")

    # Update Evidence Registry SKKNI UK-09 status to VERIFIED
    registry = EvidenceRegistry(registry_dir=REPO_ROOT / "artifacts" / "reports")
    registry.update_skkni_status("UK-08", "VERIFIED")
    registry.update_skkni_status("UK-09", "VERIFIED")
    snapshot_path = registry.save_registry_snapshot()
    print(f"Evidence Registry updated: {snapshot_path}")


if __name__ == "__main__":
    main()

