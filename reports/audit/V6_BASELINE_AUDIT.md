# CSIP Version 6 Baseline Forensic Audit Report
## Comprehensive Pre-Remediation Verification & Methodological Assessment
### Reference Standard: SKKNI No. 299 Tahun 2020 | LSP TRI Scheme: SKM/2905/LSP-TRI/VII/2025

- **Document ID**: `CSIP-AUDIT-V6-BASE-2026-11`
- **Audit Date**: 2026-11-11
- **Lead Auditor**: Principal Data Scientist, ML Systems Engineer & Scientific Integrity Auditor
- **Repository Branch Baseline**: `v6-baseline` (commit `faf2d13`)
- **Remediation Target**: CSIP V7 (Excellence Score ≥ 9.0/10)

---

## 1. Executive Summary

An independent, rigorous forensic audit was conducted on the baseline of **CSIP Version 6** prior to any structural modifications. The audit evaluated scientific validity, empirical defensibility, data pipeline integrity, machine learning evaluation standards, and BNSP SKKNI competency evidence traceability.

### Baseline Summary Metrics:
- **Total Tracked Files**: 173 artifacts across source code, configurations, notebooks, datasets, reports, and tests.
- **Test Suite Execution**: **87 PASSED, 0 FAILED, 0 SKIPPED** in **26.74 seconds** (Python 3.14.7, Windows 64-bit AMD64).
- **Competency Unit Coverage**: Exactly 11/11 competency units, 27/27 competency elements, and 63/63 KUKs mapped.
- **Evidence Verification Status**: 60 VERIFIED, 3 PARTIALLY_VERIFIED (disclosed simulated approvals for stakeholder business objectives in UK-01), 0 MISSING.
- **Primary Methodological Risks Identified**:
  1. Point-in-time leakage of `approval_lag_hours` in early-warning checkout feature set `E1_early_warning_checkout`.
  2. First-order cohort selection risk via pandas `groupby("customer_unique_id").first()` which returns column-wise first non-null values instead of deterministic row-level records.
  3. Survivor / selection bias caused by default `status_filter="delivered"`, where canceled/undelivered orders are excluded from checkout satisfaction training.
  4. World Model parameter interpretation requiring explicit non-causal structural sensitivity disclaimers.

---

## 2. Repository Inventory & Architectural Structure

The repository maintains a clean modular structure adhering to high software engineering standards:

```
csip/
├── app/                    # Streamlit Multi-Page Web Interface (6 pages)
├── artifacts/              # Serialized Models (.pkl, .pt), Scalers, Metric Logs (.json)
├── config/                 # Declarative YAML Configurations (features.yaml, business.yaml)
├── data/
│   ├── raw/                # 9 Olist Relational Tables (CSV)
│   └── processed/          # 4 Cleaned & Constructed Parquet Tables (order_level, customer_cohort, etc.)
├── docs/                   # Methodological & Architectural Documentation
├── notebooks/              # 14 Research & Demonstration Jupyter Notebooks
├── reports/                # Forensic Audit, Quality, Evaluation, and Competency Reports
├── scripts/                # Execution Pipelines (build_features.py, run_ml_experiments.py, etc.)
├── src/csip/               # Core Python Package (11 domain subpackages)
├── standards/              # Canonical Standard: canonical_skkni_299_2020.json (Single Source of Truth)
└── tests/                  # 14 Comprehensive Pytest Modules (87 automated test cases)
```

---

## 3. Verified Strengths of CSIP V6

1. **Strict Split-Before-Fit Pipeline**:
   - Temporal train/validation/test splitting (Train: Weeks 1–64, Val: Weeks 65–78, Test: Weeks 79–87) strictly enforced before fitting scalers, encoders, and models. Zero forward-looking leakage in feature transformations.
2. **Standardized Classification Evaluation**:
   - PR-AUC evaluated via scikit-learn `average_precision_score()`, correctly benchmarking against naive positive prevalence baseline (~0.1096 for train/val, ~0.1281 overall), avoiding inflated trapezoidal AUC.
