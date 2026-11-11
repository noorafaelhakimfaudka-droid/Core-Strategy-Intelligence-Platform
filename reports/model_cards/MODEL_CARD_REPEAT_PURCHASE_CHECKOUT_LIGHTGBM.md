# MODEL CARD: Repeat Purchase Checkout LightGBM (First-Order Features)
## CSIP Machine Learning Governance & Honest Evaluation Artifact

### 1. Model Details
- **Model Name**: Checkout Repeat Purchase Classifier (LightGBM)
- **Artifact Path**: `artifacts/models/best_repeat_purchase_lightgbm.joblib`
- **Metadata Sidecar**: `artifacts/models/best_repeat_purchase_lightgbm.joblib.json`
- **Model Type**: Gradient Boosted Decision Tree (`LGBMClassifier`)
- **Version**: 17.0.0
- **Release Date**: November 2026
- **Governance Decision**: **NOT SUITABLE FOR OPERATIONAL DEPLOYMENT (REJECTED)**

### 2. Operational & Business Context
- **Hypothesized Use**: Predict whether a new customer placing their first order will return to make another purchase within 90 days, enabling personalized checkout incentives or onboarding campaigns.
- **Empirical Reality**: The model demonstrates **no statistically distinguishable discriminative ability** over random chance on unseen holdout test data.

### 3. Quantitative Evaluation (Locked Test Set: $N_{test} = 13,175$)
- **PR-AUC**: **0.0202** (Empirical Base Rate: 0.0237; underperforms simple prior rate).
- **ROC-AUC**: **0.5021**
- **95% Bootstrap Confidence Interval**: **[0.4719, 0.5314]**
- **Statistical Significance vs. Chance (0.50)**: **NOT SIGNIFICANT** (`spans_chance = 1.0`, `statistically_distinguishable = 0.0`).
- **Brier Score**: 0.1670 (vs. Naive Baseline: **0.0231**; severely degraded due to class imbalance reweighting).

### 4. Root Cause & Scientific Analysis
1. **Severe Natural Sparsity**: The Olist e-commerce platform exhibits a ~97% one-time buyer pattern. Across the entire dataset, only ~3% of customers ever place a second order.
2. **Feature Informativeness at Checkout**: Basket-level transactional variables observable at checkout (e.g. `total_item_price`, `freight_ratio`, `payment_installments_max`, `seller_buyer_distance_km`) carry essentially zero mutual information with long-term brand loyalty or repeat purchasing behavior.
3. **Censoring and Attrition**: Customers without an immediate need for catalog replacement will not repurchase regardless of checkout friction or basket size.

### 5. Architectural & Governance Action
- In accordance with **Governing Principles (Rule 2 & Rule 5)**:
  - We refuse to fabricate synthetic features or manipulate random seeds to artificially boost test metrics.
  - This model is formally documented as an **Empirical Negative Finding**.
  - It is **REJECTED** for automated operational decision-making. Platform resources should instead focus on post-delivery customer retention interventions (Context B).

### Deployment Maturity Level
- **Status**: `RESEARCH_ONLY`
- **Operational Governance Assessment**: Checkout-time basket prediction benchmark. Formally REJECTED for operational deployment due to 95% bootstrap confidence interval [0.472, 0.531] spanning chance baseline 0.50 (ROC-AUC 0.5021). Valid negative finding.
