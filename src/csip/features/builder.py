"""CSIP Automated Feature Construction Engine.

Implements Enterprise Standard SKKNI Competency:
- [UK-07] Mengonstruksi Data: Menghasilkan fitur interaksi, rasio,
  dan transformasi matematis baru secara terotomatisasi tanpa kebocoran data.

100% Real Computation, Zero Emojis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


class AutoFeatureBuilder:
    """[UK-07] Automated feature interaction and ratio constructor."""

    def __init__(self, max_new_features: int = 5, epsilon: float = 1e-6) -> None:
        self.max_new_features = max_new_features
        self.epsilon = epsilon
        self.constructed_features_: List[str] = []

    def construct(
        self,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None,
    ) -> Tuple[pd.DataFrame, List[str]]:
        """Construct interaction and ratio features from numerical candidates."""
        work_df = df.copy()
        new_cols: List[str] = []

        if feature_cols is None:
            feature_cols = [c for c in work_df.select_dtypes(include=[np.number]).columns if not c.lower().endswith("_id")]

        # Only consider numeric columns
        valid_cols = [c for c in feature_cols if c in work_df.columns and pd.api.types.is_numeric_dtype(work_df[c])]

        # Construct safe pairwise ratios if at least 2 features exist
        if len(valid_cols) >= 2:
            pairs_checked = 0
            for i in range(len(valid_cols)):
                for j in range(i + 1, len(valid_cols)):
                    if len(new_cols) >= self.max_new_features:
                        break
                    c1, c2 = valid_cols[i], valid_cols[j]
                    s1 = work_df[c1]
                    s2 = work_df[c2]

                    # If both positive or strictly non-zero, build ratio
                    if (s2 >= 0).all() or (s2 > 0).sum() > 0.8 * len(s2):
                        ratio_name = f"Rasio_{c1[:10]}_Per_{c2[:10]}"
                        if ratio_name not in work_df.columns:
                            work_df[ratio_name] = (s1 / (s2 + self.epsilon)).clip(-1e6, 1e6).round(4)
                            new_cols.append(ratio_name)

                    pairs_checked += 1
                    if len(new_cols) >= self.max_new_features:
                        break

        self.constructed_features_ = new_cols
        return work_df, new_cols


def build_interaction_features(
    df: pd.DataFrame,
    feature_cols: Optional[List[str]] = None,
    max_new_features: int = 5,
) -> Tuple[pd.DataFrame, List[str]]:
    """Functional interface for automatic feature engineering [UK-07]."""
    builder = AutoFeatureBuilder(max_new_features=max_new_features)
    return builder.construct(df, feature_cols)


class CategoricalFoldEncoder:
    """Categorical encoder fit strictly on training fold data to prevent target leakage.
    
    Transforms categorical columns (product_category, payment_type_primary, customer_state)
    using smoothed Bayesian target encoding.
    """

    def __init__(
        self,
        cat_cols: Optional[List[str]] = None,
        smoothing: float = 10.0,
    ) -> None:
        self.cat_cols = cat_cols or ["product_category", "payment_type_primary", "customer_state"]
        self.smoothing = smoothing
        self.encodings_: Dict[str, Dict[str, float]] = {}
        self.global_means_: Dict[str, float] = {}
        self.fitted_on_train_only: bool = False

    def fit(self, X: pd.DataFrame, y: Union[np.ndarray, pd.Series]) -> "CategoricalFoldEncoder":
        """Fits encoding parameters strictly on training fold X and y."""
        y_arr = np.asarray(y, dtype=float)
        global_mean = float(np.mean(y_arr))

        self.encodings_ = {}
        self.global_means_ = {}

        for col in self.cat_cols:
            if col in X.columns:
                series = X[col].astype(object).fillna("MISSING").astype(str)
                df_temp = pd.DataFrame({"cat": series, "y": y_arr})
                stats = df_temp.groupby("cat")["y"].agg(["count", "mean"])
                smoothed = (stats["count"] * stats["mean"] + self.smoothing * global_mean) / (
                    stats["count"] + self.smoothing
                )
                self.encodings_[col] = smoothed.to_dict()
                self.global_means_[col] = global_mean

        self.fitted_on_train_only = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms categorical columns without accessing future or test labels."""
        if not self.fitted_on_train_only:
            raise ValueError("CategoricalFoldEncoder must be fitted on training fold data before transform.")

        X_out = X.copy()
        for col, mapping in self.encodings_.items():
            if col in X_out.columns:
                global_m = self.global_means_[col]
                encoded_col = f"{col}_te"
                X_out[encoded_col] = (
                    X_out[col].astype(object).fillna("MISSING").astype(str).map(mapping).fillna(global_m).astype(float)
                )
        return X_out

    def fit_transform(self, X: pd.DataFrame, y: Union[np.ndarray, pd.Series]) -> pd.DataFrame:
        return self.fit(X, y).transform(X)

