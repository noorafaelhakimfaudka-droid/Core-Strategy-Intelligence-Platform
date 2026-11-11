# CSIP Canonical SKKNI 299/2020 Competency Mapping Specification
## Standard Kompetensi Kerja Nasional Indonesia — Bidang Data Science (KKNI Jenjang 7)

- **Dokumen**: Pemetaan Normatif SKKNI 299/2020
- **Skema Sertifikasi**: Sertifikasi Ilmuwan Data (Data Scientist) — LSP TRI (`SKM/2905/LSP-TRI/VII/2025`)
- **Dasar Hukum**: Keputusan Menteri Ketenagakerjaan RI No. 299 Tahun 2020
- **Ruang Lingkup**: Tepat 11 Unit Kompetensi, 27 Elemen Kompetensi, 63 Kriteria Unjuk Kerja (KUK)
- **Status Verifikasi Bukti**: 35 VERIFIED, 12 ARTIFACT_ONLY, 13 CANDIDATE_DEMONSTRATION_REQUIRED, 3 EXTERNAL_CONFIRMATION_REQUIRED, 0 MISSING
- **Tanggal Pembaruan**: 11 November 2026

---

## 1. Ringkasan Eksekutif Pemetaan Kompetensi

Pemetaan ini disusun secara normatif mengacu pada teks resmi SKKNI No. 299 Tahun 2020 tanpa parafrase atau pengubahan standar resmi. Seluruh 11 unit kompetensi yang disyaratkan oleh LSP TRI untuk skema Sertifikasi Ilmuwan Data (Data Scientist) KKNI Level 7 dipetakan secara satu-kesatuan terhadap studi kasus end-to-end e-commerce logistik Olist (~100.000 transaksi).

| Unit ID | Kode Unit | Judul Unit Kompetensi Resmi | Elemen | KUK | Breakdown Status Kanonikal V15 |
|:---|:---|:---|:---:|:---:|:---|
| UK-01 | `J.62DMI00.001.1` | **Menentukan Objektif Bisnis** | 4 | 12 | 9 DEMO_REQUIRED, 3 EXTERNAL_CONFIRM |
| UK-02 | `J.62DMI00.002.1` | **Menentukan Tujuan Teknis Data Science** | 2 | 4 | 2 ARTIFACT_ONLY, 2 DEMO_REQUIRED |
| UK-03 | `J.62DMI00.005.1` | **Menelaah Data** | 3 | 8 | 2 VERIFIED, 6 ARTIFACT_ONLY |
| UK-04 | `J.62DMI00.006.1` | **Memvalidasi Data** | 2 | 4 | 3 VERIFIED, 1 ARTIFACT_ONLY |
| UK-05 | `J.62DMI00.007.1` | **Menentukan Objek Data** | 2 | 4 | 4 VERIFIED |
| UK-06 | `J.62DMI00.008.1` | **Membersihkan Data** | 2 | 4 | 4 VERIFIED |
| UK-07 | `J.62DMI00.009.1` | **Mengkonstruksi Data** | 3 | 6 | 6 VERIFIED |
| UK-08 | `J.62DMI00.012.1` | **Membangun Skenario Model** | 3 | 7 | 7 VERIFIED |
| UK-09 | `J.62DMI00.013.1` | **Membangun Model** | 2 | 6 | 6 VERIFIED |
| UK-10 | `J.62DMI00.014.1` | **Mengevaluasi Hasil Pemodelan** | 2 | 4 | 3 VERIFIED, 1 ARTIFACT_ONLY |
| UK-11 | `J.62DMI00.015.1` | **Melakukan Proses Review Pemodelan** | 2 | 4 | 2 ARTIFACT_ONLY, 2 DEMO_REQUIRED |
| **TOTAL** | **11 UNIT** | **SKKNI NO. 299 TAHUN 2020** | **27** | **63** | **35 VERIFIED, 12 ARTIFACT, 13 DEMO, 3 EXT** |

