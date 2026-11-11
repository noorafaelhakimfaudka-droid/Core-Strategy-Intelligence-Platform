# CSIP BNSP ASSESSMENT READINESS REPORT
## Evaluasi Kesiapan Bukti Asesmen Kompetensi Ilmuwan Data (Data Scientist)
### Lembaga Sertifikasi Profesi: LSP TRI | Kode Skema: SKM/2905/LSP-TRI/VII/2025
### Acuan Standar: SKKNI Nomor 299 Tahun 2020 | Target Jenjang: KKNI Level 7

- **Dokumen ID**: `CSIP-REP-BNSP-READINESS-2026-V7`
- **Versi Rilis**: 7.0.0
- **Tanggal Evaluasi**: 2026-11-11
- **Auditor Kompetensi**: Senior Data Scientist, SKKNI Mapping Specialist & Competency Assessor Auditor
- **Status Evaluasi**: COMPREHENSIVE INTERNAL ASSESSMENT COMPLETE

---

## 1. Pernyataan Batasan dan Integritas Penilaian

> **DISCLAIMER HUKUM & METODOLOGI**:
> Laporan ini merupakan audit kesiapan internal (*internal readiness assessment*) terhadap portofolio bukti proyek CSIP. Laporan ini **BUKAN merupakan keputusan resmi sertifikasi BNSP**. 
> Keputusan akhir mengenai kompetensi peserta sepenuhnya berada di bawah wewenang Asesor Kompetensi berlisensi dan Lembaga Sertifikasi Profesi (LSP TRI) melalui proses asesmen resmi (uji portofolio, wawancara, dan observasi praktik).

---

## 2. Ringkasan Eksekutif Kesiapan per Unit Kompetensi

Dari 11 Unit Kompetensi yang dipersyaratkan oleh Skema Sertifikasi Ilmuwan Data LSP TRI:
- **10 Unit Kompetensi (90,9%)**: Berkategori **READY FOR EVIDENCE REVIEW** (100% KUK didukung oleh artefak teknis, kode produksi teruji, notebook tereksekusi, dan laporan evaluasi kuantitatif).
- **1 Unit Kompetensi (9,1%)**: Berkategori **READY WITH MINOR EVIDENCE GAPS (EXTERNAL CONFIRMATION REQUIRED)** pada UK-01 (Menentukan Objektif Bisnis), di mana bukti teknis dan analitis telah lengkap, namun persetujuan bisnis akhir disimulasikan melalui dokumen internal karena menggunakan open-source historical dataset.
- **0 Unit Kompetensi**: Berkategori *NOT YET READY*.

### Tabel Rekapitulasi Kesiapan 11 Unit Kompetensi

