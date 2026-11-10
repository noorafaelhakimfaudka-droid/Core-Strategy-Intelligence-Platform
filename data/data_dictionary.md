# KAMUS DATA (DATA DICTIONARY) — CSIP MVP BDI
**Kepatuhan SKKNI: [UK-03 Menelaah Data] & [UK-05 Menentukan Objek Data]**
**Dataset Acuan**: Brazilian E-Commerce Public Dataset by Olist (9 Tabel Relasional)

Dokumen ini mendokumentasikan skema, tipe data, relasi kunci, dan peran analitik dari 9 tabel relasional Olist yang digunakan dalam platform CSIP.

---

## 1. Diagram Relasi Entitas (ERD) Konseptual

```text
[customers] (customer_unique_id, customer_id)
      | 1:N
[orders] (order_id, customer_id)
      |-- 1:N --> [order_items] (order_id, order_item_id)
      |                 |-- N:1 --> [products] (product_id)
      |                 |                 |-- N:1 --> [category_translation]
      |                 +-- N:1 --> [sellers] (seller_id)
      |                                   +-- N:1 --> [geolocation] (zip_code_prefix)
      |-- 1:N --> [order_payments] (order_id, payment_sequential)
      +-- 1:N --> [order_reviews] (review_id, order_id)
```

---

## 2. Rincian Kamus Data 9 Tabel Relasional

### 2.1 `olist_orders_dataset.csv`
- **Grain**: 1 baris per pesanan (`order_id`).
- **Total Baris**: 99,441 baris | **Total Kolom**: 8 kolom.
- **Primary Key**: `order_id` (Unik 100%).
- **Foreign Key**: `customer_id` $\to$ `olist_customers_dataset.customer_id`.
- **Peran dalam CSIP**: Tulang punggung kronologis transaksi, status pesanan, dan perhitungan durasi pemenuhan serta keterlambatan pengiriman.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `order_id` | `object` | `object` | 0.00% | Identifikator unik dari setiap transaksi pesanan. |
| `customer_id` | `object` | `object` | 0.00% | Identifikator sesi transaksi pelanggan (bukan ID unik pelanggan). |
| `order_status` | `object` | `category` | 0.00% | Status pemenuhan (`delivered`, `shipped`, `canceled`, dll.). |
| `order_purchase_timestamp` | `object` | `datetime64[ns]` | 0.00% | Waktu pelanggan melakukan pemesanan (waktu acuan transaksi). |
| `order_approved_at` | `object` | `datetime64[ns]` | 0.16% | Waktu pembayaran disetujui oleh gerbang pembayaran. |
| `order_delivered_carrier_date` | `object` | `datetime64[ns]` | 1.79% | Waktu pesanan diserahkan penjual ke mitra kurir pengiriman. |
| `order_delivered_customer_date`| `object` | `datetime64[ns]` | 2.98% | Waktu aktual pesanan diterima oleh pelanggan. |
| `order_estimated_delivery_date`| `object` | `datetime64[ns]` | 0.00% | Tanggal estimasi pengiriman yang dijanjikan pada saat checkout. |

---

### 2.2 `olist_order_items_dataset.csv`
- **Grain**: 1 baris per item barang dalam pesanan (`order_id`, `order_item_id`).
- **Total Baris**: 112,650 baris | **Total Kolom**: 7 kolom.
- **Primary Key**: Komposit (`order_id`, `order_item_id`).
- **Foreign Keys**: `product_id` $\to$ `products`, `seller_id` $\to$ `sellers`.
- **Peran dalam CSIP**: Variabel ekonomi inti (harga barang dan ongkos kirim) untuk menguji hipotesis friksi biaya (H1, H4).

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `order_id` | `object` | `object` | 0.00% | Identifikator pesanan induk. |
| `order_item_id` | `int64` | `int16` | 0.00% | Nomor urut item dalam pesanan (1, 2, 3...). |
| `product_id` | `object` | `object` | 0.00% | Identifikator unik produk barang. |
| `seller_id` | `object` | `object` | 0.00% | Identifikator unik penjual/merchant. |
| `shipping_limit_date` | `object` | `datetime64[ns]` | 0.00% | Batas waktu penjual harus menyerahkan pesanan ke kurir. |
| `price` | `float64` | `float32` | 0.00% | Harga barang per unit dalam mata uang Real Brasil (BRL). |
| `freight_value` | `float64` | `float32` | 0.00% | Biaya ongkos kirim per item dalam mata uang BRL. |

