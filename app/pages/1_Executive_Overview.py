"""Page 1: Executive Overview [UK-01, UK-02, UK-11]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Executive Overview | CSIP", page_icon="📊", layout="wide")

st.title("📊 Executive Overview & Strategic Roadmap")
st.markdown("**SKKNI Competency Standards**: `[UK-01 Menentukan Masalah Bisnis]`, `[UK-02 Menentukan Kebutuhan Data]`, `[UK-11 Mengembangkan Solusi]`")

st.write("---")

st.markdown("### 🎯 Business Problem Formulation & Scope")
st.markdown("""
E-commerce marketplaces face an existential tension between **transaction economics** (price margins, freight fees) and **operational fulfillment experience** (delivery lead times, logistics delays). 
Platforms frequently default to expensive customer acquisition subsidies without measuring whether delivery experience or pricing drives long-term customer lifetime value.

This platform investigates the **Olist Brazilian E-Commerce Ecosystem** (~100,000 orders across 27 federal states) to provide empirical behavioral intelligence for platform executives.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("💡 Core Empirical Discoveries")
    st.markdown("""
    - **Fulfillment Dominates Pricing**: Delivery delay and freight ratio interaction exert **3.4x greater attribution mass** on negative customer reviews than raw product prices (`DISC-04`).
    - **Asymmetric Delay Penalty**: Arriving early maintains ratings near 4.3 stars, but being late by just 1–3 days crashes ratings to 2.5 stars (`DISC-02`).
    - **The Repurchase Satisfaction Paradox**: Initial order review score does **NOT** predict repeat purchases ($p = 0.859$, Odds Ratio = 0.9964). 5-star buyers repeat at 2.27%, identical to 1-star buyers at 2.29% (`FAIL-HYP-H3`).
    """)

with col2:
    st.subheader("⚖️ Strategic Decision Trade-offs")
    st.markdown(r"""
    - **Carrier SLA Optimization Over Universal Subsidies**: Optimizing partner carrier logistics (S2) improves customer satisfaction with **2.8x higher capital efficiency** than flat 15% freight subsidies (S1).
    - **Targeted Subsidies for High Friction Segments**: Restricting freight subsidies exclusively to Cluster 0 (Heavy Freight Friction) captures 83.6% of satisfaction gains while slashing subsidy costs by 50.3%.
    - **Severe Class Imbalance**: In Olist, only 2.28% of cohort customers repurchase within 90 days. Models require probability calibration to output actionable risk probabilities.
    """)

st.write("---")

st.subheader("📈 Executive Scorecard: Machine Learning & Simulation")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Delivered Orders", "96,470", "Full Population")
c2.metric("Champion PR-AUC", "0.3004", "+35.6% vs Naive")
c3.metric("Brier Calibration Lift", "+44.59%", "Platt Scaling")
c4.metric("World Model Volume WAPE", "15.83%", "87 Weeks Backtest")

st.write("---")
st.subheader("📋 C-Level Action Plan")
st.markdown("""
1. **Contract Logistics Penalties**: Re-negotiate carrier SLAs with explicit penalties for delivery delays $>3$ days, as delay is the single largest controllable driver of churn risk.
2. **Eliminate Blanket Freight Subsidies**: Terminate universal fee waivers; divert the budget into dynamic routing and localized micro-fulfillment hubs in high-friction states.
3. **Decouple Retention from Satisfaction Surveys**: Base customer re-engagement on product replenishment cycles (e.g. consumables vs furniture) rather than post-purchase review stars.
""")
