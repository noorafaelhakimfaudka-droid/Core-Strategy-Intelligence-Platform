# PANDUAN ASESOR & BANK PERTANYAAN TEKNIS DEFENSE (63 KUK)
## Verifikasi Portofolio Berbasis Bukti Kerja Nyata (Evidence-Based Assessment)
### Skema Sertifikasi: Ilmuwan Data (Data Scientist) — LSP TRI | SKM/2905/LSP-TRI/VII/2025
### Standar: SKKNI No. 299 Tahun 2020 (11 Unit Kompetensi, 27 Elemen, 63 KUK)

---

## 1. Petunjuk Teknis untuk Asesor Kompetensi
Dokumen ini memuat panduan pengujian komprehensif bagi Asesor Kompetensi SKKNI pada skema Ilmuwan Data.
Setiap Kriteria Unjuk Kerja (KUK) diuji melalui tiga modalitas pembuktian:
1. **Inspeksi Artefak Fisik**: Verifikasi keberadaan file kode, notebook, model serialisasi, atau laporan di disk.
2. **Uji Praktik / Demonstrasi Langsung**: Tugas teknis langsung yang diminta asesor kepada asesi di terminal/IDE.
3. **Wawancara & Uji Lisan**: Pertanyaan konseptual mendalam, follow-up probe, dan identifikasi jebakan jawaban lemah.

---

## 2. Rincian Instrumen Asesmen Per Unit Kompetensi & 63 KUK

### UK-01: J.62DMI00.001.1 — Menentukan Objektif Bisnis
- **Jumlah Elemen**: 4 Elemen | **Jumlah KUK**: 12 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menentukan objektif bisnis dari proyek data science.
**Aspek Kritis**: Ketepatan dalam mengidentifikasi permasalahan bisnis dan menetapkan metrik kesuksesan yang terukur serta realistis.

#### Elemen E1: Menentukan permasalahan bisnis dan poin-poin objektif bisnis proyek data science dari sisi pengguna akhir

##### KUK 1.1: Latar belakang dan permasalahan bisnis untuk proyek data science diidentifikasi sesuai dengan prosedur bisnis yang berlaku.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `notebooks/01_business_and_data_understanding.ipynb`
- **Aktivitas Proyek**: Identifikasi latar belakang dan masalah bisnis keterlambatan pengiriman e-commerce Olist (8.0% pesanan terlambat, menurunkan rating dari 4.14 menjadi 2.15).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `notebooks/01_business_and_data_understanding.ipynb` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Latar belakang dan permasalahan bisnis untuk proyek data science diidentifikasi sesuai dengan prosedur bisnis yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `notebooks/01_business_and_data_understanding.ipynb`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Poin-poin objektif bisnis diidentifikasi sesuai dengan permasalahan yang telah dipilih dan sesuai dengan kebutuhan organisasi.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `README.md`
- **Aktivitas Proyek**: Identifikasi poin objektif bisnis: menurunkan churn pelanggan dan mitigasi reputasi merchant melalui peringatan dini risiko keterlambatan pengiriman.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `README.md` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Poin-poin objektif bisnis diidentifikasi sesuai dengan permasalahan yang telah dipilih dan sesuai dengan kebutuhan organisasi.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `README.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.3: Poin-poin metrik kesuksesan dibuat sesuai objektif bisnis.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Penyusunan poin metrik kesuksesan bisnis: reduksi pesanan terlambat tanpa mitigasi sebesar min 15% dan precision intervensi > 70%.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 1.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Poin-poin metrik kesuksesan dibuat sesuai objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.4: Permasalahan bisnis, poin-poin objektif bisnis dan metrik kesuksesan proyek data science ditetapkan sesuai kebutuhan pengguna.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/research_traceability_matrix.md`
- **Aktivitas Proyek**: Penetapan formal permasalahan bisnis, objektif bisnis, dan metrik kesuksesan proyek dalam dokumen spesifikasi sistem.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/research_traceability_matrix.md` dan mendemonstrasikan logika pemenuhan KUK 1.4.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Permasalahan bisnis, poin-poin objektif bisnis dan metrik kesuksesan proyek data science ditetapkan sesuai kebutuhan pengguna.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/research_traceability_matrix.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Membuat daftar terminologi, sumber daya, kebutuhan, asumsi dan batasan

##### KUK 2.1: Daftar terminologi, sumber daya, kebutuhan, asumsi dan batasan proyek diidentifikasi.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `data/data_dictionary.md`
- **Aktivitas Proyek**: Identifikasi daftar terminologi (estimated delivery date, carrier dispatch, freight ratio), sumber daya komputasi laptop 8GB RAM, kebutuhan, asumsi, dan batasan operasional.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `data/data_dictionary.md` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Daftar terminologi, sumber daya, kebutuhan, asumsi dan batasan proyek diidentifikasi.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `data/data_dictionary.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Persetujuan atas kebutuhan, asumsi dan batasan proyek diperoleh dari pengguna.
- **Status Verifikasi Portofolio**: `EXTERNAL_CONFIRMATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Persetujuan formal kebutuhan, asumsi, dan batasan proyek disimulasikan melalui Project Framing Rubric dan User Persona Sign-off Protocol.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Persetujuan atas kebutuhan, asumsi dan batasan proyek diperoleh dari pengguna.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E3: Mengidentifikasi risiko dan alternatif pelaksanaan

##### KUK 3.1: Daftar risiko dalam pelaksanaan proyek diidentifikasi.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/evidence_and_failure_register.md`
- **Aktivitas Proyek**: Identifikasi daftar risiko proyek: risiko ketidakseimbangan kelas (imbalance 8%), kebocoran target masa depan (data leakage), dan pergeseran distribusi waktu (temporal drift).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/evidence_and_failure_register.md` dan mendemonstrasikan logika pemenuhan KUK 3.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Daftar risiko dalam pelaksanaan proyek diidentifikasi.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/evidence_and_failure_register.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.2: Beberapa rencana mitigasi risiko diidentifikasi sesuai dengan daftar risiko.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `src/csip/cleaning/cleaner.py`
- **Aktivitas Proyek**: Penyusunan rencana mitigasi: isolasi temporal split, stratified sampling, kalibrasi probabilitas, dan uji zero correlation terhadap kejadian masa depan.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 3.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Beberapa rencana mitigasi risiko diidentifikasi sesuai dengan daftar risiko.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.3: Persetujuan atas risiko dan rencana mitigasi risiko diperoleh dari pengguna.
- **Status Verifikasi Portofolio**: `EXTERNAL_CONFIRMATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/research_traceability_matrix.md`
- **Aktivitas Proyek**: Persetujuan risiko dan mitigasi dicatat dalam matriks tata kelola risiko dengan persetujuan proxy lead data scientist.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/research_traceability_matrix.md` dan mendemonstrasikan logika pemenuhan KUK 3.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Persetujuan atas risiko dan rencana mitigasi risiko diperoleh dari pengguna.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/research_traceability_matrix.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E4: Menentukan biaya dan keuntungan

