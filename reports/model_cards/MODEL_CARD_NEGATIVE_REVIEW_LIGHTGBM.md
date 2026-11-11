# MODEL CARD: Negative Review LightGBM Champion (E3 Combined Interactions)
## CSIP Production Machine Learning Artifact Governance

### 1. Model Details
- **Model Name**: Best Negative Review Classifier (LightGBM)
- **Artifact Path**: `artifacts/models/best_negative_review_lightgbm.joblib`
- **Metadata Sidecar**: `artifacts/models/best_negative_review_lightgbm.joblib.json`
- **Model Type**: Gradient Boosted Decision Tree (LightGBM `LGBMClassifier`)
- **Version**: 17.0.0
- **Release Date**: November 2026
- **Developer / Maintainer**: CSIP ML Engineering & Research Group

### 2. Model Purpose & Intended Use
- **Primary Objective**: Identify e-commerce transactions at high risk of severe customer dissatisfaction (review score 1 or 2) across order fulfillment lifecycle.
- **Intended Users**: Platform Operations, Customer Experience Triage, Seller Quality Teams.
- **Intended Deployment Context**: Post-fulfillment batch triage and operational diagnostic monitoring.
- **Prohibited Uses**:
  - Automated seller account suspension without human investigation.
  - Credit scoring, individual consumer profiling, or discriminatory pricing.
  - Making causal policy interventions without experimental A/B validation (governed under Level L1/L2 associative evidence).

### 3. Training Population & Split Boundaries
- **Dataset**: Olist Brazilian E-Commerce public dataset (2016–2018).
- **Training Population**: Orders completed through 2018-03-31 ($N_{train} = 63,666$).
- **Validation Population**: Orders between 2018-04-01 and 2018-06-30 ($N_{val} = 19,587$).
- **Locked Test Population**: Out-of-time orders after 2018-06-30 ($N_{test} = 12,571$).
- **Pre-split Embargo**: Strict time-based splitting with zero customer or order leakage across partitions.

### 4. Input Features (E3 Combined Interactions)
1. `total_item_price`: Sum of item purchase prices (BRL).
2. `total_freight`: Sum of shipping freight charges (BRL).
3. `total_order_value`: Combined item price and freight charges.
4. `freight_ratio`: Ratio of freight cost to total order value.
5. `item_count`: Number of items in order.
6. `payment_installments_max`: Maximum installments chosen.
7. `delivery_lead_time_days`: Elapsed days between purchase and delivery.
8. `estimated_lead_time_days`: Platform-estimated delivery days.
9. `delivery_delay_days`: Days past promised delivery date (zero if early).
10. `is_late`: Binary indicator for delivery after estimated date.
11. `approval_lag_hours`: Hours between purchase and payment approval.
12. `seller_buyer_distance_km`: Haversine geographic distance between seller and buyer.
13. `delay_x_freight_ratio`: Interaction term between delivery delay and freight burden.
14. `distance_x_weight`: Interaction between logistics distance and parcel mass.
15. `high_value_late_flag`: Interaction indicator for expensive late orders.

### 5. Quantitative Performance (Holdout Test Split)
- **PR-AUC (Average Precision)**: **0.3061** (vs. Naive Baseline: **0.1096**; +179% improvement).
- **ROC-AUC**: **0.6745** (95% Bootstrap CI: [0.658, 0.691]).
- **F1-Score**: **0.3417** (threshold = 0.50 under balanced weighting).
- **Balanced Accuracy**: **0.6439**.
- **Uncalibrated Brier Score**: 0.1373 (raw model with balanced weighting).
- **Calibrated Brier Score (Platt Scaled)**: **0.0762** (outperforms naive majority baseline 0.0985).
- **Expected Calibration Error (ECE)**: Reduced from 0.2355 to **0.0070** post-calibration.

### 6. Calibration Strategy
- **Recalibration Method**: Platt scaling (logistic sigmoid regression on log-odds) fitted strictly on the validation partition ($N_{val} = 19,587$) and verified out-of-time on the locked test partition ($N_{test} = 12,571$).
- **Calibration Parameters**: Weight = 0.9020, Intercept = -1.8089.

### 7. Explainability & Interpretability (SHAP TreeExplainer)
- Top ranking attribution features:
  1. `delivery_delay_days` (Mean $|SHAP| = 0.3058$)
  2. `delivery_lead_time_days` (Mean $|SHAP| = 0.2252$)
  3. `item_count` (Mean $|SHAP| = 0.2086$)
  4. `estimated_lead_time_days` (Mean $|SHAP| = 0.0740$)
- **Scientific Claim Boundary**: SHAP values indicate internal tree decision contribution; they do NOT prove causal impact (Level L1/L2 claim).

### 8. Known Limitations & Failure Modes
- Under severe regional logistics disruptions (e.g. postal strikes), delays exceed historical distributions, causing elevated false positive rates.
- Orders with missing customer location coordinates receive imputed median distance, slightly dampening distance attribution.
- In deployment, the raw model output MUST pass through the Platt calibrator before entering risk-scoring APIs.

### Deployment Maturity Level
- **Status**: `CONDITIONALLY_ELIGIBLE_FOR_PILOT`
- **Operational Governance Assessment**: Offline out-of-time test validated (PR-AUC 0.3061, calibrated Brier 0.0762, ECE 0.0070). Conditionally eligible for human-in-the-loop pilot triage in customer support operations. Prospective shadow testing required before autonomous action.
