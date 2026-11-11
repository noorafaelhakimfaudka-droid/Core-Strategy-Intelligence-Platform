# Changelog

All notable changes to the **Core Strategy & Intelligence Platform (CSIP)** will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
