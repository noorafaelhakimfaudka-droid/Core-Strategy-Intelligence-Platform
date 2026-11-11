# CSIP Version 6 to Version 7 Change Log
## Detailed Technical, Scientific, and Competency Evidence Modifications
### Standard: SKKNI No. 299 Tahun 2020 | LSP TRI Scheme: SKM/2905/LSP-TRI/VII/2025

- **Document ID**: `CSIP-CHANGELOG-V6-TO-V7`
- **Release Version**: 7.0.0
- **Release Date**: 2026-11-11
- **Lead Contributors**: Principal Data Scientist, ML Systems Engineer & BNSP Assessment Auditor

---

## 1. Overview of V7 Release

CSIP Version 7 represents a comprehensive **scientific and engineering excellence remediation** of CSIP Version 6. Every verified defect and methodological risk identified during independent baseline forensic auditing was resolved at root cause.

---

## 2. Granular Modification Register

| Item ID | Category | Impacted Files | Description of Modification | Scientific / Business Rationale | Impacted SKKNI Unit | Verification Performed |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **MOD-01** | Scientific Integrity | `src/csip/models/trainer.py`, `config/features.yaml` | Removed `approval_lag_hours` from `E1_early_warning_checkout`. Added to `checkout_stage_restricted_features`. | At checkout ($t_0$), payment authorization duration is unobserved (mean 10.2h lag). Including it was point-in-time leakage. | UK-07, UK-08 | `tests/test_feature_leakage.py::test_checkout_stage_restricted_features` passed |
| **MOD-02** | Data Engineering | `src/csip/features/engineer.py` | Replaced `df_sorted.groupby('customer_unique_id').first()` with `df_sorted.drop_duplicates(subset=['customer_unique_id'], keep='first')`. | In pandas, `groupby.first()` returns column-wise first non-null values, bleeding Order 2 data into Order 1 if Order 1 had missing values. | UK-05, UK-07 | `test_first_order_cohort_null_bleeding_regression` passed |
| **MOD-03** | Methodology | `docs/methodology/PREDICTION_CONTRACT.md` | Authored formal binding prediction contract for all models. | Defines formal timestamps ($t_0, t_1$), analytical grain, target definitions, and allowed feature schemas. | UK-02, UK-07, UK-08 | Automated schema assertion in test suite |
| **MOD-04** | Audit & Governance | `reports/audit/FEATURE_AVAILABILITY_AUDIT.csv` | Generated tabular inventory of 29 features with availability events and risk decisions. | Provides full auditability of temporal feature availability for external assessors. | UK-07, UK-11 | Document review & path verification |
| **MOD-05** | Statistical Bias | `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`, `reports/audit/LABEL_OBSERVABILITY_AUDIT.csv` | Documented population funnel, estimand $\mathbb{P}(Y=1 \mid X, \text{Delivered}=1)$, and survivor bias of `status_filter='delivered'`. | Canceled/unavailable orders (1.24% of intake, 87.4% negative) are excluded; model estimates delivered satisfaction. | UK-04, UK-05, UK-11 | Data verification across 99,441 raw orders |
| **MOD-06** | World Model | `docs/methodology/WORLD_MODEL_SPECIFICATION.md`, `reports/audit/WORLD_MODEL_AUDIT.md` | Authored mathematical state-space VAR(1) specification and empirical audit report. | Transparent disclosure of non-causal sensitivity boundaries and out-of-sample holdout backtesting (Weeks 65–87). | UK-08, UK-09, UK-10 | `python scripts/run_world_model.py` holdout evaluation passed |
| **MOD-07** | Pipeline Re-run | `data/processed/*.parquet`, `artifacts/models/*`, `artifacts/reports/*` | Rebuilt all 4 analytical datasets and re-trained all ML models (B0-B3). | Updates model parameters with zero-leakage checkout feature set. LightGBM Champion PR-AUC = 0.3061 (vs 0.1096 naive). | UK-06, UK-09, UK-10 | Leaderboard generation & artifact hash check |
| **MOD-08** | Notebook Audit | `reports/audit/NOTEBOOK_EXECUTION_AUDIT.csv` | Audited all 14 Jupyter research notebooks. | Distinguishes interactive exploration, pipeline execution, and model checkpoint loading across all 14 notebooks. | UK-01 s.d. UK-11 | Manifest and file audit |
| **MOD-09** | Testing Suite | `tests/test_feature_leakage.py` | Added 2 new P0 regression tests: `test_first_order_cohort_null_bleeding_regression` and `test_future_perturbation_invariance`. | Increases test suite from 87 to 89 tests; prevents future-order column bleed and ensures temporal invariance. | UK-07, UK-08, UK-11 | `python -m pytest tests/` (89/89 passed in 23.29s) |
| **MOD-10** | Competency Matrix | `competency/BNSP_MASTER_COMPETENCY_MATRIX.xlsx`, `competency/BNSP_MASTER_COMPETENCY_MATRIX.csv` | Generated 15-column master competency matrix covering all 63 KUKs. | Provides assessors with a complete, traceable mapping from official SKKNI text to technical code and test proof. | UK-01 s.d. UK-11 | `python scripts/build_bnsp_matrix.py` |
| **MOD-11** | Evidence Registry | `competency/EVIDENCE_REGISTRY.csv` | Generated CSV registry of all 63 evidence items. | Machine-readable evidence index with relative paths and verification procedures. | UK-11 | Automated path integrity verification |
| **MOD-12** | Assessor Guide | `competency/ASSESSOR_EVIDENCE_GUIDE.md` | Authored comprehensive assessor navigation guide in formal Indonesian. | Allows assessors to quickly trace, reproduce, and verify any KUK without ambiguity. | UK-01 s.d. UK-11 | Document review |
| **MOD-13** | Candidate Guide | `competency/CANDIDATE_DEMONSTRATION_GUIDE.md` | Authored practical live demonstration and defense guide for the candidate. | Prepares candidate to demonstrate code, explain technical decisions, and address assessor questions with evidence. | UK-01 s.d. UK-11 | Document review |
| **MOD-14** | Readiness Report | `competency/ASSESSMENT_READINESS_REPORT.md` | Formulated unit-by-unit assessment readiness evaluation across all 11 units. | Transparent evaluation (10 Ready, 1 Ready with Minor Gaps, 0 Not Ready). | UK-01 s.d. UK-11 | Document review |
| **MOD-15** | Architecture & Docs | `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/methodology/DATA_METHODOLOGY.md`, `docs/methodology/MODEL_EVALUATION.md`, `docs/quality/REPRODUCIBILITY.md`, `docs/limitations/KNOWN_LIMITATIONS.md` | Authored unified, consistent system and scientific documentation suite. | Replaces fragmented documentation with coherent, cross-referenced technical specifications. | UK-01 s.d. UK-11 | Markdown linting and link validation |
