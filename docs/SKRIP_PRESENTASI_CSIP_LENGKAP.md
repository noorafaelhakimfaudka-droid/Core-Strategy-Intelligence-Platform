# NASKAH PRESENTASI DATA SCIENCE & MACHINE LEARNING — CSIP
## Pembahasan Lengkap Perumusan Masalah, Pemodelan, Validasi Temporal, Evaluasi & Simulasi
### *(Fokus Murni Domain Data Science & Machine Learning: Masalah Nyata, Analogi Sederhana, & Penjelasan Istilah Teknis)*

> **Ruang Lingkup Naskah:**  
> - **Sistem:** Core Strategy & Intelligence Platform (**CSIP** — kerangka pemodelan perilaku, evaluasi statistik, dan simulasi berbasis data historis Olist Brasil).  
> - **Cakupan Materi:** Perumusan masalah (*estimand*, target, *grain*, pencegahan kebocoran waktu), rekayasa fitur, *temporal cross-validation*, perbandingan **6 keluarga algoritma** (baseline aturan, linier, klasik, ensemble pohon, *deep learning*, `K-Means`, `Kaplan-Meier`, hingga `VAR(1)`), serta **rangkaian evaluasi mendalam** (*PR-AUC*, *ROC-AUC*, regresi *MAE/RMSE/R²*, studi ablasi, kalibrasi *Platt Scaling*, *Brier Skill Score*, *Decision Curve Analysis*, *Top-K Lift*, *SHAP TreeExplainer*, evaluasi subkelompok *Slice Robustness*, batas non-respons *Manski*, uji hipotesis *FDR*, dan pemantauan *Concept Drift*).  
> - **Gaya Penyampaian:** Berangkat dari persoalan nyata transaksi, menerangkan setiap istilah teknis tepat di sebelahnya dengan analogi yang mudah dicerna, serta memaparkan keterbatasan dan temuan negatif secara terbuka.

---

## DAFTAR ISI NAVIGASI CEPAT

- **PANDUAN ALUR PRESENTASI DATA SCIENCE (SLIDE 01–69)**
- **BAGIAN 01 — PERUMUSAN MASALAH & ESTIMAND (`BABAK 1–2` · Slide 01–11)**
  - **BABAK 1:** Pembukaan, Alur Kerja 8 Tahap, Keterlambatan vs Harga & Empat Kesalahan Metodologi (Slide 01–06)
  - **BABAK 2:** Peta Estimand, Isolasi Populasi (`1.234` *unavailable* & `962 pre-repeaters`), dan Alur Pipeline (Slide 07–11)
- **BAGIAN 02 — DATA ENGINEERING & 41 FITUR (`BABAK 3–4` · Slide 12–19)**
  - **BABAK 3:** Profil 9 Tabel Olist, Kompresi Spasial Median, Anti-*Fan-Out*, dan Integritas `646 NaN` (Slide 12–16)
  - **BABAK 4:** Rekayasa 41 Fitur Fisik-Ekonomi, Pembatasan Fitur Menurut Tahap Waktu, *Point-in-Time As-Of*, & *Bayesian Encoding* (Slide 17–19)
- **BAGIAN 03 — VALIDASI TEMPORAL KRONOLOGIS (`BABAK 5` · Slide 20–24)**
  - **BABAK 5:** Alasan Menolak *Random Split*, *4-Fold Rolling-Origin CV*, Jeda *Embargo 90 Hari*, & *Moving-Block Bootstrap* (Slide 20–24)
- **BAGIAN 04 — ARSITEKTUR ENAM KELUARGA MODEL MACHINE LEARNING (`BABAK 6–8` · Slide 25–34)**
  - **BABAK 6:** Komparasi Model Klasik & Ensemble: `Majority/Heuristic` → `LogReg/Ridge` → `CART/KNN/GaussianNB` → `Random Forest` vs `LightGBM` (Slide 25–29)
  - **BABAK 7:** *Deep Learning* (`TabularEmbeddingMLP` & `TextBiLSTM` Portugis) (Slide 30–31)
  - **BABAK 8:** Pemodelan Tanpa Supervisi (`K-Means + PCA + ARI`), Ketahanan `Kaplan-Meier`, & Dinamika `VAR(1)` Ridge (Slide 32–34)
- **BAGIAN 05 — EVALUASI BERLAPIS & BATAS MODEL (`BABAK 9–12` · Slide 35–49)**
  - **BABAK 9:** Kelemahan *Accuracy* `90,37%`, Papan Peringkat `N=12.571`/`12.630`, Studi Ablasi Fitur, & Pergeseran Rezim `Fold 3` (Slide 35–40)
  - **BABAK 10:** Batas Sinyal Checkout Saat Bayar (`0,1335`), Penolakan `Repeat Purchase (0,5021)`, *Manski Bounds*, & Tiga Poros Evaluasi (Slide 41–44)
  - **BABAK 11:** Kalibrasi *Platt Scaling* (`Brier 0,0762`, `ECE 0,0070`, `BSS +0,1215`), *Decision Curve Analysis*, & *Top-K Lift* (`5,154×`) (Slide 45–46)
  - **BABAK 12:** Interpretasi *SHAP TreeExplainer* (Asosiasi Model vs Uji Kausal) & Evaluasi Subkelompok Wilayah/Ketepatan (*Slice Robustness*) (Slide 47–49)
- **BAGIAN 06 — STATISTIKA INFERENSIAL, KEPUTUSAN & SIMULASI (`BABAK 13–14` · Slide 50–57)**
  - **BABAK 13:** Enam Hipotesis Praregistrasi (+ *FDR*), Penolakan Rating -> Retensi, & *Confounder* Wilayah (Slide 50–52)
  - **BABAK 14:** *Cost-Sensitive Threshold* (`$45 vs $5` → `tau*=0,18`), Desain A/B `80/20`, & Simulasi Kontrafaktual `VAR(1)` (6 Skenario & Batas `OOD`) (Slide 53–57)
- **BAGIAN 07 — MONITORING DRIFT, GENERALISASI & REPRODUKSI (`BABAK 15–18` · Slide 58–66)**
  - **BABAK 15:** Pemantauan Pergeseran Data (`PSI`, `KS`, `Wasserstein-1`, `JSD`) & Kriteria Seleksi *Champion–Challenger* (Slide 58–60)
  - **BABAK 16:** Generalisasi Pipeline ML Anti-Kebocoran & Empat Lensa Diagnostik Interaktif (Slide 61)
  - **BABAK 17:** Reproduksi Eksperimen 14 Notebooks (`01–14`), Tujuh Model Cards, & Verifikasi Invarian Statistik (Slide 62–64)
  - **BABAK 18:** Agenda Riset Lanjutan & Analisis Bias Induktif Lintas Keluarga Algoritma (Slide 65–66)
- **BAGIAN 08 — RINGKASAN CAPAIAN, KONTROL VALIDITAS & PENUTUP (`BABAK 19` · Slide 67–69)**
  - **BABAK 19:** Rekapitulasi Capaian Empiris, Enam Kontrol Validitas Metodologis, & Penutup (Slide 67–69)
- **LAMPIRAN MATERI: RINGKASAN METRIK & KAMUS ISTILAH MACHINE LEARNING**

---

# PANDUAN PENYAMPAIAN MATERI DATA SCIENCE

## 1. Struktur Berpikir di Setiap Bagian

Setiap bagian dalam presentasi ini mengikuti tiga alur yang saling terhubung:
1. **Konteks Data Nyata:** Memulai dari persoalan empiris pada transaksi (*mengapa keterlambatan melebihi tiga hari menjatuhkan ulasan*, *mengapa 90,37% kelas puas membiasakan akurasi*, *mengapa perlakuan merata memboroskan biaya*).
2. **Mekanisme Algoritma + Penjelasan Sederhana:** Menyebutkan metode statistik atau *Machine Learning* secara tepat (`Rolling-Origin CV`, `Platt Scaling`, `Brier Skill Score`, `Decision Curve Analysis`, `LightGBM`, `TextBiLSTM`), diikuti langsung oleh arti praktis serta analoginya.
3. **Bukti Empiris & Batas Validitas:** Menunjukkan metrik uji pada partisi terkunci sekaligus mencatat kondisi di mana model bekerja terbatas atau tidak layak dipakai.

## 2. Peta Slide Presentasi (69 Slide Widescreen 16:9)

| Rentang Slide | Babak | Fokus Utama Materi | Konsep Kunci & Analogi |
| :---: | :---: | :--- | :--- |
| **01–06** | Babak 1 | Pembukaan, Alur 8 Tahap, *Loss Aversion*, 4 Kesalahan Kontrol Bias | Penurunan tajam pasca-estimasi (`r=-0,334` vs `+0,015`), *Lookahead*, *Fan-Out* |
| **07–11** | Babak 2 | Kontrak Estimand Pemodelan, Eksklusi Populasi, Pipeline | `1.234 unavailable` (99% kosong), `962 pre-repeaters`, *Right-Censoring* 90 hari |
| **12–19** | Babak 3–4 | 9 Tabel, Median GPS `-98,1%`, Grain `order_id`, 41 Fitur | Antiledakan baris struk kasir, tahap saat bayar / serah kurir / pasca-tiba, *Bayesian Encoding* ($\alpha=10$) |
| **20–24** | Babak 5 | Larangan Acak, 4-Fold Temporal CV, Embargo & Kalender | Jeda 90 hari (*delayed ground truth*), *Moving-Block Bootstrap* (`block=5, 1000×`) |
| **25–34** | Babak 6–8 | Baseline hingga Ensemble, `MLP`, `TextBiLSTM`, `K-Means`, `KM`, `VAR(1)` | Bagging vs Boosting, `ARI 0,9832`, Segmen 2 (`31,20%`), Spectral `0,8412` |
| **35–40** | Babak 9 | Bias *Accuracy*, Leaderboard `N=12.571`, Regresi Delay, Ablasi, `Fold 3` | *PR-AUC* vs *Accuracy*, Ridge vs LGBM (`4,75` vs `4,83` hr), lonjakan `19,98%` |
| **41–44** | Babak 10 | Model Saat Bayar, Penolakan Retensi, *Manski Bounds*, 3 Poros Uji | Saat Bayar `0,1335` (Indikator Awal), `Repeat 0,5021` (Ditolak Riset), Manski `<=0,59%` |
| **45–49** | Babak 11–12 | *Platt Scaling*, *DCA Net Benefit*, *Top-K Lift*, *SHAP*, & *Slices* | Kalibrasi cuaca (`ECE 0,0070`), `5,154× Lift`, `is_late` SHAP=0, `On-Time 0,6522` |
| **50–57** | Babak 13–14 | 6 Hipotesis (*FDR*), Matriks Biaya `$45 vs $5`, A/B `80/20`, 6 Skenario & `OOD` | Penolakan Rating -> Retensi, *Confounder* es krim `-47,3%`, `tau*=0,18`, hemat `50,3%`, `Z=3,68` |
| **58–66** | Babak 15–18 | 4 Metrik *Drift*, Pipeline Generik, 14 Notebooks, Bias Induktif | `PSI/KS/W1/JSD`, Invarian Anti-Leakage, Kesesuaian Model vs Data |
| **67–69** | Babak 19 | Ringkasan Capaian Empiris, Enam Kontrol Validitas, & Penutup | `PR-AUC`, `ECE`, 6 Kontrol Validitas, Kesimpulan Jujur |

# BAGIAN 01 — PERUMUSAN MASALAH & ESTIMAND (SLIDE 01–11)

## BABAK 1: HOOK PAKET HARI JUMAT & MENGAPA MODEL ML SERING MENIPU DI PRODUKSI
*(Alokasi waktu: 3–4 menit · Slide 01–06)*

**[SLIDE 01–02 | VISUAL LAYAR]**  
*Latar gelap minimalis:*  
**CSIP — Behavioral Machine Learning & Model Evaluation Architecture**  
*Membangun Model yang Jujur di Dunia Nyata, Tanpa Kebocoran Waktu, Tanpa Ilusi Skor.*

**[NADA & GESTUR]**  
*Berdiri tenang. Pandangi audiens sejenak sebelum kalimat pertama keluar.*

**[JEDA 3 DETIK]**

**[KALIMAT YANG DIUCAPKAN]:**  
"Selamat pagi atau selamat siang. Rekan-rekan sekalian.

Izinkan saya membuka sesi teknis hari ini bukan dengan rumus, melainkan dengan sebuah fakta psikologi manusia yang tercatat di hampir seratus ribu pesanan belanja online."

**[SLIDE 03–04 | VISUAL LAYAR]**  
*Dua angka besar kontras:*  
Tiba Tepat Waktu: **`4,25 Bintang`** vs Paket Terlambat: **`2,26 Bintang`** *(melewati > 3 hari jatuh ke `1,6 bintang`)*  
*Catatan:* `99.441 transaksi Olist Brasil · 8,0% terlambat · Korelasi keterlambatan terhadap skor ulasan r = -0,334 (sedangkan harga barang r = +0,015!)`

**[KALIMAT YANG DIUCAPKAN]:**  
"Lihat dua angka ini. Di atas **99.441 transaksi e-commerce nyata** pada dataset publik Olist Brasil, ketika kurir mengantar paket sesuai janji, pembeli memberikan rata-rata **4,25 bintang**. Bahkan jika kurir datang kelewat rajin—tiba seminggu lebih awal—ratingnya tetap di sekitar **4,3 bintang**.

Namun begitu paket meleset melewati janji pengiriman—terutama setelah **melewati batas tiga hari keterlambatan**—kepuasan pembeli runtuh seketika ke **2,26 bintang**, bahkan menyentuh **1,6 bintang**. Di buku teks ekonomi perilaku, fenomena patah curam ini disebut **Asimetri Kehilangan (*Loss Aversion*)**, yaitu sifat manusia yang jauh lebih tersakiti oleh janji yang diingkari dibanding merasa berterima kasih atas datang lebih awal.

Lebih menarik lagi bagi seorang *Data Scientist*: korelasi linier antara **harga barang** (`total_item_price`) dan skor bintang ternyata mendekati nol (**$r = +0,015$**), sedangkan **lama keterlambatan (`delivery_delay_days`)** mencatat korelasi terkuat (**$r = -0,334$**)! Pembeli di Brasil tidak marah karena harga barangnya mahal; mereka marah karena ketepatan waktunya dilanggar!"

**[SLIDE 05–06 | VISUAL LAYAR]**  
*Empat Dosa Besar Pemodelan ML yang Mematikan Model di Lapangan:*  
1. **Kebocoran Masa Depan (*Lookahead Leakage*):** Melatih model prediksi kasir memakai fitur yang baru ada setelah kurir sampai.  
2. **Kebocoran Gabung Tabel (*Cartesian Fan-Out*):** Satu order terpecah jadi baris ganda antara data latih dan data uji.  
3. **Sihir Angka *Accuracy* 90%:** Pada data dengan hanya `9,63%` keluhan, menebak semua puas sudah langsung benar `90,37%`!  
4. **Skor Mentah Terlalu Panik (*Uncalibrated Overconfidence*) & Kausal Palsu:** Menganggap bobot pohon atau *SHAP* otomatis membuktikan efek intervensi sebab-akibat.

**[KALIMAT YANG DIUCAPKAN]:**  
"Di sinilah masalah klasik dunia *Machine Learning*: hampir setiap tim bisa memanggil `model.fit()` lalu mendapat angka mentereng di *notebook*. Tetapi begitu model ditaruh di dunia nyata, ia langsung melemah karena **empat cacat metodologi**: model diam-diam mengintip data masa depan (*Lookahead Leakage*), baris data meledak kembar saat menggabungkan banyak tabel (*Cartesian Fan-Out*), kita terkecoh oleh metrik **Accuracy 90%** saat mayoritas kelas memang puas, atau probabilitas mentah model terlalu panik sehingga memicu ratusan alarm palsu.

Hari ini, saya ingin membedah tuntas **bagaimana CSIP merancang, melatih, mengadu, mengkalibrasi, menjelaskan, dan—yang paling penting—menguji secara jujur seluruh keluarga model Machine Learning-nya**."

---

## BABAK 2: PETA MASALAH DATA SCIENCE DI CSIP (*ESTIMAND*, POPULASI, TARGET, & IMBALANCE*)
*(Alokasi waktu: 3,5 menit · Slide 07–11)*

**[SLIDE 07–08 | VISUAL LAYAR]**  
*Dari Pertanyaan Bisnis Menjadi Formulasi Matematis ML (spesifikasi eksperimen praregistrasi):*  
Sebelum menulis satu baris kode `fit()`, setiap model wajib mendefinisikan **Estimand** *(besaran target pasti yang ingin ditaksir di populasi mana dan pada detik kapan)*:

| ID Model | Jenis Tugas ML *(Bahasa Sederhana)* | Variabel Target `y` | Detik Prediksi Sah (*Prediction Time*) | Populasi Uji | Metrik Primer & Aturan Sukses |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Regresi Delay** | **Regresi Kontinu** *(menebak selisih angka hari)* | `delivery_delay_days` (`actual - estimated`) | **Saat Disposisi Kurir** | Semua order terkirim | **MAE** *(harus turun $\ge 10\%$ vs median)* |
| **Risiko Ulasan (Pasca-Kirim)** | **Klasifikasi Biner Timpang** *(menebak ya/tidak keluhan)* | `negative_review_flag` (`1` jika bintang `1–2`, `0` jika `3–5`, `NaN` jika kosong) | **Tahap Pasca-Pengiriman** *(pasca-tiba — diagnostik)* | Order `delivered` dgn ulasan | **PR-AUC** (`> base rate` & `LogReg`) + *Brier* |
| **Peringatan Dini Checkout** | **Klasifikasi Biner Dini** *(peringatan awal di kasir)* | `negative_review_flag` | **Tahap Checkout** *(detik klik bayar)* | Order `delivered` dgn ulasan | **PR-AUC** (hanya indikator awal jika sinyal tipis) |
| **Retensi 90 Hari & Survival** | **Klasifikasi Retensi 90 Hari & *Survival*** *(tebak beli lagi & daya tahan waktu)* | `repeat_purchase_flag` / `repeat_purchase_post_delivery` | **Tahap Checkout / Pasca-Pengiriman** | Pembeli pertama *(buang `962` pre-repeaters & buffer 90h)* | **PR-AUC & ROC-AUC** (`Tolak` jika `95% CI` menyentuh `0,50`!) |
| **Segmentasi K-Means** | **Unsupervised Clustering** *(kelompok tanpa label)* | Segmen `Cluster 0..K` | Eksplorasi perilaku | `N = 96.470` transaksi bersih | **Silhouette** $\ge 0,35$ & stabilitas **ARI** $\ge 0,80$ |
| **NLP Teks Ulasan** | **Deep Sequence NLP** *(baca teks kalimat)* | Sentimen komentar `review_score <= 2` | **Pasca-Ulasan** *(saat teks masuk)* | Ulasan dengan komentar teks | **Macro-F1** *(mengatasi timpang kelas)* |
| **Dinamika Sistem VAR(1)** | **State-Space Time Series `VAR(1)`** *(prediksi berantai mingguan)* | Vektor 4 negara bagian `[Volume, Delay, Freight, NegRate]` | Mingguan `t -> t+1` | Panel `87` minggu | **WAPE, Spectral Radius `< 1,0`, Synthetic Recovery** |

