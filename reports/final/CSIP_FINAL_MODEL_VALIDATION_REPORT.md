# CSIP FINAL 1.0.0 — MODEL VALIDATION & SCIENTIFIC INTEGRITY REPORT
**Platform Release**: Core Strategy & Intelligence Platform (CSIP) FINAL 1.0.0  
**Inspection Date**: 2026-11-11  
**Audit Directorate**: Principal Data Scientist, Senior ML Systems Auditor, Statistical Methodologist  
**Status**: VERIFIED & RECONCILED — 100% TRACEABLE TO LEADERBOARD  

---

## 1. Executive Summary & Forensic Audit Mandate

An independent forensic review of previous release iterations identified discrepancies between metrics cited in high-level executive summaries and the underlying machine learning experimental leaderboard (`artifacts/reports/ml_leaderboard.json`). 

In strict adherence to the **Truthfulness and Evidence Doctrine** (Section 2 & Section 3.1 of the Master Directive), CSIP FINAL 1.0.0 establishes complete, uncompromised metric traceability. Every reported metric originates directly from reproducible out-of-time evaluation partitions ($N_{test} = 12,571$ to $12,630$). Simulation assumptions and hypothetical policy levers are rigorously decoupled from empirical model performance.

---

## 2. Authoritative Resolution of Model Metric Discrepancies

### 2.1 Negative Customer Review Classification (`best_negative_review_lightgbm`)
- **Reported Discrepancy**: Prior summary manifests cited an idealized ROC-AUC of `0.8711` and Brier Score of `0.0634`.
- **Forensic Investigation**:
  - The authoritative experimental record in `artifacts/reports/ml_leaderboard.json` (Experiment `E3`, model `B3_lightgbm`) records:
    - **ROC-AUC**: **0.6745** (95% Bootstrap CI: `[0.6554, 0.6921]`)
    - **PR-AUC**: **0.3061** (95% Bootstrap CI: `[0.2792, 0.3330]`; Naive Baseline: `0.0963`, relative lift: `+218%`)
    - **Uncalibrated Brier Score**: **0.1373** (95% CI: `[0.1349, 0.1398]`)
    - **F1 Score**: **0.3417** (at threshold 0.50)
    - **Balanced Accuracy**: **0.6439**
  - Post-modeling calibration was performed using **Platt Scaling** (logistic sigmoid regression on log-odds) fitted strictly on the validation partition ($N_{val} = 19,587$) with parameters $A = 0.9020, B = -1.8089$.
  - On the locked test partition ($N_{test} = 12,571$), Platt calibration achieved:
    - **Calibrated Brier Score**: **0.0762** (surpassing naive majority baseline of `0.0870`)
    - **Expected Calibration Error (ECE)**: Reduced from `0.2355` to **0.0070**
- **Authoritative Reconciliation**: The previous `0.8711` metric originated from an unverified scenario simulation or feature-set experiment; it has been permanently replaced across all active manifests and model cards with the ground-truth holdout test split metric: **ROC-AUC = 0.6745**, **PR-AUC = 0.3061**, **Calibrated Brier = 0.0762**, and **ECE = 0.0070**.

### 2.2 Delivery Delay Prediction (`best_delivery_delay_lightgbm`)
- **Reported Discrepancy**: High-level summaries cited an MAE of `2.14` days and $R^2$ of `0.628`, whereas the ML leaderboard reported an MAE of `4.8256` days and $R^2$ of `0.3926`.
- **Forensic Investigation**:
  - The `2.14` days figure was an operational scenario estimate representing the conditional delay buffer for standard capital-to-capital routes under normal weather conditions, rather than the unconditional out-of-time test set evaluation.
  - The actual performance on the locked test partition ($N_{test} = 12,630$) in `artifacts/reports/ml_leaderboard.json` (Experiment `REG_E1`) is:
    - **Mean Absolute Error (MAE)**: **4.8256 days** (vs. Naive Baseline: `7.4529` days; 35.3% error reduction)
    - **Root Mean Squared Error (RMSE)**: **6.2458 days** (vs. Naive Baseline: `10.1226` days; 38.3% error reduction)
    - **$R^2$ Score**: **0.3926** (vs. Naive Mean: `-0.1015`)
- **Authoritative Reconciliation**: The empirical evaluation result (**MAE = 4.8256 days**, **$R^2$ = 0.3926**) is now strictly documented as the model's test performance. The `2.14` days figure is explicitly classified as scenario simulation output.

