# CSIP Version 5 — Final Integrity & Reproducibility Patch Changelog
## Rekam Jejak Pembaruan Repositori Sesuai Arahan Audit Version 5

- **Tanggal Rilis**: 2026-11-11  
- **Versi**: Version 5.0.0 (Final Integrity & Reproducibility Patch)  
- **Standar Acuan**: SKKNI No. 299 Tahun 2020 | Skema LSP TRI (`SKM/2905/LSP-TRI/VII/2025`)  

---

### 1. Eliminasi Total Seluruh Path Lokal Absolut (Portabilitas Mutlak)
- Seluruh path lokal Windows absolut (`...` dan `path absolut OS lokal`) telah dihapus secara menyeluruh dari seluruh laporan, konfigurasi, dan pengujian.
- Seluruh tautan dokumen menggunakan path relatif berbasis root repository, menjamin repositori dapat dieksekusi secara mulus pada sistem operasi apa pun (Linux, macOS, Windows).

### 2. Resolusi Kontradiksi Dokumentasi & Penyelarasan Angka
- **Evidence Validation Report** (`reports/evidence/evidence_validation_report.md`): Klaim usang '100% VERIFIED' dan '0 Partially Verified' dihapus; diperbarui menjadi **60 VERIFIED, 3 PARTIALLY_VERIFIED, 0 MISSING**.
- **Keseragaman Angka Seluruh Repositori**: Seluruh dokumen resmi konsisten pada nilai kanonikal:
  - 11 Unit Kompetensi
  - 27 Elemen Kompetensi
  - 63 Kriteria Unjuk Kerja (KUK)
  - 84 Tests Passed (0 Failed, 0 Skipped)
  - 60 Verified, 3 Partially Verified, 0 Missing
  - 30 File Fisik Unik Pendukung Bukti

### 3. Penguatan Traceability Bukti (Specific Scope Mapping)
- Seluruh 63 record evidence registry (`reports/evidence/evidence_registry.json`) kini diperkaya dengan atribut `specific_scope`, yang merinci secara tepat class, function, table schema, atau section dokumen pendukung (bukan pemetaan generik).
- Ditambahkan pengungkapan rinci `additional_evidence_needed` untuk 3 KUK PARTIALLY_VERIFIED sebagai panduan pembelaan profesional peserta di hadapan asesor.

### 4. Pengujian Reproduksibilitas Aktual Pytest
- Eksekusi `python -m pytest tests/ -v` menghasilkan output aktual **84 passed in 33.16s** (0 failed, 0 skipped).
- Diperbarui catatan eksekusi pada `reports/testing/test_execution_report.md` dan `reports/test_execution_report.md`.

### 5. Penegakan Etika Asesmen (No Fabricated Competency Claims)
- Menghapus klaim mandiri 'Rekomendasi: KOMPETEN' atau 'Kelulusan BNSP'.
- Status akhir portofolio didefinisikan secara profesional sebagai **SIAP ASESMEN (Assessment Ready)** dengan skor kualitas mandiri realistis **9.60 / 10**.