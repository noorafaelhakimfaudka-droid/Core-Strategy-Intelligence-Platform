# CSIP Experiment Documentation: Comprehensive Machine Learning Trial Register
## Model Architecture Comparisons, Hyperparameter Spaces, Validation Strategy & Holdout Results

**Document Version:** 1.0.0-Definitive  
**Standard Compliance:** SKKNI 299/2020 Unit 8 (`J.62DMI00.012.1`) & Unit 9 (`J.62DMI00.013.1`)  
**Experiment Ledger:** `artifacts/metadata/MODEL_RESULTS_REGISTRY.csv` & `artifacts/reports/ml_leaderboard.json`  

---

### 1. EXPERIMENTAL DESIGN & PROTOCOL

#### 1.1 Out-of-Time Temporal Splitting
All supervised learning experiments follow a strict temporal split to prevent temporal leakage and realistic assessment of operational performance:
- **Training Horizon:** All orders placed before `2018-03-01` (81,160 raw orders; 68,530 training samples after filtering).
- **Validation Protocol:** 5-Fold TimeSeriesSplit / Purged Group Cross-Validation on training split for hyperparameter tuning.
- **Sealed Holdout Test Horizon:** All orders placed on or after `2018-03-01` (15,310 raw orders; 12,630 clean evaluation samples). Zero hyperparameter tuning or feature selection was performed on the test partition.

---

### 2. EXPERIMENT 1: CUSTOMER NEGATIVE REVIEW CLASSIFICATION (`negative_review_flag`)

#### 2.1 Problem Formulation
Predict whether a customer will submit a 1-star or 2-star rating ($\text{review\_score} \le 2$) conditioned on features available at order completion. Class balance: 15.4% positive prevalence (imbalance ratio 1:5.5).

#### 2.2 Model Architecture Comparison (Holdout Test Partition)
| Architecture ID | Model Family | Hyperparameters / Structure | Test ROC-AUC | Test PR-AUC | Test Brier (Calib) | Test ECE | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **B0-Naive** | Prior Prevalence | Constant probability $\hat{p} = 0.154$ | 0.5000 | 0.1541 | 0.1303 | N/A | Baseline |
| **B1-Logistic** | L2 Logistic Regression | $C = 1.0$, `class_weight='balanced'`, StandardScaler | 0.6543 | 0.2812 | 0.0815 | 0.0185 | Baseline |
| **B2-RandomForest** | Random Forest | `n_estimators=200`, `max_depth=12`, `min_samples_leaf=20` | 0.6631 | 0.2924 | 0.0792 | 0.0142 | Candidate |
| **B3-LightGBM** | Gradient Boosted Trees | `n_estimators=150`, `learning_rate=0.05`, `num_leaves=31` | **0.6745** | **0.3061** | **0.0762** | **0.0070** | **CHAMPION** |
| **DL-MLP** | PyTorch Tabular MLP | 3-Layer MLP [128, 64, 32], Dropout=0.2, Adam | 0.6580 | 0.2850 | 0.0820 | 0.0190 | Benchmark |

**Key Finding:** LightGBM achieved the highest discriminative ability (ROC-AUC `0.6745`) and PR-AUC (`0.3061`, 2x random baseline). Platt Sigmoid probability calibration reduced the Brier score from `0.1373` to `0.0762` and compressed Expected Calibration Error to `0.0070` ($0.7\%$).

---

### 3. EXPERIMENT 2: DELIVERY DELAY CONTINUOUS REGRESSION (`delivery_delay_days`)

#### 3.1 Problem Formulation
Forecast continuous delivery delay in days ($\text{delivered\_date} - \text{estimated\_date}$) using features available at carrier dispatch.

#### 3.2 Model Architecture Comparison (Holdout Test Partition)
| Architecture ID | Model Family | Hyperparameters / Structure | Test MAE (days) | Test RMSE (days) | Test $R^2$ | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **B0-Dummy** | Median Predictor | Predicts historical median delay (-11.2 days) | 6.5412 | 8.8921 | 0.0000 | Baseline |
| **B1-Ridge** | Ridge Regression | $\alpha = 10.0$, StandardScaler | 5.1245 | 6.7820 | 0.2840 | Baseline |
| **B2-RandomForest** | Random Forest Regressor | `n_estimators=150`, `max_depth=10` | 4.9510 | 6.4120 | 0.3610 | Candidate |
| **B3-LightGBM** | Gradient Boosted Trees | `n_estimators=120`, `learning_rate=0.06`, `num_leaves=25` | **4.8256** | **6.2458** | **0.3926** | **CHAMPION** |

**Key Finding:** LightGBM regressor outperformed the dummy baseline by 1.72 days in MAE and achieved an $R^2$ of `0.3926`, providing reliable forward delay warnings for high-risk interstate routes.

---

### 4. EXPERIMENT 3: DEEP LEARNING NLP SENTIMENT CLASSIFICATION

#### 4.1 Problem Formulation
Classify customer review sentiment from raw Portuguese text comments (`olist_order_reviews_dataset.csv`, 41,000+ non-empty text reviews).

#### 4.2 Architecture Specification
- **Model:** Bidirectional Long Short-Term Memory (BiLSTM).
- **Embedding:** Word-level embedding layer (embedding dim: 64, vocab size: 10,000 tokens).
- **Recurrent Units:** 2-layer BiLSTM with hidden dimension 128 and dropout 0.3.
- **Classification Head:** Dense layer with Softmax activation (3 classes: Negative [1-2], Neutral [3], Positive [4-5]).
- **Holdout Test Performance:** Macro-F1 = `0.8420`, Accuracy = `0.8870`.
- **Artifact:** `artifacts/models/text_bilstm_review_sentiment.pt` (1,028,363 bytes).

---

### 5. EXPERIMENT 4: MACROECONOMIC SYSTEM WORLD MODEL

#### 5.1 Problem Formulation
Estimate the dynamic weekly state transition matrix $A \in \mathbb{R}^{6 \times 6}$ across 87 weekly observations:
$$s_{t+1} = A s_t + \epsilon_t$$
where $s_t = [\text{volume}, \text{delay}, \text{delay\_rate}, \text{negative\_rate}, \text{freight\_ratio}, \text{price}]^T$.

#### 5.2 Model Estimation & Stability Audit
- **Algorithm:** Multivariate Ridge Regression ($\alpha = 1.0$).
- **Information Criteria:** $\text{AIC} = -4.8920$, $\text{BIC} = -4.5120$.
- **Spectral Radius Stability:** Maximum eigenvalue modulus $\rho(A) = 0.8412 < 1.000$, proving asymptotic stability and non-explosive behavior under Monte Carlo perturbation.
- **Artifact:** `artifacts/models/world_model_state_transition.joblib` (1,512 bytes).

