# CSIP — Core Strategy & Intelligence Platform
### *Platform Machine Learning Perilaku Enterprise, Observatorium Konsep Drift Real-Time & Simulator Keputusan Operasional*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.162.4-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61.1-FF4B4B.svg?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.7.0-brightgreen.svg?style=flat-square)](https://lightgbm.readthedocs.io/)
[![Quality Gates](https://img.shields.io/badge/Quality%20Gates-8%2F8%20LULUS-success.svg?style=flat-square)](tools/verify_release.py)
[![Docker](https://img.shields.io/badge/Docker-Siap%20Pakai-2496ED.svg?style=flat-square&logo=docker&logoColor=white)](Dockerfile)
[![Lisensi: MIT](https://img.shields.io/badge/Lisensi-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## 1. Ringkasan Eksekutif & Realita Masalah Bisnis

**Core Strategy & Intelligence Platform (CSIP)** adalah sistem operasi analitis dan platform *machine learning & decision intelligence* skala *enterprise* yang dirancang untuk mengurai friksi operasional, memprediksi hambatan rantai pasok pengiriman barang, mengevaluasi tata kelola model, serta menerjemahkan wawasan prediktif menjadi rekomendasi keputusan operasional terukur dan dapat diaudit.

Platform perdagangan elektronik modern di wilayah geografis kepulauan atau benua (seperti ekosistem Olist Brasil dengan lebih dari $100.000$ transaksi pesanan di 27 negara bagian) menghadapi friksi operasional asimetris:
* **Hambatan Logistik & Keterlambatan Pengiriman:** Durasi transit pengiriman berkisar antara 2 hari hingga lebih dari 45 hari. Keterlambatan logistik memicu gelombang kekecewaan pelanggan dan menurunkan retensi secara drastis.
* **Dilema Label Tertunda (*Delayed Ground-Truth Labels*):** Penilaian kepuasan konsumen (skor ulasan/bintang) dan transaksi pemesanan ulang (*repeat purchase*) baru terjadi beberapa hari hingga beberapa bulan setelah transaksi pembelian pertama diselesaikan. Sistem analitik naif kerap terjebak dalam *lookahead target leakage* karena melatih model menggunakan fitur-fitur yang baru diketahui setelah pengiriman tiba di tangan konsumen.
* **Peluruhan Model & Konsep Drift (*Concept Decay*):** Fluktuasi musiman belanja (seperti lonjakan volume *Black Friday*), kenaikan tarif kargo logistik, serta kendala operasional kurir menyebabkan kalibrasi probabilitas model di lini produksi mengalami degradasi senyap.

**CSIP menjawab tantangan tersebut melalui arsitektur decoupled terpadu:**
1. **Partisi Temporal Ketat & Pencegahan Kebocoran Data:** Validasi silang berbasis jendela waktu bergerak (*expanding-window temporal CV*) dengan embargo pasca-pengiriman selama 90 hari, mengeliminasi kebocoran target dan fitur masa depan.
2. **Pemodelan Multi-Target Terkalibrasi:** Algoritma LightGBM presisi tinggi dipadukan dengan kalibrasi probabilitas *Platt Scaling* serta atribusi fitur berbasis *SHAP TreeExplainer*.
3. **Mesin Keputusan Bisnis (*Business Decision Engine*):** Lapisan *Decision Intelligence* terstruktur yang menerjemahkan estimasi probabilitas risiko dan keterlambatan logistik menjadi aksi operasional spesifik per fungsi (Logistik, CX, Merchant Ops, Eksekutif) dengan kuota triage harian terkonfigurasi.
4. **Tata Kelola Model Champion-Challenger (*Model Lifecycle Registry*):** Registri model dengan gerbang promosi otomatis (+1% perbaikan metrik, degradasi Brier <= 5%, lolos uji maturitas) serta kemampuan *rollback* instan ke model champion sebelumnya.
5. **Layanan Mikro Inferensi Terpisah (FastAPI):** Layanan API independen (`/predict/batch`, `/decisions/recommend`, `/models/registry`, `/monitor/drift`). Pada benchmark CPU lokal (`artifacts/reports/resource_benchmark.json`), inferensi batch 1.000 baris LightGBM memerlukan **4,33–13,02 ms** (~0,004–0,013 ms/baris) dan inferensi baris tunggal **2,62–3,78 ms**.
6. **Observatorium Konsep Drift Real-Time:** Mesin penghitung statistik tervektorisasi untuk memantau *Population Stability Index* (PSI), uji Kolmogorov-Smirnov, jarak Wasserstein, dan divergensi Jensen-Shannon.
7. **Kontrak Data & Garis Silsilah Kriptografis (*Data Contracts & Lineage*):** Validasi integritas 4-tingkat keparahan (INFO, WARNING, RECOVERABLE_ERROR, CRITICAL_FAILURE) disertai audit hash fisik SHA-256 berkas Parquet di disk.
8. **Kokpit Intelijen Terpadu 8-Modul (Streamlit):** Studio terpadu mencakup Intelijen Eksekutif, Bisnis, Data, Prediktif, Pelanggan, Keputusan, MLOps, dan Lab Riset Eksperimental dengan penegasan batas kausalitas.

---

## 2. Cakupan Analitik Lintas Sektor & Fleksibilitas Universal

CSIP tidak hanya terbatas pada studi kasus rantai pasok e-commerce, melainkan sebuah **Universal Causal Simulation & Decision Intelligence Platform** yang dioptimalkan untuk memproses data tabular apa pun dengan variabel kontinu yang saling berkorelasi:

> **Cakupan Analitik:** Optimal untuk metrik bisnis, transaksi, SDM, pemasaran, atau sains dengan variabel kontinu saling berkorelasi.

Platform ini menyediakan kapabilitas analitis serbaguna lintas domain industri:
* **Bisnis & Transaksi Pasar Modal / Komoditas:**
  - Pemodelan harga pasar aset digital/komoditas.
  - Optimasi margin profitabilitas, perputaran persediaan (*inventory turnover*), dan proyeksi arus kas operasional.
* **Manajemen SDM & People Analytics:**
  - Analisis produktivitas kerja, retensi talenta, kepuasan karyawan, dan perbandingan kompensasi terhadap masa kerja (*tenure*).
  - Deteksi dini kejenuhan kerja (*burnout*) dan prediksi pergantian staf (*attrition risk*).
* **Pemasaran, Pelanggan & Pertumbuhan Bisnis:**
  - Evaluasi efektivitas kampanye, *Customer Acquisition Cost* (CAC), *Customer Lifetime Value* (LTV).
  - Prediksi *churn* pelanggan dan elastisitas sensitivitas harga promosi.
* **Sains, Kesehatan & Riset Medis:**
  - Studi korelasi gaya hidup terhadap indikator risiko kesehatan klinis (tersedia dataset bawaan *Kasus 2: Risiko Kesehatan & Gaya Hidup*).
  - Analisis telemetri sensor industri IoT, yield reaksi kimia kontinu, dan evaluasi hasil eksperimen laboratorium.
* **Mesin Penelaah CSV Universal (Universal CSV X-Ray):**
  - Cukup unggah berkas CSV apa saja ke dalam studio. Sistem secara otomatis mendeteksi tipe data, menstandardisasi skala intuitif (misal: skor 1-5 dinormalisasi ke 0-100), membersihkan nilai hilang, dan membangun simulator interaktif secara instan.

---

## 3. Arsitektur Sistem Tingkat Tinggi

```mermaid
flowchart TD
    subgraph Data_Layer ["1. Rekayasa Data, Kontrak & Silsilah (Data Contracts & Lineage)"]
        RAW["Data Tabular (Olist E-Commerce, Custom CSV)"] --> CLEAN["Pembersihan Deterministik & Deduplikasi Geospasial"]
        CLEAN --> CONTRACTS["Kontrak Data 4-Tingkat (INFO/WARN/RECOVERABLE/CRITICAL)"]
        CONTRACTS --> GRAIN["Pemetaan Butiran Data (Order, Customer, Seller Grains)"]
        GRAIN --> LINEAGE["Audit Silsilah Hash SHA-256 Parquet Dinamis"]
        LINEAGE --> EMBARGO["Partisi Waktu Bergerak (Embargo 90 Hari, 4 Lipatan Waktu)"]
    end

    subgraph Modeling_Layer ["2. Mesin Pemodelan, Kalibrasi & Tata Kelola Model"]
        EMBARGO --> TRAIN_REG["Regressor Estimasi Keterlambatan (LightGBM)"]
        EMBARGO --> TRAIN_CLF["Peringatan Dini Checkout & Pasca-Pengiriman (LightGBM)"]
        EMBARGO --> CLUST["Segmentasi Perilaku Pelanggan (K-Means + Velocity RFM)"]
        TRAIN_CLF --> CALIB["Kalibrasi Probabilitas Platt Scaling (Brier: 0.0762)"]
        CALIB --> REGISTRY["Model Lifecycle Manager (Champion-Challenger + Rollback)"]
        TRAIN_REG --> REGISTRY
    end

    subgraph Decision_Layer ["3. Mesin Keputusan Bisnis (Business Decision Engine)"]
        REGISTRY --> RULES["Evaluator Aturan Risiko (Keterlambatan + Ulasan Negatif)"]
        RULES --> TRIAGE["Manajer Kapasitas & Alokasi Triage Kuota Harian"]
        TRIAGE --> RECS["Rekomendasi Terstruktur (Logistik, CX, Merchant Ops, Eksekutif)"]
    end

    subgraph Serving_Layer ["4. Layanan Mikro Inferensi Terpisah (FastAPI Microservice)"]
        REGISTRY --> API_SRV["Daemon FastAPI (Port 8000)"]
        RECS --> API_SRV
        API_SRV --> END_PRED["POST /predict/batch (4.3-13.0 ms / 1000 baris)"]
        API_SRV --> END_DEC["POST /decisions/recommend (Rekomendasi Operasional Batch)"]
        API_SRV --> END_MOD["GET /models/registry (Audit Champion-Challenger)"]
        API_SRV --> END_DRIFT["POST /monitor/drift (Metrik PSI, KS, Wasserstein)"]
    end

    subgraph UI_Layer ["5. Kokpit Intelijen Terpadu (Streamlit Unified Cockpit)"]
        API_SRV -.-> COCKPIT["Studio Terpadu Streamlit (Port 8501)"]
        COCKPIT --> MOD1["1. Executive Intelligence & KPI Ringkas"]
        COCKPIT --> MOD2["2. Business Intelligence & Analisis Olist"]
        COCKPIT --> MOD3["3. Data Intelligence & Profiling Kontrak"]
        COCKPIT --> MOD4["4. Predictive Intelligence & Kalibrasi"]
        COCKPIT --> MOD5["5. Customer Intelligence & Segmentasi"]
        COCKPIT --> MOD6["6. Decision Intelligence & Triage Aksi Operasional"]
        COCKPIT --> MOD7["7. ML Operations & Pemantauan Drift"]
        COCKPIT --> MOD8["8. Research Lab & Simulasi Skenario 'What-If'"]
    end
```

---

## 4. Keunggulan Ilmiah & Ketegasan Metodologi

### A. Isolasi Temporal Ketat & Eliminasi Kebocoran Data
Berbeda dengan pemodelan konvensional yang kerap mencampur data masa depan ke dalam pelatihan, CSIP membagi ketersediaan fitur berdasarkan titik pos operasional secara tegas:

| Pos Operasional | Fitur yang Sah Digunakan | Data yang Diblokir Ketat (Risiko Kebocoran) |
| :--- | :--- | :--- |
| **Titik Checkout ($T_0$)** | Item keranjang, dimensi barang, estimasi biaya logistik, jarak geospasial penjual-pembeli, metode pembayaran. | Tanggal aktual barang sampai, catatan mutasi kurir transit, teks ulasan pembeli, nilai rating bintang. |
| **Disposisi Kurir ($T_1$)** | Durasi persiapan penjual, tanggal estimasi batas serah kurir, profil historis rute transit. | Status penerimaan aktual oleh konsumen, konfirmasi ulasan, transaksi repeat order berikutnya. |
| **Pasca-Pengiriman ($T_2$)** | Durasi pengiriman aktual, selisih hari keterlambatan terhadap estimasi, status pemenuhan kurir. | Pesanan baru dari pelanggan yang sama dalam jendela 90 hari (dibendung oleh embargo 90 hari). |

### B. Probabilitas Terkalibrasi vs. Skor Mentah Algoritma
Model klasifikasi *tree-based* bawaan sering kali menghasilkan skor prediksi yang terlalu percaya diri (*overconfident*). CSIP membungkus hasil inferensi dengan **Platt Scaling** eksternal pada `ModelExplainer` ($P(y=1|f) = \frac{1}{1 + \exp(Af + B)}$), yang berhasil mereduksi *Brier Score* dari $0.1375$ menjadi $0.0762$ ($-44.59\%$) serta memangkas *Expected Calibration Error* (ECE) dari $0.2355$ menjadi $0.0070$ ($-97.02\%$).

### C. Batas Identifikasi Parsial Manski untuk Estimand Retrospektif
Dalam menganalisis ketidakpuasan pasca-pengiriman di mana konsumen memiliki kebebasan untuk tidak mengisi ulasan, asumsi *missing-at-random* sering kali tidak terpenuhi. CSIP menerapkan batas terburuk (*worst-case bounds*) Manski:
$$P(Y=1|X) \in \left[ P(Y=1, R=1|X), \quad P(Y=1, R=1|X) + P(R=0|X) \right]$$
sehingga para pengambil kebijakan tidak salah mengartikan kepuasan umum dari sampel ulasan yang terseleksi secara mandiri.

---

## 5. Observatorium Konsep Drift & Peluruhan Performa Model

Modul pemantauan CSIP (`csip.monitoring`) memberikan pengawasan statistik secara *real-time* terhadap aliran data produksi tanpa membebani sistem dengan broker eksternal yang berat.

### Formulasi Matematis

#### 1. Population Stability Index (PSI)
Mengukur pergeseran kovariat antara distribusi acuan pelatihan ($P$) dan batch data produksi ($Q$) yang dibagi ke dalam $K=10$ kuantil:
$$PSI = \sum_{k=1}^{K} \left( Q_k - P_k \right) \times \ln\left( \frac{Q_k + \epsilon}{P_k + \epsilon} \right)$$
* **Hijau ($\text{PSI} < 0.10$):** Distribusi stabil; tidak memerlukan tindakan teknis.
* **Kuning ($0.10 \le \text{PSI} < 0.25$):** Pergeseran moderat; peringatan log dicatat untuk pemantauan berkala.
* **Merah ($\text{PSI} \ge 0.25$):** Terjadi pergeseran kovariat kritis; memicu protokol *retraining* otomatis.

#### 2. Jarak Wasserstein-1 (*Earth Mover's Distance*)
Mengukur energi minimum yang diperlukan untuk mengubah distribusi referensi menjadi distribusi saat ini:
$$W_1(u, v) = \int_{-\infty}^{\infty} |U(x) - V(x)| \, dx$$

#### 3. Pemantauan Prediksi via Divergensi Jensen-Shannon (JSD)
Mendeteksi anomali pada distribusi output probabilitas model secara berkelanjutan:
$$JSD(P \parallel Q) = \frac{1}{2} D_{KL}(P \parallel M) + \frac{1}{2} D_{KL}(Q \parallel M), \quad M = \frac{1}{2}(P + Q)$$

```
========================================================================================
RADAR PERGESERAN FITUR (Contoh Batch: Lonjakan Volume Black Friday W47)
----------------------------------------------------------------------------------------
freight_value              [████████████████████] PSI: 0.2841 (PERGESERAN KRITIS)
estimated_delivery_days    [█████████████░░░░░░░] PSI: 0.1620 (PERINGATAN MODERAT)
seller_customer_distance   [█████░░░░░░░░░░░░░░░] PSI: 0.0482 (STABIL)
product_weight_g           [███░░░░░░░░░░░░░░░░░] PSI: 0.0310 (STABIL)
----------------------------------------------------------------------------------------
STATUS: Peringatan Kritis Aktif -> Siklus Retraining Model Penantang Diluncurkan.
========================================================================================
```

---

## 6. Spesifikasi REST API Layanan Mikro (FastAPI)

CSIP dilengkapi dengan peladen mikro berbasis FastAPI (`src/csip/api/server.py`) yang berjalan asinkron untuk melayani kebutuhan inferensi dan telemetri pemantauan.

### Daftar Titik Akhir (Endpoints)

#### `GET /health` & `GET /ready`
Memeriksa kesehatan layanan dan probe kesiapan (*readiness probe* Kubernetes).
```bash
curl -X GET http://127.0.0.1:8000/health
curl -X GET http://127.0.0.1:8000/ready
```
**Respons Health (200 OK):**
```json
{
  "status": "healthy",
  "service_version": "1.0.0",
  "active_model_version": "champion_v1",
  "models_loaded": {
    "delivery_delay_regressor": true,
    "early_warning_review_classifier": true,
    "negative_review_classifier": true
  }
}
```

#### `POST /predict/batch`
Menerima kumpulan data pesanan baru dan menghasilkan estimasi keterlambatan logistik serta skor risiko ulasan negatif terkalibrasi. Mendukung header pelacakan `X-Request-ID`.
```bash
curl -X POST http://127.0.0.1:8000/predict/batch \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: req-abc-123" \
  -d '{
    "orders": [
      {
        "order_id": "ORD_001",
        "total_order_value": 149.90,
        "freight_value": 22.50,
        "freight_ratio": 0.15,
        "estimated_lead_time_days": 14.0,
        "seller_buyer_distance_km": 420.5,
        "product_weight_g": 1200.0,
        "product_photos_qty": 2.0,
        "payment_installments": 3.0,
        "approval_lag_hours": 1.2
      }
    ]
  }'
```
**Respons (200 OK):**
```json
{
  "batch_size": 1,
  "execution_time_ms": 2.94,
  "latency_per_record_ms": 2.94,
  "predictions": [
    {
      "order_id": "ORD_001",
      "predicted_delay_days": -2.41,
      "early_warning_risk_score": 0.0842,
      "risk_category": "LOW_RISK",
      "is_late_warning": false
    }
  ]
}
```

#### `POST /decisions/recommend`
Menerjemahkan kumpulan prediksi dan indikator pesanan menjadi rekomendasi operasional terstruktur per departemen dengan kuota triage harian.
```bash
curl -X POST http://127.0.0.1:8000/decisions/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "max_daily_capacity": 50,
    "orders": [
      {
        "order_id": "ORD_CRIT_01",
        "predicted_delay_days": 5.2,
        "early_warning_risk_score": 0.72,
        "customer_state": "RJ",
        "freight_ratio": 0.35
      }
    ]
  }'
```
**Respons (200 OK):**
```json
{
  "total_orders_evaluated": 1,
  "actionable_recommendations_count": 1,
  "capacity_limit": 50,
  "recommendations": [
    {
      "decision_id": "DEC-ORD_CRIT_01-LOGISTICS_DISPATCH",
      "order_id": "ORD_CRIT_01",
      "priority": "CRITICAL",
      "responsible_function": "LOGISTICS_DISPATCH",
      "recommended_action": "Eskalasi prioritas rute pengiriman dan investigasi carrier transit.",
      "evidence_type": "MODEL_PREDICTION",
      "explanation": "Prediksi delay kritis (+5.2 hari) melebihi batas toleransi logistik."
    }
  ]
}
```

#### `GET /models/registry`
Inspeksi tata kelola model, status champion-challenger aktif, dan riwayat promosi model.
```bash
curl -X GET http://127.0.0.1:8000/models/registry
```

#### `POST /monitor/drift`
Menghitung skor pergeseran fitur dan target secara langsung terhadap data referensi pelatihan.
```bash
curl -X POST http://127.0.0.1:8000/monitor/drift \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 500, "sample_orders": [...]}'
```

---

## 7. Papan Peringkat & Performa Model Empiris

Seluruh model dilatih pada kumpulan data $64.156$ baris dan dievaluasi pada partisi uji out-of-time terkunci (*locked holdout partition*, $N=12.571$) menggunakan skema lipatan waktu bergerak (*expanding-window temporal cross-validation*).

| Alur Model | Kategori Tugas | Pos Operasional | Metrik Utama (Holdout Terkunci) | Baseline Pembanding | Kalibrasi Probabilitas | Status Maturitas |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Estimasi Keterlambatan Pengiriman** | Regresi | Disposisi Kurir | **MAE: 4.8256 hari** ($R^2=0.3926$) | MAE: 8.42 hari ($R^2=0.012$) | N/A (Regresi) | PRODUCTION_APPROVED |
| **Peringatan Dini Ulasan Negatif** | Klasifikasi Imbalanced | Checkout ($T_0$) | **PR-AUC: 0.1335** (ROC-AUC: 0.5468) | PR-AUC: 0.0963 (Base Rate) | Raw LightGBM (Brier: 0.2370) | PILOT_RESTRICTED |
| **Prediksi Ulasan Negatif Retrospektif** | Klasifikasi Imbalanced | Pasca-Pengiriman ($T_2$) | **PR-AUC: 0.3061** (ROC-AUC: 0.6745) | PR-AUC: 0.0963 (Base Rate) | Raw Brier: 0.1373; External Platt: 0.0762 (ECE: 0.0070) | PILOT_ELIGIBLE |
| **Klasifikasi Sentimen Ulasan BiLSTM** | NLP Deep Learning | Pasca-Pengiriman ($T_2$) | **Macro-F1: 0.8420** | Macro-F1: 0.5210 (BoW) | Softmax Probs | PRODUCTION_CANDIDATE |
| **Segmentasi Perilaku Pelanggan** | Unsupervised | Pasca-Pengiriman ($T_2$) | **Silhouette: 0.4180** (K=4) | Silhouette: 0.2100 | Calinski-Harabasz: 1842 | PRODUCTION_APPROVED |
| **Prediksi Repeat Purchase Checkout** | Klasifikasi Biner | Checkout ($T_0$) | **ROC-AUC: 0.5021** (95% CI: $[0.472, 0.531]$) | ROC-AUC: 0.5000 (Random) | Tidak Signifikan | RESEARCH_ONLY (Valid Negative) |
| **Prediksi Repeat Purchase Pasca-Kirim** | Klasifikasi Biner | Pasca-Pengiriman ($T_2$) | **ROC-AUC: 0.6120** | ROC-AUC: 0.5000 (Random) | Sigmoid | EXPERIMENTALLY_VALIDATED |

> **Rekonsiliasi Provenansi Metrik:**
> - Metrik PR-AUC $0.3061$ dan ROC-AUC $0.6745$ dievaluasi secara ketat pada partisi uji out-of-time terkunci ($N_{test} = 12.571$, pesanan setelah 30 Juni 2018).
> - Nilai ROC-AUC $0.7517$ berasal dari evaluasi *subgroup robustness temporal holdout* pada slice pesanan setelah 1 Maret 2018 ($N_{holdout} = 39.153$), yang mencakup rentang musiman lebih panjang seperti dilaporkan dalam `MODEL_ROBUSTNESS_AND_SLICE_ANALYSIS.md`. Kedua nilai ini saling melengkapi pada subset temporal yang berbeda.

### Fungsi Kerugian Finansial Asimetris (*Asymmetric Cost Matrix*)
Penetapan ambang batas klasifikasi disesuaikan dengan matriks biaya riil operasional:
$$\mathcal{L}(\hat{y}, y) = C_{FP} \cdot \mathbb{I}(\hat{y}=1, y=0) + C_{FN} \cdot \mathbb{I}(\hat{y}=0, y=1)$$
Di mana kerugian akibat hilangnya pelanggan karena ulasan buruk yang tidak tertangani ($C_{FN} = \$45.00$) jauh lebih mahal daripada biaya intervensi proaktif layanan pelanggan ($C_{FP} = \$5.00$). Nilai ambang batas optimal berada di $\tau^* = 0.18$, menghemat biaya operasional hingga **$4.2\times$ lebih efisien** dibandingkan ambang standar $0.50$.

---

## 8. Arsitektur Antarmuka: Kokpit Intelijen Terpadu 8-Modul

Aplikasi utama CSIP berjalan sebagai **CSIP Studio (`app/streamlit_app.py`)** — kokpit analitik interaktif terpadu yang menyajikan 8 modul intelijen komprehensif:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ CSIP Studio  •  Core Strategy & Intelligence Platform  •  Platform Intelijen Keputusan   │
├──────────────────────────┬───────────────────────────────────────────────────────────────┤
│ 1. Executive Intelligence│ KPI Utama, Status Kesehatan Layanan & Matriks Kerugian        │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 2. Business Intelligence │ Analisis Keterlambatan Rantai Pasok & Hambatan Logistik Olist │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 3. Data Intelligence     │ Profiling Butiran Data, Kamus Data & Audit Kontrak 4-Tingkat │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 4. Predictive Intellig.  │ Kalibrasi Probabilitas Platt Scaling, PR-AUC & Atribusi SHAP │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 5. Customer Intelligence │ Segmentasi Perilaku K-Means, Matriks RFM & Analisis Kohor     │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 6. Decision Intelligence │ Mesin Rekomendasi Tindakan Operasional & Triage Kapasitas     │
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 7. ML Operations (MLOps) │ Observatorium Drift (PSI/KS/Wasserstein) & Champion-Challenger│
├──────────────────────────┼───────────────────────────────────────────────────────────────┤
│ 8. Research Lab (Exper.) │ Studio Simulasi 'What-If', 4 Lensa Analitik & Konsul Strategis│
└──────────────────────────┴───────────────────────────────────────────────────────────────┘
```

> **Catatan Teknis Arsitektur:** Antarmuka `app/streamlit_app.py` dirancang sebagai **Single-Page Cockpit** utuh tanpa menu navigasi bertingkat yang membingungkan. Seluruh kemampuan diagnostik — mulai dari simulasi keputusan non-linear, atribusi faktor penentu, analisis sebaran data, hingga observatorium deteksi drift longitudinal — terintegrasi secara modular dalam 4 Lensa Tampilan (*view lenses*) interaktif berkinerja tinggi.

---

## 9. Panduan Memulai Cepat & Reproduksi (Quickstart)

### Kebutuhan Perangkat Keras & Perangkat Lunak
* Python versi 3.10, 3.11, 3.12, atau 3.14.
* Spesifikasi: Laptop standar dengan RAM $\le$ 8 GB (dioptimalkan penuh untuk komputasi CPU tanpa dependensi GPU).
* Jejak Memori Terukur (`artifacts/reports/resource_benchmark.json`): Proses Python dengan 3 model LightGBM + sampel Parquet memiliki RSS terukur **263,68 MB** (`tracemalloc` peak **51,57 MB**).

### 1. Kloning Repositori & Penyiapan Virtual Environment
```bash
git clone https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform.git
cd Core-Strategy-Intelligence-Platform

# Buat lingkungan virtual mandiri
python -m venv .venv
# Pada Windows PowerShell / Command Prompt:
.venv\Scripts\activate
# Pada Linux / macOS:
source .venv/bin/activate

# Instal paket lokal dalam mode editable beserta dependensi inti
pip install -e .

# (Opsional, untuk reproduksi pipeline mentah dari nol) Verifikasi / unduh data mentah Olist
python scripts/download_raw_olist.py
```

### 2. Jalankan Layanan Mikro Inferensi FastAPI
```bash
python -m uvicorn csip.api.server:app --host 127.0.0.1 --port 8000
```

### 3. Jalankan Kokpit Studio Interaktif Streamlit
```bash
python -m streamlit run app/streamlit_app.py --server.port 8501
```
Buka peramban web pada alamat `http://localhost:8501`.

### 4. Eksekusi Pengujian Otomatis & Gerbang Kelayakan Rilis
```bash
# Jalankan seluruh rangkaian unit & integration test
pytest

# Evaluasi 8 Quality Gates kelayakan ML & integritas kode
python tools/verify_release.py

# Periksa kepatuhan anti-overclaim
python tools/check_claims.py
```

### 5. Deployment Menggunakan Docker
```bash
# Bangun citra container Docker
docker build -t csip-platform:latest .

# Jalankan container dengan memetakan port 8501 dan 8000
docker run -p 8501:8501 -p 8000:8000 csip-platform:latest
```

---

## 10. Struktur Direktori Proyek

```
csip/
├── .github/                      # Konfigurasi Alur CI/CD
│   └── workflows/ci.yml          # Matriks pengujian multi-versi Python
├── app/                          # Lapisan Antarmuka Pengguna Streamlit
│   ├── streamlit_app.py          # Kokpit Terpadu 8-Modul Intelijen & Studio Analitik
│   ├── api_server.py             # Pelari daemon FastAPI uvicorn
│   ├── data_provider.py          # Penyedia cache data terpusat
│   ├── ui_components.py          # Komponen tampilan dan CSS terintegrasi
│   └── style.css                 # Gaya desain editorial & tema aurora
├── artifacts/                    # Bukti Artefak Model & Evaluasi Nyata
│   ├── models/                   # Berkas model .joblib dan sidecar metadata .json
│   ├── metadata/                 # Registri model, ledger riwayat, dan matriks
│   └── reports/                  # Ringkasan evaluasi, kurva ROC/PR terkomputasi
├── config/                       # Konfigurasi Deklaratif Model & Analisis
│   ├── analysis_plan.yaml        # Parameter protokol analisis pra-registrasi
│   └── models.yaml               # Ruang pencarian hiperparameter algoritma
├── data/                         # Berkas Parquet Bersih & Kamus Data
│   ├── processed/                # Data pesanan dan pelanggan siap guna
│   ├── interim/                  # Tabel antara hasil pembersihan tahap satu
│   └── data_dictionary.md        # Dokumentasi skema dan tipe kolom
├── notebooks/                    # 14 Berkas Notebook Riset Tervalidasi
├── src/csip/                     # Paket Modul Python Inti
│   ├── api/                      # Peladen FastAPI dan pustaka Client SDK
│   ├── cleaning/                 # Pembersihan dan sanitasi data deterministik
│   ├── data/                     # Kontrak data 4-tingkat, pemuat, silsilah hash
│   ├── decision_engine/          # Mesin rekomendasi keputusan & manajer kapasitas
│   ├── discovery/                # Segmentasi klaster pelanggan K-Means
│   ├── evaluation/               # Evaluasi dampak bisnis, kalibrasi Platt, survival
│   ├── features/                 # Pembangun fitur terisolasi pos operasional
│   ├── hypotheses/               # Uji signifikansi hipotesis statistik
│   ├── models/                   # Pelatih algoritma LightGBM, SHAP, & registry siklus
│   └── monitoring/               # Mesin drift PSI/KS/Wasserstein & auto-retrainer
├── tests/                        # Rangkaian Pengujian Unit & Integrasi ML
├── tools/                        # Alat Verifikasi Standar & Integritas Klaim
│   ├── check_claims.py           # Pemindai kepatuhan bahasa anti-overclaim
│   └── verify_release.py         # Mesin verifikasi 8 Quality Gates ML & rilis
├── Dockerfile                    # Spesifikasi kontainerisasi produksi
├── Makefile                      # Perintah pintas otomatisasi build & test
└── pyproject.toml                # Konfigurasi build metadata standar PEP 517/518
```

---

## 11. Tata Kelola Data, Etika & Efisiensi Komputasi

1. **Privasi Lokal Terkendali:** Seluruh komputasi berjalan secara internal (*in-process*) atau lewat IPC lokal. Tidak ada data pribadi pelanggan, koordinat geospasial, atau teks transaksi yang dikirimkan ke API cloud pihak ketiga.
2. **Efisiensi Komputasi Tinggi:** Dirancang hemat sumber daya (<8 GB RAM dengan komputasi vektor NumPy/SciPy), memungkinkan implementasi skala *enterprise* pada perangkat keras standar tanpa beban biaya komputasi akselerator GPU eksternal.
3. **Reproduktifitas Penuh:** Semua proses stokastik diikat secara deterministik dengan nilai acak tetap (`seed=42`), dan keabsahan berkas data dijamin melalui pemeriksaan *checksum* kriptografis SHA-256 (`data/dataset_manifest.json`).

---

## 12. Lisensi & Sitasi

Proyek ini dirilis secara sumber terbuka (*open-source*) di bawah naungan **Lisensi MIT**.

```bibtex
@software{csip2026,
  author = {Rafael Hakim Souissa},
  title = {Core Strategy & Intelligence Platform (CSIP): Platform Pembelajaran Mesin Perilaku Enterprise & Observatorium Konsep Drift},
  year = {2026},
  url = {https://github.com/noorafaelhakimfaudka-droid/Core-Strategy-Intelligence-Platform}
}
```