**[KALIMAT YANG DIUCAPKAN]:**  
"Sebagai *Principal Data Scientist*, kita tahu bahwa **80% kegagalan model lahir sebelum `train_test_split` dijalankan—yakni karena tim lupa mendefinisikan `Estimand`**, artinya pernyataan tegas mengenai *apa persisnya yang mau ditebak, pada populasi mana, menggunakan informasi pada detik waktu ke berapa, dan kapan model dianggap gagal!*

Analogi mudahnya seperti seorang dokter sebelum memberi resep: kita tidak boleh asal tes darah tanpa tahu apakah tes ini untuk mendeteksi gejala awal sebelum sakit (saat bayar), menaksir berapa hari pasien harus dirawat (saat serah kurir), atau mengaudit keluhan setelah pasien keluar rumah sakit (pasca-pengiriman).

Pada tahap praregistrasi, seluruh desain pemodelan ditetapkan dan dikunci secara eksplisit sejak awal sebelum melatih satu model pun—persis seperti pra-registrasi uji klinis medis agar tidak ada yang mengubah definisi target di tengah jalan supaya skor terlihat cantik!"

**[SLIDE 09–10 | VISUAL LAYAR]**  
*Dua Jebakan Populasi yang Diam-Diam Merusak Target Label:*  
1. **Pesanan Tidak Tersedia (`1.234 unavailable/canceled`):** Tingkat komplain ~88%, namun **99,0% pesanan `unavailable` tidak punya baris item produk** di `order_items` → tidak sah dipaksa masuk model berbasis fitur produk!  
2. **Pembeli Ulang Sebelum Paket Pertama Tiba (`962 Pre-Delivery Repeaters`):** Bayangkan melatih model *'Apakah setelah menerima paket ke-1 pelanggan puas lalu beli paket ke-2?'*, padahal ada `962` pelanggan yang sudah memesan paket ke-2 *sebelum* paket ke-1 sempat datang! Kalau tidak dikeluarkan dari estimand Retensi 90 Hari, targetnya terkontaminasi oleh pengalaman yang belum terjadi!

**[KALIMAT YANG DIUCAPKAN]:**  
"Dua detail pembersihan populasi ini sering terlewatkan oleh praktisi, padahal menentukan sah atau tidaknya label target `y` kita:  
Pertama, di studi kelayakan populasi transaksi non-delivered, kami menemukan bahwa `99,0%` pesanan berstatus *unavailable* tidak memiliki catatan produk maupun harga di database—jadi model produk hanya sah diuji pada pesanan dengan data fisik lengkap, sementara tingkat pembatalan dilaporkan terpisah.  
Kedua, ketika membangun model retensi pasca-pengiriman (`repeat_purchase_post_delivery`), kami menemukan **`962` pelanggan** yang ternyata sudah menekan tombol beli order kedua *bahkan sebelum* kurir mengantar order pertamanya! Secara logika sebab-waktu, pengalaman kurir pada order pertama mustahil memengaruhi order kedua yang terjadi lebih dulu. Maka di dalam spesifikasi praregistrasi, ke-962 pelanggan itu dikeluarkan secara eksplisit dari populasi estimand Retensi 90 Hari."

**[SLIDE 11 | VISUAL LAYAR]**  
*Alur Pipeline End-to-End Pemodelan & Evaluasi (`src/csip/`):*  
`Raw 9 CSV (1,5M+ baris)` → `Cleaner & Grain order_id` → `Split Kronologis + Embargo 90 Hari` → `41 Fitur & Bayesian Target Encoding (Strict Fit on Train)` → `Baseline Ladder hingga Deep Learning + K-Means + Survival + VAR(1)` → `Locked Test Eval + Platt Scaling + DCA + SHAP + Slice Robustness` → `Concept Drift & Lifecycle Registry`.

**[KALIMAT YANG DIUCAPKAN]:**  
"Dengan definisi estimand dan populasi yang jernih tadi, seluruh pipa eksperimen kita di `src/csip/` berdiri di atas satu garis lurus yang diaudit otomatis dari ujung data mentah hingga pemantauan pasca-tayang. Sekarang, mari kita bedah langkah pertamanya: **bagaimana data mentah dirapikan dan diubah menjadi fitur tanpa membocorkan satu detik pun informasi masa depan**."


---

# BAGIAN 02 — DATA ENGINEERING & 41 FITUR (SLIDE 12–19)

## BABAK 3: MENJINAKKAN 9 TABEL OLIST, ANALOGI NOTA KASIR (*CARTESIAN FAN-OUT*), & INTEGRITAS LABEL TARGET
*(Alokasi waktu: 4 menit · Slide 12–16)*

**[SLIDE 12–13 | VISUAL LAYAR]**  
*Inventaris Skema 9 Tabel Olist & Audit Ekor Panjang (profil 9 tabel awal):*  
`orders (99.441)` · `order_items (112.650)` · `order_payments (103.886)` · `order_reviews (99.224 — 1.603 PK duplikat)` · `customers (99.441)` · `sellers (3.095)` · `products (32.951)` · `geolocation (1.000.163 — 999.120 kode pos duplikat)` · `category_translation (71)` · **0 *orphan records*** pada *Foreign Key*.

**[KALIMAT YANG DIUCAPKAN]:**  
"Dalam pelatihan model *Machine Learning*, kualitas bahan mentah menentukan batas atas kecerdasan algoritma apa pun. Pada tahap profiling data: bahan mentah kita datang dari **9 tabel relasional berbeda** dengan total lebih dari 1,5 juta baris.  

Sebelum melatih satu model pun, di `OlistDataCleaner` kami menjalankan audit relasional dan menemukan integritas kunci relasional sempurna (*zero orphan records*—tidak ada satu pun barang pesanan tanpa induk transaksi), **tetapi distribusinya sangat miring berekor panjang (*Heavy-Tailed Skewness*)**: median harga barang memang cuma `R$ 74,99`, namun ada transaksi sampai `R$ 6.735`! Begitu pula kolom koordinat GPS punya **1.000.163 baris** di mana `999.120` di antaranya mengulang kode pos yang sama, dan beberapa koordinat tercatat nyasar di luar daratan Brasil akibat salah ketik petugas kurir.

Analogi sederhananya: kalau satu kode pos punya 50 titik GPS dan satu titik nyasar di tengah Samudra Atlantik, mengambil **rata-rata (*mean*)** akan menyeret pusat pengiriman ke laut! Karena itu kami mengambil **nilai tengah (*median*)** per prefiks kode pos sehingga `1.000.163` titik menyusut bersih menjadi **`19.015` koordinat daratan (`-98,1%`)**."

**[SLIDE 14–15 | VISUAL LAYAR]**  
*Mencegah **Cartesian Fan-Out** (Ledakan Penggandaan Baris) & Menjaga **Grain** (Satuan Dasar 1 Baris = `1 order_id`):*  
- **Masalah Nyata (*Analogi Nota Kasir*):** 1 pesanan berisi `3 item barang` × `2 metode bayar` × `2 ulasan` → jika di-`JOIN` mentah menghasilkan **`12` baris kembar!** Akibatnya di ML: bobot sampel terdistorsi dan salinan pesanan yang sama bisa masuk ke data *train* sekaligus *test*!  
- **Solusi di `OlistDataCleaner`:** Agregasi `order_items` & `order_payments` ke level `order_id` sebelum digabung · Deduplikasi `814` ulasan ganda mempertahankan survei pertama · Kompresi GPS **`1.000.163 → 19.015`** prefiks median Brasil (`-98,1%`) · Eliminasi **23 anomali kronologis** (`order_delivered_customer_date < order_delivered_carrier_date`).  
- **Jebakan Kunci Manusia:** Memisahkan **`customer_id`** *(kunci tiket sesi per order — jumlahnya 99.441)* dari **`customer_unique_id`** *(identitas permanen manusia pembeli untuk model retensi kohor & anti-entity-leakage)*.

**[KALIMAT YANG DIUCAPKAN]:**  
"Begitu 9 tabel itu mau digabung menjadi satu tabel latih ML, muncullah **dua ranjau paling mematikan di Data Engineering**:

**Ranjau pertama adalah *Cartesian Fan-Out***—yaitu meledaknya jumlah baris kembar akibat menggabungkan beberapa tabel relasional 'satu-ke-banyak' secara langsung. Analogi kasirnya sederhana: satu pelanggan membeli **3 barang** lalu membayar pakai campuran **2 kartu**, kemudian menulis **2 kali** revisi ulasan. Kalau semua tabel di-`JOIN` mentah tanpa diringkas lebih dulu ke satu struk, satu transaksi mendadak tercetak **12 baris kembar!** Bagi model ML, itu bencana ganda: baris transaksi yang sama mendapat bobot suara dua belas kali lebih besar saat latihan, dan pecahannya bisa nyasar masuk ke ruang *training* sekaligus *validation*.  
Karena itu, kami kunci **`Grain`**—artinya satuan dasar mutlak yang diwakili satu baris tabel, yaitu **tepat 1 baris = 1 `order_id` unik**. Item dan pembayaran diringkas lebih dulu per pesanan; **814 ulasan ganda** dideduplikasi mempertahankan waktu pertama; dan **23 anomali waktu mustahil** (paket tercatat diterima pembeli *sebelum* diserahkan ke kurir) langsung disaring keluar.

**Ranjau kedua adalah jebakan nama kolom `customer_id`.** Di Olist, meski bernama `customer_id`, ternyata kolom itu adalah tiket sesi pesanan sekali pakai (jumlah uniknya tepat `99.441`, sama persis dengan jumlah order!). Identitas permanen manusia aslinya ada di **`customer_unique_id`**. Membedakan dua kunci ini mencegah seorang pelanggan muncul di kubu *train* sekaligus *test* saat memodelkan retensi!"

**[SLIDE 16 | VISUAL LAYAR]**  
*Integritas Target & Corong Populasi (dataset bersih level order = `96.470` baris bersih):*  
`99.441 Raw` → pisahkan `2.963` non-delivered (`1.234 unavailable/canceled`) → `96.478` delivered → **`96.470`** dataset fitur bersih:  
- **`95.824`** memiliki `review_score` (`has_observed_review = 1`): bintang `1–2` dipetakan jadi **`1.0` (`negative_review_flag`)**, bintang `3–5` jadi **`0.0`**.  
- **`646 (0,67%)`** tidak mengisi ulasan → **tetap `NaN` (kosong jujur!)**, diverifikasi ketat oleh unit test `test_review_target_exact_mapping_values()`.

**[KALIMAT YANG DIUCAPKAN]:**  
"**Ranjau ketiga adalah pemalsuan label target (`y`).** Dari `96.470` transaksi bersih yang benar-benar terkirim, ada **`646` pembeli (0,67%)** yang tidak mengisi rating. Banyak praktisi mengisi rating kosong dengan nilai tengah bintang 3 'netral'. Kami melarang praktik itu—bayangkan mengisi sendiri survei pasien yang pulang tanpa menjawab! Ke-646 baris tersebut dipertahankan `NaN` untuk pemodelan supervisi ulasan, lalu potensi bias seleksi diam mereka kami audit tersendiri memakai batas *Manski*."

---

## BABAK 4: REKAYASA 41 FITUR, PENYEKATAN TAHAP WAKTU, *POINT-IN-TIME AS-OF*, & *BAYESIAN TARGET ENCODING*
*(Alokasi waktu: 4,5 menit · Slide 17–19)*

**[SLIDE 17 | VISUAL LAYAR]**  
*Anatomi Rekayasa Fitur Domain (tahap rekayasa fitur — Total `41` Atribut Analitik) + Bukti Stabilitas `PSI` (evaluasi rekayasa fitur):*  
1. **Fitur Ekonomi & Beban Biaya:** `total_item_price`, `total_freight`, `total_order_value`, **`freight_ratio`** ($\frac{\text{total\_freight}}{\text{total\_item\_price} + \text{total\_freight}}$ — seberapa mencekik ongkir vs harga barang!), `item_count`, `payment_installments_max`. *(Stabilitas temporal `freight_ratio`: **`PSI = 0,021`**, jauh di bawah batas `0,10`!)*  
2. **Fitur Fisika Spasial & Waktu:** **`seller_buyer_distance_km`** (rumus **Haversine** $2R \arcsin\sqrt{\dots}$ — penggaris garis lengkung bumi antar-koordinat penjual & pembeli, **`PSI = 0,018`**), `distance_x_weight`, `estimated_lead_time_days`, `approval_lag_hours`.  
3. **Fitur Pengalaman Pengiriman & Interaksi Non-Linear *(Pasca-Pengiriman)*:** `delivery_lead_time_days`, **`delivery_delay_days`** (`delivered - estimated`, **`PSI = 0,048`**), `is_late` ($\mathbb{I}(\text{delay} > 0)$), **`delay_x_freight_ratio`** (efek kemarahan ganda: ongkir mahal *sekaligus* terlambat!), `high_value_late_flag` ($\mathbb{I}(\text{price} > 150 \land \text{is\_late} = 1)$).  
4. **Fitur Riwayat Pelanggan Tanpa Bocor (**Point-in-Time As-Of**):** `prior_order_count` ($\sum_{t < t_{\text{order}}}$), `prior_avg_order_value`, `prior_avg_review_score`, `days_since_prev_order`.

**[KALIMAT YANG DIUCAPKAN]:**  
"Dalam praktik *Machine Learning* di industri, algoritma hebat tetap tumpul jika hanya disuapi kolom mentah seperti harga `total_item_price` atau kode pos `zip_code`. Tugas utama seorang *Data Scientist* pada tahap rekayasa fitur adalah **menerjemahkan angka mentah menjadi sinyal psikologi dan fisika logistik—lalu membuktikan bahwa fitur baru itu stabil lintas waktu**.

Perhatikan tiga fitur rekayasa unggulan kami:  
- Pertama, **`freight_ratio`**: ongkir Rp 25.000 tidak menyakitkan bagi pembeli kulkas Rp 4 juta, tapi terasa mencekik bagi pembeli kabel Rp 20.000! Rasio ini mengukur sakit psikologis biaya kirim relatif terhadap nilai barang.  
- Kedua, **`seller_buyer_distance_km`**: alih-alih memberi kode angka kota mentah yang tidak bermakna jarak bagi model, kita menghitung jarak lengkung permukaan bumi **Haversine** antara gudang penjual dan rumah pembeli, lalu mengalikannya dengan bobot barang menjadi **`distance_x_weight`** (*beban fisik logistik*).  
- Ketiga, fitur interaksi non-linier **`delay_x_freight_ratio`** dan **`high_value_late_flag`** (`price > R$ 150` dan telat): ini menangkap hukum psikologi konsumen bahwa pelanggan barang mahal atau pelanggan yang membayar ongkir mahal jauh lebih marah ketika kurirnya telat!

Sementara untuk riwayat pelanggan, **`prior_order_count`** memakai aturan **Point-in-Time As-Of**—artinya memotret rekam jejak transaksi murni **sebelum** stempel waktu `t_order` detik ini, layaknya mencetak rekening koran sampai kemarin sore tanpa mengintip mutasi bulan depan. Dan sebelum dipasok ke model, kami audit stabilitas distribusinya antara pra-Maret dan pasca-Maret 2018 memakai **`PSI` (*Population Stability Index*)**: hasilnya `freight_ratio = 0,021`, `distance = 0,018`, dan `delivery_delay = 0,048`—semuanya nyaman di bawah ambang peringatan `0,10`!"

**[SLIDE 18 | VISUAL LAYAR]**  
*Benteng Anti-Kebocoran Waktu (Pemisahan Himpunan Fitur `FEATURE_SETS`):*  
- **Himpunan Fitur Saat Checkout (`10 Fitur`):** Hanya fakta pra-pembayaran. **Diblokir keras** oleh validasi anti-kebocoran fitur: `approval_lag_hours`, tanggal serah kurir, `delivery_delay_days`, `delivery_lead_time_days`, `is_late`, rating & teks ulasan.  
- **Himpunan Fitur Saat Serah Kurir (`5 Fitur`):** `total_order_value`, `freight_ratio`, `estimated_lead_time_days`, `seller_buyer_distance_km`, `approval_lag_hours`.  
- **Himpunan Fitur Pasca-Pengiriman (`15 Fitur`):** Menggabungkan fitur ekonomi, pengalaman aktual kurir, dan interaksi non-linear untuk *triage* sebelum bintang satu muncul / akar masalah pasca-kirim.  
- **Himpunan Fitur Kohort Retensi (`cohort_checkout_features` `8 fitur` vs `cohort_post_delivery_features` `11 fitur` vs `cohort_post_survey_features` `13 fitur`).**

**[KALIMAT YANG DIUCAPKAN]:**  
"Namun merekayasa 41 fitur canggih saja justru berbahaya kalau kita mencampurkan detik kelahirannya! Analogi klasiknya: memakai suhu tubuh pasien saat masuk UGD tiga hari setelah minum obat untuk 'meramal' pendaftaran asuransi di hari pertama jelas curang—dalam ML itu disebut **Temporal Target Leakage**.

Pada tahap pemisahan fitur ini, setiap fitur dikunci ke dalam **batasan tahap waktu masing-masing**: pada tahap checkout saat bayar di kasir, model hanya boleh menyentuh **`10` fitur pra-bayar**; pada tahap serah kurir saat paket dikirim, model delay memakai **`5` fitur rute awal**; dan baru pada tahap pasca-pengiriman, model diagnostik ulasan diizinkan membuka ke-**`15` fitur pengalaman lengkap**. Pemisahan kamus fitur ini menjamin tidak satu pun atribut pengiriman pasca-transaksi masuk ke pelatihan tahap pembayaran."

**[SLIDE 19 | VISUAL LAYAR]**  
*Transformasi Kategorikal Tanpa Bocor & Efisiensi Memori (`Split-Before-Transform` + **Bayesian Target Encoding $\alpha = 10$**):*  
- **Mengapa tidak pakai *One-Hot Encoding* mentah untuk 70+ kategori produk & 27 provinsi?** Meledakkan dimensi kolom, memboroskan memori, dan kategori kecil mudah *overfit*.  
- **Cara Kerja **`CategoricalFoldEncoder`** (pipeline *fold encoding*):** Menghitung rata-rata risiko tiap kategori **hanya pada training fold aktif**, ditarik ke rata-rata global dengan faktor pemulus **Bayesian $\alpha = 10$** *(analogi: warung baru yang baru 1 kali telat tidak langsung dicap 100% gagal, melainkan ditarik lembut ke rata-rata seluruh toko sebelum punya cukup bukti transaksi)*. Kategori baru di uji/validasi otomatis mendapat *global training mean*.  
- **Konsistensi Tipe Variabel:** Penyesuaian tipe numerik dan kategorikal diterapkan konsisten di dalam alur transformasi tanpa membocorkan statistik validasi.