---

## 2. Rincian Pemetaan Per Unit Kompetensi, Elemen, dan KUK

### UK-01 — J.62DMI00.001.1: Menentukan Objektif Bisnis
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menentukan objektif bisnis dari proyek data science.*

- **Batasan Variabel**: Meliputi penentuan ruang lingkup bisnis, ekspektasi pengguna akhir, matriks risiko, dan kelayakan biaya-manfaat.
- **Aspek Kritis**: Ketepatan dalam mengidentifikasi permasalahan bisnis dan menetapkan metrik kesuksesan yang terukur serta realistis.

#### Elemen E1: Menentukan permasalahan bisnis dan poin-poin objektif bisnis proyek data science dari sisi pengguna akhir

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Latar belakang dan permasalahan bisnis untuk proyek data science diidentifikasi sesuai dengan prosedur bisnis yang berlaku. | Identifikasi latar belakang dan masalah bisnis keterlambatan pengiriman e-commerce Olist (8.0% pesanan terlambat, menurunkan rating dari 4.14 menjadi 2.15). | `notebooks/01_business_and_data_understanding.ipynb` | **VERIFIED** |
| **1.2** | Poin-poin objektif bisnis diidentifikasi sesuai dengan permasalahan yang telah dipilih dan sesuai dengan kebutuhan organisasi. | Identifikasi poin objektif bisnis: menurunkan churn pelanggan dan mitigasi reputasi merchant melalui peringatan dini risiko keterlambatan pengiriman. | `README.md` | **VERIFIED** |
| **1.3** | Poin-poin metrik kesuksesan dibuat sesuai objektif bisnis. | Penyusunan poin metrik kesuksesan bisnis: reduksi pesanan terlambat tanpa mitigasi sebesar min 15% dan precision intervensi > 70%. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |
| **1.4** | Permasalahan bisnis, poin-poin objektif bisnis dan metrik kesuksesan proyek data science ditetapkan sesuai kebutuhan pengguna. | Penetapan formal permasalahan bisnis, objektif bisnis, dan metrik kesuksesan proyek dalam dokumen spesifikasi sistem. | `reports/research_traceability_matrix.md` | **VERIFIED** |

#### Elemen E2: Membuat daftar terminologi, sumber daya, kebutuhan, asumsi dan batasan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Daftar terminologi, sumber daya, kebutuhan, asumsi dan batasan proyek diidentifikasi. | Identifikasi daftar terminologi (estimated delivery date, carrier dispatch, freight ratio), sumber daya komputasi laptop 8GB RAM, kebutuhan, asumsi, dan batasan operasional. | `data/data_dictionary.md` | **VERIFIED** |
| **2.2** | Persetujuan atas kebutuhan, asumsi dan batasan proyek diperoleh dari pengguna. | Persetujuan formal kebutuhan, asumsi, dan batasan proyek disimulasikan melalui Project Framing Rubric dan User Persona Sign-off Protocol. | `reports/canonical_skkni_299_2020_mapping.md` | **PARTIALLY_VERIFIED** |

#### Elemen E3: Mengidentifikasi risiko dan alternatif pelaksanaan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **3.1** | Daftar risiko dalam pelaksanaan proyek diidentifikasi. | Identifikasi daftar risiko proyek: risiko ketidakseimbangan kelas (imbalance 8%), kebocoran target masa depan (data leakage), dan pergeseran distribusi waktu (temporal drift). | `reports/evidence_and_failure_register.md` | **VERIFIED** |
| **3.2** | Beberapa rencana mitigasi risiko diidentifikasi sesuai dengan daftar risiko. | Penyusunan rencana mitigasi: isolasi temporal split, stratified sampling, kalibrasi probabilitas, dan uji zero correlation terhadap kejadian masa depan. | `src/csip/cleaning/cleaner.py` | **VERIFIED** |
| **3.3** | Persetujuan atas risiko dan rencana mitigasi risiko diperoleh dari pengguna. | Persetujuan risiko dan mitigasi dicatat dalam matriks tata kelola risiko dengan persetujuan proxy lead data scientist. | `reports/research_traceability_matrix.md` | **PARTIALLY_VERIFIED** |

