# CSIP 1.0.0 Self-Assessment & Implementation Report

**Nama Proyek:** Core Strategy & Intelligence Platform (CSIP)  
**Versi Rilis:** `1.0.0`  
**Peran Dokumen:** Laporan mandiri pengembang dan ilmuwan data pelaksana (bukan hasil audit eksternal)  
**Skema Acuan:** LSP TRI `SKM/2905/LSP-TRI/VII/2025` / SKKNI 299/2020  
**Tanggal:** 11 November 2026  

---

## 1. Lingkup Implementasi yang Dikerjakan

Repositori ini mengimplementasikan platform data science lokal yang dapat diaudit untuk analisis perilaku e-commerce berbasis dataset Olist (2016–2018):

1. **Struktur Kompetensi Data Science (SKKNI 299/2020)**:
   - Pemetaan ke 11 Unit Kompetensi skema LSP TRI.
   - Pembedaan tegas level klaim: L0 (Deskriptif), L1 (Prediktif), L2 (Asosiasional), L3 (Kausal).
2. **Rekayasa & Integritas Data**:
   - Isolasi grain pesanan (96.470 pesanan bersih).
   - Penegakan kontrak data (`csip.data.contracts`) dan pelacakan silsilah data (`artifacts/lineage/DATA_LINEAGE.json`).
   - Penanganan sensor pasca-pengiriman dan isolasi temporal sebelum transformasi.
3. **Pemodelan & Evaluasi**:
   - Model keterlambatan pengiriman (`best_delivery_delay_lightgbm`).
   - Model ulasan negatif retrospektif (`best_negative_review_lightgbm`).
   - Model retensi pelanggan dengan pelaporan jujur atas keterbatasan daya prediktif.
   - Analisis disparitas geografis per negara bagian dengan interval kepercayaan terukur.
4. **Reproduksibilitas & Arsitektur Perangkat Lunak**:
   - Pipeline deterministik dengan seed tetap.
   - Metadata sidecar JSON mendokumentasikan dependensi runtime dan SHA-256 artefak.
   - Pengujian terotomasi pytest mencakup kontrak data, kebocoran fitur, kebocoran temporal, kalibrasi, dan integritas registri.

---

## 2. Ringkasan Eksekusi Pengujian Nyata

Seluruh hasil verifikasi perangkat lunak ditautkan langsung ke berkas log eksekusi nyata pada lingkungan runtime (`reports/testing/pytest_actual.txt`):

- **Suite Uji Otomatis:** Menguji integritas fungsional, ketahanan model, kepatuhan kontrak data, dan ketiadaan kebocoran temporal.
- **Validasi Artefak Model:** Verifikasi hash SHA-256 dan deserialisasi model biner (`tools/validate_model_artifact_registry.py`).
- **Validasi Konsistensi Dokumentasi:** Penegakan sinkronisasi versi dan konsistensi matriks penelusuran (`tools/validate_documentation_consistency.py`).

---

## 3. Bagian yang Belum Diverifikasi (Unverified Limitations)

Sebagai wujud integritas ilmiah dan pelaporan objektif, aspek-aspek berikut secara eksplisit dicatat sebagai **BELUM DIVERIFIKASI** atau berada di luar cakupan pembuktian mandiri:

1. **Elemen dan Teks KUK SKKNI 299/2020 terhadap Sumber Resmi:**
   - Halaman resmi LSP TRI (`lsptri.id/skema/sertifikasi-ilmuwan-data-SKKNI`) per tanggal verifikasi hanya memuat 11 kode dan judul unit kompetensi, nomor skema, jenjang KKNI 7, dan metode asesmen.
   - Rincian 27 elemen dan 63 KUK diturunkan dari struktur canonical internal proyek; verifikasi normatif resmi terhadap dokumen SKKNI 299/2020 berstatus **NOT VERIFIED** sampai dokumen fisik/resmi dari kementerian terkait dapat diakses.
2. **Persetujuan Pengguna / Pemangku Kepentingan Eksternal:**
   - KUK 2.2, 3.3, dan 4.3 pada UK-01 mensyaratkan persetujuan pengguna atas kebutuhan, risiko, dan biaya/manfaat.
   - Karena proyek ini menggunakan data sekunder historis publik, dokumen persetujuan pemangku kepentingan berstatus **Diusulkan oleh kandidat — persetujuan pengguna: BELUM DIPEROLEH** (`EXTERNAL_CONFIRMATION_REQUIRED`). Tidak ada tanda tangan atau persetujuan fiktif yang dibuat.
3. **Generalisasi ke Pasar / Periode Lain:**
   - Seluruh model dilatih dan dievaluasi pada data historis e-commerce Brasil periode 2016–2018. Performa pada konteks pasar modern atau geografi lain belum teruji.
4. **Model Risiko Ulasan Saat Checkout:**
   - Model risiko ulasan yang ada saat ini bersifat retrospektif (menggunakan status pengiriman akhir). CSIP belum memiliki model prediktif checkout-time murni untuk risiko ulasan pesanan yang belum dikirim.
5. **Penilaian Kelulusan Asesmen:**
   - Status kompetensi sepenuhnya merupakan wewenang asesor independen berlisensi otoritas profesi pada proses asesmen resmi offline.