##### KUK 4.1: Komponen biaya dan besaran biaya pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `tests/test_data_pipeline_stress.py`
- **Aktivitas Proyek**: Identifikasi komponen biaya pelaksanaan: konsumsi RAM laptop (<= 4.5GB), CPU execution time (<= 60s per training), dan storage footprint (< 100MB Parquet).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `tests/test_data_pipeline_stress.py` dan mendemonstrasikan logika pemenuhan KUK 4.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Komponen biaya dan besaran biaya pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `tests/test_data_pipeline_stress.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 4.2: Keuntungan pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `notebooks/11_alternative_world_simulation.ipynb`
- **Aktivitas Proyek**: Identifikasi keuntungan bisnis pelaksanaan proyek: estimasi penyelamatan 1.200 pesanan per kuartal dan penghematan biaya kompensasi logistik via counterfactual simulation.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `notebooks/11_alternative_world_simulation.ipynb` dan mendemonstrasikan logika pemenuhan KUK 4.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Keuntungan pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `notebooks/11_alternative_world_simulation.ipynb`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 4.3: Biaya dan keuntungan pelaksanaan proyek dikomunikasikan dan disetujui oleh pengguna.
- **Status Verifikasi Portofolio**: `EXTERNAL_CONFIRMATION_REQUIRED`
- **Artefak Bukti Utama**: `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`
- **Aktivitas Proyek**: Komunikasi komponen biaya dan keuntungan proyek dituangkan dalam laporan eksekutif dan slide presentasi teknis.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` dan mendemonstrasikan logika pemenuhan KUK 4.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Biaya dan keuntungan pelaksanaan proyek dikomunikasikan dan disetujui oleh pengguna.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-02: J.62DMI00.002.1 — Menentukan Tujuan Teknis Data Science
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menentukan tujuan teknis data science.
**Aspek Kritis**: Kesesuaian task data science dengan objektif bisnis dan penetapan threshold metrik teknis yang terjustifikasi.

#### Elemen E1: Menyusun tujuan teknis data science