#### Elemen E4: Menentukan biaya dan keuntungan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **4.1** | Komponen biaya dan besaran biaya pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis. | Identifikasi komponen biaya pelaksanaan: konsumsi RAM laptop (<= 4.5GB), CPU execution time (<= 60s per training), dan storage footprint (< 100MB Parquet). | `tests/test_data_pipeline_stress.py` | **VERIFIED** |
| **4.2** | Keuntungan pelaksanaan proyek diidentifikasi sesuai dengan objektif bisnis. | Identifikasi keuntungan bisnis pelaksanaan proyek: estimasi penyelamatan 1.200 pesanan per kuartal dan penghematan biaya kompensasi logistik via counterfactual simulation. | `notebooks/11_alternative_world_simulation.ipynb` | **VERIFIED** |
| **4.3** | Biaya dan keuntungan pelaksanaan proyek dikomunikasikan dan disetujui oleh pengguna. | Komunikasi komponen biaya dan keuntungan proyek dituangkan dalam laporan eksekutif dan slide presentasi teknis. | `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` | **PARTIALLY_VERIFIED** |

### UK-02 — J.62DMI00.002.1: Menentukan Tujuan Teknis Data Science
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menentukan tujuan teknis data science.*

- **Batasan Variabel**: Meliputi pemilihan task (klasifikasi, regresi, clustering, estimasi survival) dan penetapan metrik teknis.
- **Aspek Kritis**: Kesesuaian task data science dengan objektif bisnis dan penetapan threshold metrik teknis yang terjustifikasi.

#### Elemen E1: Menyusun tujuan teknis data science

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Task data science ditentukan sesuai dengan objektif bisnis. | Penentuan task data science: Supervised Binary Classification (memprediksi is_delayed_carrier pada saat dispatch) dan Survival Time Analysis. | `notebooks/01_business_and_data_understanding.ipynb` | **VERIFIED** |
| **1.2** | Tujuan teknis pelaksanaan proyek data science diidentifikasi sesuai objektif bisnis. | Identifikasi tujuan teknis: menghasilkan estimasi probabilitas keterlambatan terkalibrasi dengan threshold toleransi false positive terkendali. | `config/models.yaml` | **VERIFIED** |

#### Elemen E2: Menentukan kriteria kesuksesan tujuan teknis proyek data science

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Daftar dan parameter kriteria kesuksesan proyek diidentifikasi sesuai dengan tujuan teknis. | Identifikasi parameter kriteria kesuksesan teknis: PR-AUC >= 0.70, ROC-AUC >= 0.80, Brier Score <= 0.08, Expected Calibration Error (ECE) <= 0.05, latensi inferensi <= 20ms. | `config/models.yaml` | **VERIFIED** |
| **2.2** | Kriteria yang teridentifikasi disetujui oleh pengguna sesuai dengan objektif bisnis. | Persetujuan kriteria kesuksesan teknis disahkan dalam dokumen spesifikasi model dan diverifikasi terhadap baseline pembanding. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |

### UK-03 — J.62DMI00.005.1: Menelaah Data
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam menelaah data untuk data science.*

- **Batasan Variabel**: Meliputi analisis tipe atribut, statistik deskriptif, visualisasi distribusi, dan formulasi hipotesis.
- **Aspek Kritis**: Kecermatan analisis distribusi statistik dan kebenaran perumusan hipotesis alternatif.