| No | Kode Unit | Judul Unit Kompetensi | Elemen | KUK | Status Kesiapan Internal | Keterangan Verifikasi |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **UK-01** | `J.62DMI00.001.1` | Menentukan Objektif Bisnis | 4 | 12 | **READY WITH MINOR EVIDENCE GAPS** | Analisis bisnis & ROI lengkap; sign-off eksternal disimulasikan |
| **UK-02** | `J.62DMI00.002.1` | Menentukan Tujuan Teknis Data Science | 2 | 5 | **READY FOR EVIDENCE REVIEW** | Estimand formal, kriteria teknis, dan anti-leakage contract lengkap |
| **UK-03** | `J.62DMI00.005.1` | Menelaah Data | 3 | 6 | **READY FOR EVIDENCE REVIEW** | Audit Foreign Key relasional 9 tabel dan profiling semantik lengkap |
| **UK-04** | `J.62DMI00.006.1` | Memvalidasi Data | 3 | 6 | **READY FOR EVIDENCE REVIEW** | Deteksi anomali tanggal pengiriman dan audit missingness ulasan teruji |
| **UK-05** | `J.62DMI00.007.1` | Menentukan Objek Data | 2 | 4 | **READY FOR EVIDENCE REVIEW** | Definisi 4 objek data analitis (order, cohort, corpus, panel) tervalidasi |
| **UK-06** | `J.62DMI00.008.1` | Membersihkan Data | 3 | 6 | **READY FOR EVIDENCE REVIEW** | Deduplikasi geolokasi (-98,1%), isolasi split-before-fit teruji |
| **UK-07** | `J.62DMI00.009.1` | Mengkonstruksi Data | 2 | 4 | **READY FOR EVIDENCE REVIEW** | Rekayasa 41 fitur domain, jarak Haversine, perbaikan cohort drop_duplicates |
| **UK-08** | `J.62DMI00.012.1` | Membangun Skenario Model | 2 | 6 | **READY FOR EVIDENCE REVIEW** | Tangga Baseline B0-B3 dan Dynamic State Transition VAR(1) teruji |
| **UK-09** | `J.62DMI00.013.1` | Membangun Model | 2 | 4 | **READY FOR EVIDENCE REVIEW** | Pelatihan model deterministik pada partisi temporal (Train/Val/Test) |
| **UK-10** | `J.62DMI00.014.1` | Mengevaluasi Hasil Pemodelan | 2 | 5 | **READY FOR EVIDENCE REVIEW** | PR-AUC (Average Precision), kalibrasi Platt, SHAP, out-of-sample holdout |
| **UK-11** | `J.62DMI00.015.1` | Melakukan Proses Review Pemodelan | 2 | 5 | **READY FOR EVIDENCE REVIEW** | Failure Register, penolakan hipotesis H3, tinjauan bias survivor diungkapkan |
| **TOTAL** | **11 UNIT** | **STANDAR SKKNI NO. 299/2020** | **27** | **63** | **READY FOR EVIDENCE AUDIT** | **60 VERIFIED, 3 PARTIALLY_VERIFIED, 0 MISSING** |

---

## 3. Penilaian Rinci Kesiapan Asesmen per Unit Kompetensi

---

### UK-01: J.62DMI00.001.1 — Menentukan Objektif Bisnis
1. **Persyaratan Standar**: 4 Elemen, 12 KUK. Mampu mengidentifikasi latar belakang bisnis, menentukan objektif analitis, metrik keberhasilan, dan mengkaji kelayakan biaya-manfaat.
2. **Aktivitas CSIP**: Menganalisis friksi keterlambatan pengiriman e-commerce Olist (8,0% pesanan terlambat, penurunan rating dari 4,14 menjadi 2,15) dan merumuskan analisis ROI potensi penghematan kompensasi ~R$ 142.000.
3. **Artefak Bukti**:
   - `notebooks/01_business_and_data_understanding.ipynb` (Section 1.1)
   - `config/business.yaml`
   - `reports/csip_data_scientist_technical_report.md`
4. **Hasil Verifikasi**: 9 KUK VERIFIED, 3 KUK PARTIALLY_VERIFIED (KUK 2.2, 3.3, 4.3).
5. **Kesenjangan Bukti**: Ketiadaan tanda tangan pengguna bisnis eksternal riil (diungkapkan secara transparan).
6. **Kesiapan Demonstrasi**: SANGAT BAIK. Peserta dapat memaparkan kalkulasi bisnis dan rasional penentuan metrik secara mendalam.
7. **Kategori Kesiapan**: **READY WITH MINOR EVIDENCE GAPS (EXTERNAL CONFIRMATION REQUIRED)**.

---

### UK-02: J.62DMI00.002.1 — Menentukan Tujuan Teknis Data Science
1. **Persyaratan Standar**: 2 Elemen, 5 KUK. Mampu menerjemahkan masalah bisnis ke tujuan teknis data science dan menentukan kriteria kesuksesan pemodelan.
2. **Aktivitas CSIP**: Merumuskan estimand formal $\mathbb{P}(Y=1 \mid X_{t_0}, \text{Delivered}=1)$, menetapkan aturan anti-leakage waktu checkout, dan menetapkan ambang batas evaluasi teknis (PR-AUC > 0,1096, Brier Score < 0,15, WAPE < 20%).
3. **Artefak Bukti**:
   - `docs/methodology/PREDICTION_CONTRACT.md`
   - `config/features.yaml` (Anti-leakage governance)
   - `notebooks/01_business_and_data_understanding.ipynb` (Section 2)
