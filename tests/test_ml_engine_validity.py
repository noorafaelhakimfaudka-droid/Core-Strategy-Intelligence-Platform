"""Unit tests for Universal CSV ML Engine methodological validity."""

import numpy as np
import pandas as pd

from csip.models.ml_engine import simulate_and_narrate, train_fluent_ml_pipeline


def _make_schema(cols: list[str], target: str) -> dict:
    schema = {c: {"phrase": c, "unit": "", "verb_up": "naik", "verb_down": "turun"} for c in cols}
    schema[target] = {"phrase": target, "unit": "", "verb_up": "naik", "verb_down": "turun"}
    return schema


def test_binary_classification_routing_and_cv():
    rng = np.random.default_rng(42)
    n = 120
    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    prob = 1.0 / (1.0 + np.exp(-(2.0 * x1 - 1.5 * x2)))
    y = (prob > 0.5).astype(int)
    df = pd.DataFrame({"feat_a": x1, "feat_b": x2, "target_bin": y})

    pipe = train_fluent_ml_pipeline(
        df_sample=df,
        target_col="target_bin",
        candidate_cols=["feat_a", "feat_b"],
        schema_info=_make_schema(["feat_a", "feat_b"], "target_bin"),
        audit_info={},
    )
    assert pipe["task_type"] == "classification"
    assert pipe["evaluation_mode"] == "HOLDOUT_SPLIT"
    assert pipe["cv_metrics"]["cv_folds"] >= 2
    assert "pr_auc" in pipe["classification_metrics"]
    assert "roc_auc" in pipe["classification_metrics"]
    assert "brier_score" in pipe["classification_metrics"]

    sim = simulate_and_narrate(pipe, {"feat_a": 2.0}, "target_bin", _make_schema(["feat_a", "feat_b"], "target_bin"))
    assert 0.0 <= sim["pred_val"] <= 1.0
    assert len(sim["prediction_interval_90"]) == 2
    assert sim["prediction_interval_90"][0] <= sim["prediction_interval_90"][1]
    assert sim["tipping_point_method"] == "VISUAL_EXPLORATORY_HEURISTIC_GAUSSIAN_SIGMA2"


def test_regression_routing_cv_and_uncertainty():
    rng = np.random.default_rng(7)
    n = 100
    x1 = rng.uniform(0, 10, n)
    x2 = rng.uniform(0, 5, n)
    y = 3.0 * x1 - 1.5 * x2 + rng.normal(0, 0.5, n)
    df = pd.DataFrame({"feat_a": x1, "feat_b": x2, "target_reg": y})

    pipe = train_fluent_ml_pipeline(
        df_sample=df,
        target_col="target_reg",
        candidate_cols=["feat_a", "feat_b"],
        schema_info=_make_schema(["feat_a", "feat_b"], "target_reg"),
        audit_info={},
    )
    assert pipe["task_type"] == "regression"
    assert pipe["evaluation_mode"] == "HOLDOUT_SPLIT"
    assert pipe["cv_metrics"]["cv_folds"] >= 2
    assert "cv_mae_mean" in pipe["cv_metrics"]
    assert "cv_r2_mean" in pipe["cv_metrics"]

    sim = simulate_and_narrate(pipe, {"feat_a": 8.0}, "target_reg", _make_schema(["feat_a", "feat_b"], "target_reg"))
    lo, hi = sim["prediction_interval_90"]
    assert lo <= hi
    assert sim["tipping_point_method"] == "VISUAL_EXPLORATORY_HEURISTIC_GAUSSIAN_SIGMA2"


def test_small_n_fallback_explicitly_flagged():
    df = pd.DataFrame({
        "feat_a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "feat_b": [2.0, 1.0, 4.0, 3.0, 6.0, 5.0],
        "target_reg": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
    })
    pipe = train_fluent_ml_pipeline(
        df_sample=df,
        target_col="target_reg",
        candidate_cols=["feat_a", "feat_b"],
        schema_info=_make_schema(["feat_a", "feat_b"], "target_reg"),
        audit_info={},
    )
    assert pipe["evaluation_mode"] == "IN_SAMPLE_FALLBACK_SMALL_N"
    assert pipe["cv_metrics"]["cv_folds"] == 0

