# MODEL CARD: World Model Weekly State-Transition Dynamic System
## CSIP Macro-Dynamical System & Decision Intelligence Governance

### 1. Model Details
- **Model Name**: Weekly Macro State-Transition System (World Model)
- **Artifact Path**: `artifacts/models/world_model_state_transition.joblib`
- **Metadata Sidecar**: `artifacts/models/world_model_state_transition.joblib.json`
- **Model Type**: Vector Autoregressive Dynamical System / Multivariate Ridge State Estimator
- **Version**: 17.0.0
- **Release Date**: November 2026

### 2. State Vector & Mathematical Formulation
The macro system state at week $t$ is represented by the 5-dimensional vector $\mathbf{s}_t \in \mathbb{R}^5$:
$$\mathbf{s}_t = \begin{bmatrix} \text{weekly\_order\_volume}_t \\ \text{mean\_delivery\_delay\_days}_t \\ \text{negative\_review\_rate}_t \\ \text{weekly\_gross\_merchandise\_value}_t \\ \text{repeat\_buyer\_volume}_t \end{bmatrix}$$

The transition equation governs temporal propagation:
$$\mathbf{s}_{t+1} = \mathbf{A} \mathbf{s}_t + \mathbf{B} \mathbf{u}_t + \mathbf{\epsilon}_t$$
where $\mathbf{A} \in \mathbb{R}^{5 \times 5}$ is the estimated state transition matrix, $\mathbf{B}$ is the exogenous policy intervention matrix (e.g. logistics buffer additions, subsidy levers), and $\mathbf{\epsilon}_t \sim \mathcal{N}(0, \mathbf{\Sigma})$ represents stochastic operational noise.

### 3. Quantitative Evaluation (Historical Replay & Stability)
- **Estimation Data**: 98 weekly observations (`data/processed/weekly_system_state.parquet`).
- **Mean Absolute Percentage Error (MAPE)**:
  - Weekly Order Volume: **6.4%**
  - Mean Delivery Delay: **8.1%**
  - Negative Review Rate: **5.8%**
  - Weekly GMV: **7.2%**
- **Eigenvalue Stability Criterion**: Spectral radius $\rho(\mathbf{A}) = 0.842 < 1.0$ (strictly stable dynamical system without explosive feedback loops).

### 4. Scientific Claim Governance & Causal Boundaries
- **CRITICAL DISTINCTION**:
  1. **Historical Observations**: Actual recorded weekly Olist aggregates.
  2. **Estimated System Dynamics**: Linear approximations of week-over-week momentum and cross-variable correlations.
  3. **Simulated Scenarios (Alternative Worlds)**: Hypothetical forward projections under counterfactual policy inputs.
- **Explicit Limitation**: Simulated policy interventions (e.g. reducing delay by 3 days) reflect mathematical extrapolation under historical structural assumptions; they do NOT guarantee real-world outcomes without field randomized controlled trials (Level L1/L2 associational claim).

### Deployment Maturity Level
- **Status**: `BENCHMARK_VALIDATED`
- **Operational Governance Assessment**: Macroeconomic Vector AutoRegressive (VAR) state-space model (WAPE 15.83% vs persistence baseline 22.41%). Validated for scenario analysis and counterfactual simulation; not approved as an autonomous controller.
