"""CSIP Automated Data Cleaner Engine.

Standards Compliance:
- Data Cleaning (Phase 06): Imputation of missing/infinite values, deduplication,
  and handling of mixed/constant features with zero data leakage.

Adheres strictly to Scikit-Learn Transformer contracts (fit / transform / fit_transform)
with 100% deterministic real computation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class AutoDataCleaner(BaseEstimator, TransformerMixin):
    """Automated deterministic data cleaner and transformer for tabular data.
    
    Adheres to Scikit-Learn transformer contracts (fit / transform / fit_transform)
    to strictly prevent data leakage between training and evaluation splits.
    """

    def __init__(self, drop_duplicates: bool = True) -> None:
        self.drop_duplicates = drop_duplicates
        self.imputed_medians_: Dict[str, float] = {}
        self.imputed_modes_: Dict[str, Any] = {}
        self.feature_names_in_: List[str] = []
        self.numeric_cols_: List[str] = []
        self.categorical_cols_: List[str] = []
        self.constant_cols_: List[str] = []

    def fit(self, X: pd.DataFrame, y: Any = None) -> AutoDataCleaner:
        """Learn median and mode statistics strictly on training data."""
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        self.feature_names_in_ = X.columns.tolist()
        self.imputed_medians_ = {}
        self.imputed_modes_ = {}
        self.constant_cols_ = []

        work = X.replace([np.inf, -np.inf], np.nan)

        self.numeric_cols_ = work.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols_ = work.select_dtypes(exclude=[np.number]).columns.tolist()

        # Learn numeric medians
        for col in self.numeric_cols_:
            s_clean = work[col].dropna()
            if not s_clean.empty:
                med = float(s_clean.median())
                self.imputed_medians_[col] = med
                if s_clean.nunique() <= 1:
                    self.constant_cols_.append(col)
            else:
                self.imputed_medians_[col] = 0.0

        # Learn categorical modes
        for col in self.categorical_cols_:
            s_clean = work[col].dropna()
            if not s_clean.empty:
                mode_val = s_clean.mode().iloc[0]
                self.imputed_modes_[col] = mode_val
                if s_clean.nunique() <= 1:
                    self.constant_cols_.append(col)
            else:
                self.imputed_modes_[col] = "Tidak Diketahui"

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply learned imputations to training or unseen evaluation data without leakage."""
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        work = X.copy()
        # 1. Replace infinities
        work = work.replace([np.inf, -np.inf], np.nan)

        # 2. Impute numeric columns
        for col in self.numeric_cols_:
            if col in work.columns:
                fill_val = self.imputed_medians_.get(col, 0.0)
                work[col] = work[col].fillna(fill_val)

        # 3. Impute categorical columns
        for col in self.categorical_cols_:
            if col in work.columns:
                fill_val = self.imputed_modes_.get(col, "Tidak Diketahui")
                work[col] = work[col].fillna(fill_val)

        return work

    def fit_transform(self, X: pd.DataFrame, y: Any = None, **fit_params: Any) -> pd.DataFrame:
        """Fit on X and transform X in a single step."""
        return self.fit(X, y).transform(X)

    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Convenience cleaning pipeline returning transformed DataFrame and diagnostic audit report."""
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)

        n_orig = len(df)
        work_df = df.copy()

        # 1. Replace Infinite Values
        inf_mask = np.isinf(work_df.select_dtypes(include=[np.number]))
        inf_count = int(inf_mask.sum().sum())
        work_df = work_df.replace([np.inf, -np.inf], np.nan)

        # 2. Deduplication
        dup_count = 0
        if self.drop_duplicates:
            dup_count = int(work_df.duplicated().sum())
            work_df = work_df.drop_duplicates().reset_index(drop=True)

        # 3. Fit statistics and transform
        self.fit(work_df)
        cleaned_df = self.transform(work_df)

        num_imputed = int(df.select_dtypes(include=[np.number]).isnull().sum().sum())
        cat_imputed = int(df.select_dtypes(exclude=[np.number]).isnull().sum().sum())

        report: Dict[str, Any] = {
            "initial_rows": n_orig,
            "cleaned_rows": len(cleaned_df),
            "duplicates_removed": dup_count,
            "inf_values_handled": inf_count,
            "numeric_nulls_imputed": num_imputed,
            "categorical_nulls_imputed": cat_imputed,
            "total_nulls_repaired": num_imputed + cat_imputed,
            "constant_columns_detected": self.constant_cols_,
            "is_clean": bool(cleaned_df.isnull().sum().sum() == 0),
        }

        return cleaned_df, report


def auto_clean_dataframe(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Functional interface for automated data cleaning."""
    cleaner = AutoDataCleaner(drop_duplicates=drop_duplicates)
    return cleaner.clean(df)