---

### 2.3 `olist_order_payments_dataset.csv`
- **Grain**: 1 baris per metode pembayaran per pesanan (`order_id`, `payment_sequential`).
- **Total Baris**: 103,886 baris | **Total Kolom**: 5 kolom.
- **Primary Key**: Komposit (`order_id`, `payment_sequential`).
- **Peran dalam CSIP**: Indikator daya beli, penggunaan cicilan (*installments*), dan split payment.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `order_id` | `object` | `object` | 0.00% | Identifikator pesanan terkait. |
| `payment_sequential` | `int64` | `int16` | 0.00% | Urutan pembayaran untuk pesanan yang menggunakan banyak metode. |
| `payment_type` | `object` | `category` | 0.00% | Jenis pembayaran (`credit_card`, `boleto`, `voucher`, `debit_card`). |
| `payment_installments` | `int64` | `int16` | 0.00% | Jumlah cicilan yang dipilih pembeli. |
| `payment_value` | `float64` | `float32` | 0.00% | Nilai nominal transaksi yang dibayarkan. |

---

### 2.4 `olist_order_reviews_dataset.csv`
- **Grain**: 1 baris per ulasan pesanan (`review_id`).
- **Total Baris**: 99,224 baris | **Total Kolom**: 7 kolom.
- **Primary Key**: `review_id`.
- **Foreign Key**: `order_id` $\to$ `orders.order_id`.
- **Peran dalam CSIP**: Target kepuasan pelanggan (`review_score` 1–5) dan korpus teks untuk Deep Learning NLP.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `review_id` | `object` | `object` | 0.00% | Identifikator unik ulasan. |
| `order_id` | `object` | `object` | 0.00% | Identifikator pesanan yang diulas. |
| `review_score` | `int64` | `int8` | 0.00% | Skor kepuasan pelanggan (skala ordinal integer 1 s/d 5). |
| `review_comment_title` | `object` | `object` | 88.34% | Judul pesan ulasan (opsional). |
| `review_comment_message` | `object` | `object` | 58.70% | Isi pesan teks ulasan pelanggan dalam bahasa Portugis. |
| `review_creation_date` | `object` | `datetime64[ns]` | 0.00% | Tanggal survei kepuasan dikirimkan ke pelanggan. |
| `review_answer_timestamp` | `object` | `datetime64[ns]` | 0.00% | Waktu pelanggan mengisi survei kepuasan. |

---

### 2.5 `olist_customers_dataset.csv`
- **Grain**: 1 baris per sesi transaksi pembeli (`customer_id`).
- **Total Baris**: 99,441 baris | **Total Kolom**: 5 kolom.
- **Primary Key**: `customer_id`.
- **Entity Key Sebenarnya**: `customer_unique_id` (96,096 pelanggan unik).
- **Peran dalam CSIP**: Pelacakan pembelian ulang (*repeat purchase*) dan segmentasi kohort pelanggan.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `customer_id` | `object` | `object` | 0.00% | ID sesi belanja (berganti setiap kali transaksi baru dibuat). |
| `customer_unique_id` | `object` | `object` | 0.00% | **ID unik pelanggan sesungguhnya** (digunakan untuk retensi). |
| `customer_zip_code_prefix`| `int64` | `int32` | 0.00% | 5 digit awal kode pos pelanggan. |
| `customer_city` | `object` | `object` | 0.00% | Nama kota tempat tinggal pelanggan. |
| `customer_state` | `object` | `category` | 0.00% | Kode 2 huruf negara bagian di Brasil (27 negara bagian). |

---

### 2.6 `olist_sellers_dataset.csv`
- **Grain**: 1 baris per penjual (`seller_id`).
- **Total Baris**: 3,095 baris | **Total Kolom**: 4 kolom.
- **Primary Key**: `seller_id`.
- **Peran dalam CSIP**: Analisis kinerja logistik penjual dan perhitungan jarak geografis seller-buyer.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `seller_id` | `object` | `object` | 0.00% | Identifikator unik penjual. |
| `seller_zip_code_prefix` | `int64` | `int32` | 0.00% | 5 digit awal kode pos lokasi gudang penjual. |
| `seller_city` | `object` | `object` | 0.00% | Nama kota tempat gudang penjual beroperasi. |
| `seller_state` | `object` | `category` | 0.00% | Kode 2 huruf negara bagian penjual. |

---