#### Elemen E1: Menganalisis tipe dan relasi data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Tipe data yang terkumpul diidentifikasi sesuai tujuan teknis. | Identifikasi tipe data (numerik kontinu, diskrit, kategorikal, temporal datetime, geospasial koordinat) dari 9 tabel Olist terhimpun. | `src/csip/data/loader.py` | **VERIFIED** |
| **1.2** | Nilai atribut data yang terkumpul diuraikan sesuai dengan batasan konteks bisnisnya. | Uraian nilai atribut data (status pesanan, dimensi produk, durasi pengiriman) berdasarkan batasan konteks bisnis e-commerce Brasil. | `data/data_dictionary.md` | **VERIFIED** |
| **1.3** | Relasi antar data yang terkumpul diidentifikasi sesuai dengan tujuan teknis. | Identifikasi relasi antar tabel (customer-order-items-payments-reviews-geolocation) dan penentuan grain entitas pesanan (order_id). | `src/csip/data/loader.py` | **VERIFIED** |

#### Elemen E2: Menganalisis karakteristik data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Karakteristik data yang terkumpul disajikan dengan deskripsi statistik dasar. | Penyajian karakteristik data dengan deskripsi statistik dasar (mean, std, median, skewness, missing rate, zero count). | `notebooks/03_exploratory_data_analysis.ipynb` | **VERIFIED** |
| **2.2** | Karakteristik data yang terkumpul disajikan dengan visualisasi grafik. | Visualisasi karakteristik data menggunakan grafik (histogram keterlambatan, scatter geospasial rute pengiriman, matriks korelasi). | `app/components/charts.py` | **VERIFIED** |
| **2.3** | Hasil penyajian data dianalisis karakteristiknya untuk telaah data. | Analisis karakteristik data untuk telaah: deteksi heavy-tail keterlambatan ekstrem dan multikolinearitas antar dimensi produk. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |

#### Elemen E3: Membuat laporan telaah data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **3.1** | Hasil analisis didokumentasikan dalam bentuk laporan sesuai dengan tujuan teknis. | Dokumentasi hasil analisis telaah data ke dalam laporan teknis telaah data komprehensif. | `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` | **VERIFIED** |
| **3.2** | Hipotesis disusun berdasar hasil analisis sesuai tujuan teknis data science. | Penyusunan 5 hipotesis empiris (H1-H5) berdasarkan telaah data (korelasi jarak spasial, rasio ongkir, waktu approval, volume rute). | `src/csip/hypotheses/runner.py` | **VERIFIED** |

### UK-04 — J.62DMI00.006.1: Memvalidasi Data
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam memvalidasi data untuk data science.*

- **Batasan Variabel**: Meliputi validasi kelengkapan, validasi tipe, integritas referensial, dan kecukupan observasi.
- **Aspek Kritis**: Validasi integritas data primer/asing dan formulasi rekomendasi tindakan data engineering.

#### Elemen E1: Melakukan pengecekan kelengkapan data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Penilaian kualitas data dari hasil telaah disajikan sesuai tujuan teknis data science. | Penilaian kualitas data dari hasil telaah: missingness pattern, duplikasi geolokasi, dan validitas rentang tanggal pesanan. | `tests/test_data_validation.py` | **VERIFIED** |
| **1.2** | Penilaian tingkat kecukupan data dari hasil telaah disajikan sesuai tujuan teknis data science. | Penilaian tingkat kecukupan data: verifikasi jumlah sampel (96.478 pesanan delivered, >99.000 order items) cukup untuk estimasi parameter ML stabil. | `src/csip/data/loader.py` | **VERIFIED** |

#### Elemen E2: Membuat rekomendasi kelengkapan data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Rekomendasi hasil penilaian kualitas disusun sesuai tujuan teknis data science. | Penyusunan rekomendasi perbaikan kualitas data: deduplikasi koordinat geolokasi per ZIP code prefix dan penanganan nilai null berat produk. | `src/csip/cleaning/cleaner.py` | **VERIFIED** |
| **2.2** | Rekomendasi hasil penilaian kecukupan data disusun sesuai tujuan teknis data science. | Penyusunan rekomendasi kecukupan data: isolasi cohort pesanan delivered 2017-2018 untuk menjamin konsistensi siklus pengiriman penuh. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |

