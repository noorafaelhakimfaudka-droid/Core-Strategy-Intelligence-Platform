# CSIP V6 Feature Leakage & Point-in-Time Availability Audit

**Auditor**: Data Quality & Leakage Auditor  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Feature Availability Matrix & Point-in-Time Audit

| Feature Name | Source Table | Point-in-Time Availability | Early-Warning (Purchase) | Post-Delivery Diagnostic | Leakage Risk in Early-Warning |
|:---|:---|:---:|:---:|:---:|:---:|
| `total_item_price` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `total_freight` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `total_order_value` | Computed | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `freight_ratio` | Computed | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `item_count` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `payment_installments_max` | `order_payments` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `payment_type_primary` | `order_payments` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `seller_buyer_distance_km` | `geolocation` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `approval_lag_hours` | `orders` | Order Approval ($t_{\text{app}}$) | **CONDITIONAL** | **ELIGIBLE** | Low (only if post-approval) |
| `estimated_lead_time_days` | `orders` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None (Estimated at purchase) |
| `delivery_lead_time_days` | `orders` | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `delivery_delay_days` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `is_late` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `delay_x_freight_ratio` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `high_value_late_flag` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `review_score` | `order_reviews` | Review Creation ($t_{\text{rev}}$) | **TARGET / PROHIBITED** | **TARGET / PROHIBITED** | **DIRECT TARGET LEAKAGE** |

---

## 2. Test Suite Vulnerability Analysis
- In `tests/test_feature_leakage.py`, `test_checkout_stage_restricted_features()` asserted:
  ```python
  checkout_features = [
      "total_item_price", "total_freight", "freight_ratio",
      "item_count", "payment_installments_max",
      "seller_buyer_distance_km", "approval_lag_hours"
  ]
  leakage_cols = set(checkout_features).intersection(restricted_cols)
  assert len(leakage_cols) == 0
  ```
- This test passed because it defined a dummy list! It did not verify what `ModelExperimentTrainer.FEATURE_SETS` was actually feeding into scikit-learn models.
- **Action**: The test must be refactored to inspect `ModelExperimentTrainer.EARLY_WARNING_FEATURES` directly.