##### KUK 1.1: Task data science ditentukan sesuai dengan objektif bisnis.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `notebooks/01_business_and_data_understanding.ipynb`
- **Aktivitas Proyek**: Penentuan task data science: Supervised Binary Classification (memprediksi is_delayed_carrier pada saat dispatch) dan Survival Time Analysis.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `notebooks/01_business_and_data_understanding.ipynb` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Task data science ditentukan sesuai dengan objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `notebooks/01_business_and_data_understanding.ipynb`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Tujuan teknis pelaksanaan proyek data science diidentifikasi sesuai objektif bisnis.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `config/models.yaml`
- **Aktivitas Proyek**: Identifikasi tujuan teknis: menghasilkan estimasi probabilitas keterlambatan terkalibrasi dengan threshold toleransi false positive terkendali.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/models.yaml` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Tujuan teknis pelaksanaan proyek data science diidentifikasi sesuai objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/models.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menentukan kriteria kesuksesan tujuan teknis proyek data science

##### KUK 2.1: Daftar dan parameter kriteria kesuksesan proyek diidentifikasi sesuai dengan tujuan teknis.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `config/models.yaml`
- **Aktivitas Proyek**: Identifikasi parameter kriteria kesuksesan teknis: PR-AUC >= 0.70, ROC-AUC >= 0.80, Brier Score <= 0.08, Expected Calibration Error (ECE) <= 0.05, latensi inferensi <= 20ms.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/models.yaml` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Daftar dan parameter kriteria kesuksesan proyek diidentifikasi sesuai dengan tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/models.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Kriteria yang teridentifikasi disetujui oleh pengguna sesuai dengan objektif bisnis.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Persetujuan kriteria kesuksesan teknis disahkan dalam dokumen spesifikasi model dan diverifikasi terhadap baseline pembanding.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Kriteria yang teridentifikasi disetujui oleh pengguna sesuai dengan objektif bisnis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-03: J.62DMI00.005.1 — Menelaah Data
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 8 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menelaah data untuk data science.
**Aspek Kritis**: Kecermatan analisis distribusi statistik dan kebenaran perumusan hipotesis alternatif.

#### Elemen E1: Menganalisis tipe dan relasi data

##### KUK 1.1: Tipe data yang terkumpul diidentifikasi sesuai tujuan teknis.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `src/csip/data/loader.py`
- **Aktivitas Proyek**: Identifikasi tipe data (numerik kontinu, diskrit, kategorikal, temporal datetime, geospasial koordinat) dari 9 tabel Olist terhimpun.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/data/loader.py` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Tipe data yang terkumpul diidentifikasi sesuai tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/data/loader.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Nilai atribut data yang terkumpul diuraikan sesuai dengan batasan konteks bisnisnya.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `data/data_dictionary.md`
- **Aktivitas Proyek**: Uraian nilai atribut data (status pesanan, dimensi produk, durasi pengiriman) berdasarkan batasan konteks bisnis e-commerce Brasil.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `data/data_dictionary.md` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Nilai atribut data yang terkumpul diuraikan sesuai dengan batasan konteks bisnisnya.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `data/data_dictionary.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.3: Relasi antar data yang terkumpul diidentifikasi sesuai dengan tujuan teknis.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/data/loader.py`
- **Aktivitas Proyek**: Identifikasi relasi antar tabel (customer-order-items-payments-reviews-geolocation) dan penentuan grain entitas pesanan (order_id).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/data/loader.py` dan mendemonstrasikan logika pemenuhan KUK 1.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Relasi antar data yang terkumpul diidentifikasi sesuai dengan tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/data/loader.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menganalisis karakteristik data

##### KUK 2.1: Karakteristik data yang terkumpul disajikan dengan deskripsi statistik dasar.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `notebooks/03_exploratory_data_analysis.ipynb`
- **Aktivitas Proyek**: Penyajian karakteristik data dengan deskripsi statistik dasar (mean, std, median, skewness, missing rate, zero count).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `notebooks/03_exploratory_data_analysis.ipynb` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Karakteristik data yang terkumpul disajikan dengan deskripsi statistik dasar.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `notebooks/03_exploratory_data_analysis.ipynb`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Karakteristik data yang terkumpul disajikan dengan visualisasi grafik.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `app/components/charts.py`
- **Aktivitas Proyek**: Visualisasi karakteristik data menggunakan grafik (histogram keterlambatan, scatter geospasial rute pengiriman, matriks korelasi).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `app/components/charts.py` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Karakteristik data yang terkumpul disajikan dengan visualisasi grafik.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `app/components/charts.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.3: Hasil penyajian data dianalisis karakteristiknya untuk telaah data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Analisis karakteristik data untuk telaah: deteksi heavy-tail keterlambatan ekstrem dan multikolinearitas antar dimensi produk.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 2.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hasil penyajian data dianalisis karakteristiknya untuk telaah data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E3: Membuat laporan telaah data

##### KUK 3.1: Hasil analisis didokumentasikan dalam bentuk laporan sesuai dengan tujuan teknis.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`
- **Aktivitas Proyek**: Dokumentasi hasil analisis telaah data ke dalam laporan teknis telaah data komprehensif.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` dan mendemonstrasikan logika pemenuhan KUK 3.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hasil analisis didokumentasikan dalam bentuk laporan sesuai dengan tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.2: Hipotesis disusun berdasar hasil analisis sesuai tujuan teknis data science.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `src/csip/hypotheses/runner.py`
- **Aktivitas Proyek**: Penyusunan 5 hipotesis empiris (H1-H5) berdasarkan telaah data (korelasi jarak spasial, rasio ongkir, waktu approval, volume rute).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/hypotheses/runner.py` dan mendemonstrasikan logika pemenuhan KUK 3.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hipotesis disusun berdasar hasil analisis sesuai tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/hypotheses/runner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-04: J.62DMI00.006.1 — Memvalidasi Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam memvalidasi data untuk data science.
**Aspek Kritis**: Validasi integritas data primer/asing dan formulasi rekomendasi tindakan data engineering.

