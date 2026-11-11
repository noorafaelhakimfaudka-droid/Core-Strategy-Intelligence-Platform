# CSIP SKKNI Structured Instruction Assessment Guide
## Panduan Asesmen Jalur Pelatihan / Uji Terstruktur (Uji Tertulis, Praktik Laboratorium & Wawancara Lisan)
### Skema Sertifikasi Okupasi: Ilmuwan Data (Data Scientist) — KKNI Jenjang 7
### LSP TRI (SKM/2905/LSP-TRI/VII/2025) | Standar: SKKNI No. 299 Tahun 2020

**Dokumen ID**: `CSIP-STRUCTURED-GUIDE-2026-V15`  
**Sasaran Peserta**: Peserta Pelatihan Vokasi, Mahasiswa/Lulusan Baru, Peserta Bootcamp Data Science  
**Metode Uji**: Tes Tertulis (Pilihan Ganda & Studi Kasus), Tugas Pemrograman Laboratorium, dan Uji Lisan  
**Ruang Lingkup**: 11 Unit Kompetensi, 27 Elemen, 63 KUK SKKNI 299/2020  

---

## 1. Kerangka Asesmen Jalur Terstruktur (Structured Assessment Framework)

Bagi peserta yang menempuh sertifikasi Ilmuwan Data melalui **Jalur Uji Terstruktur / Pelatihan**, penilaian kompetensi oleh Asesor LSP TRI dilaksanakan melalui tiga komponen terpadu:

1. **Uji Tertulis (Written Examination)**: Menguji penguasaan konsep teoritis, metodologis, dan normatif pada 11 Unit Kompetensi SKKNI 299/2020.
2. **Uji Praktik Demonstrasi Laboratorium (Practical Programming Tasks)**: Menguji keterampilan langsung dalam membersihkan data, merekayasa fitur anti-kebocoran, melatih model machine learning, dan mengkalibrasi probabilitas.
3. **Wawancara Lisan & Presentasi Studi Kasus (Oral Defense & Case Presentation)**: Menguji penalaran analitis, pertanggungjawaban etika data, dan artikulasi wawasan bisnis kepada pemangku kepentingan.

---

## 2. Bank Soal Uji Tertulis Pilihan Ganda (11 Unit SKKNI 299/2020)

### Unit 1: Menentukan Objektif Bisnis (`J.62DMI00.001.1`)
**Soal 1**: Sebuah platform e-commerce menghadapi masalah tingginya churn pelanggan akibat keterlambatan pengiriman. Langkah pertama yang paling tepat bagi seorang Data Scientist sesuai KUK 1.1 dan 1.3 adalah:
- A. Langsung mengunduh dataset transaksi dan melatih Deep Learning Transformer.
- B. Mengidentifikasi latar belakang masalah bisnis, merumuskan poin objektif bisnis yang terukur, dan menetapkan metrik kesuksesan bisnis seperti reduksi pesanan terlambat.
- C. Membeli server GPU baru tanpa melakukan perhitungan biaya komputasi.
- D. Menghapus pesanan yang terlambat dari dataset agar metrik perusahaan tampak bagus.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai SKKNI UK-01 Elemen E1 KUK 1.1 dan 1.3, formulasi masalah bisnis dan penetapan metrik kesuksesan terukur harus mendahului pemilihan algoritma teknis.

### Unit 2: Menentukan Tujuan Teknis Data Science (`J.62DMI00.002.1`)
**Soal 2**: Dalam memprediksi risiko keterlambatan pengiriman logistik dengan prevalensi kelas positif hanya 8.0%, metrik evaluasi teknis utama yang paling defensif digunakan adalah:
- A. Accuracy, karena mudah dipahami manajemen.
- B. Precision-Recall AUC (PR-AUC) dan Brier Score terkalibrasi, karena ROC-AUC dan Accuracy dapat memberikan ilusi performa semu pada data yang sangat tidak seimbang.
- C. Mean Squared Error pada label biner.
- D. R-squared.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai KUK 2.1, parameter kriteria kesuksesan harus sesuai tujuan teknis. Pada kelas minoritas langka (imbalance 8%), PR-AUC mengukur trade-off precision-recall secara riil tanpa terdistorsi kelas mayoritas.

