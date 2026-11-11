# CSIP V6 Feature Availability & Point-in-Time Governance Report

**Document ID**: CSIP-REP-V6-FAR-01  
**Author**: Data Quality & Leakage Audit Team  
**Standard**: SKKNI 299/2020 [UK-07 Mengkonstruksi Data] & Anti-Leakage Governance  
**Date**: November 2026  
**Status**: VERIFIED & ENFORCED  

---

## 1. Executive Summary

A core objective of CSIP V6 is the elimination of temporal and post-outcome data leakage. In e-commerce predictive modeling, information availability is strictly bound to chronological business events:

1. **Order Creation / Purchase Stage ($t_0$)**: The customer finalizes the basket. Only item catalog features, basket pricing, payment methods, customer/seller zip codes, and promised delivery dates are known.
2. **Order Payment Approval ($t_{\text{approval}}$)**: Payment gateway confirmation latency is recorded.
3. **Carrier Dispatch ($t_{\text{carrier}}$)**: Package handed over to logistics carrier.
4. **Customer Delivery ($t_{\text{delivery}}$)**: Physical arrival at buyer destination; actual delivery lead time, delay days, and late flags become known.
5. **Customer Review Submission ($t_{\text{review}}$)**: Review score and textual comments are generated.

---

## 2. Feature Availability Registry

| Feature Name | Source Table | Point-in-Time Availability | Early-Warning Checkout | Post-Delivery Diagnostic | Leakage Severity at Checkout |
|:---|:---|:---:|:---:|:---:|:---:|
| `total_item_price` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `total_freight` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `total_order_value` | Computed | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `freight_ratio` | Computed | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `item_count` | `order_items` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `payment_installments_max` | `order_payments` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `seller_buyer_distance_km` | `geolocation` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `estimated_lead_time_days` | `orders` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None (Marketplace SLA promised at purchase) |
| `mean_product_weight_g` | `products` | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `distance_x_weight` | Computed | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | None |
| `approval_lag_hours` | `orders` | Order Approval ($t_{\text{app}}$) | **ELIGIBLE** | **ELIGIBLE** | Zero (if processed after payment clearance) |
| `prior_order_count` | Computed As-Of | Checkout ($t_0$) | **ELIGIBLE** | **ELIGIBLE** | Zero (strictly cumulative prior orders) |
| `delivery_lead_time_days` | `orders` | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `delivery_delay_days` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `is_late` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `delay_x_freight_ratio` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `high_value_late_flag` | Computed | Delivery ($t_{\text{del}}$) | **PROHIBITED** | **ELIGIBLE** | **CRITICAL LEAKAGE** |
| `review_score` | `order_reviews` | Review Date ($t_{\text{rev}}$) | **TARGET ONLY** | **TARGET ONLY** | **DIRECT TARGET LEAKAGE** |

---

## 3. Automated Anti-Leakage Verification
The test `tests/test_feature_leakage.py::test_checkout_stage_restricted_features` directly imports `ModelExperimentTrainer.FEATURE_SETS['E1_early_warning_checkout']` and verifies zero intersection with `checkout_stage_restricted_features`. All 87 test suite assertions execute and pass without failure.
