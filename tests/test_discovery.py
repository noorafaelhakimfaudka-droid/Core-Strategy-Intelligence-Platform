"""Unit tests for Behavioral Discovery Engine and Unsupervised Clustering.

SKKNI Compliance:
- [UK-03 Menelaah Data]
- [UK-08 Membangun Skenario Model]
- [UK-09 Membangun Model]
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.discovery.clusterer import BehavioralClusterer
from csip.evidence.registry import EvidenceRegistry


def test_clusterer_initialization():
    """Verify clusterer initializes with default features and parameters."""
    clusterer = BehavioralClusterer()
    assert len(clusterer.features) == 5
    assert "freight_ratio" in clusterer.features
    assert "total_order_value" in clusterer.features
    assert clusterer.k_range == [3, 4, 5, 6, 7]


def test_clusterer_fit_synthetic():
    """Verify clustering pipeline runs on synthetic data and returns valid profiles."""
    np.random.seed(42)
    n = 500
    df_syn = pd.DataFrame({
        "total_order_value": np.random.uniform(20, 500, size=n),
        "freight_ratio": np.random.uniform(0.05, 0.50, size=n),
        "delivery_lead_time_days": np.random.uniform(2, 30, size=n),
        "item_count": np.random.randint(1, 5, size=n),
        "payment_installments_max": np.random.randint(1, 10, size=n),
        "repeat_purchase_flag": np.random.choice([0, 1], size=n, p=[0.97, 0.03]),
        "negative_review_flag": np.random.choice([0, 1], size=n, p=[0.85, 0.15]),
    })

    clusterer = BehavioralClusterer(k_range=[3, 4], random_state=42)
    res = clusterer.fit_evaluate(df_syn, sample_size_eval=200)

    assert "evaluation_results" in res
    assert "profiles" in res
    assert "clustered_df" in res

    eval_res = res["evaluation_results"]
    assert eval_res["selected_k"] in [3, 4]
    assert len(res["profiles"]) == eval_res["selected_k"]

    # Verify cluster_id and PCA coordinates added
    clustered_df = res["clustered_df"]
    assert "cluster_id" in clustered_df.columns
    assert "pca_1" in clustered_df.columns
    assert "pca_2" in clustered_df.columns
    assert "is_anomaly" in clustered_df.columns


def test_discovery_registry_entries():
    """Verify empirical discovery catalogue entries are tracked in EvidenceRegistry."""
    registry = EvidenceRegistry(registry_dir=REPO_ROOT / "artifacts" / "reports")
    # If snapshot exists, load it
    snapshot_path = REPO_ROOT / "artifacts" / "reports" / "evidence_registry_snapshot.json"
    if snapshot_path.exists():
        import json
        with open(snapshot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        discoveries = data.get("discoveries", {})
        assert "DISC-01" in discoveries
        assert "DISC-02" in discoveries
        assert "DISC-03" in discoveries
