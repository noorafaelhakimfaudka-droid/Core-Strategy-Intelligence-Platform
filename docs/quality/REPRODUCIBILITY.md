# CSIP Reproducibility & Environment Guide
## Full End-to-End Pipeline Execution, Deterministic Seeds, and Verification
### Standard: SKKNI No. 299 Tahun 2020 | Subbidang: Data Science (KKNI Jenjang 7)

- **Document ID**: `CSIP-DOC-REPRO-2026-V7`
- **Version**: 7.0.0
- **Status**: EMPIRICALLY VERIFIED
- **Author**: Software Quality Assurance & ML DevOps Engineer

---

## 1. System Requirements & Environment Specification

CSIP is designed and tested for zero-dependency local execution within a standard developer environment:

- **Operating System**: Windows 10/11 64-bit, Linux Ubuntu 22.04+, or macOS Sonoma.
- **Python Runtime**: Python 3.10 to Python 3.14 (Verified on Python 3.14.7 64-bit AMD64).
- **RAM Footprint**: Minimum 8 GB RAM (Peak pipeline memory utilization < 3.2 GB).
- **Disk Storage**: ~1.5 GB total (Datasets, artifacts, logs, and report images).
- **Network Dependency**: **0% (Completely Offline / No Cloud Transmission)**.

### Core Dependency Stack (`pyproject.toml` / `requirements.txt`):
- Data Processing: `numpy>=1.24.0`, `pandas>=2.0.0`, `pyarrow>=14.0.0`, `scipy>=1.10.0`
- Machine Learning: `scikit-learn>=1.3.0`, `lightgbm>=4.0.0`, `torch>=2.0.0`
- Explainability & Simulation: `shap>=0.42.0`, `joblib>=1.3.0`, `openpyxl>=3.1.0`
- Visualization & Web App: `matplotlib>=3.7.0`, `plotly>=5.15.0`, `streamlit>=1.28.0`
- Testing & Quality: `pytest>=7.4.0`

---

## 2. Step-by-Step Reproduction Guide

Execute the following commands from the repository root directory in a bash or PowerShell terminal:

### Step 1: Clean Feature Construction
Reconstructs the 4 analytical Parquet datasets from raw CSV files:
```powershell
python scripts/build_features.py
```
*Expected Output*: Generates `order_level.parquet` (96,470 rows), `customer_cohort.parquet` (75,318 rows), `review_corpus.parquet` (95,824 rows), and `weekly_system_state.parquet` (87 rows).

### Step 2: Unsupervised Behavioral Clustering
Fits K-Means ($k=3$) persona segmentation and generates cluster visualization:
```powershell
python scripts/run_behavioral_discovery.py
```
*Expected Output*: Saves `order_level_clustered.parquet`, `clustering_pipeline.joblib`, and PCA cluster plots.

### Step 3: Train Machine Learning Benchmark Ladder
Executes the supervised learning ladder (B0 to B3) across temporal splits:
```powershell
python scripts/run_ml_experiments.py
```
*Expected Output*: Trains Naive, Ridge, Decision Tree, Random Forest, and LightGBM models. Generates `artifacts/reports/ml_leaderboard.json` and `ml_leaderboard.csv`.

### Step 4: Empirical Hypothesis Battery
Runs formal hypothesis tests (H1 to H6) with Benjamini-Hochberg FDR correction:
```powershell
python scripts/run_hypothesis_investigation.py
```
*Expected Output*: Evaluates effect sizes, p-values, and saves `hypothesis_forest_plot.png`.

### Step 5: World Model & Policy Simulation
Fits the autoregressive Vector AutoRegressive (VAR) state transition model:
```powershell
python scripts/run_world_model.py
```
*Expected Output*: Executes synthetic parameter recovery and 23-week out-of-sample holdout backtesting.

### Step 6: Generate BNSP Competency Matrices
Builds the official assessment matrices and evidence registry:
```powershell
python scripts/build_bnsp_matrix.py
```
*Expected Output*: Generates `competency/BNSP_MASTER_COMPETENCY_MATRIX.xlsx`, `BNSP_MASTER_COMPETENCY_MATRIX.csv`, and `competency/EVIDENCE_REGISTRY.csv`.

### Step 7: Execute Full Automated Test Suite
Runs all 14 unit and integration test modules:
```powershell
python -m pytest tests/ -v
```
*Expected Output*: **87+ PASSED, 0 FAILED**.

### Step 8: Launch Interactive Web Studio (Streamlit)
```powershell
streamlit run app/streamlit_app.py
```
*Access URL*: `http://localhost:8501`
