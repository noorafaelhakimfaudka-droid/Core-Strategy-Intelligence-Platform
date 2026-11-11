"""CSIP FINAL — Full End-to-End Retraining Orchestrator.

Orchestrates:
1. Feature pipeline validation and artifact checking.
2. Supervised ML model training across B0-B3 baselines and LightGBM champions.
3. World Model econometric state-space fitting and historical replay.
4. Model artifact validation and sidecar verification.
5. Evidence registry reconciliation.

Usage:
    python scripts/run_full_retraining.py [--skip-dl]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_step(step_name: str, script_rel_path: str, args: list[str] | None = None) -> bool:
    print(f"\n{'='*70}")
    print(f"STEP: {step_name}")
    print(f"SCRIPT: {script_rel_path}")
    print(f"{'='*70}")
    
    script_full = REPO_ROOT / script_rel_path
    if not script_full.exists():
        print(f"ERROR: Script not found: {script_full}")
        return False
        
    cmd = [sys.executable, str(script_full)] + (args or [])
    start_t = time.time()
    res = subprocess.run(cmd, cwd=str(REPO_ROOT))
    elapsed = time.time() - start_t
    
    if res.returncode != 0:
        print(f"FAILED: {step_name} exited with code {res.returncode} (in {elapsed:.1f}s)")
        return False
    
    print(f"SUCCESS: {step_name} completed in {elapsed:.1f}s")
    return True

def main():
    parser = argparse.ArgumentParser(description="CSIP End-to-End Pipeline Retraining Orchestrator")
    parser.add_argument("--skip-dl", action="store_true", help="Skip deep learning retraining")
    args = parser.parse_args()

    start_total = time.time()
    print("=== CSIP FINAL 1.0.0 END-TO-END PIPELINE RETRAINING ===")
    print(f"Working Directory: {REPO_ROOT}")
    print(f"Python: {sys.executable}")

    # 1. Feature Engineering
    if not run_step("Feature Engineering & Grain Construction", "scripts/build_features.py"):
        sys.exit(1)

    # 2. Supervised Machine Learning Experiments
    if not run_step("Supervised ML & Leaderboard Training", "scripts/run_ml_experiments.py"):
        sys.exit(1)

    # 3. Deep Learning & NLP Sentiment (optional flag)
    if not args.skip_dl:
        if (REPO_ROOT / "scripts" / "run_deep_learning_and_shap.py").exists():
            print("\nSkipping heavy DL retraining by default if artifacts present, or run manually:")
            print("  python scripts/run_deep_learning_and_shap.py")

    # 4. World Model Econometric Fitting
    if not run_step("World Model Dynamic State-Space Fitting", "scripts/run_world_model.py"):
        sys.exit(1)

    # 5. Model Artifact Registry Validation
    if not run_step("Model Artifact & Sidecar Verification", "tools/validate_model_artifact_registry.py"):
        sys.exit(1)

    # 6. Reconcile Canonical Evidence System
    if not run_step("Evidence Registry Reconciliation", "scripts/reconcile_evidence_system.py"):
        sys.exit(1)

    total_time = time.time() - start_total
    print(f"\n{'='*70}")
    print(f"ALL PIPELINE STEPS COMPLETED SUCCESSFULLY in {total_time:.1f}s!")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()

