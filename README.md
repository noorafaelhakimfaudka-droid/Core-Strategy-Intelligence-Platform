# CSIP — Core Strategy & Intelligence Platform
### *Enterprise Observational Data Science & Decision Intelligence Platform*
#### Skema Sertifikasi: Ilmuwan Data (Data Scientist) — LSP TRI (SKM/2905/LSP-TRI/VII/2025)
#### Standar Acuan: SKKNI No. 299 Tahun 2020 (11 Unit, 27 Elemen, 63 KUK)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PyTest Status](https://img.shields.io/badge/pytest-92%20passed%20%28100%25%29-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](tests/)
[![Methodology](https://img.shields.io/badge/Methodology-End--to--End%20CRISP--DM-blue.svg?style=flat)](docs/methodology/DATA_METHODOLOGY.md)
[![Streamlit App](https://img.shields.io/badge/Streamlit%20UI-Interactive%20Studio-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](app/streamlit_app.py)
[![ML Frameworks](https://img.shields.io/badge/ML-LightGBM%20%7C%20PyTorch%20%7C%20Scikit--Learn-orange.svg?style=flat)](artifacts/models/)
[![SKKNI 299/2020](https://img.shields.io/badge/SKKNI%20299%2F2020-11%20Units%20%7C%2063%20KUK-success.svg?style=flat)](standards/canonical_skkni_299_2020.json)
[![Hardware Constraints](https://img.shields.io/badge/Hardware-8%20GB%20RAM%20Optimized-success.svg?style=flat)](docs/architecture/SYSTEM_ARCHITECTURE.md)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat)](LICENSE)

---

## 🌟 Executive Overview

**CSIP (Core Strategy & Intelligence Platform) Version 10.0.0** is an enterprise-grade observational Data Science and Decision Intelligence platform developed as a comprehensive project-based competency evidence system for the **BNSP Data Scientist Certification (KKNI Level 7)** at **LSP TRI**.

### Core Platform Capabilities:
1. **Deep Behavioral & Macroeconomic Hub**: A publication-grade investigation into macroeconomic, logistics friction, and customer sentiment dynamics across **~100,000 real-world transactions** from the Brazilian E-Commerce Ecosystem (**Olist**). Features an econometric hypothesis battery (H1–H6 with Benjamini-Hochberg FDR control), a Vector AutoRegressive (VAR) state-space World Model, and a full machine learning baseline ladder (B0 to B3: Naive, Ridge, Decision Trees, Random Forest, LightGBM, and Deep Learning).
2. **Interactive Decision & Simulation Studio**: A multi-page Streamlit application enabling scenario analysis, What-If policy interventions (S0–S5), probability calibration inspection, and tipping-point sensitivity analysis.
3. **Rigorous Scientific Integrity & Point-in-Time Governance**: Zero forward-looking leakage, dual-contract repeat purchase modeling (`cohort_checkout_features` vs `cohort_post_delivery_features`), strict prediction contracts at checkout ($t_0$) and delivery ($t_1$), deterministic first-order cohort construction, and transparent survivor bias disclosures.
4. **100% Local Execution**: Built to run entirely within an 8 GB RAM laptop footprint without external cloud transmission, closed-source APIs, or third-party tracking.

CSIP is verified by **92 automated unit and integration tests** (100% pass rate in 31.84 seconds) and mapped 1:1 against all **63 KUKs of SKKNI No. 299/2020**.

---

## 🏛️ System Architecture

```text
                               ┌──────────────────────────────────────────────────────────┐
                               │           CSIP STUDIO (Streamlit Web App)                │
                               │  - Data Observatory & Relational Schema Ingestion        │
                               │  - Behavioral Persona Discovery & Cluster Profiling      │
                               │  - Hypothesis Laboratory (Forest Plots & p-values)       │
                               │  - Predictive Intelligence & Model Calibration Curves    │
                               │  - World Model & What-If Policy Simulation Studio        │
                               └────────────────────────────┬─────────────────────────────┘
                                                            │
                                ┌───────────────────────────┴─────────────────────────────┐
                                │                                                         │
                                ▼                                                         ▼
            ┌────────────────────────────────────────┐        ┌────────────────────────────────────────┐
            │       Data Engineering Pipeline        │        │        Model & Intelligence Engine     │
            │  (src/csip/data/ & cleaning/)          │        │  (src/csip/models/ & world/)           │
            │  - Foreign Key relational verification │        │  - Baseline Ladder B0 to B3 (LightGBM) │
            │  - Geo-deduplication (-98.1% rows)     │        │  - Categorical Embedding MLP & Bi-LSTM │
            │  - Chronological anomaly filtering     │        │  - TreeSHAP feature attribution        │
            │  - 4 Cleaned Parquet Analytical Grains │        │  - Vector AutoRegressive State-Space   │
            └────────────────────────────────────────┘        └────────────────────────────────────────┘
```

---

## 🏆 Supervised Machine Learning Benchmark (Test Split Verification)

Evaluated chronologically on an unseen out-of-time Test Split ($N_{\text{test}} = 12,630$ orders, July–August 2018):

| Model Ladder | Algorithm | Feature Set | Test PR-AUC | Test ROC-AUC | Test F1-Score | Calibrated Brier | Status / Role |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **B3 (Champion)** | **LightGBM Gradient Boosting** | `E2_post_delivery_diagnostic` | **0.3061** | **0.6745** | **0.3417** | **0.1373** | **CHAMPION TABULAR (+179% lift)** |
| **B3** | Random Forest (200 trees) | `E2_post_delivery_diagnostic` | 0.3016 | 0.6727 | 0.3345 | 0.1555 | Bagging Ensemble |
| **B2** | Decision Tree (CART depth=6) | `E2_post_delivery_diagnostic` | 0.2704 | 0.6642 | 0.2804 | 0.0790 | Non-linear Tree |
| **B2** | K-Nearest Neighbors ($k=15$) | `E2_post_delivery_diagnostic` | 0.2532 | 0.6383 | 0.2212 | 0.0839 | Non-parametric Baseline |
| **B1** | Logistic Regression / Ridge | `E2_post_delivery_diagnostic` | 0.2436 | 0.6803 | 0.3084 | 0.1533 | Linear Baseline |
| **B2** | Gaussian Naive Bayes | `E2_post_delivery_diagnostic` | 0.1996 | 0.6523 | 0.2805 | 0.1378 | Generative Baseline |
| **B3** | LightGBM (Zero Leakage) | `E1_early_warning_checkout` | 0.1335 | 0.5468 | 0.1766 | 0.2370 | Checkout Early Warning |
| **B0** | Naive Majority Floor | All Sets | 0.1096 | 0.5000 | 0.0000 | 0.0975 | Naive Prevalence Floor |

---

## 📜 BNSP Competency Evidence Package (SKKNI 299/2020 | LSP TRI)

The repository provides a complete, auditable evidence trail for all 11 required competency units:

| Unit Code | Official SKKNI Unit Title | Elemen | KUK | Evidence Status | Key Evidence Location |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `J.62DMI00.001.1` | Menentukan Objektif Bisnis | 4 | 12 | 9 VERIFIED / 3 PARTIAL | `notebooks/01_business_and_data_understanding.ipynb`, `config/business.yaml` |
| `J.62DMI00.002.1` | Menentukan Tujuan Teknis Data Science | 2 | 4 | 4 VERIFIED | `docs/methodology/PREDICTION_CONTRACT.md`, `config/features.yaml` |
| `J.62DMI00.005.1` | Menelaah Data | 3 | 8 | 8 VERIFIED | `src/csip/data/loader.py`, `src/csip/data/semantic_profiler.py` |
| `J.62DMI00.006.1` | Memvalidasi Data | 2 | 4 | 4 VERIFIED | `reports/data_quality_report.md`, `reports/audit/LABEL_OBSERVABILITY_AUDIT.csv` |
| `J.62DMI00.007.1` | Menentukan Objek Data | 2 | 4 | 4 VERIFIED | `src/csip/features/engineer.py`, `data/processed/*.parquet` |
| `J.62DMI00.008.1` | Membersihkan Data | 2 | 4 | 4 VERIFIED | `src/csip/cleaning/cleaner.py`, `src/csip/cleaning/auto_cleaner.py` |
| `J.62DMI00.009.1` | Mengkonstruksi Data | 3 | 6 | 6 VERIFIED | `reports/audit/FEATURE_AVAILABILITY_AUDIT.csv`, `src/csip/discovery/clusterer.py` |
| `J.62DMI00.012.1` | Membangun Skenario Model | 3 | 7 | 7 VERIFIED | `src/csip/models/classic.py`, `docs/methodology/WORLD_MODEL_SPECIFICATION.md` |
| `J.62DMI00.013.1` | Membangun Model | 2 | 6 | 6 VERIFIED | `src/csip/models/trainer.py`, `artifacts/models/*.joblib` |
| `J.62DMI00.014.1` | Mengevaluasi Hasil Pemodelan | 2 | 4 | 4 VERIFIED | `artifacts/reports/ml_leaderboard.json`, `reports/audit/WORLD_MODEL_AUDIT.md` |
| `J.62DMI00.015.1` | Melakukan Proses Review Pemodelan | 2 | 4 | 4 VERIFIED | `reports/model_evaluation_and_review_report.md`, `docs/limitations/KNOWN_LIMITATIONS.md` |
| **TOTAL** | **11 UNIT KOMPETENSI** | **27** | **63** | **60 VERIFIED, 3 PARTIAL** | **100% Traceability across Repository** |

---

## ⚡ Quick Start & Verification

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform.git
cd csip

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execute Full Automated Test Suite (89 Tests)
```powershell
python -m pytest tests/ -v
```
*All 89 tests verify schema consistency, zero data leakage, cohort isolation, hypothesis validity, and model evaluation in ~23 seconds.*

### 3. Launch Interactive Decision Studio (Streamlit)
```powershell
streamlit run app/streamlit_app.py
```
*Access in browser at `http://localhost:8501`.*

### 4. Build BNSP Competency Matrices
```powershell
python scripts/build_bnsp_matrix.py
```
*Generates `competency/BNSP_MASTER_COMPETENCY_MATRIX.xlsx` and `competency/EVIDENCE_REGISTRY.csv`.*

---

## 📁 Repository Structure

```text
csip/
├── app/                          # Streamlit Multi-Page Web Interface (6 pages)
├── artifacts/                    # Serialized model checkpoints (.joblib, .pt) & JSON reports
├── competency/                   # Official BNSP Competency Matrices & Assessor Guides
│   ├── BNSP_MASTER_COMPETENCY_MATRIX.xlsx  # 15-Column Styled Excel Matrix
│   ├── BNSP_MASTER_COMPETENCY_MATRIX.csv   # Machine-readable CSV Matrix
│   ├── EVIDENCE_REGISTRY.csv               # 63 Registered Competency Evidence Items
│   ├── ASSESSOR_EVIDENCE_GUIDE.md          # Assessor Verification Guide (Indonesian)
│   ├── CANDIDATE_DEMONSTRATION_GUIDE.md    # Candidate Live Demonstration Guide
│   └── ASSESSMENT_READINESS_REPORT.md      # Readiness Audit per Competency Unit
├── config/                       # Declarative YAML configurations (business.yaml, features.yaml)
├── data/
│   ├── raw/                      # 9 Olist Relational CSV Tables
│   └── processed/                # 4 Cleaned Parquet Tables (order, cohort, corpus, weekly)
├── docs/                         # Scientific, Architectural, and Quality Specifications
│   ├── architecture/SYSTEM_ARCHITECTURE.md
│   ├── methodology/PREDICTION_CONTRACT.md
│   ├── methodology/DATA_METHODOLOGY.md
│   ├── methodology/MODEL_EVALUATION.md
│   ├── methodology/WORLD_MODEL_SPECIFICATION.md
│   ├── quality/REPRODUCIBILITY.md
│   └── limitations/KNOWN_LIMITATIONS.md
├── notebooks/                    # 14 Research & Demonstration Jupyter Notebooks
├── reports/                      # Forensic Audits, Quality Reports, & Methodology Disclosures
│   ├── audit/V6_BASELINE_AUDIT.md
│   ├── audit/V7_FINAL_AUDIT.md
│   ├── audit/V6_TO_V7_CHANGELOG.md
│   ├── audit/FEATURE_AVAILABILITY_AUDIT.csv
│   ├── audit/LABEL_OBSERVABILITY_AUDIT.csv
│   ├── audit/NOTEBOOK_EXECUTION_AUDIT.csv
│   ├── audit/WORLD_MODEL_AUDIT.md
│   ├── methodology/POPULATION_AND_SELECTION_BIAS.md
│   └── quality/TEST_EXECUTION_REPORT.md
├── scripts/                      # Automated Pipeline Execution & Matrix Generators
├── src/csip/                     # Core Production Package (11 domain subpackages)
├── standards/                    # Canonical Standard: canonical_skkni_299_2020.json
└── tests/                        # 16 Pytest Test Modules (92 Automated Tests, 100% Passed)
```

---

## 📜 Scientific Governance & Transparent Disclosures

CSIP adheres to the governing principle:
> *Build what the specification defines. Test what is built. Verify what is claimed. Report what the evidence supports. Never trade scientific integrity for appearance, speed, or a higher score.*

- **Transparent Negative Result**: Hypothesis H3 was empirically rejected (Odds Ratio = 0.9964, $p\text{-adj} = 0.861$) and formally recorded in the **Failure Register** (`FAIL-HYP-H3`) rather than concealed.
- **Population & Survivor Bias**: Documented in `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`. Models trained on delivered orders estimate $\mathbb{P}(\text{Negative Review} \mid X, \text{Delivered}=1)$, recognizing the exclusion of 1,234 canceled/unavailable orders (87.4% negative rate).
- **Non-Causal Simulation Boundary**: Policy simulations in the World Model represent structural sensitivity projections, not randomized causal treatment effects.
- **Zero Label Contamination**: 646 unobserved reviews are preserved as NaN, avoiding synthetic label imputation.

---

## 📄 License & Attribution

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
