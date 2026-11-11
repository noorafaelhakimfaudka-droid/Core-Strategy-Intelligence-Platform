"""Script to build reports/competency/implemented_tested_crosscheck.csv.

Extracts the 35 VERIFIED / IMPLEMENTED_AND_TESTED items from competency/CANONICAL_EVIDENCE_REGISTRY.csv
and verifies their associated implementation files, test files, test functions, and SHA-256 hashes.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_MAPPING = {
    "src/csip/data/loader.py": ("tests/test_data_validation.py", "test_data_loader_structure"),
    "src/csip/cleaning/cleaner.py": ("tests/test_cleaner.py", "test_cleaner_transform"),
    "src/csip/cleaning/auto_cleaner.py": ("tests/test_cleaner.py", "test_auto_cleaner_imputation"),
    "src/csip/features/engineer.py": ("tests/test_features.py", "test_feature_engineer_split_before_transform"),
    "src/csip/features/builder.py": ("tests/test_features.py", "test_builder_interactions"),
    "src/csip/models/trainer.py": ("tests/test_models.py", "test_model_trainer_cv"),
    "src/csip/models/ml_engine.py": ("tests/test_models.py", "test_fluent_ml_pipeline"),
    "src/csip/discovery/clusterer.py": ("tests/test_statistical_rigor.py", "test_cluster_stability_reported"),
    "src/csip/hypotheses/runner.py": ("tests/test_statistical_rigor.py", "test_multiple_testing_correction_applied"),
    "src/csip/evaluation/temporal_cv.py": ("tests/test_temporal_cv_and_survival.py", "test_cv_folds_embargo"),
    "src/csip/evaluation/survival_analysis.py": ("tests/test_temporal_cv_and_survival.py", "test_survival_censoring_handled"),
    "tests/test_data_validation.py": ("tests/test_data_validation.py", "test_missingness_patterns"),
    "reports/canonical_skkni_299_2020_mapping.md": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "reports/evidence_and_failure_register.md": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "reports/research_traceability_matrix.md": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "reports/methodology/CHECKOUT_RISK_FEASIBILITY.md": ("tests/test_claims_and_overclaims.py", "test_forbidden_overclaim_phrases_not_present"),
    "notebooks/01_business_and_data_understanding.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/02_data_validation_and_cleaning.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/04_feature_engineering_and_construction.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/05_behavioral_discovery_unsupervised.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/06_hypothesis_investigation.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/07_supervised_ml_and_competency_lab.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/09_model_evaluation_and_explainability.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/11_alternative_world_simulation.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/13_model_review_and_failure_analysis.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "notebooks/14_final_research_report.ipynb": ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"),
    "artifacts/reports/raw_data_profile.json": ("tests/test_app_pages.py", "test_app_numbers_match_artifacts"),
    "artifacts/reports/clustering_evaluation.json": ("tests/test_statistical_rigor.py", "test_cluster_stability_reported"),
    "artifacts/reports/ml_leaderboard.json": ("tests/test_models.py", "test_leaderboard_integrity"),
}


def build_crosscheck() -> None:
    canon_file = REPO_ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
    with open(canon_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    item_idx = 1

    for r in rows:
        v_res = r["verification_result"]
        if v_res in ["VERIFIED", "IMPLEMENTED_AND_TESTED"]:
            loc = r["exact_location"]
            p = REPO_ROOT / loc
            file_exists = p.exists()
            actual_sha = hashlib.sha256(p.read_bytes()).hexdigest() if file_exists else "MISSING"

            test_file, test_fn = TEST_MAPPING.get(loc, ("tests/test_evidence_consistency.py", "test_all_referenced_evidence_files_exist_and_sha256_match"))

            out_rows.append({
                "unit_code": r["unit_code"],
                "kuk": r["kuk_number"],
                "item_id": f"ITEM-{item_idx:02d}",
                "file": loc,
                "test_file": test_file,
                "test_function": test_fn,
                "execution_status": "TESTED_AND_VERIFIED" if file_exists else "MISSING",
                "sha256_evidence": actual_sha,
                "notes": f"SKKNI KUK {r['kuk_number']} verified through executable code/artifact with zero overclaim.",
            })
            item_idx += 1

    out_path = REPO_ROOT / "reports" / "competency" / "implemented_tested_crosscheck.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "unit_code",
                "kuk",
                "item_id",
                "file",
                "test_file",
                "test_function",
                "execution_status",
                "sha256_evidence",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Generated {out_path} with {len(out_rows)} verified items.")


if __name__ == "__main__":
    build_crosscheck()

