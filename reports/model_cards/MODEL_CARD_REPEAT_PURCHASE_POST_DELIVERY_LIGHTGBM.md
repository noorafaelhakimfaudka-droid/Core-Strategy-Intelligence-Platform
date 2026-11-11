# MODEL CARD: Repeat Purchase Post-Delivery Fulfillment Champion (Context B)
## CSIP Machine Learning Governance & Honest Evaluation Artifact

### 1. Model Details
- **Model Name**: Post-Delivery Repeat Purchase Classifier (LightGBM)
- **Artifact Path**: `artifacts/models/best_repeat_purchase_post_delivery_lightgbm.joblib`
- **Metadata Sidecar**: `artifacts/models/best_repeat_purchase_post_delivery_lightgbm.joblib.json`
- **Model Type**: Gradient Boosted Decision Tree (`LGBMClassifier`)
- **Version**: 17.0.0
- **Release Date**: November 2026
- **Governance Decision**: **QUALIFIED RESEARCH BENCHMARK (LEVEL L1 PREDICTIVE)**

### 2. Operational & Business Context
- **Operational Scope**: Post-delivery retention modeling. Evaluates whether fulfillment quality (delivery lead time, shipping delays, logistics friction) informs the likelihood of reordering within 90 days of order receipt.
- **Population Isolation**: Strictly isolates customers whose reorders occurred *after* delivery (`repeat_before_delivery_flag == 0`) and who possess a complete 90-day observation window (`is_censored_post_delivery == 0`).

### 3. Quantitative Evaluation (Clean Locked Test Set: $N_{test} = 4,232$)
- **Training Population**: Clean post-delivery historical cohort ($N_{train} = 21,324$).
- **Test Samples**: 4,232 orders with verified delivery and 90-day observation window.
- **PR-AUC**: **0.0245** (vs. Naive Baseline: **0.0201**).
- **ROC-AUC**: **0.5284** (95% Bootstrap CI: [0.491, 0.564]).
- **Key Observation**: While post-delivery fulfillment features provide a slight directional lift over checkout-time features, the 95% bootstrap CI still touches chance level, emphasizing that customer repeat purchases in this marketplace are driven predominantly by external replacement needs rather than platform delivery speed.

### 4. Governance Limitations & Deployment Recommendations
- Not recommended for high-stakes automated budget allocations.
- May be utilized as an observational signal in post-purchase satisfaction surveys or win-back retention pilot cohorts.

### Deployment Maturity Level
- **Status**: `RESEARCH_ONLY`
- **Operational Governance Assessment**: Post-delivery cohort behavior benchmark (PR-AUC 0.0245, ROC-AUC 0.5284). Retained strictly for empirical comparison and longitudinal customer behavior research.
