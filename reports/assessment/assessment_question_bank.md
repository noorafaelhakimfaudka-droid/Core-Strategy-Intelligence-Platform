# CSIP Comprehensive Assessment Question Bank & Technical Defense Guide
## Skema Sertifikasi Okupasi Ilmuwan Data — LSP TRI (SKM/2905/LSP-TRI/VII/2025)
### Standar: SKKNI No. 299 Tahun 2020 | Jenjang: KKNI Level 7

**Document ID**: `CSIP-QBANK-2026`  
**Execution Date**: 2026-11-11  
**Scope**: 11 Unit Kompetensi SKKNI No. 299/2020  
**Target Pengguna**: Asesi / Calon Peserta Sertifikasi Data Scientist  
**Status**: VERIFIED & READY FOR DEFENSE  

---

## 1. Executive Defense Strategy

Dokumen ini merupakan bank pertanyaan teknis komprehensif yang dirancang untuk mempersiapkan peserta dalam menghadapi uji lisan dan demonstrasi portofolio di hadapan dewan asesor **LSP TRI / BNSP**.

Setiap unit memuat:
1. Kode & Judul Resmi Unit SKKNI 299/2020.
2. Elemen Kompetensi & KUK Kunci.
3. Pertanyaan Inti Asesor.
4. Jawaban Berbasis Implementasi Aktual CSIP.
5. Pertanyaan Lanjutan (*Probe Questions*).
6. Jebakan Konseptual (*Common Pitfalls*) yang Wajib Dihindari.
7. Demonstrasi Langsung yang Dapat Ditunjukkan Peserta.

---

## 2. Granular Question Bank (11 Unit Kompetensi)

### Unit 1: `J.62DMI00.001.1` — Menentukan Objektif Bisnis
- **Pertanyaan Asesor**: *"Bagaimana Anda mengidentifikasi masalah bisnis utama pada proyek ini dan apa tolok ukur finansialnya?"*
- **Jawaban Berbasis CSIP**:
  > *"Pada e-commerce Olist, masalah bisnis utamanya adalah 97% pelanggan tidak pernah kembali belanja (churn tinggi) dan ongkos kirim menyumbang rata-rata 21.4% pengeluaran pembeli. Kami merumuskan 3 pilar: (1) Penurunan keterlambatan >3 hari sebesar 25%, (2) Reduksi komplain ulasan bintang 1 sebesar 15%, dan (3) Efisiensi subsidi logistik rute jauh. Nilai finansialnya dimodelkan di `src/csip/scenarios/simulator.py` di mana setiap penurunan 1 hari keterlambatan menghemat margin churn pembeli sebesar 3.8%."*
- **Pertanyaan Lanjutan**: *"Bagaimana Anda tahu bahwa komplain berasal dari masalah pengiriman?"*
- **Jawaban**: *"Analisis bivariat di EDA membuktikan 78.4% kata kunci pada ulasan bintang 1 berkaitan dengan kata 'atraso' (terlambat), 'chegou' (tiba), dan 'prazo' (tenggat waktu)."*
- **Jebakan Konseptual**: Menjawab secara generik 'ingin menaikkan keuntungan' tanpa angka dasar atau tanpa mengaitkannya dengan masalah logistik.
- **Demonstrasi**: Buka `config/business_objectives.yaml` dan jalankan modul `src/csip/scenarios/simulator.py`.

---

### Unit 2: `J.62DMI00.002.1` — Menentukan Tujuan Teknis Data Science
- **Pertanyaan Asesor**: *"Mengapa Anda memilih metrik PR-AUC daripada ROC-AUC untuk model klasifikasi risiko ulasan?"*
- **Jawaban Berbasis CSIP**:
  > *"Karena distribusi kelas ulasan negatif sangat timpang (extreme class imbalance, hanya ~8.1% populasi). Pada kasus ketimpangan kelas, ROC-AUC memberikan ilusi optimisme karena False Positive Rate diredam oleh besarnya jumlah True Negatives di penyebut. PR-AUC secara spesifik mengukur Precision terhadap Recall pada kelas minoritas. Kriteria keberhasilan kami tetapkan PR-AUC >= 0.28, dan LightGBM kami mencapai 0.3004 (+269% di atas baseline naive 0.0814)."*
- **Pertanyaan Lanjutan**: *"Berapa kriteria keberhasilan untuk World Model makro dan regresi waktu tiba?"*
- **Jawaban**: *"Regresi lead time memiliki KPI MAE <= 3.5 hari; World Model State-Space memiliki KPI WAPE <= 18% (tercapai 15.83% vs baseline naive 22.41%)."*
- **Jebakan Konseptual**: Membanggakan akurasi 92% padahal model hanya menebak kelas mayoritas.
- **Demonstrasi**: Tunjukkan perbandingan metrik di `config/models.yaml` dan kurva Precision-Recall di halaman 5 Streamlit.

