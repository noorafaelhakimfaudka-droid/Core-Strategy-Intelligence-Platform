# CSIP Prediction Contract Specification
## Formal Temporal Boundaries, Target Definitions, and Population Eligibility
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.002.1 & J.62DMI00.007.1

- **Document ID**: `CSIP-DOC-PRED-CONTRACT-2026-V7`
- **Version**: 7.0.0
- **Status**: APPROVED & METHODOLOGICALLY DEFENDED
- **Author**: Principal Data Scientist & ML Systems Architect

---

## 1. Purpose and Governance

To prevent data leakage, target contamination, and unstated selection bias, this document establishes the **binding prediction contract** for all machine learning models in the Core Strategy & Intelligence Platform (CSIP). 

Any feature utilized in model training or real-time inference MUST strictly satisfy the temporal availability constraints defined herein. Violations of this contract constitute methodological defects.

---

## 2. Model 1: Early-Warning Customer Dissatisfaction Prediction (`E1_early_warning_checkout`)

### 2.1 Problem Formulation & Objectives
- **Business Objective**: Proactively identify high-risk transactions at the moment of customer checkout to initiate immediate operational mitigations (e.g., priority warehouse dispatch, proactive communication, packaging upgrades) before fulfillment failures occur.
- **Technical Objective**: Supervised binary classification predicting whether an order will result in a negative customer review ($Y \in \{0, 1\}$).
- **Formal Estimand**: 
  $$\mathbb{P}(Y_{\text{negative}} = 1 \mid X_{t_0}, \text{Delivered} = 1)$$
  *Note*: Because review collection surveys are administered only upon delivery confirmation, the empirical model estimates the conditional risk of dissatisfaction among fulfilled orders.

### 2.2 Temporal and Information Boundaries
- **Unit of Analysis (Grain)**: Single e-commerce order (`order_id`).
- **Prediction Timestamp ($t_0$)**: Exactly `order_purchase_timestamp` (the millisecond the customer places the order).
- **Feature Availability Window**: Strictly $t \le t_0$.
- **Outcome Window**: Review submission date ($t_{\text{review}} \ge t_{\text{delivered}} > t_0$).

### 2.3 Permitted Feature Schema ($t \le t_0$)
The feature set `E1_early_warning_checkout` is restricted exclusively to features known at checkout:

| Feature Name | Description | Source / Formula | Timing Verification |
| :--- | :--- | :--- | :--- |
| `total_item_price` | Sum of item prices in basket | `items.sum('price')` | Fixed at checkout |
| `total_freight` | Total shipping fee charged | `items.sum('freight_value')` | Fixed at checkout |
| `total_order_value` | Total monetary spend | `total_item_price + total_freight` | Fixed at checkout |
| `freight_ratio` | Shipping fee proportion of spend | `total_freight / total_order_value` | Fixed at checkout |
| `item_count` | Number of items in order | `items.count()` | Fixed at checkout |
| `payment_installments_max` | Maximum installment plan chosen | `payments.max('installments')` | Selected at checkout |
| `seller_buyer_distance_km` | Spatial Haversine distance | Computed from buyer and seller zip coordinates | Geolocation known at checkout |
| `estimated_lead_time_days` | SLA promised delivery horizon | `(order_estimated_delivery_date - order_purchase_timestamp)` | Promoted to customer at checkout |
| `distance_x_weight` | Logistics friction interaction | `seller_buyer_distance_km * log1p(weight_g)` | Weight catalog known at checkout |
| `prior_order_count` | Historical purchases by customer | Count of prior orders with `order_purchase_timestamp < t_0` | Point-in-time historical state |

### 2.4 Prohibited Features at Checkout ($t > t_0$)
The following attributes occur strictly after $t_0$ and are **strictly forbidden** from `E1_early_warning_checkout`:
1. `order_approved_at` / `approval_lag_hours`: Payment authorization occurs asynchronously (mean lag $\approx 10.2$ hours; up to 48 hours for boleto bancário). At $t_0$, approval status is unobserved.
2. `order_delivered_carrier_date`: Dispatch to carrier.
3. `order_delivered_customer_date` / `delivery_lead_time_days`: Fulfillment arrival.
4. `delivery_delay_days` / `is_late`: Actual SLA compliance.
5. `review_score` / `review_comment_message`: Post-delivery customer feedback.

### 2.5 Target Variable & Observability
- **Target Name**: `negative_review_flag`
- **Definition**: Binary indicator where:
  $$Y = \begin{cases} 1, & \text{if } \text{review\_score} \in \{1, 2\} \\ 0, & \text{if } \text{review\_score} \in \{4, 5\} \\ \text{NaN}, & \text{if } \text{review\_score} = 3 \text{ or missing} \end{cases}$$
- **Supervised Training Filter**: `has_observed_review == 1 & negative_review_flag.notnull()`.
- **Prevalence**: 12.81% positive rate in observed population (10.96% in chronologically ordered training split).

---

## 3. Model 2: Post-Delivery Diagnostic Dissatisfaction Attribution (`E2` / `E3`)

### 3.1 Problem Formulation & Objectives
- **Business Objective**: Perform root-cause attribution and diagnostic analysis to explain why delivered orders failed customer expectations.
- **Technical Objective**: Supervised classification and SHAP attribution identifying the relative marginal contributions of fulfillment delays, freight pricing, and payment friction.
- **Prediction Timestamp ($t_1$)**: Order delivery timestamp (`order_delivered_customer_date`).
- **Feature Availability Window**: Strictly $t \le t_1$.

