# CSIP Data Dictionary: Comprehensive Feature & Entity Reference
## Semantic Definitions, Data Types, Source Provenance & Value Bounds

**Document Version:** 1.0.0-Definitive  
**Standard Compliance:** SKKNI 299/2020 Unit 3 (`J.62DMI00.005.1`) & Unit 5 (`J.62DMI00.007.1`)  
**Target Dataset:** Clean Order-Level Feature Table (`data/processed/order_level.parquet`)  

---

### 1. PRIMARY ENTITY GRAIN SPECIFICATION

- **Grain:** One physical row per unique customer order (`order_id`).
- **Population Size:** 96,470 clean, deduplicated orders (subset of 99,441 raw orders having valid items and delivery records).
- **Temporal Horizon:** September 4, 2016 through August 29, 2018.

---

### 2. ORDER-LEVEL TABLE ATTRIBUTES (42 COLUMNS)

| Column Name | Physical Data Type | Semantic Type | Value Range / Domain | Nullable | Source Table | Description |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `order_id` | string (UUID) | Identifier | 32 hex chars | No | `olist_orders_dataset` | Unique identifier of the transaction order. |
| `customer_id` | string (UUID) | Identifier | 32 hex chars | No | `olist_orders_dataset` | Key to the customer dataset (unique per order). |
| `order_status` | string | Categorical | `delivered`, `shipped`, `canceled` | No | `olist_orders_dataset` | Operational status of the transaction. |
| `order_purchase_timestamp` | datetime64 | Temporal | 2016-09-04 to 2018-08-29 | No | `olist_orders_dataset` | Exact UTC timestamp of purchase checkout. |
| `order_approved_at` | datetime64 | Temporal | 2016-09-04 to 2018-08-29 | Yes | `olist_orders_dataset` | Timestamp of payment gateway approval. |
| `order_delivered_carrier_date`| datetime64 | Temporal | 2016-09-05 to 2018-08-30 | Yes | `olist_orders_dataset` | Timestamp when order was handed to logistics carrier. |
| `order_delivered_customer_date`| datetime64 | Temporal | 2016-09-08 to 2018-08-31 | Yes | `olist_orders_dataset` | Actual timestamp when customer received package. |
| `order_estimated_delivery_date`| datetime64 | Temporal | 2016-09-15 to 2018-09-15 | No | `olist_orders_dataset` | Promised delivery deadline shown to buyer at checkout. |
| `total_item_price` | float64 | Continuous | BRL 0.85 to BRL 13,440.00 | No | `olist_order_items_dataset` | Sum of item catalog prices in the order. |
| `total_freight` | float64 | Continuous | BRL 0.00 to BRL 1,794.96 | No | `olist_order_items_dataset` | Total shipping and freight charge paid by customer. |
| `item_count` | int64 | Discrete | 1 to 21 items | No | `olist_order_items_dataset` | Total number of individual items contained in order. |
| `seller_id` | string (UUID) | Identifier | 32 hex chars | No | `olist_order_items_dataset` | Identifier of primary seller fulfilling order. |
| `product_category` | string | Categorical | 71 Brazilian categories | Yes | `olist_products_dataset` | Portuguese product category name. |
| `mean_product_weight_g` | float64 | Continuous | 0 to 40,425 grams | Yes | `olist_products_dataset` | Average weight of items in order. |
| `total_payment_value` | float64 | Continuous | BRL 0.00 to BRL 13,664.08 | Yes | `olist_order_payments` | Total transactional monetary value processed. |
| `payment_installments_max` | int64 | Discrete | 1 to 24 installments | No | `olist_order_payments` | Maximum credit card payment installments chosen. |
| `payment_type_primary` | string | Categorical | `credit_card`, `boleto`, `voucher`, `debit_card` | No | `olist_order_payments` | Primary payment method utilized. |
| `customer_unique_id` | string (UUID) | Identifier | 32 hex chars | No | `olist_customers_dataset` | Permanent natural customer identifier. |
| `customer_state` | string (UF) | Categorical | 27 Brazilian states (`SP`, `RJ`, etc.) | No | `olist_customers_dataset` | Customer billing federative unit. |
| `customer_zip_code_prefix` | int64 | Discrete | 1000 to 99990 | No | `olist_customers_dataset` | 5-digit postal code prefix of customer. |
| `seller_state` | string (UF) | Categorical | 27 Brazilian states | Yes | `olist_sellers_dataset` | Origin state of the dispatching merchant. |
| `seller_zip_code_prefix` | int64 | Discrete | 1000 to 99990 | Yes | `olist_sellers_dataset` | 5-digit postal code prefix of seller. |
| `buyer_lat` | float64 | Continuous | -36.60 to +4.58 | Yes | `clean_geolocation_dedup` | Approximate latitude of buyer zip code. |
| `buyer_lng` | float64 | Continuous | -72.67 to -34.80 | Yes | `clean_geolocation_dedup` | Approximate longitude of buyer zip code. |
| `seller_lat` | float64 | Continuous | -36.60 to +4.58 | Yes | `clean_geolocation_dedup` | Approximate latitude of seller zip code. |
| `seller_lng` | float64 | Continuous | -72.67 to -34.80 | Yes | `clean_geolocation_dedup` | Approximate longitude of seller zip code. |
| `seller_buyer_distance_km` | float64 | Continuous | 0.0 to 8,712.5 km | Yes | Calculated (Haversine) | Great-circle geographic distance between buyer & seller. |
| `total_order_value` | float64 | Continuous | BRL 0.85 to BRL 13,664.08 | No | Calculated (`price + freight`) | Total merchandise plus shipping expenditure. |
| `freight_ratio` | float64 | Continuous | 0.000 to 0.950 | No | Calculated (`freight / total`) | Proportion of total order expenditure attributed to freight. |
| `delivery_lead_time_days` | float64 | Continuous | 0.5 to 209.6 days | Yes | Calculated (`delivered - purchase`) | Actual transit duration from purchase to customer delivery. |
| `estimated_lead_time_days` | float64 | Continuous | 3.0 to 155.0 days | No | Calculated (`estimated - purchase`)| Promised transit lead time window. |
| `delivery_delay_days` | float64 | Continuous | -60.0 to +188.0 days | Yes | Calculated (`delivered - estimated`)| Delay in days relative to promised date (Positive = Late). |
| `is_late` | int64 | Binary Flag | 0 or 1 | No | Calculated (`delivery_delay > 0`) | Indicator if order arrived after promised estimate. |
| `approval_lag_hours` | float64 | Continuous | 0.0 to 720.0 hours | Yes | Calculated (`approved - purchase`)| Processing latency for payment approval. |
| `review_score` | float64 | Discrete Ordinal | 1.0, 2.0, 3.0, 4.0, 5.0 | Yes | `olist_order_reviews` | Customer satisfaction rating (1 = Worst, 5 = Best). |
| `has_review_comment` | int64 | Binary Flag | 0 or 1 | No | `olist_order_reviews` | Indicator if customer submitted written review text. |
| `has_observed_review` | int64 | Binary Flag | 0 or 1 | No | `olist_order_reviews` | Indicator if order has a corresponding review record. |
| `negative_review_flag` | float64 | Binary Target | 0.0 or 1.0 | Yes | Calculated (`review_score <= 2`) | Primary classification target (1 if score in [1, 2]). |
| `delay_x_freight_ratio` | float64 | Interaction | -50.0 to +150.0 | Yes | Engineered (`delay * freight_ratio`) | Compounded friction interaction feature. |
| `distance_x_weight` | float64 | Interaction | 0.0 to 1e8 | Yes | Engineered (`distance * weight`) | Transportation logistical burden index. |
| `high_value_late_flag` | int64 | Binary Interaction | 0 or 1 | No | Engineered (`price > 150 & is_late`)| Indicator for delayed premium orders. |
| `prior_order_count` | int64 | Discrete Counter | 0 to 16 prior orders | No | Temporal Cohort Cumulative | Prior order history of customer at purchase timestamp. |

