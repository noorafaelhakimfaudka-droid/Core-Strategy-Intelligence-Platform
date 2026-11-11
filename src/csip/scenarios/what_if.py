"""CSIP What-If & Partial Dependence Scenario Intelligence.

Implements BNSP SKKNI Competencies:
- [UK-08] Membangun Skenario Model: Simulasi interaktif perubahan variabel input pada model inferensi.
- [UK-11] Mengembangkan Solusi: Kurva respons parsial (Partial Dependence Curve) dan proyeksi selisih terhadap baseline populasi.

100% Real Computation, Local, Zero Emojis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd


def predict_what_if(pipeline: Dict[str, Any], custom_inputs: Dict[str, float]) -> Dict[str, Any]:
    """[UK-08, UK-11] Run model inference and calculate Partial Dependence Curves on user scenario.
    
    Args:
        pipeline: Trained pipeline dictionary produced by train_semantic_ml_pipeline.
        custom_inputs: Dictionary mapping feature names to user-defined scenario values.
        
    Returns:
        Dictionary containing prediction, baseline, difference metrics, and PDP curve arrays.
    """
    row = pipeline["X_median"].copy()
    for col, val in custom_inputs.items():
        if col in row.index:
            row[col] = float(val)

    X_input = pd.DataFrame([row[pipeline["feature_cols"]]])
    pred_val = float(pipeline["model"].predict(X_input)[0])
    base_val = float(pipeline["y_mean"])
    diff_val = float(pred_val - base_val)
    diff_pct = float((diff_val / (abs(base_val) + 1e-9)) * 100.0)

    # Compute Partial Dependence Curve for the top feature #1
    top_features = pipeline.get("top_features", [])
    if top_features:
        top1 = top_features[0]
        st_row = pipeline["stats_df"].iloc[0]
        f_min = float(st_row["Min"])
        f_max = float(st_row["Max"])
        if f_max <= f_min:
            f_max = f_min + 1.0
        grid_x = np.linspace(f_min, f_max, 60)

        grid_df = pd.DataFrame([row[pipeline["feature_cols"]]] * 60)
        grid_df[top1] = grid_x
        grid_preds = np.asarray(pipeline["model"].predict(grid_df), dtype=float)

        base_grid_df = pd.DataFrame([pipeline["X_median"][pipeline["feature_cols"]]] * 60)
        base_grid_df[top1] = grid_x
        base_grid_preds = np.asarray(pipeline["model"].predict(base_grid_df), dtype=float)
        current_x = float(row[top1])
    else:
        grid_x = np.linspace(0, 1, 60)
        grid_preds = np.zeros(60, dtype=float)
        base_grid_preds = np.zeros(60, dtype=float)
        current_x = 0.0

    return {
        "pred_val": pred_val,
        "base_val": base_val,
        "diff_val": diff_val,
        "diff_pct": diff_pct,
        "grid_x": grid_x,
        "grid_preds": grid_preds,
        "base_grid_preds": base_grid_preds,
        "current_x": current_x,
    }