**[KALIMAT YANG DIUCAPKAN]:**  
"Bagaimana model pohon maupun linier memproses 71 kategori produk dan puluhan negara bagian? Kalau memakai **One-Hot Encoding** (memecah 1 kolom menjadi 70 kolom angka nol-satu), tabel langsung gemuk dan kategori yang cuma punya 2 pesanan mudah menghafal kebetulan (*overfitting*).  
Di CSIP, `CategoricalFoldEncoder` menerapkan **Bayesian Target Encoding** ($\alpha = 10$) di dalam setiap lipatan latih (*training fold*). Bayangkan seorang hakim menilai reputasi pedagang baru yang baru jualan 2 kali dan kebetulan telat sekali: hakim bijak tidak menghukum 50%, melainkan menarik skor awal pedagang baru tersebut menuju rata-rata pedagang nasional ($\alpha = 10$ bertindak sebagai pemberat kehati-hatian), sementara pedagang lama dengan 5.000 transaksi dinilai murni dari rekam jejaknya sendiri—dan semua penghitungan ini patuh pada **Split-Before-Transform** (dipelajari hanya dari data latih)."

---

# BAGIAN 03 — VALIDASI TEMPORAL KRONOLOGIS (SLIDE 20–24)

## BABAK 5: STRATEGI VALIDASI TEMPORAL — *4-FOLD ROLLING-ORIGIN CV*, KARANTINA *EMBARGO 90 HARI*, *MOVING-BLOCK BOOTSTRAP* & *SINGLE LOCKED TEST*
*(Alokasi waktu: 4 menit · Slide 20–24)*

**[SLIDE 20–22 | VISUAL LAYAR]**  
*Skema **Rolling-Origin Temporal Cross-Validation** (modul evaluasi temporal):*  
- **`RollingOriginTemporalCV(n_folds=4, embargo_days=90, min_train_days=180, val_window_days=45, test_start_date="2018-07-01")`**  
- Penegakan invarian matematis: **`fold.val_start >= fold.train_end + 90 hari`**  
- Mengapa `embargo = 90 hari`? Mencegah *delayed label overlap* (label yang tertunda terwujudnya): pesanan yang dibuat menjelang ujung periode latih butuh waktu transit hingga beberapa minggu plus jendela pengamatan ulasan/retensi 90 hari hingga tuntas sebelum periode validasi dimulai!

**[KALIMAT YANG DIUCAPKAN]:**  
"Di sinilah letak pemisah antara pemula ML dan praktisi industri. Pemula sering memanggil `train_test_split(..., shuffle=True)` yang mengocok transaksi bulan Januari dan bulan Desember dalam satu mangkuk acak. Akibatnya? Model tanpa sadar belajar dari masa depan (Desember) untuk menebak masa lalu (Januari), lalu skornya melambung semu!

Pada skema validasi temporal ini, kami melarang pengocokan acak dan menerapkan **4-Fold Expanding-Window Rolling-Origin Cross-Validation**—persis seperti melatih seorang analis dari sejarah 2016–awal 2017 untuk diuji memprediksi pertengahan 2017, lalu memperluas ilmunya ke akhir 2017 untuk meramal awal 2018, maju mengikuti panah waktu! Lebih ketat lagi, di antara ujung data latih dan awal validasi kami pasang **karantina Embargo minimal `90` hari kalender**. Mengapa? Karena pesanan yang dibeli di hari terakhir masa *training* masih berjalan di truk kurir berminggu-minggu dan status puas atau beli-ulangnya baru terwujud puluhan hari kemudian!"

**[SLIDE 23 | VISUAL LAYAR]**  
*Ketidakpastian Berurutan Waktu (**Moving-Block Bootstrap**) & Evaluasi Holdout Sekali Jalan (**Locked Test Protection**):*  
1. **`compute_block_bootstrap_ci(block_size=5, n_bootstraps=1000, seed=42)`:**  
   - **Apa itu *Bootstrap* biasa?** Mengocok ulang sampel acak berulang-ulang untuk mengukur rentang keyakinan (*95% Confidence Interval*).  
   - **Mengapa pakai *Moving-Block Bootstrap*?** Pada deret waktu (*time series*), kesalahan di hari Senin berantai ke hari Selasa. Kalau dikocok per titik satuan, struktur urutan waktu rusak! *Moving-Block Bootstrap* memotong data menjadi **blok berurutan (5 titik)** lalu menyampel ulang blok tersebut 1.000 kali—persis seperti menyambung cuplikan klip video 5 detik daripada mengacak frame foto tunggal!  
2. **Kunci Tunggal `evaluate_locked_test_once()`:** Variabel pengunci `final_locked_test_reported_once` secara harfiah melempar **`RuntimeError`** apabila ada kode yang mencoba menguji berulang-ulang pada *Locked Test Holdout* (`> 2018-06-30`, `N = 12.571` / `12.630`)!

**[KALIMAT YANG DIUCAPKAN]:**  
"Ada dua penjaga kejujuran tambahan pada protokol validasi:  
Pertama, kapan pun kita melaporkan skor rata-rata model, angka tunggal tanpa rentang kepercayaan hanyalah ilusi kepastian. Karena data transaksi harian memiliki autokorelasi (*macet minggu ini berimbas ke minggu depan*), kami tidak mengocok baris secara terpisah melainkan memakai **`Moving-Block Bootstrap` (`block_size=5`, `1.000` iterasi)**—ibarat mengocok potongan video berdurasi 5 detik alih-alih mengacak bingkai foto lepas agar struktur waktu tetap utuh.  
Kedua, setelah seluruh validasi selesai, ruang uji masa depan (`Locked Test`) disegel oleh **`evaluate_locked_test_once()`**: jika ada program atau pengembang mencoba mengevaluasi ulang berulang kali untuk mencuri penyesuaian parameter (*test-set overfitting*), kode langsung menolak dengan **`RuntimeError`**!"

**[SLIDE 24 | VISUAL LAYAR]**  
*Peta Tanggal Partisi Final di `ModelExperimentTrainer` & `TemporalCVManager`:*  
- **Training Window Utama:** Awal data (`2016-09`) s/d **`2018-03-31`**  
- **Validation Window Utama:** **`2018-04-01`** s/d **`2018-06-30`** *(tuning hiperparameter, seleksi model, fitting kalibrator Platt, kalibrasi threshold kuota)*  
- **Locked Test Holdout *(Tersegel Tunggal!)*:** **`> 2018-06-30`** (`2018-07-01` s/d `2018-08-29`, `N = 12.571` klasifikasi ulasan, `N = 12.630` regresi delay).  
- Untuk model kohor *repeat purchase* (`get_cohort_temporal_splits_with_embargo`), diterapkan dua celah karantina 90 hari sekaligus: `Train <= 2017-08-31` → *(embargo 90 hari)* → `Val 2017-12-01..2018-01-31` → *(embargo 90 hari)* → `Test 2018-05-01..2018-05-31`.

**[KALIMAT YANG DIUCAPKAN]:**  
"Lihat kalender resmi pada pembagian kalender partisi. Mulai dari seleksi model terbaik, fitting pelurus probabilitas *Platt Scaling*, sampai uji kepekaan ambang batas, seluruhnya hanya boleh menyentuh jendela `Train (<= Maret 2018)` dan `Validation (Kuartal II 2018)`. Set uji terkunci sesudah `30 Juni 2018` (`N = 12.571` / `12.630`) dibiarkan steril. Dan khusus model retensi 90 hari yang berisiko terpotong kalender (*right-censoring*), kami bahkan memasang **embargo 90 hari ganda** baik sebelum jendela validasi maupun sebelum jendela uji Mei 2018."


---

# BAGIAN 04 — ARSITEKTUR ENAM KELUARGA MODEL MACHINE LEARNING (SLIDE 25–34)

## BABAK 6: PERBANDINGAN MODEL DASAR HINGGA ENSEMBLE POHON (*LIGHTGBM*)
*(Alokasi waktu: 5–6 menit · Slide 25–29)*

**[SLIDE 25–26 | VISUAL LAYAR]**  
*Filosofi Tangga Tanding (Urutan Pembandingan Algoritma dari Sederhana ke Kompleks):*  
Setiap model yang lebih rumit wajib membuktikan dirinya mengalahkan seluruh anak tangga di bawahnya pada data evaluasi yang identik (`seed = 42`):
- **Kelompok Baseline Non-ML (Aturan & Mayoritas):**  
  1. `MajorityClassClassifier`: Menebak peluang konstan sesuai kelas terbanyak di data latih.  
  2. `MeanRegressor`: Selalu menebak angka rata-rata masa latih.  
  3. `DelayHeuristicClassifier`: Aturan satu baris staf gudang (*if `is_late == 1` → risiko 85%, else 15%*).
- **Kelompok Model Linier Terregularisasi:**  
  1. `StandardScaler` + **`LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", solver="lbfgs")`** *(garis S penaksir peluang dengan penalti L2 pencegah bobot liar)*.  
  2. `StandardScaler` + **`Ridge(alpha=1.0)`** *(regresi garis lurus dengan rem penahan bobot)*.

**[KALIMAT YANG DIUCAPKAN]:**  
"Sekarang kita masuk ke jantung mesin cerdas kita pada tahap pemodelan dasar. Banyak presentasi *Machine Learning* jatuh ke satu dosa ilmiah: langsung memamerkan algoritma paling rumit tanpa menguji apakah aturan sederhana staf gudang atau garis lurus klasik sudah cukup memecahkan masalah! Analogi gampangnya: seseorang mengklaim telah merancang mobil balap tercepat, tetapi tidak pernah mengadu mobilnya melawan sepeda motor standar—dari mana kita tahu desainnya benar-benar unggul?

Di CSIP, seluruh model wajib mendaki **perbandingan bertingkat dari baseline hingga *deep learning*** dengan penguncian angka acak `random_seed = 42`:
- **Pada baseline sederhana**, kita pasang tiga patokan paling lugu: menebak konstan mayoritas, menebak rata-rata keterlambatan, dan **`DelayHeuristicClassifier`**—aturan satu baris staf operasional (*'Pokoknya paket telat → risiko 85%'*). Hukum wajibnya: model ML apa pun yang kalah melawan aturan satu baris ini langsung didiskualifikasi!
- **Pada model linier**, kita menguji apakah polanya cukup ditangkap secara linier: **`LogisticRegression` (`C=1,0`, `class_weight="balanced"`, `solver="lbfgs"`)** untuk klasifikasi keluhan (di mana `class_weight="balanced"` memberi hukuman sembilan kali lipat kalau gagal menangkap keluhan minoritas), dan **`Ridge Regression` ($\alpha = 1,0$)** untuk meramal hari keterlambatan."

**[SLIDE 27 | VISUAL LAYAR]**  
*Kelompok Klasik Non-Linier — Evaluasi Algoritma Klasik Non-Linier:*  
1. **`DecisionTreeClassifier / Regressor(max_depth=6, min_samples_split=50)`** — *Satu Pohon Keputusan Tunggal*: Membelah data dengan pertanyaan berjenjang (*misal: apakah telat > 3 hari? → ya/tidak*), dibatasi kedalaman 6 tingkat & minimal 50 transaksi per cabang supaya pohon tidak menghafal contoh unik (*overfitting*).  
2. **`StandardScaler` + `KNeighborsClassifier(n_neighbors=15, weights="distance", metric="euclidean")`** — *Bertanya ke 15 Tetangga Terdekat*: Mencari 15 transaksi historis yang paling mirip profilnya di ruang fitur terstandar, lalu memberi suara lebih besar kepada tetangga yang paling mirip (`weights="distance"`). *(Wajib pakai `StandardScaler` agar fitur jutaan tidak menenggelamkan fitur pecahan desimal!)*  
3. **`StandardScaler` + `GaussianNB` (*Naive Bayes*)** — *Penghitung Peluang Cepat Berasumsi Fitur Saling Bebas*: Menghitung probabilitas tiap ciri secara terpisah. Cepat sekali, tetapi lemah ketika fitur saling terikat kuat (seperti harga, ongkir, jarak, dan berat!).

**[KALIMAT YANG DIUCAPKAN]:**  
"Begitu kita punya patokan linier, kita menguji tiga mekanisme belajar non-linier paling terkenal di buku teks Data Science**:
- Pertama, **Decision Tree tunggal (`max_depth=6`, `min_samples_split=50`)**—persis seperti daftar tanya-jawab dokter berjenjang maksimal enam lapis agar pohonnya tidak menghafal kebetulan unik satu-dua pasien.
- Kedua, **K-Nearest Neighbors (`K=15`, `weights="distance"`)**—analogi termudahnya seperti menilai harga rumah baru dengan bertanya kepada **15 rumah tetangga terdekat** yang luas dan lokasinya paling mirip, di mana tetangga satu pagar suaranya lebih berat daripada rumah beda blok. Perhatikan bahwa di kode kami `StandardScaler` wajib dipasang sebelum KNN, karena tanpa penyama skala, jarak kilometer (`0–3.500`) akan menenggelamkan rasio ongkir (`0–0,95`)!
- Ketiga, **Gaussian Naive Bayes**, model probabilistik super cepat yang mengasumsikan semua fitur bekerja sendiri-sendiri (*statistically independent*) dan berdistribusi lonceng simetris. Tentu di logistik nyata hal itu dilanggar—paket jauh dan berat hampir pasti ongkirnya tinggi—dan nanti di papan peringkat kita lihat persis berapa harga skor yang dibayar akibat asumsi tersebut!"

**[SLIDE 28 | VISUAL LAYAR]**  
*Kelompok Ensemble Pohon — Regu Ansambel Pohon: **Random Forest** vs Juara Tabular **LightGBM Gradient Boosting**:*  
- **`RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=20, class_weight="balanced")`:** *Parlemen 100 Pohon Independen* — menumbuhkan 100 pohon pada sampel acak paralel (*Bagging* — mengundi suara terbanyak) untuk meredam varians.  
- **`LGBMClassifier / LGBMRegressor(n_estimators=150, max_depth=6, num_leaves=31, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, class_weight="balanced")`:** *Regu Estafet Koreksi Kesalahan* — menumbuhkan **150 pohon secara berurutan** (*Gradient Boosting*), di mana tiap pohon baru khusus belajar memperbaiki gradien sisa kesalahan pohon sebelumnya!

**[KALIMAT YANG DIUCAPKAN]:**  
"Lalu kita naik dari pohon tunggal ke **kerja tim ratusan pohon** (*Ensemble Learning*), dan di sini ada dua filosofi bertarung:

Pertama adalah **Random Forest (`100` pohon, kedalaman maks `8`, `min_samples_leaf=20`)**. Filosofinya adalah **Bagging (*Bootstrap Aggregating*)**: bayangkan seratus dokter magang masing-masing diberi potongan rekam medis acak sedikit berbeda lalu dimintai voting suara terbanyak. Karena masing-masing melihat sudut sedikit berbeda, kekeliruan ekstrem satu pohon dinetralkan oleh suara 99 pohon lainnya!

Kedua adalah **LightGBM Gradient Boosting (`150` pohon berurutan, `31` daun, `learning_rate=0,05`)**. Alih-alih serentak bekerja sendiri seperti anggota parlemen, pohon-pohon LightGBM bekerja seperti **regu pelukis estafet**: pelukis ke-1 menggambar sketsa utama; pelukis ke-2 datang khusus menambal bagian yang meleset paling parah pada gambar pelukis ke-1; pelukis ke-3 menambal sisa kesalahan pelukis ke-2—berulang 150 kali dengan langkah koreksi kecil `0,05` (`shrinkage`) agar gambar akhirnya presisi tanpa berlebihan!"

**[SLIDE 29 | VISUAL LAYAR]**  
*Mengapa **LightGBM** Menjadi Juara Data Tabel di CSIP (Model Terbaik Tabular)?*  
1. **Tajam Memisahkan Pola Non-Linier (*Leaf-Wise Splitting* vs *Depth-Wise*):** Data belanja & keterlambatan sangat miring (`Skewness +6,21`, ekor `+188 hari`). Strategi tumbuh daun terbaik lebih dulu (**`num_leaves = 31`**, dipagari **`max_depth = 6`**) memusatkan percabangan persis di area krisis (*misal `delay > 3 hari` & `freight_ratio > 0,25`*).  
2. **Pagar Anti-*Overfitting* (`subsample=0.8`, `colsample_bytree=0.8`):** Setiap pohon hanya mengintip `80%` baris dan `80%` kolom acak supaya model kebal menghafal satu pola tunggal.  
3. **Keseimbangan Bias-Varians dengan Regularisasi:** Pembatasan `max_depth=6` dan sampling acak `0,8` mencegah model menghafal noise lokal.

**[KALIMAT YANG DIUCAPKAN]:**  
"Pada bagian mekanika *LightGBM* ini, mari kita jawab pertanyaan teknis yang sering muncul di wawancara *Senior Data Scientist*: **bagaimana persisnya mesin internal LightGBM memodelkan distribusi miring Olist tanpa mengalami *overfitting*?**

Berbeda dengan pohon klasik yang menumbuhkan seluruh cabang tiap tingkat secara simetris (*depth-wise*—ibarat menyiram semua dahan meski dahannya kosong), LightGBM tumbuh secara **leaf-wise (*num_leaves=31*)**, artinya hanya memperdalam dahan yang memberi penurunan kesalahan (*loss reduction*) paling besar. Karena data Olist punya ekor panjang ekstrem (`delay` dari `-146` sampai `+188 hari`, `skewness +6,21`), pembelahan *leaf-wise* sangat tajam memotong penurunan tajam rating setelah `3 hari` terlambat.

Dan supaya pertumbuhan agresif itu tidak menghafal *noise*, kita menguncinya lewat **tiga batas regularisasi di konfigurasi model**: batas kedalaman `max_depth=6` (di bawah $2^6 = 64$), sampling acak `80%` baris (`subsample=0.8`), serta sampling acak `80%` fitur per pohon (`colsample_bytree=0.8`). Kombinasi ini menjaga keseimbangan antara kapasitas non-linier dan ketahanan terhadap overfitting."

---

## BABAK 7: PEMODELAN *DEEP LEARNING* (`TABULAREMBEDDINGMLP` & `TEXTBILSTM`) — KAPAN *NEURAL NET* KALAH DAN KAPAN MENANG
*(Alokasi waktu: 3,5 menit · Slide 30–31)*