#### Elemen E1: Melakukan pengecekan kelengkapan data

##### KUK 1.1: Penilaian kualitas data dari hasil telaah disajikan sesuai tujuan teknis data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `tests/test_data_validation.py`
- **Aktivitas Proyek**: Penilaian kualitas data dari hasil telaah: missingness pattern, duplikasi geolokasi, dan validitas rentang tanggal pesanan.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `tests/test_data_validation.py` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Penilaian kualitas data dari hasil telaah disajikan sesuai tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `tests/test_data_validation.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Penilaian tingkat kecukupan data dari hasil telaah disajikan sesuai tujuan teknis data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/data/loader.py`
- **Aktivitas Proyek**: Penilaian tingkat kecukupan data: verifikasi jumlah sampel (96.478 pesanan delivered, >99.000 order items) cukup untuk estimasi parameter ML stabil.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/data/loader.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Penilaian tingkat kecukupan data dari hasil telaah disajikan sesuai tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/data/loader.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Membuat rekomendasi kelengkapan data

##### KUK 2.1: Rekomendasi hasil penilaian kualitas disusun sesuai tujuan teknis data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/cleaning/cleaner.py`
- **Aktivitas Proyek**: Penyusunan rekomendasi perbaikan kualitas data: deduplikasi koordinat geolokasi per ZIP code prefix dan penanganan nilai null berat produk.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Rekomendasi hasil penilaian kualitas disusun sesuai tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Rekomendasi hasil penilaian kecukupan data disusun sesuai tujuan teknis data science.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Penyusunan rekomendasi kecukupan data: isolasi cohort pesanan delivered 2017-2018 untuk menjamin konsistensi siklus pengiriman penuh.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Rekomendasi hasil penilaian kecukupan data disusun sesuai tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-05: J.62DMI00.007.1 — Menentukan Objek Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam memilah dan memilih data yang sesuai permintaan atau kebutuhan.
**Aspek Kritis**: Ketepatan kriteria inklusi/eksklusi agar tidak menimbulkan selection bias atau survivorship bias.

#### Elemen E1: Memutuskan kriteria dan teknik pemilihan data

