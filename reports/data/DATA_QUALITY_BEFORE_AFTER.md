# CSIP Data Quality Audit: Before vs After Transformation Report
## Quantitative Ingestion, Cleansing, Deduplication & Imputation Reconciliation

**Audit Target:** Data Engineering Pipeline (`src/csip/cleaning/cleaner.py` & `scripts/build_clean_datasets.py`)  
**Standard Compliance:** SKKNI 299/2020 Unit 4 (`J.62DMI00.006.1`) & Unit 6 (`J.62DMI00.008.1`)  
**Audit Date:** 11 November 2026  

---

### 1. SUMMARY OF DATA TRANSFORMATION RECONCILIATION

The CSIP data pipeline ingests 9 raw relational CSV files from the Brazilian E-Commerce public repository (Olist) and executes deterministic cleansing, deduplication, schema alignment, and order-grain consolidation.

```
=======================================================================================================
CSIP DATA QUALITY AUDIT TABLE — BEFORE (RAW) VS AFTER (INTERIM & PROCESSED)
=======================================================================================================
Dataset Entity      Raw Rows   Raw Anomalies / Issues         Cleaned Rows Cleaned Status & Treatment
------------------  ---------  -----------------------------  ------------ ----------------------------
olist_orders           99,441  Null dates, canceled status          96,470 Filtered to valid order grain
olist_order_items     112,650  Item-level grain, multi-seller       96,470 Aggregated to order grain
olist_order_payments  103,886  Split payments (vouchers/cards)      96,470 Summed to total_payment_value
olist_order_reviews   104,719  Duplicate reviews per order          95,824 Deduplicated to latest review
olist_geolocation   1,000,163  Massive duplicate zip codes          19,015 Deduped to centroid coordinates
olist_customers        99,441  Transient vs unique customer ID      75,318 Unified to customer_unique_id
olist_products         32,951  Missing category, missing weight     32,951 Imputed with 'other' & median
olist_sellers           3,095  State codes, zip codes                3,095 Validated against geo lookup
category_translation       71  Portuguese to English mapping            71 100% mapped
=======================================================================================================
```

---

### 2. DETAILED DEFECT HARDENING & TREATMENT AUDIT

#### 2.1 Geolocation Deduplication & Outlier Removal (`clean_geolocation_dedup.parquet`)
- **Raw Issue:** The raw `olist_geolocation_dataset.csv` contains 1,000,163 records representing repeated GPS pings for the same postal codes, with several coordinates falling outside Brazilian territorial boundaries (e.g. positive latitudes $> +5^\circ$ or longitudes $< -74^\circ$).
- **Pipeline Treatment:**
  1. Filtered GPS points strictly to Brazilian geographical bounding box (Latitude: $[-34.0, +5.5]$, Longitude: $[-74.0, -34.5]$).
  2. Aggregated multiple coordinate readings per `geolocation_zip_code_prefix` to the mathematical median centroid.
  3. Output: 19,015 clean, unique zip code prefixes (337 KB Parquet), reducing disk memory footprint by 99.4% and accelerating spatial join operations from minutes to milliseconds.

#### 2.2 Relational Fan-Out & Order Grain Consolidation (`order_level.parquet`)
- **Raw Issue:** In the raw relational schema, an order can possess multiple items (`olist_order_items`) and multiple payment installments (`olist_order_payments`), causing severe row multiplication (fan-out) if joined naively.
- **Pipeline Treatment:**
  1. `olist_order_items` aggregated by `order_id`:
     - `total_item_price = sum(price)`
     - `total_freight = sum(freight_value)`
     - `item_count = count(order_item_id)`
     - `mean_product_weight_g = mean(product_weight_g)`
  2. `olist_order_payments` aggregated by `order_id`:
     - `total_payment_value = sum(payment_value)`
     - `payment_installments_max = max(payment_installments)`
     - `payment_type_primary = mode(payment_type)`
  3. Strict Uniqueness Verification: Asserted `df['order_id'].nunique() == len(df)` to ensure zero row duplication.

#### 2.3 Review Deduplication & Observed Review Indicator
- **Raw Issue:** Certain orders received multiple review entries due to customer updates or resubmissions. Furthermore, 646 orders in the dataset (~0.67%) have no submitted review.
- **Pipeline Treatment:**
  1. Grouped by `order_id` and retained the latest review by `review_creation_date` / `review_answer_timestamp`.
  2. Created explicit binary flag `has_observed_review` (1 if review exists, 0 if unreviewed).
  3. Negative review target `negative_review_flag` defined as:
     $$\text{negative\_review\_flag} = \begin{cases} 1.0 & \text{if } \text{review\_score} \le 2 \\ 0.0 & \text{if } \text{review\_score} \ge 3 \\ \text{NaN} & \text{if unreviewed} \end{cases}$$
  4. Models filter exclusively on rows where `has_observed_review == 1` without imputing fictitious ratings.

---

### 3. DATA LEAKAGE AUDIT & VERIFICATION

1. **Temporal Cutoff Enforcement:** All feature engineering involving cohort statistics (`prior_order_count`, `recency_days`) uses strictly backward-looking cumulative windows.
2. **Scaler & Imputer Fitting:** All Scikit-Learn transformers (`StandardScaler`, `SimpleImputer`, `OneHotEncoder`) are fitted strictly on the pre-2018-03-01 training partition and applied out-of-sample via Scikit-Learn Pipelines.
3. **Automated Leakage Test Suite:** `tests/test_feature_leakage.py` and `tests/test_temporal_leakage.py` verify that zero target or post-delivery information is accessible at prediction time.

