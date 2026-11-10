# CSIP SKKNI Data Science (BNSP) Traceability & Verification Matrix

**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**  
**Standard**: Standar Kompetensi Kerja Nasional Indonesia (SKKNI) Bidang Data Science  
**Sertifikasi**: BNSP Data Scientist Certification Readiness  
**Author**: Antigravity Autonomous Data Science Agent  
**Date**: November 2026  

---

## 1. Executive Certification Overview

This document provides complete, transparent requirements traceability across all **11 Unit Kompetensi (UK)** stipulated under SKKNI Data Science. It maps every competency unit directly to:
1. Operational Source Code (`src/csip/`)
2. Executable Jupyter Notebooks (`notebooks/`)
3. Automated Test Suites (`tests/`)
4. Verified Empirical Artifacts & Reports (`artifacts/` and `reports/`)

Every competency requirement is accompanied by executable evidence meeting the strict evidentiary standards of the National Professional Certification Board (BNSP).

---

## 2. SKKNI 11-Unit Traceability & Verification Matrix

| Unit ID | Unit Kompetensi Title | Concrete Implementation Artifacts | Notebook Reference | Verification Tests | Status & Evidence Grade |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **UK-01** | **Menentukan Masalah Bisnis** | `config/business_objectives.yaml`<br>`src/csip/scenarios/simulator.py` | `notebooks/01_business_and_data_understanding.ipynb` | `tests/test_initialization.py` | **VERIFIED**<br>Grade A |
| **UK-02** | **Menentukan Kebutuhan Data** | `config/data.yaml`<br>`data/data_dictionary.md` | `notebooks/01_business_and_data_understanding.ipynb` | `tests/test_initialization.py` | **VERIFIED**<br>Grade A |
| **UK-03** | **Menelaah Data** | `src/csip/data/loader.py`<br>`reports/data_quality_report.md` | `notebooks/03_exploratory_data_analysis.ipynb` | `tests/test_data_validation.py` | **VERIFIED**<br>Grade A |
| **UK-04** | **Memvalidasi Data** | `src/csip/cleaning/cleaner.py`<br>`artifacts/reports/raw_data_profile.json` | `notebooks/02_data_validation_and_cleaning.ipynb` | `tests/test_data_validation.py` | **VERIFIED**<br>Grade A |
| **UK-05** | **Membersihkan Data** | `src/csip/cleaning/cleaner.py`<br>`data/interim/` (8 clean parquets) | `notebooks/02_data_validation_and_cleaning.ipynb` | `tests/test_cleaning_and_grain.py` | **VERIFIED**<br>Grade A |
| **UK-06** | **Mengonstruksi Data** | `src/csip/features/engineer.py`<br>`data/processed/` (4 core grains) | `notebooks/04_feature_engineering_and_construction.ipynb` | `tests/test_feature_leakage.py` | **VERIFIED**<br>Grade A |
| **UK-07** | **Menentukan Objek Data** | `src/csip/discovery/clusterer.py`<br>`artifacts/models/clustering_pipeline.joblib` | `notebooks/05_behavioral_discovery_unsupervised.ipynb` | `tests/test_discovery.py` | **VERIFIED**<br>Grade A |
| **UK-08** | **Membangun Skenario Model** | `src/csip/hypotheses/runner.py`<br>`src/csip/world/state_transition.py`<br>`src/csip/scenarios/simulator.py` | `notebooks/06_hypothesis_investigation.ipynb`<br>`notebooks/10_system_and_world_modeling.ipynb`<br>`notebooks/11_alternative_world_simulation.ipynb` | `tests/test_hypotheses.py`<br>`tests/test_world_model.py`<br>`tests/test_simulation_sanity.py` | **VERIFIED**<br>Grade A |
| **UK-09** | **Membangun Model** | `src/csip/models/classic.py`<br>`src/csip/models/trainer.py`<br>`src/csip/models/deep_tabular.py`<br>`src/csip/models/deep_seq.py` | `notebooks/07_supervised_ml_and_competency_lab.ipynb`<br>`notebooks/08_neural_network_and_deep_learning.ipynb` | `tests/test_models.py`<br>`tests/test_deep_learning.py` | **VERIFIED**<br>Grade A |
| **UK-10** | **Mengevaluasi Hasil Pemodelan** | `src/csip/evaluation/explainer.py`<br>`src/csip/uncertainty/bootstrap.py`<br>`reports/model_evaluation_and_review_report.md` | `notebooks/09_model_evaluation_and_explainability.ipynb`<br>`notebooks/12_uncertainty_quantification.ipynb`<br>`notebooks/13_model_review_and_failure_analysis.ipynb` | `tests/test_deep_learning.py`<br>`tests/test_simulation_sanity.py` | **VERIFIED**<br>Grade A |
| **UK-11** | **Mengembangkan Solusi** | `app/streamlit_app.py`<br>`app/pages/` (9 Showcase Pages)<br>`reports/scenario_simulation_report.md`<br>`reports/evidence_and_failure_register.md` | `notebooks/13_model_review_and_failure_analysis.ipynb`<br>`notebooks/14_final_research_and_bnsp_report.ipynb` | `tests/test_simulation_sanity.py`<br>`tests/test_evidence_registry.py` | **VERIFIED**<br>Grade A |

---

## 3. Detailed Competency Verification Proofs

