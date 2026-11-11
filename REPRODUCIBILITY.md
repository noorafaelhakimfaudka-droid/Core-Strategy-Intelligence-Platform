# CSIP End-to-End Reproducibility Guide
## Core Strategy & Intelligence Platform (CSIP) — Version 1.0.0

**Standard**: SKKNI No. 299 Tahun 2020 Subbidang Data Science  
**Certification Scheme**: LSP TRI (SKM/2905/LSP-TRI/VII/2025) — Data Scientist KKNI Level 7  
**Target Environment**: Standard Laptop (Windows/macOS/Linux) with 8 GB RAM  
**Execution Time**: Full reproduction pipeline executes in < 30 seconds  

---

## 1. Persyaratan Sistem & Lingkungan Eksekusi
- **Sistem Operasi**: Windows 10/11 x64, macOS, atau Linux (Ubuntu 20.04+)
- **Python**: Versi 3.10 s/d 3.14 (teruji pada Python 3.14.7 x64)
- **RAM**: Minimal 8 GB RAM (arsitektur dirancang *memory-bounded* tanpa dependensi cloud/GPU)
- **Penyimpanan**: Ruang kosong disk >= 500 MB

---

## 2. Langkah Setup & Instalasi Dependensi Terkunci

### Langkah 2.1: Klon Repositori & Pembuatan Virtual Environment
```bash
# Klon repositori
git clone https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform.git csip_1.0.0
cd csip_1.0.0

# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### Langkah 2.2: Instalasi Dependensi Terkunci
```bash
python -m pip install --upgrade pip
pip install -e .[dev,ml_advanced]
```

### Langkah 2.3: Verifikasi Instalasi Paket Inti
```bash
python -c "import csip; print('CSIP Version:', csip.__version__)"
```
Keluaran yang diharapkan: `CSIP Version: 1.0.0`

---

## 3. Reproduksi Satu Perintah (One-Command Reproduction)

CSIP menyediakan pipeline reproduksi otomatis ujung-ke-ujung yang mengeksekusi:
1. Validasi integritas dan kelengkapan data olahan.
2. Pembangunan fitur dan *categorical fold target encoding*.
3. Rolling-Origin Temporal Cross-Validation (4 fold ekspansif dengan embargo ketat 90 hari).
4. Pengujian 6 hipotesis statistik empiris (H1-H6) dengan koreksi Benjamini-Hochberg FDR.
5. Evaluasi stabilitas klaster perilaku menggunakan moving bootstrap ARI dan Jaccard.
6. Audit dan validasi eksekusi 14 notebook penelitian beserta perhitungan hash sel output.

### Perintah Eksekusi:
```bash
# Menggunakan Makefile:
make reproduce

# Atau langsung via Python:
python scripts/reproduce_all.py
```

### Artefak Hasil Eksekusi:
- `artifacts/reports/temporal_cv_results.json`: Hasil metrik CV temporal per fold dan evaluasi locked test set.
- `reports/evaluation/TEMPORAL_CV_REPORT.md`: Laporan komparasi model, bootstrap 95% CI, dan Decision Curve Analysis.
- `artifacts/reports/hypothesis_evaluation.json`: Nilai statistik, p-value teruji, dan FDR Benjamini-Hochberg.
- `artifacts/reports/cluster_stability_evaluation.json`: Nilai Adjusted Rand Index dan Jaccard stabilitas klaster k=3..5.
- `reports/notebooks/notebook_exec_summary.json`: Rangkuman status eksekusi dan hash output 14 notebook.

---

## 4. Menjalankan Seluruh Rangkaian Pengujian (Automated Test Suite)

Untuk memverifikasi kebenaran implementasi fungsional dan mencegah regresi:
```bash
# Menggunakan Makefile:
make test

# Atau langsung via pytest:
python -m pytest -v --tb=short
```

Semua 210+ pengujian unit, integrasi, regresi, metodologi, dan konsistensi bukti harus berstatus `PASSED`. Hasil pengujian aktual terekam pada `reports/testing/pytest_actual.txt`.

---

## 5. Verifikasi Gerbang Kualitas Rilis (Release Gate Verification)

CSIP menerapkan 12 Gerbang Kualitas Rilis (Gates G1–G12) yang diuji secara independen:
```bash
# Menggunakan Makefile:
make verify

# Atau langsung via Python:
python tools/verify_release.py
```

Laporan status gerbang tersimpan dalam format machine-readable di `reports/verification/gates.json`.

---

## 6. Menjalankan Dashboard Interaktif Streamlit

Untuk mengeksplorasi visualisasi data, simulasi kebijakan alternatif, dan review bukti kompetensi:
```bash
# Menggunakan Makefile:
make app-test  # Menjalankan pengujian otomatis antarmuka

# Menjalankan dashboard secara lokal:
streamlit run app/streamlit_app.py
```
Akses dashboard melalui browser di `http://localhost:8501`. Seluruh angka yang ditampilkan dibaca langsung dari `artifacts/` tanpa *hardcoding*.

---

## 7. Menjalankan Prediksi Batch (CLI Deployment)

Untuk menjalankan model Champion dalam skenario deployment batch:
```bash
python scripts/predict_batch.py \
  --model-path artifacts/models/best_delivery_delay_lightgbm.joblib \
  --input-csv data/sample_input.csv \
  --output-csv data/sample_output.csv
```

Skrip ini secara otomatis memvalidasi kontrak skema input dan menolak model dengan status `RESEARCH_ONLY`.

---

## 8. Catatan Batasan & Kejujuran Ilmiah
- **Data Sekunder Observasional**: Dataset e-commerce Olist (2016-2018) adalah data historis non-eksperimental. Klaim pengaruh dibatasi pada tingkat asosiasional (L2), bukan bukti kausalitas intervensi tanpa randomisasi A/B testing.
- **Model Risiko Ulasan Bersifat Retrospektif**: Fitur keterlambatan kurir (`delivery_delay_days`) hanya tersedia pasca-delivery sehingga model risiko ulasan tidak dapat dieksekusi pada saat checkout.
- **Batas Toleransi Deterministik**: Model berbasis pohon (LightGBM/Random Forest) dan kalkulasi statistik menggunakan *fixed seed* (seed=42). Perbedaan minor floating-point antar-arsitektur prosesor berada dalam batas toleransi numerik `< 1e-4`.
