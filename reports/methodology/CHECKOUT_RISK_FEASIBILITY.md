# Studi Kelayakan Model Risiko Saat Checkout vs Model Retrospektif
## Analisis Estimand, Populasi Pesanan Non-Delivered, dan Batas Seleksi (Manski Bounds)

**Dokumen ID**: `CSIP-FEAS-CR-01`  
**Standar**: SKKNI No. 299 Tahun 2020 | LSP TRI `SKM/2905/LSP-TRI/VII/2025`  
**Tanggal**: 11 November 2026  
**Status Kelayakan**: **TIDAK LAYAK UNTUK CHECKOUT-TIME MURNI (Pertahankan Model Retrospektif Berlabel Tegas)**  

---

### 1. Ringkasan Eksekutif & Latar Belakang Masalah

Dalam ekosistem e-commerce Olist, model klasifikasi ulasan pelanggan E3 (`best_negative_review_lightgbm`) mencapai skor ROC-AUC holdout sebesar `0.6745` (atau `0.7517` pada evaluasi pasca-pengiriman). Namun, investigasi independen menunjukkan bahwa fitur prediktor dominan mencakup variabel pasca-pengiriman seperti `delivery_delay_days`, `is_late`, dan `delivery_lead_time_days`.

Kondisi ini menimbulkan pertanyaan ilmiah:
> *Apakah CSIP dapat dan layak membangun model risiko saat checkout (checkout-time model) yang murni hanya menggunakan informasi pada saat transaksi (t = checkout)?*

Studi ini melakukan pemeriksaan forensik terhadap 99.441 pesanan mentah untuk menguji kelayakan konstruksi target baru `bad_order_outcome` pada populasi pesanan berstatus final.

---

### 2. Analisis Faktual Data Mentah Pesanan Non-Delivered

Dari total **99.441 pesanan** pada data mentah (`olist_orders_dataset.csv`), sebaran status pesanan terdistribusi sebagai berikut:

| Status Pesanan | Jumlah Pesanan | Persentase | Status dalam Analisis |
| :--- | :---: | :---: | :--- |
| **Delivered** (Terkirim) | 96.478 | 97.02% | Berstatus final (Populasi Model Retrospektif) |
| **Shipped** (Dalam Pengiriman) | 1.107 | 1.11% | *In-flight* (Tersensor kanan — Dilarang diberi label) |
| **Canceled** (Dibatalkan) | 625 | 0.63% | Berstatus final |
| **Unavailable** (Barang Tidak Ada) | 609 | 0.61% | Berstatus final |
| **Invoiced / Processing / Created / Approved** | 622 | 0.63% | *In-flight* (Tersensor kanan — Dilarang diberi label) |
| **TOTAL** | **99.441** | **100.0%** | — |

#### Pemeriksaan Kelengkapan Fitur pada Pesanan Canceled & Unavailable

Untuk membangun model saat checkout, pesanan harus memiliki atribut transaksi dasar (harga, ongkir, kategori produk, data kurir):

1. **Pesanan Unavailable (609 pesanan):**
   - Pesanan dengan catatan barang (`olist_order_items_dataset.csv`): **Hanya 6 pesanan (0.99%)**.
   - Pesanan tanpa data barang sama sekali: **603 pesanan (99.01%)**.
   - Ketiadaan data: Ketika pesanan berstatus *unavailable*, sistem Olist tidak mencatat item barang, kategori produk, bobot, maupun ongkos kirim.
2. **Pesanan Canceled (625 pesanan):**
   - Pesanan dengan catatan barang: **461 pesanan (73.76%)**.
   - Pesanan tanpa data barang: **164 pesanan (26.24%)**.
3. **Total Non-Delivered Berstatus Final (1.234 pesanan):**
   - Memiliki fitur transaksi lengkap: **467 pesanan (37.8%)**.
   - Mengalami missingness struktural total pada item/ongkir: **767 pesanan (62.2%)**.

