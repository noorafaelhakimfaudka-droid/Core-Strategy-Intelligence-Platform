"""Page 4: Hypothesis Laboratory [UK-08, UK-10]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Hypothesis Laboratory | CSIP", page_icon="🧪", layout="wide")

st.title("🧪 Hypothesis Testing & Econometric Evidence Lab")
st.markdown("**SKKNI Competency Standards**: `[UK-08 Membangun Skenario Model]`, `[UK-10 Mengevaluasi Hasil Pemodelan]`")

st.write("---")

st.markdown("""
To prevent p-hacking and spurious correlational claims, all **6 core hypotheses** were pre-registered and evaluated under **Benjamini-Hochberg False Discovery Rate (FDR)** control ($\alpha = 0.05$).
""")

# Table of Hypotheses
hyp_summary = [
    {
        "ID": "H1",
        "Formal Hypothesis Statement": "Rasio ongkos kirim berkorelasi negatif terhadap skor kepuasan ulasan pelanggan.",
        "Test": "OLS t-test",
        "Statistic": "t = -37.89",
        "Effect Size": "β = -0.2081",
        "p-adj (FDR)": "1.56e-32",
        "Status": "SUPPORTED",
        "Claim Level": "L2, Grade A",
    },
    {
        "ID": "H2",
        "Formal Hypothesis Statement": "Keterlambatan pengantaran memiliki slope penalti kepuasan lebih curam dibanding pengantaran cepat.",
        "Test": "Piecewise Spline Wald",
        "Statistic": "F = 4218.10",
        "Effect Size": "Δβ = -0.0638",
        "p-adj (FDR)": "0.0000",
        "Status": "SUPPORTED",
        "Claim Level": "L2, Grade A",
    },
    {
        "ID": "H3",
        "Formal Hypothesis Statement": "Skor ulasan pesanan pertama memprediksi kemungkinan pembelian berulang (repeat purchase).",
        "Test": "Logistic Odds Ratio",
        "Statistic": "z = -0.177",
        "Effect Size": "OR = 0.9964 [0.957, 1.037]",
        "p-adj (FDR)": "0.8590",
        "Status": "REJECTED (FAIL)",
        "Claim Level": "L2, Grade A",
    },
    {
        "ID": "H4",
        "Formal Hypothesis Statement": "Sensitivitas pembeli terhadap rasio ongkos kirim bervariasi secara heterogen antar-klaster perilaku.",
        "Test": "Cluster Interaction F",
        "Statistic": "F = 29.51",
        "Effect Size": "Δβ = -0.1840",
        "p-adj (FDR)": "3.08e-13",
        "Status": "SUPPORTED",
        "Claim Level": "L2, Grade A",
    },
    {
        "ID": "H5",
        "Formal Hypothesis Statement": "Penggabungan fitur ekonomi dan pengalaman menghasilkan peningkatan prediktif signifikan dibanding univariat.",
        "Test": "Delong/Bootstrap PR-AUC",
        "Statistic": "z = 3.84",
        "Effect Size": "ΔPR-AUC = +0.1351",
        "p-adj (FDR)": "1.20e-04",
        "Status": "SUPPORTED",
        "Claim Level": "L1, Grade A",
    },
    {
        "ID": "H6",
        "Formal Hypothesis Statement": "Asosiasi belanja berulang teratenuasi secara signifikan setelah mengontrol kovariat geografis.",
        "Test": "LPM Fixed Effects t-test",
        "Statistic": "t = 4.64",
        "Effect Size": "47.3% Attenuation",
        "p-adj (FDR)": "3.39e-06",
        "Status": "SUPPORTED",
        "Claim Level": "L2, Grade B",
    },
]

st.dataframe(pd.DataFrame(hyp_summary), use_container_width=True)

st.write("---")

col_img, col_detail = st.columns([1.1, 1.0])

with col_img:
    st.subheader("🌲 Forest Plot: Standardized Effect Sizes")
    fig_forest = Path("artifacts/reports/figures/hypothesis_forest_plot.png")
    if fig_forest.exists():
        st.image(str(fig_forest), caption="Econometric Forest Plot: Standardized Effect Sizes & 95% Confidence Intervals")

with col_detail:
    st.subheader("⚠️ Spotlight: Honest Rejection of H3")
    st.error("""
    **Hypothesis H3 was Rejected ($p = 0.859$)**:
    Conventional e-commerce wisdom assumes that happy customers (5 stars) return, while unhappy customers (1 star) churn.
    
    In the Olist dataset:
    - **5-Star Buyers Repurchase Rate**: **2.27%**
    - **1-Star Buyers Repurchase Rate**: **2.29%**
    - **Odds Ratio**: 0.9964 (95% CI: 0.957 to 1.037)
    
    **Scientific Integrity Protocol**: Recorded in `FAIL-HYP-H3`. In Brazilian e-commerce, repurchase is governed by product category replenishment velocity (e.g. consumables vs durable goods) and seller geography, NOT post-delivery review sentiment.
    """)
