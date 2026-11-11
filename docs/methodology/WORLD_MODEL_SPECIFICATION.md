# CSIP World Model Specification
## Autoregressive Dynamic State-Space Formulation, Estimation, and Policy Simulation
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.008.1 & J.62DMI00.009.1

- **Document ID**: `CSIP-METH-WORLD-SPEC-2026-V7`
- **Version**: 7.0.0
- **Lead Author**: Senior Machine Learning Engineer & Macro Systems Architect
- **Status**: AUDITED & SCIENTIFICALLY BOUNDED

---

## 1. Mathematical Formulation

The CSIP World Model provides a dynamic state-space framework for macro-level e-commerce ecosystem simulation. It operates at a weekly epoch grain ($t \in \{1, \dots, T\}$), capturing the coupled dynamics of transactional volume, logistics performance, pricing burden, and customer sentiment.

The discrete-time transition equation is formalized as a first-order Vector AutoRegressive process with regularized ridge estimation:

$$S_{t+1} = C + \Phi S_t + \varepsilon_t$$

Where:
- $S_t \in \mathbb{R}^d$ ($d = 4$): Standardized system state vector at week $t$:
  $$S_t = \begin{bmatrix} \text{weekly\_order\_volume}_t \\ \text{mean\_delivery\_delay}_t \\ \text{mean\_freight\_ratio}_t \\ \text{negative\_review\_rate}_t \end{bmatrix}$$
- $C \in \mathbb{R}^d$: Empirical system drift intercept vector.
- $\Phi \in \mathbb{R}^{d \times d}$: State transition matrix encoding cross-variable feedback and temporal autocorrelation.
- $\varepsilon_t \sim \mathcal{N}(0, \Sigma)$: Innovation perturbation noise with empirical residual covariance matrix $\Sigma \in \mathbb{R}^{d \times d}$.

---

## 2. Parameter Estimation and Numerical Regularization

1. **Standardization Protocol**:
   To prevent dominance of high-magnitude variables (`weekly_order_volume` $\sim 10^3$) over bounded fractions (`mean_freight_ratio` $\in [0, 1]$), states are standardized prior to transition estimation:
   $$z_t = \frac{S_t - \mu_S}{\sigma_S + 10^{-6}}$$
2. **L2 Ridge Regularization**:
   Transition matrix $\Phi$ is estimated by solving the penalized multivariate regression:
   $$\hat{\Phi}, \hat{C} = \arg\min_{\Phi, C} \sum_{t=1}^{T-1} \|z_{t+1} - (C + \Phi z_t)\|_2^2 + \alpha \|\Phi\|_F^2$$
   Where $\alpha = 0.10$ provides numerical stability across collinear time-series.
3. **Residual Covariance Matrix ($\Sigma$)**:
   $$\hat{\Sigma} = \frac{1}{T - 2} \sum_{t=1}^{T-1} \hat{e}_t \hat{e}_t^\top, \quad \hat{e}_t = z_{t+1} - (\hat{C} + \hat{\Phi} z_t)$$

---

## 3. Counterfactual Scenario Simulation Framework

For policy evaluation (e.g., carrier SLA intervention, freight subsidies), an exogenous action vector $\Delta_a \in \mathbb{R}^d$ is introduced:

$$S_{t+1}^{\text{sim}} = C + \Phi S_t^{\text{sim}} + \Delta_a + \varepsilon_t$$

### Physical Feasibility Projections
Because unconstrained linear models can drift into non-physical values, projected states are projected back onto the admissible domain $\mathcal{S}_{\text{physical}}$:
$$\text{weekly\_order\_volume} \ge 0, \quad \text{mean\_freight\_ratio} \in [0, 1], \quad \text{negative\_review\_rate} \in [0, 1]$$

---

## 4. SCIENTIFIC DISCLOSURE: Non-Causal Boundary

> **IMPORTANT SCIENTIFIC GOVERNANCE**:
> Scenario simulations in CSIP represent **structural sensitivity projections** under empirical transition dynamics, **NOT causal treatment effects** identified from randomized controlled trials (A/B testing) or quasi-experimental instrumental variables. 
> 
> A simulated 10% freight subsidy projects what system states would follow if historical correlations remain invariant (Lucas Critique caveat). Decision-makers must treat these trajectories as scenario stress-tests rather than guaranteed causal interventions.

---

## 5. Holdout Evaluation Protocol

To avoid in-sample overfitting, the World Model is evaluated using a **chronological out-of-sample holdout**:
- **Estimation Window**: Weeks 1–64 (first 75% of panel).
- **Holdout Validation Window**: Weeks 65–87 (unseen final 23 weeks).
- **Evaluation Metrics**:
  - **WAPE** (Weighted Absolute Percentage Error): $\frac{\sum |y - \hat{y}|}{\sum |y|}$
  - **MAPE** (Mean Absolute Percentage Error): $\frac{1}{N} \sum \left|\frac{y - \hat{y}}{y}\right|$
  - **RMSE** (Root Mean Squared Error): $\sqrt{\frac{1}{N} \sum (y - \hat{y})^2}$