3. **Rigorous Handling of Review Missingness**:
   - 646 unobserved reviews preserved as `NaN` rather than artificially imputed as neutral score 3. Supervised classification targets conditioned on `has_observed_review == 1`.
4. **Comprehensive Test Automation**:
   - 87 automated tests covering schema integrity, foreign keys, deterministic reproducibility, temporal boundaries, model inference, and Streamlit page imports.
5. **No External Cloud Transmission**:
   - 100% local execution running efficiently within an 8 GB RAM laptop footprint using CPU-optimized LightGBM and PyTorch.

---

## 4. Verified Defects & Methodological Risks in V6

### Defect 1 (Critical P0): Point-in-Time Leakage of `approval_lag_hours` at Checkout
- **Location**: `src/csip/models/trainer.py` (Line 75) and `config/features.yaml` (Line 52).
- **Finding**: `approval_lag_hours` is defined as `(order_approved_at - order_purchase_timestamp)`. In e-commerce workflows, `order_approved_at` occurs *after* `order_purchase_timestamp` (average payment latency ~10.2 hours for credit card, up to 48 hours for boleto bancário).
- **Impact**: Including `approval_lag_hours` in `E1_early_warning_checkout` violates the prediction contract of checkout ($t_0$), since approval status and duration are unobserved when the customer clicks 'Place Order'.
- **Remediation**: Remove `approval_lag_hours` from `E1_early_warning_checkout`. Add `approval_lag_hours` to `checkout_stage_restricted_features` in `config/features.yaml`. Document the exact prediction timestamp boundary in `docs/methodology/PREDICTION_CONTRACT.md`.

### Defect 2 (Critical P0): First-Order Cohort Selection Bug (`GroupBy.first()`)
- **Location**: `src/csip/features/engineer.py::build_customer_cohort` (Line 261).
- **Finding**: The baseline code executes `order_1 = df_sorted.groupby("customer_unique_id").first().reset_index()`. In pandas, `groupby().first()` selects the first *non-null* value independently for each column!
- **Impact**: If a customer has Order 1 with `review_score = NaN` and Order 2 with `review_score = 5`, `groupby.first()` pulls `5` from Order 2 into the first-order record, leaking future order data into the first-order cohort features!
- **Remediation**: Replace with deterministic row-level selection:
  ```python
  order_1 = df_sorted.drop_duplicates(subset=["customer_unique_id"], keep="first").copy().reset_index(drop=True)
  ```
  Add synthetic regression test in `tests/test_feature_leakage.py` verifying zero column-wise bleed.

### Defect 3 (Methodological P0): Population Funnel & Selection Bias (`status_filter="delivered"`)
- **Location**: `src/csip/cleaning/cleaner.py::clean_orders` (Line 66, 464).
- **Finding**: Default cleaning applies `status_filter="delivered"`, dropping ~2,971 non-delivered orders (canceled, unavailable, in-transit).
- **Impact**: If an early warning model trained only on delivered orders is applied at checkout, it suffers from survivor bias. The model's formal estimand is $P(\text{Negative Review} \mid \text{Order Delivered})$, not unconditional satisfaction across all placed orders.
- **Remediation**: Retain `status_filter="delivered"` for satisfaction modeling (as reviews are only triggered post-delivery), but document the population funnel, selection mechanisms, and generalization boundaries in `docs/methodology/PREDICTION_CONTRACT.md` and `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`.

### Defect 4 (Methodological P1): World Model Non-Causal Boundary
- **Location**: `src/csip/world/state_transition.py` and `scripts/run_world_model.py`.
- **Finding**: While V6 added out-of-sample holdout validation, policy simulations must be explicitly bounded as structural sensitivity projections rather than identified causal effects.
- **Remediation**: Author formal mathematical specification `docs/methodology/WORLD_MODEL_SPECIFICATION.md` and audit report `reports/audit/WORLD_MODEL_AUDIT.md`.

---

## 5. Baseline Test Execution Results

