"""Independent re-evaluation of persisted model artifacts on the locked out-of-time test split.

Purpose: establish ONE source of truth for headline metrics by recomputing them
directly from the physical .joblib artifacts and data/processed/order_level.parquet,
instead of copying numbers between documents.

Split definition (from each artifact sidecar `split_bounds`):
    locked test = orders with order_purchase_timestamp > val_end, non-null target.

Output: artifacts/reports/locked_test_reevaluation.json
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "artifacts" / "models"
DATA = ROOT / "data" / "processed" / "order_level.parquet"
OUT = ROOT / "artifacts" / "reports" / "locked_test_reevaluation.json"

SEED = 42
N_BOOT = 1000

CLASSIFIERS = [
    "best_negative_review_lightgbm.joblib",
    "best_early_warning_review_lightgbm.joblib",
]
REGRESSORS = ["best_delivery_delay_lightgbm.joblib"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ece(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> float:
    bins = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(p, bins) - 1, 0, n_bins - 1)
    total = 0.0
    for b in range(n_bins):
        m = idx == b
        if m.any():
            total += m.mean() * abs(y[m].mean() - p[m].mean())
    return float(total)


def boot_ci(y, p, fn, rng) -> list[float]:
    n = len(y)
    vals = []
    for _ in range(N_BOOT):
        i = rng.integers(0, n, n)
        if y[i].min() == y[i].max():
            continue
        vals.append(fn(y[i], p[i]))
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]


def load(name: str):
    path = MODELS / name
    meta = json.loads((MODELS / f"{name}.json").read_text(encoding="utf-8"))
    return path, joblib.load(path), meta


def test_split(df: pd.DataFrame, meta: dict, target: str) -> pd.DataFrame:
    val_end = pd.Timestamp(meta["split_bounds"]["val_end"])
    ts = pd.to_datetime(df["order_purchase_timestamp"])
    out = df[ts > val_end].dropna(subset=[target])
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    df = pd.read_parquet(DATA)
    results: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_file": str(DATA.relative_to(ROOT)).replace("\\", "/"),
        "data_sha256": sha256(DATA),
        "bootstrap_resamples": N_BOOT,
        "seed": SEED,
        "models": {},
    }

    for name in CLASSIFIERS:
        path, model, meta = load(name)
        target = meta["target_name"]
        te = test_split(df, meta, target)
        X = te[meta["feature_list"]]
        y = te[target].astype(int).to_numpy()
        p = model.predict_proba(X)[:, 1]
        base = float(y.mean())
        results["models"][name] = {
            "artifact_sha256": sha256(path),
            "target": target,
            "feature_set": meta.get("feature_set_name"),
            "n_features": len(meta["feature_list"]),
            "split_rule": f"order_purchase_timestamp > {meta['split_bounds']['val_end']} and target not null",
            "n_test": int(len(y)),
            "base_rate": round(base, 4),
            "pr_auc": round(float(average_precision_score(y, p)), 4),
            "pr_auc_95ci": boot_ci(y, p, average_precision_score, rng),
            "roc_auc": round(float(roc_auc_score(y, p)), 4),
            "roc_auc_95ci": boot_ci(y, p, roc_auc_score, rng),
            "brier": round(float(brier_score_loss(y, p)), 4),
            "brier_baseline_constant": round(base * (1 - base), 4),
            "ece_10bin": round(ece(y, p), 4),
            "mean_predicted_prob": round(float(p.mean()), 4),
        }

    for name in REGRESSORS:
        path, model, meta = load(name)
        target = meta["target_name"]
        te = test_split(df, meta, target)
        X = te[meta["feature_list"]]
        y = te[target].to_numpy(dtype=float)
        pred = model.predict(X)
        tr_mask = pd.to_datetime(df["order_purchase_timestamp"]) <= pd.Timestamp(meta["split_bounds"]["train_end"])
        train_median = float(df.loc[tr_mask, target].dropna().median())
        results["models"][name] = {
            "artifact_sha256": sha256(path),
            "target": target,
            "n_features": len(meta["feature_list"]),
            "split_rule": f"order_purchase_timestamp > {meta['split_bounds']['val_end']} and target not null",
            "n_test": int(len(y)),
            "mae": round(float(mean_absolute_error(y, pred)), 4),
            "rmse": round(float(np.sqrt(mean_squared_error(y, pred))), 4),
            "r2": round(float(r2_score(y, pred)), 4),
            "baseline_train_median_mae": round(float(np.mean(np.abs(y - train_median))), 4),
        }

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results["models"], indent=2))


if __name__ == "__main__":
    main()

