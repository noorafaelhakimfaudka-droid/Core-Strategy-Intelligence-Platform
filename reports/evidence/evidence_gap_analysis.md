# CSIP Evidence Gap Analysis & Defense Guide (Version 5)
## Skema Sertifikasi Okupasi Ilmuwan Data (Data Scientist) — KKNI Level 7

- **Standar Acuan**: SKKNI No. 299 Tahun 2020
- **Skema Sertifikasi**: LSP TRI (`SKM/2905/LSP-TRI/VII/2025`)
- **Ruang Lingkup**: 11 Unit Kompetensi, 27 Elemen, 63 KUK
- **Distribusi Bukti**: 60 VERIFIED, 3 PARTIALLY_VERIFIED, 0 MISSING
- **File Fisik Unik**: 30 file unik terverifikasi pada repositori
- **Prinsip Utama**: MAXIMUM EVIDENCE ACCURACY, ZERO FABRICATED CLAIMS

---

## 1. Rekapitulasi Metrik Bukti Kerja

- **Total Record Evidence**: **63 record** (memetakan 1-ke-1 seluruh 63 KUK resmi).
- **Total File Fisik Unik**: **30 file** (tidak ada file kosong / duplikat fiktif).
- **Total KUK Didukung**: **63 KUK (100%)**.
- **KUK Memerlukan Bukti Tambahan**: **3 KUK** (UK-01 KUK 2.2, 3.3, 4.3).

---

## 2. Rincian 3 KUK PARTIALLY_VERIFIED & Strategi Pembelaan di Hadapan Asesor

### 1. UK-01 KUK 2.2: Persetujuan atas kebutuhan, asumsi dan batasan proyek diperoleh dari pengguna
- **Status**: `PARTIALLY_VERIFIED`
- **File Bukti CSIP**: `reports/canonical_skkni_299_2020_mapping.md` (Section 2.1) & `README.md` (Section 1.2)
- **Aktivitas Peserta**: Menyusun Project Framing Rubric dan menetapkan batasan operasional (misal waktu cut-off dispatch kurir) berbasis parameter bisnis e-commerce Olist.
- **Kesenjangan Riil**: Tidak ada sponsor korporat eksternal yang menandatangani kontrak fisik karena proyek berbasis dataset publik terbuka Kaggle.
- **Bukti Tambahan yang Dibutuhkan di Industri**: Dokumen Statement of Work (SOW) atau Project Charter bertandatangan sponsor bisnis.
- **Panduan Pembelaan Asesmen**: Peserta menjelaskan bahwa dalam riset mandiri / portofolio data science, batasan didefinisikan secara eksplisit mengacu pada domain logistik Olist dan ditinjau menggunakan persona bisnis logistik internal.

### 2. UK-01 KUK 3.3: Persetujuan atas risiko dan rencana mitigasi risiko diperoleh dari pengguna
- **Status**: `PARTIALLY_VERIFIED`
- **File Bukti CSIP**: `reports/research_traceability_matrix.md` (Section 3) & `reports/evidence_and_failure_register.md` (Section 2)
- **Aktivitas Peserta**: Mengidentifikasi 6 risiko metodologis (F-01 s.d. F-06) dan menyusun mitigasi teknis (temporal split, kalibrasi probabilitas).
- **Kesenjangan Riil**: Pengesahan risiko dilakukan secara mandiri dan melalui peer review internal, bukan komite risiko korporat.
- **Bukti Tambahan yang Dibutuhkan di Industri**: Berita acara evaluasi risiko formal dari Risk & Compliance Officer.
- **Panduan Pembelaan Asesmen**: Peserta menunjukkan matriks risiko kegagalan teknis dan membuktikan bahwa mitigasi telah diuji secara otomatis via test_feature_leakage.py sebelum model di-fit.

### 3. UK-01 KUK 4.3: Biaya dan keuntungan pelaksanaan proyek dikomunikasikan dan disetujui oleh pengguna
- **Status**: `PARTIALLY_VERIFIED`
- **File Bukti CSIP**: `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` (Section 7.2) & `notebooks/11_alternative_world_simulation.ipynb` (Section 4)
- **Aktivitas Peserta**: Menghitung estimasi ROI penyelamatan 1.200 pesanan per kuartal via counterfactual simulation dan mendokumentasikannya dalam laporan eksekutif.
- **Kesenjangan Riil**: Tidak ada steering committee eksternal yang menandatangani alokasi anggaran komersial riil.
- **Bukti Tambahan yang Dibutuhkan di Industri**: Persetujuan alokasi anggaran belanja modal/operasional dari Board of Directors / Steering Committee.
- **Panduan Pembelaan Asesmen**: Peserta mempresentasikan kalkulasi cost-benefit kepada Asesor sebagaimana mempresentasikannya kepada dewan direksi.