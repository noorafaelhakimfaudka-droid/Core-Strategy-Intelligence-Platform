"""Page 7: Alternative World Simulator [UK-08, UK-10, UK-11]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Alternative World Simulator | CSIP", page_icon="🔮", layout="wide")

st.title("🔮 Alternative World Simulator & Policy Scenarios")
st.markdown("**SKKNI Competency Standards**: `[UK-08 Membangun Skenario Model]`, `[UK-10 Mengevaluasi Hasil Pemodelan]`, `[UK-11 Mengembangkan Solusi]`")

st.write("---")

# Load precomputed simulation results
res_path = Path("artifacts/reports/scenario_simulation_results.json")
if res_path.exists():
    with open(res_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)
else:
    sim_data = {}

st.subheader("Interactive Policy Scenario Explorer")
selected_scenario_id = st.selectbox(
    "Select Counterfactual Policy Intervention to Inspect:",
    options=list(sim_data.keys()),
    format_func=lambda x: f"{x}: {sim_data[x]['name']}" if x in sim_data else x,
    index=2,  # Default to S2
)

if selected_scenario_id in sim_data:
    sc = sim_data[selected_scenario_id]
    cmp = sc.get("comparison_to_s0", {})
    guard = sc.get("guardrail", {})

    # Guardrail Alert Banner
    if guard.get("is_out_of_distribution", False):
        st.warning(f"⚠️ **Extrapolation Guardrail Triggered**: Max Z-Score = {guard.get('max_z_score', 0):.2f} (exceeds historical 3.5σ support envelope). Claim downgraded to **{guard.get('evidence_grade', 'Grade C')}**.")
    else:
        st.success(f"✅ **Extrapolation Guardrail Satisfied**: Simulated trajectory remains inside historical empirical envelope. **{guard.get('evidence_grade', 'Grade B')}**.")

    st.markdown(f"**Policy Description**: {sc['description']}")

    # Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("12-Wk Projected Volume", f"{int(round(sc['cumulative_volume'])):,} orders", f"{cmp.get('delta_volume_pct', 0):+.2f}% vs S0")
    m2.metric("Negative Review Rate", f"{sc['avg_negative_review_rate']*100:.2f}%", f"{cmp.get('delta_negative_review_pp', 0):+.2f} pp vs S0")
    m3.metric("Subsidy Cost", f"R$ {sc['subsidy_cost_brl']:,.2f}")
    m4.metric("Incremental GMV", f"R$ {cmp.get('incremental_gmv_brl', 0):,.2f}")
    m5.metric("Net Platform Profit", f"R$ {cmp.get('net_incremental_profit_brl', 0):,.2f}", f"ROI: {cmp.get('roi_ratio', 0)*100:.1f}%")

st.write("---")

st.subheader("📊 Comparative Scenario Trajectories (12 Weeks with 90% Prediction Intervals)")
fig_sc = Path("artifacts/reports/figures/scenario_simulations.png")
if fig_sc.exists():
    st.image(str(fig_sc), caption="Multi-Trajectory Residual Bootstrap: Volume, Dissatisfaction Risk, and Platform Return")

st.write("---")
st.subheader("📋 Full 6-Scenario Comparative Scorecard")
if sim_data:
    table_rows = []
    for s_id, s in sim_data.items():
        c = s.get("comparison_to_s0", {})
        table_rows.append({
            "Scenario ID": s_id,
            "Policy Name": s["name"],
            "12-Wk Volume": f"{int(round(s['cumulative_volume'])):,}",
            "Volume Lift (%)": f"{c.get('delta_volume_pct', 0):+.2f}%",
            "Review Rate (%)": f"{s['avg_negative_review_rate']*100:.2f}%",
            "Review Lift (pp)": f"{c.get('delta_negative_review_pp', 0):+.2f} pp",
            "Subsidy Cost": f"R$ {s['subsidy_cost_brl']:,.2f}",
            "Net Profit": f"R$ {c.get('net_incremental_profit_brl', 0):,.2f}",
            "Guardrail Status": "PASS" if not s["guardrail"]["is_out_of_distribution"] else "OOD WARN",
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
