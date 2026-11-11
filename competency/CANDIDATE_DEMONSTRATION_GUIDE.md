# PANDUAN DEMONSTRASI PRAKTIK & WAWANCARA PESERTA ASESMEN
## Strategi Pembuktian Kompetensi Ilmuwan Data (Data Scientist) — KKNI Level 7
### Skema Sertifikasi: LSP TRI | Kode: SKM/2905/LSP-TRI/VII/2025 | SKKNI No. 299 Tahun 2020

---

## 1. Petunjuk Umum bagi Peserta Asesmen

Panduan ini disusun untuk mempersiapkan Anda dalam menjalani asesmen kompetensi SKKNI secara percaya diri, metodologis, dan berbasis bukti kerja nyata.

### Prinsip Utama Pembuktian Kompetensi:
1. **Bicara Berdasarkan Bukti**: Jangan sekadar menghafal teori. Tunjukkan file kode sumber, notebook tereksekusi, tabel evaluasi, atau test otomatis saat menjawab pertanyaan asesor.
2. **Jelaskan Rasional Keputusan**: Asesor tingkat KKNI Level 7 menilai bukan hanya *apa* yang Anda buat, tetapi *mengapa* keputusan teknis tersebut diambil (misalnya: mengapa memilih PR-AUC daripada ROC-AUC, mengapa menolak imputasi missing value ulasan, mengapa membatasi fitur di checkout).
3. **Akui Keterbatasan Secara Ilmiah**: Data Scientist profesional tidak mengklaim model sempurna. Mengakui keterbatasan data observasional, adanya bias survivor, dan hasil negatif hipotesis H3 menunjukkan integritas ilmiah yang tinggi.

---

## 2. Panduan Langkah Demi Langkah per Unit Kompetensi (11 Unit)

---

### UNIT 1: Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
- **Tujuan Kompetensi**: Mampu mengidentifikasi masalah bisnis, menentukan metrik keberhasilan, dan mengkaji kelayakan biaya-manfaat.
- **File Kunci yang Dibuka**:
  - `notebooks/01_business_and_data_understanding.ipynb`
  - `config/business.yaml`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan Section 1.1 pada notebook 01: Jelaskan bahwa 8,0% pesanan e-commerce Olist mengalami keterlambatan logistik, yang menyebabkan anjloknya rating ulasan dari 4,14 menjadi 2,15 (drop -48%).
  - Tunjukkan formula ROI dan perhitungan penghematan biaya mitigasi ~R$ 142.000 pada `config/business.yaml`.
- **Pertanyaan Asesor yang Sering Muncul**:
  > *"Bagaimana Anda memastikan objektif data science selaras dengan kebutuhan pemangku kepentingan?"*
- **Jawaban & Pertahanan Peserta**:
  > *"Saya mendefinisikan batas permasalahan bisnis secara kuantitatif melalui biaya keterlambatan dan risiko churn. Kami menghitung dampak keterlambatan terhadap rating dan biaya kompensasi tiket CS, lalu menetapkan target reduksi ulasan negatif sebesar 20% melalui intervensi checkout dini."*

---

### UNIT 2: Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
- **Tujuan Kompetensi**: Menerjemahkan objektif bisnis ke dalam formulasi pemodelan analitis dan metrik performa teknis.
- **File Kunci yang Dibuka**:
  - `docs/methodology/PREDICTION_CONTRACT.md`
  - `notebooks/01_business_and_data_understanding.ipynb` (Section 2)
- **Bagian yang Didemonstrasikan**:
  - Buka `docs/methodology/PREDICTION_CONTRACT.md`. Tunjukkan perumusan estimand matematis:
    $$\mathbb{P}(Y_{\text{negative}} = 1 \mid X_{t_0}, \text{Delivered} = 1)$$
  - Jelaskan mengapa metrik utama klasifikasi adalah **PR-AUC (Average Precision)** dan **Brier Score**, bukan sekadar akurasi (karena ketidakseimbangan kelas 12,8% ulasan negatif).
- **Pertanyaan Asesor**:
  > *"Mengapa Anda tidak menggunakan Accuracy atau ROC-AUC sebagai metrik utama pemilihan model?"*
