# CSIP Automated Test Execution Log Reference

- **Single Source of Truth**: `reports/testing/pytest_actual.txt`
- **Standard**: SKKNI No. 299 Tahun 2020 | LSP TRI `SKM/2905/LSP-TRI/VII/2025`
- **Execution Mode**: Otomatis melalui `python -m pytest` / `make test`

Seluruh data pengujian (jumlah tes, modul, status lolos/gagal/lewati, dan durasi) dihasilkan secara deterministik dan dicatat langsung ke berkas log:
[`reports/testing/pytest_actual.txt`](pytest_actual.txt)

Dokumen ini tidak memuat angka hitungan tes manual guna mencegah desinkronisasi. Silakan merujuk langsung ke log keluaran aktual atau jalankan `make test`.
