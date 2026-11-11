# Laporan Evaluasi Temporal Cross-Validation & Out-of-Time Testing

## 1. Protokol Evaluasi
- **Desain**: Expanding-window rolling-origin temporal cross-validation.
- **Embargo**: Minimal 90 hari kalender (`max(ts_train) + 90 hari <= min(ts_val)`).
- **Jumlah Fold**: 4 fold temporal.
- **Kumpulan Uji Terkunci**: Periode 2018-07-01 to 2018-08-29 (N=12448), dievaluasi tepat satu kali tanpa modifikasi fitur/threshold.

## 2. Hasil Cross-Validation per Model

| Model | Rata-rata PR-AUC | 95% CI PR-AUC | Rata-rata ROC-AUC | 95% CI ROC-AUC | Brier Score |
|---|---|---|---|---|---|
| **LightGBM** | 0.3825 | [0.3019, 0.5073] | 0.7130 | [0.6686, 0.7702] | 0.0902 |
| **LogisticRegression** | 0.3554 | [0.2922, 0.4597] | 0.7198 | [0.6874, 0.7664] | 0.0940 |

## 3. Rincian per Fold Temporal

| Fold | Rentang Training | Rentang Validasi | N Train | N Val | Base Rate | PR-AUC (LGBM) | ROC-AUC (LGBM) |
|---|---|---|---|---|---|---|---|
| 1 | 2016-09-15 s/d 2017-03-14 | 2017-06-13 s/d 2017-07-28 | 3683 | 5115 | 0.1003 | 0.2308 | 0.6248 |
| 2 | 2016-09-15 s/d 2017-07-05 | 2017-10-04 s/d 2017-11-18 | 14498 | 6707 | 0.1148 | 0.3729 | 0.7124 |
| 3 | 2016-09-15 s/d 2017-10-25 | 2018-01-24 s/d 2018-03-10 | 29787 | 10349 | 0.1998 | 0.6417 | 0.8279 |
| 4 | 2016-09-15 s/d 2018-02-15 | 2018-05-17 s/d 2018-07-01 | 53437 | 8316 | 0.1004 | 0.2846 | 0.6870 |

## 4. Evaluasi Kumpulan Uji Terkunci (Locked Out-of-Time Test Set)
- **Ukuran Sampel Uji**: 12448 transaksi
- **Base Rate Ulasan Negatif**: 0.0961 (9.61%)
- **PR-AUC**: **0.3151** (Mengungguli base rate secara signifikan)
- **ROC-AUC**: **0.6975**
- **Brier Score (Mentah)**: 0.0762
- **Brier Score (Terkalibrasi Platt)**: **0.0763**
- **ECE (Expected Calibration Error)**: 0.0054 -> **0.0098**
- **Brier Skill Score (BSS)**: **0.1215**
- **Top 5% Lift**: **5.15x**
- **Top 10% Lift**: **3.56x**

## 5. Batasan Metodologis
1. **Model Bersifat Retrospektif (Pasca-Delivery)**: Model risiko ulasan ini hanya dapat dijalankan setelah paket terkirim karena fitur keterlambatan (`delivery_delay_days`) membutuhkan konfirmasi tanggal penerimaan kurir.
2. **Missing Reviews (646 Pesanan)**: Berdasarkan analisis batas seleksi Manski, interval prevalensi ulasan negatif berada pada [11.44%, 12.10%], membuktikan efek seleksi non-respons ulasan tidak mengubah konklusi pemodelan secara material.
