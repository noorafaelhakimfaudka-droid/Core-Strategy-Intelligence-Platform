# BUKU INDUK PROYEK & SKRIP PRESENTASI MASTER — CORE STRATEGY & INTELLIGENCE PLATFORM (CSIP v1.1.0)

> **Catatan Edisi Induk LaTeX (Otoritatif 76 Halaman):**  
> Edisi induk super-lengkap (Bagian I–IV, Bab 1–16, termasuk skrip presentasi kata-demi-kata dan ensiklopedia 25 Q&A penguji) bersumber di **[BUKU_INDUK_CSIP_LENGKAP.tex](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/BUKU_INDUK_CSIP_LENGKAP.tex)** dan dikompilasi via LaTeX (`scripts/build_csip_book.py`) menjadi **[BUKU_INDUK_CSIP_LENGKAP.pdf](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/docs/BUKU_INDUK_CSIP_LENGKAP.pdf)** (76 halaman). Dokumen Markdown ini berfungsi sebagai ringkasan teks cepat di repositori.

**Subjudul:** Panduan Lengkap dari Titik Nol hingga Produksi: Bisnis, Arsitektur Data, Algoritma Machine Learning, Tata Kelola MLOps, Skrip Presentasi Siap Baca, Panduan Live Demo & Tanya-Jawab Sidang  
**Versi Dokumen:** 1.1.0  
**Basis Kode:** `Core Strategy & Intelligence Platform (csip)`  
**Pembaca Sasaran:** Pemimpin Bisnis & Manajemen Non-Teknis, Data Scientist, Machine Learning Engineer, Data Engineer, serta Asesor Kompetensi SKKNI Level 7  

---

## DAFTAR ISI UTAMA

### BAGIAN I — BUKU ACUAN LENGKAP PROYEK CSIP (BAB 1 s/d BAB 10)

- **Bab 1** — Gambaran Besar Proyek dari Titik Nol: Masalah Bisnis, Visi Produk & Strategi Dua Lapis
- **Bab 2** — Bedah Dataset Olist (9 Tabel, 99.441 Pesanan), Pembersihan Data & Kontrak Data 4-Tingkat
- **Bab 3** — Rekayasa Fitur, Isolasi Waktu (T0, T1, T2) & Cara Mencegah Kebocoran Data (*Data Leakage*)
- **Bab 4** — Tangga Pemodelan (*Baseline Ladder B0–B4*) & Cara Kerja Seluruh Algoritma di CSIP
- **Bab 5** — Hasil Empiris Seluruh Model, Kejujuran Ilmiah (*Valid Negative Findings*) & Audit Angka
- **Bab 6** — Kalibrasi Probabilitas (*Platt Scaling*), Penjelasan SHAP & Uji Ketahanan Lintas Wilayah
- **Bab 7** — *Business Decision Engine*: Mengubah Prediksi Jadi Aksi, Kuota Tim CS & Rancangan Uji A/B
- **Bab 8** — *Universal CSV Studio* (`ml_engine.py` & `semantic_profiler.py`): Analitik Lintas Bidang
- **Bab 9** — MLOps, Observatorium *Drift* Real-Time & Siklus Promosi *Champion-Challenger*
- **Bab 10** — Layanan Mikro FastAPI, Kokpit Streamlit, Pengujian Otomatis (216 Kasus Uji) & 12 Gerbang Kualitas

### BAGIAN II — SKRIP PRESENTASI MASTER & PANDUAN TANYA-JAWAB (BAB 11 s/d BAB 14)

- **Bab 11** — Strategi Presentasi & Manajemen Waktu (Format 15 Menit Eksekutif vs 35 Menit Sidang Lengkap)
- **Bab 12** — Skrip Bicara Kata-demi-Kata (*Verbatim*): Babak 1 s/d Babak 7 (Penjelasan Proyek, Data, Metodologi & Model)
- **Bab 13** — Skrip Live Demo Kata-demi-Kata (*Verbatim*): Babak 8 s/d Babak 12 (Demo CSIP Studio, 4 Lensa, FastAPI & Audit Kode)
- **Bab 14** — Buku Saku Tanya-Jawab (*Q&A Defense Cheat-Sheet*): 15 Pertanyaan Tersulit & Jawaban Terbaiknya

---

# BAB 1 — GAMBARAN BESAR PROYEK DARI TITIK NOL: MASALAH BISNIS, VISI PRODUK & STRATEGI DUA LAPIS

## 1.1 Analogi Sederhana: Mengapa Proyek Ini Lahir?

Bayangkan sebuah toko online raksasa yang mengirim hampir 100.000 paket melintasi wilayah geografis seluas Brasil. Setiap minggu, ribuan paket bergerak di jaringan kurir yang jaraknya bisa ratusan hingga ribuan kilometer. Ketika sebagian paket terlambat tiba atau biaya kirimnya terasa terlalu mahal dibandingkan harga barang, sebagian pelanggan menjadi kecewa lalu menulis ulasan bintang 1 atau 2 dan tidak kembali berbelanja.

Tim *Customer Service* (CS) dan operasional tentu ingin membantu pelanggan sebelum kekecewaan meledak. Namun ada dua kendala nyata di lapangan:

1. **Kapasitas Manusia Terbatas:** Tim CS hanya mampu menangani ratusan kasus prioritas per hari, bukan menelpon puluhan ribu pembeli satu per satu.
2. **Menunggu Komplain Terlambat:** Jika tim baru bertindak setelah ulasan bintang 1 terbit, reputasi penjual dan kepercayaan pembeli terlanjur rusak.

Di dunia nyata, banyak proyek Data Science gagal menjawab kebutuhan ini karena terjebak di salah satu dari dua ekstrem:

- **Ekstrem Pertama (Notebook Akademik Semata):** Peneliti sibuk mengejar skor akurasi setinggi mungkin memakai pemecahan data acak (*random split*), tanpa sadar bahwa data masa depan (seperti lama pengiriman aktual) ikut terbaca untuk memprediksi kejadian saat pembeli baru membayar. Hasilnya terlihat bagus di presentasi, tetapi hancur saat dijalankan di dunia nyata.
- **Ekstrem Kedua (Dashboard Kosmetik):** Aplikasi menampilkan grafik warna-warni atau AI percakapan, tetapi angka di dalamnya tidak terhubung ke keputusan operasional yang terukur dan tidak punya pagar keamanan saat pola data berubah.

**Core Strategy & Intelligence Platform (CSIP v1.1.0)** dibangun sejak nol untuk menutup jurang tersebut. CSIP adalah platform kecerdasan bisnis dan pengambilan keputusan (*Business & Decision Intelligence Platform*) yang mengubah data transaksi mentah menjadi:

- **Pemahaman Situasi (*Deskriptif*):** Apa yang sedang terjadi di operasi pengiriman dan kepuasan pelanggan?
- **Akar Masalah (*Diagnostik*):** Faktor apa yang paling berkaitan dengan keluhan pelanggan?
- **Perkiraan Risiko (*Prediktif*):** Pesanan mana yang berisiko terlambat atau mendapat ulasan buruk pada titik waktu tertentu?
- **Daftar Tindakan (*Preskriptif*):** Pesanan mana yang harus diprioritaskan oleh tim Logistik dan CS sesuai kuota kerja harian?
- **Pemantauan Terus-Menerus (*Evaluatif*):** Apakah performa model masih sehat bulan ini, atau pola pasar sudah bergeser (*drift*)?

## 1.2 Strategi Arsitektur Dua Lapis: Kedalaman Vertikal + Keluasan Lintas Industri

Sering muncul pertanyaan penting saat menilai proyek analitik: *"Apakah sistem ini hanya bekerja untuk data toko online Olist, atau bisa menganalisis file CSV dari bisnis lain?"*

CSIP menjawabnya dengan **Strategi Dua Lapis (*Depth vs. Breadth*)** agar tidak mengorbankan ketelitian ilmiah demi keserbagunaan:

| Lapisan Sistem | Lokasi Kode & Antarmuka | Tujuan Utama | Cara Kerja Singkat |
| :--- | :--- | :--- | :--- |
| **Lapis 1: Pembuktian Mendalam Vertikal (*Olist E-Commerce*)** | `src/csip/` + Layanan API `FastAPI` + Artefak Terlatih | Membuktikan kedalaman penuh Data Science & MLOps pada skema bisnis nyata 9 tabel. | Memakai kontrak data ketat, isolasi waktu checkout vs pasca-kirim, kalibrasi probabilitas, SHAP, dan *Decision Engine*. |
| **Lapis 2: Eksplorasi Lintas Bidang (*Universal CSV Studio*)** | `app/streamlit_app.py` + `ml_engine.py` + `semantic_profiler.py` | Memungkinkan siapa pun mengunggah file CSV/Excel dari sektor mana saja untuk dibedah secara instan. | Mendeteksi arti kolom otomatis, mendeteksi risiko kebocoran tanggal/ID, memilih klasifikasi vs regresi, dan menyediakan simulator *what-if*. |

Pemisahan dua lapis ini sangat penting. Data CSV umum dari bidang kesehatan atau SDM tidak dipaksa memakai aturan ongkos kirim e-commerce, sementara model produksi e-commerce tetap terjaga kontrak skemanya tanpa tercampur data eksperimen bebas.

## 1.3 Peta Alur Sistem dari Awal hingga Akhir

```text
[1. Data Mentah / File CSV]
        |
        v
[2. Kontrak Data 4-Tingkat & Pencatatan Hash SHA-256]  --(Gagal Kritis?)--> [Pipeline Berhenti Aman]
        |
        v
[3. Pembersihan Deterministik & Penggabungan ke Level order_id]
        |
        v
[4. Isolasi Fitur Berbasis Waktu: Pos T0 Checkout | Pos T1 Kurir | Pos T2 Pasca-Kirim]
        |
        v
[5. Tangga Baseline (B0-B4) + Kalibrasi Probabilitas Platt + Atribusi SHAP]
        |
        v
[6. Business Decision Engine (Prioritas + Kuota Kapasitas CS + Rancangan Uji A/B)]
        |
        v
[7. Layanan FastAPI + Kokpit CSIP Studio + Observatorium Drift & Champion-Challenger]
```

---

# BAB 2 — BEDAH DATASET OLIST (9 TABEL, 99.441 PESANAN), PEMBERSIHAN DATA & KONTRAK DATA 4-TINGKAT

## 2.1 Mengapa Dataset Olist Bukan "Sekadar 1 File CSV Kecil"?

Banyak orang keliru mengira Olist hanya satu file tabel sederhana. Faktanya, dataset **Olist E-Commerce Brasil (2016–2018)** adalah ekosistem relasional utuh yang terdiri atas **9 tabel terpisah** dengan total lebih dari **1,5 juta baris rekaman mentah** melintasi 27 negara bagian di Brasil.

| Nama Tabel Mentah | Jumlah Baris Awal | Peran Bisnis & Tantangan Teknis |
| :--- | ---: | :--- |
| `olist_orders_dataset.csv` | 99.441 | Tabel inti pesanan: menyimpan ID pesanan, ID pembeli, status pengiriman, dan 5 stempel waktu siklus pesanan. |
| `olist_order_items_dataset.csv` | 112.650 | Rincian barang di dalam keranjang belanja (harga barang, ongkir, ID produk, ID penjual). Satu pesanan bisa berisi banyak barang. |
| `olist_order_payments_dataset.csv` | 103.886 | Cara bayar pelanggan (kartu kredit, voucher, boleto) beserta jumlah cicilan. Satu pesanan bisa dibayar terpecah. |
| `olist_order_reviews_dataset.csv` | 104.719 | Penilaian bintang 1–5 dan komentar teks berbahasa Portugis. Ada pesanan yang direvisi ulasannya dan ada yang tidak mengulas. |
| `olist_geolocation_dataset.csv` | 1.000.163 | Satu juta lebih baris koordinat GPS kode pos Brasil yang penuh duplikasi serta beberapa titik koordinat nyasar ke luar Brasil. |
| `olist_customers_dataset.csv` | 99.441 | Penghubung ID pesanan ke identitas unik pelanggan (`customer_unique_id`) yang berjumlah 75.318 orang setelah dibersihkan. |
| `olist_products_dataset.csv` | 32.951 | Spesifikasi fisik barang: kategori, berat (gram), ukuran panjang/tinggi/lebar, dan jumlah foto produk. |
| `olist_sellers_dataset.csv` | 3.095 | Lokasi penjual (kota, negara bagian, dan prefiks kode pos). |
| `product_category_name_translation.csv` | 71 | Kamus penerjemah nama kategori produk dari bahasa Portugis ke bahasa Inggris. |

## 2.2 Masalah Teknis Pertama: Bahaya *Cartesian Fan-Out* dan Solusi Agregasi

**Analogi Non-Teknis:** Bayangkan 1 transaksi pesanan berisi 3 baju, dibayar dengan 2 metode (voucher + kartu kredit), lalu pembeli mengirim 2 kali revisi ulasan. Jika tabel pesanan digabungkan langsung secara mentah ke tabel barang, pembayaran, dan ulasan, 1 transaksi tersebut akan mengganda menjadi `3 x 2 x 2 = 12` baris!

Akibatnya sangat berbahaya bagi Data Science:
1. Nilai total transaksi dan jumlah kejadian membengkak palsu.
2. Satu pesanan yang sama bisa masuk ke data latih sekaligus data uji, sehingga skor evaluasi model menjadi menipu.

**Solusi Rekayasa di `OlistDataCleaner` (`src/csip/cleaning/cleaner.py`):**  
CSIP mewajibkan aturan keras bahwa **setiap tabel anak wajib diringkas terlebih dahulu ke level 1 baris per `order_id`** sebelum digabungkan (*strict order-grain consolidation*):

