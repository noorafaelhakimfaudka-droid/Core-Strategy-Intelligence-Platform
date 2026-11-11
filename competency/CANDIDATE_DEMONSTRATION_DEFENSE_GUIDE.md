# Panduan Demonstrasi Praktik & Pertahanan Teknis Kandidat
## Skema sertifikasi profesi Data Scientist (LSP TRI / SKKNI 299/2020 — KKNI Level 7)

Dokumen ini adalah panduan operasional bagi kandidat dalam sesi uji kompetensi offline (Metode Uji: Portofolio dan Instruksi Terstruktur) untuk 11 Unit Kompetensi SKKNI 299/2020 pada platform **Core Strategy & Intelligence Platform (CSIP)**.

---

## 1. Sikap Etika & Transparansi Ilmiah Kandidat
1. **Bukan Auditor**: Kandidat tidak menetapkan skor sendiri atau mengklaim akreditasi independen tanpa bukti pengujian resmi.
2. **Keterbatasan Terbuka**: Semua asumsi, data observasional, dan hasil negatif (misalnya kesulitan prediksi repeat purchase murni) diakui secara ilmiah tanpa rekayasa.
3. **Pemisahan Status KUK**:
   - `VERIFIED`: Telah teruji melalui kode eksekusi dan tes otomatis pytest.
   - `CANDIDATE_DEMONSTRATION_REQUIRED` (13 KUK): Memerlukan demonstrasi langkah kerja dan penjelasan lisan kandidat.
   - `EXTERNAL_CONFIRMATION_REQUIRED` (3 KUK: UK-01 KUK 2.2, 3.3, 4.3): Persetujuan pengguna akhir yang belum diperoleh dari pihak eksternal pada data observasional historis.

---

## 2. Panduan per Unit Kompetensi (UK-01 s/d UK-11)

### [UK-01] Menentukan Objektif Bisnis (J.62DMI00.001.1)
- **Konteks Masalah**: E-commerce Olist mengalami tingkat keterlambatan 8.0%, yang menurunkan skor kepuasan dari 4.14 menjadi 2.15 bintang.
- **Perintah Demonstrasi**:
  ```bash
  python -c "import pandas as pd; df = pd.read_parquet('data/processed/order_level.parquet'); print(df.groupby('is_late')['review_score'].mean())"
  ```
- **Keluaran yang Diharapkan**:
  ```text
  is_late
  0    4.25
  1    2.26
  ```
- **Tanya Jawab Kritis**:
  - *Asesor*: "Mengapa persetujuan stakeholder (KUK 2.2, 3.3, 4.3) berstatus EXTERNAL_CONFIRMATION_REQUIRED?"
  - *Jawaban Kandidat*: "Dataset Olist adalah data sekunder publik (2016-2018). Kandidat secara etis tidak memalsukan tanda tangan eksternal, melainkan menyiapkan instrumen tata kelola enterprise (*defense packet*) yang siap disahkan ketika diimplementasikan pada entitas bisnis aktif."

---

### [UK-02] Menentukan Tujuan Teknis Data Science (J.62DMI00.002.1)
- **Tujuan Teknis**: Supervised Binary Classification dengan evaluasi out-of-time untuk memprediksi risiko ulasan negatif, dan analisis survival durasi repeat purchase.
- **Perintah Demonstrasi**:
  ```bash
  cat config/analysis_plan.yaml
  ```
- **Keluaran yang Diharapkan**:
  Terlihat spesifikasi estimand, target population, horizon 90 hari, dan kriteria keputusan model.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda menentukan bahwa sebuah model 'berguna' bagi bisnis?"
  - *Jawaban Kandidat*: "Berdasarkan pra-registrasi `config/analysis_plan.yaml`, model dinyatakan berguna hanya jika batas bawah 95% CI PR-AUC melampaui base rate prevalensi dan melampaui baseline heuristik serta logistik ter-regularisasi."

