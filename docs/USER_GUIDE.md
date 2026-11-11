# CSIP User & Assessor Guide: Analytical Navigation & Feature Walkthrough
## Navigating the 9 Multi-Page Analytical Modules of CSIP

**Document Version:** 1.0.0-Definitive  
**Target Audience:** Data Science Assessors, Logistics Operators, C-Level Decision Makers  

---

### 1. PLATFORM OVERVIEW & NAVIGATION STRUCTURE

The CSIP Streamlit interface is organized into **9 sequential analytical chapters** accessible from the left sidebar navigation:

```
SIDEBAR NAVIGATION
+-------------------------------------------------------------+
| Chapter 1: Executive Overview (Core Strategic Takeaway)    |
| Chapter 2: Data Observatory (Schemas & Data Contracts)      |
| Chapter 3: Behavioral Discovery Lab (Customer Clustering)   |
| Chapter 4: Hypothesis Laboratory (Non-Parametric Tests)     |
| Chapter 5: Predictive Intelligence (ML Models & Slices)     |
| Chapter 6: Macro World Model (VAR State Dynamics)           |
| Chapter 7: Alternative World Simulator (Counterfactuals)    |
| Chapter 8: Decision Studio & ROI Optimizer                  |
| Chapter 9: SKKNI Evidence Registry Review (Assessor Hub)     |
+-------------------------------------------------------------+
```

---

### 2. DETAILED MODULE WALKTHROUGH

#### Chapter 1: Executive Overview (`1_Executive_Overview.py`)
- **Purpose:** Contextualizes the core business dilemma: customer sensitivity to delivery delays vs shipping freight.
- **Key Cards:** 3 editorial story cards detailing key findings from 100,000 real orders.
- **Target Audience:** C-level executives requiring intuitive strategic summaries before technical deep-dives.

#### Chapter 2: Data Observatory (`2_Data_Observatory.py`)
- **Purpose:** Complete data profiling and schema validation.
- **Interactive Controls:** Toggle between raw Olist tables, inspect missingness heatmaps, and review runtime Data Contract validation reports.

#### Chapter 3: Behavioral Discovery Lab (`3_Behavioral_Discovery_Lab.py`)
- **Purpose:** Exploratory customer segmentation via RFM feature clustering.
- **Visualizations:** 3D interactive PCA projections, radar charts of customer persona attributes, and silhouette distribution plots.

#### Chapter 4: Hypothesis Laboratory (`4_Hypothesis_Laboratory.py`)
- **Purpose:** Scientific verification of operational hypotheses.
- **Statistical Tests:** Mann-Whitney U test on delivery delay impact ($p < 10^{-15}$), Chi-Square test on interstate shipping risks, and Kruskal-Wallis tests across product categories.

#### Chapter 5: Predictive Intelligence (`5_Predictive_Intelligence.py`)
- **Purpose:** Core machine learning hub.
- **Features:**
  - Model Leaderboard comparing Naive, Linear, Random Forest, and LightGBM models.
  - Interactive prediction playground: adjust order price, freight, and delay sliders to observe real-time calibrated negative review probability.
  - Subgroup Slice Analysis table detailing regional performance across SP, RJ, MG, RS, and PR.
  - SHAP summary beeswarm plots and Platt calibration curve visualizations.

#### Chapter 6: Macro World Model (`6_World_Model.py`)
- **Purpose:** Macroeconomic system-level dynamics.
- **Controls:** Inspect the $6 \times 6$ Ridge VAR state transition matrix, eigenvalue stability poles, and impulse response function plots.

#### Chapter 7: Alternative World Simulator (`7_Alternative_World_Simulator.py`)
- **Purpose:** Counterfactual scenario experimentation.
- **Simulation Levers:** Apply freight subsidies (-10% to -50%), logistics speedup (-1 to -5 days), or test seasonal demand spikes. Run 500-step Monte Carlo Markov Chain simulations to view projected weekly trajectories.

#### Chapter 8: Decision Studio (`8_Decision_Studio.py`)
- **Purpose:** Operational decision optimization and ROI calculation.
- **Interactive Calculator:** Configure customer lifetime value (LTV), dispute cost, and voucher subsidy values to compute the mathematically optimal probability decision threshold ($P^*$).

#### Chapter 9: SKKNI Evidence Registry Review (`9_Evidence_Registry_Review.py`)
- **Purpose:** Dedicated Assessor Audit Center.
- **Features:** Search and filter all 63 KUKs across 11 Unit Kompetensi under SKKNI 299/2020. View source artifact paths, verification procedures, and SHA-256 cryptographic hashes in real-time.