1. **Pembersihan Koordinat GPS (`clean_geolocation_dedup.parquet`):** Dari `1.000.163` baris GPS mentah, titik koordinat di luar kotak batas geografis wilayah Brasil (`Latitude` antara `-34,0` hingga `+5,5` dan `Longitude` antara `-74,0` hingga `-34,5`) dibuang. Setiap kode pos lalu diambil titik tengahnya menggunakan **median** (karena median jauh lebih kebal terhadap data nyasar dibanding rata-rata). Hasilnya menyusut 98,1% menjadi **19.015 prefiks kode pos unik**.
2. **Agregasi Keranjang Barang:** Tabel barang (`112.650` baris) diringkas per pesanan menjadi `total_item_price` (total harga barang), `total_freight` (total ongkir), `item_count` (jumlah unit), dan `mean_product_weight_g` (rata-rata berat).
3. **Agregasi Pembayaran:** Tabel pembayaran (`103.886` baris) diringkas per pesanan menjadi `total_payment_value` dan `payment_installments_max` (tenor cicilan terpanjang).
4. **Deduplikasi Ulasan & Kejujuran Label Hilang:** Dari `104.719` baris ulasan, tiap pesanan hanya mengambil **1 ulasan paling akhir** berdasarkan stempel waktu jawaban/pembuatan. Jika pelanggan tidak meninggalkan ulasan, CSIP **melarang keras menebak atau mengisi rating palsu**. Sistem membuat kolom penanda `has_observed_review` bernilai `1` jika ada ulasan, atau `0` jika kosong (`NaN`), lalu mendefinisikan target biner:
   - `negative_review_flag = 1` jika `review_score <= 2` (bintang 1 atau 2).
   - `negative_review_flag = 0` jika `review_score >= 3` (bintang 3, 4, atau 5).
   - `negative_review_flag = Kosong (NaN)` jika pelanggan tidak mengulas.

## 2.3 Transparansi Penyaringan Populasi (*Population & Selection Bias Funnel*)

Dalam `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`, CSIP mendokumentasikan secara terbuka ke mana saja perginya setiap baris pesanan dari mentah hingga siap dimodelkan:

| Tahap Penyaringan Populasi | Jumlah Pesanan | Penjelasan & Implikasi Bisnis |
| :--- | ---: | :--- |
| **1. Total Pesanan Mentah** | 99.441 | Seluruh pesanan yang tercatat masuk sistem Olist (2016–2018). |
| **2. Disaring ke Status `delivered`** | 96.478 | Memisahkan **1.234 pesanan `canceled` & `unavailable`** (yang tingkat ulasan buruknya mencapai **87,19%–87,60%**) serta status *in-transit* lain karena paket tersebut tidak pernah menjalani siklus pengantaran kurir hingga tuntas. |
| **3. Hasil Bersih Konsolidasi (`order_level`)** | 96.470 | Penggabungan bersih ber-grain tunggal `order_id` setelah audit integritas relasional. |
| **4. Pesanan dengan Ulasan Teramati** | 95.824 | Terdapat **646 pesanan terkirim tanpa ulasan (~0,67%)**. Model kepuasan pelanggan hanya melatih dan menilai pesanan yang benar-benar memiliki label ulasan (`has_observed_review == 1`). |

Dengan transparansi ini, ruang lingkup klaim model CSIP selalu dinyatakan jujur: *memprediksi risiko ulasan negatif bersyarat pada pesanan yang statusnya selesai terkirim*, bukan mengklaim seluruh pesanan gagal kirim.

## 2.4 Optimasi RAM 8 GB, Kontrak Data 4-Tingkat & Sidik Jari SHA-256

Agar proyek ini berjalan mulus di laptop standar dengan RAM 8 GB tanpa server mahal:

- **Penurunan Ukuran Tipe Data (`downcast_dataframe` di `src/csip/data/loader.py`):** Kolom desimal `float64` bawaan pandas diturunkan aman ke `float32`, dan bilangan bulat `int64` diturunkan ke `int8`/`int16`/`int32` sesuai rentangnya. Pemakaian memori langsung berkurang hampir separuh.
- **Format Penyimpanan Apache Parquet:** File `order_level.parquet` hanya memakan **~18,43 MB** di disk dibanding gabungan CSV mentah di atas 120 MB, namun tetap menyimpan tipe kolom dan tanggal secara presisi. Untuk membuat file rilis `.zip` tetap di bawah 100 MB, CSV mentah di `data/raw/` dikecualikan dari arsip dan disediakan skrip [download_raw_olist.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/scripts/download_raw_olist.py) jika pengguna ingin mengulang proses pembersihan dari awal.
- **Kontrak Data 4-Tingkat (`src/csip/data/contracts.py`):** Setiap data yang melewati pipeline wajib lolos `DataContract`. Pelanggaran dibagi empat level:
  - `INFO`: Catatan statistik normal ukuran tabel.
  - `WARNING`: Peringatan ringan seperti nilai ekstrem non-fatal.
  - `RECOVERABLE_ERROR`: Anomali minor yang bisa ditangani otomatis sesuai aturan bersih.
  - `CRITICAL_FAILURE`: Kerusakan fatal (kolom wajib hilang, ID pesanan ganda, atau tipe korup) yang memicu `DataContractViolationError` dan **menghentikan pipeline seketika** sebelum menghasilkan prediksi keliru.
- **Garis Silsilah Data (*Data Lineage*):** Setiap tabel bersih dicatat sidik jari kriptografi **SHA-256**-nya (`src/csip/data/lineage.py`) sehingga setiap hasil model selalu dapat dilacak kembali ke versi data asalnya.

---

# BAB 3 — REKAYASA FITUR, ISOLASI WAKTU (T0, T1, T2) & PENCEGAHAN KEBOCORAN DATA

## 3.1 Mengapa *Data Leakage* Adalah Musuh Nomor Satu Proyek Prediktif?

**Analogi Non-Teknis:** Bayangkan seorang guru memberi ujian prakiraan cuaca besok pagi, tetapi di lembar soal tercantum kolom *"apakah jalanan besok siang basah oleh hujan?"*. Siswa yang menebak "besok hujan" pasti mendapat nilai 100 di kelas, namun gagal total saat harus meramal cuaca di dunia nyata karena informasi jalan basah belum tersedia malam sebelumnya.

Di proyek e-commerce, kesalahan serupa paling sering terjadi: fitur **keterlambatan pengiriman aktual** ikut dimasukkan saat memprediksi keluhan **pada detik pelanggan baru menekan tombol bayar**. Itu disebut **Target Leakage / Lookahead Leakage**.

CSIP mencegah kesalahan fatal tersebut secara arsitektural dengan memisahkan fitur ke dalam **3 Pos Waktu Operasional yang Ketat**:

## 3.2 Tiga Pos Waktu Operasional (T0, T1, T2)

### Pos T0 — Saat Pembeli Melakukan Pembayaran (*Checkout Early Warning*, 10 Fitur)

Dipakai oleh model `best_early_warning_review_lightgbm.joblib`. Pada titik ini kurir belum bergerak sama sekali, sehingga **seluruh data pengiriman aktual diblokir keras**:

1. `total_item_price`: Total harga barang yang dibeli.
2. `total_freight`: Total ongkos kirim.
3. `total_order_value`: Nilai total transaksi (`harga barang + ongkir`).
4. `freight_ratio`: Perbandingan ongkos kirim terhadap harga barang (`total_freight / total_item_price`), mencerminkan beban biaya kirim secara psikologis.
5. `item_count`: Banyaknya item dalam keranjang.
6. `payment_installments_max`: Jumlah cicilan pembayaran.
7. `seller_buyer_distance_km`: Jarak lurus geografis antara kode pos penjual dan pembeli dalam kilometer (dihitung dari koordinat kode pos yang telah dibersihkan pada modul `src/csip/features/engineer.py`).
8. `estimated_lead_time_days`: Janji estimasi lama pengiriman yang tertera ke pembeli saat checkout.
9. `distance_x_weight`: Perkalian jarak pengiriman dengan rata-rata berat produk untuk memotret beban fisik ekspedisi.
10. `prior_order_count`: Jumlah transaksi terdahulu milik pelanggan yang sama **sebelum tanggal pesanan ini** (dihitung murni mundur ke belakang per `customer_unique_id` agar riwayat belanja masa depan tidak ikut terhitung).

### Pos T1 — Saat Pembayaran Disetujui & Disposisi Kurir (5 Fitur)

Dipakai oleh model regresi `best_delivery_delay_lightgbm.joblib` untuk memperkirakan berapa hari pesanan berpotensi meleset dari janji awal:

- `total_order_value`, `freight_ratio`, `estimated_lead_time_days`, `seller_buyer_distance_km`, serta `approval_lag_hours` (jeda jam dari saat pembeli klik pesan hingga pembayaran terkonfirmasi sistem).

### Pos T2 — Setelah Paket Tiba (*Post-Fulfillment Diagnostics*, 15 Fitur)

Dipakai oleh model `best_negative_review_lightgbm.joblib` setelah status pengiriman selesai untuk mendiagnosis pengalaman aktual dan menyusun prioritas penanganan tim CS sebelum maupun sesudah survei ditutup:

- Mencakup fitur ekonomi & jarak seperti di atas, ditambah **5 fitur realitas pengiriman aktual**:
  1. `delivery_lead_time_days`: Lama hari tunggu aktual dari bayar sampai paket tiba.
  2. `delivery_delay_days`: Selisih hari kedatangan aktual dikurangi estimasi janji (positif berarti telat).
  3. `is_late`: Penanda `1` jika terlambat, `0` jika tepat waktu atau lebih cepat.
  4. `delay_x_freight_ratio`: Interaksi *"kekecewaan ganda"* — sudah bayar ongkir mahal, barangnya terlambat datang pula.
  5. `high_value_late_flag`: Penanda khusus pesanan bernilai tinggi yang mengalami keterlambatan.

Pada layanan API (`src/csip/api/server.py`), pemisahan T0 dan T2 dikunci lewat endpoint yang terpisah (`/predict/early-warning` hanya menerima 10 fitur T0, sedangkan `/predict/post-fulfillment` menerima 15 fitur T2).

## 3.3 Pembagian Data Kronologis & Embargo 90 Hari (`RollingOriginTemporalCV`)

Selain memisahkan pos fitur, CSIP melarang pemecahan data acak (*random split*) untuk evaluasi model Olist. Data diurutkan murni berdasarkan waktu pembelian (`order_purchase_timestamp`):

- **Data Latih (*Training Set*):** Pesanan sampai dengan `31 Maret 2018` (`63.666` baris pada pelatihan model inti).
- **Data Validasi (*Validation Set*):** Pesanan `1 April 2018` sampai `30 Juni 2018`, dipakai untuk penyetelan model dan melatih kalibrator probabilitas.
- **Data Uji Terkunci (*Locked Holdout Test Set*):** Pesanan setelah `30 Juni 2018` (`N = 12.571` untuk model ulasan negatif; `N = 12.630` untuk model prediksi keterlambatan). Data ini dikunci hingga akhir dan hanya dievaluasi untuk mengukur kinerja nyata pada masa depan.

Untuk memastikan kestabilan performa di berbagai musim, `RollingOriginTemporalCV` (`src/csip/evaluation/temporal_cv.py`) juga menguji **4 lipatan jendela waktu mengembang (*expanding window folds*)** dengan jarak jeda (**embargo**) minimal **90 hari** antara batas akhir data latih dan awal data validasi pada setiap lipatan. Tujuannya agar pesanan dari periode latih yang pengirimannya panjang dan ulasannya baru muncul berminggu-minggu kemudian tidak tumpang tindih ke periode validasi.

---

# BAB 4 — TANGGA PEMODELAN (*BASELINE LADDER B0–B4*) & CARA KERJA SELURUH ALGORITMA DI CSIP

## 4.1 Filosofi "Mulai dari Sederhana, Baru Naik ke Kompleks"

Dalam banyak proyek amatir, pengembang langsung memakai algoritma terberat tanpa tahu apakah tebakan sederhana sebenarnya sudah cukup baik. CSIP mewajibkan setiap masalah melewati **Tangga Baseline B0 hingga B4** (`src/csip/models/classic.py` & `trainer.py`):

| Tingkat | Keluarga Model | Contoh Implementasi di CSIP | Alasan Mengapa Tingkat Ini Penting |
| :---: | :--- | :--- | :--- |
| **B0** | **Tebakan Naif & Aturan Bisnis Sederhana** | `MajorityClassClassifier` (menebak sesuai rasio kelas), `DelayHeuristicClassifier` (jika telat beri skor risiko tinggi), `MeanRegressor` / Median Latih. | Menetapkan batas lantai minimum. Jika model ML mahal tidak bisa mengalahkan aturan `if-else` B0, model ML tidak layak dipakai. |
| **B1** | **Model Linear Terstandarisasi** | `LogisticRegression` (untuk klasifikasi), `Ridge` (untuk regresi angka). | Mengukur seberapa jauh masalah bisa diselesaikan hanya dengan hubungan garis lurus antar fitur. |
| **B2** | **Non-Linear Sederhana & Berbasis Jarak** | `DecisionTree`, `KNeighbors` (KNN), `GaussianNB`. | Menguji manfaat aturan pemisahan sederhana dan kemiripan tetangga terdekat. |
| **B3** | **Kumpulan Pohon Keputusan (*Tree Ensembles*)** | `RandomForest` & **LightGBM** (`LGBMClassifier` / `LGBMRegressor`). | Menangkap interaksi kompleks antar-fitur sambil menjaga ukuran file sangat kecil dan eksekusi super cepat di CPU. |
| **B4** | **Deep Learning (Tabular & Teks)** | `TabularEmbeddingMLP` (`deep_tabular.py`) & **`TextBiLSTM`** (`deep_seq.py`). | Menguji apakah jaringan saraf tiruan memberi nilai tambah di data tabel maupun pada teks ulasan pelanggan. |

## 4.2 Penjelasan Cara Kerja Algoritma yang Digunakan di CSIP

### 1. LightGBM (*Gradient Boosted Decision Trees*) — Juara Model Tabular

- **Cara Kerja Secara Mudah:** Bayangkan serangkaian ratusan pohon tanya-jawab pendek yang bekerja secara estafet. Pohon ke-1 membuat prediksi awal, lalu melihat di pesanan mana ia masih banyak salah tebak. Pohon ke-2 khusus mempelajari kesalahan pohon ke-1, pohon ke-3 memperbaiki sisa kesalahan pohon ke-2, dan seterusnya hingga prediksi gabungan menjadi tajam.
- **Mengapa LightGBM Mengalahkan Deep Learning Tabular (`TabularEmbeddingMLP`) di Data Ini?** Data transaksi memiliki banyak nilai ekstrem miring (misalnya sebagian besar paket tiba tepat waktu, tetapi sebagian kecil terlambat hingga +30 atau +40 hari). Pohon keputusan jauh lebih tangguh memecah ambang batas angka seperti itu ketimbang jaringan saraf tiruan tabular, sekaligus jauh lebih ringan (ukuran file model hanya **~433–520 KB**, inferensi 1.000 baris di CPU hanya **4–13 milidetik**), dan sangat mudah dijelaskan faktor pengaruhnya lewat **SHAP TreeExplainer**.

### 2. PyTorch Bidirectional LSTM (`TextBiLSTM`) — Pembaca Komentar Ulasan Teks