---

### Unit 3: `J.62DMI00.005.1` — Menelaah Data
- **Pertanyaan Asesor**: *"Bagaimana Anda menelaah integritas data dari 9 tabel relasional yang disediakan?"*
- **Jawaban Berbasis CSIP**:
  > *"Saya menggunakan modul `src/csip/data/loader.py` untuk mengaudit skema relasional 9 tabel Olist. Kami membuktikan bahwa integritas referensial Foreign Key bernilai 100% tanpa ada record yatim piatu (0 orphan records). Kami menemukan heavy-tailed distribution pada harga dan ongkir, serta fenomena DISC-02: ulasan bintang 1 melonjak dari 4.2% pada pengiriman tepat waktu menjadi 43.8% saat keterlambatan melebihi 3 hari."*
- **Pertanyaan Lanjutan**: *"Bagaimana distribusi ulasan bintang 5?"*
- **Jawaban**: *"Ulasan bintang 5 mencakup 57% populasi, namun kepuasan tidak melonjak drastis jika barang datang lebih cepat (asimetri loss aversion)."*
- **Jebakan Konseptual**: Hanya melakukan `df.describe()` tanpa memeriksa relasi antar-tabel dan implikasi bisnis dari bentuk distribusi.
- **Demonstrasi**: Tunjukkan visualisasi distribusi di `notebooks/03_exploratory_data_analysis.ipynb`.

---

### Unit 4: `J.62DMI00.006.1` — Memvalidasi Data
- **Pertanyaan Asesor**: *"Apakah Anda menemukan anomali pada stempel waktu? Apa rekomendasi mitigasi yang Anda ambil?"*
- **Jawaban Berbasis CSIP**:
  > *"Ya, audit otomatis menemukan 23 baris anomali kronologis di mana tanggal kedatangan dicatat sebelum tanggal pembelian (order_delivered < order_purchase). Rekomendasi saya adalah membuang 23 baris tersebut karena melanggar logika kronologis waktu dan jumlahnya sangat kecil (<0.02%). Kami juga merekomendasikan pemfilteran transaksi berstatus non-delivered untuk menghindari bias sensor (right-censoring). Aturan ini diuji di `tests/test_data_validation.py`."*
- **Pertanyaan Lanjutan**: *"Mengapa tidak mengisi data tanggal tersebut dengan rata-rata?"*
- **Jawaban**: *"Imputasi tanggal kejadian yang tidak logis akan menyuntikkan noise palsu pada variabel target durasi kirim."*
- **Jebakan Konseptual**: Membiarkan data yang melanggar urutan kronologis tetap masuk ke dalam pelatihan.
- **Demonstrasi**: Buka `artifacts/reports/raw_data_profile.json` dan jalankan `pytest tests/test_data_validation.py`.

---

### Unit 5: `J.62DMI00.007.1` — Menentukan Objek Data
- **Pertanyaan Asesor**: *"Mengapa Anda memisahkan data menjadi 4 grain analitik terpisah?"*
- **Jawaban Berbasis CSIP**:
  > *"Untuk menjaga ortogonalitas unit observasi dan menghindari agregasi prematur yang membocorkan data. Keempat grain adalah: (1) `order_level` (N=96,470) untuk transaksi individu, (2) `customer_cohort` (N=93,358) untuk analisis retensi pelanggan dengan batas censoring 90 hari, (3) `weekly_system_state` (N=86) untuk deret waktu makro, dan (4) `review_corpus` (N=95,831) untuk pemrosesan teks NLP."*
- **Pertanyaan Lanjutan**: *"Format file apa yang digunakan untuk menyimpan keempat grain tersebut?"*
- **Jawaban**: *"Format Apache Parquet terkompresi Snappy di folder `data/processed/`, yang hemat memori dan cepat dibaca di laptop 8GB RAM."*
- **Jebakan Konseptual**: Mencampuradukkan data tingkat transaksi pesanan dengan metrik total seumur hidup pelanggan dalam satu tabel datar (*flat table*).
- **Demonstrasi**: Tunjukkan 4 file di `data/processed/` dan jalankan `pytest tests/test_cleaning_and_grain.py`.

---

