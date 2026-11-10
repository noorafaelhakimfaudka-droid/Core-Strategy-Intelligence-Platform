# LAPORAN BEHAVIORAL DISCOVERY ENGINE (LAPORAN SEGMENTASI PERILAKU)
**Kepatuhan Standar: SKKNI [UK-03 Menelaah Data], [UK-09 Membangun Model] & Validation Gate G4**
**Tanggal Pembuatan**: 2026-11-10 | **Dataset**: Olist Processed Order-Level (96,470 baris)

---

## 1. Ringkasan Eksekutif & Status Validation Gate G4

| Parameter Evaluasi | Hasil Evaluasi Empiris | Status Gate G4 |
|---|---|:---:|
| **Jumlah Klaster Optimal (k)** | **k = 3** (di antara k in [3, 4, 5, 6]) | **PASS** |
| **Silhouette Score** | **0.3865** | **PASS** |
| **Davies-Bouldin Index** | **1.2168** (Separasi antar-klaster terukur) | **PASS** |
| **Reduksi Dimensi PCA** | 2 Komponen menjelaskan varians multidimensi secara terukur | **PASS** |
| **Deteksi Anomali Perilaku** | **4,824 pesanan** (5% titik ekstrem berjarak > cutoff) | **PASS** |
| **Discovery Catalogue Terisi** | 3 Pola Asosiasi terdaftar di Evidence Registry (DISC-01 s/d DISC-03) | **PASS** |

---

## 2. Matriks Pemilihan Hyperparameter Klaster (k-range Evaluation)

| Nilai k | Silhouette Score | Davies-Bouldin Index | Calinski-Harabasz Index | Inersia |
|:---:|:---:|:---:|:---:|:---:|
| k=3 **(Optimal)** | 0.3865 | 1.2168 | 3124.5 | 56,676.86 |
| k=4 | 0.3485 | 1.2361 | 3214.7 | 48,866.38 |
| k=5 | 0.3483 | 1.1223 | 3333.3 | 42,501.74 |
| k=6 | 0.3602 | 0.9605 | 3552.8 | 36,751.62 |

---

## 3. Profil dan Persona Segmen Perilaku Pelanggan

### Segmen 0: High-Ticket Premium Basket
- **Ukuran Klaster**: 18,987 pesanan (19.68% dari total transaksi)
- **Tingkat Ulasan Negatif (<= 2 bintang)**: 15.2%
- **Tingkat Repeat Purchase**: 0.0%
- **Karakteristik Kunci**:
  - Median Order Value: 211.0 BRL
  - Freight Ratio: 13.0%
  - Delivery Days: 11.5 hari
  - Negative Review Rate: 15.2%

### Segmen 1: Fast Single-Item Convenience
- **Ukuran Klaster**: 75,244 pesanan (78.0% dari total transaksi)
- **Tingkat Ulasan Negatif (<= 2 bintang)**: 11.56%
- **Tingkat Repeat Purchase**: 0.0%
- **Karakteristik Kunci**:
  - Median Order Value: 86.9 BRL
  - Freight Ratio: 25.0%
  - Delivery Days: 10.0 hari
  - Negative Review Rate: 11.6%

### Segmen 2: High-Ticket Premium Basket
- **Ukuran Klaster**: 2,239 pesanan (2.32% dari total transaksi)
- **Tingkat Ulasan Negatif (<= 2 bintang)**: 30.73%
- **Tingkat Repeat Purchase**: 0.0%
- **Karakteristik Kunci**:
  - Median Order Value: 242.2 BRL
  - Freight Ratio: 31.0%
  - Delivery Days: 10.0 hari
  - Negative Review Rate: 30.7%

---

## 4. Implikasi Strategis & Rekomendasi Intervensi Bisnis
1. **Segmen Heavy Freight Friction**: Perlu dipertimbangkan intervensi subsidi ongkir bersyarat pada keranjang belanja multi-item untuk menurunkan friksi transaksi.
2. **Segmen Long Lead Time**: SLA pengiriman kurir mitra harus diprioritaskan di wilayah terluar untuk mencegah pembengkakan ulasan negatif.
3. **Segmen High-Ticket Premium Basket**: Pelanggan bernilai tinggi sensitif terhadap kepastian tanggal kirim; intervensi proaktif saat terjadi delay dapat menyelamatkan CLV.