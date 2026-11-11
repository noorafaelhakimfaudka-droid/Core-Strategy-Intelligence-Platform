# CSIP Data Card: Brazilian E-Commerce Public Dataset (Olist)
## Dokumentasi Aset Data, Provenansi, dan Karakteristik Distribusi

Sesuai standar dokumentasi etika dan transparansi machine learning (*Data Cards for Data Integrity*, Gebru et al.).

---

## 1. Ikhtisar Dataset (Dataset Overview)
- **Nama Dataset**: Brazilian E-Commerce Public Dataset by Olist
- **Penyedia Data**: Olist via Kaggle Datasets (Domain Publik)
- **Periode Waktu**: September 2016 s/d Agustus 2018 (24 bulan)
- **Cakupan Wilayah**: Republik Federasi Brasil (27 negara bagian, 4.119 kode pos)
- **Ukuran Data Raw**: ~120 MB CSV (9 tabel relasional)
- **Ukuran Data Processed**: 96.478 pesanan terkirim (18.43 MB Parquet)

---

## 2. Struktur Relasional & Grain Entitas
- **Entitas Inti**: `order_id` (Grain satu baris per pesanan e-commerce)
- **Tabel Relasional**:
  1. `olist_orders_dataset`: Metadata status dan jejak waktu siklus hidup pesanan (99.441 baris)
  2. `olist_order_items_dataset`: Rincian barang, harga, dan alokasi penjual (112.650 baris)
  3. `olist_order_payments_dataset`: Metode pembayaran, nilai angsuran (*installments*) (103.886 baris)
  4. `olist_order_reviews_dataset`: Skor bintang (1-5), pesan ulasan, dan waktu respons (99.224 baris)
  5. `olist_customers_dataset`: Pemetaan customer unik dan lokasi negara bagian (99.441 baris)
  6. `olist_sellers_dataset`: Lokasi gudang penjual (3.095 penjual)
  7. `olist_products_dataset`: Kategori produk, dimensi fisik, dan bobot gram (32.951 produk)
  8. `olist_geolocation_dataset`: Koordinat lintang/bujur per prefix kode pos (1.000.163 baris)

---

## 3. Karakteristik Target & Distribusi
- **Target Primer (Review Risk)**: `negative_review_flag` (1 jika `review_score <= 2`, 0 jika `>= 3`).
  - Total Teramati (Delivered): 95.832 ulasan
  - Kelas Negatif (Positif Target): 12.272 (12.81%)
  - Kelas Puas (Negatif Target): 83.560 (87.19%)
  - Rasio Ketimpangan: ~1 : 6.8 (memerlukan metrik PR-AUC dan Brier Score terkalibrasi)
- **Ulasan Hilang (Missing Reviews)**: 646 pesanan (0.67%)
  - Analisis Batas Seleksi Manski: Prevalensi negatif berada pada interval [11.44%, 12.10%].
- **Target Sekunder (Repeat Purchase)**: `repeat_purchase_flag` (1 jika customer belanja ulang dalam 90 hari).
  - Prevalensi: 3.12% (sensor kanan dimitigasi via Discrete-Time Hazard dan Kaplan-Meier).

---

## 4. Partisi Waktu & Embargo (Data Hygiene)
- **Training Expansions**: 2016-09-15 s/d 2018-02-15 (expanding across 4 folds).
- **Mandatory Embargo**: 90 hari kalender (`max(ts_train) + 90 hari <= min(ts_val)`).
- **Validation Folds**: 4 jendela evaluasi out-of-time (total 30.487 pesanan evaluasi CV).
- **Locked Test Set**: 2018-07-01 s/d 2018-08-29 (12.448 pesanan), dievaluasi tepat satu kali.

---

## 5. Pertimbangan Etis & Kebijakan Privasi
- **Anonimisasi**: Semua data identitas pribadi pelanggan (nama asli, alamat jalan, nomor telepon, dokumen pajak CPF/CNPJ) telah dienkripsi atau dihapus pada sumber publik oleh Olist.
- **Batasan Penggunaan**: Dataset ini ditujukan khusus untuk penelitian metodologi data science, riset akademis, dan portofolio kompetensi. Tidak digunakan untuk profiling individu nyata atau penentuan kelayakan kredit.

