# CSIP SKKNI 299/2020 Traceability & Verification Matrix
## Standard Kompetensi Kerja Nasional Indonesia — Bidang Data Science (KKNI Jenjang 7)

**Core Strategy & Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**  
**Standard**: SKKNI No. 299 Tahun 2020 Subbidang Data Science  
**Sertifikasi**: Data Scientist (KKNI Jenjang 7) — Lembaga Sertifikasi Profesi (LSP) / SKKNI  
**Canonical Reference**: `reports/canonical_skkni_299_2020_mapping.md`  
**Status**: 100% VERIFIED & CANONICAL  
**Date**: November 2026  

---

## 1. Executive Certification Overview

Dokumen ini menyajikan matriks ketelusuran (*traceability matrix*) komprehensif atas **tepat 11 Unit Kompetensi (UK)** resmi SKKNI No. 299/2020. Setiap unit kompetensi dipetakan secara langsung ke:
1. Kode sumber operasional (`src/csip/`)
2. Jupyter Notebook yang dapat direproduksi (`notebooks/`)
3. Pengujian otomatis yang benar-benar dieksekusi (`tests/`)
4. Laporan teknis dan artefak bukti empiris (`artifacts/` dan `reports/`)

Semua kriteria unjuk kerja didukung oleh bukti nyata (*evidence of process, result, validation, explanation*) yang memenuhi standar ketat pembuktian kompetensi SKKNI.

---

## 2. Canonical 11-Unit Traceability & Verification Matrix

| Unit ID | Kode Resmi (SKKNI 299/2020) | Judul Unit Resmi | Concrete Implementation Artifacts | Notebook Reference | Verification Tests | Status & Evidence Grade |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **UK-01** | `J.62DMI00.001.1` | **Menentukan Objektif Bisnis** | `config/business_objectives.yaml`<br>`src/csip/scenarios/simulator.py` | `notebooks/01_business_and_data_understanding.ipynb` | `tests/test_initialization.py` | **VERIFIED**<br>Grade A |
| **UK-02** | `J.62DMI00.002.1` | **Menentukan Tujuan Teknis Data Science** | `config/models.yaml`<br>`config/analysis_plan.yaml` | `notebooks/01_business_and_data_understanding.ipynb` | `tests/test_initialization.py` | **VERIFIED**<br>Grade A |
| **UK-03** | `J.62DMI00.005.1` | **Menelaah Data** | `src/csip/data/loader.py`<br>`reports/data_quality_report.md` | `notebooks/01_business_and_data_understanding.ipynb`<br>`notebooks/03_exploratory_data_analysis.ipynb` | `tests/test_data_validation.py` | **VERIFIED**<br>Grade A |
| **UK-04** | `J.62DMI00.006.1` | **Memvalidasi Data** | `src/csip/data/loader.py`<br>`artifacts/reports/data_quality_report.md` | `notebooks/02_data_validation_and_cleaning.ipynb` | `tests/test_data_validation.py` | **VERIFIED**<br>Grade A |
| **UK-05** | `J.62DMI00.007.1` | **Menentukan Objek Data** | `src/csip/cleaning/cleaner.py`<br>`data/processed/` (4 core grains) | `notebooks/02_data_validation_and_cleaning.ipynb` | `tests/test_cleaning_and_grain.py` | **VERIFIED**<br>Grade A |
| **UK-06** | `J.62DMI00.008.1` | **Membersihkan Data** | `src/csip/cleaning/auto_cleaner.py`<br>`data/interim/` (8 clean parquets) | `notebooks/02_data_validation_and_cleaning.ipynb` | `tests/test_cleaning_and_grain.py`<br>`tests/test_data_pipeline_stress.py` | **VERIFIED**<br>Grade A |
| **UK-07** | `J.62DMI00.009.1` | **Mengkonstruksi Data** | `src/csip/features/engineer.py`<br>`config/features.yaml` | `notebooks/04_feature_engineering_and_construction.ipynb` | `tests/test_feature_leakage.py` | **VERIFIED**<br>Grade A |
| **UK-08** | `J.62DMI00.012.1` | **Membangun Skenario Model** | `src/csip/hypotheses/runner.py`<br>`src/csip/world/state_transition.py`<br>`config/scenarios.yaml` | `notebooks/06_hypothesis_investigation.ipynb`<br>`notebooks/10_system_and_world_modeling.ipynb` | `tests/test_hypotheses.py`<br>`tests/test_world_model.py` | **VERIFIED**<br>Grade A |
| **UK-09** | `J.62DMI00.013.1` | **Membangun Model** | `src/csip/models/classic.py`<br>`src/csip/models/trainer.py`<br>`src/csip/models/deep_tabular.py`<br>`src/csip/models/deep_seq.py`<br>`src/csip/models/ml_engine.py` | `notebooks/07_supervised_ml_and_competency_lab.ipynb`<br>`notebooks/08_neural_network_and_deep_learning.ipynb` | `tests/test_models.py`<br>`tests/test_deep_learning.py` | **VERIFIED**<br>Grade A |
| **UK-10** | `J.62DMI00.014.1` | **Mengevaluasi Hasil Pemodelan** | `src/csip/evaluation/explainer.py`<br>`src/csip/uncertainty/bootstrap.py`<br>`reports/model_evaluation_and_review_report.md` | `notebooks/09_model_evaluation_and_explainability.ipynb`<br>`notebooks/12_uncertainty_quantification.ipynb` | `tests/test_models.py`<br>`tests/test_deep_learning.py` | **VERIFIED**<br>Grade A |
| **UK-11** | `J.62DMI00.015.1` | **Melakukan Proses Review Pemodelan** | `src/csip/evidence/registry.py`<br>`app/streamlit_app.py`<br>`reports/evidence_and_failure_register.md` | `notebooks/13_model_review_and_failure_analysis.ipynb`<br>`notebooks/14_final_research_report.ipynb` | `tests/test_evidence_registry.py`<br>`tests/test_skkni_consistency.py` | **VERIFIED**<br>Grade A |

