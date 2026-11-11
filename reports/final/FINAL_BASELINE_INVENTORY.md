> [HISTORICAL ARCHIVE] - This document is preserved as an unedited historical audit record from previous versions.

# CSIP FINAL — BASELINE FORENSIC INVENTORY
**Starting Release**: CSIP V16 (v16.0.0)  
**Target Release**: CSIP FINAL 1.0.0  
**Inspection Date**: 2026-11-11  
**Auditor**: Integrated Technical Review & Quality Assurance Directorate  
**Source Archive**: `CSIP_Source_Code_V16.zip`  
**Archive Size**: 127,126,315 bytes  
**Archive SHA-256**: `602fbeb6190d361202b7a8641a907e59a9500ef3472bbaa06a51569493366d61`  

---

## 1. Executive Summary of Baseline State

Prior to initiating modifications for the final consolidation release (**CSIP FINAL 1.0.0**), an exhaustive forensic inventory of the extracted V16 source code repository (`c:\Users\asus\.gemini\antigravity\scratch\csip_final`) was conducted. The archive was verified bitwise identical with the 361 tracked files in `AUDIT/SHA256SUMS.txt` and `SHA256SUMS_V16.txt`.

While V16 demonstrated major advances in automated testing (161 passing tests) and SKKNI 299/2020 verbatim alignment, the forensic inspection confirmed the presence of seven critical material defects that must be resolved in this final release:
1. **Model Metric Inconsistencies**: Release manifests and executive summaries reported inflated or simulation-derived metrics (e.g., ROC-AUC `0.8711`, delay MAE `2.14` days) that contradicted the actual experimental test split results in `artifacts/reports/ml_leaderboard.json` (ROC-AUC `0.6745`, delay MAE `4.8256` days).
2. **Model Artifact Path Inconsistencies**: Model artifact references in `V16_RELEASE_MANIFEST.json` cited idealized names (`negative_review_lgbm.joblib`, `delivery_delay_lgbm.joblib`) instead of the actual physical files on disk (`best_negative_review_lightgbm.joblib`, `best_delivery_delay_lightgbm.joblib`).
3. **Competency Unit Code Inconsistencies**: While canonical JSON and registry tables used the legal SKKNI 299/2020 Data Management and Data Science prefix `J.62DMI00`, `EVIDENCE_INTEGRITY_REPORT.md` erroneously used `J.62DCO00`.
4. **Missing Documented Pipeline Script**: `V16_REPRODUCIBILITY_REPORT.md` referenced `scripts/run_full_retraining.py`, but the script was absent from the repository.
5. **Hardcoded Machine-Specific Windows Paths**: Several audit and reconciliation scripts contained hardcoded absolute paths (`C:\Users\asus\...`) violating cross-platform portability.
6. **Documentation Validation Tool Limitations**: `tools/validate_documentation_consistency.py` validated existence and regex invariants but did not cross-reference model manifest values against the actual leaderboard JSON.
7. **Consolidation Release Identity**: Requirement to transition project release metadata from temporary iteration `16.0.0` to the permanent product identity: **CSIP FINAL 1.0.0**.

---

## 2. Directory and Artifact Inventory

| Directory | Item Count | Core Contents & Functional Role |
| :--- | :---: | :--- |
| `src/csip/` | 42 files | Modular production Python software: `domain/`, `features/`, `models/`, `evaluation/`, `monitoring/`, `simulation/`. |
| `tests/` | 27 files | Automated test suite containing 161 test cases across 26 modules. |
| `artifacts/models/` | 16 files | Serialized binary estimators (`.joblib`, `.pt`) and associated metadata sidecars (`.joblib.json`, `.pt.json`). |
| `artifacts/reports/` | 12 files | Authoritative experimental evaluation outputs: `ml_leaderboard.json`, EDA distributions, SHAP values. |
| `competency/` | 11 files | SKKNI/LSP TRI evidence artifacts: canonical evidence registry, master matrices (CSV/XLSX), traceability matrix, defense guides. |
| `data/` | 18 files | Processed and raw observational e-commerce datasets (Olist 2016-2018 in Apache Parquet format). |
| `reports/` | 74 files | Technical reports, model cards, audit logs, methodology specifications, and historical release archives. |
| `notebooks/` | 8 files | Executable research and EDA Jupyter notebooks covering data profiling, modeling, and deep learning. |
| `scripts/` | 50 files | Automation, data generation, training, and evidence packaging scripts. |
| `standards/` | 2 files | Canonical SKKNI 299/2020 schema specification (`canonical_skkni_299_2020.json`). |
| `tools/` | 4 files | Release validation utilities and consistency check harnesses. |
| `AUDIT/` | 4 files | SHA-256 release checksum manifests and test execution reports. |

---

## 3. Physical Model Artifact Baseline Inventory

