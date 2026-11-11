# CSIP Research Notebook Execution Manifest
## End-to-End Scientific Workflow for E-Commerce Decision Intelligence

**Document ID**: `CSIP-MANIFEST-NOTEBOOKS-2026`  
**Target Certification**: BNSP Data Scientist KKNI Level 7  
**Standard**: SKKNI No. 299 Tahun 2020  
**Status**: AUDITED & 100% REPRODUCIBLE  
**Date**: November 2026  

---

## 1. Executive Overview

Proyek **Core Strategy & Intelligence Platform (CSIP)** menyusun 14 Jupyter Notebook penelitian yang merefleksikan alur kerja ilmiah Data Scientist secara menyeluruh dan sistematis. 

Setiap notebook mengadopsi struktur kanonikal:
1. **Research Objective**: Sasaran penelitian yang spesifik.
2. **Research Question**: Pertanyaan riset yang diuji.
3. **Dataset Description**: Sumber data, ukuran baris, dan fitur.
4. **Methodology**: Landasan teori dan algoritma yang digunakan.
5. **Implementation**: Kode Python yang terdokumentasi rapi.
6. **Results**: Metrik empiris dan visualisasi visual.
7. **Interpretation**: Penjelasan makna analitis temuan.
8. **Limitations**: Batasan teknis dan metodologis.
9. **Conclusion**: Kesimpulan ilmiah dan implikasi bisnis.

---

## 2. Notebook Execution Matrix (Sequential 01 s.d. 14)

| No. | File Notebook | Input Dataset | Output Artefak / Model | SKKNI Terkait | Status Eksekusi |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | `01_business_and_data_understanding.ipynb` | `data/raw/*.csv` (9 tabel) | `config/business_objectives.yaml` | UK-01, UK-02 | **VERIFIED** |
| **02** | `02_data_validation_and_cleaning.ipynb` | `data/raw/*.csv` (9 tabel) | `data/interim/*.parquet` (8 tabel) | UK-04, UK-05, UK-06 | **VERIFIED** |
| **03** | `03_exploratory_data_analysis.ipynb` | `data/interim/*.parquet` | `reports/data_quality_report.md` | UK-03 | **VERIFIED** |
| **04** | `04_feature_engineering_and_construction.ipynb` | `data/interim/*.parquet` | `data/processed/order_level.parquet` | UK-07 | **VERIFIED** |
| **05** | `05_behavioral_discovery_unsupervised.ipynb` | `data/processed/order_level.parquet` | `artifacts/models/clustering_pipeline.joblib` | UK-07 | **VERIFIED** |
| **06** | `06_hypothesis_investigation.ipynb` | `data/processed/order_level.parquet` | `reports/hypothesis_report.md` | UK-08 | **VERIFIED** |
| **07** | `07_supervised_ml_and_competency_lab.ipynb` | `data/processed/order_level.parquet` | `artifacts/models/champion_lightgbm.joblib` | UK-09 | **VERIFIED** |
| **08** | `08_neural_network_and_deep_learning.ipynb` | `data/processed/review_corpus.parquet` | `artifacts/models/deep_bilstm.pt` | UK-09 | **VERIFIED** |
| **09** | `09_model_evaluation_and_explainability.ipynb` | `artifacts/models/*` | `reports/model_evaluation_and_review_report.md` | UK-10 | **VERIFIED** |
| **10** | `10_system_and_world_modeling.ipynb` | `data/processed/weekly_system_state.parquet` | `artifacts/models/world_model.joblib` | UK-08 | **VERIFIED** |
| **11** | `11_alternative_world_simulation.ipynb` | `artifacts/models/world_model.joblib` | `reports/scenario_simulation_report.md` | UK-08, UK-10 | **VERIFIED** |
| **12** | `12_uncertainty_quantification.ipynb` | `data/processed/order_level.parquet` | Visualisasi Residual Bootstrap 95% CI | UK-10 | **VERIFIED** |
| **13** | `13_model_review_and_failure_analysis.ipynb` | Seluruh hasil pemodelan | `reports/evidence_and_failure_register.md` | UK-11 | **VERIFIED** |
| **14** | `14_final_research_report.ipynb` | Seluruh laporan dan registry | `reports/csip_data_scientist_technical_report.md` | UK-11 | **VERIFIED** |

---

## 3. Granular Notebook Audit Profiles

### Notebook 01: `01_business_and_data_understanding.ipynb`
- **Objective**: Memahami konteks marketplace e-commerce Brasil (Olist), perumusan masalah friksi logistik, dan penetapan baseline teknis.
- **Research Question**: Bagaimana friksi pengiriman dan struktur biaya logistik mempengaruhi retensi pelanggan di ekosistem Olist?
- **Key Results**: Identifikasi bahwa 97% pelanggan hanya melakukan satu kali transaksi; ongkos kirim menyumbang rata-rata 21.4% dari total nilai transaksi.
- **Limitations**: Data hanya mencakup transaksi marketplace yang difasilitasi oleh Olist, tidak mencakup transaksi di luar platform.

### Notebook 02: `02_data_validation_and_cleaning.ipynb`
- **Objective**: Melakukan validasi kualitas data, eliminasi anomali kronologis, dan deduplikasi spasial.
- **Key Results**: Eliminasi 23 record tanggal pengiriman terbalik; kompresi 1,000,163 baris koordinat mentah menjadi 19,010 titik median kode pos (-98.1%).
- **Verification**: Seluruh 8 file interim Parquet terverifikasi bebas missing value pada primary keys.

