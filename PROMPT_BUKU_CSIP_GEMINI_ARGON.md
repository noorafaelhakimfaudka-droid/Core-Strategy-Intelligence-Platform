# MEGA PROMPT: GENERATOR BUKU UTUH "BLUEPRINT CSIP" DI GEMINI ARGON

> **Petunjuk Penggunaan**:
> Salin (*copy*) seluruh teks di dalam blok prompt di bawah ini, lalu tempelkan (*paste*) ke sesi baru di **Gemini Argon**.
> Prompt ini telah dilengkapi seluruh konteks teknis, angka empiris, formula matematis, logika 11 Unit SKKNI, hingga strategi demonstrasi sehingga Gemini Argon dapat menyusun buku teks setebal puluhan halaman bab-demi-bab secara komprehensif.

```markdown
Role: Anda adalah seorang Principal Enterprise AI Architect, Guru Besar Ilmu Data Science, dan Master Asesor Sertifikasi KKNI Level 7 yang memiliki kemampuan menulis buku teknis kaliber dunia (seperti penerbit O'Reilly, MIT Press, atau Springer).

Tugas Anda:
Tuliskan sebuah BUKU INDUK LENGKAP & DEEP-DIVE BERHALAMAN-HALAMAN berjudul:
"KITAB INDUK CSIP: Blueprint Arsitektur Data Science Enterprise, Simulator Kebijakan, dan Observatorium Integritas Model"
(Sub-judul: Dari Konsep Dasar, Matematika, Kode Produksi, hingga Panduan Sukses Asesmen BNSP KKNI Level 7).

Tujuan Buku:
Buku ini akan menjadi buku pegangan belajar utama saya. Saya ingin menghafal, memahami secara intuitif dari level 0, dan menguasai setiap baris logika, angka empiris, serta rasional keputusan teknis yang ada di platform CSIP. 

Gaya Penulisan Buku:
1. Bahasa Indonesia yang mengalir, elegan, sangat mudah dipahami (menggunakan analogi dunia nyata untuk konsep rumit), namun tetap berbobot teknis tinggi dan saintifik.
2. Setiap konsep harus dibedah dengan pola:
   - "Kenapa Masalah Ini Muncul di Bisnis?" (Latar Belakang & Konteks Riil).
   - "Bagaimana Cara Kerja Matematikanya?" (Rumus KaTeX & Penjelasan Intuitif).
   - "Bagaimana Implementasinya di Kode CSIP?" (Bedah Modul, Parameter, dan File).
   - "Rasional Keputusan: Mengapa Memilih A dan Menolak B?" (Trade-off Analysis).
   - "Simulasi Pertanyaan Asesor / Penguji & Cara Menjawabnya dengan Bukti".
3. DILARANG meringkas atau membuat bullet-point pendek yang dangkal! Tuliskan narasi penuh layaknya buku teks profesional yang mendalam.

---

### KONTEKS PROYEK CSIP YANG WAJIB DIBAHAS DI DALAM BUKU:

1. Identitas Proyek:
   - Nama: Core Strategy & Intelligence Platform (CSIP) v1.0.0.
   - Pencipta/Kandidat: Noorafael Hakim Faudka.
   - Sifat: Local, Auditable Decision Cockpit & MLOps Platform (Single-Page Streamlit Cockpit di app/streamlit_app.py).

2. Studi Kasus Riil (E-Commerce Olist Brasil):
   - ~100.000 transaksi dari 9 tabel relasional (orders, order_items, payments, reviews, customers, sellers, products, geolocation, category_translation).
   - Masalah: 8.0% pesanan mengalami keterlambatan kirim (delivery delay), yang menyebabkan rating ulasan anjlok dari 4.14 menjadi 2.15 (-48%), memicu lonjakan ulasan negatif +381%, dan membakar biaya CS kompensasi senilai ratusan ribu Real.
   - Solusi: Early Warning System sejak checkout (t_0) dan Simulator Intervensi Kebijakan.

3. Cakupan Analitik Universal (Universal Tabular Engine untuk CSV & Excel):
   - Mampu memproses CSV maupun Excel (.xlsx, .xls) lintas 8 domain industri:
     * Kesehatan/Medis (BMI, glukosa, tensi, progresi penyakit).
     * Mutu Produk/Manufaktur (komposisi kimia, flavonoid, getaran sensor, defect rate).
     * SDM (gaji, lembur, absensi, KPI).
     * Finansial/Pasar Modal (omzet, laba, harga saham, bunga, cash flow).
     * E-Commerce/Logistik (ongkir, delay, kepuasan).
     * Pemasaran Digital (CTR, CVR, CAC, churn, retensi).
     * Properti (harga rumah, luas, kamar).
     * Edukasi (jam belajar, presensi, IPK).
   - Polarity-Aware Target Optimization: Membedakan target yang harus ditekan (risiko, biaya, cacat, delay) vs yang harus didorong (laba, kepuasan, mutu).

4. Arsitektur Antarmuka (CSIP Studio Cockpit):
   - Bento Cards Kinerja: Estimasi Target, Faktor Penentu Terkuat, Selisih Standar (Toleransi MAE).
   - 4 Lensa Tampilan:
     * Lensa 1: Kurva Simulasi dan Titik Kritis Infleksi (Non-linear response & tipping point).
     * Lensa 2: Peringkat Faktor Penentu (Random Forest feature importance & Pearson r).
     * Lensa 3: Sebaran Kelompok Data (Stratifikasi Ridgeline SVG: Bawah, Menengah, Atas).
     * Lensa 4: Observatorium Drift & Stabilitas (Dual-Pane Vector SVG: Stabilitas Kovariat PSI + Kurva Densitas KDE Baseline vs Live Stream).
   - Nara (Strategic Advisor): Agen preskriptif dinamis yang mengolah angka riil, tipping points, dan drift metrics menjadi arahan taktis operasional.

5. Kepatuhan Penuh 11 Unit SKKNI No. 299 Tahun 2020 (LSP TRI KKNI Level 7):
   - Unit 1 (Objektif Bisnis): Target reduksi ulasan negatif 20% & mitigasi biaya R$ 142.000.
   - Unit 2 (Tujuan Teknis): Wajib PR-AUC & Brier Score, tolak Akurasi & ROC-AUC karena imbalanced class (10.9% negatif di test set).
   - Unit 3 (Menelaah Data): Relasi 9 tabel, 0 orphan records.
   - Unit 4 (Memvalidasi Data): Anomali waktu t_del < t_pur, 646 missing reviews dipertahankan NaN (tidak diimputasi rata-rata demi integritas ground truth).
   - Unit 5 (Objek Data): 4 grain analitis (order_level, customer_cohort, review_corpus, weekly_system_state).
   - Unit 6 (Membersihkan Data): Deduplikasi geolokasi (-98.1% reduksi dari 1.000.163 ke 19.015 zip centroids), Split-Before-Transform.
   - Unit 7 (Konstruksi Fitur): Jarak Haversine, freight_ratio, Point-in-time correctness (keluarkan approval_lag_hours dan actual_delivery_days dari model checkout).
   - Unit 8 (Skenario Model): Tangga Baseline B0 Naive -> B1 Linear/Ridge -> B2 DecisionTree/KNN -> B3 LightGBM/RandomForest; VAR World Model.
   - Unit 9 (Membangun Model): Partisi temporal sekuensial (Train Minggu 1-64: 64.156 baris, Val Minggu 65-78: 19.684 baris, Test Minggu 79-87: 12.630 baris), 4-fold expanding rolling temporal CV, embargo pengiriman 90 hari.
   - Unit 10 (Evaluasi Model): LightGBM PR-AUC 0.3061 (+179% vs naive 0.1096), Platt Scaling memangkas Brier Score -44.59%, interpretasi SHAP.
   - Unit 11 (Review Pemodelan): Hasil negatif jujur penolakan hipotesis H3 (volume vs delay tidak berkorelasi linier, p=0.861), catatan batasan non-kausal (observational sensitivity bukan A/B test), Observatorium Drift (mean PSI 0.0074 < 0.10 aman).

6. Verifikasi & Integritas Rekayasa:
   - 197/197 unit & integration tests lolos (100% pass rate).
   - 12/12 Release Quality Gates lolos.
   - 63/63 KUK Canonical Evidence Registry sinkron tanpa selisih hash.
   - 0 secrets, 0 hardcoded personal Windows paths.

---

### STRUKTUR BAB BUKU YANG HARUS ANDA SUSUN:

BAGIAN I: FILOSOFI & ARSITEKTUR KONSEPTUAL CSIP
- Bab 1: Mengapa Bisnis Butuh Decision Cockpit, Bukan Sekadar Dashboard?
- Bab 2: Anatomi Masalah E-Commerce Olist Brasil: Anatomi Rantai Pasok yang Rapuh.
- Bab 3: Universal Decision Engine: Rahasia CSIP Membedah Berkas CSV & Excel Lintas 8 Sektor Industri.
- Bab 4: Mengenal Nara: Desain Agen Penasihat Preskriptif Tanpa Template Kaku.

BAGIAN II: METODOLOGI DATA SCIENCE & INTEGRITAS STATISTIK (11 UNIT SKKNI)
- Bab 5: Dari Kebutuhan Bisnis ke Kontrak Prediksi (Unit 1 & Unit 2 SKKNI).
- Bab 6: Validasi, Pembersihan, dan Proteksi Kebocoran Data Temporal (Unit 3, 4, 5, 6 SKKNI).
- Bab 7: Rekayasa Fitur Berbasis Fisika Domain & Audit Point-in-Time Correctness (Unit 7 SKKNI).
- Bab 8: Tangga Baseline B0-B3 dan Pelatihan Model Bebas Bias Masa Depan (Unit 8 & Unit 9 SKKNI).
- Bab 9: Evaluasi PR-AUC, Kalibrasi Probabilitas Platt Scaling, dan Diagnostik SHAP (Unit 10 SKKNI).
- Bab 10: Uji Kejujuran Ilmiah: Failure Register, Penolakan Hipotesis H3 & World Model VAR (Unit 11 SKKNI).

BAGIAN III: OBSERVATORIUM REAL-TIME & TEORI CONCEPT DRIFT
- Bab 11: Teori Pergeseran Kovariat: Mengapa Model di Masa Depan Pasti Rusak?
- Bab 12: Matematika di Balik PSI, Kolmogorov-Smirnov, dan Jarak Wasserstein.
- Bab 13: Arsitektur Dual-Pane Vector SVG: Menggabungkan Meter PSI dan Kurva Densitas KDE.

BAGIAN IV: PANDUAN PRAKTIK DEMONSTRASI & UJI LISAN ASESMEN
- Bab 14: Skrip 15 Menit Demonstrasi Praktik di Depan Asesor BNSP (Panduan Bertahap).
- Bab 15: Kamus Pertahanan Ilmiah: 10 Pertanyaan Jebakan Master Asesor & Jawaban Emas Berbasis Bukti.

---

INSTRUKSI PENGERJAAN:
Mulailah dengan menuliskan Kata Pengantar, Roadmap Pembelajaran, dan langsung masuk secara mendalam ke BAGIAN I (Bab 1, 2, 3, dan 4). Tuliskan secara lengkap, detail, berbobot, berhalaman-halaman tanpa memotong penjelasan!
```

