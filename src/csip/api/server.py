"""FastAPI Decoupled Inference & Monitoring Microservice.

Provides decoupled REST API endpoints for:
1. GET /health - Service health, active champion model version, and baseline reference window.
2. POST /predict/batch - Dual-model inference (delivery delay + review risk) with latency profiling.
3. POST /monitor/drift - Real-time feature covariate drift (PSI, KS test, Wasserstein) against reference slice.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any, Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from csip.monitoring.drift_engine import DriftEngine
from csip.monitoring.stream_simulator import StreamSimulator

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Feature sets matching trained models
DELAY_FEATURES = [
    "total_order_value",
    "freight_ratio",
    "estimated_lead_time_days",
    "seller_buyer_distance_km",
    "approval_lag_hours",
]

REVIEW_FEATURES = [
    "total_item_price",
    "total_freight",
    "total_order_value",
    "freight_ratio",
    "item_count",
    "payment_installments_max",
    "seller_buyer_distance_km",
    "estimated_lead_time_days",
    "distance_x_weight",
    "prior_order_count",
]


class PredictionItem(BaseModel):
    order_id: Optional[str] = None
    predicted_delay_days: float
    predicted_negative_prob: float
    predicted_negative_flag: int


class BatchOrderRequest(BaseModel):
    orders: List[Dict[str, Any]] = Field(..., description="List of order feature dictionaries")


class BatchOrderResponse(BaseModel):
    status: str = "success"
    batch_size: int
    total_latency_ms: float
    avg_latency_per_record_ms: float
    predictions: List[PredictionItem]


class DriftRequest(BaseModel):
    records: List[Dict[str, Any]] = Field(..., description="Batch records to evaluate against reference distribution")
    features: Optional[List[str]] = Field(default=None, description="Optional list of numerical features")


class DriftResponse(BaseModel):
    status: str = "success"
    records_evaluated: int
    overall_status: str
    mean_psi: float
    max_psi: float
    worst_feature: Optional[str] = None
    drift_alert: bool
    features: Dict[str, Any]


# Global state holder
app_state: Dict[str, Any] = {
    "delay_model": None,
    "review_model": None,
    "drift_engine": None,
    "simulator": None,
    "reference_df": None,
    "reference_meta": {},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models and reference baseline upon application startup."""
    models_dir = REPO_ROOT / "artifacts" / "models"
    delay_path = models_dir / "best_delivery_delay_lightgbm.joblib"
    review_path = models_dir / "best_early_warning_review_lightgbm.joblib"
    if not review_path.exists():
        review_path = models_dir / "best_negative_review_lightgbm.joblib"

    if delay_path.exists():
        app_state["delay_model"] = joblib.load(delay_path)
    if review_path.exists():
        app_state["review_model"] = joblib.load(review_path)

    app_state["drift_engine"] = DriftEngine()
    try:
        sim = StreamSimulator()
        app_state["simulator"] = sim
        app_state["reference_df"] = sim.get_reference_data()
        app_state["reference_meta"] = {
            "train_start": "2016-09-04",
            "train_end": "2018-03-31",
            "reference_records": len(app_state["reference_df"]),
        }
    except Exception:
        app_state["reference_df"] = pd.DataFrame()
        app_state["reference_meta"] = {"status": "unloaded"}

    yield
    app_state.clear()


app = FastAPI(
    title="CSIP Decoupled Inference & Monitoring Microservice",
    description="Low-latency inference microservice and statistical drift observatory.",
    version="18.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "CSIP Decoupled Inference & Monitoring Microservice",
        "version": "18.0.0",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health():
    """Service health and model metadata check."""
    return {
        "status": "healthy",
        "service_version": "18.0.0",
        "active_model_version": "champion_v1",
        "reference_window": app_state.get("reference_meta", {}),
        "models_loaded": {
            "delivery_delay_regressor": app_state.get("delay_model") is not None,
            "negative_review_classifier": app_state.get("review_model") is not None,
        },
    }


@app.post("/predict/batch", response_model=BatchOrderResponse)
def predict_batch(payload: BatchOrderRequest):
    """Run dual-model batch inference on incoming orders."""
    if not payload.orders:
        raise HTTPException(status_code=400, detail="Empty order batch provided.")

    t0 = time.perf_counter()
    df = pd.DataFrame(payload.orders)

    # 1. Delivery delay inference
    delay_model = app_state.get("delay_model")
    if delay_model is not None:
        X_delay = df.reindex(columns=DELAY_FEATURES, fill_value=0.0).fillna(0.0)
        delay_preds = delay_model.predict(X_delay)
    else:
        delay_preds = np.zeros(len(df))

    # 2. Negative review risk inference
    review_model = app_state.get("review_model")
    if review_model is not None:
        X_rev = df.reindex(columns=REVIEW_FEATURES, fill_value=0.0).fillna(0.0)
        if hasattr(review_model, "predict_proba"):
            rev_probs = review_model.predict_proba(X_rev)[:, 1]
        else:
            rev_probs = review_model.predict(X_rev)
    else:
        rev_probs = np.full(len(df), 0.1)

    t1 = time.perf_counter()
    total_latency_ms = float(np.round((t1 - t0) * 1000.0, 2))
    avg_latency_ms = float(np.round(total_latency_ms / max(len(df), 1), 4))

    predictions = []
    for i in range(len(df)):
        oid = str(df.iloc[i].get("order_id", f"ORD-{i:05d}"))
        d_val = float(np.round(delay_preds[i], 2))
        p_val = float(np.round(rev_probs[i], 4))
        flag = 1 if p_val >= 0.50 else 0
        predictions.append(
            PredictionItem(
                order_id=oid,
                predicted_delay_days=d_val,
                predicted_negative_prob=p_val,
                predicted_negative_flag=flag,
            )
        )

    return BatchOrderResponse(
        status="success",
        batch_size=len(df),
        total_latency_ms=total_latency_ms,
        avg_latency_per_record_ms=avg_latency_ms,
        predictions=predictions,
    )


@app.post("/monitor/drift", response_model=DriftResponse)
def monitor_drift(payload: DriftRequest):
    """Evaluate statistical feature drift against the training baseline."""
    if not payload.records:
        raise HTTPException(status_code=400, detail="Empty records batch provided for drift monitoring.")

    current_df = pd.DataFrame(payload.records)
    ref_df = app_state.get("reference_df")
    drift_engine: DriftEngine = app_state.get("drift_engine") or DriftEngine()

    if ref_df is None or ref_df.empty:
        # Fallback to internal generator
        try:
            sim = StreamSimulator()
            ref_df = sim.get_reference_data()
            app_state["reference_df"] = ref_df
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Reference dataset unavailable: {e}")

    drift_report = drift_engine.evaluate_feature_drift(
        reference_df=ref_df,
        current_df=current_df,
        features=payload.features,
    )

    summary = drift_report["summary"]
    is_alert = summary["overall_status"] == "CRITICAL_DRIFT"

    return DriftResponse(
        status="success",
        records_evaluated=len(current_df),
        overall_status=summary["overall_status"],
        mean_psi=summary["mean_psi"],
        max_psi=summary["max_psi"],
        worst_feature=summary["worst_feature"],
        drift_alert=is_alert,
        features=drift_report["features"],
    )
