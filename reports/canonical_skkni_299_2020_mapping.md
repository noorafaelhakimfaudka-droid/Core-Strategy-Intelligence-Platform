# CSIP Canonical SKKNI 299/2020 Competency Mapping Specification
## Standard Kompetensi Kerja Nasional Indonesia — Bidang Data Science (KKNI Jenjang 7)

**Document ID**: `CSIP-DOC-SKKNI-CANONICAL-2026`  
**Standard Reference**: Keputusan Menteri Ketenagakerjaan RI No. 299 Tahun 2020  
**Target Certification**: Data Scientist (KKNI Level 7) — Lembaga Sertifikasi Profesi (LSP) / BNSP  
**End-to-End Case Study**: Brazilian E-Commerce Ecosystem Intelligence (~100,000 Transaksi Olist)  
**Status**: CANONICAL SOURCE OF TRUTH (VERIFIED)  
**Date**: November 2026  

---

## 1. Executive Summary & Canonical Architecture

Dokumen ini merupakan **sumber kebenaran tunggal (single canonical source of truth)** pemetaan kompetensi proyek *Core Strategy & Intelligence Platform (CSIP)* terhadap **tepat 11 Unit Kompetensi SKKNI No. 299/2020** Subbidang Data Science.

Setiap unit kompetensi dipetakan secara ketat dan granular mulai dari Kode Unit Resmi, Judul Resmi Kemnaker, Elemen Kompetensi, Kriteria Unjuk Kerja (KUK), Aktivitas Peserta Aktif, Implementasi Nyata pada CSIP, serta 4 Dimensi Bukti Kerja (*Evidence of Process*, *Result*, *Validation*, *Explanation*).

```mermaid
flowchart TD
    subgraph Phase1["1. Business Understanding"]
        U1["UK-01 (J.62DMI00.001.1)<br>Menentukan Objektif Bisnis"] --> U2["UK-02 (J.62DMI00.002.1)<br>Menentukan Tujuan Teknis DS"]
    end
    subgraph Phase2["2. Data Understanding & Preparation"]
        U2 --> U3["UK-03 (J.62DMI00.005.1)<br>Menelaah Data"]
        U3 --> U4["UK-04 (J.62DMI00.006.1)<br>Memvalidasi Data"]
        U4 --> U5["UK-05 (J.62DMI00.007.1)<br>Menentukan Objek Data"]
        U5 --> U6["UK-06 (J.62DMI00.008.1)<br>Membersihkan Data"]
        U6 --> U7["UK-07 (J.62DMI00.009.1)<br>Mengkonstruksi Data"]
    end
    subgraph Phase3["3. Modeling & Evaluation"]
        U7 --> U8["UK-08 (J.62DMI00.012.1)<br>Membangun Skenario Model"]
        U8 --> U9["UK-09 (J.62DMI00.013.1)<br>Membangun Model"]
        U9 --> U10["UK-10 (J.62DMI00.014.1)<br>Mengevaluasi Hasil Pemodelan"]
        U10 --> U11["UK-11 (J.62DMI00.015.1)<br>Melakukan Proses Review Pemodelan"]
    end
```

---

## 2. Canonical Master Table (11 Unit SKKNI 299/2020)

| Internal ID | Kode Unit Resmi (SKKNI 299/2020) | Judul Unit Resmi | Tahap Analitis | Bukti Implementasi Utama | Status Verifikasi |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **UK-01** | `J.62DMI00.001.1` | **Menentukan Objektif Bisnis** | Business Understanding | `config/business_objectives.yaml` | **VERIFIED** (Grade A) |
| **UK-02** | `J.62DMI00.002.1` | **Menentukan Tujuan Teknis Data Science** | Technical Scoping | `config/models.yaml`, `config/analysis_plan.yaml` | **VERIFIED** (Grade A) |
| **UK-03** | `J.62DMI00.005.1` | **Menelaah Data** | Data Exploration | `src/csip/data/loader.py`, `reports/data_quality_report.md` | **VERIFIED** (Grade A) |
| **UK-04** | `J.62DMI00.006.1` | **Memvalidasi Data** | Data Validation | `artifacts/reports/raw_data_profile.json`, `tests/test_data_validation.py` | **VERIFIED** (Grade A) |
| **UK-05** | `J.62DMI00.007.1` | **Menentukan Objek Data** | Data Preparation (Grain) | `data/processed/`, `config/data.yaml` | **VERIFIED** (Grade A) |
| **UK-06** | `J.62DMI00.008.1` | **Membersihkan Data** | Data Cleaning | `src/csip/cleaning/auto_cleaner.py`, `data/interim/` | **VERIFIED** (Grade A) |
| **UK-07** | `J.62DMI00.009.1` | **Mengkonstruksi Data** | Feature Engineering | `src/csip/features/engineer.py`, `tests/test_feature_leakage.py` | **VERIFIED** (Grade A) |
| **UK-08** | `J.62DMI00.012.1` | **Membangun Skenario Model** | Modeling Scenarios | `src/csip/hypotheses/runner.py`, `config/scenarios.yaml` | **VERIFIED** (Grade A) |
| **UK-09** | `J.62DMI00.013.1` | **Membangun Model** | Model Fitting | `src/csip/models/`, `artifacts/models/` | **VERIFIED** (Grade A) |
| **UK-10** | `J.62DMI00.014.1` | **Mengevaluasi Hasil Pemodelan** | Model Evaluation | `reports/model_evaluation_and_review_report.md` | **VERIFIED** (Grade A) |
| **UK-11** | `J.62DMI00.015.1` | **Melakukan Proses Review Pemodelan** | Model Governance & Review | `src/csip/evidence/registry.py`, `reports/evidence_and_failure_register.md` | **VERIFIED** (Grade A) |

