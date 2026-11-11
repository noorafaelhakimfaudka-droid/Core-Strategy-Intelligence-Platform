# LAPORAN VALIDASI KUALITAS DATA (DATA QUALITY REPORT)
**Kepatuhan Standar: Metodologi Data Science [UK-04 Memvalidasi Data] & Spesifikasi Sistem Validation Gate G1**
**Tanggal Audit**: 2026-11-10 | **Dataset**: Olist Brazilian E-Commerce (9 Tabel Relasional)
**Auditor**: CSIP Lead Data Science Architect

---

## 1. Ringkasan Eksekutif & Status Validation Gate G1

| Parameter Audit | Hasil Evaluasi Empiris | Status Kepatuhan |
|---|---|:---:|
| **Status Validation Gate G1** | Seluruh 9 tabel selesai ditelaah, skema tervalidasi, anomali terinventarisasi | **PASS** |
| **Total Tabel Divalidasi** | 9 tabel relasional (~1.43 juta baris total di memori) | **PASS** |
| **Integritas Kunci Primer (PK)** | $100\%$ unik pada tabel `orders`, `customers`, `sellers`, `products`, `reviews` | **PASS** |
| **Integritas Referensial (FK)** | **0 Orphan Records** pada 6 hubungan relasi kunci antar-tabel | **PASS (EXCELLENT)** |
| **Uji Rentang Nilai Numerik** | `price > 0`, `freight >= 0`, `payment >= 0`, `review_score in [1..5]` | **PASS** |
| **Optimasi Memori (8 GB RAM)** | Total memori mentah berkurang dari **132.4 MB** menjadi **87.0 MB** (**-34.3%**) | **PASS** |

---

## 2. Matriks Inventaris & Profiling 9 Tabel Olist

| Nama Tabel | File Sumber | Baris | Kolom | Primary Key | Duplikat PK | RAM Awal | RAM Downcast | Reduksi (%) |
|---|---|---:|---:|---|---:|---:|---:|---:|
| `orders` | `olist_orders_dataset.csv` | 99,441 | 8 | `order_id` | 0 | 21.95 MB | 11.48 MB | **-47.7%** |
| `order_items` | `olist_order_items_dataset.csv` | 112,650 | 7 | `(order_id, order_item_id)` | 0 | 18.37 MB | 14.83 MB | **-19.3%** |
| `order_payments` | `olist_order_payments_dataset.csv` | 103,886 | 5 | `(order_id, payment_seq)` | 0 | 8.11 MB | 4.85 MB | **-40.1%** |
| `order_reviews` | `olist_order_reviews_dataset.csv` | 99,224 | 7 | `review_id` | 0 | 17.84 MB | 13.68 MB | **-23.3%** |
| `customers` | `olist_customers_dataset.csv` | 99,441 | 5 | `customer_id` | 0 | 11.03 MB | 9.80 MB | **-11.2%** |
| `sellers` | `olist_sellers_dataset.csv` | 3,095 | 4 | `seller_id` | 0 | 0.22 MB | 0.19 MB | **-17.0%** |
| `products` | `olist_products_dataset.csv` | 32,951 | 9 | `product_id` | 0 | 3.73 MB | 2.17 MB | **-41.9%** |
| `geolocation` | `olist_geolocation_dataset.csv` | 1,000,163 | 5 | `zip_code_prefix` | Multiple | 50.12 MB | 30.09 MB | **-40.0%** |
| `category_translation` | `product_category_name_translation.csv` | 71 | 2 | `product_category_name` | 0 | 0.01 MB | 0.01 MB | 0.0% |
| **TOTAL** | **9 Tabel** | **1,451,922** | **52** | — | — | **132.38 MB** | **87.10 MB** | **-34.2%** |

---

## 3. Audit Integritas Referensial (Orphan Records Check)

Pemeriksaan baris yatim (*orphan records*) dilakukan untuk memastikan tidak ada transaksi atau item yang kehilangan induk relasinya:

```text
1. orders.customer_id          -> customers.customer_id        : 0 orphan (100% cocok)
2. order_items.order_id        -> orders.order_id              : 0 orphan (100% cocok)
3. order_items.product_id      -> products.product_id          : 0 orphan (100% cocok)
4. order_items.seller_id       -> sellers.seller_id            : 0 orphan (100% cocok)
5. order_payments.order_id     -> orders.order_id              : 0 orphan (100% cocok)
6. order_reviews.order_id      -> orders.order_id              : 0 orphan (100% cocok)
```

**Temuan**: Integritas relasional antara 9 tabel Olist berstatus **sempurna (zero orphan records)**. Semua pesanan terhubung ke pelanggan, produk, penjual, metode pembayaran, dan ulasan.

---