---

### 3. CUSTOMER COHORT TABLE ATTRIBUTES (`customer_cohort.parquet`)

- **Grain:** One physical row per unique customer order with temporal repeat purchase horizons.
- **Key Columns:**
  - `customer_unique_id`: Natural customer identifier.
  - `repeat_purchase_flag`: Binary indicator (1 if customer placed any subsequent order within historical dataset).
  - `days_to_repeat`: Elapsed days from current order purchase to next order purchase.
  - `repeat_purchase_post_delivery_flag`: Binary indicator (1 if customer repurchased strictly *after* receiving order delivery).
  - `is_censored`: Survival analysis censoring flag (1 if no subsequent purchase observed before dataset cutoff).

---

### 4. WEEKLY SYSTEM STATE TIME-SERIES (`weekly_system_state.parquet`)

- **Grain:** One physical row per calendar week (87 weekly records from 2016-W36 to 2018-W35).
- **State Vector Columns ($s_t$):**
  - `weekly_order_volume`: Total platform orders completed in week $t$.
  - `mean_delivery_delay`: Average delivery delay (days) for orders placed in week $t$.
  - `delay_rate`: Proportion of orders delivered late in week $t$.
  - `negative_review_rate`: Proportion of 1-star and 2-star reviews in week $t$.
  - `mean_freight_ratio`: Average shipping fee percentage in week $t$.
  - `mean_item_price`: Average merchandise order price in week $t$.

