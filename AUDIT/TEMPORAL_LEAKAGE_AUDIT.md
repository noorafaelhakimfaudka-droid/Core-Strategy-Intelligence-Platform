> [HISTORICAL ARCHIVE] - This document is preserved as an unedited historical audit record from previous versions.

# CSIP V14 TEMPORAL DATA INTEGRITY & LEAKAGE DEFENSE AUDIT
## Comprehensive Forensic Verification of Temporal Boundaries & Zero-Leakage Architecture

### 1. Executive Summary & Architectural Mandate

In predictive machine learning on transactional e-commerce data, **data leakage** is the most pervasive threat to empirical validity. Leakage occurs when information from the future (post-decision or post-outcome events) inadvertently enters the feature space used by a model at inference time.

To guarantee zero look-ahead bias and ensure production fidelity, the CSIP platform enforces the **Temporal & Feature Isolation Protocol**. This protocol strictly segregates the operational feature space into three mutually exclusive prediction horizons:

```
Timeline:  [ Order Purchase / Checkout ] -------> [ Order Delivered ] -------> [ Review Completed / Subsequent Purchase ]
                        |                                    |                                       |
Context:         CONTEXT A                            CONTEXT B                               CONTEXT C
           (Checkout-Time Prediction)        (Post-Delivery Fulfillment)             (Retrospective Diagnosis)
Features:  Item price, freight ratio,        Actual delivery lead time,              Review comment text,
           seller distance, estimated lead   delay days, late delivery flag,         survey ratings, repeat purchase
           time, historical prior orders.    transit duration.                       timing (TARGETS / AUDIT ONLY).
```

---

### 2. Horizon Definitions & Operational Contracts

#### Context A: Checkout-Time Prediction (Early Warning / Retrospective Conditional)
- **Target Audience / Decision Owner**: E-commerce Checkout Engine, Risk Underwriting, Customer Support Triage.
- **Prediction Timestamp**: Order creation/approval timestamp (`order_approved_at`).
- **Permissible Feature Set**: Strictly limited to attributes known before fulfillment commences:
  - `total_item_price`, `total_freight`, `total_order_value`, `freight_ratio`
  - `item_count`, `payment_installments_max`, `seller_buyer_distance_km`
  - `estimated_lead_time_days`, `distance_x_weight`
  - `prior_order_count` (strictly computed from orders placed prior to the current order timestamp).
- **Strictly Prohibited**: Actual delivery timestamp (`order_delivered_customer_date`), actual delay (`delivery_delay_days`), carrier shipping duration, and customer review scores.
- **Model Key**: `E1_checkout_retrospective_conditional` / `best_early_warning_review_lightgbm`.

#### Context B: Post-Delivery Fulfillment Prediction
- **Target Audience / Decision Owner**: Logistics Operations, Post-Purchase Retention & Re-engagement Team.
- **Prediction Timestamp**: Customer delivery timestamp (`order_delivered_customer_date`).
- **Permissible Feature Set**: Context A features PLUS fulfillment outcomes:
  - `delivery_lead_time_days`
  - `delivery_delay_days`
  - `is_late`
  - `delay_x_freight_ratio`
  - `high_value_late_flag`
- **Population Isolation**: To eliminate pre-delivery repeat contamination, this population strictly isolates customers whose subsequent purchase occurred *after* delivery (`repeat_before_delivery_flag == 0`) and who have at least a 90-day observation window (`is_censored_post_delivery == 0`).
- **Model Key**: `best_repeat_purchase_post_delivery_lightgbm`.

#### Context C: Retrospective Analytical Diagnosis
- **Target Audience / Decision Owner**: Principal Data Scientist, Executive Strategy, Policy Formulators.
- **Prediction Timestamp**: N/A (Offline retrospective causal and associative auditing).
- **Attributes**: Survey ratings (`review_score`), Portuguese text feedback (`review_comment_message`), customer cohort lifetime reorder history.
- **Governing Constraint**: These variables are **targets or observational outcome labels**, never features for prospective operational prediction.

---

### 3. Forensic Leakage Audit Checklist & Results

| Audit Area | Potential Failure Mode | Prevention Mechanism | Empirical Verification Status |
| :--- | :--- | :--- | :---: |
| **Temporal Embargo Splits** | Contamination across train and test boundaries due to overlapping order lifecycles | 90-day time buffer (embargo) between train end (2017-08-31) and validation start (2017-12-01), and between validation end (2018-01-31) and test start (2018-05-01). | **VERIFIED** |
| **Target Leakage** | Outcome labels (`negative_review_flag`, `repeat_purchase_flag`) entering feature matrices | Pre-training schema assert ensures target columns and raw review ratings are removed prior to `fit()`. | **VERIFIED** |
| **Entity Contamination** | Same customer appearing in both train and test splits with different orders | Customers are partitioned by the timestamp of their *first* observed order (`first_order_timestamp`). All subsequent orders for that customer remain in the originating split. | **VERIFIED** |
| **Preprocessing Leakage** | Scalers or imputers fitted on combined train + validation + test data | Scikit-learn Pipelines (`get_model_pipeline()`) fit `StandardScaler` strictly on `X_train` during `fit()` and apply `transform()` to validation and test sets. | **VERIFIED** |
| **Right-Censoring Bias** | Under-counting repeat purchases for orders placed near the end of dataset | 90-day post-delivery censoring mask (`is_censored_post_delivery`). Orders with less than 90 days of observation prior to dataset cutoff are excluded from evaluation. | **VERIFIED** |
| **Pre-Delivery Repeat Bias** | Customers reordering while order #1 is still in transit counted as fulfillment response | Explicit separation via `repeat_before_delivery_flag` (962 customers). The post-delivery model strictly trains on non-pre-delivery reorders. | **VERIFIED** |

---

### 4. Automated Regression Tests

The integrity of this protocol is verified continuously by:
- `tests/test_feature_leakage.py`
- `tests/test_v12_remediation.py`
- `tests/test_temporal_leakage.py`

All tests execute cleanly and enforce zero tolerance for look-ahead violations.
