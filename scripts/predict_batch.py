"""CSIP Batch Prediction & Inference Script.

Official Scheme Scope: "Mendukung deployment model".
Loads a validated champion model artifact and its metadata sidecar, validates
input features against schema and range contracts, rejects RESEARCH_ONLY models,
and produces batch predictions with audit metadata (model_version, timestamp).

CLI Usage:
    python scripts/predict_batch.py --model-path artifacts/models/best_delivery_delay_lightgbm.joblib --input-csv data/sample_input.csv --output-csv data/sample_output.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_batch_prediction(
    model_path: str | Path,
    input_path: str | Path,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    model_file = Path(model_path)
    if not model_file.is_absolute():
        model_file = REPO_ROOT / model_file

    if not model_file.exists():
        raise FileNotFoundError(f"Model artifact not found at {model_file}")

    sidecar_file = Path(str(model_file) + ".json")
    if not sidecar_file.exists():
        raise FileNotFoundError(f"Model sidecar metadata missing at {sidecar_file}")

    metadata = json.loads(sidecar_file.read_text(encoding="utf-8"))

    # 1. Gate check: Reject RESEARCH_ONLY status
    maturity = metadata.get("maturity_status") or metadata.get("status") or ""
    if maturity.upper() == "RESEARCH_ONLY":
        raise ValueError(
            f"Deployment Rejected: Model '{metadata.get('model_name', model_file.name)}' "
            f"is designated as RESEARCH_ONLY and cannot be deployed for operational batch inference."
        )

    # 2. Load model
    model = joblib.load(model_file)

    # 3. Read input
    input_file = Path(input_path)
    if not input_file.is_absolute():
        input_file = REPO_ROOT / input_file
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found at {input_file}")

    df_input = pd.read_csv(input_file)
    if df_input.empty:
        raise ValueError("Input data is empty.")

    # 4. Schema & Contract Validation
    expected_features = metadata.get("feature_list") or metadata.get("features")
    if not expected_features:
        # Fallback to model pipeline features if available
        if hasattr(model, "feature_names_in_"):
            expected_features = list(model.feature_names_in_)
        else:
            raise ValueError("No feature list found in model sidecar or pipeline.")

    missing_cols = [c for c in expected_features if c not in df_input.columns]
    if missing_cols:
        raise ValueError(
            f"Input schema contract violation: Missing expected columns: {missing_cols}"
        )

    X = df_input[expected_features].copy()

    # Range contract checks
    for col in X.select_dtypes(include=[np.number]).columns:
        if col in ["total_order_value", "total_item_price", "total_freight", "item_count"]:
            if (X[col] < 0).any():
                raise ValueError(f"Value range violation: Column '{col}' cannot contain negative values.")

    # 5. Execute Prediction
    df_out = df_input.copy()
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)
        if probs.ndim == 2 and probs.shape[1] >= 2:
            df_out["predicted_score"] = probs[:, 1]
            df_out["predicted_label"] = (probs[:, 1] >= 0.5).astype(int)
        else:
            df_out["predicted_score"] = probs
            df_out["predicted_label"] = model.predict(X)
    else:
        preds = model.predict(X)
        df_out["prediction"] = preds

    # 6. Provenance & Version Attribution
    model_version = metadata.get("model_version") or metadata.get("git_or_release_version") or "unknown"
    df_out["model_id"] = metadata.get("model_id") or metadata.get("model_name") or model_file.stem
    df_out["model_version"] = model_version
    df_out["predicted_at_utc"] = datetime.now(timezone.utc).isoformat()

    if output_path is not None:
        out_file = Path(output_path)
        if not out_file.is_absolute():
            out_file = REPO_ROOT / out_file
        out_file.parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(out_file, index=False)
        print(f"Batch inference complete. Output saved to {out_file} ({len(df_out)} rows).")

    return df_out

def main():
    parser = argparse.ArgumentParser(description="CSIP Batch Prediction Deployment Script")
    parser.add_argument("--model-path", required=True, help="Path to .joblib model artifact")
    parser.add_argument("--input-csv", required=True, help="Path to input features CSV")
    parser.add_argument("--output-csv", required=True, help="Path to output predictions CSV")
    args = parser.parse_args()

    try:
        run_batch_prediction(args.model_path, args.input_csv, args.output_csv)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

