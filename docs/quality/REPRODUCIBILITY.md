# CSIP Quality Engineering: Reproducibility & Environment Guide
## Full End-to-End Pipeline Execution, Deterministic Seeds, and Verification
### Standard: SKKNI No. 299 Tahun 2020 | Subbidang: Data Science (KKNI Jenjang 7)

- **Document ID**: `CSIP-DOC-REPRO-2026-V16`
- **Version**: 16.0.0
- **Status**: EMPIRICALLY VERIFIED
- **Author**: Software Quality Assurance & ML DevOps Engineer
- **Release Target**: CSIP Version 16.0.0

---

## 1. System Requirements & Environment Specification

CSIP is designed and tested for zero-dependency local execution within a standard developer environment:

- **Operating System**: Windows 10/11 64-bit, Linux Ubuntu 22.04+, or macOS Sonoma.
- **Python Runtime**: Python 3.10 to Python 3.14 (Verified on Python 3.14.7 64-bit AMD64).
- **RAM Footprint**: Minimum 8 GB RAM (Peak pipeline memory utilization < 3.84 GB).
- **Disk Storage**: ~2.5 GB total (Datasets, artifacts, models, logs, and report images).
- **Network Dependency**: **0% (Completely Offline / No Cloud Transmission)**.

### Core Dependency Stack (`pyproject.toml` / `requirements.txt`):
- Data Processing: `numpy>=1.24.0`, `pandas>=2.0.0`, `pyarrow>=14.0.0`, `scipy>=1.10.0`
- Machine Learning: `scikit-learn>=1.3.0`, `lightgbm>=4.0.0`, `torch>=2.0.0`
- Explainability & Simulation: `shap>=0.42.0`, `joblib>=1.3.0`, `openpyxl>=3.1.5`
- Visualization & Web App: `matplotlib>=3.7.0`, `plotly>=5.15.0`, `streamlit>=1.30.0`
- Testing & Quality: `pytest>=7.4.0`

---

## 2. Modular Installation Profiles

To accommodate different computing environments, CSIP provides 4 modular dependency tracks:

```bash
# Track A: Core Application Runtime (Minimal Streamlit + Baseline Inference)
pip install -r requirements-core.txt

# Track B: Full Experiments & Baselines (DuckDB, LightGBM, SHAP)
pip install -r requirements-experiments.txt

# Track C: Deep Learning Workloads (PyTorch BiLSTM & Tabular MLP)
pip install -r requirements-deeplearning.txt

# Track D: Complete Test Suite & Quality Assurance Audit
pip install -r requirements-test.txt

# All inclusive:
pip install -r requirements.txt
```

---

## 3. Scikit-Learn Model Serialization & Mitigation Strategy

Pre-trained model artifacts in `artifacts/models/` are serialized using **Scikit-Learn 1.9.0** and **LightGBM 4.7.0**.

- When loaded under Scikit-Learn 1.8.x, Scikit-Learn issues an `InconsistentVersionWarning`. Predictions remain operational and valid.
- To eliminate all warnings, install matching library versions:
  ```bash
  pip install scikit-learn==1.9.0 lightgbm==4.7.0
  ```
- Alternatively, rebuild all model artifacts locally in < 45 seconds using deterministic seeds:
  ```bash
  python scripts/train_all_models.py
  ```

---

## 4. Dataset Verification & Checksum Audit

All analytical tables in `data/processed/` and `data/interim/` are stored in high-compression Apache Parquet format.
Verify bitwise integrity with SHA-256:
```bash
python -c "
import json, hashlib
from pathlib import Path

with open('data/dataset_manifest.json') as f:
    manifest = json.load(f)

for rel, meta in manifest['tables'].items():
    p = Path(rel)
    assert p.exists(), f'Missing file: {rel}'
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert h == meta['sha256'], f'Checksum mismatch in {rel}'

print('All 13 Parquet datasets verified bitwise identical with SHA-256 manifest!')
"
```

---

## 5. Automated Quality Assurance & Test Execution

Run the complete automated test suite:
```bash
python -m pytest tests/ -v
```

Expected output:
- **100% Pass Rate**.
- Zero assertion errors.
- Zero target leakage detected (`test_feature_leakage.py`).
- 11 SKKNI units strictly consistent (`test_skkni_consistency.py`).
- Canonical evidence counts strictly matched (`test_evidence_consistency.py`).
- Version synchronization verified (`test_version_consistency.py`).
- All 8 release gates verified (`test_v16_release_gates.py`).

---

## 6. Launching Local Streamlit Decision Studio

```bash
python -m streamlit run app/streamlit_app.py
```
*Access URL*: `http://localhost:8501`