---

## 3. Detailed Canonical Unit Specifications (UK-01 s.d. UK-11)

### [UK-01] Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
- **Deskripsi Unit**: Menentukan latar belakang, permasalahan bisnis, poin objektif, dan metrik kesuksesan proyek data science dari sisi pengguna akhir dan pemangku kepentingan organisasi.
- **Elemen Kompetensi**:
  1. Menentukan permasalahan bisnis dan poin-poin objektif bisnis proyek data science dari sisi pengguna akhir.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Latar belakang dan permasalahan bisnis untuk proyek data science diidentifikasi sesuai dengan prosedur bisnis yang berlaku.
  - **1.2**: Poin-poin objektif bisnis diidentifikasi sesuai dengan permasalahan yang telah dipilih dan sesuai dengan kebutuhan organisasi.
  - **1.3**: Poin-poin metrik kesuksesan dibuat sesuai objektif bisnis.
  - **1.4**: Permasalahan bisnis, poin-poin objektif bisnis dan metrik kesuksesan proyek data science ditetapkan sesuai kebutuhan pengguna.
- **Aktivitas Peserta**:
  - Mengidentifikasi 3 friksi operasional e-commerce Olist: (1) Tingginya churn pembeli (97% single purchase), (2) Beban subsidi logistik yang tidak tertarget pada rute jarak jauh, (3) Kerusakan reputasi akibat keterlambatan kirim.
  - Merumuskan tujuan finansial: Memangkas biaya logistik tanpa menurunkan volume GMV.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Formulasi objektif dalam file konfigurasi terstruktur `config/business_objectives.yaml` dan rancangan analisis `config/analysis_plan.yaml`.
  - **Result**: Dokumen target bisnis: Target reduksi keterlambatan ekstrim (>3 hari) sebesar 25%, mitigasi komplain ulasan bintang 1 sebesar 15%.
  - **Validation**: Uji keselarasan parameter dengan modul simulasi laba rugi di `src/csip/scenarios/simulator.py`.
  - **Explanation**: Mengapa 3 pilar ini dipilih? Data historis menunjukkan bahwa friksi pengiriman berkontribusi terhadap 78.4% sentimen ulasan negatif pelanggan.
- **Lokasi Artefak**:
  - Code: `config/business_objectives.yaml`, `config/analysis_plan.yaml`
  - Notebook: `notebooks/01_business_and_data_understanding.ipynb`
  - Report: `reports/research_traceability_matrix.md`, `reports/csip_data_scientist_technical_report.md` (Bagian 2 & 3)
  - Tests: `tests/test_initialization.py`
- **Metode Verifikasi**: Pemeriksaan konsistensi parameter konfigurasi dan eksekusi skenario baseline laba rugi.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-02] Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
- **Deskripsi Unit**: Menyusun tujuan teknis data science serta menentukan daftar dan parameter kriteria kesuksesan teknis yang selaras dengan sasaran bisnis.
- **Elemen Kompetensi**:
  1. Menyusun tujuan teknis data science.
  2. Menentukan kriteria kesuksesan tujuan teknis proyek data science.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Task data science ditentukan sesuai dengan objektif bisnis.
  - **1.2**: Tujuan teknis pelaksanaan proyek data science diidentifikasi sesuai objektif bisnis.
  - **2.1**: Daftar dan parameter kriteria kesuksesan proyek diidentifikasi sesuai dengan tujuan teknis.
  - **2.2**: Kriteria yang teridentifikasi disetujui oleh pengguna sesuai dengan objektif bisnis.
- **Aktivitas Peserta**:
  - Memetakan objektif bisnis ke dalam 4 *technical machine learning tasks*:
    1. *Imbalanced Binary Classification*: Deteksi dini risiko ulasan negatif (review_score $\le 2$).
    2. *Continuous Regression*: Estimasi waktu tiba aktual dan deviasi keterlambatan hari.
    3. *Unsupervised Clustering*: Segmentasi persona perilaku sensitivitas ongkos kirim.
    4. *Vector AutoRegressive State-Space Dynamics*: Pemodelan sistem makro mingguan ekosistem.
  - Menetapkan ambang batas keberhasilan empiris: PR-AUC Tabular $\ge 0.28$ (di atas baseline naive 0.08), Silhouette Score $\ge 0.35$, World Model WAPE $\le 18\%$.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Penyusunan matriks teknis di `config/models.yaml` dan penetapan baseline ladder B0-B4.
  - **Result**: Matriks target kuantitatif terdokumentasi lengkap dengan metrik primer PR-AUC, Brier Score, ECE, MAE, R², Silhouette Score, dan WAPE.
  - **Validation**: Pengujian threshold baseline di `tests/test_initialization.py`.
  - **Explanation**: PR-AUC dipilih sebagai metrik primer klasifikasi risiko daripada ROC-AUC karena distribusi kelas ulasan negatif sangat timpang (~8% minoritas), di mana ROC-AUC dapat memberikan ilusi optimisme palsu.
