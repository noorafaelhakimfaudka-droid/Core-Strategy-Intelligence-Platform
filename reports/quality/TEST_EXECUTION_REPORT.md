# CSIP Version 7 Automated Test Execution Report
## Comprehensive Clean-Environment Test Verification & Code Quality Audit
### Reference Standard: SKKNI No. 299 Tahun 2020 | LSP TRI Scheme: SKM/2905/LSP-TRI/VII/2025

- **Document ID**: `CSIP-REP-V7-TER-01`
- **Execution Timestamp**: 2026-11-11 14:56:26 UTC+7
- **Python Runtime**: Python 3.14.7 (64-bit AMD64)
- **Pytest Version**: Pytest 9.1.1 (pluggy 1.6.0)
- **Operating System**: Windows 64-bit (win32)
- **Overall Result**: **89 PASSED, 0 FAILED, 0 SKIPPED (100% Pass Rate)**
- **Total Duration**: 23.29 seconds
- **Status**: AUDITED & VERIFIED

---

## 1. Verbatim Test Suite Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: . (repo root)
configfile: pytest.ini
plugins: anyio-4.14.2, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False
collected 89 items

tests\test_artifact_parity.py .......                                    [  7%]
tests\test_cleaning_and_grain.py ......                                  [ 14%]
tests\test_data_pipeline_stress.py ......                                [ 21%]
tests\test_data_validation.py .....                                      [ 26%]
tests\test_deep_learning.py ......                                       [ 33%]
tests\test_discovery.py ...                                              [ 37%]
tests\test_evidence_registry.py .....                                    [ 42%]
tests\test_feature_leakage.py .........                                  [ 52%]
tests\test_hypotheses.py ..                                              [ 55%]
tests\test_initialization.py ........                                    [ 64%]
tests\test_interactive_engine.py ....                                    [ 68%]
tests\test_models.py .....                                               [ 74%]
tests\test_semantic_pipeline.py .......                                  [ 82%]
tests\test_simulation_sanity.py .....                                    [ 87%]
tests\test_skkni_consistency.py ......                                   [ 94%]
tests\test_world_model.py .....                                          [100%]

============================= 89 passed in 23.29s =============================
```

---

## 2. Test Module Breakdown & SKKNI Competency Mapping

| Test Module File | Test Count | Primary Coverage Scope | Associated SKKNI Units | Execution Status |
| :--- | :---: | :--- | :---: | :---: |
| `tests/test_artifact_parity.py` | 7 | Model files & Parquet schema parity | UK-05, UK-09 | **PASSED** |
| `tests/test_cleaning_and_grain.py` | 6 | Anomaly removal, deduplication & grain definition | UK-05, UK-06 | **PASSED** |
| `tests/test_data_pipeline_stress.py` | 6 | Pipeline stress test under data distribution shifts | UK-06, UK-09 | **PASSED** |
| `tests/test_data_validation.py` | 5 | Foreign Key referential integrity & column constraints | UK-03, UK-04 | **PASSED** |
| `tests/test_deep_learning.py` | 6 | PyTorch MLP & Bi-LSTM network architectures | UK-09, UK-10 | **PASSED** |
| `tests/test_discovery.py` | 3 | K-Means clustering persona stability & silhouette score | UK-07, UK-09 | **PASSED** |
| `tests/test_evidence_registry.py` | 5 | Evidence Registry schema validation & path integrity | UK-11 | **PASSED** |
| `tests/test_feature_leakage.py` | 9 | Anti-leakage, checkout restriction, cohort non-bleed | UK-07, UK-08 | **PASSED** |
| `tests/test_hypotheses.py` | 2 | Statistical hypothesis testing battery & FDR control | UK-08, UK-10 | **PASSED** |
| `tests/test_initialization.py` | 8 | Package bootstrapping, config parsing, environment | UK-01, UK-02 | **PASSED** |
| `tests/test_interactive_engine.py` | 4 | Streamlit page loading & inference components | UK-09, UK-11 | **PASSED** |
| `tests/test_models.py` | 5 | Classical ML baseline models (B0-B3) fitting & scoring | UK-08, UK-09 | **PASSED** |
| `tests/test_semantic_pipeline.py` | 7 | Semantic data profiling & currency unit validation | UK-03, UK-04 | **PASSED** |
| `tests/test_simulation_sanity.py` | 5 | What-If policy scenario simulation bounds & monotonicity | UK-08, UK-11 | **PASSED** |
| `tests/test_skkni_consistency.py` | 6 | Canonical SKKNI standard alignment & evidence parity | UK-01 s.d. UK-11 | **PASSED** |
| `tests/test_world_model.py` | 5 | VAR state transition recovery, holdout WAPE evaluation | UK-08, UK-10 | **PASSED** |
| **TOTAL** | **89** | **Complete System & Scientific Test Suite** | **All 11 Units** | **100% PASSED** |

---

## 3. Specific Quality & Anti-Regression Verification

1. **Zero Path Leaks**: All test modules use relative resolution (`Path(__file__).resolve().parent.parent`). No hardcoded operating-system absolute paths exist within test assertions or test reports.
2. **First-Order Cohort Null-Bleeding Test**: `test_first_order_cohort_null_bleeding_regression()` explicitly passes, verifying that missing values in Order 1 are NOT bled from Order 2.
3. **Future Perturbation Invariance**: `test_future_perturbation_invariance()` verifies that altering future Order 2 data leaves prior Order 1 cohort features strictly invariant.
4. **Checkout Point-in-Time Timing**: `test_checkout_stage_restricted_features()` asserts that `approval_lag_hours` and `order_approved_at` are classified as restricted and excluded from `E1_early_warning_checkout`.
