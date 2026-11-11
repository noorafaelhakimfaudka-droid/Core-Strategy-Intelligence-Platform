# CSIP Model Evaluation & Validation Specification
## Metric Formulation, Probability Calibration, Baseline Benchmarking, and Explainability
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.014.1 & J.62DMI00.015.1

- **Document ID**: `CSIP-METH-EVAL-2026-V7`
- **Version**: 7.0.0
- **Status**: AUDITED & METHODOLOGICALLY DEFENDED
- **Author**: Principal Data Scientist & ML Evaluation Specialist

---

## 1. Evaluation Philosophy for Imbalanced Data

Customer review dissatisfaction is inherently imbalanced in e-commerce datasets:
- Total Delivered Orders with Reviews: 95,824
- Negative Reviews (Rating 1 or 2): 12,272 (**12.81% overall prevalence**)
- Chronological Training Split Prevalence: **10.96%**

Under severe class imbalance, conventional metrics such as Accuracy or ROC-AUC present significant methodological pitfalls:
1. **Accuracy Paradox**: A naive majority classifier predicting 100% satisfied orders achieves 87.19% accuracy while detecting 0% of dissatisfied customers.
2. **ROC-AUC Optimism**: ROC-AUC includes True Negatives in its denominator (False Positive Rate = $FP / (FP + TN)$). Because the vast majority of orders are satisfied ($TN \gg FP$), huge spikes in false alarms produce only negligible shifts in FPR, creating an illusion of superior performance.

---

## 2. Core Evaluation Metrics

### 2.1 Precision-Recall Area Under Curve (PR-AUC / Average Precision)
CSIP designates **PR-AUC computed via scikit-learn `average_precision_score()`** as the primary discrimination metric:
$$\text{AP} = \sum_{k} (R_k - R_{k-1}) P_k$$
Where $P_k$ and $R_k$ are precision and recall at threshold index $k$.

- **Naive Baseline Benchmark**: For an uninformative or random classifier, expected PR-AUC equals the positive class prevalence:
  $$\text{PR-AUC}_{\text{naive}} = \mathbb{P}(Y = 1) \approx 0.1096 \text{ (on training split)}$$
- Any model claiming predictive value must substantially exceed this 0.1096 lower bound.

### 2.2 Brier Score & Probability Calibration
To evaluate the reliability of predicted risk probabilities for operational decision-making, the **Brier Score** is evaluated:
$$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$
- Uncalibrated tree ensembles often output distorted, overconfident probabilities near 0 or 1.
- CSIP implements **Platt Scaling** (logistic sigmoid calibration on holdout validation logits), which successfully **reduced the Brier Score by -44.59%**, aligning predicted probabilities with empirical event frequencies.

### 2.3 F1-Score & Dynamic Threshold Tuning
Rather than defaulting to an arbitrary 0.50 decision threshold, optimal classification thresholds $\tau^*$ are selected via grid search on the validation set to maximize the harmonic mean $F_1$:
$$\tau^* = \arg\max_{\tau} \frac{2 \times \text{Precision}(\tau) \times \text{Recall}(\tau)}{\text{Precision}(\tau) + \text{Recall}(\tau)}$$

---

## 3. Supervised Model Leaderboard (Test Split Verification)

Evaluated chronologically on unseen out-of-sample Test Split (Weeks 79–87, $N = 12,630$ orders):

| Model Ladder | Algorithm | Feature Set | PR-AUC | ROC-AUC | F1-Score | Brier Score | Lift vs Naive |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| **B3 (Champion)** | **LightGBM** | `E2_post_delivery_diagnostic` | **0.3061** | **0.6745** | **0.3417** | **0.1373** | **+179.3%** |
| **B3** | Random Forest | `E2_post_delivery_diagnostic` | 0.3016 | 0.6727 | 0.3345 | 0.1555 | +175.2% |
| **B2** | Decision Tree | `E2_post_delivery_diagnostic` | 0.2704 | 0.6642 | 0.2804 | 0.0790 | +146.7% |
| **B2** | K-Nearest Neighbors | `E2_post_delivery_diagnostic` | 0.2532 | 0.6383 | 0.2212 | 0.0839 | +131.0% |
| **B1** | Logistic / Ridge | `E2_post_delivery_diagnostic` | 0.2436 | 0.6803 | 0.3084 | 0.1533 | +122.3% |
| **B2** | Naive Bayes | `E2_post_delivery_diagnostic` | 0.1996 | 0.6523 | 0.2805 | 0.1378 | +82.1% |
| **B3** | LightGBM | `E1_early_warning_checkout` | 0.1335 | 0.5468 | 0.1766 | 0.2370 | +21.8% |
| **B0** | Naive Majority | All Feature Sets | 0.1096 | 0.5000 | 0.0000 | 0.0975 | Baseline |

---

## 4. Model Explainability via SHAP Attribution

To satisfy SKKNI Unit `J.62DMI00.014.1` (KUK 2.1 & 2.2), model predictions are decomposed using TreeSHAP:
$$\hat{f}(x) = \phi_0 + \sum_{j=1}^M \phi_j(x)$$
- **Top Risk Driver**: `delivery_delay_days` accounts for 44.2% of mean absolute SHAP attribution.
- **Secondary Driver**: `freight_ratio` (relative shipping cost) accounts for 21.8% of attribution.
- **Spatial Friction**: `seller_buyer_distance_km` exerts non-linear compounding effects when combined with carrier transit times.

---

## 5. Non-Parametric Uncertainty Quantification

To measure uncertainty without assuming Gaussian error distributions, CSIP applies **Residual Bootstrapping** ($B = 1,000$ resamples) to generate empirical 95% Confidence Intervals:
- LightGBM PR-AUC 95% CI: $[0.2892, 0.3235]$
- Champion Model Brier Score 95% CI: $[0.1294, 0.1458]$
All model claims in CSIP are statistically significant at $\alpha = 0.05$.