### Unit 3: Menelaah Data (`J.62DMI00.005.1`)
**Soal 3**: Mengapa proses penelaahan data (data understanding) wajib mencakup analisis missing values, pengecekan konsistensi grain entitas, dan pengujian hipotesis bivariat sebelum pemodelan?
- A. Agar tampilan notebook menjadi lebih panjang dan berwarna.
- B. Untuk memahami karakteristik distribusi data, mendeteksi potensi anomali/drift, dan mencegah kesalahan pemilihan model yang tidak sesuai asumsi data.
- C. Karena algoritma machine learning tidak memerlukan data terstruktur.
- D. Hanya sebagai formalitas dokumentasi tanpa pengaruh ke akurasi.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-03 Elemen E2 KUK 2.1, penyajian statistik deskriptif dan analisis karakteristik data penting untuk memvalidasi kelayakan data sebelum tahap pemodelan.

### Unit 4: Memvalidasi Data (`J.62DMI00.006.1`)
**Soal 4**: Dalam dataset Olist, ditemukan beberapa pesanan memiliki `order_delivered_customer_date` yang mendahului `order_purchase_timestamp`. Tindakan validasi data yang benar sesuai KUK 1.2 adalah:
- A. Membiarkan anomali tersebut agar model belajar kejadian mustahil.
- B. Mengidentifikasi inkonsistensi temporal tersebut sebagai data cacat logika (*temporal inversion*) dan memfilternya dari data latih dengan catatan audit terdokumentasi.
- C. Mengubah nilai tanggal pembelian secara acak.
- D. Menggandakan baris tersebut 10 kali.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Validasi data mensyaratkan deteksi anomali integritas temporal yang melanggar hukum kausalitas sebelum data digunakan.

### Unit 5: Menentukan Objek Data (`J.62DMI00.007.1`)
**Soal 5**: Untuk membangun model prediksi keterlambatan pengiriman pada saat barang diserahkan ke kurir (*carrier dispatch*), subset data mana yang harus dipilih?
- A. Seluruh pesanan, termasuk pesanan yang dibatalkan (*canceled*) sebelum diproses merchant.
- B. Hanya pesanan dengan status `delivered` yang memiliki riwayat lengkap timestamp logistik, dengan mengecualikan fitur-fitur yang baru terjadi setelah pengiriman selesai.
- C. Hanya pesanan bernilai di atas $1.000.
- D. Data dari ulasan pelanggan saja.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-05 KUK 1.2, pemilihan objek data harus selaras dengan horizon keputusan operasional (*decision point*).

### Unit 6: Membersihkan Data (`J.62DMI00.008.1`)
**Soal 6**: Tabel geolokasi Olist memiliki 1.000.163 baris koordinat dengan duplikasi kode pos yang masif dan beberapa koordinat di luar wilayah Brasil. Strategi pembersihan data yang paling tepat adalah:
- A. Menghapus seluruh tabel geolokasi.
- B. Menghitung representasi median koordinat per kode pos unik dan membatasi koordinat pada batas geografis Brasil (-33.75 <= lat <= +5.27), mengurangi volume sebesar 98.1% tanpa kehilangan informasi unik.
- C. Melakukan imputasi nol untuk seluruh koordinat yang hilang.
- D. Menggunakan koordinat rata-rata global seluruh dunia.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-06 KUK 2.2, pembersihan data harus menangani duplikasi dan nilai ekstrem secara metodologis dengan reduksi redundansi yang efisien.

### Unit 7: Mengkonstruksi Data (`J.62DMI00.009.1`)
**Soal 7**: Apa yang dimaksud dengan prinsip *Split-Before-Transform* dalam rekayasa fitur data science?
- A. Membagi dataset menjadi Train dan Test setelah seluruh fitur distandarisasi dan diimputasi.
- B. Melakukan pemisahan Train, Validation, dan Test terlebih dahulu, kemudian seluruh parameter transformasi (misal mean, median, encoder) hanya di-fit pada data latih (Train) untuk mencegah kebocoran informasi ke data uji.
- C. Membagi data menjadi 100 bagian kecil secara acak.
- D. Melatih model tanpa menggunakan data latih.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-07 KUK 2.2, konstruksi data wajib menjaga integritas out-of-sample; fitting transformasi pada data uji adalah bentuk kebocoran data (*data leakage*).

