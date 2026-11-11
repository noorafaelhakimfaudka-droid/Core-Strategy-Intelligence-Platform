# MODEL CARD: Delivery Delay Regressor Champion (LightGBM)
## CSIP Machine Learning Governance & Honest Evaluation Artifact

### 1. Model Details
- **Model Name**: Delivery Delay Regressor (LightGBM)
- **Artifact Path**: `artifacts/models/best_delivery_delay_lightgbm.joblib`
- **Metadata Sidecar**: `artifacts/models/best_delivery_delay_lightgbm.joblib.json`
- **Model Type**: Gradient Boosted Decision Tree Regressor (`LGBMRegressor`)
- **Version**: 17.0.0
- **Release Date**: November 2026
- **Governance Decision**: **APPROVED FOR OPERATIONAL EARLY WARNING DISPATCH**

### 2. Operational & Business Context
- **Operational Scope**: Predict continuous delivery delays (days past promise date) at order dispatch to proactively notify customers and alert courier carrier partners.
- **Features**: `seller_buyer_distance_km`, `estimated_lead_time_days`, `total_freight`, `freight_ratio`, `distance_x_weight`, `approval_lag_hours`.

### 3. Quantitative Evaluation (Locked Test Set: $N_{test} = 12,630$)
- **Mean Absolute Error (MAE)**: **4.8256 days** (vs. Naive Baseline: 7.4529 days; 35.3% reduction in error).
- **Root Mean Squared Error (RMSE)**: **6.2458 days** (vs. Naive Baseline: 10.1226 days; 38.3% error reduction).
- **Coefficient of Determination ($R^2$)**: **0.3926** (vs. Naive Mean: -0.1015).

### 4. Governance & Usage Guidelines
- Approved for dispatch buffer estimation and logistics alerting.
- Caution: Under extreme adverse weather or carrier labor strikes, actual delay distributions exhibit heavy right tails; users should apply a conservative safety margin of $+3$ days for customer communication.

### Deployment Maturity Level
- **Status**: `CONDITIONALLY_ELIGIBLE_FOR_PILOT`
- **Operational Governance Assessment**: Offline out-of-time test validated (MAE 4.8256 days, R^2 = 0.3926). Conditionally eligible for operational pilot alerting to logistics dispatchers; carrier SLA integration monitoring required.