- **Cara Kerja Secara Mudah:** Tidak semua ketidakpuasan tertangkap oleh angka harga atau tanggal. Di `src/csip/models/deep_seq.py`, model `TextBiLSTM` membaca komentar tertulis pelanggan berbahasa Portugis kata demi kata.
- **Proses Teknis:**
  1. `SimpleTokenizer` mengubah kalimat menjadi daftar token angka menggunakan kosakata paling sering muncul (`max_vocab_size = 5.000` kata, frekuensi minimal `2`), dibatasi maksimal `50` kata per ulasan.
  2. Lapisan *Embedding* (`64` dimensi) mengubah tiap kata menjadi representasi makna numerik.
  3. **LSTM Dua Arah (*Bidirectional*):** Jaringan membaca kalimat dari kiri ke kanan **dan** dari kanan ke kiri secara bersamaan (`hidden_dim = 64`, `dropout = 0,3`). Pembacaan dua arah sangat berguna untuk menangkap frasa negasi seperti *"não chegou"* (tidak sampai) atau konteks keluhan spesifik.
  4. Ukuran modelnya tetap super ringan (**~1,03 MB**) dan berjalan di CPU tanpa GPU.

### 3. K-Means Clustering (`BehavioralClusterer`) — Pengelompokan Pelanggan

- **Cara Kerja Secara Mudah (`src/csip/discovery/clusterer.py`):** Algoritma *unsupervised* yang membagi pelanggan berdasarkan kemiripan 5 ciri perilaku belanja (total belanja, frekuensi transaksi, beban ongkos kirim, rata-rata skor ulasan, dan keterlambatan) tanpa diberi label terlebih dahulu. Fitur lebih dulu disamakan skalanya (`StandardScaler`) supaya variabel nilai uang ratusan Real tidak mendominasi angka frekuensi pesanan. Diperoleh **4 klaster perilaku** dengan kualitas pemisahan terukur **Silhouette Score `0,4180`**.

### 4. Analisis Survival Kaplan-Meier & Model Tren Mingguan (`WorldStateTransitionModel`)

- **Kaplan-Meier (`src/csip/evaluation/survival_analysis.py`):** Menjawab pertanyaan *"berapa peluang pelanggan belum melakukan pembelian ulang atau belum mengalami kejadian tertentu hingga hari ke-t?"* sambil tetap memperhitungkan pelanggan yang masa pengamatannya berakhir sebelum kejadian muncul (*right-censored data*). Dilengkapi juga evaluasi `Harrell's C-index` dan `DecisionCurveAnalysis` untuk menimbang manfaat bersih (*Net Benefit*).
- **Model Transisi Makro Mingguan (`src/csip/world/state_transition.py`):** Menggunakan model deret waktu multivariat (*Ridge-Regularized Vector Autoregression / VAR(1)* dengan parameter regularisasi `alpha = 0,1`) yang menghubungkan 4 indikator mingguan sekaligus: volume pesanan mingguan (`weekly_order_volume`), rata-rata hari telat (`mean_delivery_delay`), rata-rata rasio ongkir (`mean_freight_ratio`), dan tingkat ulasan negatif (`negative_review_rate`). Tujuannya membantu manajemen melihat proyeksi efek berantai jika volume pesanan melonjak di musim puncak. Pengujian stabilitas menunjukkan sistem simulasi bersifat stabil (*tidak meledak tak terkendali saat disimulasikan beberapa minggu ke depan*).

---

# BAB 5 — HASIL EMPIRIS SELURUH MODEL, KEJUJURAN ILMIAH & AUDIT ANGKA

## 5.1 Panduan Cepat Membaca Metrik Evaluasi bagi Non-Teknis & Data Scientist

Mengapa CSIP tidak menonjolkan **Accuracy** (persentase tebakan benar)? Karena pada kasus ketimpangan kelas (hanya **9,63%** ulasan buruk pada data uji terkunci), model malas yang selalu menebak *"Semua Pelanggan Puas"* sudah langsung mendapat **Accuracy 90,37%** — padahal model itu gagal total mendeteksi satu pun pelanggan kecewa!

Sebagai gantinya, CSIP memakai metrik yang tepat untuk masalahnya:

- **PR-AUC (*Precision-Recall Area Under Curve*):** Metrik paling jujur untuk kasus kelas minoritas langka. Pembanding dasarnya adalah angka *base rate* (misal `0,0963`). Jika PR-AUC mencapai `0,3061`, artinya kemampuan model menyaring keluhan lebih dari **3 kali lipat** lebih baik dibanding memilih secara acak.
- **ROC-AUC:** Mengukur seberapa bagus model memberi peringkat risiko lebih tinggi kepada pesanan bermasalah dibanding pesanan aman (`0,50` = tebakan acak lempar koin; semakin mendekati `1,0` semakin tajam).
- **MAE (*Mean Absolute Error*) & RMSE:** Rata-rata selisih tebakan dalam satuan hari (untuk prediksi keterlambatan pengiriman). Semakin kecil semakin akurat.
- **Brier Score & ECE (*Expected Calibration Error*):** Mengukur apakah angka persentase peluang yang dikeluarkan model benar-benar bisa dipercaya. (Jika model bilang risiko 20%, apakah betul sekitar 20% dari kelompok itu memberi bintang 1–2? Semakin mendekati `0`, semakin terkalibrasi).

## 5.2 Tabel Rekap Hasil Empiris Seluruh Model (Data Uji Masa Depan Terkunci)

Seluruh angka di bawah ini diambil langsung dari audit kode pada `artifacts/reports/locked_test_reevaluation.json`, `artifacts/reports/model_explainability.json`, dan `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv`.

| Nama Model & Artefak | Tugas & Pos Waktu | Populasi Uji | Hasil Metrik Utama | Kalibrasi & Catatan | Status Tata Kelola |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `best_negative_review_lightgbm.joblib` | Klasifikasi Ulasan Negatif, **Pos T2** (15 fitur) | `N = 12.571` (`> 2018-06-30`), *base rate* `9,63%` | **PR-AUC: `0,3061`** (`95% CI: 0,2792–0,3343`)<br>**ROC-AUC: `0,6745`** (`95% CI: 0,6556–0,6926`) | Brier mentah: `0,1373` (ECE `0,2349`). Setelah **Platt Scaling**: Brier **`0,0762`**, ECE **`0,0070`**. | **`PILOT_ELIGIBLE`** *(Wajib pakai Platt Calibrator)* |
| `best_early_warning_review_lightgbm.joblib` | Klasifikasi Ulasan Negatif, **Pos T0 Checkout** (10 fitur) | `N = 12.571` (`> 2018-06-30`), *base rate* `9,63%` | **PR-AUC: `0,1335`** (`95% CI: 0,1220–0,1480`)<br>**ROC-AUC: `0,5468`** (`95% CI: 0,5291–0,5648`) | Brier mentah: `0,2370`. Sinyal masih lemah karena kurir belum jalan saat bayar. | **`PILOT_RESTRICTED`** *(Hanya untuk pemeringkatan ringan)* |
| `best_delivery_delay_lightgbm.joblib` | Regresi Hari Keterlambatan, **Pos T1** (5 fitur) | `N = 12.630` (`> 2018-06-30`) | **MAE: `4,83` hari** (`4,8256`)<br>**RMSE: `6,25` hari** (`6,2458`)<br>**R²: `0,3926`** | Baseline median latih MAE `6,69` hari — memangkas error absolut **27,9%**. | **`PRODUCTION_APPROVED`** |
| `text_bilstm_review_sentiment.pt` | Deep Learning NLP Teks Ulasan, **Pos T2** | `N = 4.142` ulasan bertulis teks | **Macro-F1: `0,8420`**<br>**Accuracy: `0,8870`** | Khusus pada subset ulasan yang memiliki komentar tertulis (`16,2%` negatif). | **`PRODUCTION_CANDIDATE`** *(Triage teks keluhan)* |
| `world_model_state_transition.joblib` | Simulasi Tren Makro Mingguan VAR(1) Ridge | Panel mingguan agregat | **AIC: `-4,8920`**, **BIC: `-4,5120`**<br>Indeks stabilitas: **`0,8412`** (< `1,0`) | Simulasi stabil multi-minggu (meredam guncangan musiman kembali ke titik normal). | **`APPROVED FOR SIMULATION`** |
| `clustering_pipeline.joblib` | Segmentasi Pelanggan K-Means (K=4) | Profil pelanggan Olist | **Silhouette Score: `0,4180`** | Membentuk 4 persona segmen dengan perbedaan perilaku nilai transaksi & gesekan ongkir. | **`PRODUCTION_APPROVED`** *(Segmentasi)* |
| `best_repeat_purchase_lightgbm.joblib` | Klasifikasi Pelanggan Belanja Ulang, **Pos T0** | Holdout out-of-time | **ROC-AUC: `0,5021`** (`95% CI: 0,472–0,531`) | Rentang kepercayaan melewati `0,50` (setara tebakan acak). | **`REJECTED FOR DEPLOYMENT`** *(Valid Negative Finding)* |
| `best_repeat_purchase_post_delivery_lightgbm.joblib` | Klasifikasi Belanja Ulang, **Pos T2** | Holdout 30 hari | **ROC-AUC: `0,5284`** (`PR-AUC: 0,0245`) | Sinyal terlalu lemah untuk dipakai menarget promo otomatis. | **`RESEARCH_ONLY`** |

## 5.3 Mengapa Penolakan Model *Repeat Purchase* Justru Kekuatan Besar Proyek Ini?

Pada kebanyakan portofolio Data Science, semua model dipaksa terlihat berhasil. Di CSIP, model prediksi pelanggan belanja ulang (`repeat_purchase_flag`) menghasilkan **ROC-AUC `0,5021`** dengan batas bawah kepercayaan `0,472` — secara statistik hampir tidak berbeda dengan melempar koin.

Mengapa ini terjadi? Secara bisnis di dataset Olist, mayoritas pembeli hanyalah pembeli satu kali (*single-purchase marketplace shoppers*, ~97% pelanggan hanya belanja 1 kali dalam rentang data yang tersedia) dan sistem tidak memiliki data klik penelusuran (*browsing behavior*), kupon yang diterima, atau penghasilan pelanggan.

Alih-alih memanipulasi data uji agar angkanya naik, CSIP **secara resmi memberi status `REJECTED FOR DEPLOYMENT`** dan menetapkannya sebagai **Valid Negative Finding**. Ini membuktikan kepada manajemen dan asesor teknis bahwa proyek ini mengutamakan kejujuran ilmiah dan melindungi perusahaan agar tidak membakar anggaran promosi memakai model yang tidak bekerja.

## 5.4 Rekonsiliasi Transparan Angka Audit Internal

Selama audit kualitas, CSIP merapikan tiga catatan angka historis agar tidak ada kebingungan:

1. **Early Warning PR-AUC `0,2845` vs `0,1335`:** Catatan ringkas lama sempat menulis PR-AUC `0,2845`, padahal pengujian langsung pada file `.joblib` asli (`best_early_warning_review_lightgbm.joblib`) dan `ml_leaderboard.json` menunjukkan **PR-AUC `0,1335`** (`ROC-AUC 0,5468`). Angka `0,1335` inilah yang masuk akal karena keterlambatan kurir memang belum terjadi saat checkout. Seluruh dokumen & manifest telah dikoreksi memakai `0,1335`.
2. **Brier Score `0,1373` vs `0,0762`:** File `.joblib` mentah memberi output rata-rata probabilitas `0,3312` (`Brier 0,1373`) karena efek pembobotan kelas seimbang (*balanced weight*) saat training. Setelah dilewatkan kalibrator **Platt Scaling**, skor Brier turun drastis ke **`0,0762`** dan ECE turun ke **`0,0070`**.
3. **Perbedaan Ukuran Sampel Uji (`N=12.571` vs `N=12.448` vs `N=39.153`):**
   - `12.571`: evaluasi ulang langsung model `.joblib` (`locked_test_reevaluation.json`) pada semua pesanan `> 30 Juni 2018`.
   - `12.448` (PR-AUC `0,3151` / ROC-AUC `0,6975`): output pipeline eksperimen CV temporal (`temporal_cv_results.json`) dengan penyaringan fitur tambahan.
   - `39.153` (PR-AUC `0,7517`): analisis irisan subgroup (`MODEL_ROBUSTNESS_AND_SLICE_ANALYSIS.md`) pada rentang waktu lebih panjang sejak `> 1 Maret 2018` yang mencakup periode gangguan logistik besar sehingga proporsi kasus positif dan variasi sinyalnya lebih besar.

---

# BAB 6 — KALIBRASI PROBABILITAS (PLATT SCALING), PENJELASAN SHAP & KETAHANAN LINTAS WILAYAH

## 6.1 Masalah Probabilitas "Lebay" & Cara Kerja Platt Scaling

**Analogi Non-Teknis:** Agar model peka mendeteksi ulasan negatif yang jumlahnya sedikit (~9,6%), saat latihan kita memberi bobot penalti hampir 9 kali lebih besar tiap kali model melewatkan kasus kecewa (`class_weight="balanced"`). Efek sampingnya: model menjadi terlalu parno! Rata-rata skor mentahnya membengkak ke **33,12%**, padahal kenyataan aslinya hanya **9,63%**. Jika manajer langsung memakai skor mentah ini, tim CS akan kewalahan mengejar peringatan palsu.

**Solusi: Platt Scaling (`src/csip/evaluation/explainer.py`)**  
Pada dataset validasi (`April–Juni 2018`, bukan data uji!), CSIP memasang lapisan regresi logistik pengkalibrasi di atas skor mentah model (`koefisien = 0,9020`, `intersep = -1,8089`) yang mengecilkan dan meluruskan skor prediksi agar sejalan dengan persentase kejadian sebenarnya.

**Hasil Terukur (`model_explainability.json`):**

| Metrik Kalibrasi | Sebelum Kalibrasi (Raw `.joblib`) | Sesudah Platt Scaling | Peningkatan Kualitas |
| :--- | :---: | :---: | :---: |
| **Brier Score** *(lebih rendah = lebih akurat secara peluang)* | `0,1375` | **`0,0762`** | Membaik **44,59%** |
| **Expected Calibration Error / ECE** *(selisih rata-rata peluang vs realita)* | `0,2355` (meleset 23,5%) | **`0,0070`** (meleset hanya 0,7%) | Membaik **97,02%** |

## 6.2 Membuka Kotak Hitam dengan SHAP & Disiplin Klaim Ilmiah

