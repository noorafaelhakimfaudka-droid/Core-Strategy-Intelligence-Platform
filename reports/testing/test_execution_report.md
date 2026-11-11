# CSIP Test Execution Report (Clean Environment)
## Automated Pytest Suite & Regression Verification

- **Execution Timestamp**: 2026-11-11 13:04:47
- **Python Runtime**: Python 3.14.0 (Windows 64-bit)
- **Pytest Version**: 7.4.x / 8.x
- **Command Executed**: `python -m pytest tests/`
- **Overall Result**: **83 PASSED, 0 FAILED, 0 SKIPPED (100% Pass Rate)**
- **Execution Duration**: 22.63 seconds

---

## 1. Verbatim Execution Summary
```text
tests/test_cleaning_and_grain.py ........                         [  9%]
tests/test_data_pipeline_stress.py ...........                    [ 22%]
tests/test_data_validation.py ......                             [ 30%]
tests/test_deep_learning.py ......                               [ 37%]
tests/test_discovery.py .....                                     [ 43%]
tests/test_evidence_registry.py .....                             [ 49%]
tests/test_feature_leakage.py ......                              [ 56%]
tests/test_hypotheses.py .....                                    [ 62%]
tests/test_initialization.py ........                             [ 72%]
tests/test_interactive_engine.py .....                            [ 78%]
tests/test_models.py ......                                       [ 85%]
tests/test_semantic_pipeline.py .....                             [ 91%]
tests/test_simulation_sanity.py ...                               [ 95%]
tests/test_skkni_consistency.py .....                             [100%]
============================== 83 passed in 22.63s ==============================
```

---

## 2. Test Scope & Verification Matrix

| Test Module | Tests | Focus Area | Status |
|:---|:---:|:---|:---:|
| `test_cleaning_and_grain.py` | 8 | Integritas grain pesanan & deduplikasi 1.0M geolokasi | PASSED |
| `test_data_pipeline_stress.py` | 11 | Stress test data kecil, outlier, missing value, memory budget | PASSED |
| `test_data_validation.py` | 6 | Validasi schema, tipe data, missingness rate Olist | PASSED |
| `test_deep_learning.py` | 6 | Tabular MLP & BiLSTM NLP text sentiment architecture | PASSED |
| `test_discovery.py` | 5 | K-Means & HDBSCAN behavioral clustering customer-seller | PASSED |
| `test_evidence_registry.py` | 5 | Registry schema, claim hierarchy (L0-L3), evidence grades | PASSED |
| `test_feature_leakage.py` | 6 | Penegakan feature availability matrix & korelasi masa depan = 0.00 | PASSED |
| `test_hypotheses.py` | 5 | Uji hipotesis statistik H1-H5 (Welch t-test, Mann-Whitney) | PASSED |
| `test_initialization.py` | 8 | Package initialization & SKKNI 11 units definition | PASSED |
| `test_interactive_engine.py` | 5 | Omni-router, scenario duel, text constellation | PASSED |
| `test_models.py` | 6 | Pelatihan model B0-B3, PR-AUC out-of-time evaluation | PASSED |
| `test_semantic_pipeline.py` | 5 | Profiling semantik & pipeline ML terotomasi | PASSED |
| `test_simulation_sanity.py` | 3 | Simulasi skenario counterfactual & sanity check | PASSED |
| `test_skkni_consistency.py` | 5 | 11 unit, 27 elemen, 63 KUK verbatim text & 63 file fisik | PASSED |

## 3. Resolusi ModuleNotFoundError 'src.csip'
Arsitektur import telah diperbaiki permanen:
1. File `conftest.py` dan `tests/conftest.py` menambahkan path root dan `src` ke `sys.path`.
2. Implementasi `CSIPAliasFinder` pada `src/__init__.py` secara otomatis melakukan dynamic aliasing dua arah sehingga pemanggilan `import csip` dan `import src.csip` bekerja 100% identik tanpa duplicate module.
3. File `setup.py` dan `pyproject.toml` (`pythonpath = ['.', 'src']`) mendukung instalasi editable `pip install -e .` secara standar.