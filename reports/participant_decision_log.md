# CSIP Participant Decision & Methodology Log
## Active Data Scientist Human Ownership & Critical Decision Audit

**Document ID**: `CSIP-LOG-DECISION-2026`  
**Standard**: SKKNI No. 299 Tahun 2020 (KKNI Jenjang 7)  
**Role**: Principal / Senior Data Scientist (Peserta Asesmen)  
**Principle**: Peserta adalah pemegang otoritas dan pengambil keputusan metodologis utama; AI / Multi-Agent semata-mata merupakan alat bantu komputasi (*assistive tooling*).  
**Date**: November 2026  

---

## 1. Executive Statement of Participant Primacy

Dalam seluruh siklus pengembangan **Core Strategy & Intelligence Platform (CSIP)**, peserta bertindak sebagai **Lead Data Scientist** yang merancang arsitektur, menentukan formulasi masalah, mengevaluasi alternatif teknis, mengoreksi output komputasi otomatis, dan bertanggung jawab penuh secara etis dan metodologis atas seluruh temuan empiris.

Keputusan kritis tidak pernah diserahkan secara buta kepada model machine learning atau agen AI. Setiap rekomendasi otomatis selalu melalui proses validasi independen, verifikasi statistik, dan pemeriksaan integritas domain.

---

## 2. Chronological Decision & Correction Log

Berikut adalah rekaman keputusan-keputusan teknis krusial yang diambil oleh peserta:

### Keputusan 1: Pemilihan PR-AUC daripada ROC-AUC sebagai Metrik Evaluasi Primer
- **Masalah yang Ditemukan**: Distribusi kelas target komplain ulasan pelanggan (bintang 1 & 2) sangat timpang (*extreme class imbalance*, hanya ~8.1% dari total populasi).
- **Alternatif Metode**:
  1. *ROC-AUC*: Mengukur True Positive Rate terhadap False Positive Rate.
  2. *Accuracy*: Mengukur persentase prediksi benar secara agregat.
  3. *PR-AUC (Precision-Recall Area Under Curve)*: Mengukur presisi terhadap recall pada kelas minoritas.
- **Metode Terpilih**: **PR-AUC**.
- **Alasan Pemilihan Peserta**: Pada dataset dengan kelas minoritas ekstrem, metrik Akurasi menjadi tidak berguna (prediktor trivial yang memprediksi mayoritas akan meraih akurasi 92%). ROC-AUC juga menghasilkan skor optimisme palsu yang tinggi (misal: 0.85) karena False Positive Rate diredam oleh besarnya jumlah True Negatives. Sebaliknya, PR-AUC berfokus secara tajam pada kemampuan model menemukan kelas positif tanpa dibanjiri false alarm.
- **Koreksi Terhadap AI**: Menolak saran awal algoritma otomatis yang menggunakan ROC-AUC sebagai KPI tunggal; memaksa metrik PR-AUC menjadi objektif optimasi utama di `config/models.yaml`.
- **Hasil Akhir**: Model LightGBM mencapai PR-AUC 0.3004, melampaui baseline naive 0.0814 sebesar +269%.

---

### Keputusan 2: Penolakan Random K-Fold dan Penegakan Temporal Out-of-Time Holdout Split
- **Masalah yang Ditemukan**: Transaksi e-commerce memiliki korelasi serial dan pergeseran tren musiman (*distribution shift*). Pengacakan baris acak (*random k-fold split*) memasukkan observasi masa depan ke dalam subset pelatihan data masa lalu.
- **Alternatif Metode**:
  1. *Stratified 5-Fold Cross-Validation*: Mengacak data secara merata antar-kelas.
  2. *Temporal Out-of-Time (OOT) Holdout Partition*: Memotong data berdasarkan batas tanggal kronologis (*cutoff date*).
- **Metode Terpilih**: **Temporal Out-of-Time Split (Cutoff: `2018-06-01`)**.
- **Alasan Pemilihan Peserta**: Dalam lingkungan produksi nyata, sistem tidak pernah memiliki akses ke data masa depan saat melayani transaksi saat ini. K-fold acak memberikan skor performa yang terlalu optimis (*optimistic lookahead leakage*). Partisi temporal menguji kemampuan generalisasi model terhadap masa depan sesungguhnya.
- **Validasi**: Seluruh model dilatih pada data sebelum Juni 2018 ($N=76,462$) dan diuji pada data Juni s.d. Agustus 2018 ($N=20,008$).
- **Hasil Akhir**: Estimasi performa model di out-of-time test set menjadi realistis dan bebas dari kebocoran data.

---

### Keputusan 3: Penolakan Pembuktian Kausalitas dan Pembatasan Klaim Ilmiah Menjadi Asosiasi (L2)
- **Masalah yang Ditemukan**: Analisis awal menunjukkan korelasi kuat antara keterlambatan pengiriman dan ulasan negatif. Modul analisis otomatis sempat merekomendasikan klaim bahwa "mengurangi keterlambatan secara kausal pasti menaikkan GMV sebesar 18%".
- **Alternatif Metode**:
  1. *Klaim Kausalitas Langsung (L3 Causal)*: Mengklaim intervensi kebijakan pasti berdampak langsung.
  2. *Klaim Asosiasi Terkontrol & Analisis Skenario (L2 Associational)*: Mengakui batasan data observasional dan menyajikan hasil sebagai proyeksi skenario sensitivitas.
