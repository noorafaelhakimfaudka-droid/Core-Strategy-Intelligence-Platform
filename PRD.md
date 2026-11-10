# MASTER PRD: CSIP (Computational Society Intelligence Platform)
**Versi 2.0 — Master Edition (SKKNI, BNSP & Industry Portfolio Compliant)**

**Platform Data Science *end-to-end* untuk menemukan pola perilaku, menguji mekanisme dan hipotesis alternatif, memodelkan sistem yang saling memengaruhi, mengevaluasi dunia alternatif (simulasi), serta memenuhi standar sertifikasi profesi nasional (SKKNI/BNSP).**

| Informasi Dokumen | Spesifikasi Teknis & Akademis |
|---|---|
| **Nama Proyek** | Computational Society Intelligence Platform |
| **Singkatan** | CSIP |
| **Versi Dokumen** | 2.0 — Master Edition (Terintegrasi SKKNI/BNSP & 16 Modul Kompetensi) |
| **Status** | *Locked Baseline* — Siap menjadi acuan pengembangan, asesmen, & portofolio |
| **Jenis Proyek** | *End-to-End Data Science Research, Machine Learning/Deep Learning & Decision Intelligence* |
| **Kepatuhan Standar** | 11 Unit Kompetensi SKKNI (Sertifikasi BNSP) & 6 Target Pembelajaran Industri |
| **Domain MVP Awal** | Perilaku Konsumen, Transaksi, dan Ekosistem E-Commerce (Olist Dataset) |
| **Metodologi** | *Observational Data Science* menggunakan data sekunder (CRISP-DM + SKKNI Workflow) |
| **Antarmuka (UI)** | Streamlit (*Multi-page Analytical & Decision Showcase*) |
| **Bahasa & Ekosistem** | Python, Pandas, NumPy, Scikit-Learn, Statsmodels, LightGBM, PyTorch/TensorFlow |
| **Pendekatan Utama** | *Evidence-driven, modular, explainable, reproducible, audit-ready* |
| **Larangan Metodologis** | Tidak menggunakan survei, kuesioner, wawancara, eksperimen responden manusia, atau menjadikan LLM sebagai penentu bukti statistik |

---

# 0. RINGKASAN EKSEKUTIF

## 0.1 Apa itu CSIP?

CSIP adalah platform Data Science *end-to-end* yang dirancang untuk memahami fenomena perilaku manusia dan sistem sosial-ekonomi melalui data observasional yang telah tersedia. 

CSIP tidak hanya berhenti pada analisis deskriptif atau prediktif dangkal seperti:
- *Apa yang terjadi di masa lalu?*
- *Siapa segmen pelanggan yang bertransaksi?*
- *Berapa skor akurasi model prediksi?*

Tetapi CSIP melangkah lebih jauh untuk menjawab pertanyaan mekanisme dan keputusan strategis:
- **Mengapa** pola perilaku tersebut terbentuk?
- Variabel ekonomi dan pengalaman apa yang saling berinteraksi secara non-linear?
- Apakah pola tersebut konsisten di berbagai segmen, wilayah, dan rentang waktu?
- **Penjelasan alternatif (hipotesis tandingan)** apa yang mungkin menjelaskan fenomena yang sama?
- Bukti statistik apa yang mendukung atau menggugurkan masing-masing penjelasan?
- **Apa yang mungkin terjadi (*Alternative World*)** jika parameter operasional atau ekonomi diubah?
- Seberapa besar ketidakpastian (*uncertainty*) dan batas validitas dari rekomendasi yang dihasilkan?

**Prinsip Utama:** CSIP bukan sistem yang mengarang narasi paling menarik. CSIP adalah sistem rekayasa Data Science yang merumuskan objektif bisnis, menerjemahkannya ke tujuan teknis, menelaah dan mengkonstruksi data secara ketat, menguji berbagai skenario model (statistik, ML, hingga Deep Learning), serta mengevaluasi bukti secara jujur dan dapat direproduksi.

## 0.2 Filosofi & Prinsip Desain

> *Align Business Objectives. Discover Patterns. Investigate Mechanisms. Model Interacting Systems. Test Alternative Worlds. Quantify Uncertainty.*

Tujuh prinsip yang wajib mengatur seluruh kode, analisis, dan dokumentasi:
1. **Business & Technical Alignment > Blind Coding:** Setiap baris kode dan model harus menjawab objektif bisnis dan tujuan teknis yang terukur (Standar SKKNI Unit 1 & 2).
2. **Evidence > Assumption:** Klaim harus selalu memiliki tingkat pembuktian (*Claim Level* L0–L3) dan *Evidence Grade* (A–D).
3. **Validation > Complexity:** Model sederhana yang tervalidasi secara temporal lebih berharga daripada model kompleks yang mengalami *data leakage*.
4. **Explanation > Superficial Correlation:** Korelasi tidak boleh langsung diklaim sebagai kausalitas tanpa desain identifikasi yang sah.
5. **Reproducibility > One-time Results:** Seluruh pipeline dari data mentah hingga artefak UI harus dapat dijalankan ulang dengan hasil yang konsisten.
6. **Honest Uncertainty > False Confidence:** Setiap prediksi dan simulasi wajib menampilkan rentang ketidakpastian (*confidence/prediction interval*).
7. **Data Science Rigor > Unnecessary AI Hype:** Inti sistem adalah matematika, statistik, ML, dan DL yang teruji—bukan *chatbot* atau pembungkus LLM.

## 0.3 Empat Mesin Utama CSIP

| Mesin Inti | Fungsi Utama dalam Sistem | Output Artefak |
|---|---|---|
| **1. Behavioral Discovery Engine** | Menemukan pola perilaku, anomali, klaster segmen, dan interaksi variabel yang tidak langsung terlihat melalui EDA standar. | *Pattern Catalogue, Segment Profiles, Anomaly Report* |
| **2. Hypothesis Investigation Engine** | Merumuskan dan menguji berbagai penjelasan alternatif menggunakan uji statistik dan pemodelan terstruktur. | *Hypothesis Registry, Evidence Comparison Matrix* |
| **3. System & World Model** | Memodelkan transisi keadaan sistem (*state transition*) menggunakan kombinasi model prediktif ML/DL dan aturan struktural. | *System State Model, Predictive Artifacts, DL Benchmarks* |
| **4. Decision & Alternative World Engine** | Mensimulasikan skenario intervensi (*what-if*), menghitung *trade-off* risiko, dan memberikan rekomendasi berbasis bukti. | *Scenario Simulation Report, Decision Trade-off Matrix* |

---

# 1. INTEGRASI STANDAR SKKNI (BNSP) & TARGET PEMBELAJARAN

Untuk memastikan proyek ini memenuhi standar industri sekaligus memenuhi syarat asesmen **Standar Kompetensi Kerja Nasional Indonesia (SKKNI)** untuk sertifikasi **BNSP** bidang Data Science, seluruh arsitektur dan *pipeline* CSIP dipetakan secara langsung ke **11 Unit Kompetensi SKKNI**, **6 Target Pembelajaran**, dan **16 Modul Kurikulum**.

## 1.1 Matriks Pemetaan 11 Unit Kompetensi SKKNI (BNSP) ke Arsitektur CSIP

| No | Unit Kompetensi SKKNI (BNSP) | Implementasi Konkret dalam CSIP | Artefak / Bukti Asesmen (Deliverables) |
|---|---|---|---|
| **1** | **Menentukan Objektif Bisnis** | Merumuskan masalah retensi pelanggan, friksi biaya logistik (*freight*), dan kepuasan pengiriman pada ekosistem e-commerce serta dampaknya terhadap *Gross Merchandise Value* (GMV) dan *Customer Lifetime Value* (CLV). | Bab 2 PRD, `config/analysis_plan.yaml`, *Business Problem Statement* di `01_data_understanding.ipynb` |
| **2** | **Menentukan Tujuan Teknis Data Science** | Menerjemahkan objektif bisnis menjadi target metrik teknis: klasifikasi *repeat purchase* ($ROC\text{-}AUC \ge 0.65$, $PR\text{-}AUC$ di atas baseline), regresi nilai/waktu pengiriman ($MAE$, $RMSE$), klasterisasi ($Silhouette \ge 0.35$), dan kuota bukti hipotesis. | Bab 2.3 PRD, Matriks Sukses Teknis, `config/models.yaml` |
| **3** | **Menelaah Data** | Melakukan *data profiling* menyeluruh pada 9 tabel relasional Olist (~100.000 pesanan), analisis tipe data, distribusi statistik, relasi kunci (*primary/foreign keys*), dan eksplorasi pola awal (EDA). | `01_data_understanding.ipynb`, `03_eda.ipynb`, `data/data_dictionary.md`, modul `csip.data` |
| **4** | **Memvalidasi Data** | Menguji integritas skema, mendeteksi *missing values*, duplikasi, anomali *timestamp* (misal: tanggal sampai sebelum tanggal dikirim), serta memvalidasi masalah *right-censoring* pada jendela observasi pelanggan. | `02_data_quality.ipynb`, `reports/data_quality_report.md`, `tests/test_data_quality.py` |
| **5** | **Menentukan Objek Data** | Menetapkan *grain* data yang tepat (Order-level vs Customer-level vs Weekly System State), memilih atribut relevan, menetapkan populasi sampel yang bebas bias *censoring*, dan memisahkan *temporal split*. | `config/data.yaml`, Dokumentasi *Grain* & *Cohort Selection* di `04_feature_engineering.ipynb` |
| **6** | **Membersihkan Data** | Menangani *missing values* secara terukur, memperbaiki inkonsistensi format waktu/kategori, menyaring pesanan berstatus *canceled/unavailable* sesuai aturan, dan menstandarkan entitas `customer_unique_id`. | Modul `csip.cleaning`, *Clean Interim Datasets* (`data/interim/`), log pembersihan data |
| **7** | **Mengkonstruksi Data** | Merekayasa fitur (*feature engineering*) ekonomi, pengalaman pengiriman, histori perilaku (*as-of features* bebas *leakage*), fitur interaksi non-linear, *encoding*, *scaling*, dan transformasi tensor untuk Deep Learning. | `04_feature_engineering.ipynb`, modul `csip.features`, `data/processed/`, `tests/test_leakage.py` |
| **8** | **Membangun Skenario Model** | Merancang matriks eksperimen (E0–E9), menetapkan *baseline ladder* (B0–B5), mendesain skema *temporal train-validation-test split*, strategi penanganan *imbalanced data*, serta skenario simulasi *Alternative World*. | Bab 10 PRD, `config/models.yaml`, `config/scenarios.yaml`, `06_hypothesis_investigation.ipynb` |
| **9** | **Membangun Model** | Melatih dan mengoptimasi model Statistik, Supervised ML (LogReg, Decision Tree, Random Forest, LightGBM, KNN, Naive Bayes), Unsupervised (K-Means/DBSCAN), serta Neural Network / Deep Learning (MLP, LSTM/1D-CNN/TabNet). | `07_predictive_modeling.ipynb`, `10_world_model.ipynb`, modul `csip.models`, `artifacts/models/` |
| **10** | **Mengevaluasi Hasil Pemodelan** | Mengukur performa model pada *holdout test set* menggunakan metrik klasifikasi, regresi, kalibrasi probabilitas, analisis *error/residual*, SHAP *explainability*, dan *stress-testing* simulasi. | `08_temporal_validation.ipynb`, `09_explainability.ipynb`, `12_uncertainty_analysis.ipynb`, `reports/model_report.md` |
| **11** | **Melakukan Proses Review Pemodelan** | Mengaudit kepatuhan klaim ilmiah (L0–L3), melakukan *ablation study*, mencatat kegagalan model di *Failure Register*, mengevaluasi keterbatasan data, dan menyusun rekomendasi perbaikan iteratif. | `13_failure_analysis.ipynb`, `14_final_research_report.ipynb`, `reports/evidence_table.md`, Halaman 9 Streamlit |

