# CSIP Master Evidence & Failure Register

**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**  
**Standard**: SKKNI Data Science (BNSP) — [UK-10 Mengevaluasi Hasil Pemodelan] & [UK-11 Mengembangkan Solusi]  
**Governance Protocol**: SHADOW Evidence Hierarchy (L0 to L3, Grades A to D)  
**Date**: November 2026  

---

## 1. Scientific Claim & Evidence Governance Principles

Every factual claim in CSIP is indexed with explicit evidence tiers:

- **Level L0 (Descriptive)**: Tabular summary statistics, aggregations, distributions, and empirical patterns without predictive or causal claims.
- **Level L1 (Predictive)**: Statistical and supervised ML out-of-time forecasting performance (PR-AUC, ROC-AUC, Brier score, ECE).
- **Level L2 (Associational)**: Correlational and regression relationships adjusting for observed confounders ($t$-statistics, odds ratios, adjusted $p$-values via Benjamini-Hochberg FDR).
- **Level L3 (Causal)**: Structural counterfactual interventions requiring formal identification assumptions.

**Evidence Grades**:
- **Grade A (Kuat & Tervalidasi)**: Empirical evidence replicated across multiple splits, controlled for FDR, or evaluated on locked test sets.
- **Grade B (Cukup / Bersyarat)**: Well-calibrated model projections within historical convex support.
- **Grade C (Spekulatif / Guardrail Triggered)**: Extrapolation scenarios or exploratory associations requiring cautious interpretation.
- **Grade D (Tidak Memadai)**: Uncalibrated or unverified assertions.

---

## 2. Master Discovery Register (DISC-01 to DISC-07)

| ID | Title | Claim Level | Evidence Grade | Grain | Summary Findings & Supporting Metrics |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **DISC-01** | High Freight Ratio Friction Segment | L0 (Descriptive) | Grade A | `order_id` | Segmen pembeli dengan rasio ongkos kirim tinggi (>35% nilai barang) mengalami risiko ulasan negatif yang meningkat 1.8x ($Risk\ Ratio = 1.78$). |
| **DISC-02** | Asymmetric Delivery Delay Penalty | L2 (Associational) | Grade A | `order_id` | Penurunan skor kepuasan bersifat asimetris: keterlambatan 1–3 hari menjatuhkan skor ke 2.5 bintang, sementara kedatangan lebih cepat tidak menambah skor melebihi 4.3 bintang ($F = 4218.1$, late slope = $-0.0638$, $p\text{-adj} = 0.0$). |
| **DISC-03** | Fast Single-Item Convenience Majority | L0 (Descriptive) | Grade A | `order_id` | 51.0% transaksi platform merupakan pembelian barang tunggal dengan ongkos kirim wajar dan waktu pengantaran cepat, membentuk fondasi volume platform. |
| **DISC-04** | Fulfillment Dominates Pricing in Review Attribution | L1 (Predictive) / L2 (Associational) | Grade A | `order_id` | SHAP TreeExplainer membuktikan bahwa keterlambatan (`delivery_delay_days`) dan interaksi non-linear (`delay_x_freight_ratio`) memegang 3.4x atribusi lebih besar dibanding harga barang atau ongkos kirim nominal. |
| **DISC-05** | Platt Scaling Restores Reliable Probability Estimates | L1 (Predictive) | Grade A | `order_id` | Di bawah ketimpangan kelas ekstrem, kalibrasi Platt scaling memangkas Brier score sebesar $44.59\%$ dan menurunkan Expected Calibration Error (ECE) dari $0.2355$ menjadi $0.0070$ ($97.02\%$ pengurangan error). |
| **DISC-06** | Macro System Transition Identifiability & Replay Fidelity | L1 (Predictive) | Grade A | `weekly_system_state` | Model State-Space berhasil lulus uji Synthetic Parameter Recovery (mean relative error: $0.33\%$) dan mereproduksi 87 minggu riwayat e-commerce dengan WAPE volume pesanan $15.83\%$ dan WAPE review negatif $14.68\%$. |
| **DISC-07** | Carrier Logistics SLA Overhaul Dominates Freight Subsidies | L1 (Predictive) | Grade B | `weekly_system_state` | Pemangkasan delay pengiriman melalui optimasi SLA mitra logistik (S2) menghasilkan efisiensi modal 2.8x lebih tinggi dibanding subsidi ongkir universal (S1) yang merugi $-R\$\ 24,323$ akibat beban subsidi pada transaksi non-marginal. |

