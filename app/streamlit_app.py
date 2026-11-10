"""CSIP (Computational Society Intelligence Platform) - Main Entrypoint & Hub.

MVP Module: Behavioral Decision Intelligence (BDI)
Dataset: Brazilian E-Commerce (Olist, ~100k orders)
Standard: SKKNI Data Science (BNSP) - 11 Units Certified
"""

from __future__ import annotations

import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="CSIP — Behavioral Decision Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished scientific styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-grade {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #dcfce7;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧭 Computational Society Intelligence Platform (CSIP)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">MVP Module: <b>Behavioral Decision Intelligence (BDI)</b> — Brazilian E-Commerce Observational Study</div>', unsafe_allow_html=True)

# Status Badges
st.markdown("""
<span class="badge-grade">SKKNI Data Science (BNSP): 11/11 Units Verified</span>
&nbsp;&nbsp;
<span class="badge-grade">Anti-Leakage First-Order Isolation: Enforced</span>
&nbsp;&nbsp;
<span class="badge-grade">Scientific Claim Governance: L0 – L3 Certified</span>
""", unsafe_allow_html=True)

st.write("")

# KPI Metrics Row
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown('<div class="metric-card"><div class="metric-val">96,470</div><div class="metric-lbl">Delivered Orders</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-val">0.3865</div><div class="metric-lbl">Silhouette (k=3)</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-val">0.3004</div><div class="metric-lbl">Champion PR-AUC</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><div class="metric-val">0.8076</div><div class="metric-lbl">Text Bi-LSTM PR-AUC</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown('<div class="metric-card"><div class="metric-val">5 / 1</div><div class="metric-lbl">Hypotheses (Pass/Fail)</div></div>', unsafe_allow_html=True)

st.write("---")

st.markdown("### 🏛️ Platform Architecture & 9 Analytical Modules")
st.markdown("""
CSIP operates on a **Three-Tier Architecture** integrating deterministic data engineering, classical and deep predictive models, macro state-space world modeling, and counterfactual simulation:
""")

cols = st.columns(3)
with cols[0]:
    st.info("**1. Executive Overview** [UK-01, UK-02, UK-11]\n\nHigh-level strategic findings, core trade-offs, and C-level decision roadmap.")
    st.info("**2. Data Observatory** [UK-03, UK-04, UK-05, UK-06]\n\nData dictionary, referential integrity audit (0 orphan records), and 4 analytical grains.")
    st.info("**3. Behavioral Discovery Lab** [UK-03, UK-07]\n\nUnsupervised persona segmentation ($k=3$), PCA projections, and friction anomaly detection.")

with cols[1]:
    st.info("**4. Hypothesis Laboratory** [UK-08, UK-10]\n\nFormal econometric testing (H1–H6) with Benjamini-Hochberg FDR correction and honest rejection of H3.")
    st.info("**5. Predictive Intelligence** [UK-08, UK-09, UK-10]\n\nBaseline Ladder (B0–B4), LightGBM Champion vs Tabular MLP vs Text Bi-LSTM, and SHAP attributions.")
    st.info("**6. World Model** [UK-08, UK-09, UK-10]\n\nState-Space dynamics, Synthetic Parameter Recovery test (0.33% error), and historical backtest replay.")

with cols[2]:
    st.info("**7. Alternative World Simulator** [UK-08, UK-10, UK-11]\n\n12-week forward counterfactual policy simulations (S0–S5) with residual bootstrap Prediction Intervals.")
    st.info("**8. Decision Studio** [UK-01, UK-11]\n\nFinancial ROI optimization, capital efficiency analysis (Carrier SLA vs Subsidies), and policy recommendations.")
    st.info("**9. Evidence Registry & Audit** [UK-10, UK-11]\n\nFull audit of Discoveries (DISC-01 to DISC-07), Failure Register, and SKKNI Traceability Matrix.")

st.write("---")
st.caption("👈 **Select a page from the left sidebar to explore the platform modules.** All visualizations and metrics originate from precomputed, reproducible empirical evidence.")
