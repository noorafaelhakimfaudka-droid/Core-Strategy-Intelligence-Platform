# PANDUAN ASESOR — BUKTI KOMPETENSI ILMUWAN DATA (DATA SCIENTIST)
## Verifikasi Portofolio Proyek Berbasis Bukti Kerja Nyata (Project-Based Evidence)
### Skema Sertifikasi: Ilmuwan Data (Data Scientist) — LSP TRI | Kode: SKM/2905/LSP-TRI/VII/2025
### Standar Acuan: SKKNI No. 299 Tahun 2020 (11 Unit Kompetensi, 27 Elemen, 63 KUK)

---

## 1. Pengantar dan Ringkasan Eksekutif untuk Asesor

Selamat datang pada paket bukti asesmen kompetensi proyek **Core Strategy & Intelligence Platform (CSIP)**. Dokumen ini dirancang khusus untuk memfasilitasi Asesor Kompetensi dalam memverifikasi, menguji ulang, dan menilai pemenuhan seluruh kriteria unjuk kerja (KUK) secara transparan, sistematis, dan dapat dipertanggungjawabkan secara ilmiah.

### Karakteristik Utama Proyek CSIP:
- **Identitas Proyek**: Proyek Data Science observasional end-to-end yang menganalisis perilaku pelanggan, friksi logistik, dan sentimen kepuasan pada ekosistem e-commerce Brasil (Olist, 99.441 pesanan transaksi nyata periode 2016–2018).
- **Integritas Standar**: Sepenuhnya selaras dengan **11 Unit Kompetensi**, **27 Elemen Kompetensi**, dan **63 KUK** SKKNI No. 299/2020.
- **Status Verifikasi Bukti**: 
  - **VERIFIED**: 60 KUK (95,2%) — Didukung oleh kode produksi, notebook tereksekusi, pipeline teruji, dan laporan evaluasi kuantitatif.
  - **PARTIALLY_VERIFIED**: 3 KUK (4,8%) — UK-01 KUK 2.2, 3.3, dan 4.3 terkait tanda tangan persetujuan pemangku kepentingan eksternal (diungkapkan secara jujur sebagai simulasi pada open-source dataset).
  - **MISSING / UNVERIFIED**: 0 KUK (0,0%).
- **Eksekusi 100% Lokal**: Seluruh pipeline, model machine learning (LightGBM, Random Forest, PyTorch), dan simulasi berjalan secara mandiri dan deterministik di lingkungan laptop lokal (RAM 8 GB, CPU mode, tanpa transmisi data ke cloud eksternal).

---

## 2. Struktur Navigasi Bukti Kerja

Asesor dapat memeriksa dan memverifikasi bukti kompetensi melalui struktur direktori berikut:

```
csip/
├── competency/
│   ├── BNSP_MASTER_COMPETENCY_MATRIX.xlsx   # Matriks Pemetaan 63 KUK lengkap dengan format spreadsheet berbobot
│   ├── BNSP_MASTER_COMPETENCY_MATRIX.csv    # Versi CSV terbuka untuk machine-readable audit
│   ├── EVIDENCE_REGISTRY.csv                # Pendaftaran terperinci 63 artefak bukti
│   ├── ASSESSOR_EVIDENCE_GUIDE.md           # Dokumen ini (Panduan Asesor)
│   ├── CANDIDATE_DEMONSTRATION_GUIDE.md     # Panduan Demonstrasi Praktik Peserta Asesmen
│   └── ASSESSMENT_READINESS_REPORT.md       # Laporan Kesiapan Asesmen per Unit Kompetensi
├── notebooks/                               # 14 Jupyter Notebooks tereksekusi lengkap (01 s.d. 14)
├── src/csip/                                # Kode sumber produksi Python terstruktur (11 modul domain)
├── data/                                    # Dataset mentah (raw) dan terproses (processed Parquet)
├── artifacts/                               # Checkpoint model serialisasi (.joblib, .pt) dan metrik evaluasi
├── reports/                                 # Laporan forensik kualitas, bias populasi, dan metodologi
└── tests/                                   # 14 modul test otomatis (87 test cases, 100% lulus)
```

---

## 3. Matriks Verifikasi Bukti per Unit Kompetensi (11 Unit SKKNI)

### Unit 1: J.62DMI00.001.1 — Menentukan Objektif Bisnis
- **Jumlah Elemen**: 4 Elemen | **Jumlah KUK**: 12 KUK (1.1 s.d. 4.3).
- **Aktivitas Pembuktian**: Menerjemahkan permasalahan keterlambatan logistik e-commerce (8,0% pesanan terlambat, penurunan rating dari 4,14 menjadi 2,15) menjadi objektif analitis berorientasi bisnis dan menghitung analisis biaya-manfaat (*cost-benefit analysis* penghematan kompensasi ~R$ 142.000).
- **Lokasi Artefak Utama**:
  - `notebooks/01_business_and_data_understanding.ipynb`
  - `config/business.yaml`
  - `docs/methodology/PREDICTION_CONTRACT.md`
