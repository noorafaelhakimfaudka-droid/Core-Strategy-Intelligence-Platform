# CSIP Changelog — Version 6.0.0 (Scientific Integrity & Methodological Remediation)

## Release Overview
CSIP Version 6.0.0 represents a comprehensive scientific and methodological overhaul of the Core Strategy & Intelligence Platform, resolving critical audit findings regarding prediction horizons, target contamination, evaluation metrics, and state-space transition modeling.

---

## Detailed Summary of Changes

### 1. Data Pipeline & Target Integrity (Finding F-02)
- **Problem**: Missing customer reviews (646 orders, 0.67%) were imputed as neutral (3.0) and flagged as non-negative, contaminating the ground-truth target.
- **Remediation**: Implemented strict population filtering (`has_observed_review == 1`). Unobserved reviews are preserved as NaN, separating unsubmitted feedback surveys from observed ratings. True class prevalence recalculated at 12.81%.

### 2. Feature Availability & Anti-Leakage Governance (Finding F-01)
- **Problem**: The early-warning review model used fulfillment delay and delivery lead time features that are unobserved at order checkout time.
- **Remediation**: Bifurcated modeling into Task A (Early-Warning Pre-Fulfillment Model, strictly checkout variables) and Task B (Post-Delivery Diagnostic Satisfaction Model). Created authoritative Feature Availability Registry. Updated `tests/test_feature_leakage.py` to inspect real trainer feature sets.

### 3. Model Evaluation & Unbiased Metrics (Finding F-03)
- **Problem**: Trapezoidal integration of Precision-Recall curves produced an artificial PR-AUC of 0.5545 for constant naive baseline predictors.
- **Remediation**: Adopted scikit-learn's `average_precision_score()`. Naive baseline PR-AUC corrected to 0.1096 (exact positive prevalence). Distinct validation leaderboard (model selection) and locked test set (out-of-time evaluation) generated.

### 4. World Model & Out-of-Sample Holdout (Finding F-04)
- **Problem**: World state transition model docstring claimed estimation of action parameters $A_t$, while the implementation was an autoregressive state model with ad-hoc intervention offsets. Historical backtesting was conducted in-sample.
- **Remediation**: Clarified docstrings and formulas ($S_{t+1} = C + \Phi S_t + \varepsilon_t$), removing unsupported causal claims. Implemented chronological holdout validation (Train: weeks 1-64, Test: weeks 65-87) with out-of-sample WAPE reported (Volume: 19.85%, Review Rate: 27.17%).

### 5. Automated Testing & Verification Suite
- Expanded test suite to **87 comprehensive tests** (all 87 passed in 22.76s).
- Added explicit tests for target label non-contamination, real feature set anti-leakage, and world model holdout backtesting.
- Zero local absolute paths (`C:\Users\...`) across all repository files.
