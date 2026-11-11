# CSIP Data Methodology Specification
## Data Intake, Quality Assurance, Feature Construction, and Anti-Leakage Governance
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.005.1 s.d. J.62DMI00.009.1

- **Document ID**: `CSIP-METH-DATA-2026-V7`
- **Version**: 7.0.0
- **Status**: AUDITED & METHODOLOGICALLY VERIFIED
- **Author**: Lead Data Engineer & Senior Methodologist

---

## 1. Raw Data Intake and Referential Integrity

The primary empirical source comprises 9 relational tables from the Brazilian E-Commerce public dataset (Olist), covering transactions between September 2016 and October 2018.

### Referential Integrity Verification:
- **Foreign Key Consistency**: Verified via `src/csip/data/loader.py`:
  - `order_items.order_id` $\to$ `orders.order_id`: 100% matched (0 orphan records).
  - `order_payments.order_id` $\to$ `orders.order_id`: 100% matched (0 orphan records).
  - `orders.customer_id` $\to$ `customers.customer_id`: 100% matched (0 orphan records).
- **Data Types & Profiling**: Monitored via `src/csip/data/semantic_profiler.py`, confirming currency units in Brazilian Real (BRL / R$) and standardized UTC timestamp parsing.

---

## 2. Quality Assurance & Anomaly Hardening

### 2.1 Chronological Anomaly Filtering
- An inspection of order timelines identified **23 orders** where `order_delivered_customer_date < order_purchase_timestamp`.
- These records represent data entry errors or reversed timestamps and are systematically filtered out during initial cleaning.

### 2.2 Spatial Deduplication
- Raw geolocation records contained 1,000,163 rows with high redundancy per zip code prefix.
- Deduplication groups by `geolocation_zip_code_prefix` to compute mean latitude and longitude centroids, compressing the spatial table to **19,015 clean centroids** (-98.1% row reduction) while accelerating Haversine distance calculations by over 50x.

### 2.3 Review Label Observability
- Out of 96,470 cleaned delivered orders, **646 orders (0.67%)** have missing review surveys.
- Rather than imputing these as neutral (3) or positive (0), CSIP explicitly preserves them as `NaN` and flags them with `has_observed_review = 0`. Supervised learning pipelines strictly train on observed labels, eliminating synthetic label distortion.

---

## 3. Analytical Data Construction (4 Objek Data)

CSIP formalizes 4 distinct analytical objects tailored to specific research questions:

1. **`order_level`** (Grain: `order_id` | 96,470 rows x 42 columns):
   - Comprehensive transactional dataset joining item basket economics, shipping charges, carrier SLA dates, payment installments, and customer feedback.
2. **`customer_cohort`** (Grain: `customer_unique_id` | 75,318 rows x 23 columns):
   - Strict First-Order Retention dataset. Features are extracted exclusively from each customer's first completed transaction to predict 90-day repurchase.
   - Customers within 90 days of the dataset cutoff date are excluded (right-censoring mitigation).
3. **`review_corpus`** (Grain: `review_id` | 95,824 rows x 9 columns):
   - Text corpus pairing customer comments with polar sentiment labels for Bi-LSTM NLP modeling.
4. **`weekly_system_state`** (Grain: `year_week` | 87 rows x 10 columns):
   - Aggregate macro panel tracking platform order volume, mean delay, freight burden, and negative review rate across weekly epochs for the World Model.

---

## 4. Feature Engineering Methodology & Governance

### 4.1 Vectorized Spatial Distance
Geographic distance between seller and buyer zip code centroids is calculated using the vectorized Haversine formula on spherical coordinates:
$$d = 2 R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$
Where $R = 6,371 \text{ km}$.

### 4.2 Compound Friction Interaction Terms
- `freight_ratio`: $\frac{\text{total\_freight}}{\text{total\_item\_price} + 10^{-5}}$
- `delay_x_freight_ratio`: $\max(0, \text{delivery\_delay\_days}) \times \text{freight\_ratio}$ (captures compounding customer frustration when expensive shipping arrives late).
- `distance_x_weight`: $\text{seller\_buyer\_distance\_km} \times \ln(1 + \text{product\_weight\_g})$ (quantifies fulfillment logistics complexity).
- `high_value_late_flag`: $\mathbb{I}(\text{total\_order\_value} > Q_{75}) \times \mathbb{I}(\text{is\_late} = 1)$ (flags premium orders suffering delivery failure).

### 4.3 Cohort Selection Integrity (V7 Hardening)
- In V6, cohort selection used `df.groupby('customer_unique_id').first()`, which introduced a column-wise non-null selection vulnerability.
- In V7, this was refactored to deterministic row-level selection:
  ```python
  order_1 = df_sorted.drop_duplicates(subset=["customer_unique_id"], keep="first").copy().reset_index(drop=True)
  ```
  This guarantees that Order 1 features never incorporate values from subsequent transactions.

### 4.4 Split-Before-Fit Transformation
All transformers (StandardScaler, SimpleImputer, TfidfVectorizer) are fitted strictly on the Training split (Weeks 1–64) and applied passively to Validation and Test splits, preventing distribution leakage.