### 3.2 Permitted Features ($t \le t_1$)
In addition to all checkout features ($t \le t_0$), diagnostic models may utilize operational realization metrics:
- `approval_lag_hours`: Elapsed time from purchase to payment approval.
- `delivery_lead_time_days`: Elapsed time from purchase to delivery.
- `delivery_delay_days`: Difference between actual delivery and promised SLA date ($t_{\text{delivered}} - t_{\text{estimated}}$).
- `is_late`: Indicator if delivery was delayed beyond SLA.
- `delay_x_freight_ratio`: Interaction term capturing compounding friction of expensive delayed shipping.
- `high_value_late_flag`: High-ticket items that suffered delivery failure.

---

## 4. Model 3: First-Order Customer Cohort 90-Day Retention (`customer_cohort`)

### 4.1 Problem Formulation & Objectives
- **Business Objective**: Predict customer lifetime value potential and 90-day repeat purchase probability based exclusively on their initial onboarding transaction.
- **Technical Objective**: Supervised binary classification of 90-day repurchase ($Y_{\text{repeat}} \in \{0, 1\}$).
- **Formal Estimand**: 
  $$\mathbb{P}(T_{\text{order2}} - T_{\text{order1}} \le 90 \text{ days} \mid X_{\text{order1}}, T_{\text{order1}} \le T_{\max} - 90 \text{ days})$$

### 4.2 Temporal and Information Boundaries
- **Unit of Analysis (Grain)**: Unique customer (`customer_unique_id`).
- **Prediction Timestamp ($t_{\text{cohort}}$)**: The timestamp of the customer's *first ever completed order* ($T_{\text{order1}}$).
- **Feature Source**: Strictly attributes belonging to Order 1.
- **Prohibited Sources**:
  - Any feature from subsequent orders (Order 2, Order 3, etc.).
  - Lifetime summary aggregates (`lifetime_order_count`, `lifetime_total_spend`, `lifetime_avg_review`) which inherently leak future transactions.
- **Right-Censoring Mitigation**:
  - Customers whose first purchase occurred within 90 days of the dataset maximum date ($T_{\max} - 90 \text{ days}$) are excluded from evaluation because their 90-day observation window was truncated.

---

## 5. Model 4: World Model Autoregressive State Transition (VAR)

### 5.1 Formulation & Objectives
- **Objective**: Simulate macro-level platform state evolution across weekly epochs to evaluate system stability and policy scenarios.
- **Mathematical Specification**:
  $$S_{t+1} = C + \Phi S_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Sigma)$$
- **State Vector ($S_t \in \mathbb{R}^4$)**:
  1. `weekly_order_volume` (total order throughput)
  2. `mean_delivery_delay` (average delay in days)
  3. `mean_freight_ratio` (average shipping cost share)
  4. `negative_review_rate` (proportion of dissatisfied orders)
- **Temporal Alignment**:
  - $S_t$: System aggregates from Week $t$ (Sunday 00:00 to Saturday 23:59).
  - $S_{t+1}$: System aggregates from Week $t+1$.
- **Out-of-Sample Holdout Protocol**:
  - Fit on Weeks 1–64; validated out-of-sample on Weeks 65–87.
- **Non-Causal Governance**:
  - State simulations represent structural sensitivity projections under historical autoregressive dynamics, **NOT causal treatment effects**.

---

## 6. Target Population & Inclusion/Exclusion Funnel

| Funnel Stage | Criteria | Row Count | Percentage |
| :--- | :--- | ---: | ---: |
| **Raw Ingested Orders** | All records in `olist_orders_dataset.csv` | 99,441 | 100.00% |
| **Delivered Status Filter** | `order_status == 'delivered'` | 96,478 | 97.02% |
| **Chronological Anomaly Filter** | `order_delivered_customer_date >= order_purchase_timestamp` | 96,455 | 97.00% |
| **Non-Null Delivery Date** | `order_delivered_customer_date.notnull()` | 96,447 | 96.99% |
| **Matched to Clean Items** | Order has valid items, payments, and geographic data | 96,470 | 97.01% |
| **Observed Review Feedback** | Customer submitted review survey (`has_observed_review == 1`) | 95,824 | 96.36% |
| **Unambiguous Polar Target** | `review_score` in {1, 2} (negative) or {4, 5} (positive) | 86,225 | 86.71% |

### Selection Bias Disclosure
- **Canceled & Unavailable Orders (2.99%)**: Canceled orders never reach delivery, hence customer review surveys are not triggered. The dissatisfaction model cannot be used to predict order cancellations.
- **Unobserved Reviews (0.67%)**: Orders with missing review records are excluded from supervised binary classification rather than imputed, ensuring zero synthetic label contamination.

---

## 7. Verification and Enforcement

Compliance with this Prediction Contract is verified by automated regression tests in `tests/test_feature_leakage.py`:
- `test_checkout_stage_restricted_features()`: Asserts that `E1_early_warning_checkout` has zero overlap with restricted post-checkout columns.
- `test_target_label_integrity_and_zero_contamination()`: Confirms unobserved reviews are preserved as NaN.
- `test_processed_customer_cohort_zero_leakage()`: Verifies absence of lifetime summary features.
- `test_future_perturbation_invariance()`: Verifies that future order modifications leave prior-order features invariant.
