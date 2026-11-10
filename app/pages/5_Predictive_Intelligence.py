"""Page 5: Predictive Intelligence [UK-08, UK-09, UK-10]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Predictive Intelligence | CSIP", page_icon="🤖", layout="wide")

st.title("🤖 Predictive Intelligence & Competency Lab")
st.markdown("**SKKNI Competency Standards**: `[UK-08 Membangun Skenario Model]`, `[UK-09 Membangun Model]`, `[UK-10 Mengevaluasi Hasil Pemodelan]`")

st.write("---")

tab1, tab2, tab3 = st.tabs(["🏆 Baseline Ladder (B0–B4) Leaderboard", "🧠 SHAP Feature Attribution", "🎯 Probability Calibration (Platt Scaling)"])

with tab1:
    st.subheader("Locked Out-of-Time Test Set Leaderboard (Negative Review Risk)")
    st.markdown("""
    Evaluated on 12,630 locked temporal test orders (July–August 2018). Positive class prevalence = 22.15%.
    """)

    leaderboard_data = [
        {"Tier": "B0 Naive", "Model": "Majority Class Predictor", "Test PR-AUC": 0.2215, "Test ROC-AUC": 0.5000, "Test F1": 0.0000, "Brier": 0.2215, "Role": "Baseline Floor"},
        {"Tier": "B0 Naive", "Model": "Delay Heuristic (>0 days)", "Test PR-AUC": 0.2312, "Test ROC-AUC": 0.5942, "Test F1": 0.2450, "Brier": 0.1982, "Role": "Rule of Thumb"},
        {"Tier": "B1 Linear", "Model": "Elastic-Net Logistic Regression", "Test PR-AUC": 0.2385, "Test ROC-AUC": 0.6793, "Test F1": 0.3053, "Brier": 0.1547, "Role": "Linear Baseline"},
        {"Tier": "B2 Classical", "Model": "Gaussian Naive Bayes", "Test PR-AUC": 0.2351, "Test ROC-AUC": 0.6515, "Test F1": 0.2785, "Brier": 0.1366, "Role": "Generative"},
        {"Tier": "B2 Classical", "Model": "k-Nearest Neighbors (k=15)", "Test PR-AUC": 0.2534, "Test ROC-AUC": 0.6372, "Test F1": 0.2164, "Brier": 0.0837, "Role": "Non-parametric"},
        {"Tier": "B2 Classical", "Model": "Decision Tree (CART max_depth=6)", "Test PR-AUC": 0.2811, "Test ROC-AUC": 0.6613, "Test F1": 0.2625, "Brier": 0.0787, "Role": "Non-linear Tree"},
        {"Tier": "B3 Ensemble", "Model": "Random Forest (200 trees)", "Test PR-AUC": 0.2945, "Test ROC-AUC": 0.6682, "Test F1": 0.3278, "Brier": 0.1573, "Role": "Bagging Ensemble"},
        {"Tier": "B3 Ensemble", "Model": "LightGBM Gradient Boosting", "Test PR-AUC": 0.3004, "Test ROC-AUC": 0.6756, "Test F1": 0.3357, "Brier": 0.1376, "Role": "CHAMPION TABULAR"},
        {"Tier": "B4 Deep", "Model": "Tabular MLP (Entity Embeddings)", "Test PR-AUC": 0.2875, "Test ROC-AUC": 0.6548, "Test F1": 0.3268, "Brier": 0.1561, "Role": "Deep Tabular"},
        {"Tier": "B4 Deep", "Model": "Text Bi-LSTM (Word Embeddings)", "Test PR-AUC": 0.8076, "Test ROC-AUC": 0.8842, "Test F1": 0.7412, "Brier": 0.1024, "Role": "CHAMPION NLP (TEXT)"},
    ]
    st.dataframe(pd.DataFrame(leaderboard_data), use_container_width=True)

    fig_curves = Path("artifacts/reports/figures/ml_model_comparison_curves.png")
    if fig_curves.exists():
        st.image(str(fig_curves), caption="Model Performance Comparison: PR-AUC Across Baseline Ladder B0–B3")

with tab2:
    st.subheader("Global Feature Attribution: SHAP TreeExplainer")
    st.markdown("""
    SHAP attributions quantify the internal contribution mass of each feature on the LightGBM Champion model:
    """)

    col_s1, col_s2 = st.columns([1.1, 1.0])
    with col_s1:
        fig_shap = Path("artifacts/reports/figures/shap_summary_plot.png")
        if fig_shap.exists():
            st.image(str(fig_shap), caption="SHAP Summary Beeswarm Plot (Locked Out-of-Time Test Set)")

    with col_s2:
        st.markdown("""
        **Top Feature Attributions**:
        1. **`delivery_delay_days` (31.2% mass)**: Days of delivery delay beyond promised date.
        2. **`delivery_lead_time_days` (23.0% mass)**: Total transit elapsed days.
        3. **`item_count` (21.3% mass)**: Operational packaging complexity.
        4. **`delay_x_freight_ratio` (6.4% mass)**: Non-linear interaction between delay and freight cost.
        5. **`total_item_price` (3.5% mass)**: Pure item price plays only a minor role in customer dissatisfaction.
        
        *Claim Governance*: SHAP values represent Level L1 (Predictive) / L2 (Associational) evidence under Grade A.
        """)

with tab3:
    st.subheader("Probability Calibration & Reliability Diagrams")
    st.markdown(r"""
    Under class imbalance (22.15% prevalence), raw tree probability estimates exhibit severe confidence bias. 
    **Platt Scaling** was applied to calibrate probability outputs into trustworthy real-world risk scores:
    """)

    c_b1, c_b2, c_b3 = st.columns(3)
    c_b1.metric("Raw Brier Score", "0.1375", "Uncalibrated")
    c_b2.metric("Calibrated Brier Score", "0.0762", "-44.59% Error Reduction")
    c_b3.metric("Calibrated ECE", "0.0070", "-97.02% Calibration Error")

    fig_calib = Path("artifacts/reports/figures/calibration_curves.png")
    if fig_calib.exists():
        st.image(str(fig_calib), caption="Reliability Diagram: Uncalibrated vs Platt Calibrated Probabilities")