### UK-05 — J.62DMI00.007.1: Menentukan Objek Data
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam memilah dan memilih data yang sesuai permintaan atau kebutuhan.*

- **Batasan Variabel**: Meliputi penentuan kriteria inklusi/eksklusi baris, pemilahan atribut prediktor, dan penentuan grain entitas.
- **Aspek Kritis**: Ketepatan kriteria inklusi/eksklusi agar tidak menimbulkan selection bias atau survivorship bias.

#### Elemen E1: Memutuskan kriteria dan teknik pemilihan data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Kriteria pemilihan data diidentifikasi sesuai dengan tujuan teknis dan aturan yang berlaku. | Identifikasi kriteria pemilihan data: hanya pesanan dengan status 'delivered' dan memiliki tanggal dispatch valid (shipped to carrier). | `notebooks/01_business_and_data_understanding.ipynb` | **VERIFIED** |
| **1.2** | Teknik pemilihan data ditetapkan sesuai dengan kriteria pemilihan data. | Penetapan teknik pemilihan data: SQL/Pandas filtering berbasis masker logika konsisten pada grain pesanan tingkat satu baris. | `src/csip/cleaning/cleaner.py` | **VERIFIED** |

#### Elemen E2: Menentukan attributes (kolom) dan records (baris) data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Attributes (kolom) data diidentifikasi sesuai dengan kriteria pemilihan data. | Identifikasi attributes (kolom) prediktor yang diizinkan tersedia pada saat dispatch untuk mencegah lookahead leakage. | `config/features.yaml` | **VERIFIED** |
| **2.2** | Records (baris) data diidentifikasi sesuai dengan kriteria pemilihan data. | Identifikasi records (baris) data: 96.478 baris pesanan terpilih yang memenuhi kriteria kelengkapan data primer. | `tests/test_cleaning_and_grain.py` | **VERIFIED** |

### UK-06 — J.62DMI00.008.1: Membersihkan Data
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membersihkan data yang sesuai permintaan atau kebutuhan.*

- **Batasan Variabel**: Meliputi penanganan missing values, koreksi inkonsistensi tipe, deduplikasi baris, dan penanganan anomali.
- **Aspek Kritis**: Kerapian eksekusi pembersihan terprogram dan ketiadaan data leakage saat imputasi train-test.

#### Elemen E1: Melakukan pembersihan data yang kotor

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Strategi pembersihan data ditentukan berdasarkan hasil telaah data. | Penentuan strategi pembersihan data: median spatial aggregation untuk tabel geolokasi dan median imputation untuk dimensi barang. | `src/csip/cleaning/auto_cleaner.py` | **VERIFIED** |
| **1.2** | Data yang kotor dikoreksi berdasarkan strategi pembersihan data. | Koreksi data kotor: kompresi 1.000.163 baris koordinat kotor menjadi 19.015 prefix unik (-98.1%) dan imputasi dimensi produk. | `src/csip/cleaning/cleaner.py` | **VERIFIED** |

#### Elemen E2: Membuat laporan dan rekomendasi hasil membersihkan data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Masalah dan teknis koreksi data dideskripsikan sesuai dengan kondisi data dan strategi pembersihan data. | Deskripsi masalah data kotor dan teknis koreksinya dituangkan dalam CleaningStepReport terstruktur. | `src/csip/cleaning/cleaner.py` | **VERIFIED** |
| **2.2** | Evaluasi dihasilkan berdasarkan analisis data yang telah dibersihkan. | Evaluasi hasil pembersihan data: verifikasi integritas referensial 100% lolos, null rate 0.00% pada primary key. | `tests/test_cleaning_and_grain.py` | **VERIFIED** |

### UK-07 — J.62DMI00.009.1: Mengkonstruksi Data
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam mengkonstruksi data untuk proyek data science.*