##### KUK 1.1: Kriteria pemilihan data diidentifikasi sesuai dengan tujuan teknis dan aturan yang berlaku.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `notebooks/01_business_and_data_understanding.ipynb`
- **Aktivitas Proyek**: Identifikasi kriteria pemilihan data: hanya pesanan dengan status 'delivered' dan memiliki tanggal dispatch valid (shipped to carrier).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `notebooks/01_business_and_data_understanding.ipynb` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Kriteria pemilihan data diidentifikasi sesuai dengan tujuan teknis dan aturan yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `notebooks/01_business_and_data_understanding.ipynb`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Teknik pemilihan data ditetapkan sesuai dengan kriteria pemilihan data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/cleaning/cleaner.py`
- **Aktivitas Proyek**: Penetapan teknik pemilihan data: SQL/Pandas filtering berbasis masker logika konsisten pada grain pesanan tingkat satu baris.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Teknik pemilihan data ditetapkan sesuai dengan kriteria pemilihan data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menentukan attributes (kolom) dan records (baris) data

##### KUK 2.1: Attributes (kolom) data diidentifikasi sesuai dengan kriteria pemilihan data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `config/features.yaml`
- **Aktivitas Proyek**: Identifikasi attributes (kolom) prediktor yang diizinkan tersedia pada saat dispatch untuk mencegah lookahead leakage.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/features.yaml` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Attributes (kolom) data diidentifikasi sesuai dengan kriteria pemilihan data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/features.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Records (baris) data diidentifikasi sesuai dengan kriteria pemilihan data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `tests/test_cleaning_and_grain.py`
- **Aktivitas Proyek**: Identifikasi records (baris) data: 96.478 baris pesanan terpilih yang memenuhi kriteria kelengkapan data primer.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `tests/test_cleaning_and_grain.py` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Records (baris) data diidentifikasi sesuai dengan kriteria pemilihan data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `tests/test_cleaning_and_grain.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-06: J.62DMI00.008.1 — Membersihkan Data
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membersihkan data yang sesuai permintaan atau kebutuhan.
**Aspek Kritis**: Kerapian eksekusi pembersihan terprogram dan ketiadaan data leakage saat imputasi train-test.

#### Elemen E1: Melakukan pembersihan data yang kotor

##### KUK 1.1: Strategi pembersihan data ditentukan berdasarkan hasil telaah data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/cleaning/auto_cleaner.py`
- **Aktivitas Proyek**: Penentuan strategi pembersihan data: median spatial aggregation untuk tabel geolokasi dan median imputation untuk dimensi barang.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/auto_cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Strategi pembersihan data ditentukan berdasarkan hasil telaah data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/auto_cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Data yang kotor dikoreksi berdasarkan strategi pembersihan data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/cleaning/cleaner.py`
- **Aktivitas Proyek**: Koreksi data kotor: kompresi 1.000.163 baris koordinat kotor menjadi 19.015 prefix unik (-98.1%) dan imputasi dimensi produk.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Data yang kotor dikoreksi berdasarkan strategi pembersihan data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Membuat laporan dan rekomendasi hasil membersihkan data

##### KUK 2.1: Masalah dan teknis koreksi data dideskripsikan sesuai dengan kondisi data dan strategi pembersihan data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/cleaning/cleaner.py`
- **Aktivitas Proyek**: Deskripsi masalah data kotor dan teknis koreksinya dituangkan dalam CleaningStepReport terstruktur.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/cleaning/cleaner.py` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Masalah dan teknis koreksi data dideskripsikan sesuai dengan kondisi data dan strategi pembersihan data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/cleaning/cleaner.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Evaluasi dihasilkan berdasarkan analisis data yang telah dibersihkan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `tests/test_cleaning_and_grain.py`
- **Aktivitas Proyek**: Evaluasi hasil pembersihan data: verifikasi integritas referensial 100% lolos, null rate 0.00% pada primary key.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `tests/test_cleaning_and_grain.py` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Evaluasi dihasilkan berdasarkan analisis data yang telah dibersihkan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `tests/test_cleaning_and_grain.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-07: J.62DMI00.009.1 — Mengkonstruksi Data
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 6 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam mengkonstruksi data untuk proyek data science.
**Aspek Kritis**: Kreativitas rekayasa fitur domain dan penegakan isolasi temporal bebas target leakage.

#### Elemen E1: Menganalisis teknik transformasi data

##### KUK 1.1: Analisis data untuk menentukan representasi fitur data awal dilakukan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `config/features.yaml`
- **Aktivitas Proyek**: Analisis data untuk representasi fitur awal: identifikasi fitur mentah tanggal pembelian, koordinat lintang/bujur, harga, dan ongkir.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/features.yaml` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Analisis data untuk menentukan representasi fitur data awal dilakukan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/features.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Analisis representasi fitur data awal untuk menentukan teknik rekayasa fitur yang diperlukan untuk pembangunan model data science dilakukan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/features/engineer.py`
- **Aktivitas Proyek**: Analisis representasi fitur awal untuk menentukan teknik rekayasa fitur: rumus Haversine, rasio freight/price, dan jeda approval.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/features/engineer.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Analisis representasi fitur data awal untuk menentukan teknik rekayasa fitur yang diperlukan untuk pembangunan model data science dilakukan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/features/engineer.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Melakukan transformasi data

##### KUK 2.1: Transformasi dilakukan untuk mendapatkan fitur data awal.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/features/builder.py`
- **Aktivitas Proyek**: Eksekusi transformasi fitur data awal: konversi datetime string menjadi timestamp dan ekstrasi komponen waktu.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/features/builder.py` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Transformasi dilakukan untuk mendapatkan fitur data awal.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/features/builder.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Rekayasa fitur data dilakukan untuk mendapatkan fitur baru yang diperlukan untuk pembangunan model data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/features/engineer.py`
- **Aktivitas Proyek**: Rekayasa fitur baru: pembentukan 41 fitur analitik domain (distance_seller_customer_km, freight_ratio, approval_delay_hours, route_traffic_density).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/features/engineer.py` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Rekayasa fitur data dilakukan untuk mendapatkan fitur baru yang diperlukan untuk pembangunan model data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/features/engineer.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E3: Membuat dokumentasi konstruksi data

##### KUK 3.1: Teknis transformasi data dijabarkan dalam bentuk tertulis.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/modeling/feature_availability_matrix.csv`
- **Aktivitas Proyek**: Dokumentasi tertulis langkah teknis transformasi data dan kamus rumus rekayasa fitur.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/modeling/feature_availability_matrix.csv` dan mendemonstrasikan logika pemenuhan KUK 3.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Teknis transformasi data dijabarkan dalam bentuk tertulis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/modeling/feature_availability_matrix.csv`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.2: Hasil transformasi data dan rekomendasi hasil transformasi dituangkan dalam bentuk tertulis.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Penuangan hasil transformasi data dan rekomendasi teknis penggunaan fitur ke dalam laporan pemodelan.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 3.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hasil transformasi data dan rekomendasi hasil transformasi dituangkan dalam bentuk tertulis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-08: J.62DMI00.012.1 — Membangun Skenario Model
- **Jumlah Elemen**: 3 Elemen | **Jumlah KUK**: 7 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membangun skenario model.
**Aspek Kritis**: Ketepatan penyusunan skenario pengujian out-of-time (purged temporal split) yang mencegah lookahead bias.