**[SLIDE 30 | VISUAL LAYAR]**  
*Arsitektur 1 (Deep Learning Tabular): **`TabularEmbeddingMLP`** (arsitektur *deep tabular*):*  
- **Masukan Kategorikal melalui *Entity Embeddings*** *(peta koordinat makna yang dipelajari otomatis oleh jaringan saraf!)*:  
  - `product_category` (`75` kategori) → vektor **`16` dimensi**  
  - `customer_state` (`28` wilayah) → vektor **`8` dimensi**  
- **Masukan Numerik Kontinu:** Distabilkan lewat **`BatchNorm1d`** *(menjaga skala angka antarlapisan tetap seimbang selama latihan)*.  
- **Jaringan Penuh (*Feed-Forward Dense Network*):** Gabung (`concat`) `24D embedding + fitur kontinu` → **`[128 neuron → BatchNorm → ReLU → Dropout(0,2)]` → `[64 neuron → BatchNorm → ReLU → Dropout(0,2)]` → `1 Logit Output`** (`lr=0,001`, `batch=128`, `15 epochs`).  
- **Hasil Adu Uji Tabel (evaluasi model tabular):** **`PR-AUC = 0,2875`**, **`ROC-AUC = 0,6548`**, `F1 = 0,3268`, `Brier = 0,1561` *(unggul dari Logistic `0,2436`, tetapi kalah dari LightGBM `0,3061`)*.

**[KALIMAT YANG DIUCAPKAN]:**  
"Sebagai *Data Scientist*, kita sering ditanya dalam diskusi teknis: *'Sekarang zamannya AI Deep Learning—kenapa tidak pakai Neural Network saja untuk memprediksi semua masalah Olist?'*  
Alih-alih menjawab dengan opini, pada kategori *Deep Learning* kami membangun dan mengadu langsung dua arsitektur jaringan saraf PyTorch CPU-friendly!

Pada bagian *deep tabular* ini adalah arsitektur pertama: **`TabularEmbeddingMLP`** untuk data tabel. Ide briliannya adalah **Entity Embeddings**—yaitu memetakan setiap nama provinsi (`28` wilayah → `8` angka) atau kategori produk (`75` kategori → `16` angka) ke titik koordinat di peta makna, sehingga jaringan saraf bisa menyadari sendiri bila dua provinsi punya pola kirim serupa. Supaya gradien latihan stabil, kami sisipkan **Batch Normalization** (penyeimbang skala antarlapisan) dan **Dropout 20%** (mematikan seperlima neuron secara acak saat latihan supaya tidak manja menghafal pola).

Apa hasil pembuktian nyatanya? **`PR-AUC` mencapai `0,2875`** dan `ROC-AUC 0,6548`—jauh mengalahkan model linier `LogisticRegression (0,2436)` maupun pohon tunggal `Decision Tree (0,2704)`, **tetapi tetap kalah dari ansambel pohon `LightGBM` (`0,3061`)**! Mengapa? Karena seperti temuan konsisten literatur ML modern, pembelahan tegak lurus pada *gradient boosted trees* lebih hemat sampel untuk memotong batas risiko tajam pada tabel `64.000` baris dengan fitur berdistribusi miring."

**[SLIDE 31 | VISUAL LAYAR]**  
*Arsitektur 2 (Deep Sequence NLP): **`TextBiLSTM`** (Model Sequence NLP Bahasa Portugis):*  
- **Populasi Khusus Teks Tertulis (Pemisahan Populasi Teks Tertulis):** Beroperasi khusus pada `N = 41.524` pesanan yang memiliki komentar tertulis pada korpus ulasan tertulis (`N_train=26.450`, `N_val=8.150`, **`N_test=4.142`**, *base rate* lebih tinggi yaitu **`16,2%`** karena pelanggan kesal lebih rajin mengetik ulasan!).  
- **Alur Saraf PyTorch:** `SimpleTokenizer` Portugis (`vocab 5.000`, `min_freq=2`) → `Word Embedding` *(32D/64D)* → **`Bidirectional LSTM` (`hidden=64`, dua arah = `128D`)** → **`Global Max Pooling`** → `Dense(128→64→1) + Dropout`.  
- **Kinerja Terukur pada Subset Komentar Teks:**  
  - Evaluasi *Holdout Text Card* (`N=4.142`, base `16,2%`): **`PR-AUC = 0,3120`** *(+92,6% vs Text Prior `0,1620`)*, **`ROC-AUC = 0,7240`**, **`F1 = 0,3680`**, **`Test Brier = 0,1140`**.  
  - Evaluasi *Multi-Class / Full Text Checkpoint* (evaluasi penuh teks): **`Macro-F1 = 0,8420`**!

**[KALIMAT YANG DIUCAPKAN]:**  
"Sebaliknya pada pemodelan teks ulasan ini, begitu kita melangkah dari data angka di tabel masuk ke **kalimat teks komentar pelanggan bahasa Portugis**, situasinya berbalik total!

Pada kalimat manusia, urutan dan negasi menentukan makna: kalimat *'Pengiriman **tidak** tepat waktu, mengecewakan'* punya arti berlawanan dengan *'**Tidak** ada keluhan, sangat bagus!'* Pencacah frekuensi kata sederhana (*Bag-of-Words*) langsung tertipu oleh kemunculan kata 'tidak' dan 'bagus'.

Maka di **`TextBiLSTM`**, kami menggunakan **`Bidirectional LSTM`**—yaitu pembaca berantai yang menelusuri kalimat dari **kiri-ke-kanan sekaligus kanan-ke-kiri**—lalu menyaringnya dengan **`Global Max Pooling`** (*memetik sinyal emosi terkuat dari seluruh panjang kalimat*). Yang penting untuk dicatat secara jujur (Pemisahan Populasi Teks Tertulis): `TextBiLSTM` diuji di sub-populasi khusus `N_test = 4.142` pelanggan yang benar-benar mengetik komentar (di mana tingkat kemarahannya `16,2%`, bukan `9,85%` populasi umum), dan sukses meraih **`PR-AUC 0,3120`** (+92,6% di atas baseline teks `0,1620`), **`ROC-AUC 0,7240`**, serta **`Macro-F1 = 0,8420`** pada benchmark penuhnya—menjadikannya mesin triase keluhan tertulis setelah survei masuk!"

---

## BABAK 8: MODEL *UNSUPERVISED* (`K-MEANS + PCA`), *SURVIVAL* (`KAPLAN-MEIER`), & *WORLD MODEL* (`VAR(1)`)
*(Alokasi waktu: 4 menit · Slide 32–34)*

**[SLIDE 32 | VISUAL LAYAR]**  
*Segmentasi Perilaku Tanpa Label (**`BehavioralClusterer`** di modul klastering & evaluasi segmen):*  
- **5 Fitur Masukan *(distandardisasi dgn `StandardScaler`)*:** `total_order_value`, `freight_ratio`, `delivery_lead_time_days`, `item_count`, `payment_installments_max`.  
- **Seleksi Jumlah Klaster `k in [3, 4, 5, 6, 7]` (`N = 96.470` transaksi, subsample `15.000` untuk metrik jarak):**  
  - Evaluasi komposit **`Silhouette - 0,1 × Davies-Bouldin`**: **`k=3` (`Sil=0,3865`, `DB=1,2168`, `CH=3124,5`)**, `k=4` (`Sil=0,3485`, `DB=1,2361`), `k=5` (`Sil=0,3483`), `k=6` (`Sil=0,3602`). *(Catatan artefak: konfigurasi klastering pembanding meraih `K=4 Silhouette 0,4180`; uji stabilitas 45 resample bootstrap mencatat **`ARI = 0,9832`**, `Jaccard = 0,9893` pada `k=4`, dan `ARI = 0,8511` pada `k=3`!)*  
- **Reduksi Dimensi `PCA 2D`** *(memampatkan 5 fitur ke 2 sumbu visual untuk `clustering_pca_clusters.png`)*: Menjelaskan **`52,81%` total varians** (`PC1 = 31,15%`, `PC2 = 21,66%`).  
- **Deteksi Anomali Jarak Centroid:** **`4.824` transaksi ekstrem** melampaui batas jarak **`3,1838`** dari pusat kelompoknya!

**[KALIMAT YANG DIUCAPKAN]:**  
"Sekarang kita pindah dari model berlabel (*Supervised*) ke model tanpa label (*Unsupervised*) pada segmentasi tanpa supervisi. Mengapa tim Data Scientist wajib melakukan *clustering* sebelum memodelkan kebijakan harga? Karena rata-rata nasional selalu menyembunyikan kelompok ekstrem!

Kami mengambil **5 dimensi perilaku transaksi** atas `96.470` pesanan bersih yang sudah disamakan skalanya (`StandardScaler`), lalu menguji **`K-Means` dari $k=3$ hingga $k=7$**. Alih-alih memakai metode subjektif *Elbow* ('mencari siku grafik'), di `BehavioralClusterer` kami menggabungkan tiga metrik matematis: **Silhouette Score** (*mengukur seberapa rapat anggota segmen dibanding jaraknya ke segmen tetangga*), **Davies-Bouldin Index** (*makin kecil makin terpisah rapi*), dan **Calinski-Harabasz** (`3.124,5`).  
Belum cukup sampai di situ: karena K-Means peka terhadap titik awal acak, kami mengocok ulang data sebanyak **45 kali *bootstrap*** berdasarkan uji stabilitas klaster untuk mengukur **ARI (*Adjusted Rand Index*)**—yaitu konsistensi apakah transaksi yang sama selalu masuk ke kelompok yang sama. Hasilnya sangat kokoh: `ARI = 0,8511` pada $k=3$ dan memuncak ke **`0,9832`** (`Jaccard 0,9893`) pada $k=4$, plus secara otomatis mendeteksi **`4.824` titik pencilan** di luar ambang jarak centroid `3,1838`."

**[SLIDE 33 | VISUAL LAYAR]**  
*Profil Nyata 3 Segmen Persona dari Data (hasil evaluasi klastering — `N = 96.470`):*

| Segmen Klaster | Ukuran Populasi | Ciri Rata-Rata / Median Utama | Tingkat Keluhan Nyata | Wawasan Bisnis untuk Tim Produk |
| :--- | :---: | :--- | :---: | :--- |
| **Segmen 0:** *High-Ticket Premium Basket* | `18.987` (**19,68%**) | Order median `R$ 211,0` (`mean R$ 333,2`), ongkir ringan **`13%`**, kirim agak lama `11,5–14,6 hari`, **cicilan panjang (`median 8×`)** | **`15,33%`** | Pembeli kredit bernilai tinggi—sensitif ketepatan waktu meski ongkir terasa murah relatif ke harga |
| **Segmen 1:** *Fast Single-Item Convenience* | `75.244` (**78,00%**) | Order ekonomis (`median R$ 86,9`), `1` barang, **bayar langsung (`1×` cicilan)**, kirim cepat `10 hari` | **`11,63%`** | Tulang punggung volume harian dengan tingkat kepuasan paling stabil |
| **Segmen 2:** *High-Friction Multi-Item Heavy Freight* | `2.239` (**2,32%**) | Keranjang isi **`3–4` barang** (`mean R$ 372,5`), **rasio ongkir mencekik (`mean 41%`, `median 31%`!)** | **`31,20%`** *(Hampir 3× lipat Segmen 1!)* | Kelompok krisis gesekan biaya & koordinasi banyak barang—target utama **subsidi terarah!** |

**[KALIMAT YANG DIUCAPKAN]:**  
"Begitu angka klaster pada profil klaster tersebut dipetakan kembali ke profil transaksi asli, keluarlah satu **penemuan strategis yang langsung menghemat anggaran perusahaan**!

Mayoritas pembeli kita (**Segmen 1, `78%`**) adalah pembeli barang satuan praktis dengan tingkat keluhan rendah `11,63%`. Lalu **Segmen 0 (`19,68%`)** adalah pembeli barang mahal dengan cicilan panjang median `8` kali—ongkir cuma `13%` dari belanja mereka, jadi mereka tidak peduli diskon ongkir; yang mereka tuntut adalah paket jangan telat (`keluhan 15,33%`).

Namun lihat **Segmen 2**: porsinya hanya **`2,32%` (`2.239` pesanan)**, berisi keranjang **3–4 barang sekaligus** dengan **rata-rata beban ongkos kirim tembus `41%`** dari harga barang! Dan tebak berapa tingkat kemarahannya? **Melonjak hampir tiga kali lipat ke `31,20%`!** Kelompok kecil berfriksi tinggi inilah yang nanti menjadi sasaran tepat kebijakan subsidi terarah di simulasi!"

**[SLIDE 34 | VISUAL LAYAR]**  
*Dua Model Dinamika Waktu Lainnya di CSIP:*  
1. **`Survival Analysis` (modul analisis survival & DCA):**  
   - **`KaplanMeierEstimator`:** Menghitung kurva peluang bertahan $S(t)$ dan risiko kumulatif $F(t) = 1 - S(t)$ tanpa bias akibat **Sensor Kanan (*Right-Censoring*)**—seperti menghitung daya tahan bola lampu ketika sebagian lampu masih menyala saat uji lab ditutup.  
   - **`Harrell's C-Index`:** Mengukur ketepatan peringkat pasangan waktu kejadian (*apakah orang yang kembali belanja lebih cepat memang diberi skor risiko hazard lebih tinggi?*).  
   - **`DiscreteTimeHazardModel`:** Memecah jendela pengamatan ke interval `[0–30, 30–60, 60–90]` hari memakai Regresi Logistik bersyarat pada orang-orang yang *masih belum membeli ulang* di awal interval.  
2. **`WorldStateTransitionModel` (`VAR(1)` State-Space `4×4`, State-Space VAR(1)):**  
   - Persamaan gerak mingguan terstandardisasi: **$S_{t+1} = C + \Phi \cdot S_t + \epsilon_t$** memakai **`Ridge(alpha=0.1)`** *(atau `0.05` di backtest)* melintasi `87` minggu (`65` latih / `22` OOS).  
   - Mengapa perlu **`Spectral Radius = 0,8412 < 1,0`** dan **`Synthetic Recovery Test`** (*max rel error `1,60%`*, *mean `0,33%`*)? Untuk menjamin matriks dinamika tidak meledak di simulasi jangka panjang sekaligus sanggup memulihkan koefisien sebenarnya dari data buatan yang terkontrol!

**[KALIMAT YANG DIUCAPKAN]:**  
"Melengkapi model klasifikasi dan klastering tadi, kami memasukkan dua senjata waktu (*temporal modeling*):  
Pertama, untuk menjawab kapan pelanggan kembali berbelanja tanpa terjebak bias pemotongan kalender (**Sensor Kanan**), kami membangun **`KaplanMeierEstimator`** non-parametrik, metrik peringkat **`Harrell's C-Index`**, dan **`DiscreteTimeHazardModel`** pada irisan `0–30–60–90` hari—analogi gampangnya, kita menghitung peluang terjadi pembelian ulang di bulan kedua khusus di antara pelanggan yang memang masih terpantau dan belum belanja ulang di bulan pertama.  
Kedua, **`WorldStateTransitionModel`** memodelkan interaksi mingguan antar-4 indikator makro lewat regresi matriks **VAR(1) Ridge** ($S_{t+1} = C + \Phi S_t + \epsilon_t$). Sebelum dipakai menyimulasikan kebijakan, kami wajib menguji apakah model sanggup merekonstruksi matriks transisi buatan yang parameternya sudah kita ketahui sebelumnya (**Synthetic Recovery Test**): hasilnya meleset maksimal cuma **`1,60%`** (rata-rata **`0,33%`**) dan nilai peredam kestabilannya (**Spectral Radius**) **`0,8412`** (`< 1,0`)."


---

# BAGIAN 05 — EVALUASI BERLAPIS & BATAS MODEL (SLIDE 35–49)

## BABAK 9: KELEMAHAN METRIK *ACCURACY* PADA DATA TIDAK SEIMBANG, PAPAN PERINGKAT MODEL, STUDI ABLASI KELOMPOK FITUR, & DINAMIKA *FOLD 1–4*
*(Alokasi waktu: 5–6 menit · Slide 35–40)*

**[SLIDE 35–36 | VISUAL LAYAR]**  
*Mengapa Kami Menolak **`Accuracy`** untuk Data Ulasan Timpang (`N_test = 12.571`, `Base Rate = 9,63%`):*  
- **Baseline Mayoritas (*Dummy Classifier*):** Dari `12.571` pesanan uji, ia cukup menebak **"SEMUA PUAS (`0`)"** ke seluruh `12.571` pesanan → **`Accuracy = 90,37%` (`11.360` benar)**, tetapi **Recall Keluhan = `0%` (`1.211` pelanggan marah kabur tanpa tersapa!)**.  
- **Timbangan Jujur Data Science CSIP:**  
  1. **`PR-AUC`** (*Precision-Recall Area Under Curve*): Mengadu kemurnian alarm (*Precision*) vs jangkauan keluhan tertangkap (*Recall*)—seperti **mencari jarum emas keluhan di dalam jerami `90%` pembeli tenang**!  
  2. **`ROC-AUC`**: Peringkat relatif apakah pembeli yang benar-benar marah diberi skor risiko lebih tinggi daripada pembeli puas.  
  3. **`MAE` / `RMSE` / `$R^2$`**: Error selisih hari nyata untuk model regresi.

**[KALIMAT YANG DIUCAPKAN]:**  
"Selamat datang di Bagian 05—**jantung evaluasi berlapis model CSIP**. Pada awal pembahasan evaluasi ini, mari kita lihat mengapa sebuah metrik tunggal sering menyesatkan: **skor Accuracy 90%**!

Bayangkan di meja saya hari ini ada `12.571` pesanan dari set uji terkunci, di mana hanya `1.211` di antaranya (`9,63%`) yang memberi bintang 1–2, sedangkan `11.360` sisanya (`90,37%`) puas. Kalau saya bikin model palsu berbaris kode `return 0`—menebak semua orang puas—berapakah nilai *Accuracy*-nya? **`90,37%`!** Angka ujiannya kelihatan dapat A+, padahal **ke-1.211 pembeli yang kecewa semuanya lolos kecewa (`Recall = 0%`)**!

Karena itu di CSIP kami menilai klasifikasi timpang berdasarkan **`PR-AUC`**—yaitu seberapa tajam model memungut jarum emas keluhan dari tumpukan jerami `90%` mayoritas, dibandingkan patokan lantai bawah `0,0963`—serta menilai regresi memakai **error hari nyata (`MAE`, `RMSE`, `$R^2$`)**."

**[SLIDE 37–38 | VISUAL LAYAR]**  
*Papan Peringkat Resmi Seluruh Model pada **Locked Holdout Test (`> 30 Juni 2018`, hasil uji terkunci)**:*

**Tabel A — Klasifikasi Ulasan Negatif (`negative_review_flag`, `N_train = 63.666`, `N_test = 12.571`, *Base Rate* = `0,0963`):**