- **Lokasi Artefak**:
  - Code: `config/models.yaml`, `config/scenarios.yaml`
  - Notebook: `notebooks/01_business_and_data_understanding.ipynb`
  - Report: `reports/research_traceability_matrix.md`
  - Tests: `tests/test_initialization.py`
- **Metode Verifikasi**: Eksekusi uji otomatis baseline ladder dan validasi ambang batas teknis.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-03] Menelaah Data (`J.62DMI00.005.1`)
- **Deskripsi Unit**: Menganalisis tipe, batasan konteks bisnis, relasi antar-tabel data relasional, mendeskripsikan karakteristik statistik dasar, visualisasi grafik, dan merumuskan hipotesis analitis.
- **Elemen Kompetensi**:
  1. Menganalisis tipe dan relasi data.
  2. Menganalisis karakteristik data.
  3. Membuat laporan telaah data.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Tipe data yang terkumpul diidentifikasi sesuai tujuan teknis.
  - **1.2**: Nilai atribut data yang terkumpul diuraikan sesuai dengan batasan konteks bisnisnya.
  - **1.3**: Relasi antar data yang terkumpul diidentifikasi sesuai dengan tujuan teknis.
  - **2.1**: Karakteristik data yang terkumpul disajikan dengan deskripsi statistik dasar.
  - **2.2**: Karakteristik data yang terkumpul disajikan dengan visualisasi grafik.
  - **2.3**: Hasil penyajian data dianalisis karakteristiknya untuk telaah data.
  - **3.1**: Hasil analisis didokumentasikan dalam bentuk laporan sesuai dengan tujuan teknis.
  - **3.2**: Hipotesis disusun berdasar hasil analisis sesuai tujuan teknis data science.
- **Aktivitas Peserta**:
  - Membaca dan menelaah 9 tabel relasional e-commerce Olist (99,441 pesanan, 112,650 item, 100,000 ulasan).
  - Melakukan profiling distribusi: mengidentifikasi *heavy-tailed distribution* pada harga dan ongkir, serta ketimpangan ulasan (bintang 5 mendominasi 57%).
  - Merumuskan hipotesis awal: H1 (Elastisitas rasio ongkir terhadap churn), H2 (Asimetri keterlambatan terhadap rating ulasan), H3 (Dampak rating seller terhadap volume transaksi).
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Skrip profiling `src/csip/data/loader.py` dan eksplorasi visual bivariat pada `notebooks/03_exploratory_data_analysis.ipynb`.
  - **Result**: Kamus data lengkap `data/data_dictionary.md` dan laporan telaah data `reports/data_quality_report.md`.
  - **Validation**: Audit integritas Foreign Key (FK) 100% tanpa record yatim piatu (*0 orphan FK records*).
  - **Explanation**: Hubungan multi-tabel harus diperiksa secara relasional agar agregasi data di tingkat pesanan (*order level*) tidak menghasilkan duplikasi tersembunyi pada saat penggabungan item.
- **Lokasi Artefak**:
  - Code: `src/csip/data/loader.py`, `src/csip/data/semantic_profiler.py`
  - Notebook: `notebooks/01_business_and_data_understanding.ipynb`, `notebooks/03_exploratory_data_analysis.ipynb`
  - Report: `data/data_dictionary.md`, `reports/data_quality_report.md`
  - Tests: `tests/test_data_validation.py`
- **Metode Verifikasi**: Audit integritas referensial dan pengujian statistik distribusi bivariat.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-04] Memvalidasi Data (`J.62DMI00.006.1`)
- **Deskripsi Unit**: Melakukan pengecekan kelengkapan, penilaian kualitas, integritas nilai, konsistensi temporal data, dan menyusun rekomendasi mitigasi kecukupan data.
- **Elemen Kompetensi**:
  1. Melakukan pengecekan kelengkapan data.
  2. Membuat rekomendasi kelengkapan data.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Penilaian kualitas data dari hasil telaah disajikan sesuai tujuan teknis data science.
  - **1.2**: Penilaian tingkat kecukupan data dari hasil telaah disajikan sesuai tujuan teknis data science.
  - **2.1**: Rekomendasi hasil penilaian kualitas disusun sesuai tujuan teknis data science.
  - **2.2**: Rekomendasi hasil penilaian kecukupan data disusun sesuai tujuan teknis data science.