#### Elemen E1: Mengidentifikasi teknik pemodelan

##### KUK 1.1: Asumsi-asumsi spesifik mengenai data diidentifikasi sesuai karakteristik data.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/research_traceability_matrix.md`
- **Aktivitas Proyek**: Identifikasi asumsi spesifik data: imbalansi kelas (8% delay), non-linearitas hubungan jarak-ongkir, dan non-stasioneritas musiman.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/research_traceability_matrix.md` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Asumsi-asumsi spesifik mengenai data diidentifikasi sesuai karakteristik data.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/research_traceability_matrix.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Teknik-teknik pemodelan data diidentifikasi sesuai karakteristik data dan tujuan teknis data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/models/trainer.py`
- **Aktivitas Proyek**: Identifikasi teknik pemodelan: Baseline Heuristik (B0), Logistic Regression teratur (B1), Random Forest (B2), LightGBM (B3), dan Deep MLP / BiLSTM.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/models/trainer.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Teknik-teknik pemodelan data diidentifikasi sesuai karakteristik data dan tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/models/trainer.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menentukan teknik pemodelan yang sesuai dengan karakteristik data dan tujuan teknis data science

##### KUK 2.1: Teknik pemodelan yang sesuai dengan karakteristik data ditentukan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/models/classic.py`
- **Aktivitas Proyek**: Penentuan teknik pemodelan: pemilihan LightGBM dengan CalibratedClassifierCV (Isotonic) sebagai kandidat utama berdasarkan karakteristik tabular berdimensi sedang.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/models/classic.py` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Teknik pemodelan yang sesuai dengan karakteristik data ditentukan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/models/classic.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Deskripsi teknik pemodelan yang dipilih didokumentasikan sesuai SOP yang berlaku.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`
- **Aktivitas Proyek**: Dokumentasi deskripsi teknik pemodelan yang dipilih dalam spesifikasi arsitektur model sesuai SOP.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Deskripsi teknik pemodelan yang dipilih didokumentasikan sesuai SOP yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E3: Menyiapkan skenario pengujian

##### KUK 3.1: Skenario uji yang mungkin diterapkan ditentukan sesuai tujuan teknis.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/models/trainer.py`
- **Aktivitas Proyek**: Penentuan skenario pengujian: partisi data temporal terpurifikasi (Purged Temporal Holdout) dengan cutoff April 2018 untuk mensimulasikan penerapan masa depan riil.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/models/trainer.py` dan mendemonstrasikan logika pemenuhan KUK 3.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Skenario uji yang mungkin diterapkan ditentukan sesuai tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/models/trainer.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.2: Metrik evaluasi pengujian diidentifikasi sesuai skenario uji.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `config/models.yaml`
- **Aktivitas Proyek**: Identifikasi metrik evaluasi pengujian: PR-AUC (metrik utama untuk data tidak seimbang), ROC-AUC, Brier Score, ECE, dan latensi inferensi.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/models.yaml` dan mendemonstrasikan logika pemenuhan KUK 3.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Metrik evaluasi pengujian diidentifikasi sesuai skenario uji.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/models.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 3.3: Skenario uji yang dipilih didokumentasikan sesuai standar yang berlaku.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/model_evaluation_and_review_report.md`
- **Aktivitas Proyek**: Dokumentasi skenario uji yang dipilih ke dalam matriks perbandingan model terstandar.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/model_evaluation_and_review_report.md` dan mendemonstrasikan logika pemenuhan KUK 3.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Skenario uji yang dipilih didokumentasikan sesuai standar yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/model_evaluation_and_review_report.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-09: J.62DMI00.013.1 — Membangun Model
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 6 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membangun model.
**Aspek Kritis**: Eksekusi pelatihan model yang ketat, pencegahan overfitting, dan pencatatan parameter eksperimen.

#### Elemen E1: Menyiapkan parameter model