| Tangga | Model & Fitur Set | Val PR-AUC (`N=19.587`) | **Locked Test PR-AUC** | **Test ROC-AUC** | Test F1 | Test Brier *(Mentah)* | Catatan Data Scientist |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline** | `Naive Majority` *(tebak puas)* | `0,1096` | `0,0963` *(lantai dasar)* | `0,5000` | `0,0000` | `0,0985` | Lantai bawah mutlak |
| **Baseline** | `Heuristic Rule` (`is_late == 1`) | `0,1883` | — | `0,5945` *(val)* | `0,2991` *(val)* | `0,1016` *(val)* | Aturan manual logistik |
| **Klasik** | `GaussianNB` (fitur penuh) | `0,2490` | `0,1996` | `0,6523` | `0,2805` | `0,1378` | Asumsi fitur independen gagal |
| **Linier** | `LogisticRegression` (fitur penuh) | `0,3134` | `0,2436` | **`0,6803`** | `0,3084` | `0,1533` | Peringkat global baik, non-linier kalah |
| **Klasik** | `K-Nearest Neighbors` (`k=15`, kombinasi fitur lengkap) | `0,3192` | `0,2532` | `0,6383` | `0,2212` | `0,0839` | Berat di memori & sensitif dimensi |
| **Klasik** | `Decision Tree` (`depth=6`, kombinasi fitur lengkap) | `0,3316` | `0,2704` | `0,6642` | `0,2804` | `0,0790` | Satu pohon menangkap batas telat |
| **Ensemble** | `Random Forest` (`100` pohon, kombinasi fitur lengkap) | `0,3535` | `0,3016` | `0,6727` | `0,3345` | `0,1555` | Bagging sangat stabil mendekati juara |
| **Ensemble** | **`LightGBM` (Pasca-Pengiriman, `15` fitur penuh)** | **`0,3598`** | **`0,3061`** `[0,279–0,334]` | **`0,6745`** `[0,656–0,693]` | **`0,3417`** | `0,1373` *(setelah Platt: **`0,0762`**)* | **CHAMPION TABULAR (`> 3,18×` lantai!)** |
| **Ensemble** | `LightGBM` (Saat Checkout, `10` fitur) | `0,1904` | **`0,1335`** `[0,122–0,148]` | `0,5468` | `0,1766` | `0,2370` | **hanya indikator awal** *(wajar, kurir belum jalan!)* |

**Tabel B — Regresi Keterlambatan Pengiriman (`delivery_delay_days`, `N_train = 64.156`, `N_test = 12.630`, `5` fitur Tahap Disposisi Kurir):**

| Tangga | Model Regresi | Val MAE (`N=19.684`) | **Locked Test MAE** | Test RMSE | Test $R^2$ | Catatan Kritis Model |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline** | `Naive Mean / Median` | `7,4529 hari` | `6,6903 hari` *(median latih)* | `10,1226` *(val)* | `-0,1015` | Selalu menebak rata-rata historis |
| **Linier** | **`Ridge Regression` ($\alpha=1,0$)** | **`5,7350 hari`** | **`4,7509 hari`** | **`5,9685`** | **`0,4454`** | Hubungan jarak & SLA di `5` fitur cukup linier! |
| **Ensemble** | **`LightGBM Regressor`** | `5,7378 hari` | **`4,8256 hari`** | `6,2458` | `0,3926` | Error turun **-27,9%** vs baseline median (memenuhi kriteria penurunan error) |

**[KALIMAT YANG DIUCAPKAN]:**  
"Lihat Tabel A dan Tabel B pada tabel perbandingan model—di sinilah kedewasaan seorang *Data Scientist* diuji oleh data nyata!

Pada **Klasifikasi Ulasan Negatif (Pasca-Pengiriman)**, karena hanya **`9,63%`** keluhan di ujian terkunci, kita mengadu delapan model di atas metrik **PR-AUC** (*ketajaman menyaring minoritas langka*). Terlihat jelas kenaikan anak tangganya: dari model polos `0,0963`, Naive Bayes `0,1996`, Regresi Logistik `0,2436`, KNN `0,2532`, Decision Tree `0,2704`, Random Forest `0,3016`, hingga **Champion LightGBM `0,3061`**—meningkat **3,18 kali lipat** di atas tebakan acak dan unggul tajam atas semua pesaing klasik di metrik utama `PR-AUC` maupun `F1-Score` (`0,3417`)!

Sekarang lihat **kejujuran ilmiah yang menarik di Tabel B (Regresi Waktu Keterlambatan)** dengan `5` fitur awal saat disetujui bayar (Saat Serah Kurir):  
Apakah model tercanggih *LightGBM* otomatis selalu mengungguli mutlak model linier sederhana? **Tidak selalu!** Lihat angkanya pada uji holdout: pada uji terkunci `N=12.630`, `LightGBM Regressor` memang memangkas kesalahan jauh di bawah patokan median (`4,8256 hari` vs `6,6903 hari`, turun **27,9%**), **tetapi `Ridge Regression` sederhana justru sedikit lebih tajam dengan `MAE 4,7509 hari` dan `$R^2 = 0,4454`**! Mengapa? Karena dengan hanya 5 fitur rute awal (jarak, harga, estimasi waktu, ongkir, jeda bank), pola deviasi ke hari kedatangan cukup dekat dengan garis lurus sehingga penalti regulerisasi *Ridge* lebih kebal terhadap *noise* musiman akhir 2018. Mengakui kapan model linier sanggup menyaingi *gradient boosting* adalah ciri analis data sejati, bukan sekadar pemuja kompleksitas!"

**[SLIDE 39 | VISUAL LAYAR]**  
*Studi Ablasi Fitur (`Studi Ablasi Antarkelompok Fitur`, evaluasi rekayasa fitur):*  
- **Grup Fitur Ekonomi Kasir Saja** *(harga, ongkir, item, cicilan saja, `N_val=19.587`)*: LightGBM PR-AUC **`0,1786`** *(Logistic `0,1787`)* — **sinyal lemah!**  
- **Grup Fitur Pengalaman Kirim Saja** *(hanya jarak, lead time, hari keterlambatan kurir)*: LightGBM PR-AUC **`0,2986`** *(naik **`+67,2%`** dibanding fitur ekonomi kasir saja!)*  
- **Kombinasi Fitur Ekonomi + Pengiriman + Interaksi** *(ekonomi + pengiriman + `delay_x_freight_ratio` + `distance_x_weight`)*: LightGBM PR-AUC **`0,3598`** (Validasi) / **`0,3061`** (Locked Test; selisih uji ablasi `Delta PR-AUC = +0,1401`, `p = 0,00012`).  
- **Kontribusi Permutation Drop Test (evaluasi rekayasa fitur):** Mengacak `delivery_delay_days` meruntuhkan AUC sebesar **`0,0842`**, disusul `delay_x_freight_ratio` (`0,0415`) & `is_late` (`0,0321`); pada regresi delay `5` fitur vs fitur mentah saja, rekayasa fitur memangkas MAE `-0,6556 hari` (`5,4812 → 4,8256`, **`+18,1%` lonjakan $R^2$**)!

**[KALIMAT YANG DIUCAPKAN]:**  
"Banyak orang mengira model kita pintar semata-mata karena kita memilih `LightGBM`. Pada studi ablasi ini, melalui **Studi Ablasi (*Feature Ablation*)**—yaitu melepas sekelompok fitur layaknya melepas komponen mobil satu per satu untuk melihat kontribusinya—kita membuktikan bahwa **rekayasa fiturlah pahlawan utamanya**:

Ketika LightGBM hanya diberi **fitur ekonomi kasir** (harga, item, cicilan), skor PR-AUC validasinya tersangkut rendah di **`0,1786`**. Begitu kita tukar dengan **fitur pengalaman kurir (grup pengalaman kirim)**, skornya langsung melesat **`+67,2%` ke `0,2986`**. Dan saat keduanya digabung bersama fitur interaksi non-linier **`delay_x_freight_ratio` (fitur penuh)**, skornya melonjak lebih jauh ke **`0,3598`** (`0,3061` pada uji terkunci)! Uji pengacakan fitur (*Permutation Feature Importance*) mengonfirmasi: apabila kolom `delivery_delay_days` dan `delay_x_freight_ratio` diacak nilainya, daya diskriminasi AUC model langsung ambruk paling parah (`-0,0842` dan `-0,0415`)."

**[SLIDE 40 | VISUAL LAYAR]**  
*Mengintip Stabilitas Antar-Musim — Hasil Per-Fold **4-Fold Rolling-Origin Temporal CV** (hasil Temporal CV):*

| Lipatan Waktu | Jumlah Latih | Jumlah Uji Validasi | *Base Rate* Keluhan Nyata | LightGBM **PR-AUC** | LightGBM **ROC-AUC** | Brier Score | Fenomena Dunia Nyata di Lapangan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Fold 1** | `3.683` | `5.115` | `10,03%` | `0,2308` | `0,6248` | `0,0859` | Data latih masih kecil di awal pertumbuhan platform |
| **Fold 2** | `14.498` | `6.707` | `11,48%` | `0,3729` | `0,7124` | `0,0867` | Sampel latih 4× lebih kaya, PR-AUC melompat tajam |
| **Fold 3** | `29.787` | `10.349` | **`19,98%`** *(Lonjakan 2×!)* | **`0,6417`** | **`0,8279`** | `0,1060` | **Puncak kemacetan logistik / gelombang telat** — model sangat tajam menangkap krisis! |
| **Fold 4** | `53.437` | `8.316` | `10,04%` | `0,2846` | `0,6870` | `0,0821` | Musim kembali tenang normal (`10%`), kalibrasi paling stabil (`0,0821`) |
| **Rata-Rata 4 Fold** | — | — | — | **`0,3825`** `[0,302–0,507]` | **`0,7130`** `[0,669–0,770]` | **`0,0902`** | Unggul atas rata-rata `LogisticRegression` (`PR-AUC 0,3554`, `Brier 0,0940`) |

**[KALIMAT YANG DIUCAPKAN]:**  
"Sekarang lihat pembahasan terkait—**evaluasi per lipatan waktu dari hasil Temporal CV**. Ini adalah contoh nyata mengapa kita tidak boleh hanya melaporkan satu angka rata-rata lalu pulang!

Perhatikan perubahan dari Fold 1 hingga Fold 4:  
Di **Fold 1**, data latih baru 3.683 baris sehingga PR-AUC baru `0,2308`. Begitu bertambah di **Fold 2**, naik ke `0,3729`.  
Lalu lihat keajaiban di **Fold 3**: gelombang keterlambatan logistik membuat tingkat ulasan negatif dunia nyata melonjak hampir dua kali lipat menjadi **`19,98%`**—dan di masa krisis itu, model LightGBM kita bersinar sangat tajam dengan **`PR-AUC 0,6417` dan `ROC-AUC 0,8279`**!  
Kemudian di **Fold 4**, gelombang macet mereda kembali ke pola normal `10,04%`, dan PR-AUC ikut menormal ke **`0,2846`**, mendekati angka **Locked Test** kita (`0,3061`–`0,3151`)!  
Dari sinilah seorang *Data Scientist* belajar satu hukum penting: performa PR-AUC sangat dipengaruhi *regime shift* (perubahan musim & tingkat masalah di lapangan), bukan sekadar jumlah pohon algoritma."

---


## BABAK 10: BATAS SINYAL TAHAP CHECKOUT, PENOLAKAN `REPEAT PURCHASE`, *MANSKI BOUNDS*, & PEMETAAN TIGA POROS EVALUASI
*(Alokasi waktu: 4 menit · Slide 41–44)*

**[SLIDE 41–42 | VISUAL LAYAR]**  
*Dua Temuan Batas Prediktif Model:*  
1. **Model Prediksi Dini Saat Checkout:**  
   - Pengujian terkunci pada `N = 12.571`: **`PR-AUC = 0,1335`** (`95% CI [0,1220–0,1480]`), **`ROC-AUC = 0,5468`**, Brier mentah `0,2370` → terbatas sebagai indikator awal semata.  
   - **Makna Empiris:** Rendahnya skor di tahap checkout memperlihatkan pemisahan fitur waktu berjalan bersih tanpa kebocoran informasi kurir masa depan. Pada titik pembayaran, perjalanan pengiriman belum dimulai sehingga sinyal penentu kepuasan belum terbentuk. Selisih **`+0,1726` PR-AUC** dibandingkan model pasca-pengiriman **pasca-pengiriman (`0,3061`)** mengukur kontribusi nyata pengalaman kurir.  
2. **Model Pembelian Ulang 90 Hari (*Temuan Negatif yang Sah*):**  
   - **Kontrak Checkout** (`N_test = 13.175`): **`ROC-AUC = 0,5021`** (`95% CI [0,472–0,531]`, `PR-AUC = 0,0202` vs base rate `0,0237`).  
   - **Kontrak Pasca-Pengiriman** (`N_test = 4.232`, pasca-eksklusi `962` *pre-delivery repeaters* & *90 hari right-censoring*): **`ROC-AUC = 0,5284`** (`95% CI [0,491–0,564]`, `PR-AUC = 0,0245` vs baseline `0,0201`).  
   - Kedua interval kepercayaan 95% melintasi batas acak `0,50`, sehingga model ditetapkan berstatus ditolak dari operasional.

**[KALIMAT YANG DIUCAPKAN]:**  
"Dalam penelitian *Data Science* yang objektif, hasil eksperimen tidak selalu berakhir dengan angka tinggi—dan justru pengujian batas kegagalan itulah yang menunjukkan ketelitian metodologi.

Pertama, pada **Model Tahap Pembayaran (Checkout)** di Slide terkait: saat fitur dibatasi murni ke sepuluh atribut kasir sebelum kurir menerima paket, model mencatat **`PR-AUC 0,1335`** dan **`ROC-AUC 0,5468`** pada `12.571` data uji. Mengapa jauh lebih rendah dari **`0,3061`** pada tahap pasca-pengiriman? Karena pada detik pembeli membayar, keterlambatan fisik memang belum terjadi. Perbedaan **`+0,1726` PR-AUC** itulah porsi risiko yang sepenuhnya berasal dari realitas perjalanan kurir. Oleh karena itu, model checkout hanya diposisikan sebagai pemeringkat risiko awal terbatas sebagai indikator awal semata.

Kedua, pada **Model Pembelian Ulang 90 Hari (*Repeat Purchase*)** di Slide terkait: setelah `962` pelanggan yang terlanjur beli sebelum paket pertamanya tiba dikeluarkan dan efek pemotongan waktu 90 hari (*right-censoring*) dikontrol, kedua varian model menghasilkan **`ROC-AUC 0,5021`** dan **`0,5284`**, dengan interval kepercayaan 95% menyentuh angka **`0,50`**. Dengan struktur data Olist di mana ~97% transaksi berasal dari pembeli satu kali dan tanpa rekam jejak perilaku klik aplikasi maupun riwayat promosi, tidak ada dasar ilmiah untuk mendorong model ini ke operasional. Penolakan tersebut didokumentasikan secara sah sebagai **`Temuan Negatif yang Sah`** (berhenti di tahap riset)."

**[SLIDE 43–44 | VISUAL LAYAR]**  
*Analisis Bias Non-Respons (**Manski Selection Bounds**) & **Pemetaan Tiga Poros Evaluasi Antar-Model**:*  
- **Manski Bounds (`646` Transaksi Tanpa Ulasan = `0,67%` dari `96.478`):** Batas bawah optimistis (*asumsi seluruh non-respons puas*) **`11,44%`** vs batas atas pesimistis (*asumsi seluruh non-respons memberi bintang 1*) **`12,10%`** → lebar ketidakpastian hanya **`<= 0,59%`**.  
- **Pemetaan Lima Dimensi Benchmark:**  
  1. **Kalibrasi Probabilitas:** Pembobotan seimbang meningkatkan Brier mentah ke `0,1375`, namun *Platt Scaling* memulihkannya ke **`0,0762`** (`ECE 0,0070`).  
  2. **Kelayakan Retensi:** Interval kepercayaan melintasi `0,50` → pembatasan status berhenti pada tahap riset.  
  3. **Populasi Tabular vs Teks:** `LightGBM` menguji seluruh pesanan (`N=12.571`, base `9,63%`, `PR-AUC 0,3061`), sementara `TextBiLSTM` khusus komentar tertulis (`N=4.142`, base `16,2%`, `PR-AUC 0,3120`).  
  4. **Tiga Horizon Waktu:** *Locked Holdout* `> Jun 18` (`N=12.571` → `0,6745`), *4-Fold CV Locked* `Jul–Agu 18` (`N=12.448` → `0,6975`), dan *Slice Holdout* `>= Mar 18` (`N=38.942` → `0,7517`).  
  5. **Batas Tahap Fitur:** saat checkout (`0,1335`) memakai 10 atribut checkout, sedangkan pasca-pengiriman (`0,3061`) memakai 15 atribut pasca-pengiriman.

**[KALIMAT YANG DIUCAPKAN]:**  
"Selanjutnya pada bagian tersebut, kami mengukur seberapa jauh `646` transaksi tanpa ulasan dapat memengaruhi tingkat keluhan agregat menggunakan **Manski Selection Bounds** (*menghitung batas ekstrem teroptimistis vs terpesimistis tanpa mengarang asumsi distribusi*). Hasilnya menunjukkan rentang sempit antara **`11,44%` hingga `12,10%`** (lebar interval `<= 0,59%`), sehingga keabsahan distribusi target tetap kokoh.

Pada bagian tersebut, seluruh tolok ukur proyek dipetakan secara konsisten ke tiga sumbu utamanya: populasi sampel, tahap ketersediaan fitur, dan horizon tanggal uji. Perbedaan antara `ROC-AUC 0,6745` (`> Jun 2018`), `0,6975` (`CV Locked`), dan `0,7517` (`>= Mar 2018`), maupun `PR-AUC 0,3061` (tabular umum) terhadap `0,3120` (subset teks komentar tertulis), mencerminkan definisi cakupan data masing-masing eksperimen yang berbeda."

---

## BABAK 11: KALIBRASI *PLATT SCALING*, *BRIER SKILL SCORE*, *DECISION CURVE ANALYSIS* (`DCA`), & *TOP-K LIFT*
*(Alokasi waktu: 4,5 menit · Slide 45–46)*

**[SLIDE 45 | VISUAL LAYAR]**  
*Kalibrasi Probabilitas (**`Platt Scaling`**) & Evaluasi Kuantil Error Regresi (evaluasi kuantil residual & evaluasi residual regresi):*  
- **Masalah Klasifikasi:** Dilatih dengan `class_weight="balanced"`, output probabilitas mentah LightGBM membengkak ke rata-rata **`33,12%`** saat realita hanya **`9,63%`**! *(Analogi: aplikasi ramalan cuaca yang cenderung melaporkan 70% hujan padahal kenyataan hanya turun hujan 20%.)*  
- **Solusi **`Platt Scaling`** (`logit calibration` fit strictly on Validation, **`coef = 0,9020`**, **`intercept = -1,8089`**):**  
  - **Brier Score:** `0,1375` → **`0,0762`** (**membaik `44,59%`**, mengungguli tebakan konstan `0,0870`–`0,0985`!)  
  - **ECE (*Expected Calibration Error* 10-bin):** `0,2355` → **`0,0070`** (**error persentase turun `97,02%`**, tinggal meleset **`0,70%`**!)  
  - **Brier Skill Score (`BSS`):** **`+0,1215`** *(+12,15% keterampilan melampaui tebakan probabilitas tetap!)*.  
