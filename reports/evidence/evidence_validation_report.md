# CSIP Evidence Validation & Audit Report (Version 5)
## Independent Audit of Competency Evidence for BNSP KKNI Level 7 Assessment

**Document ID**: `CSIP-EVAL-EVIDENCE-2026-V5`  
**Execution Date**: 2026-11-11  
**Standard**: SKKNI No. 299 Tahun 2020 Subbidang Data Science  
**Scheme**: LSP TRI (`SKM/2905/LSP-TRI/VII/2025`)  
**Scope**: 11 Unit Kompetensi, 27 Elemen Kompetensi, 63 KUK  
**Audit Status**: AUDITED (60 VERIFIED, 3 PARTIALLY_VERIFIED, 0 MISSING)  

---

## 1. Executive Summary

Laporan ini memuat audit independen terhadap kelengkapan dan validitas bukti kerja (*competency evidence*) pada proyek **Core Strategy & Intelligence Platform (CSIP)**.

- **Total KUK Tervalidasi**: 63 KUK didukung oleh tepat **30 file fisik unik** tanpa ada file artifisial atau file kosong.
- **Distribusi Status**: **60 KUK VERIFIED** dengan bukti empiris langsung, dan **3 KUK PARTIALLY_VERIFIED** yang secara jujur diungkapkan memerlukan data/tanda tangan klien korporat eksternal jika diterapkan dalam konteks industri nyata.

### Rekapitulasi Status Bukti Kerja

| Kategori Status | Definisi | Jumlah KUK | Persentase |
|:---|:---|:---:|:---:|
| **VERIFIED** | Bukti empiris lengkap, dapat direproduksi, tervalidasi dengan kode/artefak nyata | 60 | 95.2% |
| **PARTIALLY VERIFIED** | Bukti didukung simulasi metodologis internal; pengesahan eksternal klien diungkapkan terbuka | 3 | 4.8% |
| **MISSING** | Bukti belum dibuat atau tidak ditemukan di repositori | 0 | 0.0% |
| **TOTAL** | **SELURUH KRITERIA UNJUK KERJA SKKNI 299/2020** | **63** | **100.0%** |

---

## 2. Audit 4-Dimensi Bukti Kerja Per Unit Kompetensi

### [UK-01] Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
- **Audit Status**: **VERIFIED WITH PROXY DISCLOSURE (9 Verified, 3 Partial)**
- **Evidence of Process**: Perumusan problem statement keterlambatan pengiriman Olist, cost-benefit laptop 8GB, failure register F-01 s.d. F-06.
- **Evidence of Result**: Dokumen Project Framing, target metrik bisnis (reduksi delay 15%), spesifikasi hardware.
- **Evidence of Validation**: Stress test test_data_pipeline_stress.py memastikan konsumsi memori < 4.5 GB RAM.
- **Evidence of Explanation**: KUK 2.2, 3.3, 4.3 disahkan via persona bisnis logistik internal karena sifat data sekunder publik.

### [UK-02] Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Penetapan task Supervised Classification (is_delayed_carrier) dan Survival Analysis.
- **Evidence of Result**: Threshold evaluasi teknis terukur: PR-AUC >= 0.70, ECE <= 0.05, latensi <= 20ms.
- **Evidence of Validation**: Uji otomatis test_models.py memverifikasi batas ambang performa teknis.
- **Evidence of Explanation**: Task klasifikasi biner dipilih karena keputusan operasional memerlukan probabilitas risiko delay.

### [UK-03] Menelaah Data (`J.62DMI00.005.1`)
- **Audit Status**: **VERIFIED (8/8)**
- **Evidence of Process**: Profiling 13 tabel Parquet, statistika deskriptif, downcasting memori, dan formulasi hipotesis.
- **Evidence of Result**: Visualisasi distribusi keterlambatan dan 5 hipotesis empiris (H1-H5) diuji formal.
- **Evidence of Validation**: Uji hipotesis statistik test_hypotheses.py menggunakan Welch t-test dan Mann-Whitney U.
- **Evidence of Explanation**: Skewness ekstrem jarak dan berat diidentifikasi untuk perlakuan penskalaan khusus.

### [UK-04] Memvalidasi Data (`J.62DMI00.006.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Pengecekan null-rate, integritas schema referensial Foreign Key, dan kecukupan data.
- **Evidence of Result**: Laporan kualitas data pada data/data_dictionary.md dan objek ValidationResult.
- **Evidence of Validation**: Uji pytest test_data_validation.py mengeksekusi validasi schema dan tanggal kronologis.
- **Evidence of Explanation**: Pesanan tanpa tanggal kurir disingkirkan untuk menghindari bias pelabelan.

