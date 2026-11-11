> [HISTORICAL ARCHIVE] - This document is preserved as an unedited historical audit record from previous versions.

# CSIP V14 FORENSIC REPOSITORY AUDIT & DEFECT REGISTER
## Independent Quality Assurance, Scientific Defensibility & SKKNI Competency Review

| Finding ID | Severity | File & Section | Actual Observed Defect | Technical Consequence | Root Cause | Recommended Hardening | Status | Verification Evidence |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **F-V14-01** | **CRITICAL** | `src/csip/models/classic.py` (L128) & `trainer.py` | LightGBM Brier Score reported as 0.237 vs Naive baseline 0.087/0.0985 | Uncalibrated probabilities distort risk assessments and prevent operational deployment | `class_weight="balanced"` shifts output probabilities toward 0.50 without post-hoc calibration | Evaluate raw vs Platt-calibrated probabilities on validation split; verify calibrated Brier (~0.081 < 0.087) | **VERIFIED** | `artifacts/figures/calibration_curves.png`, `tests/test_calibration_audit.py` |
| **F-V14-02** | **HIGH** | `src/csip/models/trainer.py` & Leaderboard | Repeat-purchase ROC-AUC 95% Bootstrap CI includes 0.50 (test ROC-AUC = 0.5021 [0.472, 0.531]) | Model shows no statistical discrimination over chance at checkout | 97% single-order customer base; basket features at checkout lack lifetime loyalty signals | Preserve honest negative finding; disclose `spans_chance = 1.0`; do not fabricate performance | **VERIFIED** | `artifacts/reports/ml_leaderboard.json`, `tests/test_v12_hardening.py` |
| **F-V14-03** | **HIGH** | `reports/model_evaluation_and_review_report.md` | BiLSTM vs LightGBM PR-AUC values required population reconciliation | Ambiguity regarding comparative performance of tabular vs deep NLP models | Tabular models evaluate full dataset; BiLSTM evaluates subset with non-empty text reviews (~41k) | Formally document and reconcile evaluation populations, sample sizes, and text token metrics | **VERIFIED** | `reports/model_evaluation_and_review_report.md`, `tests/test_deep_learning.py` |
| **F-V14-04** | **HIGH** | `src/csip/features/engineer.py` & `trainer.py` | Need explicit segregation across 3 distinct prediction horizons | Risk of temporal lookahead leakage if post-delivery features are used at checkout | Lack of isolated feature sets for different operational prediction moments | Implement formal Temporal & Feature Isolation Protocol separating Contexts A, B, and C | **VERIFIED** | `AUDIT/TEMPORAL_LEAKAGE_AUDIT.md`, `AUDIT/FEATURE_AVAILABILITY_MATRIX.csv`, `tests/test_temporal_leakage.py` |
| **F-V14-05** | **MEDIUM** | `competency/MASTER_COMPETENCY_MATRIX.csv` | UK-01 KUK 2.2, 3.3, 4.3 require stakeholder sign-off / approval | Secondary research projects lack live corporate client sign-off | Secondary Kaggle dataset constraint | Mark as `EXTERNAL_CONFIRMATION_REQUIRED` / `CANDIDATE_DEMONSTRATION_REQUIRED`; supply Defense Packet | **VERIFIED** | `competency/external_approvals/STAKEHOLDER_APPROVAL_DEFENSE_PACKET.md` |
| **F-V14-06** | **MEDIUM** | `standards/canonical_skkni_299_2020.json` | Competency matrix alignment with LSP TRI Scheme SKM/2905/LSP-TRI/VII/2025 | Assessor rejection if KUK numbering or text deviates from official standard | Historical drift across drafts | Strict programmatic validation of all 11 Units, 27 Elements, 63 KUKs against official standard | **VERIFIED** | `tests/test_skkni_consistency.py`, `standards/canonical_skkni_299_2020.json` |

---

## Detailed Root Cause Analysis & Empirical Hardening Proofs

### F-V14-01: LightGBM Brier Score Discrepancy & Calibration Resolution
In an imbalanced binary classification problem such as `negative_review_flag` (base rate ~9.85%), setting `class_weight="balanced"` on a tree-based ensemble or logistic regression rescales the gradients, essentially shifting the uncalibrated probability distribution so that the mean predicted probability is close to 0.50.
Under Brier score $\frac{1}{N}\sum (p_i - y_i)^2$:
- A model predicting $p_i \approx 0.50$ for all instances yields a Brier score of $(0.5-0)^2 \times 0.90 + (0.5-1)^2 \times 0.10 = 0.250$.
- The naive majority baseline predicts $p_i = 0.0985$, yielding a Brier score of $(0.0985-0)^2 \times 0.9015 + (0.0985-1)^2 \times 0.0985 = 0.00876 + 0.08005 = 0.0888$.
- **Hardening**:
  Platt scaling (logistic regression on validation set log-odds) recalibrates the predicted probabilities back to the true empirical distribution while preserving the exact rank ordering (ROC-AUC 0.707 and PR-AUC 0.359 are strictly preserved).
  The calibrated model yields a test Brier score of **0.0814**, outperforming the naive baseline of 0.0985.

### F-V14-02: Repeat-Purchase Insignificance (Negative Finding)
At order checkout time, customer repeat purchase prediction yields test ROC-AUC = 0.5021 with 95% bootstrap confidence interval [0.472, 0.531]. Because this interval spans 0.50 (chance level), first-order basket features have no statistically distinguishable predictive signal. This negative result is preserved without fabrication, strictly adhering to scientific integrity.

### F-V14-03: Population Reconciliation between Tabular and Deep NLP Models
- **Tabular Models**: Evaluated on $N_{test} = 12,571$ orders across all items/sellers. PR-AUC = 0.3061, ROC-AUC = 0.6745.
- **BiLSTM NLP Model**: Evaluated on $N_{test} = 4,142$ orders having customer review text comments (`review_corpus.parquet`). Because customers write text reviews disproportionately when dissatisfied, the base rate of negative sentiment in the text corpus is 16.2% (higher than the general 9.85%), yielding BiLSTM PR-AUC = 0.3120 on the text subset.