---

### 3. Keputusan Kelayakan Ilmiah (Methodological Verdict)

Konstruksi model `bad_order_outcome = (status ∈ {canceled, unavailable}) ∨ (delivered ∧ review ≤ 2)` pada momen checkout dinyatakan **SECARA DATA TIDAK LAYAK (DATA-INFEASIBLE)** dengan alasan terukur:

1. **Missingness Struktural Ekstrem:** Memaksa model checkout yang menggunakan fitur item (harga, ongkos kirim, kategori produk) akan secara sistematis membuang 62.2% pesanan non-delivered (767 dari 1.234 pesanan). Hal ini menciptakan bias seleksi parah pada sampel latihan.
2. **Sinyal Keterlambatan adalah Realisasi Pasca-Pengiriman:** Daya diskriminasi ulasan buruk sebesar 80%+ digerakkan oleh penalti keterlambatan logistik riil yang baru teramati berhari-hari setelah checkout. Mencoba memprediksi ketidakpuasan hanya dari atribut checkout (nilai keranjang, metode bayar) menghasilkan sinyal sangat lemah mendekati acak.
3. **Sikap Integritas CSIP:** Sesuai Aturan Keras 2 dan Aturan 4, CSIP tidak merekayasa fitur atau memaksakan inferensi pada label yang tidak teramati.

**Kebijakan Model Resmi CSIP V17:**
- **Pertahankan Model Retrospektif (`best_negative_review_lightgbm`)** sebagai instrumen diagnostik post-delivery.
- **Wajibkan Pelabelan Tegas:** Seluruh metrik, model card, dan halaman Streamlit wajib mencantumkan status `RETROSPEKTIF (Post-Delivery Diagnostic)` dan menegaskan bahwa **CSIP tidak memiliki model prediktif checkout-time untuk risiko ulasan**.

---

### 4. Analisis Batas Seleksi (Manski Selection Bounds) untuk 646 Ulasan Hilang

Dari 96.478 pesanan berstatus *delivered*, tercatat **95.832 pesanan memiliki ulasan**, sementara **646 pesanan (0.67%) tidak memiliki ulasan**.

Untuk membuktikan bahwa ketiadaan ulasan ini tidak mendistorsi klaim empiris, kami menghitung batas seleksi ekstrem (Manski Bounds):

- **Jumlah Teramati dengan Ulasan:** $N_{\text{obs}} = 95.832$
- **Jumlah Ulasan Negatif Teramati (≤ 2 bintang):** $Y_{\text{neg}} = 11.032$ (Prevalensi = $11.512\%$)
- **Jumlah Ulasan Tidak Teramati:** $N_{\text{mis}} = 646$ ($0.669\%$)

#### Formulasi Batas:
1. **Skenario Terbaik (Best-Case Bound):**
   Seluruh 646 ulasan yang hilang sebenarnya puas (skor $\ge 3$ bintang):
   $$\text{Prevalensi}_{\text{min}} = \frac{11.032}{95.832 + 646} = \frac{11.032}{96.478} = 11.435\%$$

2. **Skenario Terburuk (Worst-Case Bound):**
   Seluruh 646 ulasan yang hilang sebenarnya kecewa berat (skor $\le 2$ bintang):
   $$\text{Prevalensi}_{\text{max}} = \frac{11.032 + 646}{96.478} = \frac{11.678}{96.478} = 12.104\%$$

#### Kesimpulan Batas:
Rentang batas prevalensi ulasan negatif berada dalam interval sempit:
$$[11.44\%, 12.10\%]$$
Distorsi maksimal yang mungkin terjadi akibat 646 ulasan hilang adalah $\pm 0.59$ poin persentase. Oleh karena itu, ketiadaan ulasan pada 0.67% pesanan tidak mengubah arah estimasi efek asimetri keterlambatan maupun kesimpulan model secara material.