- **Evaluasi Operasional Regresi Delay (`DeliveryDelayOperationalImpact`):** Karena error logistik punya ekor berat (*heavy right tail* saat mogok kurir/cuaca buruk), kerangka evaluasi kuantil residual memetakan distribusi kuantil sisaan (**`p50`, `p90`, `p99`**) serta persentase paket tepat dalam toleransi **`<= 1 hari`**, **`<= 3 hari`**, dan error ekstrem **`> 7 hari`**—lalu `Model Card Delay` mewajibkan **margin penyangga `+3 hari`** saat memberi estimasi ke pelanggan!

**[KALIMAT YANG DIUCAPKAN]:**  
"Dua slide di Babak 11 ini (Slide 45–46) adalah pembeda antara tugas kuliah ML dan **standar industri siap uang**: jangan pernah langsung memakai angka probabilitas mentah dari `predict_proba()` yang dilatih dengan `class_weight="balanced"`!

Pada tahap kalibrasi ini, karena LightGBM diberi penalti keseimbangan kelas agar peka pada keluhan langka, rata-rata tebakannya membengkak menjadi **`33,12%`**, padahal kejadian nyatanya di lapangan cuma **`9,63%`**. Itu seperti aplikasi cuaca yang cenderung melaporkan *'80% hujan badai'* setiap pagi—lama-lama kalibrasi probabilitas menjadi bias!  
Dengan memasang **`Platt Scaling`** (pelurus *log-odds* regresi logistik yang dilatih **hanya pada data validasi**; `coef=0,9020, intercept=-1,8089`), **`Expected Calibration Error (ECE)` rontok `97,02%`** sampai tinggal meleset **`0,70%`**, dan **`Brier Skill Score`** positif **`+0,1215`**—artinya saat model bilang risiko 20%, memang sekitar 20 dari 100 paket itu bermasalah!  
Dan untuk model regresi `delivery_delay_days`, selain memantau rata-rata MAE `4,83 hari`, kerangka `DeliveryDelayOperationalImpact` mengecek ekor ekstrem (`p90/p99` & error `> 7 hari`), sehingga `Model Card` menetapkan aturan aman: tambahkan **penyangga `+3 hari`** dalam komunikasi estimasi ke konsumen saat cuaca/kurir bermasalah."

**[SLIDE 46 · BAGIAN A | VISUAL LAYAR]**  
***Decision Curve Analysis (`DCA` — Net Benefit)* (modul analisis survival & DCA & hasil Temporal CV):**  
- **Rumus *Net Benefit*:** $\text{Net Benefit}(p_t) = \frac{\text{TP}}{N} - \frac{\text{FP}}{N} \cdot \left(\frac{p_t}{1 - p_t}\right)$  
- **Arti Sederhana (*Analogi Dokter Mengobati Pasien*):** Di dunia nyata, memilih siapa yang diberi tindakan CS punya dua alternatif ekstrem tanpa AI: **"Tangani Semua Pesanan (*Treat All*)"** atau **"Jangan Tangani Siapa Pun (*Treat None*, Net Benefit = 0)"**.  
- **Bukti Empiris hasil Temporal CV:**  
  - Pada ambang risiko $p_t = 0,06$: **Model CSIP = `+0,0419`** vs *Treat All* = `+0,0384` *(mulai mengungguli tangani semua!)*.  
  - Pada ambang $p_t = 0,08$: **Model CSIP = `+0,0321`** vs *Treat All* = `+0,0175` *(nyaris 2× lebih untung!)*.  
  - Pada ambang **$p_t = 0,10$**: **Model CSIP = `+0,0284`** sementara ***Treat All* anjlok rugi ke `-0,0044`**!

**[KALIMAT YANG DIUCAPKAN]:**  
"Begitu peluang modelnya sudah lurus terkalibrasi, pada kurva utilitas keputusan kita membuktikan manfaat bersihnya melalui **Decision Curve Analysis (`DCA`)**—metode evaluasi yang lahir dari riset kedokteran klinis untuk menjawab satu pertanyaan brutal: *'Apakah memakai model AI ini benar-benar memberi keuntungan bersih dibanding tidak usah pakai model sama sekali?'*

Tanpa model, manajer cuma punya dua opsi ekstrem: **`Treat None`** (tidak menyapa siapa pun, untung bersih = `0`) atau **`Treat All`** (memberi voucher/telepon CS ke semua paket). Lihat angka dari hasil Temporal CV: pada batas kehati-hatian **`p_t = 0,10` (10%)**, kalau perusahaan nekat menyapa semua pesanan (`Treat All`), biaya salah sasaran menghancurkan keuntungan menjadi **`-0,0044` (rugi bersih!)**. Sebaliknya, memakai saringan model CSIP tetap menjaga **keuntungan bersih positif `+0,0284`**!"

**[SLIDE 46 · BAGIAN B | VISUAL LAYAR]**  
*Ketajaman Peringkat Operasional (**Top-K Lift** — hasil Temporal CV):*  
Seberapa kali lebih banyak keluhan nyata tertangkap jika tim hanya menindak urutan skor risiko tertinggi model dibanding menelpon acak?  
- **Top `5%` Paling Berisiko:** **`Lift = 5,154×`** *(setiap 100 panggilan di top 5% menemukan **5× lebih banyak** keluhan asli dibanding acak!)*  
- **Top `10%` Paling Berisiko:** **`Lift = 3,556×`**  
- **Top `20%` Paling Berisiko:** **`Lift = 2,346×`**

**[KALIMAT YANG DIUCAPKAN]:**  
"Dan pada analisis *Top-K Lift*, bagi kepala kapasitas seleksi yang bertanya, *'Kapasitas harian terbatas hanya untuk mengevaluasi 5% atau 10% pesanan paling rawan—seberapa besar penghematan tenaga yang diberikan model Anda?'*  
Jawabannya ada pada **`Top-K Lift`** di hasil Temporal CV: jika staf mengambil acak 5% pesanan, mereka hanya menemukan `~9,6%` keluhan. Tetapi jika mereka menelpon **Top 5% teratas hasil urutan skor CSIP**, konsentrasi pelanggan yang benar-benar akan kecewa melesat **`5,154 kali lipat`** (`3,556×` di Top 10% dan `2,346×` di Top 20%)!"

---

## BABAK 12: MEMBUKA OTAK MODEL DENGAN *SHAP TREEEXPLAINER* (ASOSIASI MODEL VS UJI KAUSAL) & AUDIT SUBKELOMPOK (*SLICE ROBUSTNESS*)
*(Alokasi waktu: 4 menit · Slide 47–49)*

**[SLIDE 47 | VISUAL LAYAR]**  
*Peringkat Pendorong Internal Model LightGBM Pasca-Pengiriman (**`SHAP TreeExplainer`**, `800` sampel acak terkendali, hasil SHAP TreeExplainer):*  
1. `delivery_delay_days`: `Mean |SHAP| = 0,3058`  
2. `delivery_lead_time_days`: `Mean |SHAP| = 0,2252`  
3. `item_count`: `Mean |SHAP| = 0,2086`  
4. `estimated_lead_time_days`: `Mean |SHAP| = 0,0740`  
5. `total_freight`: `Mean |SHAP| = 0,0701` · disusul `distance_x_weight` (`0,0665`), `payment_installments_max` (`0,0424`), `seller_buyer_distance_km` (`0,0410`), `approval_lag_hours` (`0,0298`), `freight_ratio` (`0,0277`), sedangkan `is_late = 0,0`.  
*(Penjelasan Sederhana: **SHAP** ibarat akuntan pembagi jasa yang adil—menghitung persis berapa besar dorongan tiap fitur menggeser skor keputusan model. Status klaim dibatasi pada **asosiasi observasional (Prediktif/Asosiasional)**, BUKAN sebab-akibat kausal **bukti kausal eksperimental** tanpa eksperimen acak!)*

**[KALIMAT YANG DIUCAPKAN]:**  
"Pohon gradient boosting yang terdiri dari `150` pohon sering dicap sebagai 'kotak hitam' (*black box*). Pada interpretasi fitur ini, kami membukanya memakai **`SHAP TreeExplainer`** (*Shapley Additive Explanations*) atas `800` sampel terkendali.

Analogi SHAP sangat sederhana: bayangkan empat pemain sepak bola bekerja sama memenangkan pertandingan; SHAP bekerja sebagai **akuntan teori permainan kooperatif** yang membagi persis berapa poin kontribusi masing-masing fitur untuk menaikkan atau menurunkan skor risiko tiap pesanan.  
Terlihat tiga pendorong puncak secara transparan: **`delivery_delay_days` (`0,3058`)**, panjang total waktu kirim **`delivery_lead_time_days` (`0,2252`)**, dan banyaknya jenis barang dalam satu kardus **`item_count` (`0,2086`)**.

Perhatikan juga dua poin penting pada interpretasi ini:  
1. Mengapa **`is_late`** nilainya tepat **`0,0`**? Karena kolom kontinu `delivery_delay_days` sudah membawa 100% informasi biner telat/tidak ditambah resolusi berapa harinya, sehingga pohon LightGBM selalu memilih membelah pada fitur kontinu yang lebih informatif!  
2. Kami tegaskan batas klaim **asosiasi di dalam model versus pembuktian kausal**: SHAP menjelaskan *bagaimana model menimbang korelasi di data masa lalu* (asosiasi dalam model), **bukan bukti sebab-akibat mutlak (kausal eksperimental)** layaknya payung dan hujan yang muncul bersamaan!"

**[SLIDE 48–49 | VISUAL LAYAR]**  
*Audit Keadilan & Batas Pakai Model pada Subkelompok (**Slice Robustness Analysis**, evaluasi subkelompok, Holdout sejak `2018-03-01`, `N = 38.942` / `39.153`):*

| Dimensi Irisan (*Slice*) | Subkelompok | Jumlah Sampel | Prevalensi Komplain | ROC-AUC *(Klasifikasi)* | MAE & Bias *(Regresi Delay)* | Temuan Diagnostik Penting |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Keseluruhan** | Nasional Holdout | `38.942` | — | **`0,7517`** | **`MAE 5,60 hari`** | Syarat uji tiap sel minimal `> 50` baris & 2 kelas muncul |
| **Geografis** | **Rio de Janeiro (`RJ`)** | `4.570` | **`16,89%`** | **`0,8031`** | **`MAE 7,72 hari`** *(bias `+1,33`)* | Klasifikasi paling tajam di wilayah konflik, tapi **error delay tertinggi!** |
| **Geografis** | **São Paulo (`SP`)** | `17.649` | `10,24%` | `0,7013` | **`MAE 4,25 hari`** *(bias `+1,64`)* | Prediksi waktu tiba jauh lebih presisi di pusat logistik utama |
| **Geografis** | `RS` / `MG` / `PR` | `2.002 / 4.416 / 1.997` | `11,64% / 12,68% / 10,72%` | `0,7749 / 0,7400 / 0,6977` | `6,38 / 5,95 / 5,58 hari` | Konsisten `>= 0,70` di seluruh wilayah utama |
| **Nilai Keranjang** | **Tinggi (`> BRL 150`)** | `12.978` | `14,93%` | **`0,7700`** | — | Paling akurat pada transaksi bernilai uang paling besar (`Low: 0,7234`) |
| **Status Tiba** | **Paket Tepat Waktu** | `35.578` | `8,84%` | **`0,6522`** | — | Bukti model bukan cuma aturan biner sederhana ('telat = ulasan buruk'), tetap mendeteksi friksi lain! |
| **Status Tiba** | **Paket Terlambat** | `3.364` | **`48,96%`** | **`0,8383`** | — | Nyaris 1 dari 2 paket telat berujung kecewa; diskriminasi derajat telat sangat tajam! |

*Batas Operasional Wajib (analisis slice): Model tidak dikalibrasi untuk pesanan ekstrem di bawah **`BRL 10`** maupun di atas **`BRL 5.000`** karena dukungan sampel latih terlalu tipis di ekor distribusi.*

**[KALIMAT YANG DIUCAPKAN]:**  
"Dalam evaluasi model profesional pada evaluasi subkelompok, skor rata-rata nasional saja bisa menjadi topeng berbahaya! Bisa saja model kita cemerlang di ibu kota namun gagal total di daerah, atau cuma menghafal aturan malas *'telat = marah'*.

Melalui **`Slice Robustness Analysis`** di evaluasi subkelompok, kami mengiris holdout pasca-Maret 2018 ke **tiga sumbu keadilan & stres**:  
1. **Bukti model bekerja pada paket Tepat Waktu (`On-Time`):** Ketika `3.364` paket telat dibuang dan kita uji **khusus pada `35.578` paket yang datang tepat waktu**, `ROC-AUC` model tetap bertahan di **`0,6522`**—membuktikan ia bukan sekadar aturan biner sederhana keterlambatan, melainkan sungguh mendeteksi kekecewaan akibat `item_count` banyak barang maupun tunggu mutlak (`delivery_lead_time_days`) yang terlalu panjang! Sedangkan pada paket telat (`48,96%` kecewa), ketajamannya menembus **`0,8383`**.  
2. **Audit Disparitas Wilayah:** Pada regresi waktu tiba, rute lokal pusat industri **São Paulo (`SP`)** meleset hanya **`4,25 hari`**, sedangkan pengiriman ke **Rio de Janeiro (`RJ`)** melebar menjadi **`7,72 hari`**. Transparansi ini plus pengakuan jujur bahwa ekor harga ekstrem (`< R$ 10` dan `> R$ 5.000`) belum terkalibrasi mencegah penyalahgunaan model di luar batas kompetensinya!"


---

# BAGIAN 06 — STATISTIKA INFERENSIAL, KEPUTUSAN & SIMULASI (SLIDE 50–57)

## BABAK 13: ENAM HIPOTESIS TERPRA-REGISTRASI (DENGAN KOREKSI *FDR*) — PENOLAKAN HUBUNGAN RATING–RETENSI & EFEK *CONFOUNDER*
*(Alokasi waktu: 3,5 menit · Slide 50–52)*

**[SLIDE 50–52 | VISUAL LAYAR]**  
*Uji Hipotesis Statistik Terkontrol (`hypothesis_forest_plot.png` — Uji Praregistrasi dengan koreksi uji ganda **`FDR Adjustment`**):*

| Kode | Hipotesis *(Pernyataan Uji)* | Metode Statistik *(Arti Sederhana)* | Hasil Empiris & Interval 95% | Status & Pelajaran DS |
| :---: | :--- | :--- | :--- | :---: |
| **1. Rasio Ongkir** | Rasio ongkir (`freight_ratio`) berasosiasi negatif dengan kepuasan | *OLS Multiple Regression* *(regresi linier ganda menahan jumlah item & harga konstan)* | `t = -11,858`, `p_adj = 6,17e-32`, efek `-0,2068` `[-0,241; -0,173]` | **Didukung** *(Observasional)* |
| **2. Asimetri Durasi** | Telat kirim menurunkan kepuasan jauh lebih tajam vs datang lebih cepat | *Piecewise Spline & Wald Test* *(uji patahan kemiringan kurva sebelum vs sesudah SLA)* | `F = 1657,035`, `p = 0,0`, efek `-0,0661` `[-0,068; -0,064]` | **Didukung** *(Observasional)* |
| **3. Rating -> Retensi** | Pengalaman kirim & rating order pertama memicu *repeat purchase* | *Logistic Odds Ratio* *(rasio peluang beli ulang)* | `z = -0,175`, **`p_adj = 0,8609`**, **OR = `0,9964`** `[0,957; 1,037]` | **Ditolak** *(Statistik — bintang 5 `2,27%` vs bintang 1 `2,29%`)* |
| **4. Sensitivitas Segmen** | Sensitivitas ongkir & delay berbeda antar segmen perilaku | *Moderated ANOVA Interaction* *(uji interaksi beda reaksi antar klaster)* | `F = 29,381`, `p_adj = 3,51e-13`, `[23,51; 35,26]` | **Didukung** *(Observasional)* |
| **5. Nilai Tambah Pengiriman** | Gabungan fitur ekonomi + pengiriman menaikkan *PR-AUC* dibanding ekonomi saja | *Out-of-Time Predictive Ablation* | `Delta PR-AUC = +0,1401` `[0,119; 0,161]`, `p_adj = 0,00012` | **Didukung** *(Prediktif)* |
| **6. Efek Confounder** | Hubungan nilai belanja & retensi terjelaskan oleh **Confounder** *(lokasi & basket)* | *Confounder Attenuation OLS* *(mengukur susutnya koefisien setelah faktor pengacau masuk)* | `t = -4,729`, `p_adj = 3,39e-06`, menyusut **`47,3%`** `[42,6; 52,0]` | **Didukung** *(Dengan Kontrol Confounder)* |

**[KALIMAT YANG DIUCAPKAN]:**  
"Selain membangun model prediksi, *Data Scientist* wajib menguji dugaan bisnis lewat **statistika inferensial terpra-registrasi**. Mengapa keenam hipotesis statistik dirumuskan dan ditetapkan sejak awal sebelum pengolahan hasil? Untuk mencegah **HARKing** (*mengarang hipotesis setelah melihat hasil akhir*). Dan mengapa seluruh *p-value* dikoreksi dengan **FDR Adjustment (*False Discovery Rate*)**? Agar saat menguji banyak dugaan sekaligus, kita tidak tertipu oleh kebetulan acak!

Dua temuan paling penting bagi pengambil keputusan ada pada **Uji 3 (Rating vs Retensi)** dan **Uji 6 (Variabel Pengacau)**:  
- Pada **Uji 3**, asumsi populer tim pemasaran menyatakan pelanggan bintang 5 pasti lebih sering belanja ulang. Faktanya di Olist, rasio peluangnya (**Odds Ratio**) adalah **`0,9964`** dengan `p_adj = 0,8609`—artinya ditolak tegas secara statistik!
- Pada **Uji 6**, kami menguji **Confounder**—yaitu variabel pengacau pihak ketiga yang menggerakkan dua hal sekaligus, persis seperti penjualan es krim yang sering naik bareng kasus orang tenggelam karena faktor ketiga yaitu *musim panas yang terik*! Setelah kami mengontrol faktor pengacau provinsi tempat tinggal dan komposisi keranjang, tampak hubungan nilai belanja dan retensi menyusut **47,3%**."

---

