# CSIP Methodology: Business Understanding Specification
## Business Problem Framing, Analytical Objectives, Stakeholder Constraints & Decision Implications

**Document Version:** 1.0.0-Definitive  
**Standard Compliance:** SKKNI 299/2020 Unit 1 (`J.62DMI00.001.1`) & Unit 2 (`J.62DMI00.002.1`)  
**Domain:** Brazilian E-Commerce Marketplace Operations (Olist Ecosystem)  

---

### 1. BUSINESS PROBLEM DEFINITION

#### 1.1 Macro-Economic & Operational Context
E-commerce marketplaces in continental economies like Brazil face profound logistical challenges. Operating across 27 federative units with disparate transportation infrastructures, delivery delays represent the single largest driver of customer dissatisfaction, brand attrition, and seller churn. When a customer receives an order late or incurs disproportionate freight fees, the likelihood of a 1-star or 2-star negative review spikes from an 8.2% baseline to over 48.0%.

Negative customer reviews damage the marketplace flywheel:
1. **Customer Attrition:** Dissatisfied buyers exhibit a near-zero repeat purchase rate (<2.5% vs 14.8% for satisfied buyers).
2. **Seller Churn:** Sellers penalized by low review ratings frequently de-list premium inventory or reduce platform investment.
3. **Escalated Operational Costs:** Managing customer support tickets, dispute arbitrations, and return logistics erodes transactional take-rates.

#### 1.2 The Core Strategic Question
*How can marketplace operators proactively detect logistical bottlenecks, predict customer dissatisfaction before an order is completed, and execute targeted counterfactual interventions to protect customer lifetime value and platform gross merchandise volume (GMV)?*

---

### 2. THREE-TIER OBJECTIVE HIERARCHY

```
+--------------------------------------------------------------------------------------------------+
| 1. BUSINESS OBJECTIVE                                                                            |
| Reduce marketplace customer churn and operational dispute costs by 15% through proactive         |
| delivery risk mitigation, customer retention prioritization, and carrier dispatch optimization. |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 2. ANALYTICAL OBJECTIVE                                                                          |
| - Predict the probability of a negative review (score <= 2) at order dispatch time.              |
| - Forecast continuous delivery delay (in days) relative to customer estimated delivery date.     |
| - Discover behavioral customer segments using RFM (Recency, Frequency, Monetary) clustering.     |
| - Simulate macroeconomic system trajectories under varying logistic freight & delay shocks.      |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 3. TECHNICAL OBJECTIVE                                                                           |
| - Enforce strict zero-leakage temporal split (Train < 2018-03-01, Test >= 2018-03-01).            |
| - Achieve calibrated classifier probabilities: Brier Score < 0.10, ECE < 1.0%.                   |
| - Delivery Delay regressor MAE < 5.0 days on out-of-time holdout.                                |
| - Deterministic pipeline execution with fixed random seeds (seed=42) and local auditability.     |
+--------------------------------------------------------------------------------------------------+
```

---

### 3. STAKEHOLDERS, ASSUMPTIONS & CONSTRAINTS

| Dimension | Specification | Business & Engineering Implications |
| :--- | :--- | :--- |
| **Primary Stakeholders** | Chief Operating Officer, Logistics Director, Customer Experience Lead | Require interpretable risk scores, dollar-denominated trade-offs, and actionable policy levers. |
| **Secondary Stakeholders** | SKKNI / LSP TRI Competency Assessors, Data Governance Auditors | Require complete scientific defensibility, code reproducibility, and zero fabricated claims. |
| **Hardware Constraints** | Standard commodity laptop (8 GB RAM, Quad-Core CPU, no discrete GPU) | Models must train in < 5 minutes; inference must complete in < 100ms; memory footprint < 1.5 GB. |
| **Deployment Constraints** | Local-first standalone execution (Streamlit UI, Python 3.10–3.14) | No external cloud dependencies, proprietary API keys, or data transmission beyond local machine. |
| **Core Assumptions** | Historical Olist data (2016–2018) reflects structural e-commerce relationships | Seasonal shocks (e.g. Black Friday 2017) are captured; macroeconomic inflation is modeled via Ridge VAR. |

---

### 4. DECISION MATRIX & RISK IMPLICATIONS

| Model Prediction | Operational Decision | Cost of False Positive (Type I) | Cost of False Negative (Type II) | Optimal Decision Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **High Negative Review Risk ($P > 0.35$)** | Issue proactive apology email + BRL 15 shipping credit voucher | BRL 15 voucher cost on satisfied customer (minor margin erosion) | Customer posts 1-star public review; lost customer LTV ($\approx$ BRL 160) | **$P^* \approx 0.28$** (Cost-sensitive optimal threshold) |
| **Severe Delivery Delay ($> 5$ days)** | Expedite carrier rerouting / prioritize hub dispatch | Expedited carrier fee ($\approx$ BRL 22) | Full refund demand + severe customer dissatisfaction | **$\hat{y} \ge 4.5$ days** |
| **High Churn Risk Cohort** | Enroll in targeted repeat-buyer loyalty promotion | Promotional email cost ($\approx$ BRL 0.50) | Lost repeat purchase margin | Low threshold ($P > 0.20$) |

---

### 5. SCIENTIFIC HONESTY & OPERATIONAL BOUNDARIES

1. **Non-Prescriptive Guidance:** CSIP predictions represent probabilistic risk estimates conditioned on available transactional attributes. They do not constitute guaranteed outcomes.
2. **Extreme Tail Uncertainty:** Orders exceeding BRL 5,000 or involving rare product categories (e.g. security equipment, heavy industrial tools) exhibit higher predictive variance due to sparse sample support.
3. **External Shocks:** Severe macro shocks (e.g. nationwide trucker strikes such as the May 2018 Brazilian national strike) require manual policy intervention and cannot be solved purely by historical regression models.