| Actual Filename on Disk | File Size | Serialized Type | Metadata Sidecar Present? |
| :--- | :---: | :--- | :---: |
| `best_negative_review_lightgbm.joblib` | 519,837 bytes | LightGBM Booster (`LGBMClassifier`) | YES (`best_negative_review_lightgbm.joblib.json`) |
| `best_delivery_delay_lightgbm.joblib` | 433,099 bytes | LightGBM Regressor (`LGBMRegressor`) | YES (`best_delivery_delay_lightgbm.joblib.json`) |
| `best_early_warning_review_lightgbm.joblib` | 503,165 bytes | LightGBM Classifier | YES (`best_early_warning_review_lightgbm.joblib.json`) |
| `best_repeat_purchase_lightgbm.joblib` | 498,177 bytes | LightGBM Classifier (Checkout) | YES (`best_repeat_purchase_lightgbm.joblib.json`) |
| `best_repeat_purchase_post_delivery_lightgbm.joblib` | 508,449 bytes | LightGBM Classifier (Post-Delivery) | YES (`best_repeat_purchase_post_delivery_lightgbm.joblib.json`) |
| `clustering_pipeline.joblib` | 389,500 bytes | KMeans / PCA Feature Preprocessor | YES (`clustering_pipeline.joblib.json`) |
| `world_model_state_transition.joblib` | 1,512 bytes | Vector Autoregression (`VARResultsWrapper`) | YES (`world_model_state_transition.joblib.json`) |
| `text_bilstm_review_sentiment.pt` | 1,028,363 bytes | PyTorch Neural Network (`BiLSTM`) | NO (Binary checkpoint only) |
| `tabular_mlp_negative_review.pt` | 64,290 bytes | PyTorch Tabular Neural Network | NO (Binary checkpoint only) |

---

## 4. Ground-Truth Model Evaluation Metrics (From `ml_leaderboard.json`)

To eliminate metric fabrication and documentation drift, the authoritative ground-truth metrics from `artifacts/reports/ml_leaderboard.json` and model cards are cataloged below:

### 4.1 Negative Customer Review Classification (`best_negative_review_lightgbm`)
- **Experiment ID**: `E3` (`B3_lightgbm`)
- **Evaluation Split**: Locked Test Split ($N_{test} = 12,571$; Train $N_{train} = 63,666$)
- **PR-AUC (Average Precision)**: **0.3061** (95% CI: `[0.2792, 0.3330]`; Naive Baseline: `0.0963`)
- **ROC-AUC**: **0.6745** (95% CI: `[0.6554, 0.6921]`)
- **F1 Score**: **0.3417**
- **Balanced Accuracy**: **0.6439**
- **Uncalibrated Brier Score**: **0.1373** (95% CI: `[0.1349, 0.1398]`)
- **Calibrated Brier Score (Platt Scaling)**: **0.0762** (Platt Parameters: $A = 0.9020$, $B = -1.8089$)
- **Expected Calibration Error (ECE)**: **0.0070** post-calibration (down from `0.2355` raw)

### 4.2 Delivery Delay Prediction (`best_delivery_delay_lightgbm`)
- **Experiment ID**: `REG_E1`
- **Evaluation Split**: Locked Test Split ($N_{test} = 12,630$)
- **Mean Absolute Error (MAE)**: **4.8256 days** (Naive baseline: `7.4529` days; 35.3% error reduction)
- **Root Mean Squared Error (RMSE)**: **6.2458 days** (Naive baseline: `10.1226` days)
- **$R^2$ Score**: **0.3926** (Naive baseline: `-0.1015`)

### 4.3 Portuguese Sentiment Text BiLSTM (`text_bilstm_review_sentiment.pt`)
- **Task**: Deep Sequence Classification on Customer Review Text
- **Evaluation Split**: Holdout Test Split ($N_{test} = 10,000$)
- **Macro F1**: **0.842**
- **Accuracy**: **0.887**

### 4.4 Macroeconomic World Model (`world_model_state_transition.joblib`)
- **Task**: Vector Autoregression (VAR, Lag $p = 2$)
- **Akaike Information Criterion (AIC)**: **-4.892**
- **Bayesian Information Criterion (BIC)**: **-4.512**

### 4.5 Repeat Purchase Models (Research & Negative Findings)
- `best_repeat_purchase_post_delivery_lightgbm.joblib`: ROC-AUC **0.612** (Weak empirical signal due to 97% one-time buyer sparsity).
- `best_repeat_purchase_lightgbm.joblib`: ROC-AUC **0.521** (Valid negative experimental finding proving absence of checkout-time reorder signal).

---

## 5. Hardening Action Plan for CSIP FINAL 1.0.0

Based on this baseline inventory, the following hardening actions are strictly planned and prioritized:
1. **Phase 2 & 3**: Create authoritative `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv` and `tools/validate_model_artifact_registry.py` reconciling all paths, sidecars, and ground-truth metrics.
2. **Phase 4**: Reconcile competency unit codes across all reports to `J.62DMI00.xxx.1` and synchronize `competency/SKKNI_TRACEABILITY_MATRIX.csv`.
3. **Phase 5 & 6**: Standardize release version to `1.0.0` (CSIP FINAL 1.0.0) across all manifests, packages, model cards, and documentation.
4. **Phase 7**: Implement `scripts/run_full_retraining.py` and sanitize all hardcoded Windows paths across scripts.
5. **Phase 8 & 9**: Execute the master validation tool (`tools/run_final_validation.py`) and author all mandatory release deliverables.
6. **Phase 10 & 11**: Package `CSIP_FINAL_RELEASE.zip`, extract to `csip_final_verified`, and execute independent verification.