## BABAK 14: DARI EVALUASI MODEL KE KEPUTUSAN — MATRIKS BIAYA ASIMETRIS (`$45 VS $5`), KUOTA CS, UJI A/B `80/20` & SIMULASI *WORLD MODEL* ENAM SKENARIO KONTRAFAKTUAL
*(Alokasi waktu: 5 menit · Slide 53–57)*

**[SLIDE 53–54 | VISUAL LAYAR]**  
*Menghubungkan Skor Model Terkalibrasi ke Ekonomi Bisnis Nyata (kerangka *Cost-Sensitive Classification* di `src/csip/decision_engine/`):*  
1. **Matriks Biaya Asimetris (`README.md`):**  
   - Biaya salah tebak positif palsu (*False Positive*, $C_{FP}$): **\$5,00** *(menyapa/kompensasi pelanggan yang sebenarnya baik-baik saja)*.  
   - Biaya melewatkan keluhan mahal (*False Negative*, $C_{FN}$): **\$45,00** *(kehilangan pelanggan hingga kabur — 9× lebih mahal!)*.  
   - Titik potong ambang klasifikasi optimal matematis bergeser dari default buku teks `0,50` ke **`τ* = 0,18`** (**`4,2×`** lebih efisien secara biaya!).  
2. **Penyelaras Kapasitas Nyata (`calibrate_thresholds_from_capacity`):** Menjaga agar kapasitas seleksi hanya menerima antrean sesuai kapasitas manusia (*anti-**Alert Fatigue***), mengurutkan prioritas `CRITICAL > HIGH > MEDIUM > LOW` dalam kontrak rekomendasi `12` atribut.  
3. **Menutup Jarak dari Asosiasi ke Bukti Kausal (`design_ab_holdout_plan`):** Otomatis memecah target intervensi menjadi **`80%` Treatment vs `20%` Control Holdout** agar dampak nyata diukur secara kausal.

**[KALIMAT YANG DIUCAPKAN]:**  
"Banyak presentasi berhenti pada grafik SHAP lalu bingung saat diterjemahkan menjadi aturan keputusan: *'Terus, pada peluang berapa sistem intervensi harus menekan tombol kirim voucher?'* Pada optimasi ambang berbasis biaya, **kerangka *Cost-Sensitive Classification*** menerjemahkan probabilitas terkalibrasi menjadi ekonomi keputusan!

Lihat ketidakseimbangan biaya bisnis nyata di **Matriks Biaya Asimetris**: kalau model salah menduga orang baik-baik lalu mengirim kupon sapaan (`False Positive`), kerugiannya hanya **\$5**. Tetapi jika model gagal mendeteksi pelanggan berisiko tinggi sampai ia meledak pergi permanen (`False Negative`), nilainya **\$45**—sembilan kali lebih mahal!  
Jika kita malas memakai titik potong buku teks `0,50`, kita membiarkan terlalu banyak keluhan berharga \$45 lolos. Melalui optimasi biaya harapan, titik potong geser optimal turun ke **`0,18` (`18%`)**, menghasilkan efisiensi **`4,2×`** lebih baik dibanding aturan bawaan `0,50`! Lebih realistis lagi, `calibrate_thresholds_from_capacity` menjaga jumlah tiket di bawah kapasitas penanganan supaya tidak terjadi **Alert Fatigue (*kewalahan alarm palsu*)**, dan `design_ab_holdout_plan` otomatis menyisihkan **20% kelompok pembanding acak** agar efek sebab-akibat **bukti kausal eksperimental** diuji di lapangan."

**[SLIDE 55–57 | VISUAL LAYAR]**  
*Simulasi Kebijakan Kontrafaktual 12 Minggu dengan **World Model `VAR(1)`** & **Residual Bootstrapping `B = 300×`** (`scenario_simulations.png`):*

| Skenario Kebijakan | Parameter Intervensi | Order 12 Minggu | Laju Ulasan Buruk | Biaya Subsidi | Saldo Simulasi | Guardrail Ekstrapolasi |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Skenario Baseline Historis** | Tren alamiah | `9.198` | `19,34%` | `R$ 0` | `R$ 0` | **PASS** (Dalam Batas Historis) |
| **Subsidi Ongkir Merata** | `-15%` ongkir **semua** order | `9.584` (`+386`) | `16,90%` (`-2,44 pp`) | **`R$ 33.544`** | **`-R$ 24.323,36`** | **PASS** (Dalam Batas Historis) |
| **Perbaikan Durasi Kirim** | Pangkas telat `-3,0 hari` | `9.158` (`-40`) | `18,44%` (`-0,90 pp`) | `R$ 10.989,60` | `-R$ 11.943,90` | **PASS** (Dalam Batas Historis) |
| **Subsidi Terarah (Segmen 2)** | `-25%` ongkir **Segmen Friksi saja** | `9.258` (`+60`) | `17,30%` (`-2,04 pp`) | **`R$ 16.664,40`** | `-R$ 15.227,30` | **PASS** ***(Hemat 50,3% biaya vs subsidi merata!)*** |
| **Skenario Shock Ekstrem** | `+20%` ongkir, `+4 hari` delay | `8.728` (`-470`) | **`24,20%`** (`+4,86 pp`) | `R$ 0` | `-R$ 11.218,26` | **`OOD WARN` (`Z=3,68 > 3,5σ` → Peringatan OOD!)** |
| **Intervensi Gabungan** | `-15%` ongkir & `-3 hari` delay | `9.182` (`-16`) | **`15,58%`** (`-3,76 pp`) | `R$ 41.319` | `-R$ 41.681,30` | **PASS** (Dalam Batas Historis) |

**[KALIMAT YANG DIUCAPKAN]:**  
"Lalu pada simulasi skenario makro `VAR(1)`, saat berpindah dari satu pesanan ke kebijakan skala ekosistem 12 minggu ke depan, **`WorldStateTransitionModel` (`VAR(1)`)** menjalankan **enam skenario kebijakan kontrafaktual** yang diguncang **`300` simulasi *Residual Bootstrapping*** (*memutar ulang variasi error historis untuk menggambar sabuk ketidakpastian 90% dan 95%, bukan menebak satu garis kaku*).

Temuan terbesar simulasi ini mematahkan mitos pemasaran konvensional: memberi diskon ongkir `-15%` merata ke semua orang (subsidi merata) memang menaikkan order `+386`, **tetapi biaya subsidinya tembus `R$ 33.544` dan mencatat saldo simulasi `-R$ 24.323`** karena mayoritas subsidi terbuang mensubsidi *Segmen 1* yang aslinya sudah puas tanpa diskon!  
Sebaliknya, ketika kebijakan disambungkan ke temuan **K-Means Segmen 2** (*High-Friction Multi-Item*) pada skenario **Subsidi Terarah**, **pengeluaran subsidi langsung terpangkas separuh (`-50,3%`, tinggal `R$ 16.664`)** sambil tetap mempertahankan `83,6%` penurunan keluhan!  
Dan lihat pagar kejujuran pada skenario **Shock Ekstrem**: saat skenario krisis memaksa lonjakan `+4 hari` dan `+20%` ongkir hingga **`Z_max = 3,68`** di luar pagar **`3,5 sigma`**, **`Extrapolation Guardrails`** langsung menyalakan peringatan **`OOD (Out-of-Distribution)`**—artinya *di luar peta sejarah yang pernah dipelajari model*—dan menurunkan klaim bukti menjadi **Peringatan Ekstrapolasi (Out-of-Distribution)**."

---

# BAGIAN 07 — MONITORING DRIFT, GENERALISASI & REPRODUKSI EKSPERIMEN (SLIDE 58–66)

## BABAK 15: MEMANTAU MODEL BERKALA — OBSERVATORIUM *CONCEPT DRIFT* & *CHAMPION–CHALLENGER*
*(Alokasi waktu: 3,5 menit · Slide 58–60)*