### Unit 6: `J.62DMI00.008.1` — Membersihkan Data
- **Pertanyaan Asesor**: *"Bagaimana Anda membersihkan tabel geolokasi yang memiliki lebih dari 1 juta baris?"*
- **Jawaban Berbasis CSIP**:
  > *"Tabel mentah `geolocation` memiliki 1,000,163 baris koordinat GPS berulang per kode pos. Jika di-join langsung, terjadi ledakan kartesian yang menyebabkan crash Out-Of-Memory. Saya merancang reduksi koordinat spasial median per 5 digit prefix kode pos. Langkah ini memangkas 1.0M baris menjadi 19,010 titik koordinat unik (-98.1% reduksi volume data) dengan waktu join < 0.2 detik tanpa kehilangan presisi wilayah. Kelas `AutoDataCleaner` juga mematuhi protokol Scikit-Learn transformer (`fit`, `transform`)."*
- **Pertanyaan Lanjutan**: *"Mengapa menggunakan median bukan rata-rata?"*
- **Jawaban**: *"Median kebal terhadap outlier titik koordinat yang melenceng akibat kesalahan pembacaan GPS kurir."*
- **Jebakan Konseptual**: Melakukan join langsung pada 1 juta baris mentah atau melakukan data cleaning yang tidak mematuhi protokol Scikit-Learn.
- **Demonstrasi**: Tunjukkan kode di `src/csip/cleaning/auto_cleaner.py` dan jalankan `pytest tests/test_data_pipeline_stress.py`.

---

### Unit 7: `J.62DMI00.009.1` — Mengkonstruksi Data
- **Pertanyaan Asesor**: *"Bagaimana Anda membuktikan bahwa rekayasa fitur Anda tidak mengalami kebocoran target (target leakage)?"*
- **Jawaban Berbasis CSIP**:
  > *"Kami menyusun Feature Availability Matrix yang ketat. Pada saat memprediksi risiko di fase pemesanan (T0/T1), fitur yang diizinkan hanya: harga, ongkir, rasio ongkir, jarak Haversine, kategori, dan jeda approval. Variabel pasca-pengiriman seperti durasi pengiriman aktual, keterlambatan hari, dan teks ulasan diblokir total dari matriks masukan X. Pencegahan ini diuji di `tests/test_feature_leakage.py` yang membuktikan korelasi fitur input terhadap masa depan adalah 0.00."*
- **Pertanyaan Lanjutan**: *"Bagaimana Anda menghitung jarak penjual-pembeli secara efisien?"*
- **Jawaban**: *"Menggunakan formula trigonometri Haversine yang divektorisasi murni dengan array NumPy di `src/csip/features/engineer.py` (selesai dalam 0.18 detik untuk 100k baris)."*
- **Jebakan Konseptual**: Memasukkan `delivery_delay_days` sebagai prediktor untuk memprediksi `is_late` (*tautology leakage*).
- **Demonstrasi**: Buka `reports/modeling/feature_availability_matrix.csv` dan jalankan `pytest tests/test_feature_leakage.py`.

---

### Unit 8: `J.62DMI00.012.1` — Membangun Skenario Model
- **Pertanyaan Asesor**: *"Mengapa Anda menolak hipotesis H3 (Seller Rating Premium) dalam Failure Register?"*
- **Jawaban Berbasis CSIP**:
  > *"Dalam pengujian hipotesis H3, p-value mentah adalah 0.142. Setelah diterapkan koreksi Benjamini-Hochberg False Discovery Rate (FDR) alpha=0.05 pada keluarga hipotesis H1-H6, nilai p-adjusted menjadi 0.859 dengan ukuran efek d=0.012 (dapat diabaikan). Saya secara terbuka mencatat penolakan ini dalam Failure Register (`FAIL-HYP-H3`). Mengubah hipotesis atau p-hacking demi hasil signifikan adalah pelanggaran etika ilmiah. Temuan ini membuktikan pembeli Olist lebih peduli pada ongkir dan harga dibanding reputasi masa lalu toko."*
- **Pertanyaan Lanjutan**: *"Bagaimana skema pembagian data train dan test Anda?"*
- **Jawaban**: *"Menggunakan Temporal Out-of-Time split dengan cutoff 1 Juni 2018 (Train N=76,462, Test N=20,008) guna merefleksikan kondisi produksi tanpa lookahead bias."*
- **Jebakan Konseptual**: Menyembunyikan hipotesis yang gagal atau memanipulasi p-value.
- **Demonstrasi**: Buka `reports/evidence_and_failure_register.md` dan jalankan `pytest tests/test_hypotheses.py`.

---

### Unit 9: `J.62DMI00.013.1` — Membangun Model
- **Pertanyaan Asesor**: *"Jelaskan filosofi Baseline Ladder dan mengapa LightGBM dipilih sebagai model champion tabular!"*
- **Jawaban Berbasis CSIP**:
  > *"Kami menerapkan Baseline Ladder bertingkat: B0 Naive (PR-AUC 0.0814), B1 Logistic (0.1642), B2 Decision Tree (0.2185), B3 Random Forest (0.2842), dan B3 Champion LightGBM (0.3004). LightGBM dipilih karena: (1) Meraih PR-AUC tertinggi di holdout test set (+269% vs naive), (2) Mampu menangani fitur continuous non-linear dan rasio interaksi secara otomatis, dan (3) Waktu inferensinya sangat cepat (<5ms per batch) dengan konsumsi memori hemat di laptop 8GB RAM. Kami juga melatih Text Bi-LSTM untuk ulasan teks yang meraih PR-AUC 0.8076."*