- **Jawaban Peserta**:
  > *"Karena distribusi kelas sangat imbalanced (hanya ~12,8% ulasan negatif). Model naif mayoritas dapat meraih akurasi 87,2% tanpa memprediksi satupun ulasan negatif. Sementara ROC-AUC terdistorsi oleh tingginya True Negatives, sehingga PR-AUC dipilih sebagai ukuran presisi-recall yang objektif, dengan baseline naif sebesar prevalence positif (0,1096). Brier Score digunakan untuk mengukur keandalan kalibrasi probabilitas."*

---

### UNIT 3: Menelaah Data (`J.62DMI00.005.1`)
- **Tujuan Kompetensi**: Mampu memuat, mengidentifikasi struktur data relasional, dan melakukan profiling semantik.
- **File Kunci yang Dibuka**:
  - `src/csip/data/loader.py`
  - `notebooks/02_data_validation_and_cleaning.ipynb`
- **Bagian yang Didemonstrasikan**:
  - Jalankan inspeksi skema 9 tabel relasional. Tunjukkan verifikasi integritas Foreign Key pada `loader.py` yang memastikan 0 orphan records antara `orders`, `order_items`, `customers`, dan `payments`.
- **Pertanyaan Asesor**:
  > *"Bagaimana Anda memeriksa konsistensi relasi antar tabel data sebelum pemodelan?"*
- **Jawaban Peserta**:
  > *"Melalui modul `loader.py`, kami melakukan audit otomatis pada key relasional: memastikan `order_id` pada tabel items dan payments 100% cocok dengan tabel orders, serta memvalidasi kardinalitas one-to-many antara order dan item."*

---

### UNIT 4: Memvalidasi Data (`J.62DMI00.006.1`)
- **Tujuan Kompetensi**: Mampu mengidentifikasi anomali, ketidakkonsistenan waktu, dan missing values secara sistematis.
- **File Kunci yang Dibuka**:
  - `reports/data_quality_report.md`
  - `reports/audit/LABEL_OBSERVABILITY_AUDIT.csv`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan temuan 23 pesanan yang memiliki anomali kronologis di mana tanggal pengiriman tercatat mendahului tanggal pembelian ($t_{\text{del}} < t_{\text{pur}}$).
  - Tunjukkan penanganan 646 pesanan tanpa ulasan yang dipertahankan sebagai `NaN` (bukan diimputasi).
- **Pertanyaan Asesor**:
  > *"Mengapa 646 data tanpa ulasan tidak Anda isi dengan nilai rata-rata rating 3?"*
- **Jawaban Peserta**:
  > *"Mengisi ulasan kosong dengan nilai 3 (netral) atau menganggapnya puas merupakan kontaminasi label sintetis yang menurunkan reliabilitas ground-truth. Kami mempertahankan missing review sebagai NaN dan memfilternya saat supervised learning, sehingga distribusi label pelatihan 100% murni berasal dari feedback pelanggan nyata."*

---

### UNIT 5: Menentukan Objek Data (`J.62DMI00.007.1`)
- **Tujuan Kompetensi**: Menentukan unit observasi (*grain*), populasi target, dan skema tabel analitis.
- **File Kunci yang Dibuka**:
  - `src/csip/features/engineer.py`
  - `docs/methodology/PREDICTION_CONTRACT.md` (Section 6)
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan 4 objek data analitis yang dibangun: `order_level` (grain order), `customer_cohort` (grain pelanggan unik untuk retensi), `review_corpus` (grain teks ulasan), dan `weekly_system_state` (grain panel mingguan).
- **Pertanyaan Asesor**:
  > *"Bagaimana Anda menentukan grain objek data yang tepat untuk retensi pelanggan?"*
- **Jawaban Peserta**:
  > *"Untuk analisis kepuasan pesanan, grain-nya adalah `order_id`. Namun untuk memprediksi retensi repeat order 90 hari, grain harus diagregasi ke tingkat `customer_unique_id`. Kami hanya menggunakan fitur dari Order 1 (transaksi pertama) untuk memprediksi kemungkinan transaksi kedua dalam jendela 90 hari, serta memitigasi right-censoring pada pelanggan baru."*

---