**[SLIDE 58–60 | VISUAL LAYAR]**  
*Empat Radar Statistik di **`DriftEngine`** (monitoring pergeseran distribusi) & Gerbang Pergantian Model (Seleksi *Champion–Challenger*):*  
- **Radar Input (*Covariate Shift* — perubahan ciri pesanan masuk vs zaman latihan):**  
  1. **`PSI` (*Population Stability Index* — 10 kuantil + *Laplace Smoothing* $10^{-4}$):** Hijau `< 0,10` (`STABLE`), Kuning `0,10–0,25` (`WARNING`), Merah **`>= 0,25` (`CRITICAL_DRIFT`)**.  
  2. **`Kolmogorov-Smirnov` (`KS`, $\alpha = 0,05$):** Uji beda kurva kumulatif secara statistik.  
  3. **`Wasserstein-1` (*Earth Mover's Distance*):** Jarak geser nyata dalam **satuan asli** (hari / BRL)—melindungi dari alarm semu uji KS pada sampel besar!  
- **Radar Output (*Prediction Drift*):** **`Jensen-Shannon Divergence` (`JSD`)** — mengawasi pergeseran sebaran probabilitas prediksi bahkan sebelum label bintang ulasan masuk!  
- **Tata Kelola Penggantian Model (*Champion vs Challenger*):** Penantang wajib lolos ambang kelayakan statistik, wajib menang minimal **`+1,0%`** di metrik utama, Brier Score **tidak boleh memburuk $> 5\%$**, riwayat perbandingan metrik dicatat guna menjaga konsistensi serta pemulihan model sebelumnya bila dibutuhkan.

**[KALIMAT YANG DIUCAPKAN]:**  
"Pekerjaan *Data Scientist* tidak selesai di hari model diluncurkan—karena di dunia nyata, perilaku pasar terus berubah sehingga model mengalami **Covariate Shift** (*profil input hari ini bergeser dibanding zaman latihan*) dan **Concept Decay** (*pola hubungan lama melemah*).

Di `DriftEngine`, kami memasang empat radar komplementer: **PSI** (barometer perubahan komposisi kuantil yang diberi pelicin *Laplace smoothing* agar aman dari pembagian nol; batas merah `>= 0,25`), uji statistik **KS**, jarak praktis **Wasserstein-1** yang melaporkan seberapa jauh pergeseran dalam satuan rupiah atau hari nyata, serta **Jensen-Shannon Divergence (JSD)** untuk mengendus pergeseran skor output bahkan sebelum label ulasan terlambat datang! Ketika model baru (*Challenger*) dilatih ulang, protokol seleksi tidak mengganti model *Champion* aktif kecuali ia menang minimal `+1%` tanpa merusak kalibrasi Brier lebih dari `5%`, dan menjaga jejak evaluasi antargenerasi model."

---

## BABAK 16: GENERALISASI PIPELINE DATA SCIENCE KE DATASET BARU & EMPAT LENSA DIAGNOSTIK
*(Alokasi waktu: 3–4 menit · Slide 61)*

**[SLIDE 61 | VISUAL LAYAR]**  
*Alur Pipeline ML Otomatis tanpa Bocoran Data (`train_fluent_ml_pipeline()` di pipeline generik lintas dataset & `SemanticProfiler`):*  
`Raw Dataset CSV Baru` → **`1. SemanticProfiler & Scale Normalization`** (`1–5` → `0–100`) → **`2. detect_split_strategy()`** *(pemindai otomatis risiko kebocoran tanggal/waktu & ID grup)* → **`3. Split-Before-Transform` Model Shootout** *(Mode EDA vs Regresi `Ridge` vs Klasifikasi `Logistic` vs `Random Forest`)* → **`4. Analisa Respon & Stabilitas`**: Kurva **Tipping Point** ($\frac{dy}{dx}$ puncak), Ranking Kontribusi + Korelasi Pearson, Sebaran Strata, & Audit **`PSI`** Langsung!

**[KALIMAT YANG DIUCAPKAN]:**  
"Sekarang muncul pertanyaan alami dari sesama *Data Scientist*: *'Apakah seluruh disiplin anti-kebocoran tadi cuma berlaku untuk kasus toko online Olist ini saja?'*  
Jawabannya tidak. Pada bagian generalisasi pipeline ini, kami merangkum seluruh disiplin metodologi tadi ke dalam mesin ML generik **`train_fluent_ml_pipeline()`** agar mampu melatih dan mengevaluasi dataset tabular baru—baik data e-commerce, data medis (`mg/dL`, `mmHg`), maupun data mutu produksi—tanpa merusak kaidah ilmiah:

1. **Penyaringan & Penyesuaian Skala (`SemanticProfiler`):** Mesin otomatis membuang kolom ID unik yang berbahaya menjadi hafalan (*overfitting*) dan menyelaraskan skala survei `1–5` ke indeks `0–100` dengan `preprocess_intuitive_scales()`.
2. **Detektor Risiko Kebocoran (`detect_split_strategy()`):** Sebelum membelah data, algoritma memindai kolom bertema waktu (`date/time/year/month`) dan identitas entitas (`customer/user/group_id`) untuk memperingatkan perlunya split kronologis atau berbasis grup.
3. **Adu Model Aman (`Split-Before-Transform`):** Bergantung pada tipe target `y`, mesin mengadu model linier (*Ridge / LogisticRegression*) melawan ansambel (*Random Forest*), di mana **`SimpleImputer`** dan **`StandardScaler`** dibungkus ketat dalam `Pipeline` agar hanya memelajari rata-rata dan varians dari partisi *training* saja.
4. **Empat Lensa Diagnostik & Audit PSI Langsung (Tercermin di Kokpit Interaktif Streamlit & Nara):** Keluaran pipeline tidak berhenti pada angka skor tunggal, melainkan otomatis menyusun **Lensa 1 (Kurva Simulasi & *Tipping Point*)** ($\Delta\hat{y}/\Delta x$ puncak), **Lensa 2 (Peringkat Faktor Penentu & Korelasi Pearson)**, **Lensa 3 (Sebaran Kelompok Data)**, dan **Lensa 4 (Observatorium Drift & Stabilitas)**. Pada Lensa 4 ini, sistem membelah data aktif menjadi **60% observasi awal vs 40% observasi terbaru** dan menghitung **PSI**, lalu penasihat strategi *Nara* menyajikan hasilnya secara adaptif — termasuk langsung memunculkan peringatan *'Drift Terdeteksi; disarankan kalibrasi ulang'* apabila pergeseran distribusi melewati ambang batas!"

---


## BABAK 17: REPRODUKSI 14 NOTEBOOKS (`01–14`), MODEL CARDS, & VERIFIKASI INVARIAN STATISTIK
*(Alokasi waktu: 3 menit · Slide 62–64)*

### Peta Riset 14 Jupyter Notebooks (`111` Sel / `51` Sel Kode — Eksekusi Penuh 100%):

| No | Notebook Riset | Fokus Eksperimen & Output Utama |
| :-: | :--- | :--- |
| `01` | `01_business_and_data_understanding` | Formulasi estimand matematis semua tugas pemodelan & profil skema 9 tabel sumber |
| `02` | `02_data_validation_and_cleaning` | Penegakan *grain `order_id`*, pencegahan duplikasi *join*, median GPS, & penghapusan 23 anomali kronologis |
| `03` | `03_exploratory_data_analysis` | Pembuktian asimetri kepuasan pasca-estimasi (`r = -0,334`) & distribusi miring (*heavy-tail*) |
| `04` | `04_feature_engineering_and_construction` | Konstruksi 41 fitur (`freight_ratio`, Haversine, interaksi), pembatasan Saat Bayar / Serah Kurir / Pasca-Tiba, & audit `PSI < 0,10` |
| `05` | `05_behavioral_discovery_unsupervised` | Seleksi jumlah klaster `K-Means` (`k=3..7`), proyeksi `PCA 2D`, stabilitas bootstrap `ARI`, & `4.824` pencilan |
| `06` | `06_hypothesis_investigation` | Pengujian praregistrasi enam hipotesis dengan kontrol `FDR`, penolakan hubungan rating–retensi, & dekomposisi *confounder* (`-47,3%`) |
| `07` | `07_supervised_ml_and_benchmark_lab` | Perbandingan komparasi baseline hingga ensemble pada klasifikasi ulasan, regresi delay, retensi kohort, & ablasi kelompok fitur secara bertahap |
| `08` | `08_neural_network_and_deep_learning` | Evaluasi `TabularEmbeddingMLP` (*Entity Embeddings*) vs `TextBiLSTM` pada teks Portugis |
| `09` | `09_model_evaluation_and_explainability` | Kalibrasi `Platt Scaling`, *Brier Skill Score*, *Decision Curve Analysis*, *Top-K Lift*, & *SHAP TreeExplainer* |
| `10` | `10_system_and_world_modeling` | Estimasi matriks dinamika mingguan `VAR(1)` Ridge (`87` minggu), *Spectral Radius* `0,8412`, & *Synthetic Recovery* |
| `11` | `11_alternative_world_simulation` | Simulasi enam skenario kontrafaktual (subsidi terarah hemat `50,3%` biaya) & deteksi `OOD` pada shock ekstrem (`Z=3,68`) |
| `12` | `12_uncertainty_quantification` | *Moving-Block Bootstrap* (`1.000×`), *Residual Bootstrapping* (`300×`), & *Manski Selection Bounds* |
| `13` | `13_model_review_and_failure_analysis` | *Slice Robustness* geografis/nilai/ketepatan (`On-Time 0,6522`), evaluasi batas saat checkout (`0,1335`), & *Valid Negative* |
| `14` | `14_final_research_report` | Sintesis hasil evaluasi, 7 *Model Cards*, & pemetaan struktur benchmark lintas populasi |

**[KALIMAT YANG DIUCAPKAN]:**  
"Konsistensi ilmiah dalam eksperimen *Data Science* bergantung pada keterulangan penuh proses analisis. Di Slide 62–64, seluruh alur eksperimen didokumentasikan secara kronologis pada **14 *Jupyter Notebooks*** dengan pembagian tanggung jawab yang jernih dari perumusan masalah sampai sintesis keterbatasan, disertai tujuh **Model Cards** yang merinci kondisi sah penggunaan tiap model.

Di luar dokumentasi notebook, pipeline juga dilengkapi serangkaian pemeriksaan invarian statistik otomatis untuk menjaga empat aturan wajib: pertama, memastikan fitur tahap pasca-pengiriman tidak pernah masuk ke himpunan fitur pembayaran tahap checkout serta grain data tetap `1 order_id` dengan `646` nilai kosong `NaN` tanpa imputasi buatan; kedua, menjaga jeda embargo `>= 90 hari` antar-fold CV dan penguncian *holdout* tunggal; ketiga, memverifikasi perbaikan *Brier Score* hasil *Platt Scaling* dan pemulihan parameter `VAR(1)` (`error <= 1,6%`); keempat, menandai model berstatus ditolak dari operasional agar tidak masuk ke jalur pemeringkatan operasional."

---

## BABAK 18: AGENDA RISET LANJUTAN & ANALISIS BIAS INDUKTIF LINTAS ALGORITMA
*(Alokasi waktu: 4 menit · Slide 65–66)*

**[SLIDE 65–66 | VISUAL LAYAR]**  
*Agenda Riset Data Science Lanjutan & Matriks Kesesuaian Sifat Data vs Keluarga Model:*

| Keluarga Algoritma | Asumsi Induktif Utama | Perilaku Teramati pada Data Olist |
| :--- | :--- | :--- |
| **Linear (`Ridge` & `LogReg`)** | Hubungan aditif linier + penalti L2 | Kompetitif pada regresi tahap serah kurir (`MAE 4,75 hari`) dengan 5 atribut rute halus; tertinggal pada interaksi non-linier tahap pasca-pengiriman (`PR-AUC 0,2436`). |
| **Gaussian Naive Bayes** | Independensi bersyarat & normalitas | Menurun (`PR-AUC 0,1996`) karena asumsi sebaran normal dan kebebasan antarfitur dilanggar oleh distribusi miring (`+6,21`) serta korelasi jarak–ongkir. |
| **KNN (`k=15`) & CART** | Jarak Euclidean lokal vs partisi ambang | KNN stabil setelah standardisasi (`0,2532`), sedangkan pohon tunggal menangkap patahan durasi kirim namun bervarians tinggi (`0,2704`). |
| **RF & LightGBM** | Ensemble pembelahan *axis-aligned* | Invarian terhadap skala fitur dan tajam memotong interaksi ekor panjang (`delay × freight_ratio`), meraih performa tertinggi di tahap pasca-pengiriman (`0,3016` & `0,3061`). |
| **MLP & TextBiLSTM** | Representasi vektor padat & sekuens | `TabularEmbeddingMLP` (`0,2875`) belum melampaui GBDT pada 64 ribu baris terstruktur; `TextBiLSTM` efektif menangkap pola negasi kalimat Portugis (`0,3120`). |
| **VAR(1) Ridge** | Dinamika state-space linier berpenalti | Stabil pada panel pendek 87 minggu tanpa *overfitting* koefisien (`Spectral Radius 0,8412`, `WAPE 15,83%`). |

**[KALIMAT YANG DIUCAPKAN]:**  
"Dua slide menjelang penutup merangkum pelajaran terpenting dari pemodelan enam keluarga algoritma sekaligus arah pengembangan riset selanjutnya.

Pertama pada bagian ini, kami mencatat tiga keterbatasan fitur historis saat ini dan bagaimana memperbaikinya: menambahkan sinyal perilaku sesi pengguna sebelum transaksi (*clickstream*) serta rekam jejak kinerja kurir harian guna mengangkat prediksi tahap pembayaran dan kohort retensi; membangun kalibrator probabilitas bersyarat menurut wilayah negara bagian untuk mempersempit disparitas kesalahan antara pusat logistik São Paulo dan wilayah jarak jauh seperti Rio de Janeiro; serta menghubungkan data eksperimen acak 80/20 menuju pelatihan **Uplift Modeling (CATE)** guna mengestimasi kelompok mana yang benar-benar berubah responsnya oleh intervensi, bukan sekadar memprediksi siapa yang berisiko tinggi.

Kedua pada bagian ini, matriks bias induktif menjawab mengapa tidak ada satu algoritma tunggal yang menang di semua kondisi. Pada regresi tahap serah kurir dengan hanya lima fitur awal, relasi linier ter-regularisasi `Ridge` bekerja sebanding dengan model pohon. Sebaliknya pada klasifikasi tahap pasca-pengiriman, distribusi miring hingga `+6,21` serta interaksi non-linier antara keterlambatan dan rasio ongkir membuat `Gaussian Naive Bayes` melemah sementara `LightGBM` unggul mutlak. Di sisi lain, untuk data teks ulasan tidak terstruktur, pemodelan berurutan `BiLSTM` mampu membaca konteks negasi dua arah secara langsung."

---

# BAGIAN 08 — RINGKASAN CAPAIAN, KONTROL VALIDITAS, & PENUTUP (SLIDE 67–69)

## BABAK 19: REKAPITULASI CAPAIAN, KONTROL VALIDITAS, & PENUTUP
*(Alokasi waktu: 2–3 menit · Slide 67–69)*

**[SLIDE 67–69 | VISUAL LAYAR]**  
- **Skor Empiris Lintas Tugas:** `LightGBM Pasca-Pengiriman PR-AUC 0,3061` (`3,18×` lantai `0,0963`), Kalibrasi Platt `ECE 0,0070` (`-97,02%`), `Top 5% Lift 5,154×`, Regresi Delay Ridge `MAE 4,75 hari`, `TextBiLSTM PR-AUC 0,3120` (`Macro-F1 0,8420`), Segmen Ongkir Tinggi `31,20%` (`ARI 0,9832`), `VAR(1)` `WAPE 15,83%` (`Spectral Radius 0,8412`), & efisiensi stimulus terarah `-50,3%`.
- **Slide terkait:** *Evaluasi yang Jujur Mengukur Batasnya Sendiri.*

**[KALIMAT YANG DIUCAPKAN]:**  
"Sebagai penutup pada tiga slide terakhir, seluruh proyek ini merangkai satu kesimpulan utama: ketepatan pemodelan *Data Science* tidak diukur dari seberapa rumit arsitektur yang dipakai atau seberapa tinggi angka akurasi mentahnya, melainkan dari konsistensi menjaga keabsahan data di sepanjang eksperimen.

Enam prinsip pengendalian yang konsisten dijalankan di sini adalah pemisahan fitur waktu saat bayar, serah kurir, dan pasca-tiba; pemotongan kronologis *Rolling-Origin* dengan embargo 90 hari serta uji *holdout* tunggal; keberanian menandai hasil nol-signifikansi pada *Repeat Purchase* serta uji rating terhadap retensi sebagai temuan negatif; pengukuran ketahanan target lewat batas non-respons *Manski*; pengujian diskriminasi model di luar faktor telat pada irisan tepat waktu (`ROC-AUC 0,6522`); serta pemagaran ekstrapolasi *Out-of-Distribution* pada simulasi kebijakan.

Terima kasih atas perhatian Anda."

---

# LAMPIRAN MATERI: RINGKASAN METRIK & KAMUS ISTILAH MACHINE LEARNING

## Lampiran 1: Kartu Saku Angka Evaluasi Terkunci

* **Dataset & Populasi:** `9` tabel relasional (`>1,5M` baris) → `99.441` pesanan → eksklusi `1.234 unavailable` (`99,0%` tanpa item) → `96.478 delivered` → **`96.470` bersih** (`95.824` ulasan teramati + **`646 NaN`** jujur; `1.000.163 → 19.015` titik GPS median; `23` anomali kronologis dihapus; `814` entri ulasan berulang dibersihkan).
* **Pembatasan Fitur & Validasi:** `41` fitur total (tahap checkout: **10**, tahap serah kurir: **5**, tahap pasca-pengiriman: **15**); Bayesian Target Encoding $\alpha = 10$; stabilitas distribusi fitur `PSI < 0,10` (`0,018–0,048`); **4-Fold Rolling-Origin CV** + **Embargo $\ge 90$ hari** + **Moving-Block Bootstrap (`block=5, B=1.000`)** + **Single Holdout `> 2018-06-30`**.
* **Kinerja Uji Terkunci (`> 2018-06-30`):**
  - `LightGBM Classification` (**Pasca-Pengiriman**, `N=12.571`, base rate `0,0963`): **PR-AUC `0,3061`** (`95% CI [0,279–0,334]`), **ROC-AUC `0,6745`**, F1 `0,3417` *(vs Majority `0,0963`, GaussianNB `0,1996`, LogReg `0,2436`, KNN `0,2532`, Decision Tree `0,2704`, `TabularEmbeddingMLP` `0,2875`, Random Forest `0,3016`)*.
  - `Temporal CV 4-Fold LightGBM`: Mean **PR-AUC `0,3825`**, ROC-AUC `0,7130`, Brier `0,0902` *(Fold 1 `0,2308` · Fold 2 `0,3729` · Fold 3 krisis `19,98%` → **`0,6417`** · Fold 4 `0,2846`)*.
  - `Studi Ablasi (N=19.587 val)`: Ekonomi Saja (`0,1786`) → Pengalaman Kirim Saja (`0,2986`) → Kombinasi Penuh (`0,3598` val / `0,3061` test).
  - `Checkout Model` (**Saat Bayar**, `N=12.571`): **PR-AUC `0,1335`** `[0,122–0,148]`, **ROC-AUC `0,5468`**, Raw Brier `0,2370` → **Terbatas sebagai Indikator Awal**.
  - `Regresi Delay` (**Saat Serah Kurir**, `N=12.630`): `LightGBM` **MAE `4,8256 hari`**, RMSE `6,2458 hari`, $R^2$ `0,3926`; `Ridge` **MAE `4,7509`**, RMSE `5,9685`, $R^2$ `0,4454` *(vs median baseline `6,6903` = turun `~28%`; penyangga aman `+3 hari`)*.
  - `TextBiLSTM Portugis` (**Tahap Teks Komentar**, `N_test=4.142` komentar tertulis, base `16,2%`): **PR-AUC `0,3120`** *(vs prior `0,1620`, `+92,6%`)*, **ROC-AUC `0,7240`**, F1 `0,3680`, Brier `0,1140`, **`Macro-F1 0,8420`**.
  - `K-Means Segmentation` (`N=96.470`): `k=3` Silhouette `0,3865` (`Segmen 2 Beban Ongkir Tinggi 31,20% Neg`), PCA `52,81%`, `4.824` pencilan jarak `> 3,1838`; konfigurasi `K=4` `Sil 0,4180`, bootstrap `ARI 0,9832`.
  - `Repeat Purchase 90 Hari`: Checkout **ROC-AUC `0,5021`** `[0,472–0,531]`, PR-AUC `0,0202`; Post-Delivery **ROC-AUC `0,5284`** `[0,491–0,564]`, PR-AUC `0,0245` → **Ditolak untuk Operasional (Hanya Riset)**.
* **Kalibrasi, DCA & Lift:** Platt Scaling (`coef=0,9020, intercept=-1,8089`) → Brier `0,1375 → 0,0762` (`-44,59%`), ECE `0,2355 → 0,0070` (`-97,02%`), **`BSS = +0,1215`**; DCA pada $p_t=0,10$: Model **`+0,0284`** vs *Treat All* `-0,0044`; Top-K Lift: **5% `5,154×`**, **10% `3,556×`**, **20% `2,346×`**.
* **SHAP (`800` sampel) & Slices (`N=38.942 >= Mar 2018`):** Top 3 SHAP: `delivery_delay_days (0,3058)`, `delivery_lead_time_days (0,2252)`, `item_count (0,2086)`. Slice ROC-AUC: `RJ 0,8031`, `RS 0,7749`, `MG 0,7400`, `SP 0,7013`, `PR 0,6977`; `High > BRL 150 = 0,7700`; **`On-Time 0,6522`** vs **`Delayed 0,8383`**; Delay MAE **`SP 4,25` vs `RJ 7,72` hari**; batas harga terkalibrasi **`BRL 10–5.000`**.
* **Hipotesis (enam hipotesis), Biaya & World Model:** Lima hipotesis didukung (*confounder* menyusutkan efek `-47,3%`), sementara **dugaan rating mendorong beli ulang ditolak** (`OR=0,9964, p_adj=0,8609`); Biaya `$45 vs $5` → $\tau^* = 0,18$ (`4,2×` efisiensi) + A/B `80/20`; `VAR(1) 4×4` (`87` minggu), WAPE `15,83%` vs naive `22,41%`, Spectral Radius `0,8412`, *Synthetic Recovery* `1,60%`, subsidi merata saldo `-R$ 24.323` vs subsidi terarah hemat `50,3%` biaya, skenario *shock* `Z=3,68` → Peringatan Ekstrapolasi (OOD); Drift (`PSI`, `KS`, `Wasserstein-1`, `JSD`); `14 notebooks (111 sel / 51 sel kode)`.

---

## Lampiran 2: Kamus Ringkas Istilah & Analogi Machine Learning

| Istilah Teknis ML / DS | Penjelasan Singkat | Analogi Sederhana |
| :--- | :--- | :--- |
| **`Estimand`** | Definisi tegas target, populasi uji, dan waktu pengambilan fitur | Membedakan diagnosis awal saat masuk klinik vs evaluasi sesudah perawatan selesai |
| **`Grain` & *Fan-Out*** | Satuan tunggal 1 baris (`order_id`) & duplikasi baris akibat *join* tabel | Menggabungkan struk kasir multi-item dan multi-pembayaran menjadi satu ringkasan per transaksi |
| **`Lookahead Leakage`** | Pemakaian fitur dari masa sesudah kejadian untuk melatih prediksi sebelum kejadian | Menilai soal ujian awal dengan mengintip kunci jawaban yang baru terbit minggu depan |
| **`Embargo 90 Hari`** | Jeda pemisah kalender antara masa latih dan validasi agar label tuntas sepenuhnya | Memberi tenggang waktu hingga paket ujung periode latih selesai dikirim dan dinilai |
| **`Split-Before-Transform`** | Memisahkan data uji terlebih dahulu sebelum menghitung rata-rata pengisi atau *scaler* | Menghitung rata-rata kelas latihan tanpa mencampurkan nilai peserta ujian akhir |
| **`Bayesian Target Encoding`** | Estimasi bobot kategori dengan tarikan lembut ke rata-rata global | Kategori baru dengan sedikit sampel tidak langsung dinilai ekstrem |
| **`Rolling-Origin CV` & `Block Bootstrap`** | Pengujian bertahap maju mengikuti waktu & resampling blok berdekatan `5`-baris | Menyambung segmen klip waktu berurutan daripada mengacak bingkai acak tunggal |
| **`PR-AUC` vs `Accuracy`** | Ketepatan mendeteksi kelas minoritas (`9,63%`) vs metrik yang terbawa kelas mayoritas | Mencari kelompok kecil kasus jarang tanpa tertipu dominasi kelas mayoritas |
| **`Platt Scaling`, `Brier`, `ECE`, `BSS`** | Kalibrasi log-odds agar angka probabilitas sesuai dengan frekuensi kejadian riil | Menyelaraskan perkiraan hujan "70%" agar di kenyataan benar turun sekitar 7 dari 10 hari |
| **`DCA (Net Benefit)` & `Top-K Lift`** | Selisih manfaat bersih terhadap strategi merata & kepadatan masalah di antrean teratas | Menilai efisiensi pemeriksaan selektif 5% kandidat berisiko dibandingkan memeriksa semua orang |
| **`SHAP` & `Asosiasi vs Bukti Kausal`** | Atribusi kontribusi fitur di dalam model; korelasi historis berbeda dari bukti kausal | Payung dan hujan muncul bersamaan (hubungan asosiatif), bukan payung yang mendatangkan hujan (hubungan kausal) |
| **`Confounder`** | Variabel ketiga yang memicu korelasi semu antara dua variabel lain | Penjualan es krim dan jumlah pengunjung pantai naik bersama karena faktor ketiga, yaitu musim panas |
| **`Right-Censoring` & `Kaplan-Meier`** | Pengamatan yang terhenti sebelum kejadian selesai & kurva estimasi peluang tahannya | Mengukur daya tahan komponen ketika sebagian unit masih berfungsi hingga hari pengamatan berakhir |
| **`Manski Selection Bounds`** | Rentang nilai optimistis–pesimistis terburuk akibat sebagian respons yang hilang | Menghitung batas atas dan bawah hasil survei ketika sebagian kecil responden tidak menjawab |
| **`Spectral Radius < 1,0` & `OOD`** | Syarat kestabilan matriks dinamika & peringatan saat input keluar dari rentang historis | Peredam ayunan agar simulasi tak membesar tak terbatas dan alarm saat skenario jauh dari pengalaman masa lalu |
| **`PSI`, `KS`, `Wasserstein-1`, `JSD`** | Empat metrik pemantauan pergeseran distribusi fitur input dan keluaran probabilitas | Membandingkan pergeseran bentuk dan jarak sebaran data saat ini terhadap periode latih |
| **`Leaf-Wise` vs `Depth-Wise`** | Pembelahan daun dengan penurunan loss terbesar vs pembelahan merata di setiap kedalaman | Memfokuskan pembagian cabang tepat di zona kesalahan tertinggi dengan batas kedalaman tetap |
| **`Entity Embeddings`** | Representasi vektor berdimensi rendah untuk fitur kategorikal | Peta koordinat di mana kategori dengan karakter risiko mirip terletak saling berdekatan |
| **`Permutation Importance`** | Pengukuran seberapa besar skor model jatuh saat nilai satu kolom fitur diacak | Menguji ketergantungan sistem terhadap satu variabel dengan mengacak kontribusinya |
| **`ARI` (*Adjusted Rand Index*)** | Indeks konsistensi pengelompokan klaster ketika sampel data diulang lewat bootstrap | Memeriksa apakah pembagian segmen pelanggan tetap serupa bila komposisi data sedikit berubah |
| **`Harrell's C-Index`** | Ukuran ketepatan pemeringkatan urutan waktu kejadian pada data tersensor | Menilai konsistensi urutan risiko antar-unit dalam jangka waktu pengamatan berbeda |
| **`WAPE` vs `MAPE`** | Rata-rata error dibobot volume total dibandingkan rata-rata persentase error per periode | Menghindari distorsi persentase dari periode bervolume sangat rendah terhadap rata-rata error total |
| **`Synthetic Recovery Test`** | Pengujian ulang estimator terhadap data sintetis dengan parameter matriks yang diketahui | Mengukur presisi metode estimasi matriks transisi sebelum diaplikasikan ke data riil |
| **`Residual Bootstrapping`** | Penarikan berulang error residual historis guna menyusun interval prediksi simulasi | Memproyeksikan ketidakpastian dengan variasi error nyata masa lalu ketimbang asumsi normalitas kaku |

---

## Lampiran 3: Disiplin Interpretasi Hasil Pemodelan

* **Tepat dalam Menilai Ketidakseimbangan Kelas:** Laporkan `PR-AUC 0,3061` (> `3,18×` base rate `0,0963`), kalibrasi `ECE 0,0070`, dan `Top 5% Lift 5,154×`, alih-alih mengandalkan `Accuracy 90,37%`.
* **Tepat dalam Membedakan Asosiasi dan Kausalitas:** Posisikan bobot SHAP (`delivery_delay_days 0,3058`) sebagai **bukti asosiasi dalam model**, sedangkan pembuktian **hubungan kausal eksperimental** memerlukan eksperimen acak `A/B Holdout 80/20`.
* **Transparan terhadap Keterbatasan Data:** Nyatakan secara langsung pembatasan model saat checkout ke hanya indikator awal (`0,1335`) dan penolakan model `Repeat Purchase` (`0,5021`) sebagai `Temuan Negatif yang Sah` akibat ketiadaan data klik aplikasi maupun insentif historis.

---
**Akhir Naskah Presentasi Data Science & Machine Learning — CSIP.**
