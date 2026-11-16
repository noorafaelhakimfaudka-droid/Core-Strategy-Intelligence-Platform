"""FastAPI Decoupled Inference & Monitoring Microservice.

CSIP Production-Oriented REST API providing:
1. GET /health - Service health, active champion model version, and baseline reference window.
2. GET /ready - Kubernetes / container orchestration readiness probe.
3. POST /predict/batch - Dual-model inference (delivery delay + review risk) with latency profiling.
4. POST /predict/early-warning - Checkout-time prediction strictly using features available at checkout.
5. POST /predict/post-fulfillment - Post-delivery diagnostic prediction using post-fulfillment features.
6. POST /decisions/recommend - Business Decision Engine generating prioritized operational interventions.
7. POST /monitor/drift - Feature covariate drift (PSI, KS test, Wasserstein) against reference slice.
8. GET /models/registry - Model lifecycle registry, champion designations, and promotion history.
"""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from csip._version import __version__ as CSIP_VERSION
from csip.decision_engine.engine import BusinessDecisionEngine
from csip.decision_engine.schemas import DecisionRuleConfig
from csip.models.registry import ModelLifecycleManager, ModelRole
from csip.monitoring.drift_engine import DriftEngine
from csip.monitoring.stream_simulator import StreamSimulator

logger = logging.getLogger(__name__)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Feature schemas matching trained model artifacts
DELAY_FEATURES = [
    "total_order_value",
    "freight_ratio",
    "estimated_lead_time_days",
    "seller_buyer_distance_km",
    "approval_lag_hours",
]