## 4. Audit Anomali Kronologis Timestamp (Sanity Check)

Pada tabel `orders`, dilakukan pengujian logika urutan waktu:
$$\text{Purchase Timestamp} \le \text{Approved At} \le \text{Carrier Date} \le \text{Delivered Customer Date}$$

### Temuan Anomali:
1. **Delivered Before Purchase**: Terdapat **23 pesanan** di mana `order_delivered_customer_date` tercatat lebih awal dari `order_purchase_timestamp`.
   - *Penyebab*: Kesalahan input sistem atau perbedaan zona waktu lokal.
   - *Tindakan Mitigasi*: Baris-baris ini ditandai sebagai data rusak dan disaring keluar pada tahap pembersihan (`csip.cleaning`).
2. **Delivered Before Carrier Date**: Terdapat **1 baris** di mana pesanan tercatat sampai ke pelanggan sebelum tanggal diserahkan ke kurir.
3. **Missing Delivered Date on Completed Orders**: Sebanyak **2,965 pesanan (2.98%)** memiliki nilai `order_delivered_customer_date == Null`. Dari jumlah tersebut, mayoritas adalah pesanan dengan status `shipped`, `canceled`, atau `unavailable`.
   - *Tindakan Mitigasi*: Hanya pesanan dengan status `delivered` yang digunakan untuk evaluasi waktu pemenuhan aktual.

---

## 5. Audit Entitas Pelanggan & Masalah Repeat Purchase

Analisis entitas pelanggan mengonfirmasi aturan kritis Spesifikasi Sistem Bagian 5.3:
- **Total Sesi Belanja (`customer_id`)**: $99,441$ sesi transaksi.
- **Total Pelanggan Sebenarnya (`customer_unique_id`)**: $96,096$ pelanggan unik.
- **Pelanggan dengan Pembelian Berulang ($> 1$ transaksi)**: $2,997$ pelanggan (**$3.12\%$**).

### Implikasi Metodologis & Rekayasa:
1. **Target Ketimpangan Ekstrem (Extreme Imbalance)**: Kelas positif (*repeat buyer*) hanya sebesar $3.12\%$. Evaluasi model **dilarang menggunakan akurasi biasa**, melainkan wajib menggunakan **PR-AUC (Precision-Recall AUC)**, *Balanced Accuracy*, dan kalibrasi probabilitas (*Brier Score*).
2. **Mitigasi Right-Censoring**: Karena dataset berakhir pada 17 Oktober 2018, pelanggan yang bertransaksi pertama kali dalam 90 hari sebelum tanggal akhir tidak memiliki kesempatan yang adil untuk melakukan transaksi kedua. Populasi evaluasi retensi wajib dipotong seragam $\Delta W = 90$ hari sebelum $T_{\max}$.

---

## 6. Audit Missing Values & Kualitas Kolom

1. **Ulasan Pesanan (`order_reviews`)**:
   - `review_comment_title`: Kosong sebesar **$88.34\%$** (hanya sedikit pelanggan yang menulis judul ulasan).
   - `review_comment_message`: Kosong sebesar **$58.70\%$** (pelanggan lebih sering hanya memberikan rating bintang 1–5 tanpa menulis ulasan teks panjang).
   - *Tindakan*: Dibuat fitur biner `has_review_comment` (1 jika ada ulasan teks, 0 jika kosong) dan teks kosong diimputasi dengan string kosong `""`.
2. **Karakteristik Produk (`products`)**:
   - Kolom dimensi (`product_weight_g`, `product_length_cm`, dll.) hanya memiliki nilai hilang sebesar **$0.01\%$ (hanya 2 baris)**.
   - Kolom nama kategori kosong sebesar **$1.85\%$ (610 produk)**.
   - *Tindakan*: Diimputasi dengan kategori `'unknown'` dan median dimensi kelompok.

---

## 7. Rekomendasi untuk Tahap Pembersihan & Rekayasa Fitur (Milestone 3 & 4)

1. **Deduplikasi Geolocation**: Terapkan agregasi median (`lat`, `lng`) per kode pos `geolocation_zip_code_prefix` sebelum melakukan join jarak geospasial untuk mencegah pembengkakan baris dari 1 juta ke puluhan juta baris.
2. **Deduplikasi Review Ganda**: Untuk pesanan dengan ulasan lebih dari satu, ambil ulasan berdasarkan `review_creation_date` terbaru.
3. **Penyaringan Status Pesanan**: Pisahkan analisis pengalaman pengiriman hanya pada status `delivered` dengan timestamp yang valid secara kronologis.
4. **First-Order Isolation**: Pastikan seluruh fitur prediktor retensi hanya bersumber dari pesanan pertama pelanggan untuk menjamin **Zero Data Leakage**.