### Unit 8: Membangun Skenario Model (`J.62DMI00.012.1`)
**Soal 8**: Mengapa skenario validasi berbasis *Out-of-Time Purged Temporal Split* jauh lebih unggul dibandingkan *Random K-Fold Cross-Validation* untuk data transaksi e-commerce?
- A. Karena K-Fold Cross Validation menggunakan terlalu banyak memori.
- B. Karena random split menyebabkan data dari masa depan bocor ke masa lalu (*temporal leakage*), menghasilkan estimasi performa model yang terlalu optimis dan tidak realistis saat di-deploy ke produksi.
- C. Karena K-Fold Cross Validation dilarang oleh Scikit-Learn.
- D. Karena temporal split tidak memerlukan data validasi.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Pada data deret waktu atau transaksi bisnis bertanggal, kejadian masa depan tidak boleh digunakan untuk memprediksi kejadian masa lalu. Purging buffer menjamin independensi antar cohort waktu.

### Unit 9: Membangun Model (`J.62DMI00.013.1`)
**Soal 9**: Mengapa seorang Data Scientist profesional wajib membangun *Baseline Ladder* (B0: Dummy, B1: Logistic Regression, B2: Gradient Boosting) sebelum melompat ke model kompleks?
- A. Untuk memperpanjang waktu proyek agar anggaran bertambah.
- B. Untuk membuktikan secara empiris bahwa kompleksitas model tambahan memberikan peningkatan performa nyata di atas baseline sederhana yang transparan.
- C. Karena model sederhana selalu memiliki akurasi 100%.
- D. Karena model neural network tidak dapat dilatih tanpa logistic regression.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-09 KUK 1.2 dan 2.2, pemilihan algoritma harus dapat dipertanggungjawabkan melalui pembuktian empiris bertingkat.

### Unit 10: Mengevaluasi Hasil Pemodelan (`J.62DMI00.014.1`)
**Soal 10**: Sebuah model klasifikasi memiliki ROC-AUC 0.85, namun probabilitas prediksinya terkonsentrasi pada rentang 0.01 hingga 0.05 padahal risiko keterlambatan riil mencapai 15%. Teknik apa yang harus diterapkan?
- A. Menolak model dan menghentikan proyek.
- B. Menerapkan kalibrasi probabilitas (*Platt Scaling* atau *Platt Scaling (Logistic Sigmoid on Log-Odds)*) pada validation set untuk meminimalkan *Expected Calibration Error* (ECE) dan Brier Score.
- C. Mengalikan seluruh probabilitas dengan 10 secara manual.
- D. Mengubah threshold klasifikasi menjadi 0.0001.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-10 KUK 1.2, evaluasi hasil pemodelan mencakup keandalan kalibrasi probabilitas agar probabilitas prediksi dapat digunakan secara aman dalam keputusan bisnis.

### Unit 11: Melakukan Proses Review Pemodelan (`J.62DMI00.015.1`)
**Soal 11**: Dalam tinjauan akhir pemodelan (Model Review), apa fungsi utama dari *Failure Register* dan pembatasan *Scientific Claim Hierarchy* (L0–L3)?
- A. Menyembunyikan kegagalan model dari pemangku kepentingan.
- B. Memastikan transparansi ilmiah, mencegah klaim kausalitas semu yang tidak berdasar, dan mendokumentasikan batasan operasional serta skenario kegagalan model secara jujur.
- C. Menjamin bahwa model tidak akan pernah salah dalam kondisi apa pun.
- D. Mempermudah penjualan model ke investor tanpa pengujian lebih lanjut.  
*Kunci Jawaban*: **B**  
*Justifikasi Ilmiah*: Sesuai UK-11 Elemen E1 dan E2, review pemodelan berfokus pada evaluasi keterbatasan, etika, dan batas kepatutan penggunaan hasil pemodelan.

---

## 3. Tugas Praktik Pemrograman Laboratorium Komputer

