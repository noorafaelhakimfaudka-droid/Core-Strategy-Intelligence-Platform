# CSIP V6 Model Evaluation & Diagnostic Review Report

**Document ID**: CSIP-REP-V6-MER-01  
**Author**: Model Evaluation & Explainability Team  
**Standard**: SKKNI 299/2020 [UK-10 Mengevaluasi Hasil Pemodelan]  
**Evaluation Protocol**: Strict Temporal Out-of-Time Test Set (2018-07-01 to 2018-08-31)  
**Date**: November 2026  
**Status**: VERIFIED & REPRODUCIBLE  

---

## 1. Executive Summary

CSIP V6 standardizes model evaluation by adopting **Average Precision (AP)** as the canonical metric for Precision-Recall curves, removing the trapezoidal interpolation distortion that inflated naive baselines in earlier drafts.

Two separate modeling regimes are established:
1. **Task A: Early-Warning Pre-Fulfillment Classification**: Strictly uses variables available at order creation.
2. **Task B: Post-Delivery Diagnostic Satisfaction Modeling**: Uses post-delivery fulfillment metrics for root cause attribution.

---

## 2. Empirical Model Leaderboard (Negative Review Risk)

### A. Validation Set Model Selection (Split: 2018-04-01 to 2018-06-30, $N=19,684$)

| Model ID | Model Family | Feature Set | PR-AUC (AP) | ROC-AUC | F1-Score | Brier Score |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| `B0_naive_majority` | Naive Baseline | Constant Zero | **0.1096** | 0.5000 | 0.0000 | 0.0985 |
| `B0_naive_heuristic` | Rule Heuristic | Delay Threshold (>0) | **0.1883** | 0.5945 | 0.2991 | 0.1016 |
| `B1_logistic` | Regularized GLM | E1 Early Warning Checkout | **0.1850** | 0.6129 | 0.2454 | 0.2402 |
| `B3_lightgbm` | Gradient Boosted Trees | E1 Early Warning Checkout | **0.1899** | 0.6156 | 0.2348 | 0.2380 |
| `B1_logistic` | Regularized GLM | E3 Combined Diagnostic | **0.3134** | 0.7131 | 0.3738 | 0.1630 |
| `B2_decision_tree` | CART Decision Tree | E3 Combined Diagnostic | **0.3316** | 0.7112 | 0.2827 | 0.0847 |
| `B2_knn` | K-Nearest Neighbors | E3 Combined Diagnostic | **0.3192** | 0.6764 | 0.2734 | 0.0893 |
| `B2_naive_bayes` | Gaussian Naive Bayes | E3 Combined Diagnostic | **0.2490** | 0.6740 | 0.3154 | 0.1330 |
| `B3_random_forest` | Random Forest | E3 Combined Diagnostic | **0.3535** | 0.7084 | 0.3909 | 0.1618 |
| `B3_lightgbm` | Gradient Boosted Trees | E3 Combined Diagnostic | **0.3598** | 0.7070 | 0.3857 | 0.1525 |

### B. Locked Holdout Temporal Test Set (Split: 2018-07-01 to 2018-08-31, $N=12,630$)

| Model ID | Feature Set | Task Purpose | PR-AUC (AP) | ROC-AUC | F1-Score | Brier Score |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| `B3_lightgbm` | E1 Early Warning Checkout | Early-Warning (Purchase Stage) | **0.1349** | 0.5438 | 0.1768 | 0.2384 |
| `B1_logistic` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.2436** | 0.6803 | 0.3084 | 0.1533 |
| `B2_decision_tree` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.2704** | 0.6642 | 0.2804 | 0.0790 |
| `B2_knn` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.2532** | 0.6383 | 0.2212 | 0.0839 |
| `B2_naive_bayes` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.1996** | 0.6523 | 0.2805 | 0.1378 |
| `B3_random_forest` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.3016** | 0.6727 | 0.3345 | 0.1555 |
| `B3_lightgbm` | E3 Combined Diagnostic | Post-Delivery Diagnosis | **0.3061** | 0.6745 | 0.3417 | 0.1373 |

---

## 3. Scientific Insights
1. **Unbiased Baseline Confirmation**: The naive baseline PR-AUC on validation split is exactly $0.1096$, precisely matching the positive class prevalence in that temporal window.
2. **Early-Warning Difficulty**: Predicting customer dissatisfaction strictly at checkout achieves PR-AUC $= 0.1349$ on the test set, reflecting the genuine real-world difficulty of forecasting customer perception weeks before fulfillment occurs.
3. **Fulfillment Driver Dominance**: Incorporating actual delivery delay and lead time boosts test PR-AUC to $0.3061$ ($+127\%$ relative increase), confirming that fulfillment execution—not checkout cart value—is the primary driver of e-commerce dissatisfaction.
