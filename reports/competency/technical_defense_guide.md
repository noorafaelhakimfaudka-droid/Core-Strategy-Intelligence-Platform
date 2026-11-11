# CSIP SKKNI Assessment Defense Guide & Technical Question Bank
## Simulasi Uji Lisan & Pembelaan Teknis Asesmen Kompetensi Data Scientist (KKNI Level 7)

**Document ID**: `CSIP-GUIDE-DEFENSE-2026`  
**Standard**: SKKNI No. 299 Tahun 2020 Subbidang Data Science  
**Target Sertifikasi**: Data Scientist (KKNI Jenjang 7) — LSP / SKKNI  
**Prinsip Utama**: Seluruh jawaban harus didasarkan pada implementasi konkret, kalkulasi empiris, dan rekaman kode/data nyata di dalam repositori CSIP. Hindari jawaban hafalan teoritis generik.  
**Date**: November 2026  

---

## DAFTAR ISI SIMULASI 11 UNIT KOMPETENSI

1. [UK-01: Menentukan Objektif Bisnis (`J.62DMI00.001.1`)](#uk-01-menentukan-objektif-bisnis)
2. [UK-02: Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)](#uk-02-menentukan-tujuan-teknis-data-science)
3. [UK-03: Menelaah Data (`J.62DMI00.005.1`)](#uk-03-menelaah-data)
4. [UK-04: Memvalidasi Data (`J.62DMI00.006.1`)](#uk-04-memvalidasi-data)
5. [UK-05: Menentukan Objek Data (`J.62DMI00.007.1`)](#uk-05-menentukan-objek-data)
6. [UK-06: Membersihkan Data (`J.62DMI00.008.1`)](#uk-06-membersihkan-data)
7. [UK-07: Mengkonstruksi Data (`J.62DMI00.009.1`)](#uk-07-mengkonstruksi-data)
8. [UK-08: Membangun Skenario Model (`J.62DMI00.012.1`)](#uk-08-membangun-skenario-model)
9. [UK-09: Membangun Model (`J.62DMI00.013.1`)](#uk-09-membangun-model)
10. [UK-10: Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)](#uk-10-mengevaluasi-hasil-pemodelan)
11. [UK-11: Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)](#uk-11-melakukan-proses-review-pemodelan)

---

### UK-01: Menentukan Objektif Bisnis
- **Pertanyaan Asesor**: *"Bagaimana Anda merumuskan latar belakang bisnis dan menentukan metrik kesuksesan finansial dalam proyek ini?"*
- **Kompetensi yang Diuji**: Mengidentifikasi latar belakang bisnis, poin objektif, dan metrik kesuksesan terukur.
- **KUK Terkait**: KUK 1.1, 1.2, 1.3, 1.4 (`J.62DMI00.001.1`).
- **Bukti Empiris CSIP**: File `config/business_objectives.yaml`, `notebooks/01_business_and_data_understanding.ipynb`, dan modul simulasi laba rugi di `src/csip/scenarios/simulator.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Dalam proyek CSIP pada ekosistem e-commerce Olist Brasil, latar belakang bisnis dirumuskan berdasarkan temuan bahwa 97% pelanggan hanya bertransaksi satu kali (retensi sangat rendah) dan ongkos kirim menyumbang rata-rata 21.4% dari total pengeluaran pembeli. Kami merumuskan 3 pilar objektif bisnis yang terukur: (1) Menurunkan risiko ulasan negatif bintang 1-2 sebesar minimal 15%, (2) Memangkas pesanan yang terlambat lebih dari 3 hari sebesar 25%, dan (3) Mengoptimalkan subsidi ongkos kirim pada rute logistik bernilai tinggi agar margin platform tidak tergerus. Kesuksesan finansial dimodelkan melalui simulator laba rugi di mana setiap penurunan 1 hari keterlambatan diasosiasikan dengan penghematan churn sebesar 3.8%."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Mengapa tidak langsung fokus pada akuisisi pelanggan baru daripada menekan keterlambatan kirim?"*
- **Jawaban Lanjutan**: *"Karena biaya akuisisi (CAC) di Brasil sangat mahal akibat luas geografis; mempertahankan pelanggan yang sudah ada (retensi) melalui SLA logistik yang terpercaya memiliki ROI 4x lebih tinggi berdasarkan simulasi skenario kami."*
- **Kesalahan Konseptual yang Harus Dihindari**: Menjawab dengan target umum seperti 'meningkatkan profit' tanpa parameter angka atau tanpa menghubungkan friksi logistik dengan perilaku pembeli.

---

### UK-02: Menentukan Tujuan Teknis Data Science
- **Pertanyaan Asesor**: *"Mengapa Anda memilih metrik PR-AUC sebagai tolok ukur teknis utama untuk klasifikasi risiko ulasan, bukan Accuracy atau ROC-AUC?"*
- **Kompetensi yang Diuji**: Menerjemahkan kebutuhan bisnis ke dalam task teknis ML dan parameter kriteria kesuksesan yang tepat.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.002.1`).
- **Bukti Empiris CSIP**: `config/models.yaml`, `reports/model_evaluation_and_review_report.md`, `tests/test_initialization.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Tugas klasifikasi risiko kepuasan pelanggan pada dataset Olist memiliki ketimpangan kelas yang ekstrem: kelas ulasan negatif hanya mencakup sekitar 8.1% dari total populasi (~7,800 dari 96,470 transaksi). Jika kita menggunakan Accuracy, model bodoh yang selalu menebak ulasan positif akan mendapatkan akurasi 91.9%, padahal sama sekali tidak berguna. ROC-AUC juga memberikan ilusi optimisme karena False Positive Rate diredam oleh dominannya True Negatives di penyebut. Oleh karena itu, saya secara sadar menetapkan PR-AUC (Precision-Recall Area Under Curve) sebagai KPI utama. Kriteria kesuksesan teknis kami tetapkan PR-AUC >= 0.28 (di mana baseline tebakan acak adalah 0.0814). Model champion LightGBM kami berhasil mencapai PR-AUC 0.3004, melampaui baseline sebesar +269%."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Berapa kriteria kesuksesan untuk tugas regresi dan model dinamisnya?"*
- **Jawaban Lanjutan**: *"Untuk regresi lead time pengiriman, kami menetapkan batas MAE <= 3.5 hari; untuk segmentasi persona, Silhouette Score >= 0.35 (tercapai 0.3865); dan untuk World Model Vector AutoRegressive, WAPE <= 18% (tercapai 15.83%)."*
- **Kesalahan Konseptual yang Harus Dihindari**: Mengklaim akurasi 90% sebagai bukti keberhasilan pada dataset yang tidak seimbang (*imbalanced*).

---

### UK-03: Menelaah Data
- **Pertanyaan Asesor**: *"Bagaimana Anda memeriksa hubungan dan karakteristik statistik data dari 9 tabel relasional yang disediakan?"*
- **Kompetensi yang Diuji**: Profiling univariat, bivariat, integritas relasional data, dan formulasi hipotesis awal.
- **KUK Terkait**: KUK 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2 (`J.62DMI00.005.1`).
- **Bukti Empiris CSIP**: Modul `src/csip/data/loader.py`, `notebooks/03_exploratory_data_analysis.ipynb`, `reports/data_quality_report.md`.
- **Jawaban Berbasis Implementasi**:
  > *"Saya menelaah 9 tabel menggunakan audit skema relasional di `loader.py`. Pertama, saya memverifikasi integritas Foreign Key (FK) dan membuktikan bahwa 100% relasi kunci referensial valid tanpa ada record yatim piatu (0 orphan records). Kedua, saya melakukan profiling univariat dan bivariat: menemukan heavy-tailed distribution pada nilai barang dan ongkir (median R\$ 74.99 vs maksimum R\$ 6,735). Ketiga, saya mengidentifikasi pola perilaku kritis (DISC-02): ulasan bintang 1 melonjak drastis dari 4.2% saat pengiriman tepat waktu menjadi 43.8% saat keterlambatan melebihi 3 hari. Temuan ini menjadi dasar perumusan hipotesis H1 (elastisitas rasio ongkir) dan H2 (asimetri penalti keterlambatan)."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Apakah Anda menemukan korelasi linier yang kuat antara jarak geografis penjual-pembeli dengan rating ulasan?"*
- **Jawaban Lanjutan**: *"Tidak. Jarak fisik secara langsung memiliki korelasi Pearson yang rendah terhadap rating (r = -0.06), namun ketika jarak tersebut diterjemahkan menjadi durasi pengiriman aktual dan keterlambatan hari, barulah pengaruh non-linear terhadap rating muncul secara tajam."*
- **Kesalahan Konseptual yang Harus Dihindari**: Menilai korelasi hanya dengan Pearson correlation tanpa memeriksa non-linearitas atau skewness data.

---

### UK-04: Memvalidasi Data
- **Pertanyaan Asesor**: *"Apakah Anda menemukan anomali atau data kotor pada dataset Olist? Bagaimana Anda membuktikan bahwa data tersebut valid secara temporal?"*
- **Kompetensi yang Diuji**: Audit kelengkapan data, validasi kronologi temporal, dan deteksi anomali.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.006.1`).
- **Bukti Empiris CSIP**: `artifacts/reports/data_quality_report.md`, `reports/data_quality_report.md`, `tests/test_data_validation.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Ya, audit otomatis saya menemukan dua masalah struktural: Pertama, ditemukan 23 baris anomali kronologis di mana tanggal pengiriman sampai di pelanggan dicatat lebih awal daripada tanggal pembelian (order_delivered_customer_date < order_purchase_timestamp), kemungkinan akibat kesalahan input sistem logistik mitra. Kedua, terdapat lebih dari 11,000 transaksi berstatus 'shipped/canceled/unavailable' yang belum memiliki tanggal sampai. Sebagai keputusan metodologis, saya merekomendasikan dan mengeksekusi filter tegas: 23 baris anomali dibuang, dan pesanan yang belum terkirim dikeluarkan dari analisis lead time kedatangan untuk mencegah right-censoring bias. Validasi ini diuji dan lulus 100% pada suite automated tests `test_data_validation.py`."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Mengapa tidak melakukan imputasi saja pada 23 baris yang tanggalnya terbalik?"*
- **Jawaban Lanjutan**: *"Imputasi pada tanggal kejadian yang tidak logis berisiko menyuntikkan noise palsu ke dalam target keterlambatan; karena jumlahnya hanya 23 baris dari ~100k data (< 0.02%), menghapusnya jauh lebih aman dan tidak merusak distribusi populasi."*
- **Kesalahan Konseptual yang Harus Dihindari**: Mempertahankan data yang melanggar hukum kronologis waktu tanpa filter.

---

### UK-05: Menentukan Objek Data
- **Pertanyaan Asesor**: *"Mengapa Anda membagi dataset menjadi 4 grain analitik terpisah? Mengapa tidak menggabungkan semuanya dalam satu tabel besar?"*
- **Kompetensi yang Diuji**: Menentukan kriteria pemilihan objek data, unit analisis (grain), dan isolasi level agregasi.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.007.1`).
- **Bukti Empiris CSIP**: `data/processed/` (4 Parquet files), `data/dataset_manifest.json`, `tests/test_cleaning_and_grain.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Menggabungkan semua entitas ke dalam satu tabel datar (*flat table*) adalah kesalahan arsitektural fatal karena melanggar ortogonalitas unit analisis dan menimbulkan duplikasi data. Saya menetapkan 4 grain analitik terpisah:
  > 1. `order_level` (N=96,470): Unit pesanan transaksi individual untuk prediksi risiko kepuasan.
  > 2. `customer_cohort` (N=93,358): Unit pelanggan unik untuk analisis retensi dan LTV dengan batas observasi delta_w = 90 hari guna mencegah censoring.
  > 3. `weekly_system_state` (N=86 minggu): Deret waktu makro untuk Vector AutoRegressive World Model.
  > 4. `review_corpus` (N=95,831): Korpus teks khusus pemrosesan bahasa alami (NLP Bi-LSTM).
  > Pemisahan ini menjamin tidak terjadi kebocoran antar-tingkat transaksi dan komputasi memori tetap hemat di bawah batas 8 GB RAM."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Bagaimana Anda memastikan integritas keempat grain tersebut tidak saling bertabrakan?"*
- **Jawaban Lanjutan**: *"Integritas skema dan keunikan kunci primer pada masing-masing grain diverifikasi secara otomatis melalui `tests/test_cleaning_and_grain.py`."*
- **Kesalahan Konseptual yang Harus Dihindari**: Menggabungkan data tingkat item ke tingkat pelanggan secara langsung tanpa memikirkan grain transaksi.

---

### UK-06: Membersihkan Data
- **Pertanyaan Asesor**: *"Jelaskan langkah konkret pembersihan data yang Anda lakukan pada tabel koordinat geolokasi yang memiliki lebih dari 1 juta baris!"*
- **Kompetensi yang Diuji**: Perencanaan dan eksekusi pembersihan data, penanganan kardinalitas tinggi, dan deduplikasi spasial.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.008.1`).
- **Bukti Empiris CSIP**: `src/csip/cleaning/cleaner.py`, `src/csip/cleaning/auto_cleaner.py`, `tests/test_data_pipeline_stress.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Tabel mentah `geolocation` memiliki 1,000,163 baris koordinat GPS yang sangat berulang per kode pos akibat pencatatan berkali-kali oleh kurir. Jika tabel ini di-join langsung ke data pesanan, akan terjadi ledakan kartesian (*cartesian explosion*) yang menghabiskan memori RAM laptop dan menghasilkan jutaan baris duplikat. Saya merancang strategi reduksi kardinalitas geolokasi spasial: mengelompokkan data berdasarkan 5 digit prefix kode pos, lalu menghitung koordinat median (bukan rata-rata, agar kebal terhadap outlier titik koordinat yang melenceng). Langkah ini memangkas 1,000,163 baris menjadi tepat 19,010 titik koordinat unik (-98.1% reduksi volume data) dengan waktu join < 0.2 detik tanpa kehilangan presisi geografis wilayah."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Apakah cleaner Anda mematuhi protokol Scikit-Learn?"*
- **Jawaban Lanjutan**: *"Ya, kelas `AutoDataCleaner` telah direfaktor untuk mengimplementasikan antarmuka standar Scikit-Learn Transformer dengan method `fit`, `transform`, dan `fit_transform`, sehingga statistik pembersihan hanya dipelajari dari data training."*
- **Kesalahan Konseptual yang Harus Dihindari**: Melakukan join langsung pada tabel geolokasi mentah yang menyebabkan memori laptop crash (Out-Of-Memory).

---

### UK-07: Mengkonstruksi Data
- **Pertanyaan Asesor**: *"Bagaimana Anda menjamin bahwa fitur-fitur yang Anda rekayasa bebas dari Target Leakage saat memprediksi keterlambatan pengiriman?"*
- **Kompetensi yang Diuji**: Rekayasa fitur domain, interaksi non-linear, dan penegakan isolasi temporal anti-kebocoran.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2, 3.1 (`J.62DMI00.009.1`).
- **Bukti Empiris CSIP**: `src/csip/features/engineer.py`, `reports/feature_availability_and_leakage_audit.md`, `tests/test_feature_leakage.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Saya menyusun Feature Availability Matrix yang ketat berdasarkan garis waktu transaksi (T0 Pembelian, T1 Pembayaran, T2 Kurir, T3 Tiba di Pembeli, T4 Ulasan). Saat memprediksi risiko pesanan pada saat pembelian (T0/T1), fitur yang diizinkan HANYA yang sudah tersedia saat itu: harga produk, ongkos kirim, rasio ongkir, estimasi janji platform, jeda approval, dan jarak spasial Haversine penjual-pembeli. Fitur seperti tanggal kedatangan aktual (`order_delivered_customer_date`), keterlambatan aktual (`delivery_delay_days`), dan status keterlambatan (`is_late`) secara eksplisit DIKELUARKAN dari matriks fitur X. Pencegahan ini diuji secara terprogram di `test_feature_leakage.py` yang memverifikasi bahwa korelasi fitur input terhadap target masa depan adalah 0.00."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Bagaimana Anda menghitung jarak penjual-pembeli secara efisien untuk 100k transaksi?"*
- **Jawaban Lanjutan**: *"Saya menggunakan rumus trigonometri Haversine yang divektorisasi murni dengan array NumPy di `engineer.py`, sehingga kalkulasi 100,000 baris selesai dalam 0.18 detik tanpa library geospasial eksternal."*
- **Kesalahan Konseptual yang Harus Dihindari**: Menggunakan selisih tanggal pengiriman aktual sebagai fitur prediktor untuk memprediksi keterlambatan (*tautological target leakage*).

---

### UK-08: Membangun Skenario Model
- **Pertanyaan Asesor**: *"Mengapa Anda menolak hipotesis H3 (Seller Rating Premium) dalam Failure Register? Mengapa tidak mengubah parameter pengujian agar hasilnya signifikan?"*
- **Kompetensi yang Diuji**: Perancangan skenario pengujian hipotesis, koreksi False Discovery Rate, dan integritas etika ilmiah.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.012.1`).
- **Bukti Empiris CSIP**: `src/csip/hypotheses/runner.py`, `reports/hypothesis_report.md`, `reports/evidence_and_failure_register.md` (`FAIL-HYP-H3`).
- **Jawaban Berbasis Implementasi**:
  > *"Mengubah parameter atau melakukan p-hacking agar hasil menjadi signifikan adalah pelanggaran etika profesional paling berat dalam Data Science. Dalam pengujian hipotesis H3—yang menguji apakah reputasi historis penjual berpengaruh signifikan terhadap volume pesanan—hasil ANOVA bivariat menghasilkan p-value mentah 0.142. Setelah diterapkan koreksi Benjamini-Hochberg False Discovery Rate (FDR) alpha=0.05 pada seluruh keluarga hipotesis, nilai p-adjusted menjadi 0.859 dengan ukuran efek Cohen's d hanya 0.012 (dapat diabaikan). Ini adalah temuan ilmiah negatif yang valid: di marketplace Olist, pembeli bertransaksi berdasarkan kecocokan harga barang dan ongkir, bukan reputasi masa lalu toko. Saya secara terbuka mencatat penolakan ini dalam Failure Register (`FAIL-HYP-H3`) sebagai bukti objektivitas metodologis."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Bagaimana dengan skema validasi temporal Anda?"*
- **Jawaban Lanjutan**: *"Kami membagi data secara out-of-time (OOT) dengan cutoff 1 Juni 2018: 76,462 pesanan sebelum Juni 2018 sebagai Train set, dan 20,008 pesanan Juni-Agustus 2018 sebagai Test holdout set untuk mencegah lookahead bias."*
- **Kesalahan Konseptual yang Harus Dihindari**: Memanipulasi data atau menyembunyikan hipotesis yang tidak terbukti dari laporan asesmen.

---

### UK-09: Membangun Model
- **Pertanyaan Asesor**: *"Jelaskan filosofi Baseline Ladder yang Anda gunakan dan mengapa LightGBM terpilih sebagai champion model tabular!"*
- **Kompetensi yang Diuji**: Pelatihan model terstruktur (B0-B4), optimasi hyperparameter, dan pemilihan model berbasis bukti.
- **KUK Terkait**: KUK 1.1, 2.1, 2.2 (`J.62DMI00.013.1`).
- **Bukti Empiris CSIP**: `src/csip/models/classic.py`, `trainer.py`, `ml_engine.py`, `reports/model_evaluation_and_review_report.md`.
- **Jawaban Berbasis Implementasi**:
  > *"Kami menerapkan Baseline Ladder secara sistematis untuk membuktikan bahwa penambahan kompleksitas benar-benar memberikan nilai tambah:
  > - B0 Naive Majority Predictor: PR-AUC = 0.0814
  > - B1 Logistic Regression: PR-AUC = 0.1642 (+102%)
  > - B2 Decision Tree: PR-AUC = 0.2185 (+168%)
  > - B3 Random Forest: PR-AUC = 0.2842 (+249%)
  > - B3 Champion LightGBM: PR-AUC = 0.3004 (+269%)
  > - B4 Tabular MLP (Entity Embeddings): PR-AUC = 0.2915 (+258%)
  > LightGBM terpilih sebagai champion tabular karena: (1) Menghasilkan PR-AUC tertinggi di out-of-time test set, (2) Mampu menangani fitur non-linear dan rasio interaksi secara otomatis melalui histogram-based tree learning, dan (3) Waktu inferensinya sangat cepat (< 5 ms per batch) dengan penggunaan memori yang sangat hemat di laptop 8GB RAM."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Apakah Anda juga melatih model teks untuk review pelanggan?"*
- **Jawaban Lanjutan**: *"Ya, kami melatih model Bi-LSTM dengan embedding layer dan class weighting (pos_weight) pada korpus teks ulasan di `deep_seq.py`, yang mencapai PR-AUC 0.8076 untuk triage otomatis keluhan pelanggan."*
- **Kesalahan Konseptual yang Harus Dihindari**: Langsung melatih model kompleks tanpa membandingkannya dengan baseline linier atau naive predictor.

---

### UK-10: Mengevaluasi Hasil Pemodelan
- **Pertanyaan Asesor**: *"Mengapa kalibrasi probabilitas Platt Scaling sangat penting sebelum model digunakan untuk pengambilan keputusan bisnis?"*
- **Kompetensi yang Diuji**: Evaluasi diagnostik tingkat lanjut, kalibrasi probabilitas, dan explainable AI (SHAP).
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.014.1`).
- **Bukti Empiris CSIP**: `src/csip/evaluation/explainer.py`, `reports/model_evaluation_and_review_report.md`.
- **Jawaban Berbasis Implementasi**:
  > *"Model pohon ensemble seperti LightGBM cenderung menghasilkan skor probabilitas mentah yang tidak terkalibrasi (*overconfident* pada rentang ekstrem), terutama saat dilatih pada data dengan ketimpangan kelas tinggi. Jika tim operasional menggunakan threshold keputusan biaya (misal: hanya memberikan intervensi kompensasi voucher jika probabilitas komplain > 70%), estimasi probabilitas mentah yang melenceng akan menyebabkan pemborosan anggaran atau salah sasaran. Dengan menerapkan Platt Scaling (Logistic Sigmoidal Calibration):
  > - Brier Score berhasil dipangkas sebesar 44.59% (dari 0.1375 menjadi 0.0762).
  > - Expected Calibration Error (ECE) merosot dari 0.2355 menjadi 0.0070 (-97%).
  > Selain itu, analisis SHAP TreeExplainer membuktikan secara transparan bahwa keterlambatan durasi kirim menyumbang 31.2% dari total bobot keputusan model, memberikan landasan audit yang kuat bagi pemangku kepentingan."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Bagaimana Anda mengukur ketidakpastian estimasi pada skenario kebijakan?"*
- **Jawaban Lanjutan**: *"Kami menggunakan residual bootstrap resampling (B=1,000 iterasi) di `bootstrap.py` untuk menghasilkan rentang interval kepercayaan 95% Confidence Interval pada setiap proyeksi skenario."*
- **Kesalahan Konseptual yang Harus Dihindari**: Menganggap skor output `predict_proba()` dari model pohon ensemble sudah otomatis mencerminkan probabilitas kejadian yang sebenarnya.

---

### UK-11: Melakukan Proses Review Pemodelan
- **Pertanyaan Asesor**: *"Bagaimana Anda membedakan antara korelasi observasional dengan intervensi kausal dalam rekomendasi bisnis yang Anda sajikan?"*
- **Kompetensi yang Diuji**: Peninjauan kesesuaian model terhadap tujuan bisnis, transparansi Failure Register, hierarki klaim ilmiah, dan formulasi rekomendasi.
- **KUK Terkait**: KUK 1.1, 1.2, 2.1, 2.2 (`J.62DMI00.015.1`).
- **Bukti Empiris CSIP**: `src/csip/evidence/registry.py`, `reports/evidence_and_failure_register.md`, `app/streamlit_app.py`.
- **Jawaban Berbasis Implementasi**:
  > *"Ini adalah pilar integritas tertinggi pada jenjang KKNI Level 7. Dataset Olist adalah data observasional retrospektif tanpa eksperimen acak terkontrol (Randomized Controlled Trial / A/B Test). Oleh karena itu, dalam modul `EvidenceRegistry` dan dashboard Streamlit, saya secara tegas membatasi tingkat klaim hasil pemodelan pada Level L2 (Associational Claim) dan Analisis Sensitivitas Skenario Parametrik, BUKAN Level L3 (Causal Claim mutlak). Kami menyatakan bahwa: 'Berdasarkan model observasional terkontrol, pesanan dengan rasio ongkir tinggi memiliki asosiasi penurunan kepuasan sebesar X%'. Kami tidak pernah mengklaim bahwa 'Memotong ongkir pasti secara otomatis menaikkan profit sebesar Y% tanpa variabel perancu lain'. Batasan ini dicatat secara eksplisit dalam Failure Register (`LIMIT-CAUSAL`), sehingga manajemen platform memahami risiko dan asumsi di balik setiap simulasi kebijakan."*
- **Kemungkinan Pertanyaan Lanjutan**: *"Apa rekomendasi operasional konkrit yang Anda berikan kepada manajemen Olist?"*
- **Jawaban Lanjutan**: *"Menetapkan SLA logistik batas aman maksimal 3 hari keterlambatan sebelum rating anjlok, serta mengalihkan anggaran subsidi ongkos kirim universal menjadi subsidi cerdas terfokus hanya pada barang murah rute antarpulau (Klaster 0), yang diproyeksikan menghemat 14.2% churn dengan anggaran 3.1x lebih efisien."*
- **Kesalahan Konseptual yang Harus Dihindari**: Mengklaim bahwa regresi atau model machine learning membuktikan hubungan sebab-akibat (kausalitas) tanpa pembuktian desain kuasi-eksperimental atau uji acak.