### Tugas Praktik 1: Validasi Integritas Data & Anti-Leakage (UK-04, UK-06)
Peserta diminta menuliskan fungsi Python untuk memfilter anomali temporal dan memverifikasi ketiadaan kebocoran target:
```python
def validate_logistics_records(df):
    """
    1. Pastikan order_purchase_timestamp <= order_delivered_carrier_date
    2. Pastikan freight_value >= 0 dan payment_value >= 0
    3. Kembalikan DataFrame yang bersih dan catat baris anomali yang dibuang
    """
    initial_len = len(df)
    valid_mask = (
        (df["order_delivered_carrier_date"] >= df["order_purchase_timestamp"]) &
        (df["freight_value"] >= 0) &
        (df["payment_value"] >= 0)
    )
    df_clean = df[valid_mask].copy()
    dropped = initial_len - len(df_clean)
    print(f"Validated records: {len(df_clean)} passed, {dropped} dropped ({dropped/initial_len*100:.2f}%)")
    return df_clean
```

### Tugas Praktik 2: Rekayasa Fitur Geospasial Vektorisasi (UK-07)
Peserta diminta menghitung jarak Haversine antar koordinat penjual dan pembeli secara vektorisasi tanpa loop:
```python
import numpy as np

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Menghitung jarak lingkaran besar (Great Circle) dalam kilometer."""
    R = 6371.0 # Radius bumi dalam km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat / 2.0) ** 2 +
         np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
         np.sin(dlon / 2.0) ** 2)
    c = 2.0 * np.arcsin(np.clip(np.sqrt(a), 0.0, 1.0))
    return R * c
```

### Tugas Praktik 3: Pelatihan & Kalibrasi Model LightGBM (UK-09, UK-10)
Peserta diminta melatih pipeline LightGBM dan mengkalibrasinya menggunakan Platt Scaling (Logistic Sigmoid on Log-Odds):
```python
import lightgbm as lgb
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

def train_calibrated_model(X_train, y_train, X_val, y_val):
    base_lgb = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        random_state=42,
        class_weight="balanced"
    )
    base_lgb.fit(X_train, y_train)
    
    # Kalibrasi probabilitas menggunakan Platt Scaling (Logistic Sigmoid on Log-Odds) pada validation set
    calibrated = CalibratedClassifierCV(estimator=base_lgb, method="isotonic", cv="prefit")
    calibrated.fit(X_val, y_val)
    
    val_probs = calibrated.predict_proba(X_val)[:, 1]
    brier = brier_score_loss(y_val, val_probs)
    print(f"Calibrated Model Trained. Validation Brier Score: {brier:.4f}")
    return calibrated
```

---

## 4. Panduan Presentasi & Uji Lisan Studi Kasus (Oral Case Defense)

Kandidat wajib menyiapkan paparan 10 slide terstruktur untuk sesi presentasi 15 menit di hadapan Asesor:

| Slide # | Judul Slide | Konten Kunci yang Wajib Dipaparkan |
| :---: | :--- | :--- |
| **1** | Judul Proyek & Identitas Kandidat | CSIP V15, Skema Data Scientist LSP TRI KKNI Level 7. |
| **2** | Latar Belakang & Masalah Bisnis | Keterlambatan pengiriman Olist (8%), dampak terhadap review & rating. |
| **3** | Tujuan Teknis & Formulasi Masalah | Supervised binary classification, kendala memori laptop 8GB RAM. |
| **4** | Pemahaman & Validasi Data | Audit 9 tabel Parquet, eliminasi temporal inversions, deduplikasi koordinat. |
| **5** | Rekayasa Fitur & Anti-Kebocoran | Vectorized Haversine, split April 2018 out-of-time, zero correlation check. |
| **6** | Piramida Pemodelan (Baseline Ladder) | Perbandingan B0 (Dummy) vs B1 (LogReg) vs B2 (LightGBM PR-AUC 0.3004). |
| **7** | Evaluasi & Kalibrasi Probabilitas | Penurunan ECE ke 0.0070, kurva Reliability Diagram, SHAP TreeExplainer. |
| **8** | Simulasi Kebijakan & Dampak Bisnis | Counterfactual simulation intervensi logistik, estimasi penyelamatan 1.200 order. |
| **9** | Failure Register & Etika Ilmiah | Keterbatasan model, batasan kausalitas (L1 vs L3), pelaporan temuan negatif. |
| **10** | Kesimpulan & Kesiapan Produksi | Dashboard Streamlit, 136+ unit test lulus, integritas SHA-256 terverifikasi. |

