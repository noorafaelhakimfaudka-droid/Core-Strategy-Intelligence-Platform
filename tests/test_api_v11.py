"""Integration and Unit Tests for CSIP REST API."""

import pytest
from fastapi.testclient import TestClient
from csip.api.server import app
from csip._version import __version__ as CSIP_VERSION


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["version"] == CSIP_VERSION
    assert response.headers.get("X-CSIP-Version") == CSIP_VERSION
    assert "X-Request-ID" in response.headers


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service_version"] == CSIP_VERSION
    assert "models_loaded" in data


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True
    assert data["service_version"] == CSIP_VERSION


def test_predict_batch_endpoint(client):
    payload = {
        "orders": [
            {
                "order_id": "ORD-TEST-001",
                "total_item_price": 120.0,
                "total_freight": 25.0,
                "total_order_value": 145.0,
                "freight_ratio": 0.172,
                "seller_buyer_distance_km": 450.0,
                "estimated_lead_time_days": 14.0,
                "item_count": 1,
                "payment_installments_max": 2,
                "approval_lag_hours": 1.5,
            }
        ]
    }
    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["batch_size"] == 1
    assert len(data["predictions"]) == 1
    pred = data["predictions"][0]
    assert pred["order_id"] == "ORD-TEST-001"
    assert "predicted_delay_days" in pred
    assert "predicted_negative_prob" in pred
    assert pred["prediction_timestamp_scope"] == "CHECKOUT_EARLY_WARNING"


def test_decisions_recommend_endpoint(client):
    payload = {
        "orders": [
            {
                "order_id": "ORD-TEST-HIGH-RISK",
                "total_item_price": 350.0,
                "total_freight": 85.0,
                "total_order_value": 435.0,
                "freight_ratio": 0.195,
                "seller_buyer_distance_km": 2800.0,
                "estimated_lead_time_days": 28.0,
                "item_count": 3,
                "payment_installments_max": 6,
                "approval_lag_hours": 24.0,
            }
        ],
        "risk_threshold": 0.20,
        "delay_threshold": 2.0,
    }
    response = client.post("/decisions/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "summary" in data
    assert "recommendations" in data


def test_models_registry_endpoint(client):
    response = client.get("/models/registry")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total_registered_metrics" in data
    assert data["total_registered_metrics"] > 0

