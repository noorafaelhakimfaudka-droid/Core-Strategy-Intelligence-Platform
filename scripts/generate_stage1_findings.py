import json
from pathlib import Path

AUDIT_DIR = Path("reports/v6/audit")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

findings_register = {
    "version": "6.0.0-audit",
    "timestamp": "2026-11-11T14:15:00+07:00",
    "findings": [
        {
            "finding_id": "F-01",
            "title": "Prediction Horizon and Post-Outcome Feature Leakage",
            "severity": "CRITICAL",
            "status": "VERIFIED",
            "affected_files": [
                "src/csip/models/trainer.py",
                "src/csip/features/engineer.py",
                "config/features.yaml",
                "tests/test_feature_leakage.py"
            ],
            "empirical_evidence": (
                "Feature sets E2_experience_only and E3_combined_interactions in "
                "ModelExperimentTrainer utilize 'delivery_lead_time_days', 'delivery_delay_days', "
                "'is_late', 'delay_x_freight_ratio', and 'high_value_late_flag' to predict "
                "'negative_review_flag'. These features require 'order_delivered_customer_date', "
                "which is only recorded days/weeks after purchase. Furthermore, tests/test_feature_leakage.py "
                "validated a simulated manual list rather than inspecting the trainer's actual FEATURE_SETS."
            ),
            "remediation_strategy": (
                "1. Explicitly bifurcate prediction tasks into (A) Early-Warning Pre-Fulfillment Model "
                "(features strictly known as-of purchase/approval timestamp) and (B) Post-Delivery "
                "Diagnostic Satisfaction Model (for post-hoc customer experience root cause analysis).\n"
                "2. Create an authoritative Feature Availability Registry.\n"
                "3. Update test_feature_leakage.py to inspect actual trainer feature sets."
            )
        },
        {
            "finding_id": "F-02",
            "title": "Target Label Contamination from Missing Review Imputation",
            "severity": "HIGH",
            "status": "VERIFIED",
            "affected_files": [
                "src/csip/features/engineer.py",
                "src/csip/models/trainer.py"
            ],
            "empirical_evidence": (
                "In FeatureEngineer.build_order_level(), missing review_score values (646 orders, 0.67%) "
                "were imputed via df['review_score'].fillna(3), converting unobserved customer feedback "
                "into an observed neutral rating (3.0). Consequently, negative_review_flag <= 2 assigned "
                "label 0 (non-negative) to missing reviews, contaminating the ground truth."
            ),
            "remediation_strategy": (
                "1. Restrict the supervised learning population for review prediction strictly to orders with "
                "observed reviews (review_score.notnull()).\n"
                "2. Document sample exclusion explicitly (N=646 excluded, remaining N=95,824 delivered orders).\n"
                "3. Recalculate true class prevalence (12,272 / 95,824 = 12.81%)."
            )
        },
        {
            "finding_id": "F-03",
            "title": "Model Evaluation Metric Inconsistencies and Overestimation",
            "severity": "HIGH",
            "status": "VERIFIED",
            "affected_files": [
                "src/csip/models/trainer.py",
                "artifacts/reports/ml_leaderboard.json",
                "reports/model_evaluation_and_review_report.md"
            ],
            "empirical_evidence": (
                "ModelExperimentTrainer used trapezoidal auc(rec, prec) over precision_recall_curve(). "
                "For constant baseline models (B0 naive majority), linear interpolation between positive prevalence "
                "(~0.11) and 1.0 at recall=0 produced an artificial PR-AUC of 0.5545 instead of the true "
                "baseline (positive prevalence). Scikit-learn's average_precision_score() is the standard "
                "unbiased metric. Additionally, validation set results were conflated with locked holdout test results."
            ),
            "remediation_strategy": (
                "1. Standardize PR-AUC to average_precision_score().\n"
                "2. Strictly enforce that hyperparameter tuning and model selection occur exclusively on "
                "the validation set, and locked holdout test set is evaluated once for the final models.\n"
                "3. Clearly demarcate validation leaderboard vs test leaderboard in artifacts and reports."
            )
        },
        {
            "finding_id": "F-04",
            "title": "World Model Discrepancy Between Formulation and Implementation",
            "severity": "HIGH",
            "status": "VERIFIED",
            "affected_files": [
                "src/csip/world/state_transition.py",
                "scripts/run_world_model.py",
                "notebooks/11_alternative_world_simulation.ipynb"
            ],
            "empirical_evidence": (
                "The documented formula claims S_{t+1} = C + Phi * S_t + Gamma * A_t + Psi * E_t + epsilon_t, "
                "but the Ridge regression was fitted solely on lag-1 state S_t (S_{t+1} = C + Phi * S_t). "
                "Actions were injected as heuristic ad-hoc coordinate offsets in scaled space. "
                "Furthermore, backtest_historical_replay() evaluated on the exact same dataset used for fitting, "
                "creating in-sample evaluation bias."
            ),
            "remediation_strategy": (
                "1. Formulate the model honestly as an Empirical Autoregressive Transition Model combined with "
                "Scenario Intervention Sensitivity Analysis.\n"
                "2. Remove unsupported causal claims and document intervention effects as user-defined scenario "
                "policy levers rather than estimated causal coefficients.\n"
                "3. Implement an out-of-sample chronological backtest split (Train: weeks 1-60, Test: weeks 61-80)."
            )
        },
        {
            "finding_id": "F-05",
            "title": "Evidence Registry Granularity and Disclosure of Proxy Approvals",
            "severity": "MEDIUM",
            "status": "PARTIALLY_VERIFIED",
            "affected_files": [
                "reports/evidence/evidence_registry.json",
                "reports/evidence/evidence_validation_report.md"
            ],
            "empirical_evidence": (
                "V5 established 63 canonical KUK records mapped to 30 unique physical files with 3 PARTIALLY_VERIFIED "
                "records (UK-01 KUK 2.2, 3.3, 4.3). While this was honest, additional scrutiny is needed on UK-11 "
                "(reviewing modeling quality) to ensure model review criteria are backed by reproducible validation "
                "code rather than solely narrative text."
            ),
            "remediation_strategy": (
                "1. Verify that all 63 records point to existing, reproducible artifacts.\n"
                "2. Maintain strict transparency regarding academic/open-source simulation limitations.\n"
                "3. Provide exact code symbol / section references for every single record."
            )
        },
        {
            "finding_id": "F-06",
            "title": "Documentation Cross-Reference Inconsistencies",
            "severity": "MEDIUM",
            "status": "PARTIALLY_VERIFIED",
            "affected_files": [
                "README.md",
                "FINAL_CSIP_AUDIT_REPORT.md",
                "reports/canonical_skkni_299_2020_mapping.md"
            ],
            "empirical_evidence": (
                "While V5 eliminated discrepancies between 48 vs 63 KUKs and fixed hardcoded paths, historical "
                "markdown files still contain residual references to earlier iteration counts (e.g. 72 vs 83 vs 84 "
                "tests, previous V4 nomenclature). Centralized automated report generation is needed."
            ),
            "remediation_strategy": (
                "1. Establish machine-readable single source of truth for V6.\n"
                "2. Generate all V6 validation reports programmatically from execution outputs.\n"
                "3. Eliminate legacy version confusion."
            )
        }
    ]
}

with open(AUDIT_DIR / "initial_findings_register.json", "w", encoding="utf-8") as f:
    json.dump(findings_register, f, indent=2)

print("Saved reports/v6/audit/initial_findings_register.json")