### Notebook 03: `03_exploratory_data_analysis.ipynb`
- **Objective**: Analisis distribusi bivariat dan profiling pola perilaku pelanggan terhadap waktu pengiriman.
- **Key Results**: Distribusi ulasan bintang 1 melonjak dari 4.2% pada pengiriman tepat waktu menjadi 43.8% pada pesanan yang terlambat lebih dari 3 hari (*cliff effect*).

### Notebook 04: `04_feature_engineering_and_construction.ipynb`
- **Objective**: Mengonstruksi 41 fitur analitis dan menegakkan isolasi temporal anti-kebocoran.
- **Key Results**: Konstruksi fitur `freight_ratio`, `seller_buyer_distance_km` (Haversine vectorized), dan `approval_lag_hours` tanpa melibatkan informasi pasca-pengiriman.

### Notebook 05: `05_behavioral_discovery_unsupervised.ipynb`
- **Objective**: Segmentasi persona pelanggan berbasis sensitivitas ongkos kirim dan karakteristik belanja.
- **Key Results**: Menemukan $k=3$ klaster optimal menggunakan K-Means dengan **Silhouette Score = 0.3865** (melampaui target $\ge 0.35$) dan Davies-Bouldin = 1.2168.

### Notebook 06: `06_hypothesis_investigation.ipynb`
- **Objective**: Pengujian hipotesis statistik H1 s.d. H6 dengan koreksi Benjamini-Hochberg False Discovery Rate (FDR).
- **Key Results**:
  - H1 (Elastisitas rasio ongkir): Terbukti ($p < 0.001$, $\eta^2 = 0.12$).
  - H2 (Asimetri penalti keterlambatan): Terbukti ($p < 0.001$, efek tebing > 3 hari).
  - H3 (Premi rating penjual terhadap GMV): DITOLAK ($p_{\text{adj}} = 0.859$, effect size $d = 0.012$, dicatat di Failure Register).

### Notebook 07: `07_supervised_ml_and_competency_lab.ipynb`
- **Objective**: Pelatihan bertingkat *Baseline Ladder* B0 s.d. B3 pada out-of-time test set.
- **Key Results**: LightGBM meraih Champion Tabular dengan **PR-AUC = 0.3004** (melampaui Naive 0.0814 sebesar +269% dan Random Forest 0.2842).

### Notebook 08: `08_neural_network_and_deep_learning.ipynb`
- **Objective**: Arsitektur deep learning Tabular MLP (Entity Embeddings) dan Text Bi-LSTM untuk klasifikasi keluhan pelanggan.
- **Key Results**: Bi-LSTM NLP meraih **PR-AUC = 0.8076** pada klasifikasi sentimen ulasan negatif; Tabular MLP meraih PR-AUC = 0.2915.

### Notebook 09: `09_model_evaluation_and_explainability.ipynb`
- **Objective**: Interpretasi model menggunakan SHAP TreeExplainer dan kalibrasi probabilitas Platt Scaling.
- **Key Results**: Platt scaling memangkas Brier Score sebesar **44.59%** (0.1375 ke 0.0762) dan ECE dari 0.2355 ke 0.0070. SHAP membuktikan keterlambatan menyumbang 31.2% massa atribusi.

### Notebook 10: `10_system_and_world_modeling.ipynb`
- **Objective**: Pemodelan dinamika sistem makro ekosistem mingguan menggunakan Vector AutoRegressive State-Space.
- **Key Results**: Model dunia meraih **WAPE = 15.83%** (melampaui batas toleransi KPI $\le 18\%$ dan mengungguli naive baseline WAPE 22.41%).

### Notebook 11: `11_alternative_world_simulation.ipynb`
- **Objective**: Simulasi skenario intervensi kebijakan operasional S0 s.d. S5 (subsidi ongkir terarah, percepatan rute logistik).
- **Key Results**: Skenario S2 (Subsidi ongkir selektif pada rute antar-negara bagian) diproyeksikan menghemat $14.2\%$ churn pelanggan dengan efisiensi subsidi $3.1\times$ dibanding subsidi merata.

### Notebook 12: `12_uncertainty_quantification.ipynb`
- **Objective**: Kuantifikasi ketidakpastian estimasi menggunakan residual bootstrap resampling ($B=1,000$).
- **Key Results**: Penaksiran 95% Confidence Interval untuk setiap proyeksi skenario kebijakan; margin ketidakpastian dicatat secara jujur.

### Notebook 13: `13_model_review_and_failure_analysis.ipynb`
- **Objective**: Review kritis seluruh model, pengelolaan Failure Register, dan penegakan hierarki klaim ilmiah L0-L3.
- **Key Results**: Pendokumentasian 3 kegagalan eksplisit (`FAIL-HYP-H3`, `FAIL-MOD-RIDGE`, `LIMIT-CAUSAL`) dan rekomendasi operasional mitigasi risiko.

### Notebook 14: `14_final_research_report.ipynb`
- **Objective**: Sintesis komprehensif temuan riset, dokumentasi arsitektur, dan laporan pertanggungjawaban kompetensi BNSP KKNI Level 7.
- **Key Results**: Laporan teknis lengkap siap audit dengan penelusuran 100% terhadap 11 unit SKKNI 299/2020.

