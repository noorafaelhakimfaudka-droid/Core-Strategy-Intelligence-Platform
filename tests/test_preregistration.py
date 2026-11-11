"""Tests for Phase 2: Pre-Registration & Protocol Freeze."""

import hashlib
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_plan_hash_unchanged_or_amended():
    """Verify that config/analysis_plan.yaml matches its pre-registered SHA-256 hash, or has a dated amendment."""
    plan_path = REPO_ROOT / "config" / "analysis_plan.yaml"
    hash_path = REPO_ROOT / "reports" / "preregistration" / "PLAN_HASH.txt"

    assert plan_path.exists(), "config/analysis_plan.yaml missing"
    assert hash_path.exists(), "reports/preregistration/PLAN_HASH.txt missing"

    actual_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    declared_entry = hash_path.read_text(encoding="utf-8").strip()
    declared_hash = declared_entry.split()[0]

    if actual_hash != declared_hash:
        amendment_path = REPO_ROOT / "reports" / "preregistration" / "AMENDMENTS.md"
        assert amendment_path.exists(), (
            f"Pre-registered plan hash changed ({actual_hash} != {declared_hash}) "
            f"without a formal amendment document at {amendment_path.relative_to(REPO_ROOT)}."
        )

def test_analysis_plan_contains_mandatory_specifications():
    """Verify that analysis_plan.yaml contains all pre-registered specifications required by Phase 2."""
    plan_path = REPO_ROOT / "config" / "analysis_plan.yaml"
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = yaml.safe_load(f)

    # Estimands & populations
    assert "estimands_and_populations" in plan
    assert "M1_delivery_delay" in plan["estimands_and_populations"]
    assert "M2_retrospective_review_risk" in plan["estimands_and_populations"]
    assert "M3_repeat_purchase_post_delivery" in plan["estimands_and_populations"]

    # Cross-validation scheme
    cv = plan.get("cross_validation_scheme", {})
    assert cv.get("cv_type") == "Rolling-Origin Expanding-Window Temporal Cross-Validation"
    assert cv.get("n_folds", 0) >= 4
    assert cv.get("embargo_days", 0) >= 90

    # Decision rules
    for model_key, spec in plan["estimands_and_populations"].items():
        assert "decision_rule" in spec, f"Missing decision_rule in {model_key}"

    # Data exclusion and hygiene rules
    assert "data_exclusion_and_hygiene_rules" in plan
    hygiene = plan["data_exclusion_and_hygiene_rules"]
    assert "pre_delivery_repeat_exclusion" in hygiene
    assert "right_censoring_mitigation" in hygiene

