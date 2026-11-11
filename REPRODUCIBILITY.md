# CSIP End-to-End Reproducibility Guide
## Core Strategy & Intelligence Platform (CSIP) — BNSP Data Scientist KKNI Level 7

**Standard**: SKKNI No. 299 Tahun 2020 Subbidang Data Science  
**Environment Target**: Standard Laptop (Windows/macOS/Linux) with 8 GB RAM  
**Repository**: `https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform`  
**Date**: November 2026  

---

## 1. Environment & Hardware Prerequisites

CSIP dirancang secara ketat untuk dapat dijalankan secara mandiri pada komputer/laptop standar tanpa ketergantungan pada klaster cloud atau GPU eksternal:

| Parameter | Spesifikasi Minimum | Rekomendasi Pengujian |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11, Ubuntu 22.04 LTS, macOS 12+ | Windows 11 x64 / Linux x86_64 |
| **Python Runtime** | Python 3.10 s.d. Python 3.14 | Python 3.11 atau 3.12 |
| **RAM / Memory** | 8 GB RAM | 8 GB RAM (Peak usage < 4.2 GB) |
| **Disk Space** | 2.5 GB Free Disk Space | SSD |
| **GPU / Accelerator** | Tidak Diwajibkan (PyTorch CPU fallback aktif) | CPU Multi-core |

---

## 2. Step-by-Step Installation

### Langkah 1: Klon Repositori & Buat Virtual Environment
```bash
git clone https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform.git
cd Core-Strategy-Intelligence-Platform

# Buat virtual environment lokal
python -m venv .venv

# Aktivasi virtual environment:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### Langkah 2: Instalasi Dependensi Terverifikasi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Dataset Verification & Checksum Audit

Seluruh tabel analitis siap pakai telah disertakan dalam repositori pada direktori `data/processed/` dan `data/interim/` dalam format Apache Parquet yang terkompresi tinggi.

Jalankan audit checksum SHA-256 untuk memverifikasi integritas bitwise dataset:
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

Jika ingin mereproduksi pembersihan dari raw CSV Olist:
1. Unduh dataset publik Olist dari Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Simpan 9 file CSV ke dalam folder `data/raw/`.
3. Jalankan pipeline pembersihan:
   ```bash
   python -c "from src.csip.cleaning.cleaner import run_full_cleaning_pipeline; run_full_cleaning_pipeline()"
   python -c "from src.csip.features.engineer import run_feature_engineering_pipeline; run_feature_engineering_pipeline()"
   ```

---

## 4. Executing Automated Test Suite

Untuk memastikan seluruh pipeline, model, dan aturan anti-leakage berfungsi sempurna:
```bash
# Jalankan seluruh test suite (78+ tests)
python -m pytest tests/ -v
```

Hasil yang diharapkan:
- 100% tests PASSED.
- Zero assertion error.
- Zero target leakage detected (`test_feature_leakage.py`).
- 11 SKKNI units strictly consistent (`test_skkni_consistency.py`).

---

## 5. Running Research Notebooks in Exact Sequence

14 Jupyter Notebooks dalam folder `notebooks/` disusun secara bertahap merefleksikan alur kerja ilmiah Data Scientist:

| Urutan | Notebook File | Deskripsi & Unit SKKNI Terkait |
| :---: | :--- | :--- |
| **01** | `01_business_and_data_understanding.ipynb` | Formulasi masalah bisnis, objektif teknis, dan profiling awal (UK-01, UK-02). |
| **02** | `02_data_validation_and_cleaning.ipynb` | Validasi kelengkapan, filter anomali tanggal, dan pembersihan spasial (UK-04, UK-05, UK-06). |
| **03** | `03_exploratory_data_analysis.ipynb` | Analisis bivariat dan profiling distribusi 9 tabel (UK-03). |
| **04** | `04_feature_engineering_and_construction.ipynb` | Rekayasa 41 fitur domain, rasio ongkir, Haversine vectorized (UK-07). |
| **05** | `05_behavioral_discovery_unsupervised.ipynb` | Klastering persona sensitivitas ongkir (k=3, Silhouette=0.3865) (UK-07). |
| **06** | `06_hypothesis_investigation.ipynb` | Pengujian hipotesis H1-H6 dengan Benjamini-Hochberg FDR (UK-08). |
| **07** | `07_supervised_ml_and_competency_lab.ipynb` | Pelatihan baseline ladder B0-B3 (Champion LightGBM PR-AUC 0.3004) (UK-09). |
| **08** | `08_neural_network_and_deep_learning.ipynb` | Tabular MLP Entity Embeddings & Text Bi-LSTM (PR-AUC 0.8076) (UK-09). |
| **09** | `09_model_evaluation_and_explainability.ipynb` | SHAP TreeExplainer, kurva PR/ROC, kalibrasi Platt scaling (-44.6% Brier) (UK-10). |
| **10** | `10_system_and_world_modeling.ipynb` | Autoregressive State-Space dynamics ekosistem makro (WAPE 15.83%) (UK-08). |
| **11** | `11_alternative_world_simulation.ipynb` | Simulasi What-If skenario kebijakan logistik S0-S5 (UK-08, UK-10). |
| **12** | `12_uncertainty_quantification.ipynb` | Residual bootstrap 95% confidence interval (UK-10). |
| **13** | `13_model_review_and_failure_analysis.ipynb` | Failure Register audit, review keterbatasan dan bias model (UK-11). |
| **14** | `14_final_research_report.ipynb` | Sintesis temuan ilmiah dan laporan komprehensif tingkat enterprise (UK-11). |

---

## 6. Launching Local Streamlit Decision Studio

Untuk menjalankan antarmuka visual interaktif:
```bash
python -m streamlit run app/streamlit_app.py
```
Aplikasi akan terbuka pada peramban web di: `http://localhost:8501`.
Aplikasi juga dapat diakses secara publik melalui Streamlit Cloud:  
👉 `https://core-strategy-intelligence-platform.streamlit.app`