- **Aktivitas Peserta**:
  - Membangun pipeline validasi data otomatis untuk memeriksa: rasio missing values, inkonsistensi tipe, duplikasi baris, dan anomali urutan kronologis timestamp.
  - Menemukan 23 baris anomali kronologis di mana tanggal pengiriman lebih awal daripada tanggal pembelian (`order_delivered_customer_date < order_purchase_timestamp`).
  - Menemukan 11,000+ pesanan berstatus *cancelled/unavailable/shipped* yang belum memiliki tanggal sampai tujuan.
  - Menyusun rekomendasi filter data: hanya pesanan berstatus `delivered` dengan kronologi valid yang dipertahankan untuk pemodelan kepuasan pengiriman.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Pengecekan otomatis di `src/csip/data/loader.py` dan suite pengujian `tests/test_data_validation.py`.
  - **Result**: Laporan audit profil kualitas data `artifacts/reports/raw_data_profile.json` dan `reports/data_quality_report.md`.
  - **Validation**: 100% test passing pada seluruh skenario validasi kelengkapan dan kronologi data.
  - **Explanation**: Memasukkan pesanan yang belum terkirim ke dalam analisis keterlambatan pengiriman akan menimbulkan *right-censoring bias* yang merusak validitas estimasi lead time.
- **Lokasi Artefak**:
  - Code: `src/csip/data/loader.py`, `tests/test_data_validation.py`
  - Notebook: `notebooks/02_data_validation_and_cleaning.ipynb`
  - Report: `artifacts/reports/raw_data_profile.json`, `reports/data_quality_report.md`
  - Tests: `tests/test_data_validation.py`
- **Metode Verifikasi**: Pengujian otomatis rule validation dan verifikasi log filter baris anomali.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-05] Menentukan Objek Data (`J.62DMI00.007.1`)
- **Deskripsi Unit**: Menentukan kriteria pemilihan objek data, menetapkan batasan atau kriteria seleksi data (filtering, sampling, grain definition), serta melakukan dan mendokumentasikan pemilihan objek data.
- **Elemen Kompetensi**:
  1. Menentukan kriteria pemilihan objek data.
  2. Melakukan pemilihan objek data.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Objek data yang relevan dengan tujuan teknis data science diidentifikasi.
  - **1.2**: Batasan atau kriteria seleksi data (filtering/sampling/grain definition) ditetapkan.
  - **2.1**: Data dipilih berdasarkan kriteria inklusi dan eksklusi yang telah ditetapkan.
  - **2.2**: Hasil pemilihan objek data didokumentasikan.
- **Aktivitas Peserta**:
  - Menetapkan 4 grain analitis yang saling bebas (*orthogonal analytical grains*) untuk menghindari distorsi agregasi:
    1. `order_level`: Unit pesanan individual ($N=96,470$) untuk prediksi kepuasan dan keterlambatan.
    2. `customer_cohort`: Unit agregasi pelanggan unik ($N=93,358$) untuk analisis retensi dan LTV.
    3. `weekly_system_state`: Deret waktu sistem makro ($N=86$ minggu) untuk pemodelan dinamika ekosistem.
    4. `review_corpus`: Korpus teks ulasan pelanggan ($N=95,831$) untuk Bi-LSTM NLP.
  - Menetapkan ambang batas observasi *delta_w = 90 hari* untuk mitigasi bias *right-censoring* pada cohort pelanggan baru.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Logika seleksi objek di `src/csip/cleaning/cleaner.py` dan konfigurasi `config/data.yaml`.
  - **Result**: Empat dataset terstruktur dalam format Apache Parquet di `data/processed/` dan inventarisasi manifest `data/dataset_manifest.json`.
  - **Validation**: Verifikasi integritas skema dan independensi objek data dalam `tests/test_cleaning_and_grain.py`.
  - **Explanation**: Pemisahan grain mutlak diperlukan dalam e-commerce karena perilaku tingkat pesanan (misal: ongkir pesanan ini) tidak boleh dicampuradukkan dengan metrik agregat pelanggan (misal: total pengeluaran seumur hidup) yang rawan kebocoran data.
- **Lokasi Artefak**:
  - Code: `src/csip/cleaning/cleaner.py`, `config/data.yaml`
  - Notebook: `notebooks/02_data_validation_and_cleaning.ipynb`
  - Report: `data/dataset_manifest.json`, `reports/research_traceability_matrix.md`
  - Tests: `tests/test_cleaning_and_grain.py`
- **Metode Verifikasi**: Pengujian skema, jumlah baris, dan keunikan kunci primer pada setiap grain analitis.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-06] Membersihkan Data (`J.62DMI00.008.1`)
- **Deskripsi Unit**: Merencanakan pembersihan data (anomali, missing values, duplikasi, outlier) dan mengeksekusi prosedur pembersihan terprogram serta memverifikasi data bersih dalam format terstandar.
- **Elemen Kompetensi**:
  1. Merencanakan pembersihan data.
  2. Melakukan pembersihan data.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Anomali, missing values, duplikasi, dan inkonsistensi data diidentifikasi.
  - **1.2**: Strategi dan metode pembersihan data (imputasi, deduplikasi, penanganan outlier) dirancang.
  - **2.1**: Prosedur pembersihan data dieksekusi secara terprogram.
  - **2.2**: Data bersih hasil pembersihan diverifikasi integritasnya dan disimpan dalam format terstandar.
