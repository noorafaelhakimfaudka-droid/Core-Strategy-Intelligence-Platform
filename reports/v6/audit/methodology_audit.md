# CSIP V6 Scientific Methodology & Research Design Audit

**Auditor**: Senior Data Science Research Methodologist & Statistical Validation Specialist  
**Standards**: CRISP-DM, SKKNI 299/2020 (UK-01, UK-02, UK-08, UK-09, UK-10, UK-11)  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Problem Formulation & Prediction Horizon Analysis

### The Dual-Objective Paradigm
In e-commerce operations, predictive modeling serves two fundamentally different business functions:

```
Timeline:
[Order Purchase / Checkout] ------> [Carrier Shipping] ------> [Customer Delivery] ------> [Customer Review]
            |                                                           |                          |
            V                                                           V                          V
   EARLY-WARNING MODEL                                     POST-DELIVERY DIAGNOSTIC          GROUND TRUTH
   - Features: Price, Freight,                             - Features: Actual Delay,        - Target: Negative
     Distance, Installments,                                 Actual Lead Time,                Review (1/0)
     Product Category, Prior Orders                          Seller SLA, Interactions
   - Purpose: Proactive Intervention                       - Purpose: Root Cause &
     (Priority routing, VIP packaging)                       Seller Performance Penalties
```

### Methodological Defect in V5
In V5, experiment `E3` for `negative_review_flag` combined `total_order_value`, `freight_ratio`, AND `delivery_delay_days`, `is_late` into a single model claiming to be an "early prediction of customer dissatisfaction".
- **Methodological Flaw**: If the model is an early-warning tool at checkout, `delivery_delay_days` is unobserved (time travel leakage). If it is a post-delivery tool, the model is scientifically valid, but its decision timeline must be explicitly stated as post-delivery diagnosis.

### V6 Corrective Formulation
1. **Task A: Early-Warning Pre-Fulfillment Classification**
   - **Timestamp**: Order Purchase Time ($t_0$).
   - **Eligible Features**: Items, Prices, Freight, Payment, Buyer/Seller Geolocation, Historical Customer Frequency, Product Catalog attributes.
   - **Prohibited Features**: Shipping date, delivery date, carrier transit time, delivery delay, review text.
   - **Target**: High Risk of Operational Dissatisfaction ($Y \in \{0, 1\}$).
2. **Task B: Post-Delivery Fulfillment & Experience Diagnostic Modeling**
   - **Timestamp**: Order Delivery Time ($t_{\text{delivery}}$).
   - **Eligible Features**: All Task A features + Actual Lead Time, Actual Delay, Freight-to-Delay Interaction, Carrier SLA adherence.
   - **Target**: Negative Review Occurrence ($Y \in \{0, 1\}$).
3. **Task C: First-Order Customer Retention Cohort Model**
   - **Timestamp**: Order 1 Purchase + Follow-up Window ($\Delta W = 90$ days).
   - **Censoring Rule**: Exclude customers whose first purchase occurs within 90 days of dataset maximum date.

---

## 2. Statistical Testing & Causal Inference Audit
- **Hypothesis Testing (H1 - H5)**:
  - Parametric Welch's t-test and non-parametric Mann-Whitney U tests were correctly implemented with Bonferroni correction in `src/csip/hypotheses/runner.py`.
  - Effect sizes (Cohen's d and Cliff's delta) were calculated properly.
- **Causal vs. Predictive Boundaries**:
  - The World Model in `state_transition.py` previously made implicit causal claims regarding intervention vectors ($A_t$).
  - In observational e-commerce data without randomized controlled trials (A/B testing) or instrumental variables, intervention simulations MUST be framed as **Scenario Assumptions / Sensitivity Projections**, not identified causal treatment effects.