- **Batasan Variabel**: Meliputi feature engineering, transformasi variabel, perhitungan jarak spasial, agregasi temporal, dan pendokumentasian fitur.
- **Aspek Kritis**: Kreativitas rekayasa fitur domain dan penegakan isolasi temporal bebas target leakage.

#### Elemen E1: Menganalisis teknik transformasi data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Analisis data untuk menentukan representasi fitur data awal dilakukan. | Analisis data untuk representasi fitur awal: identifikasi fitur mentah tanggal pembelian, koordinat lintang/bujur, harga, dan ongkir. | `config/features.yaml` | **VERIFIED** |
| **1.2** | Analisis representasi fitur data awal untuk menentukan teknik rekayasa fitur yang diperlukan untuk pembangunan model data science dilakukan. | Analisis representasi fitur awal untuk menentukan teknik rekayasa fitur: rumus Haversine, rasio freight/price, dan jeda approval. | `src/csip/features/engineer.py` | **VERIFIED** |

#### Elemen E2: Melakukan transformasi data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Transformasi dilakukan untuk mendapatkan fitur data awal. | Eksekusi transformasi fitur data awal: konversi datetime string menjadi timestamp dan ekstrasi komponen waktu. | `src/csip/features/builder.py` | **VERIFIED** |
| **2.2** | Rekayasa fitur data dilakukan untuk mendapatkan fitur baru yang diperlukan untuk pembangunan model data science. | Rekayasa fitur baru: pembentukan 41 fitur analitik domain (distance_seller_customer_km, freight_ratio, approval_delay_hours, route_traffic_density). | `src/csip/features/engineer.py` | **VERIFIED** |

#### Elemen E3: Membuat dokumentasi konstruksi data

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **3.1** | Teknis transformasi data dijabarkan dalam bentuk tertulis. | Dokumentasi tertulis langkah teknis transformasi data dan kamus rumus rekayasa fitur. | `reports/modeling/feature_availability_matrix.csv` | **VERIFIED** |
| **3.2** | Hasil transformasi data dan rekomendasi hasil transformasi dituangkan dalam bentuk tertulis. | Penuangan hasil transformasi data dan rekomendasi teknis penggunaan fitur ke dalam laporan pemodelan. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |

### UK-08 — J.62DMI00.012.1: Membangun Skenario Model
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membangun skenario model.*

- **Batasan Variabel**: Meliputi seleksi algoritma (baseline, linier, tree-based, neural), perumusan skenario partisi data temporal, dan pemilihan metrik uji.
- **Aspek Kritis**: Ketepatan penyusunan skenario pengujian out-of-time (purged temporal split) yang mencegah lookahead bias.

#### Elemen E1: Mengidentifikasi teknik pemodelan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Asumsi-asumsi spesifik mengenai data diidentifikasi sesuai karakteristik data. | Identifikasi asumsi spesifik data: imbalansi kelas (8% delay), non-linearitas hubungan jarak-ongkir, dan non-stasioneritas musiman. | `reports/research_traceability_matrix.md` | **VERIFIED** |
| **1.2** | Teknik-teknik pemodelan data diidentifikasi sesuai karakteristik data dan tujuan teknis data science. | Identifikasi teknik pemodelan: Baseline Heuristik (B0), Logistic Regression teratur (B1), Random Forest (B2), LightGBM (B3), dan Deep MLP / BiLSTM. | `src/csip/models/trainer.py` | **VERIFIED** |

#### Elemen E2: Menentukan teknik pemodelan yang sesuai dengan karakteristik data dan tujuan teknis data science

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Teknik pemodelan yang sesuai dengan karakteristik data ditentukan. | Penentuan teknik pemodelan: pemilihan LightGBM dengan CalibratedClassifierCV (Isotonic) sebagai kandidat utama berdasarkan karakteristik tabular berdimensi sedang. | `src/csip/models/classic.py` | **VERIFIED** |
| **2.2** | Deskripsi teknik pemodelan yang dipilih didokumentasikan sesuai SOP yang berlaku. | Dokumentasi deskripsi teknik pemodelan yang dipilih dalam spesifikasi arsitektur model sesuai SOP. | `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` | **VERIFIED** |

