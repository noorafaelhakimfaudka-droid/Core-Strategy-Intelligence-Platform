# CSIP Testing & Quality Assurance Guide
## Layered Test Architecture, Pytest Execution, Test Categories & Acceptance Gates

**Document Version:** 1.0.0-Definitive  
**Test Suite Size:** 199+ Automated Pytest Tests across 32 Test Modules  
**Target Quality Standard:** Definitive Level Testing & Reproducibility  

---

### 1. LAYERED TEST SUITE ARCHITECTURE

The CSIP test suite is organized into **12 explicit functional tiers** to guarantee scientific validity, data integrity, model reliability, and release readiness:

| Layer # | Test Category | Target Modules | Primary Invariants Verified |
| :---: | :--- | :--- | :--- |
| **L01** | **Final Release Acceptance Gates** | `tests/test_final_release_gates.py`, `tests/test_quality_gates_g1_g15.py` | 15 Quality Gates (G1-G15), version sync, manifest parity |
| **L02** | **Data Contracts & Validation** | `tests/test_data_contracts.py`, `tests/test_data_validation.py` | Schema adherence, column dtypes, non-null, range constraints |
| **L03** | **Data Pipeline Stress & Ingestion**| `tests/test_data_pipeline_stress.py`, `tests/test_cleaning_and_grain.py` | Order-grain deduplication, corrupt input resilience |
| **L04** | **Data Lineage & Provenance** | `tests/test_data_lineage.py` | Unbroken data provenance chain from raw CSVs to models |
| **L05** | **Temporal Leakage Isolation** | `tests/test_temporal_leakage.py` | Strict temporal cutoff (2018-03-01); zero future leakage |
| **L06** | **Feature Leakage Prevention** | `tests/test_feature_leakage.py` | Fit-on-train-only transformers; zero post-delivery target leakage |
| **L07** | **Calibration & Probability Bounds**| `tests/test_calibration_audit.py` | Platt scaling, Brier score < 0.10, ECE < 1.0% |
| **L08** | **Model Robustness & Slices** | `tests/test_model_robustness.py` | Subgroup disparity across states and order value tiers |
| **L09** | **Deep Learning & NLP Pipelines** | `tests/test_deep_learning.py` | BiLSTM tensor shapes, vocab embeddings, checkpoint loading |
| **L10** | **Statistical Hypotheses & World Model**| `tests/test_hypotheses.py`, `tests/test_world_model.py` | Mann-Whitney U, Chi-Square, Ridge VAR spectral radius |
| **L11** | **SKKNI & Canonical Evidence** | `tests/test_skkni_consistency.py`, `tests/test_evidence_registry.py` | 63 KUKs mapped to J.62DMI00.xxx.1; evidence file hashes |
| **L12** | **Interactive Engine & Simulation** | `tests/test_interactive_engine.py`, `tests/test_simulation_sanity.py` | Monte Carlo Markov Chain stability, bounds checking |

---

### 2. EXECUTION INSTRUCTIONS

#### Running the Full Test Suite
```bash
python -m pytest tests/ -v --tb=short
```
*Expected: 199 passed in ~65 seconds.*

#### Running Specific Test Categories
```bash
# Data Contracts and Schema Validation
pytest tests/test_data_contracts.py -v

# Scientific Leakage Prevention
pytest tests/test_temporal_leakage.py tests/test_feature_leakage.py -v

# Model Calibration and Robustness
pytest tests/test_calibration_audit.py tests/test_model_robustness.py -v

# Master Acceptance Gates G1-G15
pytest tests/test_quality_gates_g1_g15.py -v
```

#### Running the Master Quality Gates Runner
```bash
python tools/run_final_validation.py
```
This executes the 19 automated release gates, generates `reports/final/FINAL_QUALITY_GATES_REPORT.md`, and outputs an immediate exit code (0 for PASS, 1 for FAIL).

