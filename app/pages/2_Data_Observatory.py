"""Page 2: Data Observatory [UK-03, UK-04, UK-05, UK-06]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Data Observatory | CSIP", page_icon="🔭", layout="wide")

st.title("🔭 Data Observatory & Pipeline Architecture")
st.markdown("**SKKNI Competency Standards**: `[UK-03 Menelaah Data]`, `[UK-04 Memvalidasi Data]`, `[UK-05 Membersihkan Data]`, `[UK-06 Mengonstruksi Data]`")

st.write("---")

tab1, tab2, tab3 = st.tabs(["🏛️ 4 Core Analytical Grains", "🧹 Cleaning & Memory Optimization", "🔍 Referential Integrity & Distributions"])

with tab1:
    st.subheader("Architectural Granularity: 4 Core Processed Datasets")
    st.markdown("""
    To avoid aggregation bias, Simpson's paradox, and data leakage, the platform processes data at **4 distinct analytical grains**:
    """)

    grain_df = pd.DataFrame([
        {
            "Dataset Grain": "order_level.parquet",
            "Rows": "96,470",
            "Columns": "41",
            "Entity Key": "order_id",
            "Purpose": "Transaction economics, spatial logistics, and satisfaction risk modeling.",
        },
        {
            "Dataset Grain": "customer_cohort.parquet",
            "Rows": "75,318",
            "Columns": "23",
            "Entity Key": "customer_unique_id",
            "Purpose": "Strict First-Order Isolation. Excludes 18,032 right-censored users (<90 days). Repeat rate = 2.28%.",
        },
        {
            "Dataset Grain": "review_corpus.parquet",
            "Rows": "95,824",
            "Columns": "9",
            "Entity Key": "review_id",
            "Purpose": "NLP sequence corpus (38,870 non-empty text reviews) in Brazilian Portuguese.",
        },
        {
            "Dataset Grain": "weekly_system_state.parquet",
            "Rows": "87",
            "Columns": "10",
            "Entity Key": "year_week",
            "Purpose": "Weekly macroeconomic panel (Jan 2017 – Aug 2018) for dynamic state-space world modeling.",
        },
    ])
    st.dataframe(grain_df, use_container_width=True)

    st.info("🔒 **Strict Anti-Leakage Protocol**: In `customer_cohort.parquet`, only first-order checkout features are permitted. Post-delivery fulfillment features (actual delivery date, reviews) and lifetime aggregates are strictly isolated.")

with tab2:
    st.subheader("Memory Optimization & Data Cleaning Pipeline")
    c1, c2, c3 = st.columns(3)
    c1.metric("Raw Table RAM", "132.38 MB", "9 Tables")
    c2.metric("Downcast RAM", "87.10 MB", "-34.2% Reduction")
    c3.metric("Geolocation Compression", "19,010 Rows", "-98.1% Cartesian Fix")

    st.markdown("""
    - **Dtype Downcasting**: Automatic casting from `float64`/`int64` to `float32`, `int16`/`int32`, and string categorical encodings.
    - **Geolocation Cartesian Explosion Fix**: Raw geolocation table contained 1,000,163 entries with duplicate coordinates per zip code. Compressed to median lat/lng per `geolocation_zip_code_prefix` (19,010 unique rows), enabling sub-second spatial joins without RAM bottlenecks.
    - **Chronological Anomaly Removal**: Dropped 23 corrupt rows where `order_delivered_customer_date < order_purchase_timestamp`.
    - **Order Status Filtering**: Restated to delivered orders (`order_status == 'delivered'`).
    """)

with tab3:
    st.subheader("Referential Integrity Audit: 0 Orphan Foreign Keys")
    ref_df = pd.DataFrame([
        {"Child Table": "order_items", "FK Column": "order_id", "Parent Table": "orders", "Orphans": 0, "Integrity": "100.0%"},
        {"Child Table": "order_payments", "FK Column": "order_id", "Parent Table": "orders", "Orphans": 0, "Integrity": "100.0%"},
        {"Child Table": "order_reviews", "FK Column": "order_id", "Parent Table": "orders", "Orphans": 0, "Integrity": "100.0%"},
        {"Child Table": "orders", "FK Column": "customer_id", "Parent Table": "customers", "Orphans": 0, "Integrity": "100.0%"},
        {"Child Table": "order_items", "FK Column": "product_id", "Parent Table": "products", "Orphans": 0, "Integrity": "100.0%"},
        {"Child Table": "order_items", "FK Column": "seller_id", "Parent Table": "sellers", "Orphans": 0, "Integrity": "100.0%"},
    ])
    st.dataframe(ref_df, use_container_width=True)

    st.write("---")
    st.subheader("Key Empirical Visualizations")
    col_a, col_b = st.columns(2)
    fig_a = Path("artifacts/reports/figures/eda_delay_vs_satisfaction.png")
    fig_b = Path("artifacts/reports/figures/eda_weekly_order_trend.png")

    if fig_a.exists():
        col_a.image(str(fig_a), caption="Asymmetric Penalty: Delivery Delay vs Satisfaction (H2)")
    if fig_b.exists():
        col_b.image(str(fig_b), caption="Weekly System Growth & Macro Dynamics (2017–2018)")