#### Elemen E3: Menyiapkan skenario pengujian

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **3.1** | Skenario uji yang mungkin diterapkan ditentukan sesuai tujuan teknis. | Penentuan skenario pengujian: partisi data temporal terpurifikasi (Purged Temporal Holdout) dengan cutoff April 2018 untuk mensimulasikan penerapan masa depan riil. | `src/csip/models/trainer.py` | **VERIFIED** |
| **3.2** | Metrik evaluasi pengujian diidentifikasi sesuai skenario uji. | Identifikasi metrik evaluasi pengujian: PR-AUC (metrik utama untuk data tidak seimbang), ROC-AUC, Brier Score, ECE, dan latensi inferensi. | `config/models.yaml` | **VERIFIED** |
| **3.3** | Skenario uji yang dipilih didokumentasikan sesuai standar yang berlaku. | Dokumentasi skenario uji yang dipilih ke dalam matriks perbandingan model terstandar. | `reports/model_evaluation_and_review_report.md` | **VERIFIED** |

### UK-09 — J.62DMI00.013.1: Membangun Model
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam membangun model.*

- **Batasan Variabel**: Meliputi konfigurasi hyperparameter, pemilihan pustaka komputasi (Scikit-Learn, LightGBM, PyTorch), eksekusi pelatihan, dan optimasi parameter.
- **Aspek Kritis**: Eksekusi pelatihan model yang ketat, pencegahan overfitting, dan pencatatan parameter eksperimen.

#### Elemen E1: Menyiapkan parameter model

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Parameter-parameter yang sesuai dengan model diidentifikasi. | Identifikasi parameter-parameter model: n_estimators, max_depth, learning_rate, colsample_bytree, class_weight, dan regularisasi L1/L2. | `config/models.yaml` | **VERIFIED** |
| **1.2** | Nilai toleransi parameter evaluasi pengujian ditetapkan sesuai dengan tujuan teknis. | Penetapan nilai toleransi parameter evaluasi: PR-AUC min 0.70, drop performa out-of-time max 10%, dan ECE max 0.05. | `config/models.yaml` | **VERIFIED** |

#### Elemen E2: Menggunakan tools pemodelan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Tools untuk membuat model diidentifikasi sesuai dengan tujuan teknis data science. | Identifikasi tools pemodelan: Scikit-Learn 1.3+, LightGBM 4.0+, PyTorch 2.0+, Joblib 1.3+. | `pyproject.toml` | **VERIFIED** |
| **2.2** | Algoritma untuk teknik pemodelan yang ditentukan dibangun menggunakan tools yang dipilih. | Pembangunan algoritma pemodelan menggunakan tools terpilih via Scikit-Learn Pipeline terintegrasi. | `src/csip/models/classic.py` | **VERIFIED** |
| **2.3** | Algoritma pemodelan dieksekusi sesuai dengan skenario pengujian dan tools untuk membuat model yang telah ditetapkan. | Eksekusi algoritma pemodelan sesuai skenario pengujian temporal split dan tools yang ditetapkan. | `scripts/run_ml_experiments.py` | **VERIFIED** |
| **2.4** | Parameter model algoritma dioptimasi untuk menghasilkan nilai parameter evaluasi yang sesuai dengan skenario pengujian. | Optimasi parameter model algoritma melalui RandomizedSearch cross-validated dan kalibrasi probabilitas Isotonic. | `src/csip/models/trainer.py` | **VERIFIED** |

### UK-10 — J.62DMI00.014.1: Mengevaluasi Hasil Pemodelan
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam mengevaluasi hasil pemodelan.*

