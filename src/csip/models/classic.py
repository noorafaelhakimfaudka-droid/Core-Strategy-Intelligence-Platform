"""CSIP Classical Machine Learning Models & Baseline Ladder (B0 - B3).

SKKNI Compliance:
- [UK-08 Membangun Skenario Model]: Baseline Ladder B0-B3 dan parameter model.
- [UK-09 Membangun Model]: Pelatihan model LogReg, Ridge, Decision Tree, KNN, Naive Bayes, Random Forest, LightGBM.

All models adhere to 8 GB RAM laptop limits (bounded depths, n_jobs limits, vectorized scalers).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

logger = logging.getLogger(__name__)


class MajorityClassClassifier(BaseEstimator, ClassifierMixin):
    """B0 Naive Baseline: Predicts majority class probability from training data."""

    def __init__(self) -> None:
        self.majority_class_: int = 0
        self.class_prob_: float = 0.5
        self.classes_: np.ndarray = np.array([0, 1])

    def fit(self, X: Any, y: np.ndarray) -> MajorityClassClassifier:
        y_arr = np.asarray(y)
        counts = np.bincount(y_arr)
        self.majority_class_ = int(np.argmax(counts))
        self.class_prob_ = float(counts[1] / len(y_arr)) if len(counts) > 1 else 0.0
        return self

    def predict(self, X: Any) -> np.ndarray:
        n = len(X)
        return np.full(n, self.majority_class_, dtype=np.int8)

    def predict_proba(self, X: Any) -> np.ndarray:
        n = len(X)
        p1 = self.class_prob_
        p0 = 1.0 - p1
        probs = np.tile([p0, p1], (n, 1))
        return probs


class DelayHeuristicClassifier(BaseEstimator, ClassifierMixin):
    """B0 Heuristic Baseline: If is_late == 1 -> negative_review = 1, else 0."""

    def __init__(self, delay_feature_idx: int = 0) -> None:
        self.delay_feature_idx = delay_feature_idx
        self.classes_: np.ndarray = np.array([0, 1])

    def fit(self, X: Any, y: Optional[Any] = None) -> DelayHeuristicClassifier:
        return self

    def predict(self, X: Any) -> np.ndarray:
        X_arr = np.asarray(X)
        is_late = (X_arr[:, self.delay_feature_idx] > 0).astype(np.int8)
        return is_late

    def predict_proba(self, X: Any) -> np.ndarray:
        preds = self.predict(X)
        probs = np.zeros((len(preds), 2))
        probs[preds == 1, 1] = 0.85
        probs[preds == 1, 0] = 0.15
        probs[preds == 0, 0] = 0.85
        probs[preds == 0, 1] = 0.15
        return probs


class MeanRegressor(BaseEstimator, RegressorMixin):
    """B0 Naive Regressor: Always predicts the training set mean."""

    def __init__(self) -> None:
        self.mean_val_: float = 0.0

    def fit(self, X: Any, y: np.ndarray) -> MeanRegressor:
        self.mean_val_ = float(np.mean(y))
        return self

    def predict(self, X: Any) -> np.ndarray:
        return np.full(len(X), self.mean_val_, dtype=np.float32)


def get_model_pipeline(
    model_key: str,
    problem_type: str = "classification",
    random_state: int = 42,
) -> Pipeline:
    """Factory creating scikit-learn compatible pipelines for Baseline Ladder B0 - B3."""
    if problem_type == "classification":
        if model_key == "B0_naive_majority":
            return Pipeline([("clf", MajorityClassClassifier())])
        elif model_key == "B0_naive_heuristic":
            return Pipeline([("clf", DelayHeuristicClassifier(delay_feature_idx=0))])
        elif model_key == "B1_logistic":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=random_state,
                )),
            ])
        elif model_key == "B2_decision_tree":
            return Pipeline([
                ("clf", DecisionTreeClassifier(
                    max_depth=6,
                    min_samples_split=50,
                    random_state=random_state,
                )),
            ])
        elif model_key == "B2_knn":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("clf", KNeighborsClassifier(
                    n_neighbors=15,
                    weights="distance",
                    metric="euclidean",
                )),
            ])
        elif model_key == "B2_naive_bayes":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("clf", GaussianNB()),
            ])
        elif model_key == "B3_random_forest":
            return Pipeline([
                ("clf", RandomForestClassifier(
                    n_estimators=100,
                    max_depth=8,
                    min_samples_leaf=20,
                    class_weight="balanced",
                    n_jobs=-1,
                    random_state=random_state,
                )),
            ])
        elif model_key == "B3_lightgbm":
            return Pipeline([
                ("clf", LGBMClassifier(
                    n_estimators=150,
                    max_depth=6,
                    num_leaves=31,
                    learning_rate=0.05,
                    class_weight="balanced",
                    n_jobs=-1,
                    random_state=random_state,
                    verbose=-1,
                )),
            ])
        else:
            raise ValueError(f"Unknown classification model_key: {model_key}")

    elif problem_type == "regression":
        if model_key == "B0_naive_mean":
            return Pipeline([("reg", MeanRegressor())])
        elif model_key == "B1_ridge":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("reg", Ridge(alpha=1.0, random_state=random_state)),
            ])
        elif model_key == "B2_decision_tree":
            return Pipeline([
                ("reg", DecisionTreeRegressor(
                    max_depth=6,
                    min_samples_split=50,
                    random_state=random_state,
                )),
            ])
        elif model_key == "B2_knn":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("reg", KNeighborsRegressor(
                    n_neighbors=15,
                    weights="distance",
                )),
            ])
        elif model_key == "B3_random_forest":
            return Pipeline([
                ("reg", RandomForestRegressor(
                    n_estimators=100,
                    max_depth=8,
                    min_samples_leaf=20,
                    n_jobs=-1,
                    random_state=random_state,
                )),
            ])
        elif model_key == "B3_lightgbm":
            return Pipeline([
                ("reg", LGBMRegressor(
                    n_estimators=150,
                    max_depth=6,
                    num_leaves=31,
                    learning_rate=0.05,
                    n_jobs=-1,
                    random_state=random_state,
                    verbose=-1,
                )),
            ])
        else:
            raise ValueError(f"Unknown regression model_key: {model_key}")

    else:
        raise ValueError(f"Unknown problem_type: {problem_type}")