### UNIT 6: Membersihkan Data (`J.62DMI00.008.1`)
- **Tujuan Kompetensi**: Menerapkan prosedur pembersihan, transformasi, dan deduplikasi tanpa kebocoran data.
- **File Kunci yang Dibuka**:
  - `src/csip/cleaning/cleaner.py`
  - `src/csip/cleaning/auto_cleaner.py`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan deduplikasi geolokasi pada `cleaner.py`: mengompresi 1.000.163 baris koordinat menjadi 19.015 zip code centroids unik (-98,1% reduksi baris).
  - Tunjukkan bahwa `auto_cleaner.py` mematuhi protokol transformer Scikit-Learn (`fit` pada train, `transform` pada test) untuk mencegah kebocoran statistik.
- **Pertanyaan Asesor**:
  > *"Bagaimana Anda memastikan proses pembersihan data tidak menyebabkan data leakage?"*
- **Jawaban Peserta**:
  > *"Seluruh parameter pembersihan—seperti nilai imputasi, statistik scaling, dan filter korelasi—hanya diestimasi (fit) pada data pelatihan (Train Split: Minggu 1–64). Parameter tersebut kemudian diterapkan secara pasif (transform) ke data validasi dan pengujian, menjamin isolasi temporal 100%."*

---

### UNIT 7: Mengkonstruksi Data (`J.62DMI00.009.1`)
- **Tujuan Kompetensi**: Merekayasa fitur prediktif, melakukan seleksi fitur, dan pengelompokan tanpa target leakage.
- **File Kunci yang Dibuka**:
  - `src/csip/features/engineer.py`
  - `reports/audit/FEATURE_AVAILABILITY_AUDIT.csv`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan rekayasa jarak Haversine tervektorisasi dan interaksi logistik `delay_x_freight_ratio`.
  - Buka `FEATURE_AVAILABILITY_AUDIT.csv` dan jelaskan keputusan V7: `approval_lag_hours` dikeluarkan dari fitur checkout `E1_early_warning_checkout` karena status approval belum terjadi saat checkout.
  - Tunjukkan perbaikan bug cohort: penggunaan `drop_duplicates(subset=['customer_unique_id'], keep='first')` alih-alih `groupby.first()` yang berisiko menarik kolom non-null dari order selanjutnya.
- **Pertanyaan Asesor**:
  > *"Mengapa `approval_lag_hours` dikeluarkan dari model checkout dini?"*
- **Jawaban Peserta**:
  > *"Karena pada saat pelanggan menekan tombol 'Place Order' ($t_0$), transaksi pembayaran baru diajukan dan belum di-approve oleh payment gateway. Rata-rata jeda approval kartu kredit adalah 10,2 jam, dan tiket boleto membutuhkan 24-48 jam. Memasukkan durasi approval pada waktu checkout melanggar prinsip point-in-time correctness."*

---

### UNIT 8: Membangun Skenario Model (`J.62DMI00.012.1`)
- **Tujuan Kompetensi**: Merancang skenario pemodelan terstruktur dan kriteria perbandingan kandidat algoritma.
- **File Kunci yang Dibuka**:
  - `src/csip/models/classic.py`
  - `docs/methodology/WORLD_MODEL_SPECIFICATION.md`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan rancangan Tangga Baseline (B0 Naive $\to$ B1 Linear/Ridge $\to$ B2 Pohon Tunggal/KNN $\to$ B3 Ensembles/LightGBM).
  - Tunjukkan skenario dynamic state transition Vector AutoRegressive (VAR) pada World Model untuk simulasi kebijakan makro.
- **Pertanyaan Asesor**:
  > *"Apa dasar Anda dalam memilih arsitektur Tangga Baseline B0 hingga B3?"*
- **Jawaban Peserta**:
  > *"Tangga Baseline memastikan bahwa kompleksitas model dijustifikasi oleh data. Model B0 menetapkan batas bawah terendah (naive baseline). Model B1 menguji keterpisahan linier. Model B2 menangkap hubungan non-linier sederhana. Model B3 (Gradient Boosting LightGBM) menangkap interaksi kompleks. Kami hanya mengadopsi model kompleks jika secara signifikan melampaui baseline sederhana pada PR-AUC dan Brier Score."*

---