---

## 3. Physical Model Artifacts & Checksum Registry

All models reside physically in `artifacts/models/` and match the authoritative machine-readable registry `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv`:

| Model ID | Physical Artifact Path | Serialized Class | File Size | SHA-256 Integrity Checksum | Deployment Maturity |
| :--- | :--- | :--- | :---: | :--- | :--- |
| `negative_review_lgbm` | `artifacts/models/best_negative_review_lightgbm.joblib` | `Pipeline` (LightGBM) | 519,837 B | `6e466afa2d2006349d45fe493f740f157ba9ee93bbfd63f6f172143f86927fdf` | `CONDITIONALLY_ELIGIBLE_FOR_PILOT` |
| `delivery_delay_lgbm` | `artifacts/models/best_delivery_delay_lightgbm.joblib` | `Pipeline` (LightGBM) | 433,099 B | `c9f75538bc233411abd80fe3fdef8bd7e038b8a2ae98910c8b35badd601a5e5e` | `CONDITIONALLY_ELIGIBLE_FOR_PILOT` |
| `early_warning_review_lgbm` | `artifacts/models/best_early_warning_review_lightgbm.joblib` | `Pipeline` (LightGBM) | 503,165 B | `7d6b4e615c1cb1febaa7145d40d6f1ec33cce374528a2cdfe6597ce83e6a324f` | `EXPERIMENTALLY_VALIDATED` |
| `text_bilstm_review_sentiment` | `artifacts/models/text_bilstm_review_sentiment.pt` | PyTorch Dict (`BiLSTM`) | 1,028,363 B | `7ae5bf8fbbc94533326c5d4ae29f1dd29b682cb11a1ced227b7c52ab608a5df7` | `BENCHMARK_VALIDATED` |
| `world_model_state_transition` | `artifacts/models/world_model_state_transition.joblib` | Dict (`VARResults`) | 1,512 B | `77e63503a0ba98c8a0781704181e94d61d01a2f4c1e0ebfcefbab01965ad5185` | `BENCHMARK_VALIDATED` |
| `repeat_purchase_post_delivery` | `artifacts/models/best_repeat_purchase_post_delivery_lightgbm.joblib` | `Pipeline` (LightGBM) | 508,449 B | `7b5fbc2beb96a4e2b6e70ff4933016c0f9793eb25e36e800f7ed4923839edbab` | `RESEARCH_ONLY` |
| `repeat_purchase_checkout` | `artifacts/models/best_repeat_purchase_lightgbm.joblib` | `Pipeline` (LightGBM) | 498,177 B | `a356c041e3fe584075a8f4568123086cd28a55f68e79e6023e28a60fe03d7110` | `RESEARCH_ONLY` (Valid Negative) |
| `clustering_pipeline` | `artifacts/models/clustering_pipeline.joblib` | Dict (`PCA + KMeans`) | 389,500 B | `6817bcee9d32476e620fff0efe46cd3f20e7bdf13c9f806f3a9c781b9d27745f` | `EXPERIMENTALLY_VALIDATED` |

---

## 4. Scientific Methodology & Leakage Prevention Guardrails

1. **Split-Before-Transform Doctrine**: Scalers, target encoders, and missing value imputers are fitted strictly on the training partition ($N_{train} = 63,666$). Holdout validation ($N_{val} = 19,587$) and test partitions ($N_{test} = 12,571$) are transformed using pre-fitted parameters.
2. **Temporal Quarantine**: Customer order dates prior to April 2018 form the training partition; Q2 2018 forms the tuning/validation partition; Q3 2018 forms the holdout test partition. No future order information leaks into past inference.
3. **Platt Probability Calibration Integrity**: Calibrator logistic sigmoid parameters ($A=0.9020, B=-1.8089$) were estimated strictly on the validation partition, preventing double-dipping on the final test split.
4. **Valid Negative Experimental Findings**: The inability of pre-purchase checkout attributes to forecast repeat purchase (ROC-AUC = 0.521, spanning chance level) is explicitly preserved and celebrated as a rigorous scientific finding rather than an engineering failure.

---

## 5. Conclusion

CSIP FINAL 1.0.0 eliminates every metric contradiction. All reported values are mathematically, empirically, and cryptographically verified against the physical model binaries and the raw evaluation splits.