Agar manajemen percaya pada prediksi LightGBM, modul `ModelExplainer` menjalankan **SHAP TreeExplainer** pada sampel terkendali **800 pesanan** (dipilih 800 agar perhitungan selesai kurang dari 1 detik pada RAM 8 GB). Peringkat teratas pendorong keputusan model Pos T2 pada `model_explainability.json` adalah:

1. **`delivery_delay_days` (Mean |SHAP| `0,3058`)** — Faktor paling dominan (hampir sepertiga dari seluruh bobot pengaruh model!).
2. **`delivery_lead_time_days` (`0,2252`)** — Total durasi tunggu sejak bayar hingga paket sampai.
3. **`item_count` (`0,2086`)** — Keranjang berisi banyak item punya risiko gesekan pengemasan/kelengkapan lebih tinggi.
4. **`estimated_lead_time_days` (`0,0740`)** dan **`total_freight` (`0,0701`)**.

**Batas Kejujuran Klaim (Level L1/L2 vs Level L3):**  
CSIP dengan tegas mencatat di dokumentasi dan UI bahwa skor SHAP adalah **bukti asosiatif/prediktif** tentang bagaimana model mengambil keputusan dari data historis — **bukan bukti sebab-akibat kausal**. Untuk membuktikan berapa persen komplain benar-benar turun akibat suatu kebijakan baru, tetap dibutuhkan uji coba terkontrol (*A/B testing*).

## 6.3 Uji Ketahanan Lintas Wilayah & Segmen (`src/csip/evaluation/robustness.py`)

Model yang bagus di kota besar São Paulo bisa saja kacau di wilayah terpencil. Oleh karena itu `evaluate_negative_review_slices` memecah performa uji model berdasarkan:

1. **Negara Bagian Utama (`customer_state`):** `SP`, `RJ`, `MG`, `RS`, `PR` (syarat uji minimal 50 sampel dan kedua kelas label muncul).
2. **Tier Nilai Keranjang (`total_order_value`):** Kategori Rendah (`< BRL 60`), Sedang (`BRL 60–150`), dan Tinggi (`> BRL 150`).
3. **Status Keterlambatan (`is_late`):** Menguji apakah model masih bisa membedakan potensi keluhan *bahkan di antara paket yang datang tepat waktu* (bukan sekadar menjadi saklar tunggal "telat = marah").

---

# BAB 7 — BUSINESS DECISION ENGINE: MENGUBAH PREDIKSI JADI AKSI, KUOTA TIM CS & RANCANGAN UJI A/B

## 7.1 Mengapa Angka `0,72` Saja Belum Bisa Dieksekusi oleh Tim Operasional?

Jika komputer hanya mencetak *"Pesanan #9941 berisiko 72%"*, staf operasional masih bingung: siapa yang harus bertindak, apa isi tindakannya, berapa biayanya, dan kapan harus berhenti agar tim tidak kehabisan waktu?

Modul `src/csip/decision_engine/` memecahkan masalah ini dengan memisahkan secara tegas empat hal berbeda:

1. **Probabilitas Model:** Angka peluang risiko terkalibrasi (misalnya `72%`).
2. **Estimasi Keterlambatan:** Prakiraan hari meleset dari model regresi (misalnya `+8,5 hari`).
3. **Tingkat Prioritas Bisnis (`DecisionPriority`):** Menggabungkan tingkat risiko dengan nilai ekonomi keranjang belanja (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
4. **Paket Rekomendasi Operasional:** Kontrak struktur data `DecisionRecommendation` berisi **12 informasi wajib** (`decision_id`, masalah bisnis, entitas pesanan, bukti numerik, prioritas, faktor pemicu beserta ambang batasnya, tindakan konkret, fungsi penanggung jawab seperti `Logistics & Fulfillment` atau `Customer Experience & Retention`, sasaran operasional, KPI evaluasi, keterbatasan bukti, serta status & jenis bukti).

## 7.2 Kalibrasi Ambang Batas Berdasarkan Kapasitas Tim (`calibrate_thresholds_from_capacity`)

Salah satu fitur paling praktis di `src/csip/decision_engine/engine.py` adalah penyesuaian ambang peringatan terhadap kapasitas nyata tim manusia:

- Misalkan tim CS hanya sanggup menghubungi maksimal **10% pesanan teratas** (`max_alert_rate = 0,10`) atau maksimal `100` pesanan per batch.
- Metode `calibrate_thresholds_from_capacity()` melihat sebaran probabilitas pada data validasi lalu otomatis menghitung batas persentase risiko persis untuk top 10% (`risk_probability_threshold`) serta batas `CRITICAL` untuk sepertiga teratasnya (`critical_risk_probability_threshold`), lengkap dengan laporan presisi aktual dan *lift* atas baseline.
- Saat `generate_recommendations()` dijalankan, seluruh pesanan diurutkan berdasarkan prioritas (`CRITICAL > HIGH > MEDIUM > LOW`) dan dipotong rapi sesuai batas kuota harian agar tim CS terhindar dari kelelahan peringatan (*alert fatigue*).

## 7.3 Rancangan Uji A/B Holdout (`design_ab_holdout_plan`)

Karena biaya membiarkan pelanggan kecewa hingga berhenti belanja jauh lebih mahal dibanding biaya pesan proaktif atau kompensasi kecil, CSIP menggunakan matriks prioritas berbasis nilai pesanan. Namun perusahaan tidak boleh sekadar *berasumsi* intervensi berhasil.

Oleh karena itu `BusinessDecisionEngine.design_ab_holdout_plan()` otomatis membagi pesanan berisiko tinggi yang lolos kuota secara acak terkendali (`seed` tetap) menjadi:

- **80% Grup Treatment:** Menerima tindakan proaktif (misalnya pesan pemberitahuan keterlambatan via WhatsApp/SMS, eskalasi kurir ekspres, atau voucher jaminan).
- **20% Grup Control Holdout:** Sengaja tidak diintervensi sebagai kelompok pembanding adil. Setelah siklus pengiriman selesai, tingkat ulasan negatif kedua kelompok diukur agar efektivitas program terbukti secara nyata, bukan kira-kira.

---

# BAB 8 — UNIVERSAL CSV STUDIO (`ml_engine.py` & `semantic_profiler.py`): ANALITIK LINTAS BIDANG

## 8.1 Mengapa Pengguna Bisa Mengunggah CSV Apa Saja di CSIP Studio?

Sesuai arsitektur dua lapis di Bab 1, selain model khusus Olist, pengguna akhir sering membawa data tabel dari luar e-commerce — misalnya data medis pasien, data kualitas produksi pabrik, kinerja SDM, atau transaksi bisnis umum.

Jika CSV sembarang dianalisis secara serampangan, dua error klasik sering terjadi: (1) kolom target Ya/Tidak (`0/1`) keliru dimodelkan seperti regresi biasa, dan (2) sistem diam-diam membocorkan informasi saat imputasi atau mengevaluasi model pada data latih yang sama (*in-sample overfitting*).

Modul `src/csip/models/ml_engine.py` dan `src/csip/data/semantic_profiler.py` membangun alur otomatis 4 tahap yang tetap disiplin secara ilmiah:

## 8.2 Alur Teknis 4 Tahap Ketika File CSV/Excel Diunggah

1. **Tahap 1 — Pemetaan Bahasa Alami 11 Sektor Industri (`semantic_profiler.py`):**  
   Mencocokkan nama kolom ke kamus `NATURAL_LEXICON` (mencakup keuangan, akuntansi, e-commerce, SDM, pemasaran digital, kesehatan, mutu manufaktur, dll.) untuk membentuk label manusiawi, satuan ukuran (`Rp`, `$`, `%`, `hari`, `poin`), dan kalimat penjelas arah tren. Skala rating 1–5 otomatis dinormalkan ke skala 0–100 agar mudah dibandingkan.

2. **Tahap 2 — Audit Kualitas Data & Radar Kebocoran (`perform_exploratory_data_analysis` & `detect_split_strategy`):**  
   Menghitung persentase data kosong, tingkat kemiringan sebaran, jumlah outlier IQR, dan baris duplikat. Sistem juga memindai nama kolom untuk memberi peringatan kebocoran:
   - Kolom mengandung kata waktu (`date`, `time`, `timestamp`, `year`, `month`) → memperingatkan kebutuhan **`TEMPORAL_HOLDOUT`** (pemecahan berbasis urutan waktu).
   - Kolom mengandung identitas entitas (`id`, `customer`, `seller`, `user`, `client`) → memperingatkan kebutuhan **`GROUP_AWARE_SPLIT`**.

3. **Tahap 3 — Routing Otomatis Klasifikasi vs Regresi, *Split-Before-Transform* & Validasi Silang (`train_fluent_ml_pipeline`):**
   - **Deteksi Tugas Otomatis:** Jika kolom target hanya berisi dua nilai unik `{0, 1}`, mesin otomatis masuk mode **Klasifikasi Biner** (`LogisticRegression` sebagai baseline vs `RandomForestClassifier` sebagai model utama, menampilkan *PR-AUC*, *ROC-AUC*, dan *Brier Score*). Jika berupa angka kontinu, masuk mode **Regresi** (`Ridge` sebagai baseline vs `RandomForestRegressor`, menampilkan *MAE*, *RMSE*, dan *R²*).
   - **Larangan Mengintip Data Uji (*Split-Before-Transform*):** Pengisian data kosong (`SimpleImputer` median) dan penyaringan kolom redundan (korelasi antar-fitur `> 0,94` atau duplikat target `> 0,992`) dihitung **hanya dari bagian data latih**, lalu barulah diterapkan ke data uji.
   - **Evaluasi *Out-of-Sample K-Fold CV*:** Jika baris mencukupi (`N >= 15`), menjalankan 2 hingga 5 lipatan *Cross-Validation* untuk menghasilkan rata-rata dan rentang variasi skor (`mean ± std`). Jika baris terlalu sedikit (`N < 8`), UI dengan jujur melabelinya sebagai `IN_SAMPLE_FALLBACK_SMALL_N`.

4. **Tahap 4 — Simulasi Interaktif & Interval Ketidakpastian 90%:**  
   Saat pengguna menggeser *slider* fitur, fungsi simulator memanggil peluang probabilitas kontinu (`predict_proba`) untuk klasifikasi atau nilai prediksi (`predict`) untuk regresi, sekaligus menghitung **rentang perkiraan 90% (*prediction interval [persentil 5, persentil 95]*)** dari sebaran ratusan pohon di dalam `RandomForest`. Titik belok kurva simulasi ditandai jujur sebagai panduan eksplorasi visual (*ceteris paribus*), bukan klaim sebab-akibat mutlak.

---

# BAB 9 — MLOPS, OBSERVATORIUM DRIFT REAL-TIME & SIKLUS PROMOSI CHAMPION-CHALLENGER

## 9.1 Mengapa Model yang Hari Ini Bagus Bisa Menurun Bulan Depan?

Model Machine Learning tidak pernah "selesai sekali jalan". Ketika terjadi lonjakan belanja akhir tahun (*Black Friday*), pergantian mitra kurir, atau inflasi biaya kirim, distribusi data produksi hari ini mulai bergeser menjauhi distribusi data waktu model dulu dilatih. Inilah yang disebut **Data Drift**.

## 9.2 Empat Radar Statistik pada `DriftEngine` (`src/csip/monitoring/drift_engine.py`)

CSIP menghitung empat indikator pergeseran tanpa memerlukan server streaming berat:

1. **Population Stability Index (PSI):** Membagi data acuan lama ke dalam 10 kelompok kuantil dan membandingkan porsi per kelompok terhadap data baru (dilengkapi perlindungan angka nol *Laplace smoothing*). Lampu statusnya sangat mudah dipahami tim operasional:
   - **PSI `< 0,10` → `STABLE` (Hijau):** Distribusi data masih konsisten dengan masa latih.
   - **`0,10 <=` PSI `< 0,25` → `WARNING` (Kuning):** Mulai ada pergeseran pola, perlu diawasi.
   - **PSI `>= 0,25` → `CRITICAL_DRIFT` (Merah):** Distribusi berubah signifikan, model perlu dievaluasi ulang atau dilatih ulang.
2. **Uji Kolmogorov-Smirnov (KS-Test):** Menguji secara statistik (batas signifikansi `alpha = 0,05`) apakah kedua sampel masih berasal dari distribusi yang sama.
3. **Jarak Wasserstein (*Earth Mover's Distance*):** Mengukur seberapa jauh "pergeseran rata-rata dan sebaran" sebuah variabel bergeser secara metrik (berguna saat PSI jenuh karena outlier).
4. **Jensen-Shannon Divergence (JSD):** Mengukur apakah distribusi probabilitas output prediksi model sendiri ikut bergeser.

## 9.3 Tata Kelola Pelatihan Ulang: Gerbang Champion vs Challenger

Pada `src/csip/monitoring/retrainer.py` (`SlidingWindowRetrainer`) dan `src/csip/models/registry.py` (`ModelLifecycleManager`), model yang dilatih ulang (**Challenger**) **dilarang keras langsung menimpa** model aktif di produksi (**Champion**).

Aturan promosi di CSIP berjalan ketat:

1. Kedua model diadu pada data uji terbaru secara *head-to-head*.
2. **Syarat Promosi (`PROMOTED`):** Challenger hanya boleh menggantikan Champion jika meningkatkan metrik utama minimal **+1,0%**, sekaligus tidak memperburuk kalibrasi (`Brier Score`) lebih dari **5%**.
3. Jika syarat gagal, sistem mencatat status **`RETAINED`** (Champion lama tetap dipertahankan), menyimpan log historisnya ke `PROMOTION_HISTORY.csv`, dan selalu menyediakan tombol pemulihan cepat (*rollback*) lewat sidik jari **SHA-256** setiap versi artefak.

---

# BAB 10 — LAYANAN MIKRO FASTAPI, KOKPIT STREAMLIT, PENGUJIAN OTOMATIS & 12 GERBANG KUALITAS

## 10.1 Layanan Mikro FastAPI (`src/csip/api/server.py` & `client.py`)

Dalam arsitektur rekayasa perangkat lunak yang sehat, tampilan grafik UI tidak boleh menjadi pintu masuk bagi sistem transaksi eksternal untuk meminta prediksi. Oleh karena itu CSIP memisahkan peladen API `FastAPI` di port `8000` (lengkap dengan validasi skema ketat Pydantic dan pelacakan `X-Request-ID`):

| Endpoint API | Kegunaan Operasional | Penjagaan Teknis |
| :--- | :--- | :--- |
| `GET /health` & `GET /ready` | Memeriksa kesehatan server, versi `1.1.0`, dan kesiapan model di memori. | Menolak trafik jika model utama belum termuat (*readiness probe*). |
| `POST /predict/early-warning` | Meminta skor risiko saat pesanan baru dibayar (**Pos T0**). | Hanya mengizinkan **10 fitur T0**; menolak kolom pasca-kirim. |
| `POST /predict/post-fulfillment` | Menganalisis penyebab risiko setelah paket terkirim (**Pos T2**). | Menerima **15 fitur T2** secara lengkap. |
| `POST /predict/batch` | Menilai ribuan pesanan sekaligus sambil mencatat waktu eksekusi (`ms`). | Memblokir model berstatus `RESEARCH_ONLY` agar tidak masuk operasi nyata. |
| `POST /decisions/recommend` | Mengubah batch pesanan menjadi daftar tindakan dari `BusinessDecisionEngine`. | Memotong otomatis sesuai kapasitas harian tim CS. |
| `GET /models/registry` | Menampilkan daftar model, metrik uji, dan riwayat status `Champion`. | Mengambil langsung dari `MODEL_RESULTS_REGISTRY.csv`. |
| `POST /monitor/drift` | Mengecek PSI, KS, dan Wasserstein antara batch data baru dan acuan. | Mengembalikan status `STABLE` / `WARNING` / `CRITICAL_DRIFT`. |

## 10.2 Kokpit Interaktif CSIP Studio (`app/streamlit_app.py`)

Antarmuka utama di `port 8501` dirancang agar orang non-teknis maupun analis dapat mengoperasikan sistem dengan satu layar terpadu yang bersih:

- **Panel Kontrol Kiri (Sumber Data & Tuas Simulasi):**
  1. Unggah berkas **CSV atau Excel (`.xlsx`, `.xls`)** milik sendiri, **atau** pilih langsung 3 kasus bawaan: *Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)*, *Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)*, dan *Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)*.
  2. Pilih variabel target pada menu **"Yang ingin dioptimalkan"**, disertai kotak terjemahan awam **"Artinya begini"**.
  3. **Tuas Simulasi Top-3:** 3 *slider* interaktif untuk 3 faktor paling berpengaruh beserta tombol **Setel ulang**.