### 2.7 `olist_products_dataset.csv`
- **Grain**: 1 baris per produk unik (`product_id`).
- **Total Baris**: 32,951 baris | **Total Kolom**: 9 kolom.
- **Primary Key**: `product_id`.
- **Peran dalam CSIP**: Karakteristik fisik barang, kategori produk, dan determinan biaya ongkir.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi & Aturan Bisnis |
|---|---|---|---|---|
| `product_id` | `object` | `object` | 0.00% | Identifikator unik produk katalog. |
| `product_category_name` | `object` | `category` | 1.85% | Nama kategori produk dalam bahasa Portugis. |
| `product_name_lenght` | `float64` | `float32` | 1.85% | Jumlah karakter judul nama produk. |
| `product_description_lenght`| `float64` | `float32` | 1.85% | Jumlah karakter deskripsi produk. |
| `product_photos_qty` | `float64` | `float32` | 1.85% | Jumlah foto produk dalam listing. |
| `product_weight_g` | `float64` | `float32` | 0.01% | Berat fisik produk dalam satuan gram. |
| `product_length_cm` | `float64` | `float32` | 0.01% | Panjang dimensi produk dalam cm. |
| `product_height_cm` | `float64` | `float32` | 0.01% | Tinggi dimensi produk dalam cm. |
| `product_width_cm` | `float64` | `float32` | 0.01% | Lebar dimensi produk dalam cm. |

---

### 2.8 `olist_geolocation_dataset.csv`
- **Grain Asli**: Koordinat per kode pos (`geolocation_zip_code_prefix`).
- **Total Baris**: 1,000,163 baris | **Total Kolom**: 5 kolom.
- **Aturan Agregasi CSIP**: Menggunakan nilai **median** `lat` dan `lng` per `zip_code_prefix` untuk mencegah *Cartesian product explosion* saat melakukan join.
- **Peran dalam CSIP**: Menghitung jarak spasial Haversine antara kode pos penjual dan pembeli.

| Nama Kolom | Tipe Data Asli | Tipe Data Downcast | Null (%) | Deskripsi |
|---|---|---|---|---|
| `geolocation_zip_code_prefix` | `int64` | `int32` | 0.00% | 5 digit kode pos. |
| `geolocation_lat` | `float64` | `float32` | 0.00% | Derajat lintang (Latitude). |
| `geolocation_lng` | `float64` | `float32` | 0.00% | Derajat bujur (Longitude). |
| `geolocation_city` | `object` | `object` | 0.00% | Nama kota kode pos. |
| `geolocation_state` | `object` | `category` | 0.00% | Kode negara bagian. |

---

### 2.9 `product_category_name_translation.csv`
- **Grain**: 1 baris per nama kategori.
- **Total Baris**: 71 baris | **Total Kolom**: 2 kolom.
- **Peran dalam CSIP**: Menerjemahkan 71 kategori produk dari bahasa Portugis ke bahasa Inggris untuk standardisasi interpretasi.

---

## 3. Spesifikasi 4 Analytical Grains (Objek Data)

1. **Order-Level Analytical Table (`data/processed/order_level.parquet`)**:
   - Primary Key: `order_id`
   - Target: `review_score` (1–5) & `negative_review_flag` ($\le 2$), `delivery_delay_days`.
   - Sumber Join: `orders` + aggregated `order_items` + aggregated `payments` + aggregated `reviews` + buyer/seller distance.
2. **Customer-Cohort Table (`data/processed/customer_cohort.parquet`)**:
   - Primary Key: `customer_unique_id`
   - Target: `repeat_purchase_flag` (apakah ada transaksi ke-2 dalam $\Delta W = 90$ hari).
   - Fitur: HANYA fitur transaksi pertama (*First-Order Isolation*) untuk mencegah *data leakage*.
3. **Review-Text Corpus Table (`data/processed/review_corpus.parquet`)**:
   - Primary Key: `review_id`
   - Kolom: `review_comment_message`, `review_score`, `has_review_comment`.
   - Peran: Pemodelan klasifikasi teks Naive Bayes dan Deep Learning Bi-LSTM.
4. **Weekly System State Panel (`data/processed/weekly_system_state.parquet`)**:
   - Primary Key: `year_week`
   - Kolom: Volume pesanan, rata-rata rasio ongkir, rata-rata durasi kirim, persentase telat, estimasi repeat rate.
   - Peran: *World Model* dan simulasi skenario intervensi (*Alternative World*).

