"""Unit tests for CSIP Business Impact Evaluation Framework."""

import pytest
import numpy as np
from csip.evaluation.business_impact import (
    BusinessImpactEvaluator,
    ClassificationCapacityImpact,
    DeliveryDelayOperationalImpact,
)


def test_classification_capacity_evaluation():
    np.random.seed(42)
    n = 1000
    # 10% positive rate
    y_true = np.zeros(n)
    y_true[:100] = 1
    # Model scores correlated with target
    y_prob = np.clip(y_true * 0.6 + np.random.uniform(0.0, 0.4, size=n), 0.0, 1.0)

    impacts = BusinessImpactEvaluator.evaluate_classification_capacity(
        y_true=y_true,
        y_prob=y_prob,
        capacity_pcts=[0.05, 0.10],
    )

    assert len(impacts) == 2
    # At 5% capacity, flagged orders should be 50
    assert impacts[0].flagged_orders_count == 50
    assert impacts[0].capacity_pct == 0.05
    assert impacts[0].precision_at_capacity > 0.0
    assert impacts[0].recall_at_capacity > 0.0
    assert "non-dissatisfied" in impacts[0].false_positive_burden_desc
    assert "Observational ranking metric" in impacts[0].methodological_caveat


def test_delivery_delay_operational_impact():
    np.random.seed(42)
    n = 500
    y_true = np.random.normal(loc=12.0, scale=4.0, size=n)
    # Predicted with small noise
    y_pred = y_true + np.random.normal(loc=0.0, scale=1.5, size=n)

    impact = BusinessImpactEvaluator.evaluate_delivery_operational_impact(
        y_true_days=y_true,
        y_pred_days=y_pred,
    )

    assert impact.total_evaluated == 500
    assert impact.mae_days > 0.0
    assert impact.rmse_days >= impact.mae_days
    assert impact.within_3_days_pct > 70.0
    assert "supply chain operations" in impact.triage_opportunity_desc
    assert len(impact.population_limitation) > 0

