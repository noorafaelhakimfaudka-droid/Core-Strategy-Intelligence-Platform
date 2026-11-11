# CSIP V6 Automated Test Execution Report

**Document ID**: CSIP-REP-V6-TER-01  
**Execution Timestamp**: 2026-11-11 14:23:16  
**Python Runtime**: Python 3.14.7 (64-bit AMD64)  
**Pytest Version**: Pytest 9.1.1  
**Operating System**: Windows 64-bit (win32)  
**Overall Result**: **87 PASSED, 0 FAILED, 0 SKIPPED (100% Pass Rate)**  
**Duration**: 22.76 seconds  

---

## 1. Verbatim Test Suite Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: .
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
plugins: anyio-4.14.2, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False
collected 87 items

tests\test_artifact_parity.py .......                                    [  8%]
tests\test_cleaning_and_grain.py ......                                  [ 14%]
tests\test_data_pipeline_stress.py ......                                [ 21%]
tests\test_data_validation.py .....                                      [ 27%]
tests\test_deep_learning.py ......                                       [ 34%]
tests\test_discovery.py ...                                              [ 37%]
tests\test_evidence_registry.py .....                                    [ 43%]
tests\test_feature_leakage.py .......                                    [ 51%]
tests\test_hypotheses.py ..                                              [ 54%]
tests\test_initialization.py ........                                    [ 63%]
tests\test_interactive_engine.py ....                                    [ 67%]
tests\test_models.py .....                                               [ 73%]
tests\test_semantic_pipeline.py .......                                  [ 81%]
tests\test_simulation_sanity.py .....                                    [ 87%]
tests\test_skkni_consistency.py ......                                   [ 94%]
tests\test_world_model.py .....                                          [100%]

============================= 87 passed in 22.76s =============================
```

---

## 2. Test Module Breakdown

| Module | Items | Coverage Focus | Status |
|:---|:---:|:---|:---:|
| `tests/test_artifact_parity.py` | 7 | Model files & Parquet schema parity | PASSED |
| `tests/test_cleaning_and_grain.py` | 6 | Order grain uniqueness & geolocation dedup | PASSED |
| `tests/test_data_pipeline_stress.py` | 6 | Edge cases, missing values, empty inputs | PASSED |
| `tests/test_data_validation.py` | 5 | Range checks, date format, foreign key integrity | PASSED |
| `tests/test_deep_learning.py` | 6 | MLP and BiLSTM PyTorch architectures | PASSED |
| `tests/test_discovery.py` | 3 | Behavioral clustering & latent PCA projection | PASSED |
| `tests/test_evidence_registry.py` | 5 | Evidence schema & claim levels (L0-L3) | PASSED |
| `tests/test_feature_leakage.py` | 7 | **Anti-leakage rules, target contamination, AP metric** | PASSED |
| `tests/test_hypotheses.py` | 2 | Statistical tests H1-H6 on real clean data | PASSED |
| `tests/test_initialization.py` | 8 | Package setup & 11 SKKNI unit mappings | PASSED |
| `tests/test_interactive_engine.py` | 4 | Decision simulator & scenario duel | PASSED |
| `tests/test_models.py` | 5 | Supervised models B0-B3 training and predict | PASSED |
| `tests/test_semantic_pipeline.py` | 7 | Fluent data profiling & continuous ML engine | PASSED |
| `tests/test_simulation_sanity.py` | 5 | Physical bounds and non-linear interactions | PASSED |
| `tests/test_skkni_consistency.py` | 6 | Canonical SKKNI 63 KUKs & 30 unique evidence files | PASSED |
| `tests/test_world_model.py` | 5 | **VAR transition, bounds, OOS holdout backtest** | PASSED |
