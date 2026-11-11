"""CSIP Automated Data Cleaner Engine.

Implements BNSP SKKNI Competency:
- [UK-06] Membersihkan Data: Pembersihan nilai infinit, dedukplikasi baris,
  dan penanganan missing values (imputasi median/modus) secara otomatis dan deterministik.

100% Real Computation, Zero Hardcoding, Zero Emojis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


class AutoDataCleaner:
    """[UK-06] Automated deterministic cleaner for arbitrary tabular data."""

    def __init__(self, drop_duplicates: bool = True) -> None:
        self.drop_duplicates = drop_duplicates
        self.imputed_medians_: Dict[str, float] = {}
        self.imputed_modes_: Dict[str, Any] = {}

    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Clean dataset by handling infinites, deduplicating, and imputing nulls."""
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

        # 3. Median & Mode Imputation
        numeric_cols = work_df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = work_df.select_dtypes(exclude=[np.number]).columns.tolist()

        num_imputed = 0
        cat_imputed = 0

        for col in numeric_cols:
            n_null = int(work_df[col].isnull().sum())
            if n_null > 0:
                median_val = float(work_df[col].median()) if not work_df[col].dropna().empty else 0.0
                self.imputed_medians_[col] = median_val
                work_df[col] = work_df[col].fillna(median_val)
                num_imputed += n_null

        for col in cat_cols:
            n_null = int(work_df[col].isnull().sum())
            if n_null > 0:
                mode_series = work_df[col].mode(dropna=True)
                mode_val = mode_series.iloc[0] if not mode_series.empty else "Tidak Diketahui"
                self.imputed_modes_[col] = mode_val
                work_df[col] = work_df[col].fillna(mode_val)
                cat_imputed += n_null

        report: Dict[str, Any] = {
            "initial_rows": n_orig,
            "cleaned_rows": len(work_df),
            "duplicates_removed": dup_count,
            "inf_values_handled": inf_count,
            "numeric_nulls_imputed": num_imputed,
            "categorical_nulls_imputed": cat_imputed,
            "total_nulls_repaired": num_imputed + cat_imputed,
            "is_clean": bool(work_df.isnull().sum().sum() == 0),
        }

        return work_df, report


def auto_clean_dataframe(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Functional interface for automated data cleaning [UK-06]."""
    cleaner = AutoDataCleaner(drop_duplicates=drop_duplicates)
    return cleaner.clean(df)