- **Catatan Asesor**: KUK 2.2, 3.3, dan 4.3 berstatus *PARTIALLY_VERIFIED* karena persetujuan pengguna akhir disimulasikan melalui dokumen spesifikasi internal, bukan tanda tangan pengguna riil.

---

### Unit 2: J.62DMI00.002.1 — Menentukan Tujuan Teknis Data Science
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Menetapkan tujuan teknis machine learning: supervised classification kepuasan (`negative_review_flag`), regresi keterlambatan (`delivery_delay_days`), dan retensi 90 hari (`repeat_purchase_flag`). Merumuskan kriteria keberhasilan teknis (PR-AUC > Baseline Naive 0,1096, Brier Score < 0,15, WAPE World Model < 20%).
- **Lokasi Artefak Utama**:
  - `docs/methodology/PREDICTION_CONTRACT.md`
  - `notebooks/01_business_and_data_understanding.ipynb` (Section 2)
  - `config/features.yaml` (Anti-leakage rules)

---

### Unit 3: J.62DMI00.005.1 — Menelaah Data
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 8 KUK (1.1 s.d. 3.3).
- **Aktivitas Pembuktian**: Memuat 9 tabel relasional e-commerce Olist, memverifikasi skema relasional, menguji integritas referensial Foreign Key (100% konsisten, 0 orphan records), dan melakukan profiling statistik semantik (tipe data, missingness, kardinalitas, deteksi unit harga/freight).
- **Lokasi Artefak Utama**:
  - `src/csip/data/loader.py` & `src/csip/data/semantic_profiler.py`
  - `notebooks/02_data_validation_and_cleaning.ipynb`
  - `reports/audit/project_inventory.md`

---

### Unit 4: J.62DMI00.006.1 — Memvalidasi Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Mengidentifikasi anomali data (23 anomali tanggal pengiriman $t_{\text{del}} < t_{\text{pur}}$, duplikasi koordinat geografis yang membengkak 1.0M baris), mengaudit pola missing value (646 ulasan tidak diobservasi), dan memverifikasi kesesuaian data terhadap aturan bisnis.
- **Lokasi Artefak Utama**:
  - `reports/data_quality_report.md`
  - `reports/audit/LABEL_OBSERVABILITY_AUDIT.csv`
  - `tests/test_data_validation.py` (9 automated tests passed)

---

### Unit 5: J.62DMI00.007.1 — Menentukan Objek Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Mengonstruksi 4 objek data analitis dengan definisi butir data (*grain*) dan skema formal:
  1. `order_level` (Grain: `order_id`, 96.470 baris x 42 kolom)
  2. `customer_cohort` (Grain: `customer_unique_id`, 75.318 baris x 23 kolom)
  3. `review_corpus` (Grain: `review_id`, 95.824 baris x 9 kolom)
  4. `weekly_system_state` (Grain: `year_week`, 87 minggu panel)
- **Lokasi Artefak Utama**:
  - `src/csip/features/engineer.py`
  - `data/processed/*.parquet`
  - `docs/methodology/PREDICTION_CONTRACT.md` (Section 6)

---

### Unit 6: J.62DMI00.008.1 — Membersihkan Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Menjalankan pipeline pembersihan deterministik: menyaring anomali kronologis, melakukan deduplikasi geolokasi dengan reduksi memori -98,1%, menangani duplikasi ulasan melalui strategi `latest_created`, dan memastikan isolasi *split-before-transform*.
- **Lokasi Artefak Utama**:
  - `src/csip/cleaning/cleaner.py`
  - `src/csip/cleaning/auto_cleaner.py` (Scikit-Learn Transformer Protocol)
  - `tests/test_cleaning_pipeline.py` (8 automated tests passed)

---

### Unit 7: J.62DMI00.009.1 — Mengkonstruksi Data
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 6 KUK (1.1 s.d. 3.2).
- **Aktivitas Pembuktian**: Mereka 41 fitur domain e-commerce, termasuk jarak spasial Haversine tervektorisasi, rasio ongkir non-linear, interaksi keterlambatan majemuk (`delay_x_freight_ratio`), agregasi riwayat point-in-time (`prior_order_count`), serta pengelompokan persona perilaku via K-Means ($k=3$).
- **Lokasi Artefak Utama**:
  - `src/csip/features/engineer.py`
  - `src/csip/discovery/clusterer.py`
  - `reports/audit/FEATURE_AVAILABILITY_AUDIT.csv` (29 fitur diaudit bebas kebocoran waktu)

