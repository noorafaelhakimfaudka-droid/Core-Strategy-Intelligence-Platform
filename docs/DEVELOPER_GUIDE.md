# CSIP Developer & Maintainer Guide: Architecture, Pipelines & Code Standards
## Codebase Conventions, Module Extension, Retraining Pipelines & Git Workflow

**Document Version:** 1.0.0-Definitive  
**Target Audience:** Machine Learning Engineers, Data Scientists, MLOps Engineers  

---

### 1. CODEBASE ARCHITECTURE & DIRECTORY MAP

```
csip/
├── app/                     # Presentation layer (Streamlit pages & UI components)
│   ├── pages/               # 9 Analytical chapters
│   └── ui_components.py     # Reusable HTML/Plotly styling components
├── artifacts/               # Binary models, sidecars, and generated reports
│   ├── models/              # Serialized .joblib and .pt models
│   ├── metadata/            # MODEL_RESULTS_REGISTRY.csv, DATA_LINEAGE.json
│   └── reports/             # JSON leaderboards and figure plots
├── competency/              # SKKNI / SKKNI 299/2020 Evidence Registries & Matrices
├── config/                  # Hyperparameter settings and schema definitions
├── data/                    # Data storage (raw, interim, processed parquets)
├── docs/                    # 18-Chapter Technical Product Documentation Suite
├── reports/                 # Formal model cards, audit reports, quality assessments
├── scripts/                 # Standalone ETL, retraining, and verification scripts
├── src/csip/                # Core Data Science package (12 domain subpackages)
├── tests/                   # 199+ Automated pytest unit and integration tests
└── tools/                   # Master Quality Gates runner and registry validators
```

---

### 2. DEVELOPER WORKFLOWS

#### 2.1 Adding a New Engineered Feature
1. Open `src/csip/features/engineer.py`.
2. Implement the feature calculation inside `build_order_level_features()` or `build_customer_cohort_features()`.
3. Ensure the feature uses only information available at the designated operational timestamp.
4. Document the feature rationale in `reports/models/FEATURE_ENGINEERING_REPORT.md` and add schema entry to `docs/methodology/DATA_DICTIONARY.md`.
5. Run `pytest tests/test_feature_leakage.py` to confirm zero target leakage.

#### 2.2 Re-Running the Full Automated Retraining Pipeline
To retrain all 8 models from raw CSV files in a clean, reproducible execution:
```bash
python scripts/run_full_retraining.py
```
This orchestrates:
- Feature generation on `data/raw/`.
- Temporal train/test splitting at `2018-03-01`.
- Fitting LightGBM classifiers and regressors with Platt scaling.
- Training the Ridge state-transition matrix.
- Generating updated metadata sidecars in `artifacts/models/*.joblib.json`.
- Refreshing `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv`.

#### 2.3 Running Quality Gates Pre-Commit
Before committing any changes, run the Master Quality Gates:
```bash
python tools/run_final_validation.py
```
Assert that all gates pass (`APPROVED (PASS)`).