---

### [UK-03] Menelaah Data (J.62DMI00.005.1)
- **Perintah Demonstrasi**:
  ```bash
  python -c "from csip.data.loader import DataLoader; dl = DataLoader(); raw = dl.load_raw_data(); print(list(raw.keys()))"
  ```
- **Keluaran yang Diharapkan**:
  Daftar 9 tabel relasional e-commerce (orders, items, payments, reviews, customers, sellers, products, geolocation).
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda memverifikasi relasi antar-tabel dan granularitas entitas?"
  - *Jawaban Kandidat*: "Grain entitas utama adalah `order_id`. Penggabungan dilakukan dari item dan pembayaran yang diagregasikan ke level order sebelum digabungkan dengan ulasan pelanggan untuk mencegah duplikasi baris."

---

### [UK-04] Memvalidasi Data (J.62DMI00.006.1)
- **Perintah Demonstrasi**:
  ```bash
  python -m pytest tests/test_data_validation.py -v
  ```
- **Keluaran yang Diharapkan**:
  Semua tes validasi schema, missing values, dan temporal logic lolos (`PASSED`).
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda menangani 646 ulasan yang hilang pada pesanan terkirim?"
  - *Jawaban Kandidat*: "Kandidat menghitung batas seleksi Manski (*Manski selection bounds*). Rentang prevalensi negatif berada pada [11.44%, 12.10%] (selisih <= 0.59%), membuktikan bahwa seleksi non-respons ulasan tidak membiaskan temuan kepuasan."

---

### [UK-05] Menentukan Objek Data (J.62DMI00.007.1)
- **Perintah Demonstrasi**:
  ```bash
  python -c "import pandas as pd; df = pd.read_parquet('data/processed/order_level.parquet'); print('Delivered status count:', (df['order_status'] == 'delivered').sum())"
  ```
- **Keluaran yang Diharapkan**:
  96.478 pesanan delivered terseleksi sebagai objek analisis utama.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Mengapa pesanan yang dibatalkan (canceled/unavailable) tidak dimasukkan dalam evaluasi risiko ulasan?"
  - *Jawaban Kandidat*: "Berdasarkan studi kelayakan `reports/methodology/CHECKOUT_RISK_FEASIBILITY.md`, 99.0% pesanan unavailable tidak memiliki catatan item/produk dalam data Olist, sehingga pemodelan berbasis produk tidak layak secara data (*data-infeasible*)."

---

### [UK-06] Membersihkan Data (J.62DMI00.008.1)
- **Perintah Demonstrasi**:
  ```bash
  python -m pytest tests/test_cleaner.py -v
  ```
- **Keluaran yang Diharapkan**:
  Pembersihan data bebas kebocoran, deduplikasi geolokasi, dan imputasi median fitted strictly on train.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda menjamin tidak ada data leakage dalam pembersihan data?"
  - *Jawaban Kandidat*: "Kami menerapkan prinsip *Split-Before-Transform*. Semua parameter imputasi dan penskalaan di-fit hanya pada data training, kemudian ditransformasikan ke validation/test tanpa menghitung ulang statistik dari data evaluasi."

---

### [UK-07] Mengonstruksi Data (J.62DMI00.009.1)
- **Perintah Demonstrasi**:
  ```bash
  python -m pytest tests/test_features.py -v
  ```
- **Keluaran yang Diharapkan**:
  Interaksi fitur rasio ongkir (`freight_ratio`), keterlambatan interaksi (`delay_x_freight_ratio`), dan target encoding Bayesian per fold tervalidasi.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda melakukan target encoding untuk fitur kategorikal tanpa bocor ke masa depan?"
  - *Jawaban Kandidat*: "Melalui `CategoricalFoldEncoder` di `csip.features.builder`, target encoding dihitung strictly pada training fold dengan Bayesian smoothing. Kategori yang belum pernah muncul di training dipetakan ke *global training mean*."