---

### Unit 8: J.62DMI00.012.1 — Membangun Skenario Model
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 7 KUK (1.1 s.d. 3.2).
- **Aktivitas Pembuktian**: Merancang skenario pemodelan terstruktur:
  - **Skenario Klasifikasi Tangga Baseline (B0-B3)**: Naive Majority (B0) $\to$ Logistic/Ridge (B1) $\to$ Decision Tree/KNN/Naive Bayes (B2) $\to$ Random Forest & LightGBM (B3).
  - **Skenario Deep Learning**: Categorical Entity Embedding MLP & Bi-LSTM NLP.
  - **Skenario Dynamic State Transition (World Model)**: Vector AutoRegressive VAR(1) dengan regularisasi Ridge untuk simulasi skenario intervensi kebijakan S0-S5.
- **Lokasi Artefak Utama**:
  - `src/csip/models/classic.py` & `src/csip/world/state_transition.py`
  - `docs/methodology/WORLD_MODEL_SPECIFICATION.md`
  - `notebooks/07_supervised_ml_and_competency_lab.ipynb`

---

### Unit 9: J.62DMI00.013.1 — Membangun Model
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 6 KUK (1.1 s.d. 2.3).
- **Aktivitas Pembuktian**: Melatih model machine learning pada partisi waktu historis yang ketat (Train: Minggu 1–64, Val: Minggu 65–78, Test: Minggu 79–87). Seluruh hiperparameter dicatat secara deklaratif dan model diserialisasi secara deterministik (`random_state=42`).
- **Lokasi Artefak Utama**:
  - `src/csip/models/trainer.py`
  - `artifacts/models/*.joblib`, `artifacts/models/*.pt`
  - `scripts/run_ml_experiments.py`

---

### Unit 10: J.62DMI00.014.1 — Mengevaluasi Hasil Pemodelan
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Mengevaluasi model menggunakan metrik klasifikasi imbalanced: PR-AUC (Average Precision tanpa bias), ROC-AUC, F1-Score, Brier Score, dan kalibrasi probabilitas Platt Scaling (memangkas Brier -44,59%). Melakukan atribusi SHAP TreeExplainer serta backtest out-of-sample holdout pada World Model (WAPE ongkir 7,55%, delay 19,80%, volume 19,85%).
- **Lokasi Artefak Utama**:
  - `artifacts/reports/ml_leaderboard.json` & `ml_leaderboard.csv`
  - `src/csip/evaluation/explainer.py` & `src/csip/uncertainty/bootstrap.py`
  - `reports/audit/WORLD_MODEL_AUDIT.md`
  - `tests/test_model_evaluation.py` (7 automated tests passed)

---

### Unit 11: J.62DMI00.015.1 — Melakukan Proses Review Pemodelan
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK (1.1 s.d. 2.2).
- **Aktivitas Pembuktian**: Menjalankan tinjauan metodologi independen menyeluruh: mengaudit batas-batas kebocoran data, mencatat kegagalan dan penolakan hipotesis H3 secara transparan di Failure Register, menguji ketidakpastian via Bootstrap resampling (B=1.000, CI 95%), serta menyusun rekomendasi mitigasi bisnis yang realistis.
- **Lokasi Artefak Utama**:
  - `reports/model_evaluation_and_review_report.md`
  - `reports/evidence/evidence_and_failure_register.md`
  - `reports/hypothesis_report.md`
  - `docs/limitations/KNOWN_LIMITATIONS.md`

---

## 4. Prosedur Uji Petik Mandiri bagi Asesor (Independent Audit Verification)

Asesor dapat menjalankan perintah berikut pada terminal PowerShell/CMD untuk mereproduksi hasil pengujian secara instan:

```powershell
# 1. Jalankan seluruh test suite otomatis (87 test cases terverifikasi)
python -m pytest tests/ -v

# 2. Uji khusus pencegahan kebocoran data dan integritas waktu (Zero Leakage)
python -m pytest tests/test_feature_leakage.py -v

# 3. Periksa leaderboard evaluasi model machine learning
python -c "import pandas as pd; df=pd.read_csv('artifacts/reports/ml_leaderboard.csv'); print(df[['model_name','feature_set_name','split_name','pr_auc','roc_auc','brier_score']].to_string())"

# 4. Verifikasi matriks kompetensi BNSP
python -c "import pandas as pd; df=pd.read_csv('competency/BNSP_MASTER_COMPETENCY_MATRIX.csv'); print(df['evidence_status'].value_counts())"
```