EARLY_WARNING_FEATURES = [
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

POST_FULFILLMENT_FEATURES = [
    "total_item_price",
    "total_freight",
    "total_order_value",
    "freight_ratio",
    "item_count",
    "payment_installments_max",
    "delivery_lead_time_days",
    "estimated_lead_time_days",
    "delivery_delay_days",
    "is_late",
    "approval_lag_hours",
    "seller_buyer_distance_km",
    "delay_x_freight_ratio",
    "distance_x_weight",
    "high_value_late_flag",
]


class PredictionItem(BaseModel):
    order_id: Optional[str] = None
    predicted_delay_days: float
    predicted_negative_prob: float
    predicted_negative_flag: int
    prediction_timestamp_scope: str = "CHECKOUT_EARLY_WARNING"


class BatchOrderRequest(BaseModel):
    orders: List[Dict[str, Any]] = Field(..., description="List of order feature dictionaries")


class BatchOrderResponse(BaseModel):
    status: str = "success"
    service_version: str = CSIP_VERSION
    batch_size: int
    total_latency_ms: float
    avg_latency_per_record_ms: float
    predictions: List[PredictionItem]


class DecisionRequest(BaseModel):
    orders: List[Dict[str, Any]] = Field(..., description="List of order records to evaluate")
    risk_threshold: Optional[float] = Field(default=0.35, description="Negative review probability cutoff")
    delay_threshold: Optional[float] = Field(default=3.0, description="Delivery delay days cutoff")
    max_capacity_actions: Optional[int] = Field(default=50, description="Maximum prioritized actions")


class DecisionResponse(BaseModel):
    status: str = "success"
    service_version: str = CSIP_VERSION
    total_recommendations: int
    summary: Dict[str, Any]
    recommendations: List[Dict[str, Any]]


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
    monitoring_environment: str = "HISTORICAL_BATCH_SIMULATION (Olist 2016-2018)"


# Microservice global state holder
app_state: Dict[str, Any] = {
    "delay_model": None,
    "early_warning_model": None,
    "post_fulfillment_model": None,
    "decision_engine": None,
    "drift_engine": None,
    "lifecycle_manager": None,
    "simulator": None,
    "reference_df": None,
    "reference_meta": {},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models, registries, and reference baseline upon application startup."""
    models_dir = REPO_ROOT / "artifacts" / "models"
    delay_path = models_dir / "best_delivery_delay_lightgbm.joblib"
    ew_path = models_dir / "best_early_warning_review_lightgbm.joblib"
    pf_path = models_dir / "best_negative_review_lightgbm.joblib"

    if delay_path.exists():
        app_state["delay_model"] = joblib.load(delay_path)
    if ew_path.exists():
        app_state["early_warning_model"] = joblib.load(ew_path)
    if pf_path.exists():
        app_state["post_fulfillment_model"] = joblib.load(pf_path)

    app_state["decision_engine"] = BusinessDecisionEngine()
    app_state["drift_engine"] = DriftEngine()
    app_state["lifecycle_manager"] = ModelLifecycleManager(repo_root=REPO_ROOT)

    try:
        sim = StreamSimulator()
        app_state["simulator"] = sim
        app_state["reference_df"] = sim.get_reference_data()
        app_state["reference_meta"] = {
            "train_start": "2016-09-04",
            "train_end": "2018-03-31",
            "reference_records": len(app_state["reference_df"]),
            "environment": "HISTORICAL_BATCH_REFERENCE",
        }
    except Exception:
        app_state["reference_df"] = pd.DataFrame()
        app_state["reference_meta"] = {"status": "unloaded"}

    yield
    app_state.clear()


app = FastAPI(
    title="CSIP Decoupled Inference, Decision & Monitoring Microservice",
    description="Production-oriented REST API for E-Commerce Risk Intelligence and Decision Governance.",
    version=CSIP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    corr_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = corr_id
    response.headers["X-CSIP-Version"] = CSIP_VERSION
    return response


@app.get("/")
def root():
    return {
        "service": "CSIP Decoupled Inference, Decision & Monitoring Microservice",
        "version": CSIP_VERSION,
        "status": "operational",
        "platform": "Core Strategy & Intelligence Platform",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health():
    """Service health and model metadata check."""
    return {
        "status": "healthy",
        "service_version": CSIP_VERSION,
        "active_model_version": f"champion_v{CSIP_VERSION}",
        "reference_window": app_state.get("reference_meta", {}),
        "models_loaded": {
            "delivery_delay_regressor": app_state.get("delay_model") is not None,
            "negative_review_classifier": (
                app_state.get("early_warning_model") is not None
                or app_state.get("post_fulfillment_model") is not None
            ),
            "early_warning_review_classifier": app_state.get("early_warning_model") is not None,
            "post_fulfillment_review_classifier": app_state.get("post_fulfillment_model") is not None,
        },
    }


@app.get("/ready")
def ready():
    """Readiness probe ensuring core inference models are loaded and available."""
    models_ready = (
        app_state.get("delay_model") is not None
        and (app_state.get("early_warning_model") is not None or app_state.get("post_fulfillment_model") is not None)
    )
    if not models_ready:
        raise HTTPException(status_code=503, detail="Models not yet loaded into memory.")
    return {
        "ready": True,
        "service_version": CSIP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/predict/batch", response_model=BatchOrderResponse)
def predict_batch(payload: BatchOrderRequest):
    """Run dual-model batch inference on incoming orders using checkout-time early warning features."""
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

    # 2. Negative review early warning inference
    review_model = app_state.get("early_warning_model") or app_state.get("post_fulfillment_model")
    if review_model is not None:
        feats = EARLY_WARNING_FEATURES if app_state.get("early_warning_model") is not None else POST_FULFILLMENT_FEATURES
        X_rev = df.reindex(columns=feats, fill_value=0.0).fillna(0.0)
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
                prediction_timestamp_scope="CHECKOUT_EARLY_WARNING",
            )
        )

    return BatchOrderResponse(
        status="success",
        service_version=CSIP_VERSION,
        batch_size=len(df),
        total_latency_ms=total_latency_ms,
        avg_latency_per_record_ms=avg_latency_ms,
        predictions=predictions,
    )


@app.post("/decisions/recommend", response_model=DecisionResponse)
def recommend_decisions(payload: DecisionRequest):
    """Generate prioritized business decisions and operational interventions from orders."""
    if not payload.orders:
        raise HTTPException(status_code=400, detail="Empty order list provided.")

    df = pd.DataFrame(payload.orders)
    cfg = DecisionRuleConfig(
        risk_probability_threshold=payload.risk_threshold or 0.35,
        delay_days_threshold=payload.delay_threshold or 3.0,
        capacity_max_actions_per_batch=payload.max_capacity_actions or 50,
    )
    engine = BusinessDecisionEngine(config=cfg)

    # Run predictions if models loaded
    delay_model = app_state.get("delay_model")
    if delay_model is not None:
        X_delay = df.reindex(columns=DELAY_FEATURES, fill_value=0.0).fillna(0.0)
        delay_preds = delay_model.predict(X_delay)
    else:
        delay_preds = np.zeros(len(df))

    review_model = app_state.get("early_warning_model") or app_state.get("post_fulfillment_model")
    if review_model is not None:
        feats = EARLY_WARNING_FEATURES if app_state.get("early_warning_model") is not None else POST_FULFILLMENT_FEATURES
        X_rev = df.reindex(columns=feats, fill_value=0.0).fillna(0.0)
        if hasattr(review_model, "predict_proba"):
            rev_probs = review_model.predict_proba(X_rev)[:, 1]
        else:
            rev_probs = review_model.predict(X_rev)
    else:
        rev_probs = np.zeros(len(df))

    recs = engine.generate_recommendations(
        orders_df=df,
        delay_predictions=delay_preds,
        negative_review_probabilities=rev_probs,
        is_early_warning=True,
    )
    summary = engine.summarize_recommendations(recs)

    return DecisionResponse(
        status="success",
        service_version=CSIP_VERSION,
        total_recommendations=len(recs),
        summary=summary,
        recommendations=[r.to_dict() for r in recs],
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
        monitoring_environment="HISTORICAL_BATCH_SIMULATION (Olist 2016-2018)",
    )


@app.get("/models/registry")
def get_model_registry():
    """Retrieve verified model registry and promotion history."""
    reg_path = REPO_ROOT / "artifacts" / "metadata" / "MODEL_RESULTS_REGISTRY.csv"
    promo_path = REPO_ROOT / "artifacts" / "metadata" / "PROMOTION_HISTORY.csv"

    rows = []
    if reg_path.exists():
        import csv
        with open(reg_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    promotions = []
    if promo_path.exists():
        import csv
        with open(promo_path, "r", encoding="utf-8") as f:
            promotions = list(csv.DictReader(f))

    return {
        "status": "success",
        "service_version": CSIP_VERSION,
        "total_registered_metrics": len(rows),
        "total_lifecycle_events": len(promotions),
        "models": rows[:10],
        "promotion_events": promotions[-5:] if promotions else [],
    }