##### KUK 1.1: Parameter-parameter yang sesuai dengan model diidentifikasi.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `config/models.yaml`
- **Aktivitas Proyek**: Identifikasi parameter-parameter model: n_estimators, max_depth, learning_rate, colsample_bytree, class_weight, dan regularisasi L1/L2.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/models.yaml` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Parameter-parameter yang sesuai dengan model diidentifikasi.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/models.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Nilai toleransi parameter evaluasi pengujian ditetapkan sesuai dengan tujuan teknis.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `config/models.yaml`
- **Aktivitas Proyek**: Penetapan nilai toleransi parameter evaluasi: PR-AUC min 0.70, drop performa out-of-time max 10%, dan ECE max 0.05.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `config/models.yaml` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Nilai toleransi parameter evaluasi pengujian ditetapkan sesuai dengan tujuan teknis.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `config/models.yaml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menggunakan tools pemodelan

##### KUK 2.1: Tools untuk membuat model diidentifikasi sesuai dengan tujuan teknis data science.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `pyproject.toml`
- **Aktivitas Proyek**: Identifikasi tools pemodelan: Scikit-Learn 1.3+, LightGBM 4.0+, PyTorch 2.0+, Joblib 1.3+.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `pyproject.toml` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Tools untuk membuat model diidentifikasi sesuai dengan tujuan teknis data science.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `pyproject.toml`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Algoritma untuk teknik pemodelan yang ditentukan dibangun menggunakan tools yang dipilih.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/models/classic.py`
- **Aktivitas Proyek**: Pembangunan algoritma pemodelan menggunakan tools terpilih via Scikit-Learn Pipeline terintegrasi.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/models/classic.py` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Algoritma untuk teknik pemodelan yang ditentukan dibangun menggunakan tools yang dipilih.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/models/classic.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.3: Algoritma pemodelan dieksekusi sesuai dengan skenario pengujian dan tools untuk membuat model yang telah ditetapkan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `scripts/run_ml_experiments.py`
- **Aktivitas Proyek**: Eksekusi algoritma pemodelan sesuai skenario pengujian temporal split dan tools yang ditetapkan.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `scripts/run_ml_experiments.py` dan mendemonstrasikan logika pemenuhan KUK 2.3.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Algoritma pemodelan dieksekusi sesuai dengan skenario pengujian dan tools untuk membuat model yang telah ditetapkan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `scripts/run_ml_experiments.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.4: Parameter model algoritma dioptimasi untuk menghasilkan nilai parameter evaluasi yang sesuai dengan skenario pengujian.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `src/csip/models/trainer.py`
- **Aktivitas Proyek**: Optimasi parameter model algoritma melalui RandomizedSearch cross-validated dan kalibrasi probabilitas Isotonic.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `src/csip/models/trainer.py` dan mendemonstrasikan logika pemenuhan KUK 2.4.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Parameter model algoritma dioptimasi untuk menghasilkan nilai parameter evaluasi yang sesuai dengan skenario pengujian.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `src/csip/models/trainer.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-10: J.62DMI00.014.1 — Mengevaluasi Hasil Pemodelan
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam mengevaluasi hasil pemodelan.
**Aspek Kritis**: Validitas empiris evaluasi tanpa kebocoran data uji dan interpretasi berbasis explainability.

#### Elemen E1: Menggunakan model dengan data riil

##### KUK 1.1: Data baru untuk evaluasi pemodelan dikumpulkan sesuai kebutuhan yang mengacu kepada parameter evaluasi.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `data/processed/order_level.parquet`
- **Aktivitas Proyek**: Pengumpulan data baru untuk evaluasi: himpunan data uji temporal out-of-time (pesanan setelah 1 April 2018, n=24.120 pesanan).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `data/processed/order_level.parquet` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Data baru untuk evaluasi pemodelan dikumpulkan sesuai kebutuhan yang mengacu kepada parameter evaluasi.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `data/processed/order_level.parquet`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Model diuji dengan menggunakan data riil yang telah dikumpulkan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `tests/test_models.py`
- **Aktivitas Proyek**: Pengujian model dengan menggunakan data riil out-of-time untuk mengukur generalisasi waktu nyata.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `tests/test_models.py` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Model diuji dengan menggunakan data riil yang telah dikumpulkan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `tests/test_models.py`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menilai hasil pemodelan

##### KUK 2.1: Keluaran pengujian model dinilai berdasarkan metrik kesuksesan.
- **Status Verifikasi Portofolio**: `VERIFIED`
- **Artefak Bukti Utama**: `reports/model_evaluation_and_review_report.md`
- **Aktivitas Proyek**: Penilaian keluaran pengujian berdasarkan metrik kesuksesan: PR-AUC 0.74 (memenuhi target >=0.70), ROC-AUC 0.81, Brier Score 0.06, ECE 0.038.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/model_evaluation_and_review_report.md` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Keluaran pengujian model dinilai berdasarkan metrik kesuksesan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/model_evaluation_and_review_report.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Hasil penilaian didokumentasikan sesuai standar yang berlaku.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`
- **Aktivitas Proyek**: Dokumentasi hasil penilaian pengujian model ke dalam format matriks komparasi dan laporan teknis.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hasil penilaian didokumentasikan sesuai standar yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

