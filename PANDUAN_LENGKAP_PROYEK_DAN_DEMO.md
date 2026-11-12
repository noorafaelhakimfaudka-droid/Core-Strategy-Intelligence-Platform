# PANDUAN MASTER: PEMAHAMAN PROYEK CSIP, 11 UNIT KOMPETENSI SKKNI/BNSP, DAN STRATEGI DEMONSTRASI PRAKTIK

> **Dokumen Resmi Pembelajaran Mandiri & Persiapan Asesmen Sertifikasi**  
> **Skema**: Ilmuwan Data (Data Scientist) — KKNI Level 7  
> **Standar Rujukan**: SKKNI No. 299 Tahun 2020 | LSP TRI (Kode: `SKM/2905/LSP-TRI/VII/2025`)  
> **Platform**: *Core Strategy & Intelligence Platform (CSIP)* v1.0.0  
> **Penyusun Portofolio**: Noorafael Hakim Faudka  

---

## DAFTAR ISI
1. [BAB 1: APA SEBENARNYA PROYEK CSIP INI? (KONSEP, FILOSOFI & ARSITEKTUR)](#bab-1-apa-sebenarnya-proyek-csip-ini)
   - [1.1 Penjelasan dengan Bahasa Awam & Konsep Dasar](#11-penjelasan-dengan-bahasa-awam--konsep-dasar)
   - [1.2 Masalah Nyata yang Diselesaikan (Studi Kasus E-Commerce Olist)](#12-masalah-nyata-yang-diselesaikan-studi-kasus-e-commerce-olist)
   - [1.3 Cakupan Lintas Bidang (Universal Tabular X-Ray untuk CSV & Excel)](#13-cakupan-lintas-bidang-universal-tabular-x-ray-untuk-csv--excel)
   - [1.4 Arsitektur Antarmuka: Kokpit Single-Page CSIP Studio](#14-arsitektur-antarmuka-kokpit-single-page-csip-studio)
   - [1.5 Siapa Nara? Peran Agen Penasihat Strategis Cerdas](#15-siapa-nara-peran-agen-penasihat-strategis-cerdas)
2. [BAB 2: PETA LENGKAP 11 UNIT KOMPETENSI SKKNI 299 TAHUN 2020](#bab-2-peta-lengkap-11-unit-kompetensi-skkni-299-tahun-2020)
   - [Unit 1: Menentukan Objektif Bisnis (`J.62DMI00.001.1`)](#unit-1-menentukan-objektif-bisnis-j62dmi000011)
   - [Unit 2: Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)](#unit-2-menentukan-tujuan-teknis-data-science-j62dmi000021)
   - [Unit 3: Menelaah Data (`J.62DMI00.005.1`)](#unit-3-menelaah-data-j62dmi000051)
   - [Unit 4: Memvalidasi Data (`J.62DMI00.006.1`)](#unit-4-memvalidasi-data-j62dmi000061)
   - [Unit 5: Menentukan Objek Data (`J.62DMI00.007.1`)](#unit-5-menentukan-objek-data-j62dmi000071)
   - [Unit 6: Membersihkan Data (`J.62DMI00.008.1`)](#unit-6-membersihkan-data-j62dmi000081)
   - [Unit 7: Mengkonstruksi Data / Rekayasa Fitur (`J.62DMI00.009.1`)](#unit-7-mengkonstruksi-data--rekayasa-fitur-j62dmi000091)
   - [Unit 8: Membangun Skenario Model (`J.62DMI00.012.1`)](#unit-8-membangun-skenario-model-j62dmi000121)
   - [Unit 9: Membangun Model Machine Learning (`J.62DMI00.013.1`)](#unit-9-membangun-model-machine-learning-j62dmi000131)
   - [Unit 10: Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)](#unit-10-mengevaluasi-hasil-pemodelan-j62dmi000141)
   - [Unit 11: Melakukan Review Pemodelan (`J.62DMI00.015.1`)](#unit-11-melakukan-review-pemodelan-j62dmi000151)
3. [BAB 3: PANDUAN BELAJAR STEP-BY-STEP (DARI NOL HINGGA MAHIR)](#bab-3-panduan-belajar-step-by-step)
   - [Langkah 1: Menguasai Fondasi Bisnis & Data](#langkah-1-menguasai-fondasi-bisnis--data)
   - [Langkah 2: Memahami Proteksi Kebocoran Data (Anti-Leakage)](#langkah-2-memahami-proteksi-kebocoran-data-anti-leakage)
   - [Langkah 3: Memahami Pemodelan Mesin & Kalibrasi Probabilitas](#langkah-3-memahami-pemodelan-mesin--kalibrasi-probabilitas)
   - [Langkah 4: Memahami World Model & Simulasi Dinamika Sistem](#langkah-4-memahami-world-model--simulasi-dinamika-sistem)
   - [Langkah 5: Memahami Observatorium Drift & Stabilitas Kovariat](#langkah-5-memahami-observatorium-drift--stabilitas-kovariat)
4. [BAB 4: SKRIP DEMONSTRASI PRAKTIK DI DEPAN ASESOR / PENGUJI (15-20 MENIT)](#bab-4-skrip-demonstrasi-praktik)
   - [Fase 1: Pembukaan & Gambaran Eksekutif (2 Menit)](#fase-1-pembukaan--gambaran-eksekutif-2-menit)
   - [Fase 2: Demonstrasi Fleksibilitas Data & Profiling Semantik (3 Menit)](#fase-2-demonstrasi-fleksibilitas-data--profiling-semantik-3-menit)
   - [Fase 3: Pengujian Tuas Simulasi & Titik Kritis Bento Cards (4 Menit)](#fase-3-pengujian-tuas-simulasi--titik-kritis-bento-cards-4-menit)
   - [Fase 4: Eksplorasi 4 Lensa Analitik Interaktif (5 Menit)](#fase-4-eksplorasi-4-lensa-analitik-interaktif-5-menit)
   - [Fase 5: Menunjukkan Narasi Cerdas Penasihat Nara (3 Menit)](#fase-5-menunjukkan-narasi-cerdas-penasihat-nara-3-menit)
   - [Fase 6: Pembuktian Kualitas Kode, CI/CD & Audit KUK (3 Menit)](#fase-6-pembuktian-kualitas-kode-cicd--audit-kuk-3-menit)
5. [BAB 5: BANK TANYA-JAWAB UJI LISAN (ORAL DEFENSE) & JAWABAN EMAS](#bab-5-bank-tanya-jawab-uji-lisan-oral-defense)

---

## BAB 1: APA SEBENARNYA PROYEK CSIP INI?

### 1.1 Penjelasan dengan Bahasa Awam & Konsep Dasar
Bayangkan sebuah perusahaan ritel atau industri yang memiliki data operasional berukuran masif (ratusan ribu baris transaksi). Sering kali, para pimpinan bisnis bingung menjawab pertanyaan kritis seperti:
* *"Berapa kerugian kita jika jadwal kirim barang terlambat 3 hari?"*
* *"Faktor mana yang paling memicu kekecewaan pembeli atau ketidakpuasan pelanggan?"*
* *"Berapa batas aman toleransi biaya pengiriman sebelum rating ulasan anjlok?"*
* *"Apakah model machine learning kita masih akurat saat pola data masyarakat bergeser di lapangan?"*

**CSIP (*Core Strategy & Intelligence Platform*)** diciptakan untuk menjawab seluruh pertanyaan tersebut. CSIP bukan sekadar dashboard visual biasa, melainkan **Platform Analitik Keputusan Terintegrasi (*Decision Cockpit*)** yang menggabungkan:
1. **Machine Learning Terkalibrasi**: Memprediksi risiko dan perilaku secara saintifik.
2. **Simulator Intervensi Kebijakan (*Policy Simulator*)**: Memungkinkan pengguna menggeser "tuas" operasional untuk melihat simulasi dampak sebelum kebijakan sungguhan diterapkan di dunia nyata.
3. **Observatorium Pergeseran Data (*Concept Drift Observatory*)**: Mengaudit stabilitas statistik model secara real-time agar model tidak mengambil keputusan yang salah saat kondisi pasar berubah.
4. **Nara (Penasihat Strategi)**: Agen analitik cerdas yang menerjemahkan angka rumit menjadi arahan bisnis yang taktis, elegan, dan terukur.

---

### 1.2 Masalah Nyata yang Diselesaikan (Studi Kasus E-Commerce Olist)
Sebagai studi kasus *baseline* skala besar, CSIP membedah ekosistem e-commerce Brasil (Olist) yang mencakup:
* **~100.000 Transaksi Riil** dari 9 tabel basis data relasional.
* **Tantangan Utama**: Sekitar 8,0% pesanan mengalami keterlambatan logistik karena bentang geografis Brasil yang sangat luas.
* **Dampak Bisnis**: Saat pesanan datang terlambat, rating kepuasan pembeli anjlok dari rata-rata **4,14 menjadi 2,15 (-48%)**, yang memicu lonjakan ulasan negatif ekstrem sebesar **+381%** serta memicu klaim kompensasi tiket CS bernilai ratusan ribu Real Brasil.
* **Solusi CSIP**: Membangun model sistem peringatan dini (*Early Warning System*) sejak tombol checkout ditekan, sehingga tim logistik dapat mengambil tindakan pencegahan sebelum barang dikirim.

---

### 1.3 Cakupan Lintas Bidang (Universal Tabular X-Ray untuk CSV & Excel)
CSIP dirancang dengan prinsip **Universal Decision Intelligence Engine**. Artinya, platform ini **tidak terbatas** pada data e-commerce saja. CSIP dapat membaca sembarang berkas **CSV** maupun **Microsoft Excel (`.xlsx`, `.xls`)** yang memiliki variabel angka kontinu saling berkorelasi.

Sistem secara otomatis mendeteksi karakteristik semantik kolom ke dalam **8 Sektor Industri**:
1. **E-Commerce & Logistik**: Ongkir, harga barang, hari keterlambatan kirim, skor ulasan kepuasan.
2. **Kesehatan & Medis / Gaya Hidup**: BMI, gula darah, tekanan darah, kolesterol, progresi risiko keparahan penyakit.
3. **Mutu Produk & Manufaktur**: Komposisi kimia, flavonoid, kadar alkohol, getaran sensor mesin, tingkat cacat produk.
4. **Keuangan, Akuntansi & Pasar Modal**: Harga pasar, omzet penjualan, laba bersih, biaya operasional, bunga pinjaman.
5. **SDM & Manajemen Tenaga Kerja**: Jam kerja lembur, masa kerja, absensi, gaji, skor pencapaian KPI.
6. **Pemasaran Digital & Pertumbuhan**: Rasio klik (CTR), konversi (CVR), biaya akuisisi (CAC), churn rate, retensi pelanggan.
7. **Properti & Real Estate**: Harga rumah, luas bangunan, luas tanah, jarak fasilitas, usia bangunan.
8. **Edukasi & Akademik**: Jam belajar mandiri, presensi kehadiran, nilai ujian kelulusan, IPK.
9. **Sains & Eksperimen Terapan**: Analisis korelasi multivariat universal untuk sembarang data tabular angka.

---

### 1.4 Arsitektur Antarmuka: Kokpit Single-Page CSIP Studio
Aplikasi utama CSIP dijalankan melalui **CSIP Studio (`app/streamlit_app.py`)** yang menggunakan tata letak *Single-Page Editorial Cockpit* tanpa navigasi halaman berantakan:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ CSIP Studio • Core Strategy & Intelligence Platform (Ilmuwan Data Otomatis)     │
├──────────────────────────┬───────────────────────────────────────────────────────┤
│ PANEL KIRI (INPUT DATA)  │ PANGGUNG KANAN (ANALITIK & KEPUTUSAN)                 │
│                          │                                                       │
│ 1. Sumber Data & Fokus   │ 1. Kartu Bento Ringkasan:                             │
│    - Upload CSV / Excel  │    [ Estimasi Target ]  [ Faktor Terkuat ]  [ Selisih ]│
│    - Pilih Target        │                                                       │
│                          │ 2. Lensa Tampilan Interaktif (4 Tab):                 │
│ 2. Tuas Simulasi         │    Tab 1: Kurva Simulasi dan Titik Kritis             │
│    - Slider Faktor #1    │    Tab 2: Peringkat Faktor Penentu                    │
│    - Slider Faktor #2    │    Tab 3: Sebaran Kelompok Data (Ridgeline)           │
│    - Slider Faktor #3    │    Tab 4: Observatorium Drift & Stabilitas (Dual SVG) │
│                          │                                                       │
│                          │ 3. Kartu Penasihat Nara:                              │
│                          │    [Avatar Nara] Rekomendasi Preskriptif Terukur      │
│                          │    Pill Aksi #1  |  Pill Aksi #2                      │
└──────────────────────────┴───────────────────────────────────────────────────────┘
```

---

### 1.5 Siapa Nara? Peran Agen Penasihat Strategis Cerdas
**Nara** adalah personifikasi modul *Prescriptive Decision Intelligence* di dalam CSIP.
* Nara bertindak sebagai **Chief Strategy Advisor & Principal Data Scientist**.
* Nara tidak menggunakan template teks yang kaku atau kalimat hafalan mati.
* Nara secara dinamis menganalisis:
  - Posisi tuas input yang digeser pengguna.
  - Titik kritis (*tipping point*) kurva di mana respons mulai berubah tajam.
  - Polaritas target (membedakan apakah target harus ditekan rendah seperti risiko/biaya, atau didorong tinggi seperti laba/kepuasan).
  - Status kestabilan distribusi data operasional (PSI, Wasserstein distance, dan keselarasan kurva).
  - Memberikan 2 butir tindakan nyata (*Action Pills*) yang langsung bisa dieksekusi pemangku kepentingan.

---

## BAB 2: PETA LENGKAP 11 UNIT KOMPETENSI SKKNI 299 TAHUN 2020

Berikut adalah pemetaan mendalam terhadap seluruh 11 unit kompetensi resmi SKKNI No. 299 Tahun 2020 untuk skema **Ilmuwan Data (Data Scientist) KKNI Level 7**.

---

### UNIT 1: Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
* **Tujuan**: Mampu mengidentifikasi persoalan bisnis, memetakan kebutuhan pemangku kepentingan, dan merumuskan metrik keberhasilan kuantitatif.
* **Implementasi di CSIP**:
  - Mengkaji friksi rantai pasok Olist di mana 8,0% pesanan terlambat, menurunkan rating kepuasan dari 4,14 ke 2,15.
  - Merumuskan batas biaya operasional kompensasi pembeli pada [config/business.yaml](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/config/business.yaml) dengan potensi penghematan tahunan sebesar ~R$ 142.000.
* **Bukti Fisik & Kode Sumber**:
  - Notebook: [notebooks/01_business_and_data_understanding.ipynb](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/notebooks/01_business_and_data_understanding.ipynb) (Section 1.1)
  - Laporan: [reports/discovery_report.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/discovery_report.md)
* **Kunci Jawaban Ujian**:
  > *"Objektif bisnis kami tetapkan secara kuantitatif: mereduksi ulasan negatif sebesar 20% dan memangkas biaya friksi logistik sebesar R$ 142.000 melalui peringatan dini saat checkout."*

---

### UNIT 2: Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
* **Tujuan**: Menerjemahkan objektif bisnis ke dalam formulasi pemodelan teknis, menentukan tipe problem ML, dan memilih metrik evaluasi yang tepat.
* **Implementasi di CSIP**:
  - Merumuskan estimand matematis pada [docs/methodology/PREDICTION_CONTRACT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/methodology/PREDICTION_CONTRACT.md):
    $$\mathbb{P}(Y_{\text{negative}} = 1 \mid X_{t_0}, \text{Delivered} = 1)$$
  - Menolak metrik Accuracy dan ROC-AUC karena distribusi ulasan negatif timpang (*extreme class imbalance*, hanya ~10,9% ulasan negatif pada split test).
  - Menetapkan metrik teknis utama: **PR-AUC (Precision-Recall AUC / Average Precision)** dan **Brier Score** untuk kalibrasi probabilitas.
* **Bukti Fisik**:
  - Kontrak Prediksi: [docs/methodology/PREDICTION_CONTRACT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/methodology/PREDICTION_CONTRACT.md)
  - Laporan Metrik: [reports/methodology/CHECKOUT_RISK_FEASIBILITY.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/methodology/CHECKOUT_RISK_FEASIBILITY.md)
* **Kunci Jawaban Ujian**:
  > *"Pada data dengan ketimpangan kelas ekstrem, model naif yang selalu menebak kelas mayoritas bisa mendapatkan Akurasi 89%, padahal tidak berguna sama sekali. ROC-AUC pun memberikan ilusi optimisme karena besarnya True Negatives di penyebut. Oleh karena itu, kami mewajibkan PR-AUC sebagai tolok ukur ketepatan kelas minoritas, dengan target melampaui baseline naif 0,1096."*

---

### UNIT 3: Menelaah Data (`J.62DMI00.005.1`)
* **Tujuan**: Mengumpulkan data, memahami skema relasional, dan melakukan profiling semantik terhadap variabel.
* **Implementasi di CSIP**:
  - Mengintegrasikan 9 tabel relasional e-commerce Olist: `orders`, `order_items`, `order_payments`, `order_reviews`, `customers`, `sellers`, `products`, `geolocation`, `product_category_name_translation`.
  - Memverifikasi integritas kunci primer (*Primary Key*) dan kunci asing (*Foreign Key*) dengan memastikan **0 orphan records**.
* **Bukti Fisik**:
  - Modul Pemuat: [src/csip/data/loader.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/data/loader.py)
  - Semantic Profiler: [src/csip/data/semantic_profiler.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/data/semantic_profiler.py)
  - Notebook Profiling: [notebooks/02_data_validation_and_cleaning.ipynb](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/notebooks/02_data_validation_and_cleaning.ipynb)
* **Kunci Jawaban Ujian**:
  > *"Pemeriksaan struktur data dilakukan dengan memverifikasi kardinalitas 1-to-many antara pesanan dan barang belanjaan, serta memastikan integritas referensial 100% konsisten tanpa catatan yatim (zero orphan records)."*

---

### UNIT 4: Memvalidasi Data (`J.62DMI00.006.1`)
* **Tujuan**: Mengidentifikasi inkonsistensi kronologis, nilai anomali, outlier, dan missing values secara saintifik.
* **Implementasi di CSIP**:
  - Mendeteksi anomali kronologis: menemukan 23 pesanan di mana tanggal kirim tercatat lebih awal dari tanggal beli ($t_{\text{del}} < t_{\text{pur}}$).
  - Menangani 646 data tanpa ulasan (*missing reviews*): **tidak diimputasi rata-rata**, melainkan dipertahankan sebagai `NaN` untuk menjaga kemurnian label *ground truth*.
  - Mengidentifikasi batasan *survivor bias*: kepuasan hanya terobservasi pada pesanan berstatus *delivered*, sementara pesanan dibatalkan/hilang memiliki dinamika terpisah.
* **Bukti Fisik**:
  - Laporan Mutu Data: [reports/data_quality_report.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/data_quality_report.md)
  - Audit Observabilitas Label: [reports/audit/LABEL_OBSERVABILITY_AUDIT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/audit/LABEL_OBSERVABILITY_AUDIT.csv)
* **Kunci Jawaban Ujian**:
  > *"Mengisi ulasan kosong dengan nilai median rating 3 atau menganggapnya puas merupakan kontaminasi label sintetis terlarang. Data Scientist profesional memisahkan missing labels agar model dilatih murni dari umpan balik pelanggan nyata."*

---

### UNIT 5: Menentukan Objek Data (`J.62DMI00.007.1`)
* **Tujuan**: Menentukan unit analisis (*grain*) yang tepat untuk setiap tujuan permodelan bisnis.
* **Implementasi di CSIP**:
  - Membangun 4 objek data analitis terstandarisasi:
    1. `order_level` (Grain: `order_id`): Untuk estimasi ulasan negatif dan risiko logistik.
    2. `customer_cohort` (Grain: `customer_unique_id`): Untuk prediksi retensi pembelian berulang 90 hari (*repeat purchase*).
    3. `review_corpus` (Grain: `review_id`): Korpus teks ulasan multibahasa untuk NLP Bi-LSTM.
    4. `weekly_system_state` (Grain: minggu kalender): Panel agregat runtun waktu untuk World Model VAR.
* **Bukti Fisik**:
  - Modul Rekayasa: [src/csip/features/engineer.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/features/engineer.py)
  - Dokumentasi Objek Data: [reports/audit/project_inventory.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/audit/project_inventory.md)
* **Kunci Jawaban Ujian**:
  > *"Grain analisis harus disesuaikan dengan pertanyaan bisnis: untuk kepuasan transaksi kita memakai tingkat order_id, namun untuk retensi pelanggan kita wajib mengagregasi ke tingkat customer_unique_id dengan hanya mengambil fitur dari transaksi pertama (Order 1) agar tidak terjadi kontaminasi informasi masa depan."*

---

### UNIT 6: Membersihkan Data (`J.62DMI00.008.1`)
* **Tujuan**: Menghapus duplikasi, menormalisasi data, dan menerapkan transformasi data tanpa menyebabkan *data leakage*.
* **Implementasi di CSIP**:
  - Deduplikasi geolokasi: Mengompresi 1.000.163 baris koordinat geolokasi menjadi 19.015 titik tengah (*centroid*) zip code unik (-98,1% reduksi tanpa kehilangan presisi geografis).
  - Protokol Transformer Scikit-Learn: Seluruh imputasi dan kalkulasi scaling dilakukan dengan aturan `fit()` strictly pada data latih (*Train Split*), lalu diterapkan secara pasif `transform()` pada data validasi dan uji.
* **Bukti Fisik**:
  - Pembersih Data: [src/csip/cleaning/cleaner.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/cleaning/cleaner.py)
  - Pipeline Pembersih: [src/csip/cleaning/auto_cleaner.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/cleaning/auto_cleaner.py)
  - Perbandingan Sebelum-Sesudah: [reports/data/DATA_QUALITY_BEFORE_AFTER.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/data/DATA_QUALITY_BEFORE_AFTER.md)
* **Kunci Jawaban Ujian**:
  > *"Pembersihan data kami mematuhi prinsip Split-Before-Transform. Seluruh parameter median atau mean dihitung murni dari subset pelatihan untuk mencegah kebocoran statistik masa depan ke masa lalu."*

---

### UNIT 7: Mengkonstruksi Data / Rekayasa Fitur (`J.62DMI00.009.1`)
* **Tujuan**: Mentransformasikan data mentah menjadi fitur prediktif baru dan mengeliminasi fitur yang membocorkan target (*target leakage*).
* **Implementasi di CSIP**:
  - Rekayasa Fitur Domain:
    - Jarak spasial Haversine tervektorisasi antara penjual dan pembeli.
    - Rasio ongkir terhadap harga barang (`freight_ratio`).
    - Interaksi logistik `delay_x_freight_ratio`.
  - **Audit Kebocoran Waktu Nyata (*Point-in-Time Correctness*)**:
    - Mengeluarkan `approval_lag_hours` dari model checkout dini karena status pembayaran belum disetujui saat tombol beli ditekan.
    - Menolak penggunaan durasi aktual pengiriman (`actual_delivery_days`) pada model checkout karena barang belum dikirim!
* **Bukti Fisik**:
  - Audit Kebocoran Fitur: [reports/feature_availability_and_leakage_audit.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/feature_availability_and_leakage_audit.md)
  - Matrix Audit CSV: [reports/audit/FEATURE_AVAILABILITY_AUDIT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/audit/FEATURE_AVAILABILITY_AUDIT.csv)
* **Kunci Jawaban Ujian**:
  > *"Jika kita memasukkan durasi pengiriman nyata ke dalam model checkout, model akan tampak sangat cerdas dengan PR-AUC 0,60+, tetapi itu adalah model palsu karena di dunia nyata barang belum dikirim saat checkout. Kami secara ketat mengaudit ketersediaan fitur berdasarkan linimasa temporalnya."*

---

### UNIT 8: Membangun Skenario Model (`J.62DMI00.012.1`)
* **Tujuan**: Merancang skenario permodelan terstruktur, kriteria perbandingan, dan tangga algoritma pembanding (*baseline ladder*).
* **Implementasi di CSIP**:
  - Menerapkan **Tangga Baseline 4 Tingkat**:
    - **Tingkat B0**: *Naive Baseline* (Tebakan probabilitas prior konstan).
    - **Tingkat B1**: *Linear Model* (Logistic Regression dengan regularisasi L2 / Ridge).
    - **Tingkat B2**: *Interpretable Non-linear* (Decision Tree & K-Nearest Neighbors).
    - **Tingkat B3**: *High-Capacity Ensemble* (LightGBM Gradient Boosting & Random Forest).
  - Model Sekunder: Vector AutoRegressive (VAR) orde-1 untuk dinamika makro rantai pasok mingguan.
* **Bukti Fisik**:
  - Spesifikasi Skenario: [src/csip/models/classic.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/models/classic.py)
  - World Model Spec: [docs/methodology/WORLD_MODEL_SPECIFICATION.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/methodology/WORLD_MODEL_SPECIFICATION.md)
* **Kunci Jawaban Ujian**:
  > *"Tangga baseline memastikan bahwa kompleksitas model dijustifikasi oleh data. Algoritma canggih hanya diadopsi jika secara statistik mengungguli model sederhana pada PR-AUC dan Brier Score."*

---

### UNIT 9: Membangun Model Machine Learning (`J.62DMI00.013.1`)
* **Tujuan**: Melatih model, menyetel hiperparameter, dan membagi partisi data dengan validasi silang temporal.
* **Implementasi di CSIP**:
  - **Partisi Temporal Kronologis Nyata** (Bukan random shuffle):
    - **Train Split**: 64.156 pesanan (Minggu ke-1 s.d. Minggu ke-64).
    - **Validation Split**: 19.684 pesanan (Minggu ke-65 s.d. Minggu ke-78).
    - **Locked Test Split**: 12.630 pesanan (Minggu ke-79 s.d. Minggu ke-87).
  - Menerapkan *Rolling-Origin Temporal Cross-Validation* dengan 4 lipatan (*expanding folds*) dan embargo pengiriman selama 90 hari untuk mencegah kebocoran waktu tunggu ulasan.
* **Bukti Fisik**:
  - Modul Pelatihan: [src/csip/models/trainer.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/models/trainer.py)
  - Laporan Temporal CV: [reports/evaluation/TEMPORAL_CV_REPORT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/evaluation/TEMPORAL_CV_REPORT.md)
  - Skrip Pelatihan: [scripts/run_ml_experiments.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/scripts/run_ml_experiments.py)
* **Kunci Jawaban Ujian**:
  > *"Transaksi e-commerce memiliki tren sekuensial waktu. Pemisahan data wajib menggunakan partisi temporal dengan embargo pengiriman agar model benar-benar diuji pada data masa depan yang belum pernah dilihat sama sekali."*

---

### UNIT 10: Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
* **Tujuan**: Mengevaluasi performa model pada data uji independen, mengaudit kalibrasi probabilitas, dan mendiagnosis residual.
* **Implementasi di CSIP**:
  - **Performa Model Utama (LightGBM)** pada Locked Test Set:
    - **PR-AUC**: **0,3061** (Unggul +179% dari baseline naif 0,1096).
    - **Kalibrasi Platt Scaling**: Memangkas Brier Score sebesar **-44,59%**, mengubah skor mentah menjadi probabilitas nyata yang akurat untuk penetapan keputusan finansial.
  - Interpretasi Fitur: Nilai SHAP (*Shapley Additive Explanations*) memvalidasi bahwa jarak logistik dan rasio ongkir mendominasi 72% keputusan prediksi.
* **Bukti Fisik**:
  - Leaderboard Evaluasi: [artifacts/reports/ml_leaderboard.json](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/artifacts/reports/ml_leaderboard.json)
  - Laporan Evaluasi: [reports/model_evaluation_and_review_report.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/model_evaluation_and_review_report.md)
* **Kunci Jawaban Ujian**:
  > *"PR-AUC 0,3061 adalah angka murni berbasis fitur checkout dini (tanpa kebocoran durasi pengiriman). Model kami memiliki daya angkat (lift) hampir 3 kali lipat lebih presisi dibanding tebakan acak, dengan probabilitas yang terkalibrasi sempurna melalui Platt Scaling."*

---

### UNIT 11: Melakukan Review Pemodelan (`J.62DMI00.015.1`)
* **Tujuan**: Melakukan tinjauan menyeluruh terhadap keandalan model, mencatat kegagalan/keterbatasan, dan menyusun mitigasi risiko.
* **Implementasi di CSIP**:
  - **Register Kegagalan & Hasil Negatif Empiris**:
    - Menolak hipotesis H3 secara jujur: Terbukti volume pesanan harian tidak berkorelasi linier dengan durasi keterlambatan ($p = 0,861$). Keterlambatan lebih dipengaruhi kapasitas kurir dan jarak geografis.
  - **Batasan Kausalitas**:
    - Mencatat secara eksplisit bahwa simulasi skenario adalah analisis asosiasi terkontrol (*structural sensitivity*), bukan uji kausal A/B testing laboratorium.
  - **Sistem Pemantauan Pergeseran (Concept Drift)**:
    - Memasang observatorium Population Stability Index (PSI) dan Kolmogorov-Smirnov Test untuk mendeteksi keusangan model di masa produksi.
* **Bukti Fisik**:
  - Failure Register: [reports/evidence/evidence_and_failure_register.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/evidence/evidence_and_failure_register.md)
  - Catatan Batasan: [KNOWN_LIMITATIONS.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/KNOWN_LIMITATIONS.md)
  - Engine Drift: [src/csip/monitoring/drift_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/monitoring/drift_engine.py)
* **Kunci Jawaban Ujian**:
  > *"Seorang Data Scientist KKNI Level 7 berani melaporkan hasil negatif secara transparan. Hipotesis H3 kami tolak karena bukti data menunjukkan keterlambatan disebabkan rute logistik, bukan volume pesanan. Model kami juga dilengkapi observatorium drift untuk memantau integritas statistik secara berkelanjutan."*

---

## BAB 3: PANDUAN BELAJAR STEP-BY-STEP

Gunakan urutan 5 langkah berikut untuk menguasai proyek CSIP dari dasar:

### Langkah 1: Menguasai Fondasi Bisnis & Data
1. Buka dan baca ringkasan eksekutif: [reports/final/CSIP_FINAL_EXECUTIVE_SUMMARY.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/final/CSIP_FINAL_EXECUTIVE_SUMMARY.md).
2. Pahami diagram relasi 9 tabel Olist di [notebooks/01_business_and_data_understanding.ipynb](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/notebooks/01_business_and_data_understanding.ipynb).
3. Pahami mengapa keterlambatan pengiriman adalah "musuh nomor satu" kepuasan pelanggan.

### Langkah 2: Memahami Proteksi Kebocoran Data (Anti-Leakage)
1. Buka [reports/feature_availability_and_leakage_audit.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/reports/feature_availability_and_leakage_audit.md).
2. Pahami perbedaan antara:
   - **Informasi saat Checkout ($t_0$)**: Ongkir yang ditagih, harga barang, metode pembayaran, lokasi pembeli/penjual, jarak estimasi.
   - **Informasi pasca Pengiriman ($t_{\text{del}}$)**: Tanggal terima barang riil, durasi keterlambatan nyata, bintang ulasan.
3. Ingat selalu: **Model checkout tidak boleh menggunakan fitur pasca pengiriman!**

### Langkah 3: Memahami Pemodelan Mesin & Kalibrasi Probabilitas
1. Buka [artifacts/reports/ml_leaderboard.json](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/artifacts/reports/ml_leaderboard.json).
2. Pahami mengapa LightGBM menang atas Logistic Regression dan Random Forest.
3. Pahami fungsi **Platt Scaling**: Mengapa probabilitas 0,80 harus benar-benar berarti bahwa 80 dari 100 pesanan tersebut akan kecewa.

### Langkah 4: Memahami World Model & Simulasi Dinamika Sistem
1. Buka [docs/methodology/WORLD_MODEL_SPECIFICATION.md](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/methodology/WORLD_MODEL_SPECIFICATION.md).
2. Pelajari bagaimana sistem membuat simulasi intervensi makro: apa yang terjadi pada kepuasan jika biaya logistik naik 10% atau waktu transit dipotong 2 hari.

### Langkah 5: Memahami Observatorium Drift & Stabilitas Kovariat
1. Buka [src/csip/monitoring/drift_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/src/csip/monitoring/drift_engine.py).
2. Pahami metrik **Population Stability Index (PSI)**:
   - $\text{PSI} < 0,10$: Distribusi stabil (Aman).
   - $0,10 \le \text{PSI} < 0,25$: Pergeseran moderat (Waspada).
   - $\text{PSI} \ge 0,25$: Terjadi *concept drift* signifikan (Model wajib di-retrain).

---

## BAB 4: SKRIP DEMONSTRASI PRAKTIK DI DEPAN ASESOR / PENGUJI (15–20 MENIT)

Saat Anda diminta mendemonstrasikan sistem di hadapan asesor atau penguji, ikuti urutan langkah taktis berikut:

---

### Fase 1: Pembukaan & Gambaran Eksekutif (2 Menit)
1. Buka terminal di folder proyek dan jalankan Streamlit:
   ```powershell
   streamlit run app/streamlit_app.py
   ```
2. Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`.
3. **Kalimat Pembuka yang Diucapkan**:
   > *"Selamat pagi/siang Bapak/Ibu Asesor. Hari ini saya mendemonstrasikan Core Strategy & Intelligence Platform (CSIP), sebuah platform decision intelligence tingkat enterprise yang telah divalidasi penuh terhadap 11 Unit Kompetensi SKKNI No. 299 Tahun 2020 untuk skema Ilmuwan Data KKNI Level 7.*  
   > *CSIP dirancang tidak hanya untuk melatih model prediktif, tetapi juga sebagai simulator keputusan berbasis kebijakan dan observatorium integritas model secara real-time."*

---

### Fase 2: Demonstrasi Fleksibilitas Data & Profiling Semantik (3 Menit)
1. Pada **Langkah 1 (Panel Kiri)**, perlihatkan dropdown *"Atau pakai dataset bawaan"*:
   - Tunjukkan **Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)**.
   - Pilihlah **Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)** atau **Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)**.
   - Tunjukkan bahwa sistem langsung membaca kolom, tipe data, dan menyesuaikan konteks analisis secara instan.
2. Tunjukkan bahwa platform juga menerima unggahan berkas **CSV maupun Excel (`.xlsx`)** dari komputer lokal.
3. Tunjukkan penjelasan otomatis pada kotak oranye (*"Artinya begini..."*) yang menerangkan definisi variabel target.

---

### Fase 3: Pengujian Tuas Simulasi & Titik Kritis Bento Cards (4 Menit)
1. Pilih kembali dataset **Kasus 1: Toko Online & Kepuasan Pembeli**.
2. Pada **Langkah 2 (Tuas Simulasi)**, tunjukkan 3 slider fitur dominan:
   - Tuas #1: *Keterlambatan Kirim* (Bobot Pengaruh ~35%).
   - Tuas #2: *Lama Pengiriman*.
   - Tuas #3: *Ongkos Kirim*.
3. Geser slider *Keterlambatan Kirim* dari nilai median (0 hari) menjadi **5 hari terlambat**.
4. Perhatikan dan tunjukkan ke asesor bagaimana **3 Kartu Bento** di kanan atas berubah seketika:
   - **Kartu 1 (Estimasi Kepuasan)**: Nilai estimasi anjlok dari ~83 poin menjadi ~45 poin (Warna berubah menjadi merah / *"Perlu Perhatian"*).
   - **Kartu 2 (Faktor Penentu Terkuat)**: Menampilkan bahwa Keterlambatan Kirim memegang pengaruh dominan dengan arah berlawanan (*Makin tinggi, kepuasan tergerus turun*).
   - **Kartu 3 (Selisih dari Standar)**: Menunjukkan defisit performa yang presisi (misal: -38,2 poin) lengkap dengan toleransi error model MAE.

---

### Fase 4: Eksplorasi 4 Lensa Analitik Interaktif (5 Menit)
Tunjukkan secara bergantian ke-4 Lensa Tampilan pada radio button di panel kanan:

1. **Pilih Lensa 1 (Kurva Simulasi dan Titik Kritis)**:
   - Tunjukkan kurva respons non-linier teal dengan titik kritis infleksi (*amber badge*).
   - Jelaskan ke asesor:
     > *"Kurva ini membuktikan bahwa respons kepuasan pelanggan tidak linier sempurna. Di sekitar titik keterlambatan 1,5 hari, kurva mengalami penurunan tajam sebelum akhirnya mendatar di zona jenuh kepuasan rendah."*
2. **Pilih Lensa 2 (Peringkat Faktor Penentu)**:
   - Tunjukkan diagram batang horizontal yang memetakan persentase pengaruh fitur.
   - Tunjukkan bahwa 2 faktor logistik teratas menguasai lebih dari 60% dinamika kepuasan transaksi.
3. **Pilih Lensa 3 (Sebaran Kelompok Data)**:
   - Tunjukkan kurva sebaran kepadatan bertumpuk (*Ridgeline Visualization*).
   - Jelaskan bahwa populasi dibagi ke dalam 3 strata (Kelompok Bawah, Menengah, Atas) dan tunjukkan garis penanda di mana posisi simulasi tuas saat ini berada di dalam sebaran populasi.
4. **Pilih Lensa 4 (Observatorium Drift & Stabilitas Kovariat)**:
   - Tunjukkan tampilan *Dual-Pane Vector SVG Layout*:
     - **Panel Kiri**: 5 meter stabilitas kovariat (PSI) dengan garis batas ambang aman 0,10 dan badge status hijau (*✓ Stabil*).
     - **Panel Kanan**: Kurva kepadatan ganda (*KDE curves*) yang membandingkan Data Acuan (Baseline) vs Data Terpantau (Live Stream) dengan badge keselarasan distribusi aktual (~99%).
   - Jelaskan ke asesor:
     > *"Lensa 4 adalah pembuktian Unit 11 (Review Pemodelan). Kami mengaudit apakah aliran data baru mengalami pergeseran statistik kovariat. Rata-rata PSI tercatat 0,0074, jauh di bawah ambang bahaya 0,10, membuktikan model aman dari keusangan (concept drift)."*

---

### Fase 5: Menunjukkan Narasi Cerdas Penasihat Nara (3 Menit)
1. Tunjukkan **Kartu Narasi Nara** di bagian bawah panggung pameran.
2. Jelaskan bahwa Nara membaca angka-angka dari kalkulasi ML secara langsung:
   - Menyebutkan persentase pengaruh faktor utama dan sekunder secara presisi.
   - Menyebutkan posisi estimasi saat ini terhadap baseline acuan.
   - Memberikan 2 butir rekomendasi taktis (*Action Pills*) yang siap ditindaklanjuti direksi.

---

### Fase 6: Pembuktian Kualitas Kode, CI/CD & Audit KUK (3 Menit)
Buka terminal dan jalankan 2 perintah pembuktian kualitas otomatis untuk membuktikan kesiapan portofolio secara transparan:

1. **Jalankan Verifikasi Rilis 12 Gerbang Mutu**:
   ```powershell
   python tools/verify_release.py
   ```
   *Tunjukkan bahwa seluruh 12 Quality Gates (G1–G12) berstatus `[PASS]`.*

2. **Jalankan Audit Bukti 63 Kriteria Unjuk Kerja (KUK)**:
   ```powershell
   python scripts/run_evidence_check.py
   ```
   *Tunjukkan bahwa 63/63 KUK terverifikasi dengan 0 berkas hilang dan 0 hash mismatch.*

3. **Jalankan Pengujian Otomatis Pytest**:
   ```powershell
   pytest tests/test_app_pages.py -v
   ```
   *Tunjukkan bahwa seluruh tes antarmuka dan lensa analitik lolos 100%.*

---

## BAB 5: BANK TANYA-JAWAB UJI LISAN (ORAL DEFENSE) & JAWABAN EMAS

Berikut adalah 10 pertanyaan tersulit yang sering diajukan Master Asesor BNSP KKNI Level 7 beserta **Jawaban Emas Berbasis Bukti**:

#### Q1: "Mengapa Anda menggunakan PR-AUC bukan ROC-AUC atau Akurasi?"
> **Jawaban Emas**:
> *"Karena pada kasus e-commerce Olist, distribusi kelas ulasan negatif sangat timpang (hanya ~10,9% populasi uji). Akurasi akan tertipu oleh kelas mayoritas puas. Sementara ROC-AUC diredam oleh tingginya True Negatives pada penyebut False Positive Rate ($FPR = \frac{FP}{FP+TN}$). PR-AUC secara murni mengevaluasi rasio Precision terhadap Recall khusus pada kelas minoritas, dengan baseline acuan berupa nilai prevalensi positif (0,1096). Model kami mencapai PR-AUC 0,3061 (+179% di atas baseline naif)."*

#### Q2: "Bagaimana Anda membuktikan bahwa model Anda bebas dari Data Leakage?"
> **Jawaban Emas**:
> *"Kami menerapkan protokol Split-Before-Transform dan audit ketersediaan fitur titik-waktu (Point-in-Time Correctness). Pertama, pemisahan data dilakukan secara temporal sebelum proses imputasi atau scaling dijalankan. Kedua, kami mengeluarkan fitur pasca-transaksi seperti durasi pengiriman nyata dan approval lag dari model checkout karena informasi tersebut belum ada saat pesanan dibuat."*

#### Q3: "Mengapa Anda memilih pemisahan data Temporal daripada K-Fold Cross Validation acak?"
> **Jawaban Emas**:
> *"Data transaksi komersial memiliki ketergantungan urutan waktu. Random cross-validation menyebabkan lookahead bias karena model mempelajari pola masa depan untuk memprediksi masa lalu. Kami membagi data secara kronologis: Train (Minggu 1–64), Validation (Minggu 65–78), dan Test (Minggu 79–87) dengan embargo 90 hari untuk merefleksikan kondisi operasional nyata di lapangan."*

#### Q4: "Apa fungsi Platt Scaling pada model Anda?"
> **Jawaban Emas**:
> *"Algoritma ensemble seperti LightGBM sering menghasilkan skor probabilitas mentah yang tidak terkalibrasi secara proporsional. Kami menerapkan kalibrasi logistik pasca-pemodelan (Platt Scaling) yang berhasil memangkas Brier Score sebesar -44,59%. Dengan demikian, probabilitas output model dapat dipercaya secara andal untuk pengambilan keputusan kompensasi finansial."*

#### Q5: "Apa itu World Model yang Anda bangun di Unit 8?"
> **Jawaban Emas**:
> *"World Model adalah permodelan dinamika sistem makro berbasis Vector AutoRegressive (VAR) tingkat mingguan. Tujuannya bukan memprediksi order individu, melainkan mensimulasikan interaksi lintas variabel sistem: bagaimana guncangan biaya ongkir mempengaruhi volume pesanan dan keterlambatan rata-rata di minggu-minggu berikutnya."*

#### Q6: "Mengapa Anda menolak hipotesis H3 (bahwa volume pesanan berkorelasi linier dengan delay)?"
> **Jawaban Emas**:
> *"Berdasarkan pengujian statistik empiris, korelasi Pearson antara volume harian dan durasi keterlambatan menghasilkan nilai p-value 0,861 (tidak signifikan secara statistik). Data membuktikan bahwa keterlambatan logistik lebih dipengaruhi oleh jarak geografis antarkota dan kapabilitas armada kurir lokal, bukan semata-mata karena lonjakan pesanan harian. Kami mencatat penolakan hipotesis ini secara terbuka di Failure Register."*

#### Q7: "Apa yang dimaksud dengan Concept Drift dan bagaimana CSIP memantaunya?"
> **Jawaban Emas**:
> *"Concept drift adalah penurunan performa model akibat pergeseran hubungan statistik antara fitur input dan target di dunia nyata. CSIP memasang DriftEngine yang mengukur Population Stability Index (PSI) dan uji dua sampel Kolmogorov-Smirnov. Selama nilai PSI di bawah 0,10, model dikategorikan stabil. Jika melewati 0,25, sistem membunyikan alarm perlunya retraining otomatis."*

#### Q8: "Bagaimana Anda memastikan pengujian sistem Anda dapat direproduksi (Reproducible)?"
> **Jawaban Emas**:
> *"Seluruh eksperimen menggunakan seed deterministik tetap (random_state=42), versi pustaka terpin pada requirements.txt, serta registri bukti SHA-256 pada CANONICAL_EVIDENCE_REGISTRY.csv. Skrip tools/verify_release.py dan scripts/run_evidence_check.py dapat dijalankan dengan satu perintah untuk memverifikasi 100% konsistensi seluruh artefak."*

#### Q9: "Apakah rekomendasi Nara dapat dianggap sebagai intervensi kausal definitif?"
> **Jawaban Emas**:
> *"Secara etika data science, kami menyatakan secara transparan bahwa rekomendasi intervensi berbasis data observasional merupakan analisis asosiasi terkontrol dan simulasi struktural. Untuk membuktikan hubungan sebab-akibat murni tanpa bias perancu (confounding bias), rekomendasi Nara wajib divalidasi terlebih dahulu melalui uji acak terkendali (A/B testing) di lapangan sebelum diimplementasikan secara permanen."*

#### Q10: "Mengapa CSIP dikembangkan dengan antarmuka Single-Page Cockpit?"
> **Jawaban Emas**:
> *"Pendekatan Single-Page Cockpit menyatukan rantai nilai data science—mulai dari input data, simulasi parameter, diagnosis kurva non-linier, hingga audit integritas drift—ke dalam satu bidang pandang kerja yang ergonomis. Pengambil keputusan bisnis tidak perlu berpindah-pindah menu yang membingungkan untuk memahami dampak suatu keputusan secara holistik."*

---

> [!TIP]
> **Kunci Keberhasilan Asesmen**:
> Bicaralah dengan tenang, percaya diri, dan selalu arahkan layar monitor asesor ke file atau baris kode yang membuktikan ucapan Anda. Integritas ilmiah dan kejujuran metodologis adalah nilai tertinggi seorang Ilmuwan Data KKNI Level 7.