- **Metode Terpilih**: **L2 (Associational Claim) & Scenario Sensitivity Analysis**.
- **Alasan Pemilihan Peserta**: Dataset Olist adalah data observasional retrospektif tanpa eksperimen uji acak terkontrol (*Randomized Controlled Trial / A/B Test*). Mengklaim efek kausal tanpa identifikasi instrumen atau kuasi-eksperimen yang valid melanggar integritas ilmiah Data Science tingkat lanjut.
- **Koreksi Terhadap AI**: Mengubah narasi di dashboard Streamlit dan laporan dari "Dampak Kausal Intervensi" menjadi "Simulasi Skenario Kebijakan Berbasis Asosiasi Terkontrol", serta mencatat batasan ini dalam `FailureRecord` (`LIMIT-CAUSAL`).
- **Hasil Akhir**: Seluruh rekomendasi kebijakan logistik disajikan dengan rentang ketidakpastian bootstrap 95% CI yang jujur dan dapat dipertanggungjawabkan.

---

### Keputusan 4: Pencatatan Terbuka Penolakan Hipotesis H3 (FAIL-HYP-H3)
- **Masalah yang Ditemukan**: Hipotesis bisnis umum mengasumsikan bahwa penjual dengan skor rating tinggi menikmati volume transaksi yang jauh lebih besar (*seller rating premium*).
- **Alternatif Tindakan**:
  1. Melakukan *p-hacking* atau mengubah definisi hipotesis agar hasil uji menjadi signifikan (*statistically significant*).
  2. Menyembunyikan hasil hipotesis yang tidak terbukti dari laporan akhir.
  3. Merekam hasil penolakan hipotesis secara transparan sebagai temuan negatif yang valid (*valid negative result*).
- **Keputusan Peserta**: **Merekam Penolakan Hipotesis di Failure Register (`FAIL-HYP-H3`)**.
- **Alasan Pemilihan Peserta**: Pengujian statistik inferensial setelah koreksi Benjamini-Hochberg FDR menghasilkan $p_{\text{adj}} = 0.859$ dengan ukuran efek $d = 0.012$ (dapat diabaikan). Menyembunyikan hasil negatif adalah pelanggaran etika ilmiah. Temuan ini membuktikan bahwa di marketplace Olist, pembeli jauh lebih dipengaruhi oleh harga produk dan biaya pengiriman daripada reputasi masa lalu penjual.
- **Hasil Akhir**: Transparansi kegagalan meningkatkan kredibilitas analitis proyek di hadapan asesor BNSP dan mengarahkan fokus efisiensi bisnis ke subsidi ongkir alih-alih gamifikasi rating penjual.

---

### Keputusan 5: Penegakan Kalibrasi Probabilitas Platt Scaling Sebelum Decisioning
- **Masalah yang Ditemukan**: Model pohon seperti LightGBM dan Random Forest menghasilkan estimasi probabilitas mentah (*raw predicted probabilities*) yang terdistorsi dan overconfident pada ekor probabilitas tinggi.
- **Alternatif Metode**:
  1. Menggunakan skor probabilitas mentah langsung untuk klasifikasi dengan threshold default 0.5.
  2. Menerapkan *Platt Scaling (Logistic Sigmoidal Calibration)* pada validation set terpisah.
  3. Menerapkan *Isotonic Regression*.
- **Metode Terpilih**: **Platt Scaling Calibration**.
- **Alasan Pemilihan Peserta**: Untuk dataset dengan ketimpangan kelas, Isotonic Regression rawan overfitting pada data yang jarang di ekor. Platt scaling menghasilkan kurva kalibrasi parametrik yang halus dan stabil.
- **Validasi**: Brier Score terpangkas sebesar **44.59%** (dari 0.1375 menjadi 0.0762) dan Expected Calibration Error (ECE) merosot dari 0.2355 menjadi 0.0070.
- **Hasil Akhir**: Probabilitas risiko ulasan negatif yang ditampilkan kepada tim customer service di antarmuka Streamlit benar-benar mencerminkan frekuensi empiris kejadian di dunia nyata.

---

## 3. Matriks Pertanggungjawaban Peserta

| Area Kerja | Kontribusi Alat Bantu (AI/Scripts) | Keputusan & Tanggung Jawab Peserta (Human Data Scientist) |
| :--- | :--- | :--- |
| **Formulasi Masalah** | Ekstraksi statistik mentah dataset | Menentukan 3 pilar objektif bisnis dan kriteria kesuksesan finansial. |
| **Validasi & Pembersihan** | Eksekusi fungsi perulangan filter baris | Menetapkan aturan eliminasi 23 baris anomali dan batas waktu *censoring*. |
| **Rekayasa Fitur** | Perhitungan vektorisasi formula matematis | Merancang variabel interaksi domain dan menegakkan isolasi temporal anti-kebocoran. |
| **Pemilihan Model** | Training otomatis baseline ladder B0-B4 | Memilih LightGBM atas pertimbangan non-linearitas, interpretasi SHAP, dan batas 8GB RAM. |
| **Evaluasi & Governance** | Kalkulasi matriks metrik dan plot kurva | Menerapkan kalibrasi probabilitas, mencatat kegagalan H3, dan membatasi klaim L0-L3. |