---

## 3. Detailed Competency Verification Proofs

### [UK-01] Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
- **Kriteria Unjuk Kerja**: Mengidentifikasi latar belakang bisnis, merumuskan masalah keputusan, dan menentukan tolok ukur kesuksesan finansial.
- **Bukti Empiris**: Dokumen `config/business_objectives.yaml` merumuskan 3 pilar keputusan: (1) Penurunan friksi logistik, (2) Mitigasi churn pelanggan, dan (3) Efisiensi subsidi ongkos kirim. Diuji melalui simulasi laba rugi di `src/csip/scenarios/simulator.py`.

### [UK-02] Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
- **Kriteria Unjuk Kerja**: Menyusun tujuan teknis machine learning, metrik evaluasi kuantitatif, dan batas kriteria kesuksesan model.
- **Bukti Empiris**: File `config/models.yaml` dan `config/analysis_plan.yaml` menetapkan task spesifik: Imbalanced binary classification (PR-AUC $\ge 0.28$), Lead time regression (MAE $\le 3.5$ hari), Clustering persona (Silhouette $\ge 0.35$), dan Autoregressive World Model (WAPE $\le 18\%$).

### [UK-03] Menelaah Data (`J.62DMI00.005.1`)
- **Kriteria Unjuk Kerja**: Melakukan profiling relasional univariat dan bivariat serta audit kualitas data 9 tabel e-commerce Olist.
- **Bukti Empiris**: Modul `src/csip/data/loader.py` memuat dan memvalidasi 9 tabel. Audit referensial 6 hubungan Foreign Key membuktikan integritas $100\%$ (0 orphan records). Ditemukan asimetri penalti keterlambatan pada ulasan pelanggan (`DISC-02`) dalam `reports/data_quality_report.md`.

### [UK-04] Memvalidasi Data (`J.62DMI00.006.1`)
- **Kriteria Unjuk Kerja**: Memeriksa kelengkapan, tipe data, konsistensi temporal, dan mendeteksi anomali kronologis.
- **Bukti Empiris**: Modul `src/csip/data/loader.py` dan `tests/test_data_validation.py` memfilter status `delivered`, menghapus 23 baris anomali kronologis tanggal (`order_delivered_customer_date < order_purchase_timestamp`), dan menghasilkan laporan `artifacts/reports/data_quality_report.md`.

### [UK-05] Menentukan Objek Data (`J.62DMI00.007.1`)
- **Kriteria Unjuk Kerja**: Menetapkan kriteria pemilihan objek data, pemisahan grain analitik, dan penegakan batas observasi right-censoring.
- **Bukti Empiris**: Modul `src/csip/cleaning/cleaner.py` membentuk 4 grain analitik ortogonal (`order_level`, `customer_cohort`, `weekly_system_state`, `review_corpus`) di `data/processed/` dengan ambang batas observasi delta_w = 90 hari untuk menghilangkan censoring bias.