## 1.2 Pemenuhan 6 Target Pembelajaran Utama

1. **Memahami objektif bisnis & menerjemahkannya ke tujuan teknis DS:** Dijabarkan secara eksplisit pada **Bab 2** melalui penyelarasan masalah retensi/logistik e-commerce menjadi metrik optimasi model dan hipotesis terukur.
2. **Menguasai pengolahan data (penelaahan, validasi, pembersihan, konstruksi):** Dijabarkan pada **Bab 6 & Bab 7** melalui arsitektur *pipeline* data multi-grain yang dilengkapi pengujian otomatis (*unit test* anti-leakage).
3. **Mampu melakukan eksplorasi data (EDA) dan visualisasi untuk insight:** Dijabarkan pada **Bab 8 & Bab 14** melalui *Behavioral Discovery Engine* dan visualisasi interaktif berbasis Plotly/Matplotlib di Jupyter dan Streamlit.
4. **Mampu membangun skenario dan model ML supervised & unsupervised:** Dijabarkan pada **Bab 10** melalui matriks eksperimen menyeluruh yang mencakup regresi, klasifikasi, dan klasterisasi perilaku.
5. **Menguasai evaluasi, review, dan perbaikan performa model:** Dijabarkan pada **Bab 10, Bab 12, & Bab 15** melalui validasi temporal, *hyperparameter tuning*, kalibrasi, *ablation study*, dan *Validation Gates* (G0–G11).
6. **Mampu mengembangkan model lanjutan menggunakan Neural Network & Deep Learning:** Dijabarkan pada **Bab 10.5 & Bab 18** melalui *Deep Learning Competency Laboratory* (arsitektur MLP dengan *Embedding Layers* untuk data tabular/kategorikal, serta Sequence/Text DL untuk ulasan dan deret waktu).

---

# 2. OBJEKTIF BISNIS, TUJUAN TEKNIS, DAN LANDASAN PENELITIAN
*(Pemenuhan SKKNI Unit 1 & Unit 2)*

## 2.1 Latar Belakang & Fenomena Awal

Dalam ekosistem perdagangan digital dan sistem sosial-ekonomi, keputusan manusia jarang ditentukan oleh satu faktor tunggal. Sebagai ilustrasi konseptual: ketika dihadapkan pada dua pilihan toko dengan selisih harga relatif kecil, konsumen sering kali memilih toko yang memberikan pengalaman transaksi lebih baik, kepastian pengiriman lebih andal, atau reputasi yang lebih tepercaya.

Namun, analisis bisnis konvensional sering memisahkan faktor-faktor tersebut ke dalam silo yang terisolasi:
- Tim penetapan harga hanya menganalisis elastisitas harga terhadap volume penjualan.
- Tim logistik hanya memantau rata-rata hari pengiriman.
- Tim layanan pelanggan hanya melihat skor ulasan (*review score*) secara agregat.

Akibatnya, perusahaan gagal memahami **mekanisme interaksi**: *Pada batas biaya berapakah keterlambatan pengiriman mulai menghancurkan probabilitas pembelian ulang? Apakah pengalaman pengiriman yang buruk berdampak sama pada semua segmen pelanggan, atau ada kelompok yang jauh lebih sensitif?*

## 2.2 Objektif Bisnis (SKKNI Unit 1)

Bagi manajemen marketplace dan penjual (*sellers*), tantangan bisnis utama adalah **rendahnya tingkat retensi pelanggan (*repeat purchase rate*)** dan **tingginya biaya akuisisi pelanggan baru**, yang diperburuk oleh ketidakefisienan biaya pengiriman (*freight cost*) serta fluktuasi kualitas pemenuhan pesanan (*fulfillment*).

Oleh karena itu, **Objektif Bisnis Utama CSIP** adalah:
1. **Identifikasi Penggerak Retensi & Kepuasan:** Mengungkap faktor-faktor ekonomi (harga produk, rasio ongkos kirim) dan operasional (ketepatan waktu pengiriman, kecepatan pemrosesan) yang paling kritis dalam membentuk kepuasan pelanggan dan keputusan pembelian ulang.
2. **Mitigasi Risiko Churn & Ulasan Negatif:** Mendeteksi dini transaksi atau segmen pelanggan yang berisiko tinggi memberikan ulasan buruk ($\le 2$ bintang) atau tidak melakukan pembelian kembali setelah transaksi pertama.
3. **Optimalisasi Kebijakan Logistik & Harga (Simulasi Keputusan):** Menyediakan alat bantu simulasi (*Alternative World*) bagi pengambil keputusan untuk mengevaluasi *trade-off* antara subsidi ongkos kirim vs. peningkatan kecepatan pengiriman terhadap proyeksi pertumbuhan pesanan dan retensi.
4. **Efisiensi Alokasi Sumber Daya Segmen:** Mengelompokkan pelanggan dan kategori produk ke dalam segmen perilaku yang bermakna agar strategi intervensi bisnis dapat ditargetkan secara presisi.

## 2.3 Tujuan Teknis Data Science (SKKNI Unit 2)

Untuk menjawab Objektif Bisnis di atas secara terukur, ditetapkan **Tujuan Teknis Data Science** beserta kriteria keberhasilan kuantitatifnya:

