"""Client SDK for CSIP Inference & Monitoring Microservice with Standalone Fallback.

Ensures seamless operation whether the FastAPI daemon is active or Streamlit runs in
standalone offline mode.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any, Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
import requests

from csip.monitoring.drift_engine import DriftEngine
from csip.monitoring.stream_simulator import StreamSimulator

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

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


class InferenceMonitoringClient:
    """Client for decoupled FastAPI microservice with automatic in-process fallback."""

    def __init__(self, api_url: str = "http://127.0.0.1:8000", timeout: float = 2.0) -> None:
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self._delay_model = None
        self._review_model = None
        self._drift_engine = None
        self._simulator = None
        self._reference_df = None

    def is_microservice_online(self) -> bool:
        """Check if external FastAPI daemon is reachable."""
        try:
            resp = requests.get(f"{self.api_url}/health", timeout=0.6)
            return resp.status_code == 200
        except Exception:
            return False

    def _ensure_local_assets(self) -> None:
        """Lazy-load local models and reference baseline for fallback mode."""
        if self._delay_model is None or self._review_model is None:
            models_dir = REPO_ROOT / "artifacts" / "models"
            delay_path = models_dir / "best_delivery_delay_lightgbm.joblib"
            review_path = models_dir / "best_early_warning_review_lightgbm.joblib"
            if not review_path.exists():
                review_path = models_dir / "best_negative_review_lightgbm.joblib"

            if delay_path.exists():
                self._delay_model = joblib.load(delay_path)
            if review_path.exists():
                self._review_model = joblib.load(review_path)

        if self._drift_engine is None:
            self._drift_engine = DriftEngine()

        if self._reference_df is None:
            try:
                self._simulator = StreamSimulator()
                self._reference_df = self._simulator.get_reference_data()
            except Exception:
                self._reference_df = pd.DataFrame()

    def get_health(self) -> Dict[str, Any]:
        """Fetch service health or construct fallback status."""
        if self.is_microservice_online():
            try:
                resp = requests.get(f"{self.api_url}/health", timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    data["connection_mode"] = "FASTAPI_MICROSERVICE"
                    return data
            except Exception:
                pass

        # Standalone Fallback
        self._ensure_local_assets()
        return {
            "status": "healthy",
            "service_version": "18.0.0-standalone",
            "active_model_version": "champion_v1",
            "connection_mode": "STANDALONE_FALLBACK",
            "reference_window": {
                "train_start": "2016-09-04",
                "train_end": "2018-03-31",
                "reference_records": len(self._reference_df) if self._reference_df is not None else 0,
            },
            "models_loaded": {
                "delivery_delay_regressor": self._delay_model is not None,
                "negative_review_classifier": self._review_model is not None,
            },
        }

    def predict_batch(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run batch inference via REST API or local fallback."""
        if not orders:
            return {"status": "success", "batch_size": 0, "predictions": [], "total_latency_ms": 0.0}

        if self.is_microservice_online():
            try:
                resp = requests.post(
                    f"{self.api_url}/predict/batch",
                    json={"orders": orders},
                    timeout=self.timeout + 3.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    data["executed_via"] = "FASTAPI_MICROSERVICE"
                    return data
            except Exception:
                pass

        # Standalone Fallback
        self._ensure_local_assets()
        t0 = time.perf_counter()
        df = pd.DataFrame(orders)

        if self._delay_model is not None:
            X_delay = df.reindex(columns=DELAY_FEATURES, fill_value=0.0).fillna(0.0)
            delay_preds = self._delay_model.predict(X_delay)
        else:
            delay_preds = np.zeros(len(df))

        if self._review_model is not None:
            X_rev = df.reindex(columns=REVIEW_FEATURES, fill_value=0.0).fillna(0.0)
            if hasattr(self._review_model, "predict_proba"):
                rev_probs = self._review_model.predict_proba(X_rev)[:, 1]
            else:
                rev_probs = self._review_model.predict(X_rev)
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
            predictions.append({
                "order_id": oid,
                "predicted_delay_days": d_val,
                "predicted_negative_prob": p_val,
                "predicted_negative_flag": flag,
            })

        return {
            "status": "success",
            "batch_size": len(df),
            "total_latency_ms": total_latency_ms,
            "avg_latency_per_record_ms": avg_latency_ms,
            "predictions": predictions,
            "executed_via": "STANDALONE_FALLBACK",
        }

    def monitor_drift(
        self,
        records: List[Dict[str, Any]],
        features: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Compute statistical drift via REST API or local fallback."""
        if not records:
            return {"status": "empty", "records_evaluated": 0, "overall_status": "STABLE"}

        if self.is_microservice_online():
            try:
                resp = requests.post(
                    f"{self.api_url}/monitor/drift",
                    json={"records": records, "features": features},
                    timeout=self.timeout + 5.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    data["executed_via"] = "FASTAPI_MICROSERVICE"
                    return data
            except Exception:
                pass

        # Standalone Fallback
        self._ensure_local_assets()
        current_df = pd.DataFrame(records)
        report = self._drift_engine.evaluate_feature_drift(
            reference_df=self._reference_df,
            current_df=current_df,
            features=features,
        )

        summary = report["summary"]
        is_alert = summary["overall_status"] == "CRITICAL_DRIFT"

        return {
            "status": "success",
            "records_evaluated": len(current_df),
            "overall_status": summary["overall_status"],
            "mean_psi": summary["mean_psi"],
            "max_psi": summary["max_psi"],
            "worst_feature": summary["worst_feature"],
            "drift_alert": is_alert,
            "features": report["features"],
            "executed_via": "STANDALONE_FALLBACK",
        }