- **Aktivitas Peserta**:
  - Merancang dan mengeksekusi pipeline pembersihan:
    1. Filter status pesanan: hanya mempertahankan `order_status == 'delivered'`.
    2. Deduplikasi geolokasi: memampatkan 1,000,163 baris koordinat mentah menjadi 19,010 titik median per prefix kode pos (-98.1% reduksi baris).
    3. Deduplikasi ulasan: menggabungkan ulasan multi-item per pesanan agar tidak terjadi duplikasi observasi ulasan.
    4. Penerapan protokol *Scikit-Learn Transformer* (`AutoDataCleaner`: `fit`, `transform`, `fit_transform`) untuk menjamin transformasi bersih bebas kebocoran.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Implementasi `src/csip/cleaning/cleaner.py` dan `src/csip/cleaning/auto_cleaner.py`.
  - **Result**: 8 tabel interim bersih disimpan dalam format Parquet di `data/interim/`.
  - **Validation**: 100% lolos pada pengujian deduplikasi, imputasi, dan stress test ekstrem (`tests/test_cleaning_and_grain.py`, `tests/test_data_pipeline_stress.py`).
  - **Explanation**: Agregasi median koordinat dipilih karena koordinat GPS pada zip code yang sama sering mengalami fluktuasi pengukuran acak; deduplikasi ini mengeliminasi *cartesian explosion* saat melakukan *spatial join*.
- **Lokasi Artefak**:
  - Code: `src/csip/cleaning/cleaner.py`, `src/csip/cleaning/auto_cleaner.py`
  - Notebook: `notebooks/02_data_validation_and_cleaning.ipynb`
  - Report: `reports/data_quality_report.md`
  - Tests: `tests/test_cleaning_and_grain.py`, `tests/test_data_pipeline_stress.py`
- **Metode Verifikasi**: Audit integritas baris sebelum vs sesudah pembersihan serta eksekusi stress test suite.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-07] Mengkonstruksi Data (`J.62DMI00.009.1`)
- **Deskripsi Unit**: Menganalisis teknik transformasi data, merancang dan melakukan rekayasa fitur (*feature engineering*), serta membuat dokumentasi konstruksi data bebas kebocoran target.
- **Elemen Kompetensi**:
  1. Menganalisis teknik transformasi data.
  2. Melakukan transformasi data.
  3. Membuat dokumentasi konstruksi data.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Representasi fitur data awal dianalisis.
  - **1.2**: Teknik rekayasa fitur (*feature engineering*) yang diperlukan ditentukan sesuai tujuan pemodelan.
  - **2.1**: Fitur turunan, interaksi, agregasi as-of, dan encoding variabel dibentuk tanpa data leakage.
  - **2.2**: Dataset hasil konstruksi siap pakai divalidasi spesifikasi teknisnya.
  - **3.1**: Setiap transformasi dan rancangan fitur didokumentasikan secara rinci.
- **Aktivitas Peserta**:
  - Merekayasa fitur domain e-commerce bernilai analitis tinggi:
    1. `freight_ratio`: Rasio biaya pengiriman terhadap harga barang ($\frac{\text{freight}}{\text{price}}$).
    2. `seller_buyer_distance_km`: Jarak geografis antarmuka pembeli-penjual menggunakan rumus Haversine tervarisasi.
    3. `approval_lag_hours`: Jeda waktu antara pesanan dibuat dengan konfirmasi pembayaran.
    4. `delivery_lead_time_days` & `delivery_delay_days`: Durasi aktual dan selisih terhadap estimasi tanggal tiba.
    5. `is_late` & `high_value_late_flag`: Fitur interaksi bernilai tinggi saat barang mahal terlambat.
  - Menegakkan prinsip *Temporal Anti-Leakage Isolation*: fitur pasca-pengiriman tidak diizinkan masuk ke model estimasi awal.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Mesin rekayasa fitur `src/csip/features/engineer.py` dan konfigurasi spesifikasi `config/features.yaml`.
  - **Result**: Dataset `data/processed/order_level.parquet` dengan 41 variabel terkonstruksi lengkap.
  - **Validation**: Pengujian kebocoran fitur otomatis dalam `tests/test_feature_leakage.py` membuktikan zero correlation dengan masa depan.
  - **Explanation**: Vectorized Haversine implementation diimplementasikan menggunakan NumPy trigonometri murni untuk memproses 100,000 baris dalam < 0.2 detik tanpa ketergantungan library geospasial berat.
- **Lokasi Artefak**:
  - Code: `src/csip/features/engineer.py`, `config/features.yaml`
  - Notebook: `notebooks/04_feature_engineering_and_construction.ipynb`
  - Report: `reports/feature_availability_and_leakage_audit.md`, `data/data_dictionary.md`
  - Tests: `tests/test_feature_leakage.py`
