# CSIP Automated Test Execution Report
## Version 10.0 Verification & Code Quality Audit
### Reference Standard: SKKNI No. 299 Tahun 2020 | LSP TRI Scheme: SKM/2905/LSP-TRI/VII/2025

- **Document ID**: `CSIP-REP-V10-TER-01`
- **Execution Timestamp**: 2026-11-11 15:25:44 UTC+7
- **Python Runtime**: Python 3.14.7 (64-bit AMD64)
- **Pytest Version**: Pytest 9.1.1 (pluggy 1.6.0)
- **Operating System**: Windows 64-bit (win32)
- **Overall Result**: **92 PASSED, 0 FAILED, 0 SKIPPED (100% Pass Rate)**
- **Duration**: 31.84 seconds

---

## 1. Verbatim Test Suite Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: . (repo root)
configfile: pytest.ini
plugins: anyio-4.14.2, asyncio-1.4.0
collected 92 items

tests\test_artifact_parity.py .......                                    [  7%]
tests\test_cleaning_and_grain.py ......                                  [ 14%]
tests\test_data_pipeline_stress.py ......                                [ 20%]
tests\test_data_validation.py .....                                      [ 26%]
tests\test_deep_learning.py ......                                       [ 32%]
tests\test_discovery.py ...                                              [ 35%]
tests\test_evidence_registry.py .....                                    [ 41%]
tests\test_feature_leakage.py ...........                                [ 53%]
tests\test_hypotheses.py ..                                              [ 55%]
tests\test_initialization.py ........                                    [ 64%]
tests\test_interactive_engine.py ....                                    [ 68%]
tests\test_models.py .....                                               [ 73%]
tests\test_semantic_pipeline.py .......                                  [ 81%]
tests\test_simulation_sanity.py .....                                    [ 86%]
tests\test_skkni_consistency.py .......                                  [ 94%]
tests\test_world_model.py .....                                          [100%]

============================= 92 passed in 31.84s =============================
```

---

## 2. Test Module Breakdown

| Module | Items | Coverage Focus | Status |
|:---|:---:|:---|:---:|
| `tests/test_artifact_parity.py` | 7 | Model files & Parquet schema parity | PASSED |
| `tests/test_cleaning_and_grain.py` | 6 | Anomaly removal, deduplication & grain definition | PASSED |
| `tests/test_data_pipeline_stress.py` | 6 | Pipeline stress test under data distribution shifts | PASSED |
| `tests/test_data_validation.py` | 5 | Foreign Key referential integrity & column constraints | PASSED |
| `tests/test_deep_learning.py` | 6 | PyTorch MLP & Bi-LSTM network architectures | PASSED |
| `tests/test_discovery.py` | 3 | K-Means clustering persona stability & silhouette score | PASSED |
| `tests/test_evidence_registry.py` | 5 | Evidence Registry schema validation & path integrity | PASSED |
| `tests/test_feature_leakage.py` | 11 | Anti-leakage, checkout restriction, cohort non-bleed, dual contract & target exact mapping | PASSED |
| `tests/test_hypotheses.py` | 2 | Statistical hypothesis testing battery & FDR control | PASSED |
| `tests/test_initialization.py` | 8 | Dual package import path (`csip` & `src.csip`) & registry | PASSED |
| `tests/test_interactive_engine.py` | 4 | Streamlit session state & interactive engine sanity | PASSED |
| `tests/test_models.py` | 5 | Baseline ladder B0-B3 models & temporal splits | PASSED |
| `tests/test_semantic_pipeline.py` | 7 | Data profiling & semantic schema inference | PASSED |
| `tests/test_simulation_sanity.py` | 5 | Scenario policy simulation logic & non-causal bounds | PASSED |
| `tests/test_skkni_consistency.py` | 7 | SKKNI 299/2020 11 units, 27 elements, 63 KUKs exact canonical text & doc distribution | PASSED |
| `tests/test_world_model.py` | 5 | VAR(1) vector autoregressive stability & holdout WAPE | PASSED |
| **TOTAL** | **92** | **16 Test Modules | 100% Comprehensive Automated Verification** | **ALL PASSED** |

---

## 3. Verification Conclusion
The complete CSIP test suite executes deterministically in 31.84 seconds on standard 8GB RAM hardware with zero test skips and zero test failures.
