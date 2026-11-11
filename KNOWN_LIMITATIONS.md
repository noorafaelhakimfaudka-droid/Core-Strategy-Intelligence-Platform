# CSIP Known Limitations & Scientific Scope Disclosure
## Core Strategy & Intelligence Platform — Version 1.0.0

Dokumen ini mendokumentasikan batasan metodologis, keterbatasan data, dan ruang lingkup operasional CSIP secara terbuka dan jujur, sesuai dengan standar etika ilmu data (SKKNI 299/2020) dan aturan rekayasa verifikasi.

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

## 5. Status Konfirmasi Pengguna Eksternal (UK-01 KUK 2.2, 3.3, 4.3)
- **Konteks**: Karena riset ini berbasis dataset historis publik, persetujuan pengguna akhir eksternal saat ini berstatus `EXTERNAL_CONFIRMATION_REQUIRED`.
- **Mitigasi**: Kandidat menyusun paket pertahanan tata kelola lengkap (`competency/external_approvals/STAKEHOLDER_APPROVAL_DEFENSE_PACKET.md`) yang berisi rubrik kebutuhan, register risiko, dan struktur biaya-keuntungan yang siap ditandatangani oleh pemangku kepentingan saat platform diimplementasikan di industri.

---

## 6. Ruang Lingkup Verifikasi Skema LSP TRI
- **Verifikasi Resmi**: Halaman resmi skema sertifikasi LSP TRI (`lsptri.id/skema/sertifikasi-ilmuwan-data-SKKNI`) memverifikasi: 11 kode dan judul unit SKKNI 299/2020, nomor skema `SKM/2905/LSP-TRI/VII/2025`, jenjang KKNI Level 7, metode uji Portofolio dan Instruksi Terstruktur, serta lingkup kerja mencakup "mendukung deployment model".
- **Elemen dan KUK**: Rincian 27 elemen dan 63 KUK berstatus `NOT VERIFIED` terhadap sumber online resmi sampai dokumen SKKNI 299/2020 atau FR/APL resmi diterbitkan secara publik. Proyek ini memetakan 63 KUK secara konsisten berdasarkan kanonikal internal.

