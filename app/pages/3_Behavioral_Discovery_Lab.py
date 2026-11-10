"""Page 3: Behavioral Discovery Lab [UK-03, UK-07]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Behavioral Discovery Lab | CSIP", page_icon="🧬", layout="wide")

st.title("🧬 Behavioral Discovery & Unsupervised Clustering Lab")
st.markdown("**SKKNI Competency Standards**: `[UK-03 Menelaah Data]`, `[UK-07 Menentukan Objek Data]`")

st.write("---")

# Metrics Banner
c1, c2, c3, c4 = st.columns(4)
c1.metric("Optimal Clusters (k)", "3", "k in [3, 4, 5, 6]")
c2.metric("Silhouette Score", "0.3865", "Threshold >= 0.35 (PASSED)")
c3.metric("Davies-Bouldin Index", "1.2168", "Lower is Better")
c4.metric("Extreme Anomalies", "4,824 orders", "5.0% Friction Tail")

st.write("---")

col_left, col_right = st.columns([1.1, 1.0])

with col_left:
    st.subheader("👥 3 Behavioral Archetype Personas")
    st.markdown("""
    Unsupervised $k$-Means clustering on PCA-transformed standardized behavioral dimensions revealed **3 distinct customer archetypes**:
    """)

    personas = [
        {
            "Persona": "Persona 0: Heavy Freight Friction",
            "Population Share": "40.2% (38,819 orders)",
            "Freight Ratio": "38.2% (High)",
            "Avg Lead Time": "15.4 days",
            "Risk Profile": "1.78x higher negative review risk. Highly vulnerable to carrier delays.",
            "Policy Action": "Targeted freight relief (Scenario S3) and regional micro-fulfillment.",
        },
        {
            "Persona": "Persona 1: Fast Single-Item Convenience",
            "Population Share": "51.0% (49,183 orders)",
            "Freight Ratio": "14.1% (Low)",
            "Avg Lead Time": "9.2 days",
            "Risk Profile": "Lowest defect rate. Core everyday marketplace volume.",
            "Policy Action": "Standard operations; maintain carrier SLAs.",
        },
        {
            "Persona": "Persona 2: High-Ticket Premium Basket",
            "Population Share": "8.8% (8,468 orders)",
            "Freight Ratio": "7.8% (Very Low)",
            "Avg Lead Time": "12.8 days",
            "Risk Profile": "High order value (>R$ 450). Low price sensitivity, high packaging sensitivity.",
            "Policy Action": "White-glove carrier tracking and guaranteed SLA insurance.",
        },
    ]
    st.dataframe(pd.DataFrame(personas), use_container_width=True)

with col_right:
    st.subheader("🗺️ PCA Dimensional Projection")
    fig_pca = Path("artifacts/reports/figures/clustering_pca_clusters.png")
    if fig_pca.exists():
        st.image(str(fig_pca), caption="PCA 2D Projection: 3 Behavioral Clusters & Friction Anomalies")

st.write("---")

st.subheader("📜 Discoveries Registered in Evidence Registry")
st.markdown(r"""
- **DISC-01 (High Freight Friction Segment)**: Buyers with freight ratio >35% experience a 1.78x increased risk of leaving 1-star/2-star negative reviews (Claim Level L0, Grade A).
- **DISC-02 (Asymmetric Delivery Delay Penalty)**: Delays exceeding 1–3 days collapse ratings to 2.5 stars, while early arrivals saturate at 4.3 stars (Claim Level L2, Grade A).
- **DISC-03 (Fast Convenience Core)**: 51% of marketplace transactions are fast single-item purchases forming base platform liquidity (Claim Level L0, Grade A).
""")