- **Panggung Kanan (Hasil & 4 Lensa Analitik + Penasihat Nara):**
  - **3 Kartu Bento KPI:** Estimasi hasil terkini, faktor penentu terkuat beserta persentase pengaruhnya, dan selisih dari standar acuan.
  - **4 Lensa Tampilan Interaktif:**
    - **Lensa `1. Kurva Simulasi dan Titik Kritis`:** Grafik respons prediksi terhadap perubahan faktor dominan plus penanda titik perubahan tajam.
    - **Lensa `2. Peringkat Faktor Penentu`:** Urutan persentase kekuatan pengaruh dan arah korelasi seluruh fitur.
    - **Lensa `3. Sebaran Kelompok Data`:** Perbandingan distribusi populasi di tiap tingkatan faktor utama.
    - **Lensa `4. Observatorium Drift & Stabilitas`:** Audit kualitas distribusi dan status stabilitas PSI.
  - **Kartu Penasihat Strategi "Nara":** Narasi otomatis yang menerjemahkan grafik statistik menjadi bahasa rekomendasi bisnis yang mudah dipahami manajer tanpa menghilangkan catatan batasan ketidakpastian model.

Sementara itu, modul [data_provider.py](file:///c:/Users/asus/.gemini/antigravity/scratch/csip/app/data_provider.py) memastikan laporan audit Olist dibaca langsung dari artefak JSON/CSV terverifikasi di `artifacts/` (bukan angka ketik manual).

## 10.3 Pengujian Otomatis, Jejak Memori, 12 Gerbang Kualitas & SKKNI Level 7

- **Kebutuhan Sumber Daya Nyata (`artifacts/reports/resource_benchmark.json`):** Saat memuat sampel 1.000 baris dan ke-3 model LightGBM inti di laptop CPU standar, total pemakaian RAM proses terukur hanya **263,68 MB** (`tracemalloc` puncak **51,57 MB**), jauh di bawah batas target laptop RAM 8 GB. Latensi penilaian batch 1.000 baris berkisar **4,33–13,02 milidetik**.
- **216 Pengujian Otomatis (`tests/`, 39 Berkas):** Mencakup test kebocoran waktu & embargo 90 hari, test kontrak data korup, test keabsahan regresi/klasifikasi `ml_engine`, test stabilitas model makro, test API FastAPI, test `AppTest` Streamlit untuk ke-4 lensa, hingga test pemindai klaim berlebihan.
- **12 Gerbang Kualitas Rilis (`tools/verify_release.py`):**

| Kode | Nama Gerbang Verifikasi | Apa yang Dicek Otomatis |
| :---: | :--- | :--- |
| **G1** | Single Version Truth | Versi `1.1.0` seragam di seluruh kode, `pyproject.toml`, dan manifest. |
| **G2** | Zero Failed Tests | Eksekusi test lulus bersih tanpa ada yang gagal. |
| **G3** | Clean Claims & Anti-Overclaim | `tools/check_claims.py` memastikan 0 kalimat klaim berlebihan/palsu. |
| **G4** | Preregistration & Frozen Plan | Rencana analisis terkunci di `config/analysis_plan.yaml` belum diubah diam-diam. |
| **G5** | Valid Rolling-Origin Temporal CV | Bukti 4 fold mengembang dengan embargo 90 hari ada di artefak laporan. |
| **G6** | Single Evaluation Locked Test | Pengujian akhir sekali jalan pada holdout `> 2018-06-30` terverifikasi. |
| **G7** | Estimand Population Scope | Audit penyusutan populasi dan batas non-responden tercatat jujur. |
| **G8** | Tested Dashboard with Provenance | Kokpit Streamlit lolos simulasi `AppTest` di semua 4 lensa. |
| **G9** | Rerunable Competency Evidence | Seluruh **63 Kriteria Unjuk Kerja (KUK) SKKNI Level 7** di `CANONICAL_EVIDENCE_REGISTRY.csv` dicek keberadaannya & hash-nya (0 file hilang). |
| **G10** | One-Command Reproduction | Skrip reproduksi lengkap & audit 14 notebook riset tersedia dan lengkap. |
| **G11** | CI Multi-Version Workflow | Konfigurasi GitHub Actions lintas versi Python tersedia di `.github/workflows/ci.yml`. |
| **G12** | Honest Competency Provenance | Memisahkan jujur status `VERIFIED` (35 KUK), `ARTIFACT_ONLY` (12 KUK), `CANDIDATE_DEMONSTRATION_REQUIRED` (13 KUK), dan `EXTERNAL_CONFIRMATION_REQUIRED` (3 KUK). |

## 10.4 Peta Bedah Modul Kode Sumber (`src/csip/` & Skrip Pendukung)

Bagi pengembang atau penguji teknis yang ingin langsung membuka bagian kode tertentu, berikut peta lengkap berkas utama CSIP beserta tanggung jawab spesifiknya:

| Jalur File / Modul | Simbol Kelas & Fungsi Kunci | Logika Teknis yang Dijalankan |
| :--- | :--- | :--- |
| `src/csip/data/loader.py` | `downcast_dataframe` | Menurunkan presisi `float64`/`int64` ke tipe paling ringkas agar dataset tetap aman di RAM 8 GB. |
| `src/csip/data/contracts.py` | `DataContract`, `ValidationReport`, `ContractSeverity` | Memvalidasi skema & primary key ke dalam 4 tingkat keparahan dan menghentikan pipeline jika terjadi `CRITICAL_FAILURE`. |
| `src/csip/data/lineage.py` | Pencatat SHA-256 Lineage | Merekam sidik jari file mentah hingga tabel Parquet akhir ke `DATA_LINEAGE.json`. |
| `src/csip/cleaning/cleaner.py` | `OlistDataCleaner`, `CleaningStepReport` | Menyaring koordinat GPS ke wilayah Brasil, agregasi item/pembayaran/ulasan ke `order_id`, menjaga `has_observed_review`. |
| `src/csip/features/engineer.py` | `FeatureEngineer`, `haversine_np` | Menghitung jarak geografis pembeli-penjual, rasio ongkir, interaksi keterlambatan, dan riwayat belanja *backward-looking*. |
| `src/csip/evaluation/temporal_cv.py` | `RollingOriginTemporalCV`, `TemporalFold` | Membagi 4 lipatan validasi silang ekspansi dengan syarat jeda embargo minimal 90 hari. |
| `src/csip/models/classic.py` & `trainer.py` | `MajorityClassClassifier`, `DelayHeuristicClassifier`, `ModelExperimentTrainer` | Menjalankan eksperimen Tangga Baseline B0–B4 per himpunan fitur terisolasi (`E1` T0 vs `E3` T2). |
| `src/csip/models/deep_seq.py` | `SimpleTokenizer`, `TextBiLSTM` | Tokenisasi komentar bahasa Portugis (maks 5.000 kata, panjang 50 token) dan klasifikasi sentimen 2 arah di CPU. |
| `src/csip/evaluation/explainer.py` | `ModelExplainer`, `compute_ece` | Melatih Platt Scaling di partisi validasi, mengukur penurunan Brier/ECE, dan menjalankan SHAP `TreeExplainer` (800 sampel). |
| `src/csip/evaluation/robustness.py` | `evaluate_negative_review_slices` | Menguji konsistensi performa per negara bagian, kuantil nilai transaksi, dan kondisi `is_late`. |
| `src/csip/evaluation/survival_analysis.py` | `KaplanMeierEstimator`, `calculate_concordance_index` | Analisis kurva survival pada data tersensor serta evaluasi manfaat bersih keputusan. |
| `src/csip/discovery/clusterer.py` | `BehavioralClusterer`, `ClusterProfile` | Segmentasi K-Means (`K=4`) dengan `StandardScaler` untuk pemetaan persona pelanggan. |
| `src/csip/world/state_transition.py` | `WorldStateTransitionModel` | Simulasi kebijakan makro mingguan berbasis VAR(1) Ridge dan verifikasi kestabilan rollout. |
| `src/csip/decision_engine/rules.py`, `engine.py`, `schemas.py` | `DecisionRuleEvaluator`, `BusinessDecisionEngine`, `DecisionRecommendation` | Mengubah skor menjadi prioritas bisnis, mengkalibrasi batas sesuai kapasitas CS, dan mempartisi uji A/B 80/20. |
| `src/csip/models/ml_engine.py` & `semantic_profiler.py` | `train_fluent_ml_pipeline`, `perform_exploratory_data_analysis`, `NATURAL_LEXICON` | Mesin otomatis CSV Studio: kamus 11 sektor, radar kebocoran tanggal/ID, auto-routing tugas, CV tanpa kebocoran, & interval 90%. |
| `src/csip/monitoring/drift_engine.py`, `retrainer.py`, `registry.py` | `DriftEngine`, `SlidingWindowRetrainer`, `ModelLifecycleManager` | Radar PSI/KS/Wasserstein/JSD serta gerbang promosi ketat Champion-Challenger (+1% lift, degradasi Brier <= 5%). |
| `src/csip/api/server.py` | Aplikasi `FastAPI` (7 rute endpoint HTTP) | Menyediakan endpoint `/`, `/health`, `/ready`, `/predict/batch`, `/decisions/recommend`, `/monitor/drift`, dan `/models/registry` beserta HTTP middleware. |
| `tools/verify_release.py` & `check_claims.py` | Mesin Verifikasi 12 Gerbang & Scanner Anti-Overclaim | Menjamin integritas versi, pengujian, hash, klaim bahasa, dan bukti 63 KUK sebelum rilis atau pengemasan `.zip`. |

---

# BAGIAN II — SKRIP PRESENTASI MASTER & PANDUAN TANYA-JAWAB (BAB 11 s/d BAB 14)

> **Catatan Penggunaan Bagian II:**  
> Bab 11 hingga Bab 14 disusun sebagai **naskah siap baca** yang terhubung langsung dengan teori dan angka pada Bagian I. Anda cukup mengikuti petunjuk **[Tampilan Layar / Slide]** lalu membacakan bagian **[Kalimat yang Diucapkan]** dengan intonasi santai namun meyakinkan.

---

# BAB 11 — STRATEGI PRESENTASI & PENGATURAN WAKTU

## 11.1 Kenali Audiens Anda Sebelum Mulai Berbicara

Proyek CSIP punya kekuatan unik karena berbicara dalam **dua bahasa**: bahasa **nilai bisnis & efisiensi kerja** (untuk manajer/eksekutif non-teknis), dan bahasa **disiplin ilmiah & rekayasa produksi** (untuk Data Scientist, Engineer, dan Penguji Sidang/Asesor SKKNI).

- **Untuk Audiens Non-Teknis:** Tekankan analogi waktu, penghematan tenaga tim CS lewat kuota kapasitas harian, transparansi saat model tidak layak dipakai (*repeat purchase* ditolak), dan kemudahan memakai `CSIP Studio` dengan slider simulasi + penasihat bahasa manusia `Nara`. Hindari menyebut detail sintaks kode terlalu dalam kecuali ditanya.
- **Untuk Penguji Teknis / Data Scientist:** Tekankan 5 pilar metodologi yang membedakan CSIP dari proyek biasa: (1) agregasi *anti fan-out* ke `order_id`, (2) pemisahan keras Pos T0 vs Pos T2 dan Embargo 90 hari, (3) bukti kalibrasi Platt (`Brier 0,1375 -> 0,0762`, `ECE 0,2355 -> 0,0070`), (4) keberanian melaporkan `ROC-AUC 0,5021` dan `PR-AUC 0,1335` secara jujur, serta (5) `BusinessDecisionEngine`, `ml_engine.py`, dan 12 gerbang rilis otomatis.

## 11.2 Panduan Pengaturan Waktu (*Pacing Guide*)

| Skenario Presentasi | Alokasi Babak yang Dipakai | Total Durasi |
| :--- | :--- | :---: |
| **Pitch Eksekutif / Manajemen Cepat** | Babak 1 (Masalah) → Ringkasan Babak 3 (Kejujuran Waktu) → Babak 7 (Decision Engine & Kuota) → Babak 9–11 (Demo CSIP Studio & Nara) | **12–15 Menit** |
| **Presentasi Sidang / Asesmen SKKNI Level 7 Lengkap + Live Demo** | Seluruh Babak 1 hingga Babak 12 berurutan + sesi Tanya-Jawab menggunakan bekal Bab 14 | **35–45 Menit** |

## 11.3 Daftar Periksa 5 Menit Sebelum Presentasi Dimulai

Sebelum membuka layar di hadapan pimpinan atau tim penguji, pastikan empat langkah praktis ini sudah siap:

1. **Siapkan Dua Terminal Berjalan:** Terminal 1 menjalankan FastAPI (`uvicorn csip.api.server:app --host 127.0.0.1 --port 8000`) dan Terminal 2 menjalankan kokpit (`streamlit run app/streamlit_app.py --server.port 8501`) agar saat tiba di Babak 8 tidak menunggu loading awal.
2. **Buka Dua Tab Browser:** Tab 1 menunjuk ke `http://127.0.0.1:8501` (CSIP Studio) dan Tab 2 ke `http://127.0.0.1:8000/docs` (Swagger UI FastAPI).
3. **Siapkan 1 File CSV Contoh Lintas Bidang:** Misalnya file data medis/penjualan sederhana di Desktop agar saat demo Babak 10 Anda bisa menunjukkan fitur tarik-lepas CSV selain 3 kasus bawaan.
4. **Catat 3 Larangan Ucap Paling Penting:** Jangan pernah menyebut *"Accuracy 90% membuktikan model hebat"* (sebut **PR-AUC 0,3061 vs baseline 0,0963**), jangan menyebut *"SHAP membuktikan sebab-akibat"* (sebut **asosiasi prediktif**, perlu uji A/B untuk kausal), dan jangan menyembunyikan model `repeat_purchase` (`ROC-AUC 0,5021`) yang sengaja ditolak.

---

# BAB 12 — SKRIP BICARA KATA-DEMI-KATA: BABAK 1 s/d BABAK 7 (PENJELASAN PROYEK, DATA, METODOLOGI & MODEL)

### BABAK 1: PEMBUKAAN & RUMUSAN MASALAH BISNIS (DURASI ~3 MENIT)

**[Tampilan Layar / Slide 1–2: Judul Proyek CSIP v1.1.0 & Diagram 5 Pertanyaan Bisnis + Alur 7 Langkah]**

**[Kalimat yang Diucapkan]:**  
"Selamat pagi/siang Bapak, Ibu, dan rekan-rekan penguji sekalian. Hari ini saya akan mempresentasikan **CSIP — Core Strategy & Intelligence Platform versi 1.1.0**.

Sebelum masuk ke model atau kode, saya ingin mengajak kita melihat masalah nyata yang melatarbelakangi proyek ini. Bayangkan sebuah platform toko online besar yang menangani hampir **100 ribu pesanan** dengan pengiriman antar-kota seluas Brasil. Setiap hari, pasti ada sebagian paket yang terlambat atau ongkos kirimnya terasa memberatkan dibanding harga barang. Akibatnya, sebagian pembeli memberi ulasan bintang 1 atau 2.

Nah, biasanya perusahaan menghadapi dua masalah besar. Pertama, jika tim *Customer Service* baru bergerak setelah bintang 1 terbit, reputasi terlanjur rusak. Kedua, kapasitas tim CS itu terbatas — tidak mungkin menelpon puluhan ribu pembeli setiap minggu.

Di sisi lain, banyak proyek Data Science berhenti menjadi sekadar *Jupyter Notebook* dengan skor tinggi yang ternyata membocorkan data masa depan, atau berhenti jadi dashboard grafik yang tidak tahu tindakan apa yang harus diambil tim operasional.

Karena itu saya membangun **CSIP** bukan sekadar sebagai eksperimen model, melainkan sistem kecerdasan keputusan dari hulu ke hilir — mulai dari kontrak pengamanan data mentah, pencegahan kebocoran waktu, pemodelan berjenjang, kalibrasi peluang, hingga mengubah angka prediksi menjadi daftar prioritas aksi harian bagi tim Logistik dan CS.

Selain itu, agar tidak terbatas hanya pada satu data e-commerce, saya merancang CSIP dengan strategi dua lapis: **lapisan vertikal** yang membedah tuntas ekosistem transaksi **Olist Brasil**, dan **lapisan horizontal** bernama **CSIP Studio** yang memungkinkan pengguna mengunggah file CSV atau Excel dari industri apa pun — misalnya kesehatan, SDM, atau manufaktur — untuk dianalisis secara aman dan interaktif."

- **Poin Kunci & Transisi ke Babak 2:** *"Jadi inti proyek ini bukan sekadar melatih satu algoritma, melainkan membangun rantai lengkap dari data mentah sampai keputusan tim operasional. Sekarang mari kita bedah fondasi pertamanya: data transaksi Olist."*

---

### BABAK 2: BEDAH DATASET OLIST, PENANGANAN FAN-OUT & KONTRAK DATA (DURASI ~3 MENIT)

**[Tampilan Layar / Slide 3–4: Skema 9 Tabel Olist + Funnel Populasi 99.441 -> 95.824 + Kontrak 4 Tingkat]**

**[Kalimat yang Diucapkan]:**  
"Mari kita lihat fondasi datanya terlebih dahulu. Studi kasus vertikal utama CSIP memakai ekosistem **Olist E-Commerce Brasil** yang sering dianggap satu dataset kecil, padahal aslinya terdiri atas **9 tabel terpisah** dengan lebih dari **1,5 juta baris rekaman mentah** — mulai dari 99.441 pesanan, 112 ribu baris detail barang, 103 ribu catatan cicilan/pembayaran, 104 ribu ulasan bahasa Portugis, hingga **lebih dari 1 juta titik koordinat GPS kode pos**.

Di tahap ini ada dua jebakan rekayasa data yang wajib dibereskan sejak awal:

Pertama, masalah **Cartesian Fan-Out**. Satu pesanan bisa berisi 3 barang, dibayar pakai 2 metode sekaligus, dan direvisi ulasannya 2 kali. Jika kita langsung melakukan `JOIN` mentah antar tabel, satu pesanan bisa mengganda menjadi 12 baris! Angka omzet akan membengkak palsu dan pesanan yang sama bisa bocor antara data latih dan data uji. Karena itu, di modul `OlistDataCleaner`, seluruh tabel anak saya ringkas lebih dulu secara ketat ke **1 baris unik per ID pesanan (`order_id`)**. Sementara 1 juta baris GPS disaring hanya ke koordinat wilayah Brasil dan diambil titik tengah mediannya, menyusut bersih menjadi **19.015 prefiks kode pos unik**.

Kedua, **kejujuran terhadap status pesanan dan ulasan kosong**. Dari 99.441 pesanan mentah, ketika fokus analisis diarahkan ke pengalaman pengiriman hingga barang tiba (`delivered`), tercatat 96.478 pesanan — artinya ada 1.234 pesanan yang dibatalkan atau stoknya kosong yang tingkat keluhannya hampir 88%, dan kami pisahkan penjelasannya secara transparan agar tidak memalsukan cakupan model. Dari pesanan terkirim yang bersih sebanyak 96.470 transaksi, sebanyak **95.824 memiliki ulasan**, sementara 646 lainnya memilih diam. Kami melarang sistem mengarang rating palsu untuk pesanan yang tidak diulas.

Seluruh tabel olahan ini lalu diperketat dengan **Kontrak Data 4-Tingkat** (`INFO`, `WARNING`, `RECOVERABLE_ERROR`, dan `CRITICAL_FAILURE`). Jika ada kolom wajib hilang atau ID ganda, pipeline langsung berhenti otomatis sebelum menghasilkan prediksi yang menyesatkan, dan setiap berkas disimpan dalam format Parquet ringan berukuran **18,4 MB** dengan sidik jari hash **SHA-256** agar tetap nyaman berjalan di laptop dengan RAM 8 GB."

- **Poin Kunci & Transisi ke Babak 3:** *"Setelah strukturnya bersih dan bebas duplikasi fan-out, pertanyaan berikutnya adalah: apakah fitur di tabel itu aman dipakai untuk memprediksi? Di sini kita masuk ke pagar terpenting dalam proyek ini, yaitu isolasi waktu."*

---

### BABAK 3: KUNCI METODOLOGI — ISOLASI WAKTU T0/T1/T2 & EMBARGO 90 HARI (DURASI ~4 MENIT)

**[Tampilan Layar / Slide 5–6: Garis Waktu Checkout (T0) -> Disposisi Kurir (T1) -> Paket Sampai (T2) & Skema CV 4 Lipatan]**

**[Kalimat yang Diucapkan]:**  
"Bagian ini adalah jantung integritas ilmiah proyek CSIP, yaitu **pencegahan kebocoran data (*Data Leakage*)**.

Analogi sederhananya begini: kalau kita ingin menebak apakah pelanggan akan marah *pada detik ia baru mengklik tombol bayar di kasir*, kita jelas **tidak boleh** memakai informasi apakah paketnya nanti terlambat 5 hari di jalan. Sebab saat pembeli baru bayar, kurirnya saja belum menjemput barang! Jika informasi keterlambatan ikut dimasukkan ke fitur saat checkout, skor akurasi di laporan memang bisa terlihat tinggi sekali, tapi saat dipakai di aplikasi nyata, model itu langsung lumpuh.

Oleh sebab itu, saya mengunci arsitektur fitur ke dalam **tiga pos waktu yang terpisah keras**:

- **Pos T0 (Titik Checkout — 10 Fitur):** Hanya memakai informasi yang sah diketahui saat pembeli membayar — seperti harga barang, beban rasio ongkir terhadap harga, jumlah barang, cicilan, jarak penjual-pembeli dalam kilometer, janji estimasi hari kirim, dan jumlah transaksi pelanggan tersebut *sebelum* hari transaksi ini. Semua data pengiriman aktual diblokir keras.
- **Pos T1 (Disposisi Kurir — 5 Fitur):** Ditambah jeda jam konfirmasi pembayaran untuk memprediksi potensi hari keterlambatan logistik.
- **Pos T2 (Pasca-Pengiriman — 15 Fitur):** Baru membuka fakta aktual perjalanan kurir — berapa hari paket benar-benar sampai, berapa hari keterlambatannya, serta interaksi *kekecewaan ganda* ketika ongkir sudah mahal tetapi paket juga datang terlambat. Model T2 ini dipakai untuk **diagnosis akar masalah dan prioritas penanganan CS**, bukan untuk prediksi saat checkout.

Selain itu, dalam membagi data latih dan data uji, kami **tidak memakai random split**. Data dibagi sesuai alur kalender nyata: data latih sampai **Maret 2018**, data validasi **April hingga Juni 2018**, dan **data uji masa depan terkunci setelah 30 Juni 2018** sebanyak 12.571 pesanan. Saat melakukan uji silang (*Rolling-Origin Temporal Cross-Validation*), kami memasang jarak jeda atau **embargo 90 hari** di antara batas data latih dan validasi agar paket pengiriman panjang dari periode lama tidak tumpang tindih ke periode uji berikutnya."

- **Poin Kunci & Transisi ke Babak 4:** *"Dengan pemisahan T0, T1, T2 dan embargo 90 hari ini, kita siap membandingkan model dari yang paling sederhana hingga yang paling cerdas."*

---

### BABAK 4: TANGGA PEMODELAN B0–B4 & PENDEKATAN ALGORITMA (DURASI ~3 MENIT)

**[Tampilan Layar / Slide 7: Tangga Baseline B0–B4 & Peran Masing-Masing Algoritma]**

**[Kalimat yang Diucapkan]:**  
"Setelah data dan waktunya bersih, bagaimana kami memilih algoritma? Di CSIP kami menerapkan prinsip **'Mulai dari yang Sederhana, Baru Naik ke yang Kompleks'** lewat **Tangga Baseline B0 hingga B4**.

- Di anak tangga **B0**, kami membuat aturan naif seperti tebakan kelas terbanyak dan aturan *if-else* sederhana (jika paket telat maka beri risiko tinggi). Ini menjadi batas lantai: kalau model canggih kalah dari aturan `if-else`, model itu harus dibuang.
- Di **B1 dan B2**, kami uji model garis lurus seperti `LogisticRegression` dan `Ridge`, serta pohon keputusan tunggal.
- Di **B3**, kami jalankan `RandomForest` dan **LightGBM**. Di sinilah pemenang untuk data tabel kami ditemukan. Mengapa LightGBM lebih unggul dibanding Deep Learning tabular di proyek ini? Karena data keterlambatan pengiriman sangat miring — sebagian besar paket datang tepat waktu, lalu ada ekor ekstrem yang telat hingga 30–40 hari. Pohon bertahap LightGBM sangat tangguh membelah ambang batas seperti ini, ukuran filenya hanya setengah megabyte (~500 KB), cepat dijalankan tanpa GPU, dan mudah diaudit penyebab keputusannya.
- Lalu di **B4 Deep Learning**, kami menempatkan jaringan saraf bukan secara paksa di tabel kecil, melainkan di tempat yang memang membutuhkannya: membaca komentar teks ulasan bahasa Portugis memakai **PyTorch Bi-LSTM** ringan (~1 MB) yang membaca kalimat dari dua arah untuk menangkap frasa negasi seperti *'tidak sampai'*.
- Melengkapi model prediksi tadi, kami juga memakai **K-Means Clustering** untuk membagi profil pelanggan menjadi 4 kelompok perilaku, analisis survival **Kaplan-Meier**, serta model tren makro mingguan untuk mensimulasikan dampak berantai lonjakan volume pesanan terhadap keterlambatan."

---

### BABAK 5: HASIL EMPIRIS, KEJUJURAN ILMIAH & PENOLAKAN MODEL GAGAL (DURASI ~3,5 MENIT)

**[Tampilan Layar / Slide 8: Tabel Papan Peringkat Seluruh Model & Kasus Valid Negative Finding]**

**[Kalimat yang Diucapkan]:**  
"Sekarang mari kita lihat hasil pengujian nyata pada data masa depan terkunci setelah Juni 2018. Perlu saya tekankan lebih dulu: karena hanya **9,63%** ulasan yang bernilai negatif, metrik *Accuracy* biasa sangat menipu — menebak 'semua pelanggan puas' saja sudah benar 90,4%. Maka untuk klasifikasi kami fokus pada **PR-AUC** (kemampuan menemukan kelompok keluhan di tengah mayoritas yang puas) dan **ROC-AUC**.

Berikut empat temuan utama kami:

1. **Prediksi Keterlambatan (Pos T1) meraih `MAE 4,83 hari` dan `R² 0,3926`**, memangkas kesalahan tebakan hampir **28%** dibanding baseline median, sehingga disetujui berstatus **`PRODUCTION_APPROVED`**.
2. **Model Diagnostik Pasca-Pengiriman (Pos T2)** mencapai **`PR-AUC 0,3061`** (lebih dari **3 kali lipat** di atas base rate `0,0963`) dengan **`ROC-AUC 0,6745`**, berstatus **`PILOT_ELIGIBLE`** dengan syarat wajib melewati lapisan kalibrasi peluang. Sementara untuk komentar teks tertulis, **`TextBiLSTM`** meraih **`Macro-F1 0,8420`** dan **`Accuracy 88,7%`**.
3. **Model Peringatan Dini Checkout (Pos T0)** saat dievaluasi langsung pada file model `.joblib`-nya menghasilkan **`PR-AUC 0,1335`** dan **`ROC-AUC 0,5468`**. Selama audit internal, kami sempat menemukan laporan lama yang mencatat angka `0,2845`, dan langsung kami perbaiki secara transparan ke angka aktual `0,1335` serta membatasinya ke status **`PILOT_RESTRICTED`**. Mengapa angkanya jauh lebih rendah daripada Pos T2? Justru ini membuktikan sistem kami jujur bebas kebocoran — karena di titik checkout, faktor penyebab utama kemarahan yaitu keterlambatan kurir memang belum terjadi!
4. **Kejujuran Ilmiah pada Model Pelanggan Belanja Ulang (*Repeat Purchase*):** Ketika kami menguji prediksi apakah pelanggan akan belanja lagi, hasil di data masa depan hanya **`ROC-AUC 0,5021`** — setara melempar koin. Mengapa? Mayoritas pembeli Olist memang belanja satu kali dan kami tidak memiliki data riwayat klik penelusuran mereka. Alih-alih memanipulasi tuning agar terlihat bagus, model ini secara resmi kami beri status **`REJECTED FOR DEPLOYMENT`** sebagai *Valid Negative Finding*. Bagi bisnis, menolak model yang tidak bekerja jauh lebih berharga karena menyelamatkan perusahaan dari membuang anggaran promosi."

---

### BABAK 6: KALIBRASI PROBABILITAS (PLATT SCALING) & PENJELASAN SHAP (DURASI ~2,5 MENIT)

**[Tampilan Layar / Slide 9: Grafik Sebelum vs Sesudah Platt Scaling & Peringkat Fitur SHAP]**

**[Kalimat yang Diucapkan]:**  
"Satu hal yang sering dilupakan Data Scientist adalah **kalibrasi peluang**. Karena saat melatih model ketidakpuasan kita memberi bobot lebih pada kelas minoritas yang jarang muncul, skor probabilitas mentah dari LightGBM membengkak rata-rata menjadi **33,1%**, padahal kejadian aslinya cuma **9,6%**. Kalau angka mentah ini dipakai langsung untuk memberi voucher kompensasi, biaya perusahaan bisa membengkak karena terlalu sering memicu alarm palsu.

Oleh karena itu, pada data validasi kami melatih lapisan penyeimbang **Platt Scaling**. Hasilnya sangat signifikan: **Brier Score** membaik **44,6%** dari `0,1375` turun menjadi **`0,0762`**, dan tingkat meleset kalibrasi (**ECE**) anjlok **97%** dari `23,5%` tinggal **`0,70%`**. Artinya, ketika model terkalibrasi menyebut peluang kecewa 20%, kenyataannya di lapangan memang mendekati 20%.

Lalu bagaimana agar tim bisnis tidak melihat model sebagai kotak hitam? Kami menjalankan **SHAP TreeExplainer** pada 800 sampel terkendali. Terlihat jelas bahwa **jumlah hari keterlambatan (`delivery_delay_days`)** menjadi pendorong nomor satu — menyumbang sekitar sepertiga total kekuatan keputusan model — diikuti durasi tunggu pengiriman dan jumlah item dalam keranjang. Namun kami selalu memberi garis tegas di laporan: SHAP menjelaskan faktor asosiasi di data historis, bukan jaminan sebab-akibat otomatis tanpa uji eksperimen."

---

### BABAK 7: BUSINESS DECISION ENGINE, KUOTA TIM CS & UJI A/B (DURASI ~3 MENIT)

**[Tampilan Layar / Slide 10: Alur Decision Engine -> 12 Atribut Rekomendasi -> Kuota Kapasitas & Rancangan A/B 80/20]**

**[Kalimat yang Diucapkan]:**  
"Sekarang kita masuk ke pertanyaan paling penting bagi manajemen: *'Setelah tahu pesanan mana yang berisiko 72%, lalu besok pagi tim kita harus ngapain?'*

Di sinilah modul **`BusinessDecisionEngine`** bekerja. Modul ini menerjemahkan angka probabilitas dan nilai ekonomi pesanan ke dalam **4 tingkat prioritas bisnis** (`CRITICAL`, `HIGH`, `MEDIUM`, dan `LOW`) dalam format kontrak **12 atribut** — lengkap mencantumkan siapa tim penanggung jawabnya (`Logistics` atau `Customer Experience`), tindakan nyatanya (seperti eskalasi kurir ekspres atau sapaan proaktif WhatsApp sebelum komplain meledak), serta KPI untuk mengukurnya.

Agar tim CS tidak kelelahan menghadapi ribuan peringatan, kami membangun fungsi **`calibrate_thresholds_from_capacity`**. Jika manajer mengatur bahwa tim CS hanya sanggup menangani maksimal **10% pesanan paling berisiko** atau 100 kasus per hari, mesin otomatis menyetel ambang batas probabilitas di titik kuantil top 10% tersebut dan menyaring antrean secara ketat.

Terakhir, untuk membuktikan apakah intervensi proaktif tadi benar-benar menurunkan ulasan buruk di lapangan, sistem menyertakan **`design_ab_holdout_plan`** yang otomatis membagi pesanan berisiko menjadi **80% kelompok yang diintervensi (*Treatment*)** dan **20% kelompok pembanding (*Control Holdout*)** untuk diukur hasilnya setelah pengiriman selesai."

- **Poin Kunci & Transisi ke Live Demo:** *"Demikian kerangka teori, metodologi, hasil empiris, hingga mesin keputusannya. Supaya tidak hanya di slide, sekarang saya izin beralih ke aplikasi langsung untuk mendemokan bagaimana sistem ini bekerja di layar nyata."*

---

# BAB 13 — SKRIP LIVE DEMO KATA-DEMI-KATA: BABAK 8 s/d BABAK 12 (DEMO APLIKASI, UNIVERSAL CSV STUDIO, FASTAPI & AUDIT KODE)

### BABAK 8: MEMBUKA KOKPIT CSIP STUDIO & PEMAHAMAN AWAM (DURASI ~3 MENIT)

**[Tampilan Layar / Live Demo: Buka browser `http://127.0.0.1:8501` — Tampilan `CSIP Studio` dengan dataset bawaan `Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)`]**

**[Kalimat yang Diucapkan]:**  
"Baik, sekarang kita beralih dari teori ke demonstrasi langsung aplikasinya. Di layar Bapak/Ibu adalah **CSIP Studio**, kokpit interaktif berbasis Streamlit yang memang sengaja dirancang bersih supaya baik eksekutif non-teknis maupun analis data bisa langsung memakainya tanpa melihat kode.

Lihat di panel kiri Langkah 1 **'Sumber data dan fokus'**. Di sini tersedia dua mode: pertama, kita bisa memilih **3 kasus bawaan lintas bidang** (Olist E-Commerce, Risiko Kesehatan Medis, dan Mutu Produk), atau kedua, pengguna bisa menarik file **CSV atau Excel** apa pun dari komputer.

Saat ini aktif pada **Kasus 1 Data Olist**, dengan target **'Yang ingin dioptimalkan'** adalah skor kepuasan/keterkaitan pelanggan. Tepat di bawahnya ada kotak amber bertajuk **'Artinya begini'** yang otomatis menerjemahkan istilah kolom data menjadi kalimat bahasa Indonesia yang mudah dimengerti orang awam.

Sekarang lihat di Langkah 2 **'Tuas simulasi'**. Mesin otomatis memeringkat 3 faktor paling berpengaruh dan menyiapkan *slider* interaktifnya. Di sebelah kanan, tiga **Kartu Bento KPI** langsung menampilkan estimasi nilai target saat ini, faktor penentu terkuat beserta persentase pengaruhnya, dan selisihnya dibanding standar acuan."

---

### BABAK 9: MENGGERAKKAN TUAS SIMULASI & 4 LENSA ANALITIK (DURASI ~3,5 MENIT)

**[Tampilan Layar / Live Demo: Geser slider faktor nomor 1 ke kanan/ekstrem, lalu klik satu per satu ke-4 pilihan radio `Lensa tampilan`]**

**[Kalimat yang Diucapkan]:**  
"Mari kita simulasikan sebuah skenario nyata. *[Arahkan kursor dan geser slider #1 pada Tuas Simulasi]*. Perhatikan ketika saya menggeser faktor paling dominan ini — misalnya keterlambatan atau rasio beban biaya — kartu KPI estimasi dan persentase selisih di sebelah kanan langsung berubah secara real-time, lengkap dengan perubahan warna indikator (*Terkendali Standar* vs *Perlu Perhatian*). Di bawah grafik, **Penasihat Strategi Nara** juga memperbarui rangkuman narasinya dalam bahasa bisnis beserta catatan batas ketidakpastian model. Kita bisa menekan **'Setel ulang'** kapan saja untuk kembali ke nilai median.

Sekarang mari kita lihat **4 Lensa Tampilan** di panggung utama:

1. *[Klik Lensa 1]* **'1. Kurva Simulasi dan Titik Kritis'**: Menampilkan kurva respon bagaimana prediksi target berubah sepanjang rentang nilai fitur teratas, termasuk menandai titik belok kritis di mana risiko mulai melonjak tajam.
2. *[Klik Lensa 2]* **'2. Peringkat Faktor Penentu'**: Memeringkat kekuatan pengaruh tiap fitur dalam persen beserta arah hubungannya (apakah menaikkan atau menekan target).
3. *[Klik Lensa 3]* **'3. Sebaran Kelompok Data'**: Memperlihatkan perbedaan distribusi populasi di berbagai tingkatan faktor utama sehingga kita tahu masalah terjadi pada kelompok mana.
4. *[Klik Lensa 4]* **'4. Observatorium Drift & Stabilitas'**: Mengaudit stabilitas distribusi data menggunakan indeks **PSI** untuk memastikan tidak ada pergeseran pola yang membahayakan keandalan model."

---

### BABAK 10: DEMO UNIVERSAL CSV STUDIO — ANALITIK LINTAS INDUSTRI (DURASI ~3 MENIT)

**[Tampilan Layar / Live Demo: Ganti dropdown `Atau pakai dataset bawaan` ke `Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)` atau unggah sebuah file CSV contoh dengan target biner 0/1 maupun kontinu]**

**[Kalimat yang Diucapkan]:**  
"Tadi saya menjanjikan bahwa CSIP tidak hanya terkunci pada data toko online. Mari saya buktikan secara langsung. *[Klik pilihan dataset bawaan menjadi Kasus 2 Data Medis, atau unggah file CSV lain]*.

Begitu file atau dataset baru masuk, di balik layar ada dua modul cerdas yang langsung bekerja — **`semantic_profiler.py`** dan **`ml_engine.py`**:

- Pertama, *semantic profiler* membaca nama-nama kolom dan mencocokkannya dengan **kamus 11 sektor industri** untuk menamai ulang satuan ukur seperti persen, hari, atau poin kesehatan secara otomatis.
- Kedua, *EDA & Leakage Detector* memindai apakah ada kolom tanggal atau ID pelanggan yang berisiko membocorkan data, lalu menghitung persentase data hilang dan outlier.
- Ketiga, sistem memeriksa isi kolom target: jika nilainya hanya `0` dan `1`, mesin otomatis berpindah jalur ke **Klasifikasi Biner** (`LogisticRegression` vs `RandomForestClassifier` dengan *PR-AUC* dan *Brier Score*); jika angkanya kontinu, otomatis memakai jalur **Regresi** (`Ridge` vs `RandomForestRegressor` dengan *MAE*, *RMSE*, dan *R²*).
- Keempat, semua langkah pengisian data kosong dan penyaringan multikolinearitas dilakukan ketat hanya pada data latih (*Split-Before-Transform*) dan diuji dengan **Out-of-Sample K-Fold Cross-Validation**, sementara hasil simulasi menampilkan rentang ketidakpastian 90% dari seluruh pohon keputusan."

---

### BABAK 11: DEMO FASTAPI MICROSERVICE & KETAHANAN PRODUKSI (DURASI ~2 MENIT)

**[Tampilan Layar / Live Demo: Buka tab browser `http://127.0.0.1:8000/docs` (Swagger UI FastAPI) — tunjukkan daftar endpoint, atau tunjukkan terminal pengujian]**

**[Kalimat yang Diucapkan]:**  
"Sementara kokpit Streamlit tadi melayani pengguna manusia dan analis, sistem operasional seperti aplikasi checkout atau CRM perusahaan membutuhkan pintu komunikasi mesin-ke-mesin. Untuk itu kami memisahkan layanan mikro **FastAPI** di port 8000.

Bisa kita lihat di dokumentasi interaktif Swagger ini:
- Ada `/health` dan `/ready` untuk pemantauan infrastruktur kontainer.
- Ada pemisahan endpoint prediksi **`/predict/early-warning`** yang hanya menerima 10 fitur Pos T0 saat checkout, dan **`/predict/post-fulfillment`** untuk 15 fitur Pos T2. Jadi mustahil ada aplikasi hulu yang tidak sengaja mengirim data keterlambatan saat checkout.
- Ada **`/decisions/recommend`** yang langsung mengembalikan rekomendasi 12 atribut lengkap dari *Decision Engine* sesuai kuota tim CS.
- Dan ada **`/monitor/drift`** serta **`/models/registry`** untuk integrasi MLOps, di mana model berstatus `RESEARCH_ONLY` diblokir otomatis dari layanan produksi."

---

### BABAK 12: BUKTI PENGUJIAN OTOMATIS, 12 GERBANG KUALITAS & PENUTUP (DURASI ~2,5 MENIT)

**[Tampilan Layar / Slide 11–12: Terminal hasil `pytest` (216 passed) + `verify_release.py` (12 Gates PASS) + Ringkasan 4 Pilar]**

**[Kalimat yang Diucapkan]:**  
"Untuk menutup presentasi ini, saya ingin menunjukkan bagaimana kami menjamin seluruh sistem yang baru saja saya jelaskan tidak hanya jalan di komputer saya hari ini, tetapi siap diaudit dan diuji ulang kapan saja.

Kami memiliki **216 pengujian otomatis (`pytest`)** yang memeriksa mulai dari aturan embargo 90 hari, kontrak data rusak, keabsahan `ml_engine`, layanan FastAPI, hingga simulasi klik keempat lensa Streamlit melalui `AppTest`. Selain itu, kami membangun skrip pengawal rilis **`verify_release.py`** yang mengecek **12 Gerbang Kualitas (G1–G12)** sekaligus: konsistensi versi, nol test gagal, nol kalimat klaim berlebihan lewat `check_claims.py`, keutuhan 63 Kriteria Unjuk Kerja SKKNI Level 7, hingga verifikasi hash SHA-256 ratusan file artefak. Total pemakaian memorinya pun sangat hemat — hanya sekitar **264 MB RAM** dan latensi prediksi di bawah **15 milidetik** per 1.000 pesanan di CPU laptop standar.

Singkatnya, CSIP v1.1.0 membuktikan bahwa proyek Data Science yang matang bukan tentang seberapa rumit algoritmanya atau seberapa tinggi angka akurasi semunya, melainkan bagaimana kita menjaga **kejujuran waktu**, **ketepatan kalibrasi peluang**, **transparansi terhadap keterbatasan model**, dan **keterhubungan langsung ke kapasitas tindakan bisnis**.

Terima kasih banyak atas perhatian Bapak, Ibu, dan para penguji. Saya persilakan apabila ada pertanyaan atau aspek kode yang ingin kita bedah lebih dalam."

---

# BAB 14 — BUKU SAKU TANYA-JAWAB (Q&A DEFENSE CHEAT-SHEET): 15 PERTANYAAN TERSULIT & JAWABAN TERBAIKNYA

Gunakan panduan ini saat sesi tanya-jawab. Setiap pertanyaan dilengkapi **Jawaban Singkat (untuk Eksekutif)** dan **Jawaban Mendalam (untuk Penguji Data Science)**.

---

### Pertanyaan 1: "Apakah dataset Olist itu terlalu kecil atau sempit untuk sebuah platform Data Science?"
- **Jawaban Singkat:** Tidak kecil — Olist adalah skema relasional 9 tabel berisi hampir 100 ribu transaksi nyata dan lebih dari 1 juta titik GPS, dan selain Olist, CSIP juga punya `Universal CSV Studio` untuk dataset industri lain.
- **Jawaban Teknis:** Ukuran bukan dilihat dari jumlah baris mentah belaka, melainkan kompleksitas masalah nyatanya: *many-to-many join* yang berisiko *fan-out*, ketimpangan kelas 9,63%, label tertunda, bias seleksi pesanan batal, serta pergeseran distribusi antar musim 2016–2018.

---

### Pertanyaan 2: "Kenapa PR-AUC model Pasca-Pengiriman (T2) `0,3061` dan Checkout (T0) cuma `0,1335`? Bukankah angka `0,30` terlihat kecil?"
- **Jawaban Singkat:** Pada data yang kasus keluhannya hanya 9,6%, nilai baseline acak PR-AUC adalah `0,096`. Jadi `0,3061` artinya kemampuan penyaringan model **3,2 kali lebih tajam** dibanding tebakan acak. Sementara nilai `0,1335` di checkout wajar karena kurir belum mengantar barang saat pembeli baru bayar.
- **Jawaban Teknis:** Ini membuktikan pemodelan bebas kebocoran waktu. Jika kami mencampur fitur pasca-kirim ke checkout atau memakai random split, PR-AUC mudah melambung secara artifisial tetapi gagal saat produksi.

---

### Pertanyaan 3: "Kenapa model *Repeat Purchase* (`ROC-AUC 0,5021`) tidak dihapus saja atau di-tuning supaya tinggi?"
- **Jawaban Singkat:** Karena di bisnis nyata kita harus jujur memberi tahu manajemen mana alat yang berfungsi dan mana yang tidak layak dipakai agar perusahaan tidak membuang biaya promosi.
- **Jawaban Teknis:** Data Olist memiliki keterbatasan fitur perilaku pra-pembelian (tidak ada riwayat klik, promo, atau sesi login) dan lebih dari 97% pembeli hanya belanja sekali. Mencatatnya sebagai *Valid Negative Finding* dengan status `REJECTED FOR DEPLOYMENT` menunjukkan disiplin ilmiah agar *metric hacking* tidak terjadi.

---

### Pertanyaan 4: "Apa gunanya memisahkan `Accuracy` vs `PR-AUC` vs `Brier Score`?"
- **Jawaban Singkat:** *PR-AUC* menjawab *"apakah model jago mengurutkan pesanan bermasalah ke antrean atas?"*; sedangkan *Brier Score* dan *ECE* menjawab *"apakah persentase risiko yang ditampilkan model bisa dipercaya untuk menghitung biaya voucher/kompensasi?"*
- **Jawaban Teknis:** Karena model dilatih dengan `class_weight="balanced"`, skor `predict_proba` mentahnya melambung (rata-rata `0,3312`, `Brier 0,1373`). Kalibrasi **Platt Scaling** meluruskan probabilitasnya tanpa merusak urutan peringkatnya sehingga `Brier` turun ke `0,0762` dan `ECE` ke `0,0070`.

---

### Pertanyaan 5: "Bagaimana cara membuktikan tidak ada kebocoran data (*Data Leakage*) di proyek ini?"
- **Jawaban Singkat:** Ada empat kunci pengaman: tabel digabung per pesanan dulu, fitur dipisah keras antara saat bayar vs setelah paket sampai, data uji selalu diambil dari bulan-bulan masa depan, dan seluruh aturan itu diuji otomatis oleh unit test.
- **Jawaban Teknis:** (1) Agregasi *anti fan-out* di `cleaner.py`; (2) `prior_order_count` dihitung *strictly as-of*; (3) partisi kronologis terkunci (`train <= 2018-03-31`, `locked test > 2018-06-30`) dan `RollingOriginTemporalCV` ber-embargo 90 hari; (4) `ml_engine.py` menerapkan *Split-Before-Transform*; dan (5) divalidasi oleh `test_feature_leakage.py`, `test_temporal_leakage.py`, dan `test_temporal_isolation.py`.

---

### Pertanyaan 6: "Mengapa memakai embargo 90 hari pada validasi silang temporal?"
- **Jawaban Singkat:** Untuk memberi jarak aman antar periode latih dan validasi supaya pesanan lama yang proses kirim dan pengisian ulasannya memakan waktu berminggu-minggu sudah tuntas seluruhnya sebelum periode uji dimulai.
- **Jawaban Teknis:** Memastikan syarat pemisahan batas waktu latih dan validasi menghilangkan tumpang tindih label tertunda (*delayed ground-truth label overlap*).

---

### Pertanyaan 7: "Kenapa memilih LightGBM sebagai juara model tabular, bukan Deep Learning atau XGBoost?"
- **Jawaban Singkat:** LightGBM paling cepat, ringan di laptop RAM 8 GB (file hanya ~500 KB, inferensi ~4–13 ms), dan paling cocok untuk data tabel transaksi dibanding neural network.
- **Jawaban Teknis:** Pada 10–15 fitur dengan distribusi ekor panjang (`delivery_delay_days`), GBDT menangani interaksi non-linear lebih efisien ketimbang `TabularEmbeddingMLP`, dan memiliki dukungan SHAP *TreeExplainer* yang cepat dan eksak. Deep Learning tetap kami pakai di tempat terbaiknya yaitu teks ulasan (`TextBiLSTM`).

---

### Pertanyaan 8: "Kenapa tidak memakai LLM (seperti GPT / Llama) untuk membaca ulasan pelanggan?"
- **Jawaban Singkat:** Karena proyek ini mewajibkan privasi lokal penuh (data tidak boleh dikirim ke cloud) dan harus ringan berjalan di laptop RAM 8 GB tanpa GPU.
- **Jawaban Teknis:** `TextBiLSTM` hanya berukuran **~1,03 MB**, memakai kosakata 5.000 kata lokal, dan sudah meraih **Macro-F1 `0,8420`** pada ulasan teks tanpa memakan beberapa gigabyte VRAM atau biaya API eksternal.

---

### Pertanyaan 9: "Jika SHAP menunjukkan keterlambatan adalah faktor terbesar, apakah berarti mengurangi keterlambatan pasti menurunkan komplain sekian persen?"
- **Jawaban Singkat:** Belum tentu sebesar angka di grafik secara otomatis; SHAP hanya menunjukkan pola kuat dari riwayat masa lalu, sehingga perlu diuji lewat percobaan lapangan (uji A/B).
- **Jawaban Teknis:** CSIP memisahkan klaim prediktif/asosiatif (*Level L1/L2*) dari klaim kausal (*Level L3*). Untuk melangkah ke pembuktian kausal, `BusinessDecisionEngine` sudah menyediakan metode `design_ab_holdout_plan` (80% Treatment vs 20% Control Holdout).

---

### Pertanyaan 10: "Apa jadinya kalau besok tim CS hanya punya kapasitas menangani 50 pesanan, padahal sistem memprediksi 800 pesanan berisiko?"
- **Jawaban Singkat:** Sistem otomatis mengurutkan dari prioritas tertinggi (`CRITICAL`) yang paling besar dampaknya lalu memotong tepat 50 kasus agar tim CS tidak kewalahan.
- **Jawaban Teknis:** Metode `calibrate_thresholds_from_capacity()` mengkalibrasi ulang batas probabilitas risiko berdasarkan batas `max_alert_rate` dan kuota batch `capacity_max_actions_per_batch` pada `DecisionRuleConfig`.

---

### Pertanyaan 11: "Kalau pengguna mengunggah CSV yang isinya kolom Ya/Tidak (`0/1`), atau dataset cuma punya 10 baris, apakah studio Anda tidak error atau overfit?"
- **Jawaban Singkat:** Tidak — `ml_engine.py` otomatis mendeteksi apakah targetnya kategori (`0/1`) atau angka biasa, dan kalau barisnya terlalu sedikit, sistem memberi label jujur bahwa data belum cukup untuk uji silang penuh.
- **Jawaban Teknis:** Ketika nilai unik target tepat `{0, 1}`, pipeline otomatis beralih dari `Ridge/RandomForestRegressor` ke `LogisticRegression/RandomForestClassifier` dengan metrik `PR-AUC`, `ROC-AUC`, `Brier`, dan memakai `predict_proba` pada simulator. Untuk `N < 8`, ia secara eksplisit menandai mode `IN_SAMPLE_FALLBACK_SMALL_N`.

---

### Pertanyaan 12: "Bagaimana cara kerja deteksi *Drift* di CSIP? Apakah menunggu laporan manual?"
- **Jawaban Singkat:** Tidak, sistem memantau pergeseran distribusi data baru terhadap data acuan secara otomatis memakai status lampu lalu lintas hijau-kuning-merah (*PSI*).
- **Jawaban Teknis:** `DriftEngine` menghitung **PSI** (ambang `< 0,10` Stabil, `0,10–0,25` Peringatan, `>= 0,25` Kritis), uji **Kolmogorov-Smirnov** (`alpha = 0,05`), **Wasserstein**, dan **JSD**. Jika model dilatih ulang (`SlidingWindowRetrainer`), model baru wajib unggul minimal `+1,0%` dan tidak merusak Brier lebih dari `5%` sebelum boleh menggantikan model produksi.

---

### Pertanyaan 13: "Apakah hasil aplikasi bisa dipercaya atau angkanya diketik manual di dashboard?"
- **Jawaban Singkat:** Seluruh angka audit model berasal dari file laporan terverifikasi yang dihasilkan oleh kode pengujian, dan UI dashboard diuji otomatis memakai `AppTest`.
- **Jawaban Teknis:** Modul `app/data_provider.py` hanya membaca JSON/CSV di `artifacts/reports/`, `scripts/reevaluate_locked_test.py` mengevaluasi ulang `.joblib` langsung pada `order_level.parquet`, dan gerbang **G8** pada `verify_release.py` memverifikasi bahwa UI bebas error.

---

### Pertanyaan 14: "Mengapa file CSV mentah Olist (`data/raw/`) tidak ikut dimasukkan ke dalam file `.zip` rilis?"
- **Jawaban Singkat:** Karena 9 file CSV mentah totalnya di atas 120 MB sehingga akan membuat file rilis melampaui batas praktis 100 MB, padahal tabel bersihnya (`Parquet`) sudah tersedia di dalam paket untuk langsung dipakai.
- **Jawaban Teknis:** `data/processed/order_level.parquet` (~18,4 MB) dan seluruh artefak terlatih sudah termasuk dalam `csip_v1.1.0.zip` (~82 MB), sedangkan pengguna yang ingin mereproduksi tahap *raw-to-processed* cukup menjalankan `python scripts/download_raw_olist.py`.

---

### Pertanyaan 15: "Jika suatu hari project ini akan dikembangkan lebih lanjut ke produksi skala besar (*enterprise*), bagian mana saja yang menjadi keterbatasan saat ini?"
- **Jawaban Singkat:** Ada tiga hal utama: pertama, data historis Olist berasal dari periode 2016–2018 dan belum mencakup perilaku klik pengguna; kedua, uji A/B kausal baru berupa rancangan siap pakai dan belum dijalankan langsung di toko live; ketiga, kalibrasi Platt masih berada pada lapisan pembungkus evaluasi terpisah dari file `.joblib` mentah.
- **Jawaban Teknis:** Seluruh keterbatasan ini didokumentasikan jujur di `KNOWN_LIMITATIONS.md`, sekaligus menunjukkan arah pengembangan selanjutnya: menyematkan *CalibratedClassifierCV / Platt wrapper* langsung ke dalam pipeline `.joblib` inferensi API, menghubungkan data *clickstream* real-time untuk memperkuat sinyal Pos T0 checkout, dan menutup siklus *causal feedback* dari eksperimen A/B langsung ke peladen `FastAPI`.

---

## LAMPIRAN CEPAT: PERINTAH REPRODUKSI & PRESENTASI DARI TERMINAL

```bash
# 1. Aktifkan lingkungan virtual Python
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/macOS

# 2. Jalankan seluruh pengujian otomatis & audit 12 gerbang rilis
python -m pytest
python tools/check_claims.py
python tools/verify_release.py

# 3. Audit ulang performa langsung dari file model (.joblib) terhadap Parquet
python scripts/reevaluate_locked_test.py

# 4. Jalankan Layanan Mikro FastAPI (Terminal 1) & Kokpit CSIP Studio (Terminal 2)
python -m uvicorn csip.api.server:app --host 127.0.0.1 --port 8000
python -m streamlit run app/streamlit_app.py --server.port 8501

# 5. Kompilasi ulang buku & skrip presentasi PDF ini
python scripts/build_csip_book.py
```

---
*Akhir Buku Induk & Skrip Presentasi Master — Core Strategy & Intelligence Platform (CSIP v1.1.0).*