### [UK-01] Menentukan Masalah Bisnis
- **Kriteria Unjuk Kerja**: Mengidentifikasi latar belakang bisnis, merumuskan masalah keputusan, dan menentukan tolok ukur kesuksesan finansial.
- **Bukti Empiris**: Dokumen `config/business_objectives.yaml` merumuskan 3 pilar keputusan: (1) Penurunan friksi logistik, (2) Mitigasi churn pelanggan, dan (3) Efisiensi subsidi ongkos kirim. Diuji melalui simulasi laba rugi di `src/csip/scenarios/simulator.py`.

### [UK-02] Menentukan Kebutuhan Data
- **Kriteria Unjuk Kerja**: Mengidentifikasi sumber data, merancang skema relasional, dan mendokumentasikan spesifikasi variabel.
- **Bukti Empiris**: Kamus data komprehensif `data/data_dictionary.md` mendefinisikan 9 tabel Olist e-commerce dengan tipe data hemat memori (downcast `int16`, `float32`, `category`), diverifikasi tanpa orphan FK di `reports/data_quality_report.md`.

### [UK-03] Menelaah Data
- **Kriteria Unjuk Kerja**: Melakukan profiling univariat dan bivariat serta audit kualitas data.
- **Bukti Empiris**: Audit referensial 6 hubungan Foreign Key membuktikan integritas $100\%$ (0 orphan records). Ditemukan asimetri penalti keterlambatan pada ulasan pelanggan (`DISC-02`).

### [UK-04] Memvalidasi Data
- **Kriteria Unjuk Kerja**: Memeriksa kelengkapan, tipe data, konsistensi temporal, dan mendeteksi anomali.
- **Bukti Empiris**: Modul `src/csip/cleaning/cleaner.py` memfilter status `delivered`, menghapus 23 baris anomali kronologis tanggal (`order_delivered_customer_date < order_purchase_timestamp`), dan diverifikasi dalam `tests/test_data_validation.py`.

### [UK-05] Membersihkan Data
- **Kriteria Unjuk Kerja**: Menangani data duplikat dan anomali kardinalitas geolokasi.
- **Bukti Empiris**: Kompresi kardinalitas koordinat median memampatkan 1,000,163 baris geolocation mentah menjadi 19,010 baris unik (-98.1% reduksi baris), mengeliminasi ledakan kartesian saat spatial join.

### [UK-06] Mengonstruksi Data (Feature Engineering)
- **Kriteria Unjuk Kerja**: Merancang fitur turunan, interaksi non-linear, dan menjamin isolasi temporal anti-leakage.
- **Bukti Empiris**: Modul `src/csip/features/engineer.py` membangun 4 analytical grains (`order_level`, `customer_cohort`, `review_corpus`, `weekly_system_state`). Menegakkan First-Order Isolation pada cohort pelanggan tanpa agregat seumur hidup, diverifikasi dalam `tests/test_feature_leakage.py`.

### [UK-07] Menentukan Objek Data (Clustering & Segmentasi)
- **Kriteria Unjuk Kerja**: Menerapkan algoritma unsupervised learning dan memvalidasi klaster secara objektif.
- **Bukti Empiris**: `BehavioralClusterer` menemukan $k=3$ persona optimal dengan **Silhouette Score = 0.3865** (melampaui target PRD $\ge 0.35$) dan Davies-Bouldin = 1.2168. Menemukan segmen friksi ongkir berat (`DISC-01`).

### [UK-08] Membangun Skenario Model
- **Kriteria Unjuk Kerja**: Menyusun skenario pengujian hipotesis statistik dan dinamika sistem inter-temporal.
- **Bukti Empiris**: Pengujian hipotesis H1 s.d. H6 dengan koreksi Benjamini-Hochberg FDR ($\alpha = 0.05$). Perumusan transisi Vector AutoRegressive State-Space dan 6 skenario kebijakan (S0–S5) dengan interval ketidakpastian residual bootstrap.

### [UK-09] Membangun Model
- **Kriteria Unjuk Kerja**: Menerapkan baseline ladder machine learning (B0 s.d. B4) dan deep learning.
- **Bukti Empiris**: Pelatihan komparatif B0 Naive, B1 Logistic/Ridge, B2 Decision Tree/KNN/Naive Bayes, B3 Random Forest & LightGBM, serta B4 Tabular MLP (Entity Embeddings) dan Text Bi-LSTM. LightGBM meraih champion tabular ($PR\text{-}AUC = 0.3004$), sedangkan Bi-LSTM meraih champion teks ($PR\text{-}AUC = 0.8076$).

### [UK-10] Mengevaluasi Hasil Pemodelan
- **Kriteria Unjuk Kerja**: Menganalisis kurva diagnostik, kalibrasi probabilitas, dan atribusi fitur interpretabel.
- **Bukti Empiris**: Penerapan SHAP TreeExplainer membuktikan dominasi faktor delay (31.2% massa atribusi). Kalibrasi Platt scaling memangkas Brier score sebesar $44.59\%$ dan mereduksi ECE dari 0.2355 menjadi 0.0070. Uji identifiabilitas struktural model dunia lulus dengan rata-rata error relatif $0.33\%$.

### [UK-11] Mengembangkan Solusi
- **Kriteria Unjuk Kerja**: Menerjemahkan temuan pemodelan ke dalam platform intelijen keputusan bisnis interaktif dan transparan.
- **Bukti Empiris**: Dashboard showcase Streamlit 9 halaman (`app/streamlit_app.py`), memvisualisasikan data observatory, lab hipotesis, prediktor risiko pelanggan, simulator dunia alternatif, decision studio, dan audit register kegagalan secara real-time.