4. **Hasil Verifikasi**: 5/5 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK. Peserta siap menjelaskan batasan estimand dan justifikasi metrik imbalanced.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-03: J.62DMI00.005.1 — Menelaah Data
1. **Persyaratan Standar**: 3 Elemen, 6 KUK. Mampu mengidentifikasi sumber data, memverifikasi struktur relasional, dan melakukan profiling semantik.
2. **Aktivitas CSIP**: Memuat 9 tabel relasional e-commerce Olist, memvalidasi Foreign Key (0 orphan records), dan melakukan profiling statistik semantik (tipe data, kardinalitas, missingness, deteksi satuan moneter).
3. **Artefak Bukti**:
   - `src/csip/data/loader.py`
   - `src/csip/data/semantic_profiler.py`
   - `notebooks/02_data_validation_and_cleaning.ipynb`
4. **Hasil Verifikasi**: 6/6 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK. Peserta dapat menjalankan pemeriksaan relasional langsung di depan asesor.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-04: J.62DMI00.006.1 — Memvalidasi Data
1. **Persyaratan Standar**: 3 Elemen, 6 KUK. Mampu mengidentifikasi anomali data, menguji konsistensi aturan bisnis, dan mengaudit missing value.
2. **Aktivitas CSIP**: Mengidentifikasi 23 anomali pengiriman mendahului pembelian, mengaudit 646 ulasan tidak diobservasi (dipertahankan sebagai NaN), dan memeriksa duplikasi koordinat geolokasi.
3. **Artefak Bukti**:
   - `reports/data_quality_report.md`
   - `reports/audit/LABEL_OBSERVABILITY_AUDIT.csv`
   - `tests/test_data_validation.py` (9 tests passed)
4. **Hasil Verifikasi**: 6/6 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-05: J.62DMI00.007.1 — Menentukan Objek Data
1. **Persyaratan Standar**: 2 Elemen, 4 KUK. Mampu menentukan unit analisis (grain), kriteria inklusi/eksklusi populasi, dan skema tabel analitis.
2. **Aktivitas CSIP**: Membangun 4 objek data analitis formal (`order_level`, `customer_cohort`, `review_corpus`, `weekly_system_state`) dengan spesifikasi skema yang ketat.
3. **Artefak Bukti**:
   - `docs/methodology/PREDICTION_CONTRACT.md` (Section 6)
   - `src/csip/features/engineer.py`
   - `data/processed/*.parquet`
4. **Hasil Verifikasi**: 4/4 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-06: J.62DMI00.008.1 — Membersihkan Data
1. **Persyaratan Standar**: 3 Elemen, 6 KUK. Mampu menjalankan prosedur pembersihan, menangani missing value, duplikasi, dan mencegah data leakage.
2. **Aktivitas CSIP**: Menyaring anomali kronologis, melakukan deduplikasi koordinat geolokasi (-98,1%), deduplikasi ulasan via `latest_created`, serta menerapkan protokol transformer `fit` train / `transform` test.
3. **Artefak Bukti**:
   - `src/csip/cleaning/cleaner.py`
   - `src/csip/cleaning/auto_cleaner.py`
   - `tests/test_cleaning_pipeline.py` (8 tests passed)
4. **Hasil Verifikasi**: 6/6 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-07: J.62DMI00.009.1 — Mengkonstruksi Data
1. **Persyaratan Standar**: 2 Elemen, 4 KUK. Mampu merekayasa fitur prediktif, melakukan seleksi fitur, dan pengelompokan persona.
2. **Aktivitas CSIP**: Mengonstruksi 41 fitur domain, jarak Haversine, interaksi logistik, agregasi riwayat point-in-time, pengelompokan K-Means persona ($k=3$), serta perbaikan pemilihan cohort berbasis `drop_duplicates(subset=['customer_unique_id'], keep='first')`.
3. **Artefak Bukti**:
   - `src/csip/features/engineer.py`
   - `src/csip/discovery/clusterer.py`
   - `reports/audit/FEATURE_AVAILABILITY_AUDIT.csv` (29 fitur terdaftar)
   - `tests/test_feature_leakage.py` (9 tests passed)