### UK-11: J.62DMI00.015.1 — Melakukan Proses Review Pemodelan
- **Jumlah Elemen**: 2 Elemen | **Jumlah KUK**: 4 KUK
**Deskripsi Unit**: Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam melakukan proses review pemodelan.
**Aspek Kritis**: Kejujuran ilmiah dalam mendokumentasikan kegagalan/keterbatasan model dan penentuan kelayakan deploy.

#### Elemen E1: Menilai kesesuaian proses pemodelan

##### KUK 1.1: Proses pemodelan diperiksa kesesuaiannya berdasarkan tahapan yang ditentukan.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/canonical_skkni_299_2020_mapping.md`
- **Aktivitas Proyek**: Pemeriksaan kesesuaian seluruh tahapan pemodelan berdasarkan metodologi CRISP-DM dan 11 Unit SKKNI 299/2020.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/canonical_skkni_299_2020_mapping.md` dan mendemonstrasikan logika pemenuhan KUK 1.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Proses pemodelan diperiksa kesesuaiannya berdasarkan tahapan yang ditentukan.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/canonical_skkni_299_2020_mapping.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 1.2: Tindak lanjut yang perlu diambil ditentukan berdasarkan hasil pengujian model hasil pemeriksaan kesesuaian.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `reports/evidence_and_failure_register.md`
- **Aktivitas Proyek**: Penentuan tindak lanjut berdasarkan hasil pengujian: kewajiban modul kalibrasi probabilitas karena model mentah mengalami overconfidence (F-02).
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/evidence_and_failure_register.md` dan mendemonstrasikan logika pemenuhan KUK 1.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Tindak lanjut yang perlu diambil ditentukan berdasarkan hasil pengujian model hasil pemeriksaan kesesuaian.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/evidence_and_failure_register.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

#### Elemen E2: Menilai kualitas proses pemodelan

##### KUK 2.1: Proses pemodelan dinilai berdasarkan rencana pelaksanaan proyek.
- **Status Verifikasi Portofolio**: `CANDIDATE_DEMONSTRATION_REQUIRED`
- **Artefak Bukti Utama**: `reports/research_traceability_matrix.md`
- **Aktivitas Proyek**: Penilaian proses pemodelan terhadap rencana pelaksanaan proyek: verifikasi kepatuhan batasan memori 8GB RAM, reproduktifitas seed 42, dan isolasi temporal.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `reports/research_traceability_matrix.md` dan mendemonstrasikan logika pemenuhan KUK 2.1.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Proses pemodelan dinilai berdasarkan rencana pelaksanaan proyek.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `reports/research_traceability_matrix.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.

##### KUK 2.2: Hasil penilaian didokumentasikan sesuai standard yang berlaku.
- **Status Verifikasi Portofolio**: `ARTIFACT_ONLY`
- **Artefak Bukti Utama**: `FINAL_CSIP_AUDIT_REPORT.md`
- **Aktivitas Proyek**: Dokumentasi hasil penilaian proses pemodelan, batasan klaim (Claim Level L0-L1), dan rekomendasi operasional.
- **Tugas Demonstrasi Praktik**: Asesor meminta asesi membuka `FINAL_CSIP_AUDIT_REPORT.md` dan mendemonstrasikan logika pemenuhan KUK 2.2.
- **Pertanyaan Inti Asesor**: *"Bagaimana Anda membuktikan pemenuhan kriteria 'Hasil penilaian didokumentasikan sesuai standard yang berlaku.' dalam proyek ini?"*
- **Penalaran Teknis yang Diharapkan (Asesi)**: Asesi menjelaskan implementasi konkret pada `FINAL_CSIP_AUDIT_REPORT.md`, metodologi yang diterapkan (misal: Split-Before-Transform, isolasi temporal, mitigasi overconfidence kalibrasi), serta batasan klaim ilmiah (Level L1/L2).
- **Pertanyaan Lanjutan (*Probe Question*)*: *"Apa konsekuensi ilmiah jika langkah pada KUK ini diabaikan atau menggunakan pendekatan naif?"*
- **Contoh Jawaban Lemah / Jebakan**: Memberikan jawaban hafalan teoritis tanpa merujuk ke data/kode riil, atau mengklaim hasil 100% sempurna tanpa mengungkapkan keterbatasan data observasional.
- **Tolok Ukur Jawaban Asesi Kompeten**: Mampu menunjukkan file di disk, menjelaskan alasan pemilihan metode, menyebutkan trade-off komputasi/akurasi, dan menyajikan hasil uji validasi yang dapat direproduksi.
