# CSIP — Computational Society Intelligence Platform
### *Universal Data Scientist & Decision Simulator*
**Master Portfolio & SKKNI BNSP Data Science Certified Research Architecture**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PyTest Status](https://img.shields.io/badge/pytest-72%20passed%20%28100%25%29-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](tests/)
[![SKKNI BNSP](https://img.shields.io/badge/SKKNI%20Data%20Science-11%2F11%20Competency%20Units%20Verified-blue.svg?style=flat)](reports/skkni_bnsp_traceability_matrix.md)
[![Streamlit App](https://img.shields.io/badge/Streamlit%20UI-Interactive%20Studio-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](app/streamlit_app.py)
[![ML Frameworks](https://img.shields.io/badge/ML-LightGBM%20%7C%20PyTorch%20%7C%20Scikit--Learn-orange.svg?style=flat)](artifacts/models/)
[![Hardware Constraints](https://img.shields.io/badge/Hardware-8%20GB%20RAM%20Optimized-success.svg?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat)](LICENSE)

---

## 🌟 Executive Overview

**CSIP (Computational Society Intelligence Platform)** is a production-grade observational data science and automated decision intelligence platform. It operates in two unified operational modes:

1. **CSIP Studio (Universal Adaptive Decision Simulator)**: A drag-and-drop web studio that accepts **any tabular dataset** (e.g., e-commerce, sports facility reservations, logistics, healthcare, HR). It autonomously profiles semantic roles, trains machine learning models on the fly, computes continuous response curves, identifies mathematical **critical tipping points**, and generates deterministic strategic recommendations from **"Nara"** (Strategic AI Advisor) with **zero hallucination** and **zero hardcoded templates**.
2. **Deep Behavioral & Macroeconomic Research Hub**: A comprehensive, publication-grade investigation into macroeconomic and behavioral dynamics across **~100,000 real-world customer transactions** in the Brazilian E-Commerce Ecosystem (**Olist**). It validates 6 econometric hypotheses, features a state-space macroeconomic world model, and implements a full baseline ladder from naive heuristics to Tabular MLPs and Bi-LSTM neural networks.

CSIP is strictly aligned with the **Standar Kompetensi Kerja Nasional Indonesia (SKKNI) Data Science** (11 Unit Kompetensi) and verified by **72 automated test suites**.

---

## 🚀 Key Highlights & Capabilities

### 1. Universal Semantic Profiler & Zero-Hardcode Architecture
- **Dynamic Variable Ingestion**: Ingests arbitrary CSV files and dynamically classifies columns into intuitive roles: *Primary Target*, *Numerical Levers*, *Categorical Levers*, and *Informational Context*.
- **Scale-Aware Preprocessing**: Automatically formats currency, ratios, and discrete groups into human-readable units (e.g., $0-1$ binary active/inactive flags, multi-class discrete groups, and thousand/million abbreviations) without modifying underlying mathematical values.
- **Cross-Device Robustness**: Pure CSS grid and container-query layouts designed to maintain proportional fidelity and responsive typography across phones, laptops, and ultra-wide external monitors.

### 2. Live Machine Learning & Tipping Point Engine
- **Instantaneous On-the-Fly Modeling**: Trains high-speed tabular regressors (`LightGBM` / `Ridge` / `RandomForest`) dynamically on user-provided data.
- **Continuous Marginal Simulation Curves**: Evaluates 50 uniform marginal points across the slider domain with Gaussian filter smoothing to reveal true non-linear relationships.
- **Mathematical Inflection Points**: Pinpoints the exact tipping point ($x_{\text{critical}} = \arg\max |\Delta y / \Delta x|$) where a metric shifts rapidly, providing data-backed thresholds for policy intervention.
- **Zero-Hallucination Explanations**: Recommendations from the strategic persona ("Nara") are strictly bound to statistical outputs: normalized feature importance, Pearson correlation $r$, $p$-values, and empirical validation errors ($\pm\text{MAE}$).

### 3. Rigorous Macroeconomic Research (Olist 100k Dataset)
- **7 Master Discoveries (DISC-01 to DISC-07)**: Quantifies the asymmetric impact of delivery delays, freight elasticity, and customer cohort retention dynamics.
- **Benjamini-Hochberg FDR Controlled Hypotheses**: Tests 6 formal hypotheses (H1–H6) with false discovery rate corrections ($q = 0.05$).
- **Transparent Failure Protocol**: Hypothesis H3 was empirically rejected (Odds Ratio = 0.9964, $p$-adj = 0.859) and formally documented in the **Failure Register** (`FAIL-HYP-H3`) rather than concealed.
- **Macro State-Space World Model**: Linear state-transition matrix recovering system dynamics with $0.33\%$ parameter error and $15.83\%$ volume WAPE over 87 consecutive weeks.

---

## 🏛️ System Architecture

```text
                               ┌──────────────────────────────────────────────────────────┐
                               │           CSIP STUDIO (Streamlit Web App)                │
                               │  - Universal CSV Ingestion & Semantic X-Ray             │
                               │  - Interactive Simulation Sliders & Decision Levers      │
                               │  - Continuous Marginal Prediction Curves                 │
                               │  - Tipping Point Detection & Grounded Strategic Advisor  │
                               └────────────────────────────┬─────────────────────────────┘
                                                            │
                                ┌───────────────────────────┴─────────────────────────────┐
                                │                                                         │
                                ▼                                                         ▼
            ┌────────────────────────────────────────┐        ┌────────────────────────────────────────┐
            │       Universal Auto-Engine            │        │     Olist Macroeconomic Hub            │
            │  (src/csip/data/semantic_profiler.py)  │        │  (14 Pre-Rendered Research Notebooks)  │
            │  - Dynamic schema role inference       │        │  - 01 Data Understanding               │
            │  - Live Ridge/LGBM model training      │        │  - 02 Schema Validation & Cleaning     │
            │  - Inflection point derivative search  │        │  - 03 Exploratory Data Analysis (EDA)  │
            │  - Grounded deterministic narrative    │        │  - 04 Feature Engineering (Anti-Leak)  │
            └────────────────────────────────────────┘        │  - 05 Behavioral Clustering (K-Means)  │
                                                              │  - 06 Hypothesis Testing (H1 - H6)     │
                                                              │  - 07 Supervised ML (B0 - B3 Models)   │
                                                              │  - 08 Deep Learning (MLP & Bi-LSTM)    │
                                                              │  - 09 SHAP Explainability & Calib      │
                                                              │  - 10 State-Space World Model          │
                                                              │  - 11 Alternative World Simulator      │
                                                              │  - 12 Uncertainty Quantification       │
                                                              │  - 13 Model Review & Failure Audit     │
                                                              │  - 14 Final Research & BNSP Matrix     │
                                                              └────────────────────────────────────────┘
```

---

## 📓 14 Research Notebooks (Pre-Rendered & Executed)

All 14 notebooks in `notebooks/` are **fully executed with complete pre-rendered visual outputs, charts, and tables**:

| # | Notebook | SKKNI Unit | Key Algorithms / Techniques | Status |
| :-: | :--- | :--- | :--- | :-: |
| **01** | [`01_business_and_data_understanding.ipynb`](notebooks/01_business_and_data_understanding.ipynb) | UK-01, UK-02, UK-03 | Business framing, CRISP-DM, data profiling (9 tables, 100k rows) | ✅ Executed |
| **02** | [`02_data_validation_and_cleaning.ipynb`](notebooks/02_data_validation_and_cleaning.ipynb) | UK-04, UK-05, UK-06 | Temporal sanity, schema integrity, deduplication, cohort definition | ✅ Executed |
| **03** | [`03_exploratory_data_analysis.ipynb`](notebooks/03_exploratory_data_analysis.ipynb) | UK-03 | Bivariate distributions, log transforms, weekly order trend analysis | ✅ Executed |
| **04** | [`04_feature_engineering_and_construction.ipynb`](notebooks/04_feature_engineering_and_construction.ipynb) | UK-07 | Anti-leakage temporal splitting, interaction ratios, log scaling | ✅ Executed |
| **05** | [`05_behavioral_discovery_unsupervised.ipynb`](notebooks/05_behavioral_discovery_unsupervised.ipynb) | UK-09 | $K$-Means clustering ($k=4$), PCA projection, silhouette evaluation | ✅ Executed |
| **06** | [`06_hypothesis_investigation.ipynb`](notebooks/06_hypothesis_investigation.ipynb) | UK-08, UK-09 | ANOVA, OLS regression, Forest Plot, Benjamini-Hochberg FDR | ✅ Executed |
| **07** | [`07_supervised_ml_and_competency_lab.ipynb`](notebooks/07_supervised_ml_and_competency_lab.ipynb) | UK-08, UK-09 | LogReg, Decision Trees, Random Forest, LightGBM, Naive Bayes, KNN | ✅ Executed |
| **08** | [`08_neural_network_and_deep_learning.ipynb`](notebooks/08_neural_network_and_deep_learning.ipynb) | UK-09 | PyTorch Tabular MLP (Entity Embeddings) & Text Bi-LSTM | ✅ Executed |
| **09** | [`09_model_evaluation_and_explainability.ipynb`](notebooks/09_model_evaluation_and_explainability.ipynb) | UK-10 | Platt Scaling (Brier calibration), TreeSHAP feature importance | ✅ Executed |
| **10** | [`10_system_and_world_modeling.ipynb`](notebooks/10_system_and_world_modeling.ipynb) | UK-09, UK-10 | State-transition matrix $\Phi$, backtesting replay, parameter recovery | ✅ Executed |
| **11** | [`11_alternative_world_simulation.ipynb`](notebooks/11_alternative_world_simulation.ipynb) | UK-08, UK-10 | Counterfactual interventions (S0–S5), carrier SLA optimization | ✅ Executed |
| **12** | [`12_uncertainty_quantification.ipynb`](notebooks/12_uncertainty_quantification.ipynb) | UK-10 | Residual bootstrapping (95% PI), Mahalanobis OOD guardrails | ✅ Executed |
| **13** | [`13_model_review_and_failure_analysis.ipynb`](notebooks/13_model_review_and_failure_analysis.ipynb) | UK-11 | Feature ablation studies, Evidence Registry, Failure Analysis (H3) | ✅ Executed |
| **14** | [`14_final_research_and_bnsp_report.ipynb`](notebooks/14_final_research_and_bnsp_report.ipynb) | UK-01 to UK-11 | Executive summary, BNSP competency matrix, scientific audit trail | ✅ Executed |

---

## 🏆 Machine Learning Baseline Ladder (B0 to B4)

Evaluated on a strictly locked, temporal out-of-time test set ($N_{\text{test}} = 12,630$ orders, July–August 2018):

| Baseline Tier | Model Architecture | Feature Set | Test PR-AUC | Test ROC-AUC | Test F1-Score | Calibrated Brier | Role |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **B0** | Majority Class Predictor | None | 0.2215 | 0.5000 | 0.0000 | 0.2215 | Naive Floor |
| **B0** | Delay Heuristic (>0 days) | Delay | 0.2312 | 0.5942 | 0.2450 | 0.1982 | Rule-of-Thumb |
| **B1** | Logistic Regression | E3 Full | 0.2385 | 0.6793 | 0.3053 | 0.1547 | Linear Baseline |
| **B2** | Gaussian Naive Bayes | E3 Full | 0.2351 | 0.6515 | 0.2785 | 0.1366 | Generative |
| **B2** | $k$-Nearest Neighbors ($k=15$) | E3 Full | 0.2534 | 0.6372 | 0.2164 | 0.0837 | Non-parametric |
| **B2** | Decision Tree (CART depth=6) | E3 Full | 0.2811 | 0.6613 | 0.2625 | 0.0787 | Non-linear Tree |
| **B3** | Random Forest (200 trees) | E3 Full | 0.2945 | 0.6682 | 0.3278 | 0.1573 | Bagging Ensemble |
| **B3** | **LightGBM Gradient Boosting** | **E3 Full** | **0.3004** | **0.6756** | **0.3357** | **0.0762** | **CHAMPION TABULAR** |
| **B4** | Tabular MLP (Entity Embeddings) | Cat + Cont | 0.2875 | 0.6548 | 0.3268 | 0.1561 | Deep Neural Net |
| **B4** | **Text Bi-LSTM (Word Embeddings)**| Review Text | **0.8076** | **0.8842** | **0.7412** | **0.1024** | **CHAMPION NLP (TEXT)**|

---

## ⚡ Quick Start & Installation

### 1. Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/csip.git
cd csip

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch CSIP Studio (Streamlit Dashboard)
```bash
streamlit run app/streamlit_app.py
```
*Open your browser at `http://localhost:8501`. Upload your own CSV dataset (e.g., sales, operations, customer feedback) or explore the pre-loaded Olist Macroeconomic Showcase!*

### 3. Run Automated PyTest Verification (72 Tests)
```bash
python -m pytest tests/ -v
```
*All 72 tests verify artifact parity, data validation, leak-free feature pipelines, statistical hypotheses, and interactive engine stability in under 25 seconds.*

---

## 📁 Repository Structure

```text
csip/
├── app/
│   ├── streamlit_app.py          # Unified CSIP Studio Dashboard
│   ├── style.css                 # Cross-device responsive design & modern theme
│   ├── ui_components.py          # Grounded KPI cards, sliders, and Nara recommendations
│   ├── components/
│   │   └── charts.py             # Plotly interactive charting engine
│   └── pages/                    # 9 Multi-Page Observatories
│       ├── 1_Executive_Overview.py
│       ├── 2_Data_Observatory.py
│       ├── 3_Behavioral_Discovery_Lab.py
│       ├── 4_Hypothesis_Laboratory.py
│       ├── 5_Predictive_Intelligence.py
│       ├── 6_World_Model.py
│       ├── 7_Alternative_World_Simulator.py
│       ├── 8_Decision_Studio.py
│       └── 9_Evidence_Registry_Review.py
├── src/csip/                     # Core Production Package Engine
│   ├── cleaning/                 # Automated data cleaning & grain consistency
│   ├── data/                     # Semantic Profiler & data loader
│   ├── discovery/                # Behavioral clustering (K-Means & PCA)
│   ├── engine/                   # Decision engine & text constellation
│   ├── evaluation/               # TreeSHAP explainer & Platt calibration
│   ├── evidence/                 # EvidenceRegistry & Failure logging
│   ├── features/                 # Anti-leakage feature engineering
│   ├── hypotheses/               # Econometric hypothesis testing runner
│   ├── models/                   # Classical ML, Tabular MLP, & Bi-LSTM
│   ├── scenarios/                # Counterfactual what-if simulator
│   ├── uncertainty/              # Residual bootstrap & prediction intervals
│   └── world/                    # Macro state-space transition world model
├── notebooks/                    # 14 Pre-Rendered Research Notebooks (Modules 01 - 14)
├── reports/                      # 7 Comprehensive Written Research & BNSP Reports
│   ├── data_quality_report.md
│   ├── discovery_report.md
│   ├── evidence_and_failure_register.md
│   ├── hypothesis_report.md
│   ├── model_evaluation_and_review_report.md
│   ├── scenario_simulation_report.md
│   └── skkni_bnsp_traceability_matrix.md
├── artifacts/                    # Precomputed model checkpoints, JSONs, & figures
│   ├── models/                   # Trained .joblib & .pt model checkpoints
│   ├── reports/                  # Precomputed evaluation JSONs
│   └── reports/figures/          # 9 High-resolution diagnostic figures
├── data/
│   ├── raw/                      # Original 9 Olist CSV tables
│   ├── interim/                  # Cleaned & deduplicated Parquet tables
│   └── processed/                # 4 Core Analytical Grains (order, cohort, review, weekly)
├── config/                       # Declarative YAML configurations
├── tests/                        # 72 Automated PyTest Unit & Integration Tests
└── requirements.txt              # Pinned production dependencies
```

---

## 📜 Scientific Governance & Honest Failure Protocol

CSIP strictly follows the **Governing Scientific Principle**:
> *Build what the PRD specifies. Test what is built. Verify what is claimed. Report what the evidence supports. Never trade scientific integrity for appearance, speed, or a higher score.*

- **Transparent Negative Findings**: When hypothesis H3 failed to demonstrate statistical significance (Odds Ratio = 0.9964, $p\text{-adj} = 0.859$), the system did not manipulate features or p-hack the result. Instead, it was formally registered in the **Failure Register** (`FAIL-HYP-H3`) and highlighted as an empirical discovery.
- **Extrapolation Guardrails**: When counterfactual scenarios generate out-of-distribution states exceeding $3.5\sigma$, the system automatically flags the simulation as extrapolated and downgrades claim certainty.
- **Strict Anti-Leakage Separation**: Customer lifetime aggregates and post-delivery survey contents are strictly isolated from first-order transaction decision points.

---

## 📄 License & Citation

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```bibtex
@software{csip2026,
  author = {CSIP Development Team},
  title = {CSIP: Computational Society Intelligence Platform & Universal Decision Simulator},
  year = {2026},
  url = {https://github.com/your-username/csip}
}
```
