"""Page 8: Decision Studio [UK-01, UK-11]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Decision Studio | CSIP", page_icon="🎯", layout="wide")

st.title("🎯 Strategic Decision Studio & Policy Optimization")
st.markdown("**SKKNI Competency Standards**: `[UK-01 Menentukan Masalah Bisnis]`, `[UK-11 Mengembangkan Solusi]`")

st.write("---")

st.subheader("💡 Strategic Policy Optimization Matrix")
st.markdown("""
Based on the empirical evidence from 96,470 orders, econometric tests (H1–H6), SHAP feature attribution (31.2% delay mass), and counterfactual simulations (S0–S5), the platform recommends the following policy matrix:
""")

matrix_df = pd.DataFrame([
    {
        "Strategic Option": "Option 1: Universal Freight Subsidy (S1)",
        "Capital Cost": "High (R$ 33,544 / 12 wks)",
        "Satisfaction Impact": "Moderate (-2.44 pp reviews)",
        "Capital Efficiency": "Very Poor (Negative Net Profit)",
        "Strategic Verdict": "DO NOT ADOPT (Deadweight loss on inframarginal orders)",
    },
    {
        "Strategic Option": "Option 2: Carrier Logistics SLA Overhaul (S2)",
        "Capital Cost": "Low (R$ 10,989 / 12 wks)",
        "Satisfaction Impact": "Solid (-0.90 pp reviews)",
        "Capital Efficiency": "2.8x Higher than Subsidies",
        "Strategic Verdict": "HIGH PRIORITY (Directly targets root driver of churn)",
    },
    {
        "Strategic Option": "Option 3: Targeted Friction Subsidy (S3)",
        "Capital Cost": "Medium (R$ 16,664 / 12 wks)",
        "Satisfaction Impact": "Strong (-2.04 pp reviews)",
        "Capital Efficiency": "Balanced (Captures 84% of S1 at 50% cost)",
        "Strategic Verdict": "RECOMMENDED (Deploy selectively to Cluster 0)",
    },
    {
        "Strategic Option": "Option 4: Combined Seasonal Blitz (S5)",
        "Capital Cost": "High (R$ 41,319 / 12 wks)",
        "Satisfaction Impact": "Maximum (-3.76 pp reviews)",
        "Capital Efficiency": "Seasonal Investment",
        "Strategic Verdict": "TACTICAL ONLY (Reserve for Q4 Black Friday surge)",
    },
])
st.dataframe(matrix_df, use_container_width=True)

st.write("---")

st.subheader("🧮 Interactive Platform Financial Impact Calculator")
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("##### Platform Parameters")
    take_rate_pct = st.slider("Platform Take Rate (%)", min_value=5.0, max_value=25.0, value=15.0, step=1.0)
    subsidy_per_order = st.slider("Subsidy per Order (BRL)", min_value=0.0, max_value=10.0, value=3.5, step=0.5)
    projected_orders = st.number_input("Projected Quarterly Orders", min_value=1000, max_value=50000, value=9500, step=500)
    aov = st.number_input("Average Order Value (BRL)", min_value=50.0, max_value=500.0, value=160.0, step=10.0)

with col_out:
    st.markdown("##### Financial Projection")
    gross_gmv = projected_orders * aov
    platform_take = gross_gmv * (take_rate_pct / 100.0)
    total_subsidy = projected_orders * subsidy_per_order
    net_contrib = platform_take - total_subsidy
    subsidy_drag = (total_subsidy / platform_take) * 100 if platform_take > 0 else 0

    st.metric("Quarterly Gross GMV", f"R$ {gross_gmv:,.2f}")
    st.metric("Platform Net Revenue", f"R$ {platform_take:,.2f}")
    st.metric("Subsidy Expenditure", f"R$ {total_subsidy:,.2f}", f"{subsidy_drag:.1f}% of Take Revenue")
    st.metric("Net Platform Margin After Subsidy", f"R$ {net_contrib:,.2f}", delta=f"{net_contrib:+,.2f}")

st.write("---")
st.subheader("🗓️ 90-Day Operational Execution Roadmap")
st.markdown("""
- **Days 1–30 (Logistics Contracting)**: Enforce carrier delivery SLA thresholds; introduce SLA breach penalties for delivery delays $>3$ days.
- **Days 31–60 (Targeted Subsidy Rollout)**: Launch selective freight discounts restricted to **Cluster 0 (Heavy Freight Friction buyers)** in remote northern states.
- **Days 61–90 (System Monitoring & Recalibration)**: Continuous tracking of weekly system state transitions in the World Model; check Extrapolation Guardrails weekly.
""")