- **Metode Verifikasi**: Audit feature availability matrix dan eksekusi uji temporal anti-leakage.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-08] Membangun Skenario Model (`J.62DMI00.012.1`)
- **Deskripsi Unit**: Mengidentifikasi teknik pemodelan sesuai karakteristik data, merancang skenario pengujian hipotesis statistik, partisi validasi temporal, serta skenario intervensi sistem.
- **Elemen Kompetensi**:
  1. Mengidentifikasi teknik pemodelan.
  2. Menyiapkan skenario pengujian dan validasi model.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Karakteristik data dan asumsi teknis model diselaraskan.
  - **1.2**: Algoritma dan paradigma pemodelan (supervised, unsupervised, deep learning, state-space) dipilih sesuai KPI.
  - **2.1**: Skema partisi data (train/validation/test temporal holdout) dirancang untuk mencegah leakage.
  - **2.2**: Matriks eksperimen, skenario intervensi/kebijakan, dan protokol pengujian hipotesis ditetapkan.
- **Aktivitas Peserta**:
  - Merancang protokol pengujian hipotesis ilmiah H1 s.d. H6 dengan uji Falsifikasi dan koreksi Benjamini-Hochberg FDR ($\alpha = 0.05$).
  - Merancang skema validasi temporal out-of-time (OOT): Data sebelum `2018-06-01` sebagai Train set ($N=76,462$), data `2018-06-01` s.d. `2018-08-29` sebagai Test set holdout ($N=20,008$).
  - Merancang matriks eksperimen B0 s.d. B4 dan 6 skenario kebijakan operasional logistik (S0 s.d. S5).
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Modul hipotesis `src/csip/hypotheses/runner.py` dan simulator transisi `src/csip/world/state_transition.py`.
  - **Result**: Laporan hasil pengujian hipotesis `reports/hypothesis_report.md` dan matriks skenario `reports/scenario_simulation_report.md`.
  - **Validation**: H1 terbukti ($p < 0.001$, $\eta^2 = 0.12$), H2 terbukti ($p < 0.001$, cliff effect pada delay > 3 hari), H3 ditolak secara jujur ($p_{\text{adj}} = 0.859$, tercatat sebagai `FAIL-HYP-H3`).
  - **Explanation**: Partisi temporal holdout dipilih secara metodologis alih-alih k-fold cross-validation acak untuk mensimulasikan penerapan nyata di mana model harus memprediksi masa depan berdasarkan masa lalu tanpa bocoran informasi masa depan (*lookahead bias*).
- **Lokasi Artefak**:
  - Code: `src/csip/hypotheses/runner.py`, `src/csip/world/state_transition.py`, `config/scenarios.yaml`
  - Notebook: `notebooks/06_hypothesis_investigation.ipynb`, `notebooks/10_system_and_world_modeling.ipynb`
  - Report: `reports/hypothesis_report.md`, `reports/scenario_simulation_report.md`
  - Tests: `tests/test_hypotheses.py`, `tests/test_world_model.py`
- **Metode Verifikasi**: Verifikasi formula statistik inferensial, simulasi sensitivitas skenario, dan penegakan koreksi FDR.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-09] Membangun Model (`J.62DMI00.013.1`)
- **Deskripsi Unit**: Mempersiapkan data untuk pemodelan (fit preprocessing strictly on training data), melatih model baseline berjenjang (B0-B4), hyperparameter optimization, dan mencatat proses secara reproducible.
- **Elemen Kompetensi**:
  1. Mempersiapkan data untuk pemodelan.
  2. Melakukan pelatihan model.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Pipeline pelatihan dan preprocessing di-fit hanya pada data training.
  - **2.1**: Model baseline (B0-B1), model klasik (B2-B3), dan model tingkat lanjut (B4 deep learning) dilatih.
  - **2.2**: Hyperparameter dioptimalkan dan proses pelatihan dicatat secara reproducible.
- **Aktivitas Peserta**:
  - Mengeksekusi pelatihan berjenjang *Baseline Ladder*:
    - B0: Naive Majority Classifier (PR-AUC = 0.0814) & Mean Regressor.
    - B1: Logistic Regression & Ridge Regression.
    - B2: Decision Tree Classifier, KNN, Gaussian Naive Bayes.
    - B3: Random Forest & LightGBM Gradient Boosting.
    - B4: Tabular MLP dengan *Categorical Entity Embeddings* & Text Bi-LSTM NLP.
  - Menegakkan pemisahan ketat: Imputer dan Standard Scaler di-fit eksklusif pada $X_{\text{train}}$.
  - Menerapkan arsitektur PyTorch Bi-LSTM berbobot kelas (*pos_weight*) untuk ulasan teks.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Implementasi `src/csip/models/classic.py`, `trainer.py`, `deep_tabular.py`, `deep_seq.py`, dan `ml_engine.py`.
  - **Result**: Model terlatih tersimpan di `artifacts/models/`; LightGBM meraih Champion Tabular (PR-AUC = 0.3004), Bi-LSTM meraih Champion Teks (PR-AUC = 0.8076).
  - **Validation**: 100% reproducible dengan random seed tetap (`random_state=42`), dievaluasi dalam `tests/test_models.py` dan `tests/test_deep_learning.py`.
  - **Explanation**: LightGBM dipilih sebagai model produksi tabular karena ketahanannya terhadap outlier numerik, kemampuan menemukan interaksi non-linear secara otomatis, dan efisiensi memori di laptop 8GB RAM.
