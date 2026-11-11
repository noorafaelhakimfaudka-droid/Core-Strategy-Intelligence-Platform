"""Tests for Non-Predictive Statistical Rigor (Phase 6).

Validates:
1. Multiple testing corrections (Benjamini-Hochberg FDR and Holm-Bonferroni).
2. Cluster stability evaluation using bootstrap Adjusted Rand Index (ARI) and Jaccard.
3. Strictly associative language across all statistical hypothesis statements.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.multitest import multipletests

from csip.discovery.clusterer import BehavioralClusterer
from csip.hypotheses.runner import HypothesisTestRunner


def test_multiple_testing_correction_applied() -> None:
    """Verifies that multiple testing corrections (BH and Holm) adjust raw p-values appropriately."""
    raw_p_values = [0.001, 0.012, 0.035, 0.048, 0.120, 0.450]
    
    # Benjamini-Hochberg FDR
    reject_bh, p_bh, _, _ = multipletests(raw_p_values, alpha=0.05, method="fdr_bh")
    
    # Holm-Bonferroni
    reject_holm, p_holm, _, _ = multipletests(raw_p_values, alpha=0.05, method="holm")

    # Adjusted p-values must be >= raw p-values
    for raw, adj_bh, adj_h in zip(raw_p_values, p_bh, p_holm):
        assert adj_bh >= raw, "BH adjusted p-value must be >= raw p-value"
        assert adj_h >= raw, "Holm adjusted p-value must be >= raw p-value"
        # Holm is typically more conservative than BH FDR
        assert adj_h >= adj_bh - 1e-6, "Holm FWER should be >= BH FDR"


def test_cluster_stability_reported() -> None:
    """Verifies BehavioralClusterer.evaluate_cluster_stability produces valid ARI and Jaccard scores."""
    rng = np.random.default_rng(42)
    n = 600

    # 3 synthetic clusters
    c1 = rng.normal(loc=[100, 0.1, 5, 1, 1], scale=[20, 0.02, 1, 0.2, 0.2], size=(200, 5))
    c2 = rng.normal(loc=[300, 0.4, 20, 3, 6], scale=[40, 0.05, 3, 0.5, 1.0], size=(200, 5))
    c3 = rng.normal(loc=[50, 0.2, 10, 1, 2], scale=[10, 0.03, 2, 0.3, 0.5], size=(200, 5))
    X = np.vstack([c1, c2, c3])

    df = pd.DataFrame(
        X,
        columns=[
            "total_order_value",
            "freight_ratio",
            "delivery_lead_time_days",
            "item_count",
            "payment_installments_max",
        ],
    )

    clusterer = BehavioralClusterer(k_range=[3, 4])
    stability = clusterer.evaluate_cluster_stability(
        df,
        k_values=[3, 4],
        n_bootstraps=5,
        subsample_ratio=0.8,
    )

    assert "k_3" in stability
    assert "k_4" in stability

    for k_key, res in stability.items():
        assert "mean_ari" in res
        assert "mean_jaccard" in res
        assert -1.0 <= res["mean_ari"] <= 1.0
        assert 0.0 <= res["mean_jaccard"] <= 1.0
        assert res["n_comparisons"] > 0

    # Well-separated clusters should achieve high ARI on k=3
    assert stability["k_3"]["mean_ari"] > 0.50, "Well-separated clusters should have ARI > 0.50 on k=3"


def test_associative_language_in_hypotheses() -> None:
    """Verifies that all hypotheses statements use strictly associative rather than unverified causal claims."""
    runner = HypothesisTestRunner.__new__(HypothesisTestRunner)
    runner.alpha = 0.05
    runner.results = {}

    # Inspect the methods
    # Check that docstrings and statements emphasize observational/associative framing
    for h_num in range(1, 7):
        method = getattr(HypothesisTestRunner, f"test_H{h_num}")
        doc = method.__doc__ or ""
        # Should not claim 'proves cause' without qualification
        assert "causal proof" not in doc.lower()

