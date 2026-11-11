# CSIP Known Limitations & Scientific Disclosures
## Methodological Boundaries, Observational Constraints, and Governance Disclosures
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.015.1 (KUK 2.2 & 2.3)

- **Document ID**: `CSIP-DOC-LIMIT-2026-V7`
- **Version**: 7.0.0
- **Status**: AUDITED & SCIENTIFICALLY DISCLOSED
- **Author**: Principal Data Scientist & Scientific Integrity Auditor

---

## 1. Observational Data Limitations

1. **Context and Geography**:
   - The empirical analysis is based entirely on the Olist Brazilian E-Commerce public dataset (2016–2018).
   - Findings reflect Brazilian retail geography, domestic carrier transit infrastructures (Correios), and macro-economic conditions during that specific historical epoch.
   - Direct generalization to other geographies or modern ultra-fast delivery platforms (e.g., same-day quick-commerce) requires local re-calibration.

---

## 2. Population Definition & Survivor Bias

1. **Delivered Orders Conditioning**:
   - As documented in `reports/methodology/POPULATION_AND_SELECTION_BIAS.md`, data cleaning filters for delivered orders (`status == 'delivered'`).
   - Consequently, **1,234 non-delivered orders (canceled + unavailable stockouts)** are excluded from satisfaction modeling.
   - Because canceled orders exhibit an extreme 87.2% negative review rate, models trained on delivered orders estimate the conditional probability:
     $$\mathbb{P}(\text{Negative Review} \mid X, \text{Delivered} = 1)$$
   - The early-warning model cannot be used to predict inventory stockouts or merchant order cancellations prior to fulfillment.

2. **Unobserved Customer Feedback**:
   - 646 delivered orders (0.67%) have no recorded customer review.
   - CSIP treats these as unobserved values (`NaN`) and excludes them from supervised training rather than applying synthetic imputations (such as neutral score 3), which would artificially suppress the empirical dissatisfaction rate.

---

## 3. World Model & Policy Simulation Non-Causal Boundary

1. **Structural Sensitivity vs Causal Identification**:
   - The World Model state transition engine ($S_{t+1} = C + \Phi S_t + \varepsilon_t$) models empirical autoregressive dynamics across weekly system states.
   - Simulations of policy interventions (e.g., freight subsidies or carrier SLA enhancements) represent **structural sensitivity projections**, NOT causally identified treatment effects derived from randomized controlled trials (A/B testing) or quasi-experimental instrumental variables.
   - Decision-makers must recognize the Lucas Critique: large-scale policy shifts may alter agent behavior and shift the empirical transition matrix $\Phi$.

---

## 4. External Stakeholder Verification Disclosure

1. **Open-Source Dataset Constraints**:
   - Because CSIP utilizes a public historical dataset, direct access to the original e-commerce management team or live end-users was unavailable.
   - In SKKNI Unit `J.62DMI00.001.1` (Menentukan Objektif Bisnis), KUK 2.2, 3.3, and 4.3 are disclosed as **PARTIALLY_VERIFIED**: business objectives, success criteria, and ROI cost-benefit models are mathematically complete and fully documented in internal specifications, but actual external formal approval signatures were simulated.
   - No fake stakeholder identities or fraudulent meeting records have been fabricated.

---

## 5. Computing Environment & Hardware Bounds

1. **Resource Constraints**:
   - CSIP is deliberately optimized for execution on standard developer laptops (8 GB RAM, multi-core CPU).
   - Massive hyperparameter search grids and multi-billion-parameter neural foundation models are omitted in favor of lightweight, CPU-efficient algorithms (LightGBM, PyTorch MLP, Bi-LSTM).
   - This design choice prioritizes auditability, rapid reproducibility, and accessibility over unconstrained computational scale.