4. **Hasil Verifikasi**: 4/4 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-08: J.62DMI00.012.1 — Membangun Skenario Model
1. **Persyaratan Standar**: 2 Elemen, 6 KUK. Mampu menyusun skenario perbandingan algoritma, menentukan kriteria seleksi, dan merancang validasi temporal.
2. **Aktivitas CSIP**: Merancang Tangga Baseline B0-B3 (Naive, Ridge, Decision Tree, Random Forest, LightGBM) dan model transisi dinamis Vector AutoRegressive (VAR) dengan out-of-sample holdout.
3. **Artefak Bukti**:
   - `src/csip/models/classic.py`
   - `src/csip/world/state_transition.py`
   - `docs/methodology/WORLD_MODEL_SPECIFICATION.md`
4. **Hasil Verifikasi**: 6/6 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-09: J.62DMI00.013.1 — Membangun Model
1. **Persyaratan Standar**: 2 Elemen, 4 KUK. Mampu melatih model machine learning, mengatur hiperparameter, dan memisahkan partisi data secara deterministik.
2. **Aktivitas CSIP**: Melatih model supervised dan deep learning pada partisi waktu historis (Train: 64.156, Val: 19.684, Test: 12.630 pesanan) menggunakan seed deterministik (`random_state=42`) dan menyimpan bobot model ke `artifacts/models/`.
3. **Artefak Bukti**:
   - `src/csip/models/trainer.py`
   - `scripts/run_ml_experiments.py`
   - `artifacts/models/*.joblib`, `artifacts/models/*.pt`
   - `tests/test_ml_models.py` (13 tests passed)
4. **Hasil Verifikasi**: 4/4 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-10: J.62DMI00.014.1 — Mengevaluasi Hasil Pemodelan
1. **Persyaratan Standar**: 2 Elemen, 5 KUK. Mampu mengevaluasi performa model dengan metrik yang valid, melakukan kalibrasi probabilitas, dan interpretasi fitur.
2. **Aktivitas CSIP**: Mengevaluasi model menggunakan PR-AUC (Average Precision tanpa bias, LightGBM Champion = 0,3061), ROC-AUC, F1-Score, Brier Score, kalibrasi Platt Scaling (-44,59% Brier), SHAP TreeExplainer, serta backtest out-of-sample World Model (WAPE ongkir 7,55%, delay 19,80%).
3. **Artefak Bukti**:
   - `artifacts/reports/ml_leaderboard.json` / `ml_leaderboard.csv`
   - `reports/audit/WORLD_MODEL_AUDIT.md`
   - `src/csip/evaluation/explainer.py`
   - `tests/test_model_evaluation.py` (7 tests passed)
4. **Hasil Verifikasi**: 5/5 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

### UK-11: J.62DMI00.015.1 — Melakukan Proses Review Pemodelan
1. **Persyaratan Standar**: 2 Elemen, 5 KUK. Mampu melakukan tinjauan metodologi, mengidentifikasi keterbatasan model, mencatat kegagalan, dan menyusun mitigasi.
2. **Aktivitas CSIP**: Menjalankan audit forensik menyeluruh, mencatat penolakan hipotesis H3 secara transparan di Failure Register, mengungkapkan survivor bias populasi, menyusun batas non-kausal World Model, dan merancang skenario mitigasi bisnis.
3. **Artefak Bukti**:
   - `reports/model_evaluation_and_review_report.md`
   - `reports/evidence/evidence_and_failure_register.md`
   - `docs/limitations/KNOWN_LIMITATIONS.md`
   - `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`
4. **Hasil Verifikasi**: 5/5 KUK VERIFIED (100%).
5. **Kesiapan Demonstrasi**: SANGAT BAIK.
6. **Kategori Kesiapan**: **READY FOR EVIDENCE REVIEW**.

---

## 4. Kesimpulan Kesiapan Asesmen

Portofolio proyek CSIP Version 7 memenuhi kualifikasi pembuktian kompetensi Ilmuwan Data (Data Scientist) tingkat KKNI Level 7 secara komprehensif. Seluruh 11 unit kompetensi terpetakan dengan rantai bukti yang koheren, dapat direproduksi (*reproducible*), dan bebas dari klaim berlebihan yang tidak didukung data.

Paket bukti ini dinyatakan:
**SIAP DIAJUKAN UNTUK ASESMEN PORTOFOLIO DAN UJI KOMPETENSI RESMI BNSP DI LSP TRI.**