---

## 3. Formal Hypothesis Testing Register (H1 to H6)

All hypotheses were pre-registered and evaluated with **Benjamini-Hochberg False Discovery Rate (FDR)** correction at $\alpha = 0.05$:

| ID | Formal Hypothesis Statement | Test Statistic | Effect Size | $p$-adj (FDR) | Empirical Outcome | Claim Level & Grade |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **H1** | Rasio ongkos kirim berkorelasi negatif terhadap skor kepuasan ulasan | $t = -37.89$ | $\beta = -0.2081$ | $1.56 \times 10^{-32}$ | **SUPPORTED** | L2, Grade A |
| **H2** | Keterlambatan pengantaran memiliki slope penalti lebih curam dibanding pengantaran cepat | $F = 4218.1$ | $\Delta \beta = -0.0638$ | $0.000$ | **SUPPORTED** | L2, Grade A |
| **H3** | Skor ulasan pesanan pertama memprediksi kemungkinan pembelian berulang (repeat purchase) | $z = -0.177$ | Odds Ratio = 0.9964 | $0.859$ | **REJECTED** | L2, Grade A |
| **H4** | Sensitivitas pembeli terhadap rasio ongkir bervariasi secara heterogen antar-klaster perilaku | $F = 29.51$ | $\Delta \beta = -0.184$ | $3.08 \times 10^{-13}$ | **SUPPORTED** | L2, Grade A |
| **H5** | Penggabungan fitur ekonomi dan pengalaman menghasilkan lift prediktif signifikan dibanding univariat | $\Delta PR = +0.135$ | $+69.5\%$ lift | $1.20 \times 10^{-4}$ | **SUPPORTED** | L1, Grade A |
| **H6** | Asosiasi belanja berulang teratenuasi secara signifikan setelah mengontrol kovariat geografis | $t = 4.64$ | $47.3\%$ atenuasi | $3.39 \times 10^{-6}$ | **SUPPORTED** | L2, Grade B |

---

## 4. Failure Register & Limitation Audit

In strict compliance with the **SHADOW Project Rules (Section 2 & 13)**, negative outcomes, model limitations, and guardrail alerts are preserved with full diagnostic root causes:

### Entry FAIL-HYP-H3: Empirical Rejection of Hypothesis H3
- **Component**: Statistical Hypothesis Testing (`src/csip/hypotheses/runner.py`)
- **Recorded Date**: 2026-11-10
- **Finding**: Odds Ratio = $0.9964$, 95% Confidence Interval: $[0.957, 1.037]$, $p\text{-adj} = 0.859$.
- **Diagnostic Root Cause**: On Brazilian marketplace platforms, initial satisfaction is necessary but not sufficient for repurchase. Repeat purchases are driven by product replenishment cycles (e.g. hygiene vs one-off electronics) and regional seller availability rather than 5-star vs 1-star ratings.
- **Impact Assessment**: Product review scores cannot be used as a standalone predictor for customer lifetime retention.
- **Mitigation**: Switched to multi-factor behavioral feature sets including category velocity and logistics proximity.

### Entry FAIL-OOD-S4: Extrapolation Guardrail Trigger on Macroeconomic Shock
- **Component**: Alternative World Simulator (`src/csip/scenarios/simulator.py`)
- **Recorded Date**: 2026-11-10
- **Finding**: Scenario S4 (+20% freight, +4 days delay) resulted in $Z_{\text{max}} = 3.68$, exceeding the $3.5\sigma$ historical envelope.
- **Diagnostic Root Cause**: Macroeconomic fuel price spikes and systemic carrier strikes push the system beyond historical observational support.
- **Impact Assessment**: Linear state-space transition cannot guarantee unobserved non-linear tipping points or mass platform insolvency.
- **Mitigation**: System automatically downgraded claim to **Grade C (Spekulatif / Guardrail Triggered)** and displayed actionable alerts in executive reporting.
