# CSIP (Computational Society Intelligence Platform)
## Modul MVP: Behavioral Decision Intelligence (BDI)
**Versi 2.0 — Master Edition (SKKNI, BNSP & Industry Portfolio Compliant)**

CSIP adalah platform *Observational Data Science* end-to-end yang dirancang untuk meneliti interaksi antara faktor ekonomi (harga produk, rasio ongkos kirim), pengalaman pemenuhan pesanan (kecepatan dan keterlambatan pengiriman), serta perilaku pembelian ulang (*repeat purchase*) pelanggan menggunakan dataset publik **Brazilian E-Commerce by Olist**.

---

## 1. Pemenuhan 11 Unit Kompetensi SKKNI (BNSP)

Proyek ini dirancang untuk memenuhi secara eksplisit **11 Unit Kompetensi SKKNI Bidang Data Science (Sertifikasi BNSP)**:

| No | Unit Kompetensi SKKNI | Implementasi dalam CSIP | Artefak & Bukti Verifikasi |
|:--:|:---|:---|:---|
| **UK-01** | **Menentukan Objektif Bisnis** | Perumusan masalah retensi, friksi biaya ongkos kirim, dan kepuasan pelanggan terhadap GMV & CLV. | `config/business_objectives.yaml`, `config/analysis_plan.yaml` |
| **UK-02** | **Menentukan Tujuan Teknis DS** | Penetapan metrik kuantitatif: PR-AUC & ROC-AUC ($\ge 0.65$), MAE delay, Silhouette score ($\ge 0.35$). | `config/models.yaml`, `config/business_objectives.yaml` |
| **UK-03** | **Menelaah Data** | Profiling relasional 9 tabel Olist, analisis tipe data, distribusi, dan eksplorasi EDA awal. | `src/csip/data/loader.py`, `data/data_dictionary.md` |
| **UK-04** | **Memvalidasi Data** | Audit integritas skema, deteksi missing values, duplikasi PK, dan uji kronologi timestamp pesanan. | `src/csip/data/loader.py`, `tests/test_data_validation.py` |
| **UK-05** | **Menentukan Objek Data** | Penetapan 4 grain analitik terpisah dan mitigasi right-censoring dengan jendela observasi seragam ($\Delta W = 90$ hari). | `config/data.yaml`, `tests/test_cleaning_and_grain.py` |
| **UK-06** | **Membersihkan Data** | Penyaringan status pesanan, deduplikasi koordinat geolokasi (median) & ulasan, penanganan outlier. | `src/csip/cleaning/` |
| **UK-07** | **Mengkonstruksi Data** | Rekayasa fitur ekonomi, pemenuhan pesanan, histori as-of, interaksi non-linear, dan audit anti-leakage. | `config/features.yaml`, `tests/test_feature_leakage.py` |
| **UK-08** | **Membangun Skenario Model** | Perancangan matriks eksperimen E0–E9, hipotesis alternatif H1–H6, dan validasi temporal out-of-time split. | `config/models.yaml`, `config/scenarios.yaml` |
| **UK-09** | **Membangun Model** | Pelatihan model statistik (B1), ML klasik (B2, B3), dan Deep Learning Tabular MLP + Text (B4). | `src/csip/models/`, `artifacts/models/` |
| **UK-10** | **Mengevaluasi Hasil Pemodelan** | Evaluasi holdout temporal, PR-AUC kurva, kalibrasi Brier score, analisis SHAP, dan verifikasi World Model. | `src/csip/evaluation/`, `reports/model_report.md` |
| **UK-11** | **Melakukan Proses Review Pemodelan** | Audit klaim ilmiah L0–L3, ablation study, pencatatan Failure Register, dan validasi paritas Streamlit. | `src/csip/evidence/registry.py`, `reports/evidence_table.md` |

---

## 2. Batasan Performa & Hardware (8 GB RAM Constraints)

Sistem dioptimalkan secara ketat untuk berjalan pada laptop Intel Core i5 generasi ke-11 dengan RAM 8 GB:
1. **Memory Downcasting Otomatis**: Numerik 64-bit diubah ke `float32` dan `int32`/`int16`; string berkardinalitas rendah diubah ke tipe `category`.
2. **DuckDB & Parquet Acceleration**: Agregasi dan query tabel besar dilakukan menggunakan DuckDB / Parquet tanpa melakukan join 9 tabel sekaligus di memori.
3. **No Heavy Training in UI**: Antarmuka Streamlit hanya membaca artefak terkomputasi (`artifacts/`) dan tidak menjalankan pelatihan model dalam siklus render.

---

## 3. Kebijakan Klaim Ilmiah (Claim Levels L0–L3 & Evidence Grades A–D)

Setiap output dan rekomendasi CSIP diatur oleh tingkatan klaim ilmiah:
- **L0 (Descriptive)**: Fakta distribusi sampel teramati.
- **L1 (Predictive)**: Model memprediksi target out-of-sample lebih baik dari baseline.
- **L2 (Associational)**: Variabel berasosiasi secara statistik setelah mengontrol pembaur (*confounders*).
- **L3 (Causal)**: Identifikasi kausal formal terpenuhi (hanya jika syarat identifikasi terpenuhi).
- **Evidence Grades**: **Grade A** (Kuat & Tervalidasi), **Grade B** (Cukup / Bersyarat), **Grade C** (Eksploratif), **Grade D** (Gagal / Failure Register).

---

## 4. Instalasi & Menjalankan Pengujian

```bash
# Clone atau masuk ke repositori
cd C:\Users\asus\.gemini\antigravity\scratch\csip

# Install dependensi
pip install -r requirements.txt

# Jalankan seluruh unit test otomatis
pytest tests -v
```