---

### [UK-08] Membangun Skenario Model (J.62DMI00.010.1)
- **Perintah Demonstrasi**:
  ```bash
  python -m pytest tests/test_temporal_cv_and_survival.py -k "test_cv_folds_embargo" -v
  ```
- **Keluaran yang Diharapkan**:
  4 fold temporal expanding-window dengan embargo >= 90 hari tervalidasi.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Mengapa cross-validation acak (K-Fold acak) tidak valid untuk data transaksi e-commerce?"
  - *Jawaban Kandidat*: "K-Fold acak menyebabkan kebocoran temporal (*look-ahead bias*), di mana transaksi masa depan digunakan untuk memprediksi masa lalu. CSIP menggunakan Rolling-Origin CV dengan embargo 90 hari sesuai siklus pemenuhan label ulasan dan retensi."

---

### [UK-09] Membangun Model (J.62DMI00.011.1)
- **Perintah Demonstrasi**:
  ```bash
  python scripts/predict_batch.py --model-path artifacts/models/best_delivery_delay_lightgbm.joblib --input-csv data/sample_input.csv --output-csv data/sample_output.csv
  ```
- **Keluaran yang Diharapkan**:
  Prediksi batch berhasil dieksekusi dengan schema and range contract check, menghasilkan skor dan label audit.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Bagaimana Anda memastikan model yang belum matang tidak digunakan untuk inferensi operasional?"
  - *Jawaban Kandidat*: "`predict_batch.py` membaca metadata sidecar model dan secara otomatis melempar `ValueError` serta memblokir eksekusi jika status kematangan model bertuliskan `RESEARCH_ONLY`."

---

### [UK-10] Mengevaluasi Hasil Pemodelan (J.62DMI00.012.1)
- **Perintah Demonstrasi**:
  ```bash
  cat reports/evaluation/TEMPORAL_CV_REPORT.md
  ```
- **Keluaran yang Diharapkan**:
  Metrik per fold temporal, 95% Confidence Interval berbasis Moving-Block Bootstrap, Brier Skill Score, dan Decision Curve Analysis.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Mengapa Anda menggunakan PR-AUC bukan ROC-AUC sebagai metrik utama?"
  - *Jawaban Kandidat*: "Target ulasan negatif mengalami ketidakseimbangan kelas (*class imbalance* ~10-12%). ROC-AUC dapat tampak optimis semu karena dominasi kelas mayoritas negatif sejati, sedangkan PR-AUC mengevaluasi secara ketat presisi pada kelas minoritas positif."

---

### [UK-11] Melakukan Proses Review Pemodelan (J.62DMI00.013.1)
- **Perintah Demonstrasi**:
  ```bash
  python -m pytest tests/test_statistical_rigor.py -v
  ```
- **Keluaran yang Diharapkan**:
  Koreksi multiple testing Benjamini-Hochberg FDR dan stabilitas klaster bootstrap ARI/Jaccard (k=3..5) lolos pengujian.
- **Tanya Jawab Kritis**:
  - *Asesor*: "Apakah penurunan kepuasan akibat keterlambatan merupakan hubungan kausal murni?"
  - *Jawaban Kandidat*: "Data Olist adalah data observasional tanpa randomisasi perlakuan A/B testing. Oleh karena itu, seluruh klaim dibatasi pada Level L2 (Asosiasional terkontrol pembaur), bukan kausalitas deterministik."

---

## 3. Checklist Kesiapan Uji Portofolio
1. Seluruh 210+ tes unit dan integrasi lolos hijau (`python -m pytest`).
2. Log eksekusi nyata tersimpan di `reports/testing/pytest_actual.txt`.
3. Verifikasi gerbang rilis lolos penuh (`python tools/verify_release.py`).
4. Dashboard interaktif dapat dijalankan lokal (`streamlit run app/streamlit_app.py`).

