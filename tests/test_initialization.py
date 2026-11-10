"""Unit tests for configuration integrity and SKKNI traceability initialization.

SKKNI Compliance:
- [UK-01 Objektif Bisnis]
- [UK-02 Tujuan Teknis DS]
- [UK-05 Menentukan Objek Data]
"""

import sys
from pathlib import Path
import pytest
import yaml

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip import SKKNI_UNITS, CLAIM_LEVELS, EVIDENCE_GRADES


def test_skkni_11_units_complete():
    """Verify all 11 SKKNI BNSP units are registered."""
    assert len(SKKNI_UNITS) == 11
    expected_codes = [f"UK-{i:02d}" for i in range(1, 12)]
    for code in expected_codes:
        assert code in SKKNI_UNITS


def test_claim_levels_complete():
    """Verify all 4 claim levels L0-L3 are present."""
    assert "L0" in CLAIM_LEVELS
    assert "L1" in CLAIM_LEVELS
    assert "L2" in CLAIM_LEVELS
    assert "L3" in CLAIM_LEVELS


def test_evidence_grades_complete():
    """Verify grades A through D exist."""
    assert "Grade A" in EVIDENCE_GRADES
    assert "Grade B" in EVIDENCE_GRADES
    assert "Grade C" in EVIDENCE_GRADES
    assert "Grade D" in EVIDENCE_GRADES


def test_config_data_yaml_structure():
    """Verify config/data.yaml has all 9 Olist tables and required keys."""
    cfg_path = REPO_ROOT / "config" / "data.yaml"
    assert cfg_path.exists(), "config/data.yaml is missing"

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "tables" in cfg
    tables = cfg["tables"]
    expected_tables = [
        "orders",
        "order_items",
        "order_payments",
        "order_reviews",
        "customers",
        "sellers",
        "products",
        "geolocation",
        "category_translation",
    ]
    for tbl in expected_tables:
        assert tbl in tables, f"Missing table configuration for '{tbl}'"
        assert "primary_key" in tables[tbl]

    # Verify 4 analytical grains are specified
    assert "analytical_grains" in cfg
    grains = cfg["analytical_grains"]
    assert "grain_1_order_level" in grains
    assert "grain_2_customer_cohort" in grains
    assert "grain_3_review_text" in grains
    assert "grain_4_weekly_system_state" in grains


def test_config_analysis_plan_yaml_structure():
    """Verify config/analysis_plan.yaml contains hypotheses H1-H6 and temporal splits."""
    cfg_path = REPO_ROOT / "config" / "analysis_plan.yaml"
    assert cfg_path.exists(), "config/analysis_plan.yaml is missing"

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "observation_windows" in cfg
    assert cfg["observation_windows"]["primary_window_days"] == 90
    assert "temporal_split" in cfg
    splits = cfg["temporal_split"]["splits"]
    assert "train" in splits
    assert "validation" in splits
    assert "test" in splits
    assert "censoring_buffer" in splits

    assert "hypotheses" in cfg
    hyps = cfg["hypotheses"]
    for i in range(1, 7):
        h_id = f"H{i}"
        assert h_id in hyps, f"Hypothesis {h_id} missing in analysis_plan.yaml"
        assert "statement" in hyps[h_id]
        assert "target_claim_level" in hyps[h_id]
        assert "falsification_condition" in hyps[h_id]


def test_config_features_yaml_structure():
    """Verify config/features.yaml contains the 5 feature groups and anti-leakage rules."""
    cfg_path = REPO_ROOT / "config" / "features.yaml"
    assert cfg_path.exists()

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "feature_groups" in cfg
    fg = cfg["feature_groups"]
    assert "economic" in fg
    assert "fulfillment_experience" in fg
    assert "as_of_behavioral" in fg
    assert "interaction_nonlinear" in fg
    assert "text_and_deep_learning" in fg

    assert "anti_leakage_rules" in cfg
    al = cfg["anti_leakage_rules"]
    assert "checkout_stage_restricted_features" in al
    assert "first_order_repeat_prediction_rule" in al


def test_config_models_yaml_structure():
    """Verify config/models.yaml defines Baseline Ladder B0-B4 and targets."""
    cfg_path = REPO_ROOT / "config" / "models.yaml"
    assert cfg_path.exists()

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "targets" in cfg
    assert "baseline_ladder" in cfg
    bl = cfg["baseline_ladder"]
    assert "B0_naive" in bl
    assert "B1_statistical" in bl
    assert "B2_classical_benchmarks" in bl
    assert "B3_ensemble_trees" in bl
    assert "B4_neural_and_deep_learning" in bl


def test_config_scenarios_yaml_structure():
    """Verify config/scenarios.yaml defines Alternative World simulation scenarios and guardrails."""
    cfg_path = REPO_ROOT / "config" / "scenarios.yaml"
    assert cfg_path.exists()

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "world_model" in cfg
    assert "simulation_scenarios" in cfg
    assert "extrapolation_guardrails" in cfg
    scenarios = cfg["simulation_scenarios"]
    assert "baseline_world" in scenarios
    assert "freight_subsidy_moderate" in scenarios
    assert "sla_improvement_carrier" in scenarios