### UNIT 9: Membangun Model (`J.62DMI00.013.1`)
- **Tujuan Kompetensi**: Melatih model machine learning, mengatur hiperparameter, dan memvalidasi partisi data.
- **File Kunci yang Dibuka**:
  - `src/csip/models/trainer.py`
  - `scripts/run_ml_experiments.py`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan partisi temporal waktu nyata:
    - Train: 64.156 pesanan (Minggu 1–64)
    - Validation: 19.684 pesanan (Minggu 65–78)
    - Test: 12.630 pesanan (Minggu 79–87)
  - Tunjukkan bahwa seluruh proses pelatihan menggunakan seed deterministik (`random_state=42`) dan menyimpan model ke `artifacts/models/`.
- **Pertanyaan Asesor**:
  > *"Mengapa Anda menggunakan pemisahan temporal daripada K-Fold Cross Validation acak?"*
- **Jawaban Peserta**:
  > *"Dalam data transaksi e-commerce, pola perilaku, inflasi harga, dan volume logistik bersifat sekuensial waktu. Random cross-validation akan mencampur data masa depan ke dalam data masa lalu (lookahead bias). Pemisahan kronologis ketat memastikan model diuji pada data masa depan yang belum pernah dilihat sama sekali, menyerupai kondisi operasional produksi."*

---

### UNIT 10: Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
- **Tujuan Kompetensi**: Mengevaluasi performa model, keandalan kalibrasi probabilitas, dan interpretasi fitur.
- **File Kunci yang Dibuka**:
  - `artifacts/reports/ml_leaderboard.json` / `ml_leaderboard.csv`
  - `reports/audit/WORLD_MODEL_AUDIT.md`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan hasil evaluasi Test Split: LightGBM meraih Champion PR-AUC **0,3061** (unggul +179% dari baseline naif 0,1096).
  - Tunjukkan kalibrasi Platt Scaling yang memangkas Brier Score sebesar -44,59%.
  - Tunjukkan out-of-sample backtesting World Model dengan WAPE ongkir 7,55% dan delay 19,80%.
- **Pertanyaan Asesor**:
  > *"PR-AUC Anda sebesar 0,3061. Apakah angka tersebut dapat dikategorikan bagus untuk kasus ini?"*
- **Jawaban Peserta**:
  > *"Sangat defensibel. Karena prevalensi dasar ulasan negatif pada split pengujian adalah 0,1096, PR-AUC sebesar 0,3061 berarti model memiliki daya diskriminasi hampir 3 kali lipat (lift ~2,8x) lebih presisi dibanding tebakan acak pada data tanpa kebocoran fitur pengiriman. Jika model memasukkan durasi pengiriman aktual (yang belum ada saat checkout), nilai PR-AUC akan melonjak ke 0,60+, tetapi itu adalah kebocoran data terlarang. Angka 0,3061 adalah performa murni berbasis informasi checkout dini."*

---

### UNIT 11: Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)
- **Tujuan Kompetensi**: Melakukan peninjauan menyeluruh terhadap kualitas model, mencatat kegagalan, dan menyusun mitigasi.
- **File Kunci yang Dibuka**:
  - `reports/model_evaluation_and_review_report.md`
  - `reports/evidence/evidence_and_failure_register.md`
  - `docs/limitations/KNOWN_LIMITATIONS.md`
- **Bagian yang Didemonstrasikan**:
  - Tunjukkan Failure Register: Dokumentasi penolakan hipotesis H3 (bahwa volume pesanan harian tidak berkorelasi linier dengan durasi delay, $p = 0,861$).
  - Tunjukkan pernyataan batasan non-kausal: Simulasi World Model adalah uji sensitivitas struktural, bukan inferensi kausal treatment effects eksperimen A/B.
- **Pertanyaan Asesor**:
  > *"Apa temuan kegagalan atau keterbatasan terbesar yang Anda temukan selama proses review model?"*
- **Jawaban Peserta**:
  > *"Tiga temuan utama: Pertama, kami mengidentifikasi potensi survivor bias karena data kepuasan hanya bersumber dari pesanan yang berstatus delivered, sedangkan 1.234 pesanan yang dibatalkan/stockout tidak terwakili. Kedua, hipotesis H3 ditolak secara empiris karena keterlambatan lebih dipengaruhi jarak geografis dan kapasitas kurir daripada lonjakan volume harian. Ketiga, kami mengungkapkan secara transparan bahwa simulasi intervensi kebijakan bersifat non-kausal dan memerlukan uji A/B sebelum implementasi skala penuh."*
