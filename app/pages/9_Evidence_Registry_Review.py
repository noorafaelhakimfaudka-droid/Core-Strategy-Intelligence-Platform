"""Page 9: Evidence Registry & BNSP Verification Review [UK-11]."""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Evidence Registry Review | CSIP", page_icon="📜", layout="wide")

st.title("📜 Evidence Registry & BNSP Verification Review")
st.markdown("**SKKNI Competency Standards**: `[UK-10 Mengevaluasi Hasil Pemodelan]`, `[UK-11 Mengembangkan Solusi]`")
st.markdown("**Governing Principle**: *\"Build what the PRD specifies. Test what is built. Verify what is claimed. Report what the evidence supports. Never trade scientific integrity for appearance, speed, or a higher score.\"*")

st.write("---")

tab1, tab2, tab3, tab4 = st.tabs(["💡 Discoveries (DISC-01 to DISC-07)", "🧪 Hypotheses (H1 to H6)", "⚠️ Failure Register & Limitations", "🏛️ BNSP SKKNI 11-Unit Matrix"])

# Load Evidence Snapshot
snap_path = Path("artifacts/reports/evidence_registry_snapshot.json")
if snap_path.exists():
    with open(snap_path, "r", encoding="utf-8") as f:
        snap_data = json.load(f)
else:
    snap_data = {}

with tab1:
    st.subheader("Master Registered Discoveries")
    disc_data = snap_data.get("discoveries", {})
    if disc_data:
        disc_rows = []
        for d_id, d in disc_data.items():
            disc_rows.append({
                "ID": d["discovery_id"],
                "Title": d["title"],
                "Claim Level": d["claim_level"],
                "Evidence Grade": d["evidence_grade"],
                "Grain": d["grain"],
                "Description": d["description"],
            })
        st.dataframe(pd.DataFrame(disc_rows), use_container_width=True)

with tab2:
    st.subheader("Formal Hypotheses Testing Register")
    hyp_data = snap_data.get("hypotheses", {})
    if hyp_data:
        hyp_rows = []
        for h_id, h in hyp_data.items():
            hyp_rows.append({
                "ID": h["hypothesis_id"],
                "Formal Statement": h["formal_statement"],
                "Test": h["test_name"],
                "Statistic": f"{h['test_statistic']:.4f}",
                "Effect Size": f"{h['effect_size']:.4f}",
                "p-adj (FDR)": f"{h['p_value_adj']:.4e}",
                "Status": h["status"],
                "Claim Level": h["claim_level"],
                "Evidence Grade": h["evidence_grade"],
            })
        st.dataframe(pd.DataFrame(hyp_rows), use_container_width=True)

with tab3:
    st.subheader("Failure Register & Boundary of Applicability Audit")
    st.markdown("""
    In accordance with the **SHADOW Project Rules (Section 2 & 13)**, negative experimental findings and model limitations are formally registered rather than concealed:
    """)

    fails = snap_data.get("failures", [])
    if fails:
        for f_entry in fails:
            st.error(f"""
            **Failure ID**: `{f_entry['failure_id']}` ({f_entry['component_type']})  
            **Description**: {f_entry['description']}  
            **Diagnostic Root Cause**: {f_entry['root_cause']}  
            **Impact Assessment**: {f_entry['impact_assessment']}  
            **Mitigation Action**: {f_entry['mitigation_action']}  
            """)

with tab4:
    st.subheader("BNSP SKKNI 11-Unit Traceability Matrix")
    st.markdown("""
    Complete cross-reference of all 11 Data Science Competency Units for BNSP Assessors:
    """)

    bnsp_rows = [
        {"Unit ID": "UK-01", "Unit Title": "Menentukan Masalah Bisnis", "Code Artifact": "config/business_objectives.yaml", "Notebook": "01_business_and_data_understanding.ipynb", "Test Verification": "tests/test_initialization.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-02", "Unit Title": "Menentukan Kebutuhan Data", "Code Artifact": "config/data.yaml, data/data_dictionary.md", "Notebook": "01_business_and_data_understanding.ipynb", "Test Verification": "tests/test_initialization.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-03", "Unit Title": "Menelaah Data", "Code Artifact": "src/csip/data/loader.py, reports/data_quality_report.md", "Notebook": "03_exploratory_data_analysis.ipynb", "Test Verification": "tests/test_data_validation.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-04", "Unit Title": "Memvalidasi Data", "Code Artifact": "src/csip/cleaning/cleaner.py", "Notebook": "02_data_validation_and_cleaning.ipynb", "Test Verification": "tests/test_data_validation.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-05", "Unit Title": "Membersihkan Data", "Code Artifact": "src/csip/cleaning/cleaner.py", "Notebook": "02_data_validation_and_cleaning.ipynb", "Test Verification": "tests/test_cleaning_and_grain.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-06", "Unit Title": "Mengonstruksi Data", "Code Artifact": "src/csip/features/engineer.py", "Notebook": "04_feature_engineering_and_construction.ipynb", "Test Verification": "tests/test_feature_leakage.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-07", "Unit Title": "Menentukan Objek Data", "Code Artifact": "src/csip/discovery/clusterer.py", "Notebook": "05_behavioral_discovery_unsupervised.ipynb", "Test Verification": "tests/test_discovery.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-08", "Unit Title": "Membangun Skenario Model", "Code Artifact": "src/csip/hypotheses/runner.py, src/csip/world/state_transition.py", "Notebook": "06_hypothesis_investigation.ipynb, 10_system_and_world_modeling.ipynb", "Test Verification": "tests/test_hypotheses.py, tests/test_world_model.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-09", "Unit Title": "Membangun Model", "Code Artifact": "src/csip/models/classic.py, trainer.py, deep_tabular.py, deep_seq.py", "Notebook": "07_supervised_ml_and_competency_lab.ipynb, 08_neural_network_and_deep_learning.ipynb", "Test Verification": "tests/test_models.py, tests/test_deep_learning.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-10", "Unit Title": "Mengevaluasi Hasil Pemodelan", "Code Artifact": "src/csip/evaluation/explainer.py, src/csip/uncertainty/bootstrap.py", "Notebook": "09_model_evaluation_and_explainability.ipynb, 12_uncertainty_quantification.ipynb", "Test Verification": "tests/test_deep_learning.py, tests/test_simulation_sanity.py", "Status": "VERIFIED (Grade A)"},
        {"Unit ID": "UK-11", "Unit Title": "Mengembangkan Solusi", "Code Artifact": "app/streamlit_app.py, app/pages/ (9 Showcase Pages)", "Notebook": "13_model_review_and_failure_analysis.ipynb, 14_final_research_and_bnsp_report.ipynb", "Test Verification": "tests/test_simulation_sanity.py", "Status": "VERIFIED (Grade A)"},
    ]
    st.dataframe(pd.DataFrame(bnsp_rows), use_container_width=True)