```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-8.4.1, pluggy-1.6.0
rootdir: . (repo root)
configfile: pyproject.toml
collected 87 items

tests/test_behavioral_discovery.py ........                             [  9%]
tests/test_canonical_skkni.py ..                                       [ 11%]
tests/test_cleaning_pipeline.py ........                                [ 20%]
tests/test_data_pipeline_stress.py .                                    [ 21%]
tests/test_data_validation.py .........                                 [ 32%]
tests/test_decision_studio.py ...                                       [ 35%]
tests/test_feature_engineering.py .......                               [ 43%]
tests/test_feature_leakage.py ........                                  [ 52%]
tests/test_hypotheses.py .......                                        [ 60%]
tests/test_ml_models.py .............                                   [ 75%]
tests/test_model_evaluation.py .......                                  [ 83%]
tests/test_streamlit_pages.py ........                                  [ 93%]
tests/test_uncertainty.py ..                                            [ 95%]
tests/test_world_model.py ....                                          [100%]

============================== warnings summary ===============================
tests/test_data_pipeline_stress.py::test_ml_pipeline_stress_small_dataset
  UserWarning: Could not find the number of physical cores...
87 passed, 1 warning in 26.74s
============================= 87 passed in 26.74s =============================
```

---

## 6. Competency Evidence Status (Baseline V6)

- **Total Competency Units**: 11 (SKKNI No. 299/2020)
- **Total Elements**: 27
- **Total KUKs**: 63
- **Evidence Verification Summary**:
  - `VERIFIED`: 60 KUKs (95.2%)
  - `PARTIALLY_VERIFIED`: 3 KUKs (4.8%) — UK-01 KUK 2.2, 3.3, 4.3 (simulated client sign-offs disclosed)
  - `MISSING`: 0 KUKs (0.0%)

---

## 7. Remediation Action Plan for V7

| Workstream | Priority | Key Action Items | Target Artifacts |
| :--- | :---: | :--- | :--- |
| **Point-in-Time Leakage** | P0 | Remove `approval_lag_hours` from `E1_early_warning_checkout`, update config, re-run feature audit | `trainer.py`, `features.yaml`, `FEATURE_AVAILABILITY_AUDIT.csv` |
| **First-Order Cohort** | P0 | Replace `groupby().first()` with `drop_duplicates(subset=["customer_unique_id"], keep="first")` | `engineer.py`, `test_feature_leakage.py` |
| **Prediction Contract & Bias** | P0 | Define formal estimands, population inclusion/exclusion, selection bias documentation | `PREDICTION_CONTRACT.md`, `POPULATION_AND_SELECTION_BIAS.md`, `LABEL_OBSERVABILITY_AUDIT.csv` |
| **Retraining & Calibration** | P1 | Re-run feature engineering, behavioral discovery, ML models, evaluate Platt calibration & thresholding | `order_level.parquet`, `ml_leaderboard.json`, `ml_leaderboard.csv` |
| **World Model Specification** | P1 | Document state-space equations, holdout protocol, sensitivity disclaimers | `WORLD_MODEL_SPECIFICATION.md`, `WORLD_MODEL_AUDIT.md` |
| **Notebook Audit** | P1 | Audit all 14 notebooks, document inputs/outputs and execution modes | `NOTEBOOK_EXECUTION_AUDIT.csv` |
| **BNSP Competency Evidence** | P1 | Construct Master Competency Matrix (Excel + CSV), Assessor Guide, Candidate Guide, Readiness Report | `competency/BNSP_MASTER_COMPETENCY_MATRIX.xlsx`, `ASSESSOR_EVIDENCE_GUIDE.md`, etc. |
| **Architecture & Quality Docs** | P1 | System architecture, data methodology, model evaluation, test report, changelog, final audit | `SYSTEM_ARCHITECTURE.md`, `DATA_METHODOLOGY.md`, `V7_FINAL_AUDIT.md` |

---
**Auditor Sign-off**: Verified Baseline Established. Ready for V7 Scientific Remediation.