- **Lokasi Artefak**:
  - Code: `src/csip/models/`, `src/csip/models/ml_engine.py`
  - Notebook: `notebooks/07_supervised_ml_and_competency_lab.ipynb`, `notebooks/08_neural_network_and_deep_learning.ipynb`
  - Report: `reports/model_evaluation_and_review_report.md`
  - Tests: `tests/test_models.py`, `tests/test_deep_learning.py`
- **Metode Verifikasi**: Evaluasi skor loss konvergen, perbandingan kinerja bertingkat, dan pengujian inferensi out-of-sample.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-10] Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
- **Deskripsi Unit**: Menganalisis performa model menggunakan metrik evaluasi yang tepat, membandingkan dengan baseline, mengkalibrasi probabilitas, dan menginterpretasikan atribusi fitur menggunakan explainable AI.
- **Elemen Kompetensi**:
  1. Menganalisis performa model.
  2. Melakukan interpretasi model.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Metrik teknis (PR-AUC, ROC-AUC, Brier Score, ECE, MAE, R2, WAPE) dihitung pada test set holdout.
  - **1.2**: Baseline comparison dilakukan untuk membuktikan keunggulan model terpilih.
  - **2.1**: Kontribusi fitur diinterpretasikan menggunakan metode explainable AI (SHAP TreeExplainer).
  - **2.2**: Keterbatasan dan ketidakpastian prediksi diukur (bootstrap confidence interval).
- **Aktivitas Peserta**:
  - Mengevaluasi model pada dataset holdout temporal:
    - LightGBM melampaui Naive Classifier sebesar +269% (PR-AUC 0.3004 vs 0.0814).
    - Menerapkan *Platt Scaling Probability Calibration*: mereduksi Brier Score dari 0.1375 menjadi 0.0762 (-44.59%) dan memangkas Expected Calibration Error (ECE) dari 0.2355 menjadi 0.0070.
    - Menganalisis atribusi *SHAP TreeExplainer*: menemukan bahwa fitur keterlambatan (`delivery_delay_days`) menyumbang 31.2% dari total massa kepentingan model.
    - Menghitung interval ketidakpastian bootstrap 95% untuk estimasi skenario.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Pipeline evaluasi di `src/csip/evaluation/explainer.py` dan modul `src/csip/uncertainty/bootstrap.py`.
  - **Result**: Laporan evaluasi komprehensif `reports/model_evaluation_and_review_report.md` dan visualisasi SHAP summary plot.
  - **Validation**: Kurva kalibrasi probabilitas terbukti linear mendekati diagonal sempurna ($y=x$).
  - **Explanation**: Kalibrasi probabilitas adalah keharusan mutlak sebelum model digunakan untuk keputusan bisnis berbasis ambang batas (*threshold decisioning*), karena skor output model pohon yang tidak terkalibrasi tidak merepresentasikan frekuensi probabilitas kejadian sesungguhnya.
- **Lokasi Artefak**:
  - Code: `src/csip/evaluation/explainer.py`, `src/csip/uncertainty/bootstrap.py`
  - Notebook: `notebooks/09_model_evaluation_and_explainability.ipynb`, `notebooks/12_uncertainty_quantification.ipynb`
  - Report: `reports/model_evaluation_and_review_report.md`
  - Tests: `tests/test_models.py`, `tests/test_deep_learning.py`
- **Metode Verifikasi**: Perhitungan metrik evaluasi multivariat, audit kurva kalibrasi reliabilitas, dan verifikasi atribusi SHAP.
- **Status**: **VERIFIED (Grade A)**

---

### [UK-11] Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)
- **Deskripsi Unit**: Meninjau kesesuaian model terhadap tujuan bisnis, mendokumentasikan kegagalan dan batasan dalam Failure Register, menegakkan hierarki klaim ilmiah (L0-L3), serta merumuskan rekomendasi keputusan.
- **Elemen Kompetensi**:
  1. Meninjau kesesuaian model terhadap tujuan bisnis.
  2. Menentukan tindak lanjut dan rekomendasi.
- **Kriteria Unjuk Kerja (KUK)**:
  - **1.1**: Hasil pemodelan ditinjau ulang terhadap objektif bisnis dan kriteria kesuksesan awal.
  - **1.2**: Potensi risiko, failure modes, dan batasan operasional didokumentasikan dalam Failure Register.
  - **2.1**: Rekomendasi strategis dan batasan klaim (L0-L3) dirumuskan untuk pengguna akhir.
  - **2.2**: Keputusan kelayakan model dan arahan perbaikan jangka panjang ditetapkan.
