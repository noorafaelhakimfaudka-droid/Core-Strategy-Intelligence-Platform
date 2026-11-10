"""Unit tests for Hypothesis Investigation Engine and Statistical Evidence Verification.

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]
- [UK-10 Mengevaluasi Hasil Pemodelan]
- [UK-11 Melakukan Proses Review Pemodelan]
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.hypotheses.runner import HypothesisTestRunner
from csip.evidence.registry import ClaimLevel, EvidenceGrade, HypothesisStatus


def test_hypothesis_runner_battery_execution():
    """Verify HypothesisTestRunner executes all 6 hypotheses on real processed data."""
    order_path = REPO_ROOT / "data" / "processed" / "order_level_clustered.parquet"
    cohort_path = REPO_ROOT / "data" / "processed" / "customer_cohort.parquet"

    if not order_path.exists() or not cohort_path.exists():
        pytest.skip("Processed datasets not yet generated.")

    runner = HypothesisTestRunner(
        order_level_path=order_path,
        customer_cohort_path=cohort_path,
        alpha=0.05,
    )
    results = runner.run_all()

    # Verify all 6 hypotheses tested
    expected_ids = ["H1", "H2", "H3", "H4", "H5", "H6"]
    for h_id in expected_ids:
        assert h_id in results, f"Missing test result for hypothesis {h_id}"
        rec = results[h_id]
        assert rec.p_value is not None
        assert rec.p_value_adjusted is not None
        assert rec.effect_size is not None
        assert rec.confidence_interval_95 is not None
        assert len(rec.confidence_interval_95) == 2
        assert rec.status in [HypothesisStatus.SUPPORTED.value, HypothesisStatus.REJECTED.value]
        assert rec.claim_level in [ClaimLevel.L1_PREDICTIVE.value, ClaimLevel.L2_ASSOCIATIONAL.value]
        assert rec.evidence_grade in [EvidenceGrade.GRADE_A.value, EvidenceGrade.GRADE_B.value]


def test_fdr_correction_adjustment():
    """Verify Benjamini-Hochberg FDR p-value adjustment property (p_adj >= p_raw)."""
    order_path = REPO_ROOT / "data" / "processed" / "order_level_clustered.parquet"
    cohort_path = REPO_ROOT / "data" / "processed" / "customer_cohort.parquet"

    if not order_path.exists() or not cohort_path.exists():
        pytest.skip("Processed datasets not yet generated.")

    runner = HypothesisTestRunner(
        order_level_path=order_path,
        customer_cohort_path=cohort_path,
    )
    results = runner.run_all()

    for rec in results.values():
        assert rec.p_value_adjusted >= rec.p_value - 1e-12, "FDR adjusted p-value must be >= raw p-value"