### [UK-05] Menentukan Objek Data (`J.62DMI00.007.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Seleksi kohort pesanan berstatus delivered dan penentuan grain entitas pesanan (order_id).
- **Evidence of Result**: Dataset terpilih 96.470 baris pesanan bebas duplikasi pada order_level.parquet.
- **Evidence of Validation**: Uji test_cleaning_and_grain.py memastikan order_id unik 100%.
- **Evidence of Explanation**: Eksklusi pesanan non-delivered mencegah kebocoran informasi masa depan.

### [UK-06] Membersihkan Data (`J.62DMI00.008.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Pipeline pembersihan terprogram: deduplikasi geolokasi spasial dan imputasi median.
- **Evidence of Result**: Kompresi 1.000.163 baris koordinat menjadi 19.010 prefix unik (-98.1%) di data/interim/.
- **Evidence of Validation**: Uji test_cleaning_and_grain.py memverifikasi integritas referensial data bersih.
- **Evidence of Explanation**: Deduplikasi per prefix kode pos menghemat 98% memori tanpa kehilangan presisi jarak.

### [UK-07] Mengkonstruksi Data (`J.62DMI00.009.1`)
- **Audit Status**: **VERIFIED (6/6)**
- **Evidence of Process**: Rekayasa 41 fitur analitik domain (vektorisasi Haversine, rasio freight, approval delay).
- **Evidence of Result**: Dataset order_level.parquet dengan 41 fitur domain dan feature_availability_matrix.csv.
- **Evidence of Validation**: Uji test_feature_leakage.py membuktikan korelasi fitur terhadap target masa depan = 0.00.
- **Evidence of Explanation**: Pemisahan ketersediaan fitur berdasarkan timestamp mencegah kebocoran lookahead.

### [UK-08] Membangun Skenario Model (`J.62DMI00.012.1`)
- **Audit Status**: **VERIFIED (7/7)**
- **Evidence of Process**: Perancangan skenario partisi temporal (Purged Temporal Split April 2018) dan taksonomi B0-B3.
- **Evidence of Result**: Matriks perbandingan model dan spesifikasi arsitektur LightGBM / MLP / BiLSTM.
- **Evidence of Validation**: Uji test_models.py mengevaluasi skenario temporal out-of-time secara ketat.
- **Evidence of Explanation**: Temporal holdout split mensimulasikan penerapan masa depan lebih realistis dibanding K-Fold acak.

### [UK-09] Membangun Model (`J.62DMI00.013.1`)
- **Audit Status**: **VERIFIED (6/6)**
- **Evidence of Process**: Eksekusi pipeline pelatihan terintegrasi Scikit-Learn dan kalibrasi Isotonic probabilitas.
- **Evidence of Result**: Model terlatih best_delivery_delay_lightgbm.joblib dan log parameter eksperimen.
- **Evidence of Validation**: Uji test_models.py mengonfirmasi model terlatih mengalahkan baseline B0.
- **Evidence of Explanation**: Kalibrasi Isotonic menurunkan ECE secara dramatis dari 0.2355 menjadi 0.0070.

### [UK-10] Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Evaluasi model pada partisi out-of-time (n=24.120 pesanan) dan atribusi fitur SHAP.
- **Evidence of Result**: Laporan model_evaluation_and_review_report.md: PR-AUC 0.74, ROC-AUC 0.81, Brier 0.06.
- **Evidence of Validation**: Uji test_models.py memverifikasi PR-AUC out-of-time >= 0.70.
- **Evidence of Explanation**: Model terbukti stabil lintas waktu dan fitur jarak/ongkir mendominasi atribusi SHAP.

### [UK-11] Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)
- **Audit Status**: **VERIFIED (4/4)**
- **Evidence of Process**: Review kesesuaian siklus CRISP-DM, failure register governance, dan batasan klaim L0-L1.
- **Evidence of Result**: Dokumen FINAL_CSIP_AUDIT_REPORT.md dan failure_register.md mencatat 6 failure modes.
- **Evidence of Validation**: Uji test_skkni_consistency.py memverifikasi 100% kepatuhan standar dan dokumen.
- **Evidence of Explanation**: Review menyeluruh menjamin transparansi keterbatasan model sebelum rekomendasi disajikan.
