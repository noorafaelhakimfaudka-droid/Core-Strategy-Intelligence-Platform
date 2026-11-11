# CSIP Population Definition, Selection Bias, and Label Observability
## Rigorous Methodological Audit of Analytical Population and Survivor Bias
### Reference Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.005.1 & J.62DMI00.007.1

- **Document ID**: `CSIP-METH-POP-BIAS-2026-V7`
- **Version**: 7.0.0
- **Lead Author**: Principal Data Scientist & Research Methodologist
- **Status**: AUDITED & METHODOLOGICALLY VERIFIED

---

## 1. Executive Summary

A critical requirement in observational Data Science is defining the **analytical target population** and identifying any **selection bias** introduced during data cleaning and filtering. 

In CSIP, data cleaning applies a default filter:
$$\text{order\_status} == \text{'delivered'}$$
This document provides a thorough audit of the population funnel, quantifies the effect of excluding non-delivered orders, formalizes the exact estimand, and documents the handling of unobserved customer reviews.

---

## 2. The Population Funnel Breakdown

The complete intake funnel from the raw Brazilian e-commerce dataset (Olist) to the supervised modeling population is quantified below:

| Funnel Stage | Subpopulation / Status | Order Count | % of Raw Intake | Observability Rate | Negative Prevalence |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **Stage 0: Raw Intake** | All placed orders | 99,441 | 100.00% | 99.19% | 14.78% |
| **Stage 1: Fulfillment Status** | Delivered (`status == 'delivered'`) | 96,478 | 97.02% | 99.33% | 12.81% |
| | Canceled (`status == 'canceled'`) | 625 | 0.63% | 97.44% | 87.19% |
| | Unavailable / Stockout (`status == 'unavailable'`) | 609 | 0.61% | 98.03% | 87.60% |
| | Shipped / In-Transit (`status == 'shipped'`) | 1,107 | 1.11% | 94.22% | 63.09% |
| | Processing / Invoiced / Created / Approved | 622 | 0.63% | 98.71% | 18.08% |
| **Stage 2: Chronological Integrity** | Delivered with valid timestamps ($t_{\text{del}} \ge t_{\text{pur}}$) | 96,447 | 96.99% | 99.33% | 12.81% |
| **Stage 3: Analytical Dataset** | Cleaned & joined with items, payments, geolocation | 96,470 | 97.01% | 99.33% | 12.81% |
| **Stage 4: Supervised Labeling** | Orders with Observed Reviews (`has_observed_review == 1`) | 95,824 | 96.36% | 100.00% | 12.81% |
| | Orders with Missing Reviews (`has_observed_review == 0`) | 646 | 0.65% | 0.00% | N/A (NaN) |

---

## 3. The Target Estimand and Survivor Bias Analysis

### 3.1 Formal Estimand Specification
When training supervised models on delivered orders, the model does NOT estimate unconditional customer dissatisfaction across all placed checkouts. Instead, it estimates the **conditional expectation**:

$$\theta(x) = \mathbb{P}\left(Y_{\text{negative}} = 1 \mid X = x, \text{Status} = \text{'delivered'}\right)$$

### 3.2 Survivor Bias Mechanisms
1. **Extreme Dissatisfaction in Non-Delivered Orders**:
   - As shown in empirical audit table `LABEL_OBSERVABILITY_AUDIT.csv`, orders with status `canceled` (625) and `unavailable` (609) have an extraordinary negative review rate of **87.2%** and **87.6%**, respectively.
   - Customers whose orders were canceled or experienced inventory stockouts frequently leave severe 1-star complaints regarding non-delivery and unresponsiveness.
2. **Impact of `status_filter="delivered"`**:
   - By filtering for delivered orders, exactly **1,234 catastrophic failure orders** (canceled + unavailable) are excluded from the training set.
   - Consequently, the observed negative review rate drops from **14.78%** across all orders to **12.81%** in the delivered subset.
3. **Scientific Justification for Retention of Filter**:
   - While excluding canceled orders introduces survivor bias, it is methodologically essential for satisfaction modeling:
     - The underlying failure mechanics are fundamentally different. Cancellations are caused by merchant inventory stockouts, payment rejection, or buyer cancellation. Delivered dissatisfaction is driven by transit delays, freight burden, product expectation mismatch, and packaging damage.
     - Mixing unfulfilled orders into a logistics delay model creates severe missing-variable bias, because delivery duration ($t_{\text{delivered}} - t_{\text{purchase}}$) is mathematically undefined for orders that were never delivered!
4. **Generalization Boundary & Operational Disclaimer**:
   > **IMPORTANT**: The early-warning checkout model (`E1_early_warning_checkout`) must be interpreted as predicting the *conditional risk of delivery dissatisfaction given that fulfillment is completed*. It must NOT be used as a predictor for inventory stockout or merchant cancellation.

---

## 4. Audit of Unobserved Reviews (Missing Label Integrity)

### 4.1 Missingness Profile
- In the cleaned delivered cohort ($N = 96,470$), exactly **646 orders (0.67%)** have no recorded customer review.
- Missingness is predominantly Missing at Random (MAR) associated with platform survey dispatch drops or customers who ignored the email survey.

### 4.2 Rejection of Synthetic Label Imputation
- In some naive pipelines, missing reviews are imputed as a neutral score 3 (`review_score = 3`), or assumed to be satisfied (`negative_review_flag = 0`).
- **CSIP Methodological Ruling**: Synthetic imputation of unobserved reviews is strictly prohibited:
  - Imputing missing reviews as positive (0) artificially suppresses the true dissatisfaction rate by 0.67%.
  - Imputing as neutral (3) distorts score variance and invalidates ordinal calibration.
- **V7 Implementation**:
  - `has_observed_review` is explicitly encoded as `0` for these 646 orders.
  - `negative_review_flag` is explicitly set to `np.nan`.
  - All supervised model training pipelines filter strictly via:
    ```python
    df_supervised = df[df["has_observed_review"] == 1]
    ```
  - This guarantees **zero synthetic label contamination** in the ground-truth training and evaluation sets.

---

## 5. Summary and Methodological Governance

1. **Estimand Integrity**: The CSIP dissatisfaction model strictly estimates $\mathbb{P}(Y = 1 \mid X, \text{Delivered} = 1)$.
2. **Survivor Bias Acknowledged**: Canceled/unavailable orders (1.24% of intake, 87.4% negative) are documented as excluded due to non-comparable fulfillment mechanics.
3. **Label Purity**: 646 unobserved reviews are preserved as NaN, ensuring 100% authentic ground-truth labels for all model metrics.
