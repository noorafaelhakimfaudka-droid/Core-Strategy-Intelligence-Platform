# CSIP Known Limitations & Scientific Scope Disclosure
## Core Strategy & Intelligence Platform — Version 1.1.0

Dokumen ini mendokumentasikan batasan metodologis, keterbatasan data, dan ruang lingkup operasional CSIP secara terbuka dan jujur.

---

## 1. Sifat Data Sekunder Observasional (Bukan Eksperimen A/B)
- **Sumber Data**: Dataset publik Brazilian E-Commerce Olist (100.000 pesanan, kurun waktu 2016 s/d 2018).
- **Implikasi**: Data ini adalah data observasional historis tanpa randomisasi perlakuan intervensi (*A/B testing*).
- **Batasan Klaim**: Hubungan antara fitur (seperti rasio ongkir atau keterlambatan pengiriman) dengan kepuasan pelanggan dibatasi pada **Level L2 (Asosiasional)**. CSIP tidak mengklaim bukti kausalitas murni (L3) tanpa adanya eksperimen terkontrol lapangan.

---

## 2. Model Risiko Ulasan Bersifat Retrospektif (Pasca-Delivery)
- **Keterbatasan Waktu**: Fitur penentu utama ulasan negatif (terutama `delivery_delay_days` dan waktu penerimaan barang) baru diketahui secara fisik setelah kurir menyelesaikan pengantaran.
- **Ketidaklayakan Checkout**: Berdasarkan studi kelayakan formal (`reports/methodology/CHECKOUT_RISK_FEASIBILITY.md`), 99.0% pesanan yang berstatus *unavailable* tidak memiliki catatan item produk di database Olist. Mencoba memaksakan model berbasis produk saat checkout akan membuang sebagian besar pesanan non-delivered.
- **Penggunaan yang Sah**: Model ini berfungsi sebagai sistem *early warning* pasca-pengiriman untuk mendeteksi pesanan bermasalah sebelum atau saat ulasan tiba, bukan saat checkout.

---

## 3. Prediksi Pembelian Ulang (Repeat Purchase) & Sensor Kanan
- **Distribusi Sangat Timpang**: Hanya ~3% pelanggan yang melakukan pembelian ulang dalam periode observasi.
- **Sensor Kanan (Right-Censoring)**: Banyak pelanggan yang melakukan pembelian pertama di kuartal akhir data (2018) belum sempat melakukan repeat purchase dalam jendela 90 hari.
- **Mitigasi**: Digunakan pemisahan kohor dan metode analisis survival non-parametrik (Kaplan-Meier) serta model *Discrete-Time Hazard* untuk memodelkan probabilitas bersyarat secara adil.

---

## 4. Analisis Batas Seleksi Manski atas Ulasan Hilang
- **Temuan**: Dari 96.478 pesanan terkirim, terdapat 646 pesanan (0.67%) yang tidak memiliki skor ulasan (`NaN`).
- **Uji Sensitivitas**: Berdasarkan analisis batas seleksi Manski (*Manski selection bounds*):
  - Kasus terekstrem terburuk: Prevalensi negatif = 12.10%
  - Kasus terekstrem terbaik: Prevalensi negatif = 11.44%
  - Delta batas seleksi <= 0.59%
- **Konklusi**: Efek seleksi non-respons ulasan sangat kecil dan tidak mengubah kesimpulan pemodelan secara material.

---

## 5. Rekomendasi Mesin Keputusan: Observasional vs. Kausalitas Intervensi (L2 vs. L3)
- **Sifat Rekomendasi**: Rekomendasi operasional yang dihasilkan oleh `BusinessDecisionEngine` didasarkan pada pemetaan aturan heuristik atas skor risiko prediksi asosiasional (Judea Pearl Level L2).
- **Batasan Pembuktian**: CSIP **tidak mengklaim** bahwa tindakan intervensi (seperti kontak proaktif atau perubahan mitra logistik) secara otomatis menjamin penurunan laju ulasan negatif atau pembatalan, karena data historis Olist tidak memuat uji coba acak terkendali (*randomized controlled trial* / A/B testing).
- **Protokol Verifikasi**: Evaluasi efektivitas intervensi harus dilakukan melalui pilot bertahap dengan kelompok kontrol (*holdout control group*) sebelum diterapkan secara penuh ke seluruh pesanan.

---

## 6. Beban Operasional False Positive & Batasan Kapasitas Triage
- **Dilema Presisi vs. Recall**: Pada tingkat prevalensi ulasan negatif yang rendah (~8-10%), menargetkan recall tinggi akan meningkatkan jumlah *false positive* (pesanan yang diprediksi berisiko padahal tidak bermasalah).
- **Beban Tim Operasional**: Setiap intervensi layanan pelanggan atau eskalasi logistik membutuhkan waktu dan biaya operasional riil. Jika batas ambang risiko ditetapkan terlalu rendah tanpa kuota triage harian, tim operasional akan mengalami kelebihan beban kerja (*alert fatigue*).
- **Mitigasi Operasional**: `BusinessDecisionEngine` dilengkapi konfigurasi kapasitas operasional maksimal (`max_daily_capacity`) dan klasifikasi prioritas bertingkat (CRITICAL, HIGH, MEDIUM, LOW) untuk membatasi intervensi pada kasus dengan dampak tertinggi.

---

## 7. Batas Daya Prediksi Tabular Pembelian Ulang (Repeat Purchase)
- **Temuan Empiris Negatif**: Model tabular *repeat purchase* berbasis data checkout menunjukkan interval kepercayaan 95% untuk ROC-AUC melintasi garis peluang acak ($0.50$), yaitu $[0.472, 0.531]$.
- **Kejujuran Ilmiah**: CSIP secara transparan mendokumentasikan temuan negatif ini sebagai keterbatasan inheren dari sinyal fitur transaksi awal Olist, dan tidak memaksakan klaim prediksi akurat pada ranah yang secara statistik tidak didukung oleh data.

---

## 8. Partisi Pos Operasional: Peringatan Dini Checkout vs. Pasca-Pengiriman
- **Isolasi Fitur Pos Terbuka**: Model peringatan dini checkout (`best_early_warning_review_lightgbm`) secara ketat dibatasi pada 10 fitur yang sah diketahui saat pembayaran, dengan performa aktual pada holdout terkunci ($N=12.571$) sebesar PR-AUC **0.1335** (95% CI $[0.1220, 0.1480]$), ROC-AUC **0.5468**, dan Brier uncalibrated **0.2370**. Sinyal prediktif saat checkout masih lemah karena faktor penentu utama kepuasan (keterlambatan transit kurir) belum terjadi.
- **Model Pasca-Pengiriman**: Model ulasan pasca-pengiriman (`best_negative_review_lightgbm`) memanfaatkan 15 fitur termasuk durasi aktual transit dan hari keterlambatan logistik, mencapai PR-AUC **0.3061** (95% CI $[0.2792, 0.3343]$) dan ROC-AUC **0.6745** (Brier uncalibrated **0.1373**; Brier **0.0762** dengan kalibrator Platt eksternal di `ModelExplainer`).
- **Larangan Kontaminasi**: Model pasca-pengiriman dilarang keras digunakan pada antarmuka checkout karena melibatkan variabel masa depan (*lookahead leakage*).


