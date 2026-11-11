# CSIP Test Coverage & Code Quality Assurance Report
## Verification for BNSP Data Scientist KKNI Level 7 Assessment

**Document ID**: `CSIP-REP-COVERAGE-2026-V4`  
**Execution Date**: 2026-11-11  
**Runner**: Pytest 9.1.1  
**Total Test Cases**: **83 passed in 22.63s (100% Pass Rate)**  
**Scope**: 11 Unit Kompetensi, 27 Elemen Kompetensi, 63 KUK  
**Status**: VERIFIED & REPRODUCIBLE  

---

## 1. Test Suite Coverage Summary

Pengujian kode pada CSIP dirancang untuk memverifikasi logika inti (*core domain logic*), kontrak protokol Scikit-Learn, pencegahan kebocoran target, kalkulasi statistik inferensial, serta integritas referensi standar kompetensi SKKNI No. 299 Tahun 2020.

| Modul Uji | Jumlah Test | Komponen yang Diverifikasi | Hasil |
|:---|:---:|:---|:---:|
| `tests/test_cleaning_and_grain.py` | 8 | Integritas order grain, penanganan deduplikasi spasial | PASSED |
| `tests/test_data_pipeline_stress.py` | 11 | Stress pipeline dataset kecil, missing value, memory limit | PASSED |
| `tests/test_data_validation.py` | 6 | Validasi tipe, schema null-rate, integritas data referensial | PASSED |
| `tests/test_deep_learning.py` | 6 | Arsitektur MLP Tabular & BiLSTM NLP text sentiment | PASSED |
| `tests/test_discovery.py` | 5 | K-Means & HDBSCAN behavioral clustering customer-seller | PASSED |
| `tests/test_evidence_registry.py` | 5 | Skema registry, hierarki klaim (L0-L3), grade bukti | PASSED |
| `tests/test_feature_leakage.py` | 6 | Isolasi temporal split, korelasi masa depan = 0.00 | PASSED |
| `tests/test_hypotheses.py` | 5 | Uji hipotesis statistik H1-H5 (Welch t-test, Mann-Whitney) | PASSED |
| `tests/test_initialization.py` | 8 | Inisialisasi package, definisi 11 unit SKKNI | PASSED |
| `tests/test_interactive_engine.py` | 5 | Router kueri omni, scenario duel, text constellation | PASSED |
| `tests/test_models.py` | 6 | Model baseline B0-B3, PR-AUC, ROC-AUC, Brier score | PASSED |
| `tests/test_semantic_pipeline.py` | 5 | Profiling semantik & pipeline ML terotomasi | PASSED |
| `tests/test_simulation_sanity.py` | 3 | Simulasi skenario counterfactual & sanity check | PASSED |
| `tests/test_skkni_consistency.py` | 5 | 11 unit, 27 elemen, 63 KUK verbatim & 63 file fisik | PASSED |
| **TOTAL** | **83** | **SELURUH MODUL SISTEM CSIP** | **83 PASSED** |