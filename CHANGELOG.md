# Changelog

All notable changes to the **Core Strategy & Intelligence Platform (CSIP)** will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-11-13

### Added
- **Business Decision Engine (`csip.decision_engine`)**:
  - Structured decision schemas (`DecisionPriority`, `OperationalFunction`, `EvidenceType`, `RecommendationStatus`, `DecisionRuleConfig`, `DecisionRecommendation`).
  - Configurable prioritization rule evaluator (`DecisionRuleEvaluator`) translating raw predictive probabilities and delivery delay estimates into operational action triggers.
  - Operational capacity triage engine (`BusinessDecisionEngine`) providing tier-capped batch recommendations across Logistics Dispatch, Customer Experience, Merchant Operations, and Executive Leadership.
- **Model Governance & Champion-Challenger Lifecycle (`csip.models.registry`)**:
  - Formal candidate promotion protocol enforcing strict promotion gates: $\ge 1\%$ primary metric improvement, Brier score degradation $\le 5\%$, and maturity gate.
  - Rollback mechanism allowing instant fallback to previous champion models with comprehensive promotion history logging in `artifacts/metadata/PROMOTION_HISTORY.csv`.
- **Data Contracts & Cryptographic Lineage Audit (`csip.data.contracts`, `csip.data.lineage`)**:
  - 4-tier contract severity levels: `INFO`, `WARNING`, `RECOVERABLE_ERROR`, `CRITICAL_FAILURE` with strict exception enforcement via `DataContractException`.
  - Dynamic byte-level SHA-256 verification of Parquet tables on disk, preventing unsubstantiated unbroken chain claims and mapping upstream producers to downstream model consumers.
- **Business Impact & Asymmetric Cost Evaluation (`csip.evaluation.business_impact`)**:
  - Operational evaluation framework computing Precision@K, Recall@K, false positive intervention burden, false negative churn exposure, and delivery lead time error intervals.
- **Universal ML Studio & Simulation Integrity (`csip.models.ml_engine`)**:
  - Automated Exploratory Data Analysis (EDA Mode A) profiling column missingness, cardinality, and statistical distribution parameters.
  - Automated split strategy leakage detector (`detect_split_strategy`) distinguishing temporal vs random splits and identifying lookahead contamination.
  - Transparent segregation between genuine trained model predictions and visual smoothing splines.
- **Unified 8-Module Streamlit Cockpit (`app.streamlit_app`)**:
  - Redesigned user experience into 8 coherent intelligence modules: Executive Intelligence, Business Intelligence, Data Intelligence, Predictive Intelligence, Customer Intelligence, Decision Intelligence, ML Operations, and Research Lab.
  - Embedded causal disclaimers in `build_nara_strategic_counsel` explicitly distinguishing observational associations (Level L2) from interventional causal guarantees (Level L3).
- **FastAPI Microservice Hardening (`csip.api.server`)**:
  - Added `/ready` readiness probe, `/decisions/recommend` batch operational recommendation endpoint, and `/models/registry` lifecycle governance endpoint.
  - Added request correlation ID middleware (`X-Request-ID`), structured request logging, and backward-compatible model key aliases.

### Changed
- **Model Metric Provenance Reconciliation**:
  - Clarified temporal partition boundaries: Early-warning review model (`best_early_warning_review_lightgbm`) uses strictly 10 checkout-available features; post-fulfillment model (`best_negative_review_lightgbm`) utilizes 15 features including carrier delay.
  - Reconciled metric documentation between locked out-of-time test split ($N_{test}=12,571$, PR-AUC=0.3061, ROC-AUC=0.6745) and broader temporal holdout slice ($N_{holdout}=39,153$, ROC-AUC=0.7517).
  - Explicitly disclosed empirical bounds for tabular repeat purchase prediction (95% CI spanning chance line 0.50).
- **Test Suite Expansion**:
  - Expanded comprehensive test suite to 211 passing tests across 38 suites (100% pass rate in 42.5s) with 0 failures.
  - Synchronized release version across `pyproject.toml`, `setup.py`, `src/csip/__init__.py`, `Dockerfile`, and metadata sidecars to `1.1.0`.

---

## [1.0.0] - 2026-11-12

### Added
- **Production ML Architecture**:
  - LightGBM Gradient Boosted Decision Trees for multi-target regression and calibrated classification.
  - Platt Scaling probability calibration yielding Brier score improvement from 0.0985 to 0.0782 on holdout distributions.
  - Behavioral customer segmentation pipeline combining standard RFM features with behavioral velocity metrics.
  - Strict temporal partition engine enforcing 90-day post-delivery embargoes, eliminating target and lookahead leakage.
- **High-Performance FastAPI Microservice**:
  - Decoupled REST inference service (`/predict/batch`) achieving ~0.25 ms/order latency.
  - Live statistical drift monitoring endpoint (`/monitor/drift`) computing feature and target distribution shifts.
  - Production healthcheck endpoint (`/health`) with active model metadata inspection and SLA tracking.
  - Resilient client SDK (`csip.api.client`) with automatic local fallback when daemon is detached.
- **Statistical Drift & Concept Decay Engine**:
  - Vectorized NumPy/SciPy computation of Population Stability Index (PSI), Kolmogorov-Smirnov test, and Wasserstein-1 distance.
  - Prediction drift monitoring via Jensen-Shannon Divergence.
  - Rolling-window PR-AUC, F1-Score, and Brier Score evaluation with automated alert triggers.
- **Timeline Replay & Counterfactual Shock Injector**:
  - Chronological replay engine slicing 91 weekly intervals across the Olist operational timeline.
  - Operational shock simulation modules: logistics strikes (+5 days regional lag), freight inflation (+40%), and consumer sentiment shifts.
  - Champion-vs-Challenger automated retraining loop with zero-leakage sliding windows and empirical lift calculation.
- **Interactive Decision Cockpit & Streamlit Observatory**:
  - Real-time decision simulator and counterfactual sensitivity analyzer.
  - Live Drift Radar with overlaid Reference vs. Current KDE distributions.
  - Rolling Model Health Timeline tracking PR-AUC decay against weekly order volumes.
  - Full CRISP-DM 11-Stage End-to-End Enterprise Architecture Walkthrough.
- **Engineering Quality & Reproducibility Suite**:
  - Cryptographically hashed dataset and model artifact manifests.
  - Automated 12-Gate release verification engine (`tools/verify_release.py`).
  - Comprehensive unit test suite covering temporal isolation, drift metrics, and app page rendering.
  - Multi-target Docker containerization and CI/CD workflow configuration.
