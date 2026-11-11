# CSIP V6 Source Code Audit Report

**Auditor**: Software Quality Assurance & Data Science Architecture Team  
**Scope**: All Python modules in `src/csip/`, test suite in `tests/`, entry points in `app/` and `scripts/`  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Executive Summary

An exhaustive static and dynamic inspection was conducted across the 206 tracked files in the repository.
The code quality is structurally sound (modular layout, separation of concerns, vectorized pandas/numpy implementations), but contains methodological flaws in feature availability, label imputation, and evaluation metrics that require surgical remediation.

## 2. Module-by-Module Inspection Findings

### A. `src/csip/data/loader.py` & `src/csip/data/semantic_profiler.py`
- **Strengths**: Robust Parquet caching, automated type downcasting (reducing memory footprint by >55%), defensive directory creation.
- **Findings**: Data loading assumes clean UTF-8 encoding; handles CSV and Parquet gracefully. Memory footprint on 8GB RAM is well within 1.2 GB limit.

### B. `src/csip/cleaning/cleaner.py`
- **Strengths**: Clean logging, tracking of cleaning steps with `CleaningStepReport`.
- **Findings**: `clean_orders()` defaults to `status_filter="delivered"`. This is valid for fulfillment and satisfaction analyses, but excludes 3,000+ non-delivered orders (canceled, unavailable) from the broader operational population. When conducting early-warning prediction at checkout, filtering by `status == 'delivered'` introduces survival bias (conditioning on future completion).

### C. `src/csip/features/engineer.py`
- **Findings (CRITICAL)**:
  1. Imputation of `review_score` using `fillna(3)` (neutral) conflates missing reviews with neutral ratings (Finding F-02).
  2. Construction of fulfillment experience features (`delivery_lead_time_days`, `delivery_delay_days`, `is_late`) occurs in the single `order_level` dataset without clear stage metadata tagging (Finding F-01).

### D. `src/csip/models/trainer.py` & `src/csip/models/classic.py`
- **Findings (HIGH)**:
  1. `ModelExperimentTrainer.FEATURE_SETS` mixes pre-delivery economic features with post-delivery delay features in experiment `E2` and `E3` for target `negative_review_flag`.
  2. Calculation of PR-AUC via `auc(rec, prec)` overestimates performance on constant classifiers (0.5545 instead of baseline prevalence ~0.11) due to trapezoidal interpolation (Finding F-03).
  3. Leaderboard conflates validation set model selection metrics with locked test set generalization metrics.

### E. `src/csip/world/state_transition.py`
- **Findings (HIGH)**:
  1. Discrepancy between docstring formulation ($S_{t+1} = C + \Phi S_t + \Gamma A_t + \Psi E_t + arepsilon_t$) and actual Ridge autoregression ($S_{t+1} = C + \Phi S_t + arepsilon_t$).
  2. Interventions are directly injected as state offsets without empirical action parameter estimation (Finding F-04).
  3. `backtest_historical_replay()` evaluates in-sample without chronological holdout.

### F. `tests/test_feature_leakage.py`
- **Findings (CRITICAL)**:
  1. Validates a manually hardcoded list of `checkout_features` rather than inspecting the actual `FEATURE_SETS` in `ModelExperimentTrainer` (Finding F-01).

---

## 3. Remediation Directives for Stage 2 - 8
1. Refactor `engineer.py` to create separate feature subsets with explicit availability timestamps.
2. Refactor `trainer.py` to support two distinct prediction regimes:
   - Early-Warning Model (Order Purchase Stage, zero fulfillment leakage).
   - Post-Delivery Diagnostic Satisfaction Model (Post-Delivery Root Cause Analysis).
3. Standardize evaluation metrics to `average_precision_score()`.
4. Refactor `state_transition.py` to implement genuine out-of-sample chronological backtesting and honest scenario simulation framing.
