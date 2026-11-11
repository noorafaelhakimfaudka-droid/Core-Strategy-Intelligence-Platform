# CSIP System Architecture Specification
## Observational Data Science & Decision Intelligence Platform Architecture
### Standard: SKKNI No. 299 Tahun 2020 | Subbidang: Data Science (KKNI Jenjang 7)

- **Document ID**: `CSIP-ARCH-SYS-2026-V7`
- **Version**: 7.0.0
- **Status**: ARCHITECTURALLY VERIFIED
- **Author**: Principal Data Scientist & Systems Architect

---

## 1. Architectural Principles & Boundary

The **Core Strategy & Intelligence Platform (CSIP)** is engineered as a local, auditable, high-performance Data Science and Decision Intelligence system.

### Core Architecture Pillars:
1. **Data Science-Centric, Not Agent-Centric**: Strictly an observational Data Science platform investigating human behavior, e-commerce friction, and decision intelligence. CSIP does not contain autonomous LLM agents, chatbots, or generic agent swarms.
2. **100% Local Execution**: Operates entirely within an 8 GB RAM laptop envelope without external API calls, cloud storage dependencies, or remote data transmission.
3. **Strict Point-in-Time Separation**: Data transformations and model training follow a rigid *split-before-fit* regime, with temporal prediction contracts enforced at checkout ($t_0$) and delivery ($t_1$).
4. **Deterministic & Auditable**: Every processing step from raw CSV ingestion to model serialization is governed by fixed seeds (`random_state=42`) and validated by automated test suites.

---

## 2. End-to-End System Pipeline

```mermaid
flowchart TD
    subgraph Data Intake & Governance
        RAW[9 Olist Relational Tables CSV] --> VAL[Data Validation & Profiling]
        VAL --> CLEAN[Cleaner & Geo Deduplication]
    end

    subgraph Analytical Construction
        CLEAN --> FE[Feature Engineering Engine]
        FE --> D1[(Objek Data 1: order_level)]
        FE --> D2[(Objek Data 2: customer_cohort)]
        FE --> D3[(Objek Data 3: review_corpus)]
        FE --> D4[(Objek Data 4: weekly_system_state)]
    end

    subgraph Modeling & Intelligence
        D1 --> CLUST[Behavioral Persona Clustering k=3]
        D1 --> HYP[Hypothesis Battery H1-H6]
        D1 --> ML[Supervised ML Ladder B0-B3]
        D4 --> WM[World Model VAR 1 State-Space]
    end

    subgraph Evaluation & Decision Intelligence
        ML --> EVAL[PR-AUC & Brier Evaluation]
        ML --> CALIB[Platt Probability Calibration]
        ML --> SHAP[SHAP TreeExplainer Attribution]
        WM --> SIM[What-If Policy Simulation S0-S5]
        WM --> REPLAY[Historical Replay Backtest]
    end

    subgraph User & Audit Interface
        EVAL --> STREAMLIT[Streamlit Multi-Page Studio]
        SIM --> STREAMLIT
        EVAL --> REGISTRY[SKKNI Competency Evidence Registry]
```

---

## 3. Package and Subsystem Structure (`src/csip/`)

```
src/csip/
├── cleaning/           # Data cleaning pipelines, chronological anomaly filtering, geo-deduplication
│   ├── cleaner.py      # Core data cleaner and outlier handler
│   └── auto_cleaner.py # Scikit-Learn transformer protocol wrapper
├── data/               # Data ingestion, schema validation, semantic profiling
│   ├── loader.py       # 9 Olist CSV table loader & Foreign Key integrity verifier
│   └── semantic_profiler.py # Semantic data profiler (monetary units, distributions)
├── discovery/          # Unsupervised machine learning & customer segmentation
│   └── clusterer.py    # K-Means clustering persona sensitivity model
├── engine/             # Execution wrappers and pipeline runners
├── evaluation/         # Model evaluation, calibration, and feature attribution
│   └── explainer.py    # SHAP TreeExplainer and Platt Scaling calibration
├── evidence/           # Competency evidence registration and failure register
│   └── registry.py     # Multi-level evidence snapshot generator
├── features/           # Feature engineering, spatial Haversine, interaction terms
│   └── engineer.py     # 41 domain features, cohort construction (drop_duplicates)
├── hypotheses/         # Statistical hypothesis testing framework
│   └── runner.py       # Formal hypothesis battery (H1-H6) with FDR Benjamini-Hochberg
├── models/             # Machine Learning model definitions and trainers
│   ├── classic.py      # Baseline ladder (B0-B3: Naive, Ridge, DT, RF, LightGBM)
│   ├── deep_tabular.py # PyTorch MLP with categorical entity embeddings
│   ├── deep_seq.py     # PyTorch Bi-LSTM NLP text sentiment model
│   ├── ml_engine.py    # Fluent scikit-learn continuous ML pipeline
│   └── trainer.py      # Full experiment runner, temporal splits, artifact persistence
├── scenarios/          # Policy simulation and sensitivity rollouts
│   └── simulator.py    # What-If policy simulation engine (S0-S5)
├── uncertainty/        # Non-parametric uncertainty estimation
│   └── bootstrap.py    # Residual bootstrapping (B=1,000) for confidence intervals
└── world/              # Macro-level state-space dynamic transition
    └── state_transition.py # Vector AutoRegressive (VAR) state transition with holdout
```

---

## 4. Hardware and Runtime Governance

- **Target Hardware**: Intel/AMD x86_64 Laptop with 8 GB RAM.
- **CPU Optimization**: Multi-threading bounded to prevent OOM errors during gradient boosting and PyTorch training.
- **Memory Optimization**: Downcasting routines automatically convert `float64` to `float32` and `int64` to `int16`/`int8`, reducing in-memory footprint by over 60%.
- **Parquet Storage**: Analytical datasets utilize columnar Snappy compression for rapid I/O and zero metadata loss.
