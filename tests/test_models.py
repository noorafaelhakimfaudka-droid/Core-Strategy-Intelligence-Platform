"""Unit tests for Supervised Machine Learning Pipelines & Baseline Ladder (B0 - B3).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]
- [UK-09 Membangun Model]
- [UK-10 Mengevaluasi Hasil Pemodelan]
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from csip.models.classic import (
    DelayHeuristicClassifier,
    MajorityClassClassifier,
    MeanRegressor,
    get_model_pipeline,
)
from csip.models.trainer import ModelExperimentTrainer


def test_majority_classifier_synthetic():
    """Verify B0 MajorityClassClassifier fits majority and outputs proper probabilities."""
    y = np.array([0, 0, 0, 0, 1, 0, 1, 0])
    X = np.ones((8, 2))
    clf = MajorityClassClassifier()
    clf.fit(X, y)

    assert clf.majority_class_ == 0
    assert pytest.approx(clf.class_prob_) == 2 / 8

    preds = clf.predict(X)
    assert len(preds) == 8
    assert (preds == 0).all()

    probs = clf.predict_proba(X)
    assert probs.shape == (8, 2)
    assert pytest.approx(probs[0, 1]) == 0.25


def test_delay_heuristic_classifier_rule():
    """Verify B0 DelayHeuristicClassifier flags negative review when delay > 0."""
    X = np.array([
        [-5.0, 100.0],  # Early -> 0
        [0.0, 50.0],    # On time -> 0
        [3.0, 75.0],    # Late -> 1
        [14.0, 200.0],  # Late -> 1
    ])
    clf = DelayHeuristicClassifier(delay_feature_idx=0)
    clf.fit(X)
    preds = clf.predict(X)

    assert list(preds) == [0, 0, 1, 1]


def test_mean_regressor():
    """Verify B0 MeanRegressor predicts training mean."""
    y = np.array([10.0, 20.0, 30.0])
    X = np.ones((3, 1))
    reg = MeanRegressor()
    reg.fit(X, y)

    assert reg.mean_val_ == 20.0
    preds = reg.predict(np.zeros((5, 1)))
    assert len(preds) == 5
    assert (preds == 20.0).all()


def test_pipeline_factory_instantiation():
    """Verify get_model_pipeline creates all classification and regression models."""
    clf_keys = [
        "B0_naive_majority",
        "B0_naive_heuristic",
        "B1_logistic",
        "B2_decision_tree",
        "B2_knn",
        "B2_naive_bayes",
        "B3_random_forest",
        "B3_lightgbm",
    ]
    for k in clf_keys:
        pipe = get_model_pipeline(k, problem_type="classification")
        assert pipe is not None

    reg_keys = [
        "B0_naive_mean",
        "B1_ridge",
        "B2_decision_tree",
        "B2_knn",
        "B3_random_forest",
        "B3_lightgbm",
    ]
    for k in reg_keys:
        pipe = get_model_pipeline(k, problem_type="regression")
        assert pipe is not None


def test_trainer_temporal_splits_ordering():
    """Verify get_temporal_splits partitions chronologically without row overlap."""
    trainer = ModelExperimentTrainer()
    df_syn = pd.DataFrame({
        "order_purchase_timestamp": pd.to_datetime([
            "2017-06-15",
            "2018-02-10",
            "2018-05-12",
            "2018-07-20",
        ]),
        "val": [1, 2, 3, 4],
    })

    train, val, test = trainer.get_temporal_splits(
        df_syn, train_end="2018-03-31", val_end="2018-06-30"
    )

    assert len(train) == 2  # 2017-06, 2018-02
    assert len(val) == 1    # 2018-05
    assert len(test) == 1   # 2018-07
    assert train["order_purchase_timestamp"].max() <= pd.Timestamp("2018-03-31")
    assert val["order_purchase_timestamp"].min() > pd.Timestamp("2018-03-31")
    assert test["order_purchase_timestamp"].min() > pd.Timestamp("2018-06-30")