- **Pertanyaan Lanjutan**: *"Bagaimana Anda menjamin reproducibility pelatihan model?"*
- **Jawaban**: *"Semua random seed dikunci (`random_state=42`) di NumPy, Scikit-Learn, LightGBM, dan PyTorch, serta artefak model diserialisasi di `artifacts/models/`."*
- **Jebakan Konseptual**: Langsung melatih model kompleks tanpa membuktikan peningkatannya terhadap model baseline sederhana.
- **Demonstrasi**: Tunjukkan model file di `artifacts/models/` dan jalankan `pytest tests/test_models.py`.

---

### Unit 10: `J.62DMI00.014.1` — Mengevaluasi Hasil Pemodelan
- **Pertanyaan Asesor**: *"Mengapa kalibrasi probabilitas Platt Scaling wajib dilakukan sebelum skor model digunakan untuk keputusan bisnis?"*
- **Jawaban Berbasis CSIP**:
  > *"Model pohon ensemble seperti LightGBM menghasilkan skor probabilitas mentah yang terdistorsi dan overconfident pada data dengan ketimpangan kelas. Jika tim bisnis menggunakan threshold biaya untuk intervensi voucher, probabilitas yang melenceng akan menyebabkan pemborosan anggaran. Dengan Platt Scaling:
  > - Brier Score berhasil dipangkas sebesar 44.59% (dari 0.1375 menjadi 0.0762).
  > - Expected Calibration Error (ECE) merosot dari 0.2355 menjadi 0.0070 (-97%).
  > Selain itu, analisis SHAP TreeExplainer membuktikan keterlambatan pengiriman menyumbang 31.2% dari total bobot keputusan model."*
- **Pertanyaan Lanjutan**: *"Bagaimana Anda mengukur ketidakpastian proyeksi skenario kebijakan?"*
- **Jawaban**: *"Menggunakan residual bootstrap resampling (B=1,000 iterasi) untuk menghasilkan rentang interval kepercayaan 95% CI pada setiap estimasi skenario."*
- **Jebakan Konseptual**: Menggunakan skor `predict_proba()` mentah tanpa kalibrasi reliabilitas.
- **Demonstrasi**: Tunjukkan plot kurva kalibrasi probabilitas dan SHAP summary di halaman 5 Streamlit.

---

### Unit 11: `J.62DMI00.015.1` — Melakukan Proses Review Pemodelan
- **Pertanyaan Asesor**: *"Bagaimana Anda membedakan korelasi observasional dengan intervensi kausal dalam rekomendasi bisnis yang Anda rumuskan?"*
- **Jawaban Berbasis CSIP**:
  > *"Ini adalah standar etika ilmiah tertinggi KKNI Level 7. Dataset Olist adalah data observasional retrospektif tanpa eksperimen acak terkontrol (A/B testing). Oleh karena itu, dalam Failure Register dan dashboard, saya secara tegas membatasi klaim pada Level L2 (Asosiasi Terkontrol) dan analisis sensitivitas skenario, BUKAN klaim kausalitas mutlak (Level L3). Kami menyatakan: 'Berdasarkan model observasional, pesanan dengan rasio ongkir tinggi memiliki asosiasi penurunan kepuasan sebesar X%'. Kami tidak pernah mengklaim bahwa memotong ongkir pasti menaikkan profit tanpa variabel perancu lain. Batasan ini dicatat di `LIMIT-CAUSAL`."*
- **Pertanyaan Lanjutan**: *"Apa rekomendasi konkrit yang Anda berikan kepada manajemen e-commerce Olist?"*
- **Jawaban**: *"Menetapkan batas kritis SLA logistik maksimal 3 hari sebelum rating anjlok, serta mentransformasikan diskon ongkir universal menjadi subsidi cerdas terfokus hanya pada barang murah rute antar-wilayah (Klaster 0), yang diproyeksikan menghemat 14.2% churn dengan anggaran 3.1x lebih efisien."*
- **Jebakan Konseptual**: Mengklaim bahwa korelasi statistik adalah bukti kausalitas sebab-akibat tanpa eksperimen acak.
- **Demonstrasi**: Buka `reports/evidence_and_failure_register.md` dan tampilkan halaman 8 Streamlit (Model Governance).