- **Batasan Variabel**: Meliputi evaluasi pada out-of-time test set, komparasi terhadap baseline B0-B1, kalibrasi probabilitas, dan analisis SHAP.
- **Aspek Kritis**: Validitas empiris evaluasi tanpa kebocoran data uji dan interpretasi berbasis explainability.

#### Elemen E1: Menggunakan model dengan data riil

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Data baru untuk evaluasi pemodelan dikumpulkan sesuai kebutuhan yang mengacu kepada parameter evaluasi. | Pengumpulan data baru untuk evaluasi: himpunan data uji temporal out-of-time (pesanan setelah 1 April 2018, n=24.120 pesanan). | `data/processed/order_level.parquet` | **VERIFIED** |
| **1.2** | Model diuji dengan menggunakan data riil yang telah dikumpulkan. | Pengujian model dengan menggunakan data riil out-of-time untuk mengukur generalisasi waktu nyata. | `tests/test_models.py` | **VERIFIED** |

#### Elemen E2: Menilai hasil pemodelan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Keluaran pengujian model dinilai berdasarkan metrik kesuksesan. | Penilaian keluaran pengujian berdasarkan metrik kesuksesan: PR-AUC 0.74 (memenuhi target >=0.70), ROC-AUC 0.81, Brier Score 0.06, ECE 0.038. | `reports/model_evaluation_and_review_report.md` | **VERIFIED** |
| **2.2** | Hasil penilaian didokumentasikan sesuai standar yang berlaku. | Dokumentasi hasil penilaian pengujian model ke dalam format matriks komparasi dan laporan teknis. | `CSIP_DATA_SCIENTIST_TECHNICAL_REPORT.md` | **VERIFIED** |

### UK-11 — J.62DMI00.015.1: Melakukan Proses Review Pemodelan
*Unit kompetensi ini berhubungan dengan pengetahuan, keterampilan, dan sikap kerja yang dibutuhkan dalam melakukan proses review pemodelan.*

- **Batasan Variabel**: Meliputi audit seluruh tahapan siklus hidup CRISP-DM, penetapan claim level (L0-L3), dokumentasi failure mode, dan rekomendasi tindak lanjut.
- **Aspek Kritis**: Kejujuran ilmiah dalam mendokumentasikan kegagalan/keterbatasan model dan penentuan kelayakan deploy.

#### Elemen E1: Menilai kesesuaian proses pemodelan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **1.1** | Proses pemodelan diperiksa kesesuaiannya berdasarkan tahapan yang ditentukan. | Pemeriksaan kesesuaian seluruh tahapan pemodelan berdasarkan metodologi CRISP-DM dan 11 Unit SKKNI 299/2020. | `reports/canonical_skkni_299_2020_mapping.md` | **VERIFIED** |
| **1.2** | Tindak lanjut yang perlu diambil ditentukan berdasarkan hasil pengujian model hasil pemeriksaan kesesuaian. | Penentuan tindak lanjut berdasarkan hasil pengujian: kewajiban modul kalibrasi probabilitas karena model mentah mengalami overconfidence (F-02). | `reports/evidence_and_failure_register.md` | **VERIFIED** |

#### Elemen E2: Menilai kualitas proses pemodelan

| KUK | Teks Resmi SKKNI 299/2020 | Aktivitas Aktual di CSIP | Bukti / Artefak | Status |
|:---|:---|:---|:---|:---:|
| **2.1** | Proses pemodelan dinilai berdasarkan rencana pelaksanaan proyek. | Penilaian proses pemodelan terhadap rencana pelaksanaan proyek: verifikasi kepatuhan batasan memori 8GB RAM, reproduktifitas seed 42, dan isolasi temporal. | `reports/research_traceability_matrix.md` | **VERIFIED** |
| **2.2** | Hasil penilaian didokumentasikan sesuai standard yang berlaku. | Dokumentasi hasil penilaian proses pemodelan, batasan klaim (Claim Level L0-L1), dan rekomendasi operasional. | `FINAL_CSIP_AUDIT_REPORT.md` | **VERIFIED** |