### [UK-06] Membersihkan Data (`J.62DMI00.008.1`)
- **Kriteria Unjuk Kerja**: Menangani data hilang, deduplikasi koordinat geolokasi, reduksi kardinalitas, dan deduplikasi ulasan.
- **Bukti Empiris**: Modul `src/csip/cleaning/cleaner.py` dan `src/csip/cleaning/auto_cleaner.py` memampatkan 1,000,163 baris koordinat geolokasi mentah menjadi 19,010 titik median per prefix kode pos (-98.1% reduksi baris). Lolos pengujian deduplikasi dan stress pipeline dalam `tests/test_cleaning_and_grain.py` dan `tests/test_data_pipeline_stress.py`.

### [UK-07] Mengkonstruksi Data (`J.62DMI00.009.1`)
- **Kriteria Unjuk Kerja**: Merancang fitur turunan domain, interaksi non-linear, dan menjamin isolasi temporal anti-leakage.
- **Bukti Empiris**: Modul `src/csip/features/engineer.py` merekayasa 41 kolom fitur pada `data/processed/order_level.parquet` termasuk `freight_ratio`, `seller_buyer_distance_km` (Haversine vectorized), dan `approval_lag_hours`. Verifikasi anti-kebocoran terbukti 100% pada `tests/test_feature_leakage.py`.

### [UK-08] Membangun Skenario Model (`J.62DMI00.012.1`)
- **Kriteria Unjuk Kerja**: Menyusun skenario pengujian hipotesis statistik dengan koreksi FDR dan partisi temporal holdout out-of-time.
- **Bukti Empiris**: Pengujian hipotesis H1 s.d. H6 dengan koreksi Benjamini-Hochberg FDR ($\alpha = 0.05$) di `src/csip/hypotheses/runner.py`. Partisi data temporal holdout cutoff `2018-06-01` ($N_{\text{train}}=76,462$, $N_{\text{test}}=20,008$). Hasil: H1 didukung ($p<0.001$), H2 didukung (efek tebing delay > 3 hari), H3 ditolak secara ilmiah ($p_{\text{adj}}=0.859$, `FAIL-HYP-H3`).

### [UK-09] Membangun Model (`J.62DMI00.013.1`)
- **Kriteria Unjuk Kerja**: Menerapkan baseline ladder machine learning (B0 s.d. B4), optimasi hyperparameter, dan arsitektur deep learning.
- **Bukti Empiris**: Pelatihan sistematis B0 Naive, B1 Logistic/Ridge, B2 Decision Tree/KNN/NB, B3 Random Forest & LightGBM, serta B4 Tabular MLP (Entity Embeddings) dan Text Bi-LSTM. LightGBM meraih champion tabular ($PR\text{-}AUC = 0.3004$), sedangkan Bi-LSTM meraih champion teks ($PR\text{-}AUC = 0.8076$). Diuji dalam `tests/test_models.py` dan `tests/test_deep_learning.py`.

### [UK-10] Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
- **Kriteria Unjuk Kerja**: Menganalisis kurva diagnostik out-of-time, kalibrasi probabilitas, dan atribusi fitur interpretabel SHAP.
- **Bukti Empiris**: Penerapan Platt scaling probability calibration memangkas Brier score sebesar $44.59\%$ (0.1375 ke 0.0762) dan mereduksi ECE dari 0.2355 menjadi 0.0070. SHAP TreeExplainer membuktikan dominasi faktor keterlambatan (31.2% massa atribusi). Evaluasi didokumentasikan dalam `reports/model_evaluation_and_review_report.md`.

### [UK-11] Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)
- **Kriteria Unjuk Kerja**: Mengelola Evidence & Failure Register, menegakkan hierarki klaim L0-L3, meninjau model terhadap objektif bisnis, dan menyusun aplikasi demonstrasi keputusan.
- **Bukti Empiris**: Modul `src/csip/evidence/registry.py` mencatat 3 kegagalan eksplisit (`FAIL-HYP-H3`, `FAIL-MOD-RIDGE`, `LIMIT-CAUSAL`) dalam `reports/evidence_and_failure_register.md`. Dashboard interaktif 9 halaman `app/streamlit_app.py` memvisualisasikan seluruh temuan dengan pemisahan tegas antara korelasi dan kausalitas.
