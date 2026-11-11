# CSIP V6 Scientific Methodology & Research Design

**Document ID**: CSIP-REP-V6-SMR-01  
**Author**: Principal Data Scientist & Senior Research Methodologist  
**Standard**: SKKNI 299/2020 Subbidang Data Science  
**Date**: November 2026  
**Status**: APPROVED & CANONICAL  

---

## 1. Problem Formulation & Research Design

CSIP models the multi-sided dynamics of e-commerce marketplaces under the Brazilian Olist ecosystem (96,470 delivered orders, 95,824 observed reviews, 75,318 customer cohorts, 87 macro weeks).

The platform addresses four central research questions:
1. **RQ1 (Pricing & Friction)**: What is the cross-elasticity between shipping cost burden (`freight_ratio`) and customer satisfaction?
2. **RQ2 (Fulfillment Asymmetry)**: Does fulfillment delay past promised SLA induce an asymmetric, non-linear penalty on buyer sentiment?
3. **RQ3 (Cohort Retention)**: How does first-order fulfillment experience influence long-term repeat purchase probability ($\Delta W = 90$ days)?
4. **RQ4 (Macro Dynamics)**: How do macro logistics shocks propagate through the platform's state-space over multi-month horizons?

---

## 2. Split-Before-Transform & Anti-Leakage Protocol

1. **Temporal Horizon Splitting**:
   - Order-level: Train $\le$ 2018-03-31, Validation: 2018-04-01 to 2018-06-30, Test: 2018-07-01 to 2018-08-31.
   - Customer-cohort: Train $\le$ 2017-12-31, Validation: 2018-01-01 to 2018-03-31, Test: 2018-04-01 to 2018-08-31.
   - Macro state panel: In-sample Train: Weeks 1-64, Out-of-sample Test: Weeks 65-87.
2. **Imputation Protocol**:
   - Scalers, imputers, and encoders are fit strictly on training splits.
   - Missing target labels (unobserved review surveys) are separated from the training set, eliminating denominator contamination.