- **Aktivitas Peserta**:
  - Melakukan review kritis terhadap keseluruhan siklus pemodelan:
    1. Mengelola **Evidence & Failure Register**: mencatat secara transparan 3 kegagalan empiris (`FAIL-HYP-H3`: hipotesis reputasi seller ditolak, `FAIL-MOD-RIDGE`: model linier gagal menangkap non-linearitas keterlambatan, `LIMIT-CAUSAL`: simulasi kebijakan adalah asosiasi berbasis observasi, bukan eksperimen intervensi acak murni).
    2. Menegakkan **Hierarki Klaim Ilmiah**: mengklasifikasikan setiap temuan ke dalam tingkat L0 (Deskriptif), L1 (Prediktif), L2 (Asosiasional), atau L3 (Kausalitas Bersyarat).
    3. Merumuskan rekomendasi bisnis: Menetapkan SLA batas aman pengiriman maksimal 3 hari sebelum efek tebing kepuasan pembeli anjlok.
    4. Menyusun aplikasi demonstrasi Streamlit (`app/streamlit_app.py`) dan laporan teknis komprehensif.
- **Bukti Kerja 4 Dimensi**:
  - **Process**: Sistem manajemen audit di `src/csip/evidence/registry.py` dan dashboard interaktif di `app/streamlit_app.py`.
  - **Result**: Laporan resmi kegagalan dan klaim ilmiah `reports/evidence_and_failure_register.md` serta *Data Scientist Technical Report*.
  - **Validation**: Verifikasi parity artefak di `tests/test_evidence_registry.py` dan consistency check di `tests/test_skkni_consistency.py`.
  - **Explanation**: Mendokumentasikan kegagalan dan batasan metodologis secara transparan adalah ciri utama integritas seorang Data Scientist profesional pada KKNI Level 7; korelasi tidak pernah diklaim sebagai kausalitas tanpa pembuktian rancangan eksperimen acak (*randomized trial*).
- **Lokasi Artefak**:
  - Code: `src/csip/evidence/registry.py`, `app/streamlit_app.py`
  - Notebook: `notebooks/13_model_review_and_failure_analysis.ipynb`, `notebooks/14_final_research_report.ipynb`
  - Report: `reports/evidence_and_failure_register.md`, `reports/csip_data_scientist_technical_report.md`
  - Tests: `tests/test_evidence_registry.py`, `tests/test_skkni_consistency.py`
- **Metode Verifikasi**: Audit independen kepatuhan bukti kerja, verifikasi Failure Register, dan pengujian konsistensi otomatis.
- **Status**: **VERIFIED (Grade A)**

---

## 4. Evidence Traceability & Verification Summary

| Unit ID | Kode Resmi | Process Evidence | Result Evidence | Validation Evidence | Explanation Evidence | Grade |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **UK-01** | `J.62DMI00.001.1` | `config/business_objectives.yaml` | 3 Pilar Bisnis Terukur | `simulator.py` Laba Rugi | Asosiasi Friksi Logistik | **Grade A** |
| **UK-02** | `J.62DMI00.002.1` | `config/models.yaml` | Matriks KPI (PR-AUC, WAPE) | Benchmark Naive Ladder | Alasan Pemilihan PR-AUC | **Grade A** |
| **UK-03** | `J.62DMI00.005.1` | `src/csip/data/loader.py` | Profiling 9 Tabel Relasional | 100% Integritas Foreign Key | Deteksi Bottleneck Rantai Nilai | **Grade A** |
| **UK-04** | `J.62DMI00.006.1` | `tests/test_data_validation.py` | Filter 23 Anomali Kronologi | Automated Test Pass 100% | Right-Censoring Mitigation | **Grade A** |
| **UK-05** | `J.62DMI00.007.1` | `src/csip/cleaning/cleaner.py` | 4 Grain Analitis Parquet | Uji Struktur & Skema Grain | Orthogonal Grain Rationale | **Grade A** |
| **UK-06** | `J.62DMI00.008.1` | `src/csip/cleaning/auto_cleaner.py` | -98.1% Reduksi Geolocation | `test_data_pipeline_stress.py` | Median Spatial Aggregation | **Grade A** |
| **UK-07** | `J.62DMI00.009.1` | `src/csip/features/engineer.py` | 41 Variabel Order-Level | `test_feature_leakage.py` | Vectorized Haversine Efficiency | **Grade A** |
| **UK-08** | `J.62DMI00.012.1` | `src/csip/hypotheses/runner.py` | H1-H6 FDR Benjamini-Hochberg | `test_hypotheses.py` | OOT Split vs K-Fold Bias | **Grade A** |
| **UK-09** | `J.62DMI00.013.1` | `src/csip/models/` | B0-B4 Ladder, Champion LightGBM | `test_models.py` | Model Selection & 8GB Limits | **Grade A** |
| **UK-10** | `J.62DMI00.014.1` | `src/csip/evaluation/explainer.py` | Platt Scaling -44.6% Brier | SHAP 31.2% Delay Dominance | Probability Calibration Imperative | **Grade A** |
| **UK-11** | `J.62DMI00.015.1` | `src/csip/evidence/registry.py` | Failure Register (3 Failures) | `test_skkni_consistency.py` | Transparansi & Korelasi vs Kausalitas | **Grade A** |

---

## 5. Automated Consistency Rule
Setiap artefak, notebook, dan laporan dalam repositori CSIP wajib mematuhi pemetaan kanonikal di atas. Inkonsistensi kode unit, judul unit, atau referensi file akan dideteksi dan digagalkan secara otomatis oleh automated test suite `tests/test_skkni_consistency.py`.

