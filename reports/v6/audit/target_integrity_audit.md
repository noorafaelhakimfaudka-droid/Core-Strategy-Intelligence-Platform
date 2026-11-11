# CSIP V6 Target Construction & Label Integrity Audit

**Auditor**: Statistical Validation Specialist & Data Quality Auditor  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Ground Truth Contamination Analysis

### Finding F-02 Verification
In `src/csip/features/engineer.py`, lines 204-207:
```python
df["review_score"] = df["review_score"].fillna(3).astype(np.int8)
df["has_review_comment"] = df["has_review_comment"].fillna(0).astype(np.int8)
df["negative_review_flag"] = (df["review_score"] <= 2).astype(np.int8)
```

### Empirical Measurement of Missingness
- Total delivered orders: **96,470**
- Orders with observed review: **95,824 (99.33%)**
- Orders with unobserved/missing review: **646 (0.67%)**
- Breakdown of observed reviews:
  - Score 5: 56,742 (59.22%)
  - Score 4: 18,894 (19.72%)
  - Score 3: 7,916 (8.26%)
  - Score 2: 2,919 (3.05%)
  - Score 1: 9,353 (9.76%)
  - Missing (NaN): 646 (0.67%)

### Scientific Impact
1. Missing reviews are **Missing Completely at Random / Missing at Random** (unsubmitted feedback surveys). Imputing them as neutral (3.0) and assigning `negative_review_flag = 0` creates **label noise**: we assume an unsubmitted survey is a satisfied/neutral customer.
2. In supervised learning, when the target is unobserved, the standard scientific protocol is **complete case analysis on the eligible target population**:
   $$\mathcal{D}_{\text{eligible}} = \{ (x_i, y_i) \mid y_i \text{ is observed} \}$$
3. True negative review count: $2,919 + 9,353 = 12,272$ orders.
4. Correct prevalence:
   $$\text{Prevalence} = \frac{12,272}{95,824} = 12.8068\% \approx 12.81\%$$
   (V5 reported $12,272 / 96,470 = 12.72\%$ due to denominator contamination).

---

## 2. Target Remediation Plan
1. In `engineer.py`, preserve `review_score` as nullable float or integer with NaN.
2. Create an explicit boolean mask `has_observed_review`.
3. In `trainer.py`, filter training and evaluation datasets to `has_observed_review == True` when training review models.
4. Document the 646 excluded orders in data cleaning reports.
