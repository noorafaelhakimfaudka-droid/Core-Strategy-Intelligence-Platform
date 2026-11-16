"""Unit tests for CSIP Business Decision Engine & Decision Intelligence Layer."""

import pytest
import numpy as np
import pandas as pd
from csip.decision_engine.engine import BusinessDecisionEngine
from csip.decision_engine.rules import DecisionRuleEvaluator
from csip.decision_engine.schemas import (
    DecisionPriority,
    DecisionRecommendation,
    DecisionRuleConfig,
    EvidenceType,
    OperationalFunction,
    RecommendationStatus,
)


def test_decision_rule_evaluator_critical_order():
    cfg = DecisionRuleConfig()
    evaluator = DecisionRuleEvaluator(config=cfg)

    high_risk_order = {
        "order_id": "ORD-CRIT-999999",
        "total_order_value": 450.0,
        "total_freight": 95.0,
        "freight_ratio": 0.21,
        "seller_buyer_distance_km": 2500.0,
        "estimated_lead_time_days": 25.0,
    }

    # Severe delay (+8.5 days) on high-value order
    rec = evaluator.evaluate_order(
        order_data=high_risk_order,
        predicted_delay_days=8.5,
        predicted_negative_prob=0.72,
        is_early_warning=True,
    )

    assert rec is not None
    assert rec.priority_level == DecisionPriority.CRITICAL
    assert rec.responsible_function == OperationalFunction.LOGISTICS_FULFILLMENT
    assert rec.evidence_type == EvidenceType.OBSERVATIONAL_PREDICTIVE
    assert len(rec.contributing_factors) >= 2
    assert "re-routing" in rec.limitations_and_uncertainty.lower() or "observational" in rec.limitations_and_uncertainty.lower()
    assert rec.recommendation_status == RecommendationStatus.PROPOSED


def test_decision_rule_evaluator_freight_burden_early_warning():
    cfg = DecisionRuleConfig(freight_ratio_threshold=0.25, risk_probability_threshold=0.30)
    evaluator = DecisionRuleEvaluator(config=cfg)

    order = {
        "order_id": "ORD-EW-000123",
        "total_order_value": 60.0,
        "total_freight": 28.0,
        "freight_ratio": 0.32,  # High burden
        "seller_buyer_distance_km": 600.0,
        "estimated_lead_time_days": 10.0,
    }

    rec = evaluator.evaluate_order(
        order_data=order,
        predicted_delay_days=0.5,
        predicted_negative_prob=0.45,
        is_early_warning=True,
    )

    assert rec is not None
    assert rec.priority_level == DecisionPriority.MEDIUM
    assert rec.responsible_function == OperationalFunction.CUSTOMER_EXPERIENCE
    assert "freight" in rec.business_problem.lower() or "shipping" in rec.business_problem.lower()


def test_business_decision_engine_batch_and_capacity():
    cfg = DecisionRuleConfig(capacity_max_actions_per_batch=2)
    engine = BusinessDecisionEngine(config=cfg)

    df_orders = pd.DataFrame([
        {
            "order_id": "ORD-1",
            "total_order_value": 300.0,
            "total_freight": 50.0,
            "freight_ratio": 0.20,
            "seller_buyer_distance_km": 1500.0,
        },
        {
            "order_id": "ORD-2",
            "total_order_value": 50.0,
            "total_freight": 10.0,
            "freight_ratio": 0.15,
            "seller_buyer_distance_km": 200.0,
        },
        {
            "order_id": "ORD-3",
            "total_order_value": 500.0,
            "total_freight": 80.0,
            "freight_ratio": 0.18,
            "seller_buyer_distance_km": 2200.0,
        },
    ])

    delays = np.array([4.0, 0.2, 9.0])
    probs = np.array([0.40, 0.10, 0.85])

    recs = engine.generate_recommendations(
        orders_df=df_orders,
        delay_predictions=delays,
        negative_review_probabilities=probs,
        is_early_warning=True,
    )

    # Capacity limits to top 2
    assert len(recs) == 2
    # First should be highest priority (ORD-3 with CRITICAL)
    assert recs[0].priority_level == DecisionPriority.CRITICAL

    summary = engine.summarize_recommendations(recs)
    assert summary["total_recommendations"] == 2
    assert summary["critical_action_count"] >= 1


def test_calibrate_thresholds_from_capacity():
    rng = np.random.default_rng(42)
    y_prob = np.linspace(0.05, 0.95, 200)
    y_true = (y_prob + rng.normal(0, 0.15, 200) > 0.70).astype(int)

    engine = BusinessDecisionEngine()
    cal = engine.calibrate_thresholds_from_capacity(
        y_true=y_true, y_prob=y_prob, max_alert_rate=0.15, apply=True
    )
    assert 0.0 < cal["recommended_risk_threshold"] < 1.0
    assert cal["recommended_critical_threshold"] >= cal["recommended_risk_threshold"]
    assert cal["lift_over_baseline"] > 1.0
    assert cal["applied_to_config"] is True
    assert engine.config.risk_probability_threshold == cal["recommended_risk_threshold"]


def test_design_ab_holdout_plan():
    engine = BusinessDecisionEngine(DecisionRuleConfig(capacity_max_actions_per_batch=10))
    df_orders = pd.DataFrame([
        {"order_id": f"ORD-{i}", "total_order_value": 400.0, "freight_ratio": 0.2, "seller_buyer_distance_km": 1500.0}
        for i in range(10)
    ])
    recs = engine.generate_recommendations(
        orders_df=df_orders,
        delay_predictions=np.full(10, 8.0),
        negative_review_probabilities=np.full(10, 0.7),
    )
    plan = engine.design_ab_holdout_plan(recs, holdout_fraction=0.20, random_seed=42)
    assert plan["n_total"] == 10
    assert plan["n_control_holdout"] == 2
    assert plan["n_treatment"] == 8
    assert set(plan["treatment_decision_ids"]).isdisjoint(set(plan["control_decision_ids"]))