| ID Tujuan | Kategori Teknis | Deskripsi Tujuan Teknis Data Science | Metrik Evaluasi Utama & Kriteria Sukses Baseline |
|---|---|---|---|
| **TT-01** | **Data Engineering & Konstruksi** | Membangun *pipeline* integrasi 9 tabel mentah Olist menjadi *analytical datasets* multi-grain yang bersih, tervalidasi, dan bebas *time-travel data leakage*. | $100\%$ lulus *automated schema & leakage tests* (`pytest`); persentase *unhandled missing values* $= 0\%$ pada fitur model. |
| **TT-02** | **Unsupervised Learning (Segmentasi)** | Mengidentifikasi klaster perilaku pelanggan dan profil transaksi menggunakan algoritma *clustering* untuk menemukan struktur segmen alami. | *Silhouette Score* $\ge 0.35$, *Davies-Bouldin Index* terendah di antara kandidat, serta stabilitas profil klaster lintas waktu. |
| **TT-03** | **Hypothesis Testing & Statistik** | Menguji minimal 6 hipotesis terstruktur (H1–H6) terkait interaksi harga, ongkir, keterlambatan pengiriman, dan retensi dengan kontrol *False Discovery Rate* (FDR). | Nilai $p\text{-value}$ terkoreksi ($\alpha = 0.05$), ukuran efek (*effect size* seperti *Odds Ratio*, Cohen's $d$, atau $\beta$ terstandarisasi) beserta $95\%$ *Confidence Interval*. |
| **TT-04** | **Supervised Learning (Klasifikasi)** | Membangun model prediktif untuk memprediksi: (a) probabilitas *repeat purchase* dalam jendela observasi tetap, dan (b) risiko ulasan negatif (*negative review flag*). | Mengungguli *Naive/LogReg Baseline* (B0/B1) pada *temporal holdout test set* berdasarkan $PR\text{-}AUC$, $ROC\text{-}AUC$, $F1\text{-Score}$, dan *Brier Score* (kalibrasi). |
| **TT-05** | **Supervised Learning (Regresi)** | Membangun model regresi untuk mengestimasi durasi waktu pengiriman aktual, nilai total pengeluaran pelanggan, atau deviasi keterlambatan. | Penurunan $MAE$ dan $RMSE$ minimal $10\%$ dibandingkan *baseline mean/median predictor*, serta analisis distribusi *residual* yang tervalidasi. |
| **TT-06** | **Neural Network & Deep Learning** | Mengembangkan arsitektur *Deep Learning* (MLP dengan *Entity Embeddings* untuk tabular, serta model *Sequence/NLP* untuk teks ulasan/deret waktu) dan membandingkannya secara adil dengan model *tree-based* (LightGBM). | Konvergensi *loss function* tanpa *overfitting* ekstrem pada *validation set*; dokumentasi komparasi performa dan *computational trade-off*. |
| **TT-07** | **World Model & Simulasi Skenario** | Membangun model transisi keadaan mingguan $\mathbf{S}_{t+1} = f(\mathbf{S}_t, \mathbf{A}_t, \mathbf{E}_t) + \boldsymbol{\epsilon}_t$ untuk memproyeksikan dampak perubahan parameter ongkir dan waktu pengiriman. | Lulus *Synthetic Recovery Test*, *Historical Replay Validation* ($MAPE / WAPE$ terukur), dan menampilkan $90\%/95\%$ *Prediction Interval*. |

## 2.4 Rumusan Masalah & Hipotesis Penelitian (BDI Module)

**Pertanyaan Penelitian Utama:**
> *Bagaimana hubungan dan interaksi antara struktur biaya transaksi (harga dan ongkos kirim), pengalaman pemenuhan pesanan (durasi dan keterlambatan pengiriman), serta karakteristik produk terhadap kepuasan dan probabilitas pelanggan melakukan pembelian ulang dalam ekosistem e-commerce?*

**Kandidat Hipotesis untuk Diuji (Bukan Asumsi yang Dipaksakan Terbukti):**

| ID | Pernyataan Hipotesis | Jenis Analisis | Variabel Kunci |
|---|---|---|---|
| **H1** | Rasio ongkos kirim terhadap harga produk ($\text{Freight Ratio}$) memiliki asosiasi negatif terhadap nilai kepuasan transaksi dan konversi keranjang multi-item. | Asosiasi & Regresi | `price`, `freight_value`, `freight_ratio`, `review_score` |
| **H2** | Keterlambatan pengiriman melewati tanggal estimasi ($\text{Delivery Delay} > 0$) memberikan dampak penurunan kepuasan pelanggan yang bersifat asimetris (non-linear) dibandingkan pengiriman lebih cepat. | Non-linear Association | `delivery_delay_days`, `delivered_on_time`, `review_score` |
| **H3** | Pengalaman pengiriman dan skor ulasan pada transaksi pertama berasosiasi secara signifikan dengan probabilitas pelanggan melakukan pembelian ulang (*repeat purchase*). | Klasifikasi & Survival/Cohort | `first_order_review`, `first_order_delay`, `repeat_purchase_flag` |
| **H4** | Sensitivitas pelanggan terhadap ongkos kirim dan keterlambatan pengiriman bersifat heterogen (berbeda secara signifikan) antarsegmen perilaku dan kategori produk. | Heterogenitas & Interaksi | `cluster_id`, `product_category`, interaksi `delay_x_freight` |
| **H5** | Penggabungan fitur ekonomi, indikator pengalaman pengiriman, dan representasi teks ulasan/embedding meningkatkan daya prediksi model dibandingkan hanya menggunakan fitur ekonomi. | *Predictive Ablation* | Fitur Ekonomi vs. Pengalaman vs. Gabungan (ML & DL) |
| **H6** | Pola hubungan yang tampak antara nilai pengeluaran dan pembelian ulang sebagian dijelaskan oleh faktor pembaur (*confounders*) seperti kategori produk kebutuhan berulang dan lokasi geografis. | *Alternative Explanation Testing* | `customer_state`, `category_repeatability`, `total_spending` |

**Batasan Konstruk Penelitian:** Dataset Olist tidak mengukur "keramahan interpersonal penjual" secara langsung. Oleh karena itu, CSIP membatasi klaim empiris MVP pada **indikator pengalaman pemenuhan pesanan dan persepsi ulasan pelanggan**, sembari menyiapkan kerangka metodologis untuk data interpersonal pada fase ekspansi.

---

# 3. SCOPE PRODUK

## 3.1 In Scope (Wajib Dicakup)
1. Perumusan objektif bisnis dan tujuan teknis sesuai standar SKKNI/BNSP.
2. Akuisisi, penelaahan (*profiling*), dan validasi kualitas data sekunder multi-tabel.
3. Penentuan objek data (*grain definition*, pemilihan *cohort*) dan pembersihan data terstruktur.
4. Konstruksi data dan *feature engineering* dengan pencegahan *data leakage* yang ketat.
5. *Behavioral Pattern Discovery* melalui metode eksplorasi statistik dan *unsupervised clustering*.
6. *Hypothesis Investigation Engine* untuk menguji dan membandingkan hipotesis alternatif.
7. Pemodelan *Supervised Learning* lengkap (Linear/Logistic Regression, Decision Tree, Random Forest, LightGBM, KNN, Naive Bayes).
8. Eksperimen dan implementasi *Neural Network* & *Deep Learning* (MLP *Tabular Embeddings*, *Text/Sequence Deep Learning*).
9. Evaluasi model komprehensif, validasi temporal, *explainability* (SHAP), dan *review* pemodelan (*Ablation & Failure Analysis*).
10. *System & World Modeling* beserta *Alternative World Scenario Simulation* dan kuantifikasi ketidakpastian.
11. Pembuatan paket Python modular (`src/csip`) dan antarmuka aplikasi analitik 9 halaman berbasis Streamlit.

## 3.2 Out of Scope (Di Luar Cakupan MVP)
- Pengumpulan data primer melalui survei, kuesioner, wawancara, atau eksperimen psikologis terhadap responden manusia.
- Pengembangan sistem berbasis *chatbot*, *autonomous LLM agent*, atau menjadikan LLM sebagai mesin kesimpulan statistik.
- Klaim psikologis/kepribadian individu atau klaim kausalitas universal di luar domain dan periode observasi data.
- Integrasi langsung (*real-time production deployment*) ke infrastruktur ERP/sistem transaksi internal perusahaan.

---

# 4. ARSITEKTUR KONSEPTUAL CSIP

## 4.1 Spesifikasi Matematis Empat Mesin Utama

### A. Behavioral Discovery Engine
Bertugas melakukan pemetaan ruang fitur berdimensi tinggi $\mathbf{X} \in \mathbb{R}^{N \times D}$ menjadi struktur kelompok dan pola asosiasi:
- **Segmentasi Perilaku:** Mengelompokkan vektor fitur pelanggan $\mathbf{x}_i$ ke dalam klaster $C_k \in \{C_1, \dots, C_K\}$ sedemikian sehingga meminimalkan varians intra-klaster dan memaksimalkan separasi antar-klaster.
- **Deteksi Interaksi & Anomali:** Mengidentifikasi pasangan variabel $(X_j, X_m)$ di mana efek gabungan terhadap target $Y$ menyimpang secara signifikan dari efek aditif individualnya.

### B. Hypothesis Investigation Engine
Untuk setiap fenomena teramati $\mathcal{F}$, mesin ini mengevaluasi himpunan hipotesis yang saling bersaing $\mathcal{H} = \{H_1, H_2, \dots, H_M\}$:
- Setiap hipotesis $H_m$ dipetakan ke model spesifikasi statistik $M_m$ dengan himpunan variabel kontrol/konfounding $\mathbf{Z}_m$.
- Sistem menguji apakah estimasi parameter efek $\hat{\theta}_m$ tetap stabil dan signifikan ketika diuji terhadap spesifikasi alternatif $\mathbf{Z}_{m'}$.
- Jika dua hipotesis menghasilkan kecocokan empiris yang setara dan tidak dapat dipisahkan oleh data yang tersedia, sistem wajib menetapkan status **"Indistinguishable given current data"**.

### C. System & World Model
Menggambarkan dinamika agregat atau segmen sistem pada interval waktu diskret $t$ (misal: mingguan):

$$\mathbf{S}_{t+1} = f_{\Theta}(\mathbf{S}_t, \mathbf{A}_t, \mathbf{E}_t) + \boldsymbol{\epsilon}_t$$

Di mana:
- $\mathbf{S}_t$: Vektor keadaan sistem pada waktu $t$ (misal: volume pesanan aktif, rata-rata waktu pengiriman, proporsi ulasan negatif, tingkat retensi *cohort*).
- $\mathbf{A}_t$: Vektor variabel kontrol atau intervensi skenario (misal: perubahan struktur tarif ongkir $\Delta \text{Freight}$, perubahan kapasitas kecepatan pengiriman $\Delta \text{LeadTime}$).
- $\mathbf{E}_t$: Faktor eksternal/kontekstual (musiman, komposisi kategori produk, distribusi geografis).
- $f_{\Theta}$: Kombinasi fungsi transisi yang terdiri dari model prediktif terlatih (ML/DL) dan identitas akuntansi deterministik (misal: $\text{Total Cost} \equiv \text{Item Price} + \text{Freight Value}$).
- $\boldsymbol{\epsilon}_t$: Vektor gangguan stokastik / ketidakpastian residual yang diestimasi melalui *bootstrapping* atau *quantile regression*.

### D. Decision & Alternative World Engine
Mengevaluasi perbedaan distribusi hasil antara dunia dasar (*Baseline World* $\mathbf{A}^{(0)}$) dan dunia intervensi (*Alternative World* $\mathbf{A}^{(1)}$):

$$\Delta \mathbf{Y}_{t+1} = \mathbf{Y}_{t+1}(\mathbf{A}^{(1)}) - \mathbf{Y}_{t+1}(\mathbf{A}^{(0)})$$

Menghitung nilai ekspektasi $\mathbb{E}[\Delta \mathbf{Y}]$, rentang interval prediksi $[Q_{0.05}, Q_{0.95}]$, serta *tipping point* (titik batas di mana perubahan asumsi membalikkan arah rekomendasi).

## 4.2 Diagram Alir Arsitektur & Pipeline SKKNI

```text
[1. Objektif Bisnis] ---> [2. Tujuan Teknis DS]
                                  |
                                  v
                    [DATA SOURCES: Olist 9 Tables]
                                  |
                                  v
              [3. Menelaah Data & 4. Memvalidasi Data]
             (Profiling, Schema Check, Quality Report)
                                  |
                                  v
           [5. Menentukan Objek Data & 6. Membersihkan Data]
          (Grain Definition, Cohort Filtering, Deduplication)
                                  |
                                  v
                    [7. Mengkonstruksi Data]
       (As-Of Feature Engineering, Interactions, Leakage Check)
                                  |
          +-----------------------+-----------------------+
          |                                               |
          v                                               v
[BEHAVIORAL DISCOVERY]                        [8. Membangun Skenario Model]
(Clustering, Anomalies, EDA)                  (Hypotheses H1-H6, Split Design)
          |                                               |
          +-----------------------+-----------------------+
                                  |
                                  v
                        [9. Membangun Model]
      (Statistical, Tree-based ML, KNN/NB, Neural Net & Deep Learning)
                                  |
                                  v
                   [10. Mengevaluasi Hasil Pemodelan]
          (Temporal Validation, Metrics, Calibration, SHAP)
                                  |
                                  v
                [SYSTEM WORLD MODEL & ALTERNATIVE WORLD]
            (State Transition, What-If Simulation, Uncertainty)
                                  |
                                  v
                 [11. Melakukan Proses Review Pemodelan]
         (Evidence Grading, Ablation, Failure Register, Streamlit UI)
```

---

# 5. SPESIFIKASI DATA, PENELAAHAN, DAN VALIDASI DATA
*(Pemenuhan SKKNI Unit 3, Unit 4, & Unit 5)*

## 5.1 Sumber Data Utama (SKKNI Unit 3: Menelaah Data)

Dataset utama MVP adalah **Brazilian E-Commerce Public Dataset by Olist** (~100.000 pesanan pada periode 2016–2018) yang terdiri dari 9 tabel relasional:

| Nama File Tabel | Primary / Foreign Key | Grain Tabel | Variabel Utama untuk Ditelaah | Peran dalam CSIP |
|---|---|---|---|---|
| `olist_orders_dataset.csv` | `order_id`, `customer_id` | 1 baris per pesanan | `order_status`, `order_purchase_timestamp`, `order_delivered_customer_date`, `order_estimated_delivery_date` | Tulang punggung waktu transaksi, status pesanan, dan perhitungan keterlambatan pengiriman. |
| `olist_order_items_dataset.csv` | `order_id`, `order_item_id`, `product_id`, `seller_id` | 1 baris per item dalam pesanan | `price`, `freight_value`, `shipping_limit_date` | Variabel ekonomi inti (harga barang dan biaya ongkos kirim). |
| `olist_order_payments_dataset.csv` | `order_id`, `payment_sequential` | 1 baris per metode pembayaran per pesanan | `payment_type`, `payment_installments`, `payment_value` | Perilaku pembayaran, jumlah cicilan, dan nilai total transaksi. |
| `olist_order_reviews_dataset.csv` | `review_id`, `order_id` | 1 baris per ulasan pesanan | `review_score` (1–5), `review_comment_title`, `review_comment_message` | Indikator pengalaman pelanggan, kepuasan, dan korpus teks untuk NLP/Deep Learning. |
| `olist_customers_dataset.csv` | `customer_id`, `customer_unique_id` | 1 baris per sesi transaksi pelanggan | `customer_zip_code_prefix`, `customer_city`, `customer_state` | Identifikasi entitas pelanggan sebenarnya (`customer_unique_id`) untuk melacak *repeat purchase*. |
| `olist_sellers_dataset.csv` | `seller_id` | 1 baris per penjual | `seller_zip_code_prefix`, `seller_city`, `seller_state` | Analisis kinerja pemenuhan pesanan tingkat penjual dan jarak geografis. |
| `olist_products_dataset.csv` | `product_id` | 1 baris per produk unik | `product_category_name`, dimensi fisik (`weight_g`, `length_cm`, dll.) | Karakteristik fisik produk dan determinan biaya pengiriman. |
| `olist_geolocation_dataset.csv` | `geolocation_zip_code_prefix` | Koordinat per kode pos | `geolocation_lat`, `geolocation_lng` | Perhitungan jarak Haversine antara lokasi penjual dan pembeli. |
| `product_category_name_translation.csv` | `product_category_name` | 1 baris per kategori | `product_category_name_english` | Standardisasi nama kategori produk ke bahasa Inggris. |

## 5.2 Aturan Validasi Data (SKKNI Unit 4: Memvalidasi Data)

Sebelum data masuk ke tahap pembersihan dan konstruksi, modul `csip.data.validator` wajib menjalankan pemeriksaan otomatis dan menghasilkan **Data Quality Report**:

1. **Validasi Kunci & Kardinalitas:**
   - Memastikan `order_id` unik pada `olist_orders_dataset`.
   - Memeriksa *orphan records* (misal: `order_id` di tabel pembayaran atau ulasan yang tidak memiliki pasangan di tabel pesanan).
   - Mendeteksi pesanan dengan banyak ulasan (*multiple reviews per order*) dan menetapkan aturan agregasi/deduplikasi yang konsisten.
2. **Validasi Logika Kronologis (Timestamp Sanity Check):**
   - Memeriksa pelanggaran urutan waktu: $\text{Purchase Date} \le \text{Approved Date} \le \text{Carrier Date} \le \text{Delivered Date}$.
   - Mencatat jumlah baris yang memiliki anomali kronologis (misal: tanggal diterima pelanggan lebih awal daripada tanggal pembelian).
3. **Validasi Rentang Nilai Numerik:**
   - Memastikan $\text{price} > 0$, $\text{freight\_value} \ge 0$, $\text{payment\_value} \ge 0$, dan $\text{review\_score} \in \{1, 2, 3, 4, 5\}$.
4. **Validasi Distribusi & Missing Values:**
   - Menghitung persentase *null/missing* pada setiap kolom (khususnya `order_delivered_customer_date` pada pesanan yang belum selesai dan `review_comment_message` pada ulasan tanpa teks).

## 5.3 Penentuan Objek Data & Mitigasi Right-Censoring (SKKNI Unit 5: Menentukan Objek Data)

Kesalahan paling fatal pada analisis dataset Olist adalah mencampuradukkan `customer_id` (ID per transaksi) dengan `customer_unique_id` (ID pelanggan sebenarnya), serta mengabaikan *right-censoring* di akhir periode dataset.

CSIP menetapkan **4 Objek Data (Analytical Grains)** yang terpisah secara tegas:
1. **Objek Data 1 — Order-Level Table (`grain: order_id`):** Digunakan untuk analisis nilai transaksi, prediksi risiko keterlambatan pengiriman, dan prediksi skor ulasan pesanan.
2. **Objek Data 2 — Customer-Cohort Table (`grain: customer_unique_id`):** Digunakan untuk analisis retensi, segmentasi perilaku (*clustering*), dan prediksi *repeat purchase*.
3. **Objek Data 3 — Review-Text Corpus (`grain: review_id / order_id`):** Digunakan untuk analisis NLP dan pemodelan *Deep Learning* berbasis teks.
4. **Objek Data 4 — Weekly System State Panel (`grain: year_week`):** Digunakan untuk *World Model*, analisis deret waktu (*time-series*), dan simulasi skenario *Alternative World*.

**Aturan Penanganan Right-Censoring pada Definisi Repeat Purchase:**
- Jika dataset berakhir pada tanggal $T_{\max}$, pelanggan yang melakukan pembelian pertama pada $T_{\max} - 7\text{ hari}$ hampir pasti tercatat tidak melakukan pembelian ulang hanya karena waktu pengamatan sudah habis.
- Oleh karena itu, CSIP mendefinisikan jendela observasi tetap $\Delta W$ (misal: $90$ atau $180$ hari setelah pembelian pertama, disertai analisis sensitivitas untuk berbagai nilai $\Delta W$).
- Pelanggan yang pembelian pertamanya terjadi setelah $T_{\max} - \Delta W$ dikeluarkan dari populasi evaluasi target *repeat purchase* agar label kelas tidak terdistorsi oleh *censoring*.

---

# 6. PEMBERSIHAN DAN KONSTRUKSI DATA (FEATURE ENGINEERING)
*(Pemenuhan SKKNI Unit 6 & Unit 7)*

## 6.1 Prosedur Pembersihan Data (SKKNI Unit 6: Membersihkan Data)

Semua langkah pembersihan harus bersifat deterministik, terdokumentasi di `csip.cleaning`, dan mencatat jumlah baris sebelum serta sesudah pemrosesan:
1. **Penanganan Status Pesanan:** Untuk analisis pengalaman pengiriman aktual, saring pesanan dengan `order_status == 'delivered'`. Untuk analisis pembatalan/risiko kegagalan pemenuhan, simpan status `'canceled'` dan `'unavailable'` dalam objek data terpisah.
2. **Deduplikasi Geolocation & Reviews:**
   - Pada tabel `geolocation`, agregasikan koordinat (`lat`, `lng`) menggunakan nilai **median** per `geolocation_zip_code_prefix` untuk menghilangkan *outlier* koordinat dan mencegah *cartesian explosion* saat melakukan *join*.
   - Pada tabel `reviews`, jika satu `order_id` memiliki lebih dari satu ulasan, ambil ulasan berdasarkan aturan waktu pembuatan terbaru (`review_creation_date`) atau rata-rata skor sesuai spesifikasi grain.
3. **Imputasi & Penanganan Missing Values:**
   - Kolom teks ulasan yang kosong (`NaN`) diisi dengan token kosong `""` dan dibuatkan fitur indikator biner `has_review_comment = 0/1`.
   - Dimensi produk atau kategori yang kosong diimputasi menggunakan median kategori atau dikelompokkan ke dalam kategori `'unknown'` (nilai parameter imputasi **wajib** di-*fit* hanya pada *training split*).
4. **Penanganan Outlier Ekstrem:**
   - Nilai `price`, `freight_value`, dan `delivery_days` yang berada di atas persentil ke-$99.5$ dianalisis secara khusus; untuk model sensitif skala (seperti Regresi Linear, KNN, dan Neural Network), diterapkan *winsorizing* atau transformasi logaritmik $\log(1 + x)$.

## 6.2 Konstruksi Data & Rekayasa Fitur (SKKNI Unit 7: Mengkonstruksi Data)

Fitur dikonstruksi secara sistematis ke dalam 5 kelompok utama:

### 1. Fitur Ekonomi Transaksi (Economic Features)
- $\text{total\_item\_price} = \sum \text{price}_i$ per pesanan.
- $\text{total\_freight} = \sum \text{freight\_value}_i$ per pesanan.
- $\text{total\_order\_value} = \text{total\_item\_price} + \text{total\_freight}$.
- $\text{freight\_ratio} = \frac{\text{total\_freight}}{\text{total\_item\_price} + \epsilon}$ (mengukur beban relatif ongkos kirim terhadap harga barang).
- `item_count`: Jumlah unit barang dalam satu pesanan.
- `payment_installments_max`: Jumlah cicilan maksimum yang digunakan.

### 2. Fitur Pengalaman Pemenuhan Pesanan (Fulfillment & Experience Features)
- $\text{delivery\_lead\_time\_days} = (\text{delivered\_date} - \text{purchase\_timestamp})$ dalam satuan hari.
- $\text{estimated\_lead\_time\_days} = (\text{estimated\_date} - \text{purchase\_timestamp})$ dalam satuan hari.
- $\text{delivery\_delay\_days} = (\text{delivered\_date} - \text{estimated\_date})$ (nilai positif berarti terlambat, nilai negatif berarti datang lebih cepat dari janji).
- $\text{is\_late} = \mathbb{I}(\text{delivery\_delay\_days} > 0)$ (indikator biner keterlambatan).
- $\text{approval\_lag\_hours} = (\text{approved\_at} - \text{purchase\_timestamp})$ dalam satuan jam.
- $\text{seller\_ buyer\_distance\_km}$: Jarak geografis Haversine antara kode pos penjual dan pembeli.

### 3. Fitur Perilaku & Histori Pelanggan (As-Of Behavioral Features)
- `prior_order_count`: Jumlah pesanan pelanggan *sebelum* transaksi saat ini.
- `prior_avg_order_value`: Rata-rata nilai pesanan historis.
- `prior_avg_review_score`: Rata-rata skor ulasan yang pernah diberikan sebelumnya.
- `days_since_first_order` dan `days_since_prev_order`.
- `distinct_categories_bought`: Keragaman kategori produk yang pernah dibeli.

### 4. Fitur Interaksi Non-Linear (Interaction Features)
- $\text{delay\_x\_freight\_ratio} = \max(0, \text{delivery\_delay\_days}) \times \text{freight\_ratio}$ (menguji efek gabungan barang dengan ongkir mahal yang juga datang terlambat).
- $\text{distance\_x\_weight} = \text{seller\_buyer\_distance\_km} \times \log(1 + \text{product\_weight\_g})$.
- $\text{high\_value\_late\_flag} = \mathbb{I}(\text{total\_order\_value} > Q_{0.75}) \times \text{is\_late}$.

### 5. Representasi Teks & Deep Learning Features
- Panjang karakter dan jumlah kata komentar ulasan (`comment_length`, `word_count`).
- Fitur TF-IDF / n-gram untuk model klasik (Naive Bayes / Linear).
- Token indeks sekuensial dan *Categorical Entity IDs* (`category_idx`, `state_idx`) untuk lapisan *Embedding* pada arsitektur *Neural Network / Deep Learning*.

## 6.3 Protokol Anti-Leakage (Zero Data Leakage Guarantee)

Setiap fitur yang masuk ke dalam model wajib lulus pemeriksaan `tests/test_leakage.py`:
1. **Point-in-Time Correctness:** Jika model bertugas memprediksi risiko keterlambatan pada saat pesanan dibuat (*at checkout*), fitur `order_delivered_customer_date` atau `review_score` **dilarang keras** masuk sebagai prediktor.
2. **First-Order Isolation untuk Prediksi Retensi:** Ketika memprediksi apakah pelanggan baru akan melakukan pembelian kedua (`repeat_purchase_flag`), seluruh fitur prediktor hanya boleh diekstrak dari **transaksi pertama** pelanggan tersebut, bukan agregasi dari seluruh transaksi seumur hidupnya (karena agregasi seluruh transaksi secara implisit membocorkan informasi bahwa pelanggan tersebut bertransaksi lebih dari sekali).
3. **Split-Before-Transform:** Semua proses *StandardScaler*, *MinMaxScaler*, *Target Encoding*, *TF-IDF Vectorizer*, dan imputasi nilai hilang **wajib** melakukan `.fit()` hanya pada *Training Set* (periode waktu awal) dan menerapkan `.transform()` pada *Validation* serta *Test Set* (periode waktu berikutnya).

---

# 7. KEBIJAKAN KLAIM ILMIAH & EVIDENCE REGISTRY

CSIP menegakkan pemisahan tegas antara deskripsi data, kemampuan prediksi, asosiasi statistik, dan klaim sebab-akibat.

## 7.1 Empat Level Klaim Ilmiah (Claim Levels)

| Level | Kategori Klaim | Makna Metodologis | Syarat Pembuktian Minimum dalam CSIP |
|---|---|---|---|
| **L0** | **Descriptive** | Menggambarkan fakta atau distribusi yang teramati pada sampel dataset. | Validasi kualitas data (Unit 4) dan statistik deskriptif yang akurat. |
| **L1** | **Predictive** | Model mampu memprediksi target $Y$ pada data baru (*out-of-sample*) lebih baik dari baseline. | Validasi temporal (*out-of-time test set*), bebas *leakage*, metrik evaluasi terkalibrasi. |
| **L2** | **Associational** | Variabel $X$ memiliki hubungan statistik yang terukur dengan $Y$ setelah mengontrol variabel teramati $\mathbf{Z}$. | Uji hipotesis multivariat, interval kepercayaan ($CI$), koreksi *multiple testing*, dan uji stabilitas sub-sampel. |
| **L3** | **Causal** | Perubahan pada $X$ menyebabkan perubahan pada $Y$ melalui identifikasi kausal yang valid. | Desain identifikasi eksplisit (DAG, *Matching/IPW*, *DiD*, atau *IV*), uji *overlap/positivity*, dan *sensitivity analysis* terhadap *unobserved confounding*. |

**Aturan Keras:** Nilai *Feature Importance* atau SHAP dari model Random Forest/LightGBM/Deep Learning **hanya mendukung klaim L1/L2** (bagaimana model menggunakan fitur untuk memprediksi), dan **tidak pernah** otomatis menjadi bukti L3 (kausalitas di dunia nyata).

## 7.2 Sistem Peringkat Bukti (Evidence Grade A–D)

| Grade | Status Bukti | Kriteria Penilaian | Kelayakan Penggunaan Keputusan |
|---|---|---|---|
| **Grade A** | **Kuat & Tervalidasi** | Lulus seluruh *validation gates*, konsisten lintas segmen/waktu, mengalahkan baseline secara signifikan, sensitivitas rendah terhadap asumsi. | Layak menjadi dasar utama rekomendasi keputusan dalam domain yang diuji. |
| **Grade B** | **Cukup / Bersyarat** | Didukung bukti statistik/prediktif yang valid, namun memiliki keterbatasan cakupan atau sensitivitas moderat terhadap asumsi tertentu. | Layak untuk rekomendasi bersyarat dengan pencantuman batasan secara eksplisit. |
| **Grade C** | **Eksploratif / Lemah** | Pola menarik tetapi ukuran sampel kecil, belum stabil lintas waktu, atau bergantung kuat pada parameter yang diasumsikan. | Hanya untuk bahan eksplorasi lanjutan; tidak boleh dijadikan dasar keputusan operasional. |
| **Grade D** | **Tidak Terbukti / Gagal** | Hipotesis ditolak oleh data, model gagal mengalahkan *naive baseline*, atau validasi gagal. | Disimpan di *Failure Register* sebagai pembelajaran ilmiah; dilarang digunakan untuk rekomendasi. |

---

# 8. SKENARIO PEMODELAN, MACHINE LEARNING, & DEEP LEARNING
*(Pemenuhan SKKNI Unit 8, Unit 9, & 16 Kompetensi Kurikulum)*

## 8.1 Strategi Pembagian Data Temporal (SKKNI Unit 8: Membangun Skenario Model)

Karena perilaku transaksi memiliki ketergantungan waktu, tren musiman, dan perubahan struktur pasar, penggunaan *random train-test split* sebagai satu-satunya evaluasi dilarang untuk klaim utama. CSIP menggunakan **Temporal Split Architecture**:

```text
Linimasa Dataset Olist (2016 - 2018):
|================ TRAINING SET (T_train) ================|=== VALIDATION (T_val) ===|=== LOCKED TEST (T_test) ===|--- Censoring Buffer ---|
```
1. **Training Set ($T_{\text{train}}$):** Digunakan untuk melatih parameter model, *fit* transformasi fitur, dan pencarian pola awal.
2. **Validation Set ($T_{\text{val}}$):** Periode waktu setelah $T_{\text{train}}$, digunakan untuk *hyperparameter tuning*, pemilihan fitur, dan penentuan *threshold* klasifikasi.
3. **Locked Holdout Test Set ($T_{\text{test}}$):** Periode waktu paling akhir (dikurangi *buffer* jendela observasi *right-censoring*), hanya dibuka untuk evaluasi final (SKKNI Unit 10).

## 8.2 Baseline Ladder (Tangga Pembanding Model)

Setiap tugas pemodelan wajib melewati tangga komparasi berikut agar kompleksitas model benar-benar terjustifikasi:
- **B0 — Naive Baseline:** Prediksi kelas mayoritas / rata-rata historis / aturan heuristik sederhana (misal: semua pesanan yang terlambat $> 3$ hari diprediksi memberikan ulasan buruk).
- **B1 — Statistical Baseline:** *Logistic Regression* (untuk klasifikasi) dan *Ordinary Least Squares / Ridge Linear Regression* (untuk regresi) dengan fitur dasar yang dapat diinterpretasikan secara langsung.
- **B2 — Classical Non-Linear & Instance/Probabilistic Benchmarks:** *Decision Tree*, *K-Nearest Neighbors (KNN)*, dan *Naive Bayes*.
- **B3 — Ensemble Tree Models:** *Random Forest* dan *Gradient Boosting (LightGBM)* dengan fitur konstruksi lengkap dan interaksi.
- **B4 — Neural Network & Deep Learning Models:** *Multi-Layer Perceptron (MLP) dengan Entity Embeddings*, serta arsitektur *Deep Learning* sekuensial/teks (1D-CNN / Bi-LSTM / Transformer-based atau TabNet).

## 8.3 Matriks Eksperimen Pemodelan (E0–E9)

| ID Eksperimen | Fokus Skenario Eksperimen | Model yang Diuji | Pertanyaan Teknis yang Dijawab |
|---|---|---|---|
| **E0** | *Naive & Heuristic Baseline* | Majority Class, Mean Predictor, Rule-based | Berapa batas bawah performa tanpa *Machine Learning*? |
| **E1** | *Economic Features Only* | Linear/Logistic Regression, LightGBM | Seberapa besar daya prediksi jika hanya menggunakan variabel harga dan ongkos kirim? |
| **E2** | *Experience & Fulfillment Only* | Logistic Regression, Decision Tree, LightGBM | Seberapa kuat indikator keterlambatan dan waktu pengiriman memprediksi kepuasan dan retensi? |
| **E3** | *Combined + Interaction Features* | Random Forest, LightGBM | Apakah penggabungan variabel ekonomi, pengalaman, dan interaksi non-linear meningkatkan $PR\text{-}AUC$ / menurunkan $RMSE$? |
| **E4** | *Imbalanced Handling Scenarios* | Class Weighting, SMOTE / Undersampling, Threshold Moving | Strategi mana yang paling optimal menangani ketimpangan kelas pada *repeat purchase* (~3–8% positif) tanpa merusak kalibrasi? |
| **E5** | *Unsupervised Behavioral Clustering* | K-Means, MiniBatch K-Means, DBSCAN / GMM | Berapa jumlah segmen perilaku pelanggan yang paling stabil dan memiliki interpretasi bisnis paling tajam? |
| **E6** | *Classical Algorithm Competency Lab* | KNN (dengan berbagai nilai $k$) & Naive Bayes (Gaussian/Multinomial) | Bagaimana performa KNN pada ruang fitur terstandarisasi dan Naive Bayes pada klasifikasi teks/ulasan? |
| **E7** | *Deep Learning 1 (Tabular NN)* | PyTorch/Keras MLP + *Categorical Entity Embeddings* + *Dropout/BatchNorm* | Apakah representasi *embedding* terpelajar pada kategori produk dan geografi mampu bersaing dengan model *tree-based*? |
| **E8** | *Deep Learning 2 (Sequence / Text / Time-Series)* | Bi-LSTM / 1D-CNN pada teks ulasan (`review_comment_message`) atau deret waktu transaksi | Seberapa besar peningkatan akurasi deteksi ketidakpuasan pelanggan ketika sinyal semantik teks ulasan diekstraksi dengan *Deep Learning*? |
| **E9** | *Ablation & Robustness Study* | Model Terbaik dari E3/E7/E8 | Komponen fitur mana yang jika dihapus paling menjatuhkan performa model, dan seberapa stabil model pada sub-populasi berbeda? |

## 8.4 Spesifikasi Implementasi 16 Kompetensi Kurikulum dalam CSIP

Tabel ini memastikan seluruh **16 modul pembelajaran** terimplementasi secara nyata di dalam repositori:

| No | Modul Kompetensi | Implementasi Spesifik dalam Proyek CSIP | Lokasi File / Notebook |
|---|---|---|---|
| **1** | **Pengenalan Data Science** | Perumusan kerangka kerja CRISP-DM + SKKNI, desain *research framing*, definisi objektif bisnis (Unit 1) dan tujuan teknis (Unit 2). | `README.md`, `01_data_understanding.ipynb` |
| **2** | **Dasar Pemrograman Python** | Pembuatan paket modular `src/csip` menggunakan fungsi murni, *type hinting*, *dataclasses*, *exception handling*, dan *unit testing* (`pytest`). | `src/csip/`, `tests/` |
| **3** | **Python for Data Science** | Manipulasi relasional 9 tabel Olist menggunakan vektorisasi NumPy, agregasi multi-indeks Pandas, *window functions*, dan operasi waktu. | `src/csip/data/`, `src/csip/features/` |
| **4** | **Data Visualization** | Pembuatan grafik distribusi, *heatmap* interaksi, kurva *survival/retention*, *calibration plot*, dan *dashboard* interaktif Plotly di Streamlit. | `03_eda.ipynb`, `app/pages/` |
| **5** | **Exploratory Data Analysis (EDA)** | Analisis univariat, bivariat, multivariat, analisis nilai hilang, deteksi *outlier*, dan ekstraksi fenomena kandidat untuk *Discovery Catalogue*. | `02_data_quality.ipynb`, `03_eda.ipynb` |
| **6** | **Machine Learning** | Desain *pipeline* `scikit-learn` (`ColumnTransformer`, `Pipeline`), strategi validasi silang temporal (*TimeSeriesSplit*), dan pencegahan *data leakage*. | `src/csip/models/`, `07_predictive_modeling.ipynb` |
| **7** | **Supervised Learning** | Perumusan masalah prediksi berlabel untuk klasifikasi biner (*repeat purchase*, *negative review*) dan regresi (*delivery delay*, *order value*). | `07_predictive_modeling.ipynb` |
| **8** | **Linear Regression** | Pemodelan OLS, Ridge ($L_2$), dan Lasso ($L_1$) untuk mengestimasi hubungan linier dan elastisitas biaya/jarak terhadap durasi pengiriman dan pengeluaran. | `06_hypothesis_investigation.ipynb`, `07_predictive_modeling.ipynb` |
| **9** | **Logistic Regression** | Baseline probabilistik (B1) untuk estimasi *Odds Ratio* faktor risiko keterlambatan terhadap kepuasan dan pembelian ulang. | `06_hypothesis_investigation.ipynb`, `07_predictive_modeling.ipynb` |
| **10** | **Decision Tree** | Pohon keputusan dengan pembatasan kedalaman (`max_depth`) untuk mengekstrak aturan keputusan (*decision rules*) yang transparan serta *ensemble* (RF/LightGBM). | `05_behavioral_discovery.ipynb`, `07_predictive_modeling.ipynb` |
| **11** | **Naive Bayes** | Implementasi *Multinomial/Complement Naive Bayes* untuk klasifikasi sentimen/topik cepat pada komentar ulasan dan *Gaussian NB* sebagai benchmark. | `07_predictive_modeling.ipynb` (Jalur Eksperimen E6) |
| **12** | **K-Nearest Neighbors (KNN)** | Klasifikasi dan pencarian kemiripan profil pelanggan/produk (*similarity search*) pada fitur numerik yang telah dinormalisasi (`StandardScaler`). | `07_predictive_modeling.ipynb` (Jalur Eksperimen E6) |
| **13** | **Unsupervised Learning** | Segmentasi perilaku pelanggan menggunakan *K-Means*, *GMM/DBSCAN*, dan reduksi dimensi (PCA/UMAP) pada *Behavioral Discovery Engine*. | `05_behavioral_discovery.ipynb`, `src/csip/discovery/` |
| **14** | **Neural Network** | Pembangunan arsitektur *Multi-Layer Perceptron (MLP)* dari dasar untuk data tabular dengan fungsi aktivasi ReLU/GELU, *Batch Normalization*, dan *Dropout*. | `07_predictive_modeling.ipynb` (Jalur Eksperimen E7) |
| **15** | **Deep Learning 1** | Optimasi jaringan saraf menggunakan *Entity Embeddings* untuk variabel kategorikal kardinalitas tinggi (kategori produk, kode wilayah), *learning rate scheduling*, dan *early stopping*. | `07_predictive_modeling.ipynb`, `src/csip/models/deep_tabular.py` |
| **16** | **Deep Learning 2** | Arsitektur *Deep Learning* lanjutan: model sekuensial/konvolusional (1D-CNN / Bi-LSTM) untuk representasi teks ulasan berbahasa Portugis atau peramalan deret waktu *World Model*. | `07_predictive_modeling.ipynb`, `10_world_model.ipynb`, `src/csip/models/deep_seq.py` |

---

# 9. EVALUASI DAN PROSES REVIEW PEMODELAN
*(Pemenuhan SKKNI Unit 10 & Unit 11)*

## 9.1 Metrik Evaluasi Komprehensif (SKKNI Unit 10: Mengevaluasi Hasil Pemodelan)

Evaluasi tidak boleh hanya mengandalkan satu angka *Accuracy* (terutama karena *repeat purchase* pada Olist sangat timpang / *imbalanced*). Setiap model dievaluasi menggunakan matriks metrik berikut:

1. **Metrik Klasifikasi (Repeat Purchase & Negative Review Risk):**
   - **PR-AUC (Precision-Recall AUC):** Metrik utama untuk kelas minoritas yang timpang.
   - **ROC-AUC:** Mengukur kemampuan pemisahan peringkat (*ranking*) secara keseluruhan.
   - **F1-Score, Precision@K, dan Recall@K:** Mengevaluasi efektivitas penargetan pada $K\%$ pelanggan berisiko tertinggi.
   - **Balanced Accuracy & Confusion Matrix** pada *threshold* optimal.
   - **Kalibrasi Probabilitas (*Brier Score* & *Reliability Diagram*):** Wajib dilakukan karena probabilitas prediksi model akan diumpankan ke dalam simulasi *World Model*. Jika probabilitas tidak terkalibrasi, digunakan *Platt Scaling* atau *Isotonic Regression*.
2. **Metrik Regresi (Delivery Lead Time & Spending):**
   - **MAE (Mean Absolute Error):** Kesalahan rata-rata dalam satuan asli (hari atau mata uang BRL).
   - **RMSE (Root Mean Squared Error):** Mengukur sensitivitas terhadap kesalahan prediksi yang besar (*outlier*).
   - **$R^2$ (Coefficient of Determination) & WAPE (Weighted Absolute Percentage Error).**
3. **Metrik Unsupervised Clustering:**
   - **Silhouette Coefficient**, **Davies-Bouldin Index**, **Calinski-Harabasz Index**, serta **Uji Stabilitas Klaster** (mengukur konsistensi penugasan klaster pada *bootstrap sub-samples*).
4. **Explainability & Error Analysis:**
   - Analisis nilai SHAP (*SHapley Additive exPlanations*) global dan lokal.
   - *Subgroup Error Auditing*: Memeriksa apakah error model terpusat pada wilayah geografis tertentu atau kategori produk tertentu.

## 9.2 Protokol Review Pemodelan (SKKNI Unit 11: Melakukan Proses Review Pemodelan)

Sesuai dengan Unit Kompetensi ke-11 SKKNI, tahap pemodelan tidak berakhir saat metrik dihitung. Tim/pengembang wajib melaksanakan **Proses Review Pemodelan Formal** yang didokumentasikan dalam `13_failure_analysis.ipynb` dan `reports/model_report.md`:

1. **Audit Ketercapaian Tujuan Teknis vs Objektif Bisnis:**
   - Menilai apakah peningkatan metrik teknis (misal: kenaikan $PR\text{-}AUC$ sebesar $+0.08$) benar-benar memberikan nilai tambah praktis bagi keputusan bisnis dibandingkan aturan heuristik sederhana.
2. **Ablation Study (Uji Pelucutan Komponen):**
   - Mengukur penurunan performa ketika kelompok fitur tertentu (misal: fitur keterlambatan pengiriman atau *embedding* teks ulasan) dilepas dari model. Jika sebuah kelompok fitur kompleks tidak memberikan kontribusi nyata ($\Delta \text{Metrik} \approx 0$), fitur tersebut dipangkas demi efisiensi.
3. **Pencatatan Failure Register (Daftar Kegagalan & Batasan):**
   - Mendokumentasikan secara transparan hipotesis yang ditolak, segmen data di mana model gagal memprediksi dengan baik, serta eksperimen algoritma yang tidak mengungguli baseline.
4. **Rekomendasi Perbaikan Iteratif (Model Improvement Plan):**
   - Menyusun langkah tindak lanjut konkret: apakah perbaikan berikutnya memerlukan penambahan data eksternal, penyesuaian *hyperparameter*, kalibrasi ulang *threshold*, atau perubahan definisi jendela waktu kohort.

---

# 10. WORLD MODEL & ALTERNATIVE WORLD SIMULATION ENGINE

## 10.1 Struktur World Model

*World Model* CSIP mengintegrasikan komponen prediktif yang telah terkalibrasi ke dalam model sistem mingguan/kohort untuk mengevaluasi dampak kebijakan di tingkat ekosistem:

1. **Variabel Keadaan ($\mathbf{S}_t$):**
   - Volume pesanan masuk ($O_t$), rata-rata harga produk ($\bar{P}_t$), rata-rata rasio ongkir ($\bar{F}_t$).
   - Distribusi waktu pengiriman ($\text{LeadTime}_t$) dan tingkat keterlambatan ($\text{DelayRate}_t$).
   - Tingkat kepuasan rata-rata ($\overline{\text{Review}}_t$) dan proporsi ulasan negatif ($\text{NegRate}_t$).
   - Ekspektasi tingkat pembelian ulang kohort ($\widehat{\text{RepeatRate}}_t$).
2. **Variabel Intervensi Skenario ($\mathbf{A}_t$):**
   - **Skenario Ekonomi:** Subsidi atau kenaikan ongkos kirim sebesar $\delta_F \in [-30\%, +30\%]$.
   - **Skenario Operasional Logistik:** Pengurangan rata-rata keterlambatan pengiriman sebesar $\delta_D$ hari atau pemangkasan ekor keterlambatan ekstrem (*tail-risk reduction* pada persentil ke-90).
   - **Skenario Kombinasi (Joint Policy):** Subsidi ongkir terarah khusus untuk kategori produk berat/jarak jauh yang dikombinasikan dengan perbaikan SLA pengiriman.

## 10.2 Tiga Lapis Validasi Simulasi & Kuantifikasi Ketidakpastian

1. **Lapis 1 — Synthetic Recovery Validation:** Menguji mesin simulasi pada data sintetis dengan parameter struktural yang diketahui secara pasti untuk memastikan kode simulasi mampu memulihkan efek yang sebenarnya tanpa bias pemrograman.
2. **Lapis 2 — Historical Replay Backtesting:** Menjalankan *World Model* dari minggu $t_0$ hingga $t_k$ pada periode historis dan membandingkan lintasan proyeksi sistem dengan realisasi aktual di dataset.
3. **Lapis 3 — Uncertainty & Extrapolation Guardrails:**
   - Menghasilkan rentang ketidakpastian ($50\%$ dan $90\%$ *Prediction Intervals*) menggunakan *Monte Carlo / Residual Bootstrapping*.
   - **Extrapolation Warning System:** Jika pengguna di antarmuka Streamlit memasukkan parameter simulasi di luar rentang dukungan data historis (misal: memotong waktu pengiriman hingga $0$ hari atau menaikkan ongkir $500\%$), sistem wajib memunculkan peringatan merah **OUT-OF-DISTRIBUTION EXTRAPOLATION WARNING** dan menurunkan *Evidence Grade* simulasi menjadi **Grade C/D**.

---

# 11. ARSITEKTUR TEKNIS & DESAIN APLIKASI STREAMLIT

## 11.1 Arsitektur Tiga Lapis (Three-Tier Architecture)

1. **Lapis 1 — Research & Evidence Layer (`notebooks/`):**
   - 14 Jupyter Notebooks terstruktur yang menjadi sumber kebenaran ilmiah (*single source of truth*), mencakup langkah SKKNI Unit 1 hingga Unit 11 secara berurutan.
2. **Lapis 2 — Core Python Package (`src/csip/`):**
   - Kode produksi yang bersih, modular, terdokumentasi (*docstrings*), dan diuji dengan `pytest`. Tidak boleh ada duplikasi logika rumus antara *notebook* dan aplikasi UI.
3. **Lapis 3 — Decision Showcase Layer (`app/`):**
   - Aplikasi Streamlit multi-halaman yang membaca artefak tervalidasi (`artifacts/models/`, `artifacts/reports/`, `data/processed/`) untuk menyajikan eksplorasi interaktif dan simulasi *real-time* ringan tanpa menjalankan *training* berat di UI.

## 11.2 Spesifikasi 9 Halaman Aplikasi Streamlit

| No | Nama Halaman Streamlit | Konten & Fitur Interaktif Utama | Keterkaitan Unit SKKNI |
|---|---|---|---|
| **1** | **CSIP Executive Overview** | Ringkasan objektif bisnis, tujuan teknis, status *Validation Gates* (G0–G11), metrik utama ekosistem, dan ringkasan temuan kunci. | Unit 1 & Unit 2 |
| **2** | **Data Observatory & Quality** | Inventaris 9 tabel Olist, *schema graph*, laporan validasi kualitas data, distribusi *missing values*, dan *timestamp sanity audit*. | Unit 3, Unit 4, Unit 5, Unit 6 |
| **3** | **Behavioral Discovery Lab** | Eksplorasi interaktif hasil *Unsupervised Clustering* (profil segmen pelanggan), peta interaksi non-linear (ongkir vs keterlambatan), dan *Discovery Catalogue*. | Unit 3, Unit 7, Unit 9 |
| **4** | **Hypothesis Laboratory** | Matriks investigasi hipotesis H1–H6, perbandingan penjelasan alternatif, forest plot *effect size* + $95\%$ CI, dan status bukti. | Unit 8, Unit 10, Unit 11 |
| **5** | **Predictive Intelligence (ML & DL)** | Papan peringkat (*leaderboard*) model B0–B4 (LogReg, RF, LightGBM, KNN, NB, MLP Embeddings, Deep Learning Text/Seq), kurva ROC/PR, kalibrasi, dan SHAP *explainer*. | Unit 8, Unit 9, Unit 10 |
| **6** | **System & World Model** | Visualisasi dinamika variabel keadaan mingguan ($\mathbf{S}_t$), struktur dependensi antar-komponen sistem, dan hasil *Historical Replay Backtesting*. | Unit 8, Unit 9, Unit 10 |
| **7** | **Alternative World Simulator** | Panel kontrol interaktif (*sliders*) untuk mengubah parameter ongkir, SLA pengiriman, dan komposisi segmen; menampilkan proyeksi *Baseline vs Alternative World* beserta *Prediction Interval* dan *Extrapolation Warning*. | Unit 8, Unit 9, Unit 10 |
| **8** | **Decision Intelligence Studio** | Analisis *trade-off* multi-objektif (biaya subsidi vs peningkatan retensi/kepuasan), matriks risiko, dan rekomendasi keputusan bersyarat. | Unit 1, Unit 10, Unit 11 |
| **9** | **Evidence Registry & Model Review** | Tabel audit klaim ilmiah (L0–L3), *Evidence Grade* (A–D), hasil *Ablation Study*, *Failure Register*, keterbatasan data, dan metadata reprodusibilitas. | Unit 11 |

---

# 12. STRUKTUR REPOSITORY & QUALITY GATES

## 12.1 Struktur Direktori Standar Industri

```text
CSIP/
│
├── README.md                         # Dokumentasi utama, panduan instalasi, & pemetaan SKKNI/BNSP
├── pyproject.toml                    # Konfigurasi paket Python & dependensi
├── requirements.txt                  # Daftar pustaka terkunci (locked dependencies)
├── Makefile                          # Otomasi pipeline (make data, make test, make train, make app)
│
├── config/
│   ├── business_objectives.yaml      # [SKKNI 1 & 2] Target bisnis & metrik teknis DS
│   ├── data.yaml                     # [SKKNI 3, 4, 5] Skema tabel, grain, & aturan cohort
│   ├── features.yaml                 # [SKKNI 6 & 7] Spesifikasi pembersihan & konstruksi fitur
│   ├── models.yaml                   # [SKKNI 8 & 9] Konfigurasi baseline, ML, & Deep Learning
│   └── scenarios.yaml                # [SKKNI 8] Parameter simulasi Alternative World & batas validitas
│
├── data/
│   ├── raw/                          # 9 file CSV asli Olist (diabaikan oleh Git)
│   ├── interim/                      # Data yang telah divalidasi & dibersihkan (Parquet/DuckDB)
│   ├── processed/                    # Analytical datasets siap pakai untuk pemodelan
│   ├── synthetic/                    # Dataset sintetis untuk validasi pemulihan parameter simulasi
│   └── data_dictionary.md            # Kamus data lengkap seluruh tabel dan fitur turunan
│
├── notebooks/
│   ├── 01_business_and_data_understanding.ipynb   # [SKKNI 1, 2, 3] Objektif bisnis, tujuan teknis, & telaah awal
│   ├── 02_data_validation_and_cleaning.ipynb      # [SKKNI 4, 5, 6] Validasi skema, pemilihan objek, & pembersihan
│   ├── 03_exploratory_data_analysis.ipynb         # [SKKNI 3] EDA mendalam & visualisasi multivariat
│   ├── 04_feature_engineering_and_construction.ipynb # [SKKNI 7] Konstruksi fitur & verifikasi anti-leakage
│   ├── 05_behavioral_discovery_unsupervised.ipynb # [SKKNI 9] Clustering perilaku & Discovery Catalogue
│   ├── 06_hypothesis_investigation.ipynb          # [SKKNI 8, 9] Pengujian hipotesis H1-H6 & penjelasan alternatif
│   ├── 07_supervised_ml_and_competency_lab.ipynb  # [SKKNI 8, 9] Regresi, Klasifikasi, Tree, KNN, Naive Bayes
│   ├── 08_neural_network_and_deep_learning.ipynb  # [SKKNI 9] MLP Entity Embeddings & Deep Learning (Text/Seq)
│   ├── 09_model_evaluation_and_explainability.ipynb # [SKKNI 10] Evaluasi temporal, kalibrasi, & SHAP
│   ├── 10_system_and_world_modeling.ipynb         # [SKKNI 9, 10] State transition model & historical replay
│   ├── 11_alternative_world_simulation.ipynb      # [SKKNI 8, 10] Simulasi skenario intervensi & sensitivitas
│   ├── 12_uncertainty_quantification.ipynb        # [SKKNI 10] Prediction intervals & bootstrap analysis
│   ├── 13_model_review_and_failure_analysis.ipynb # [SKKNI 11] Ablation study, Failure Register, & review model
│   └── 14_final_research_and_bnsp_report.ipynb    # [SKKNI 1-11] Ringkasan eksekutif & bukti portofolio BNSP
│
├── src/
│   └── csip/
│       ├── __init__.py
│       ├── data/                     # Loader, schema validator, & data profiling (SKKNI 3, 4, 5)
│       ├── cleaning/                 # Deduplikasi, filtering status, & imputasi (SKKNI 6)
│       ├── features/                 # Konstruksi fitur ekonomi, pengalaman, & teks (SKKNI 7)
│       ├── discovery/                # Unsupervised clustering & anomaly detection
│       ├── hypotheses/               # Hypothesis registry & statistical test runners
│       ├── models/                   # Wrapper model klasik, ensemble, & PyTorch/Keras DL (SKKNI 8, 9)
│       ├── evaluation/               # Metrik, kalibrasi, temporal split, & SHAP (SKKNI 10)
│       ├── world/                    # State transition engine
│       ├── scenarios/                # Alternative world simulator & extrapolation checker
│       ├── uncertainty/              # Bootstrap & interval estimators
│       └── evidence/                 # Evidence grading, claim validator, & model review (SKKNI 11)
│
├── app/
│   ├── streamlit_app.py              # Entry point aplikasi Streamlit
│   └── pages/                        # 9 halaman modul analitik & simulasi
│
├── artifacts/
│   ├── models/                       # Bobot model terlatih & pipeline preprocessor
│   ├── reports/                      # Tabel hasil eksperimen (JSON/Parquet) untuk UI
│   └── metadata/                     # Checksum data, konfigurasi seed, & log eksperimen
│
├── reports/
│   ├── skkni_bnsp_traceability_matrix.md # Dokumen pemetaan bukti untuk asesor BNSP
│   ├── data_quality_report.md
│   ├── discovery_report.md
│   ├── hypothesis_report.md
│   ├── model_evaluation_and_review_report.md
│   ├── scenario_simulation_report.md
│   └── evidence_and_failure_register.md
│
└── tests/
    ├── test_data_validation.py       # Menguji integritas skema & aturan validasi (SKKNI 4)
    ├── test_cleaning_and_grain.py    # Menguji ketepatan grain & bebas duplikasi (SKKNI 5, 6)
    ├── test_feature_leakage.py       # Menguji ketidakadaan kebocoran masa depan (SKKNI 7)
    ├── test_models_and_shapes.py     # Menguji pipeline ML & Deep Learning (SKKNI 9)
    ├── test_simulation_sanity.py     # Menguji konsistensi simulasi & batas ekstrapolasi
    └── test_artifact_parity.py       # Memastikan angka di Streamlit identik dengan Notebook
```

## 12.2 Gerbang Kualitas dan Validasi (12 Validation Gates)

Setiap tahap pengembangan wajib melewati *Validation Gate* berikut sebelum diizinkan lanjut ke tahap berikutnya:

| Gate | Tahap & Referensi SKKNI | Kriteria Lulus Wajib (Pass Criteria) |
|---|---|---|
| **G0** | *Business & Technical Framing* (Unit 1 & 2) | Dokumen objektif bisnis, tujuan teknis, metrik target, dan rencana analisis (`config/*.yaml`) terkunci sebelum pemodelan. |
| **G1** | *Data Exploration & Validation* (Unit 3 & 4) | Seluruh 9 tabel selesai ditelaah, anomalinya tercatat di *Data Quality Report*, dan `test_data_validation.py` berstatus PASS. |
| **G2** | *Object Selection & Cleaning* (Unit 5 & 6) | Definisi *grain* terdokumentasi, populasi bebas distorsi *right-censoring*, dan proses pembersihan bersifat deterministik. |
| **G3** | *Data Construction & Anti-Leakage* (Unit 7) | Seluruh fitur selesai dikonstruksi, transformasi di-*fit* hanya pada *train split*, dan `test_feature_leakage.py` berstatus PASS $100\%$. |
| **G4** | *Behavioral Discovery* (Unit 3 & 9) | Klaster perilaku pelanggan memiliki *Silhouette Score* yang terukur, stabil pada *sub-sampling*, dan katalog pola terbentuk. |
| **G5** | *Hypothesis Investigation* (Unit 8 & 10) | Hipotesis H1–H6 selesai diuji dengan penjelasan alternatif, ukuran efek + CI dilaporkan, dan koreksi *multiple testing* diterapkan. |
| **G6** | *Supervised ML & DL Modeling* (Unit 8 & 9) | Seluruh model pada *Baseline Ladder* (B0–B4) termasuk algoritma klasik (KNN, NB) dan *Deep Learning* (MLP/Seq) selesai dilatih secara adil. |
| **G7** | *Temporal Evaluation & Calibration* (Unit 10) | Evaluasi final dilakukan pada *locked temporal test set*, kurva kalibrasi diperiksa, dan analisis SHAP selaras dengan level klaim. |
| **G8** | *World Model Validation* (Unit 9 & 10) | Model transisi keadaan lulus *Synthetic Recovery Test* dan memiliki *error* yang terukur pada *Historical Replay*. |
| **G9** | *Scenario & Uncertainty Check* (Unit 8 & 10) | Simulasi *Alternative World* menampilkan *Prediction Interval* dan mengaktifkan peringatan otomatis saat terjadi ekstrapolasi. |
| **G10** | *Formal Model Review* (Unit 11) | *Ablation study* selesai, *Failure Register* terisi jujur, dan rekomendasi perbaikan model terdokumentasi. |
| **G11** | *Product Parity & BNSP Readiness* (Unit 1–11) | Paket Python, 14 Notebook, 9 Halaman Streamlit, dan Matriks Ketertelusuran SKKNI/BNSP sinkron $100\%$. |

---

# 13. ROADMAP IMPLEMENTASI (12 MINGGU) & DEFINITION OF DONE

## 13.1 Peta Jalan Eksekusi Terintegrasi SKKNI

| Minggu | Fokus Pengembangan | Unit SKKNI yang Diselesaikan | Output Utama |
|---|---|---|---|
| **Minggu 1** | Setup arsitektur repo, perumusan masalah bisnis, tujuan teknis DS, dan *analysis plan*. | **Unit 1 & Unit 2** | Repo Git, `config/`, Notebook 01 (Bagian Bisnis & Teknis) |
| **Minggu 2** | *Data ingestion*, penelaahan 9 tabel Olist, dan validasi integritas data. | **Unit 3 & Unit 4** | Notebook 01 & 02, `data_dictionary.md`, `data_quality_report.md` |
| **Minggu 3** | Penentuan objek data (*grain/cohort*), pembersihan data, dan EDA visualisasi mendalam. | **Unit 5 & Unit 6** | Notebook 02 & 03, modul `csip.cleaning`, dataset interim bersih |
| **Minggu 4** | Konstruksi fitur ekonomi, pengalaman, interaksi, teks, dan pengujian anti-leakage. | **Unit 7** | Notebook 04, modul `csip.features`, `test_feature_leakage.py` |
| **Minggu 5** | *Behavioral Discovery Engine*: Unsupervised clustering, profil segmen, dan deteksi anomali. | **Unit 8 & Unit 9** | Notebook 05, modul `csip.discovery`, `discovery_report.md` |
| **Minggu 6** | *Hypothesis Investigation Engine*: Pengujian statistik H1–H6 dan pembandingan penjelasan alternatif. | **Unit 8, Unit 9, Unit 10** | Notebook 06, modul `csip.hypotheses`, `hypothesis_report.md` |
| **Minggu 7** | Pemodelan *Supervised ML* (Linear, LogReg, Tree, RF, LightGBM, KNN, Naive Bayes). | **Unit 8 & Unit 9** | Notebook 07, modul `csip.models`, log eksperimen E0–E6 |
| **Minggu 8** | Eksperimen *Neural Network & Deep Learning* (MLP Embeddings & Text/Sequence DL) serta Evaluasi Temporal & SHAP. | **Unit 9 & Unit 10** | Notebook 08 & 09, model DL terlatih, laporan evaluasi & kalibrasi |
| **Minggu 9** | Pembangunan *System & World Model* serta *Historical Replay Backtesting*. | **Unit 9 & Unit 10** | Notebook 10, modul `csip.world` |
| **Minggu 10** | Pembangunan *Alternative World Simulator* dan kuantifikasi ketidakpastian (*Prediction Intervals*). | **Unit 8 & Unit 10** | Notebook 11 & 12, modul `csip.scenarios` & `csip.uncertainty` |
| **Minggu 11** | Proses *Review Pemodelan*, *Ablation Study*, *Failure Analysis*, dan penyusunan *Evidence Registry*. | **Unit 11** | Notebook 13, `evidence_and_failure_register.md` |
| **Minggu 12** | Pengembangan 9 halaman Streamlit, pengujian paritas otomatis, dan finalisasi portofolio BNSP. | **Seluruh Unit (1–11)** | Aplikasi Streamlit lengkap, Notebook 14, `skkni_bnsp_traceability_matrix.md` |

## 13.2 Definition of Done (Kriteria Selesai Mutlak)

Proyek CSIP dinyatakan **SELESAI (DONE)** dan siap diajukan untuk uji kompetensi/portofolio industri apabila seluruh daftar periksa berikut terpenuhi:
- [ ] **Kepatuhan SKKNI & BNSP:** Seluruh 11 Unit Kompetensi SKKNI memiliki bukti kode, analisis di *notebook*, dan laporan tertulis yang terhubung di `reports/skkni_bnsp_traceability_matrix.md`.
- [ ] **Kepatuhan 6 Target Pembelajaran & 16 Modul:** Seluruh metode dari eksplorasi data, regresi, klasifikasi, *unsupervised clustering*, hingga *Neural Network* dan *Deep Learning* telah diimplementasikan dan dievaluasi secara objektif.
- [ ] **Integritas Pipeline Data:** Seluruh pengujian otomatis pada folder `tests/` (validasi skema, *grain*, anti-leakage, dan paritas artefak) berjalan hijau (*100% Passed*).
- [ ] **Kejujuran Ilmiah:** Setiap temuan memiliki *Claim Level* (L0–L3) dan *Evidence Grade* (A–D); hipotesis yang ditolak atau model yang gagal tetap dilaporkan di *Failure Register*.
- [ ] **Kesiapan Produk Showcase:** Aplikasi Streamlit 9 halaman dapat dijalankan secara lokal dengan satu perintah (`streamlit run app/streamlit_app.py`) dan menampilkan seluruh hasil riset, model, serta simulasi secara interaktif dan akurat.