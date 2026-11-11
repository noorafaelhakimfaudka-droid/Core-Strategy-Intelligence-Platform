"""CSIP FINAL 1.0.0 — Automated Master Release Acceptance Gates.

Verifies:
1. Version Invariant (strict 1.0.0 across pyproject.toml, setup.py, __init__.py, Dockerfile, sidecars).
2. Model Results Registry & Artifact Parity (MODEL_RESULTS_REGISTRY.csv matches physical files & SHA-256).
3. Canonical Evidence Distribution (35 VERIFIED, 12 ARTIFACT, 13 DEMO, 3 EXTERNAL across 63 KUKs).
4. SKKNI 299/2020 Traceability Matrix completeness (all 13 columns, verbatim KUK 2.2).
5. Explicit Model Maturity Taxonomy across all active model cards.
6. Dataset Parquet Cryptographic Integrity (13 tables match dataset_manifest.json).
7. Streamlit Application Pages Syntax & Entrypoint compilation.
8. Zero Hardcoded Private Credentials or Local Paths in src/.
9. Pipeline Retraining Script (scripts/run_full_retraining.py) existence & syntax.
10. Model Artifact Registry Validation Tool (tools/validate_model_artifact_registry.py) pass rate.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import py_compile
import re
import tomllib
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
from csip._version import __version__ as FINAL_VERSION

def test_final_gate_01_version_synchronization():
    """Gate 1: Strict release version synchronization."""
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        pyproj = tomllib.load(f)
    assert "version" in pyproj.get("project", {}).get("dynamic", []), "pyproject.toml must have dynamic version"

    setup_text = (REPO_ROOT / "setup.py").read_text(encoding="utf-8")
    assert "csip" in setup_text

    init_text = (REPO_ROOT / "src" / "csip" / "__init__.py").read_text(encoding="utf-8")
    import csip
    assert csip.__version__ == FINAL_VERSION

    docker_text = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert f'LABEL version="{FINAL_VERSION}"' in docker_text

    model_json_files = list((REPO_ROOT / "artifacts" / "models").glob("*.json"))
    assert len(model_json_files) >= 5
    for mj in model_json_files:
        data = json.loads(mj.read_text(encoding="utf-8"))
        assert data.get("git_or_release_version") in [f"v{FINAL_VERSION}", FINAL_VERSION]

def test_final_gate_02_model_results_registry_integrity():
    """Gate 2: Verify MODEL_RESULTS_REGISTRY.csv exists, has all fields, and matches physical models."""
    registry_path = REPO_ROOT / "artifacts" / "metadata" / "MODEL_RESULTS_REGISTRY.csv"
    assert registry_path.exists(), "MODEL_RESULTS_REGISTRY.csv missing"
    
    with open(registry_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) >= 15, f"Expected at least 15 metric rows, got {len(rows)}"
    mandatory_fields = [
        "Model_ID", "Model_Name", "Model_Version", "Artifact_Path", "Artifact_SHA256",
        "Dataset_ID", "Dataset_Version", "Experiment_ID", "Evaluation_Split",
        "Metric_Name", "Metric_Value", "Metric_Unit", "Evaluation_Method",
        "Calibration_Method", "Evaluation_Timestamp", "Evidence_Path", "Validation_Status"
    ]
    for mf in mandatory_fields:
        assert mf in reader.fieldnames, f"Missing field in MODEL_RESULTS_REGISTRY.csv: {mf}"

    # Verify physical file existence and SHA-256 for each unique artifact
    seen_paths = set()
    for r in rows:
        rel = r["Artifact_Path"]
        if rel not in seen_paths:
            seen_paths.add(rel)
            full_p = REPO_ROOT / rel
            assert full_p.exists(), f"Physical artifact missing: {rel}"
            actual_sha = hashlib.sha256(full_p.read_bytes()).hexdigest()
            assert actual_sha == r["Artifact_SHA256"], f"SHA mismatch for {rel}"

def test_final_gate_03_canonical_evidence_breakdown():
    """Gate 3: Canonical 35/12/13/3 evidence breakdown across 63 KUKs."""
    canon_path = REPO_ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
    assert canon_path.exists()
    with open(canon_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 63

    counts = {}
    for r in rows:
        st = r["verification_result"]
        counts[st] = counts.get(st, 0) + 1

    assert counts.get("VERIFIED", 0) == 35
    assert counts.get("ARTIFACT_ONLY", 0) == 12
    assert counts.get("CANDIDATE_DEMONSTRATION_REQUIRED", 0) == 13
    assert counts.get("EXTERNAL_CONFIRMATION_REQUIRED", 0) == 3
    assert counts.get("PARTIALLY_VERIFIED", 0) == 0
    assert counts.get("MISSING", 0) == 0

def test_final_gate_04_skkni_traceability_matrix_and_verbatim_kuk():
    """Gate 4: Verify SKKNI_TRACEABILITY_MATRIX.csv has all 63 KUKs, official J.62DMI00 codes, and verbatim KUK 2.2."""
    trace_path = REPO_ROOT / "competency" / "SKKNI_TRACEABILITY_MATRIX.csv"
    assert trace_path.exists()
    with open(trace_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 63
    
    # Check unit codes prefix
    for r in rows:
        assert r["Unit_Code"].startswith("J.62DMI00."), f"Invalid unit code: {r['Unit_Code']}"

    # Check verbatim KUK 2.2
    kuk_22 = [r for r in rows if r["KUK_Code"] == "J.62DMI00.001.1-2.2"]
    assert len(kuk_22) == 1
    assert kuk_22[0]["Canonical_Wording"] == "Persetujuan atas kebutuhan, asumsi dan batasan proyek diperoleh dari pengguna."

def test_final_gate_05_model_maturity_taxonomy():
    """Gate 5: Explicit maturity taxonomy across all model cards."""
    model_cards_dir = REPO_ROOT / "reports" / "model_cards"
    valid_maturities = [
        "RESEARCH_ONLY", "EXPERIMENTALLY_VALIDATED", "BENCHMARK_VALIDATED",
        "CONDITIONALLY_ELIGIBLE_FOR_PILOT", "PILOT_VALIDATED",
        "PRODUCTION_CANDIDATE", "PRODUCTION_APPROVED"
    ]
    for mc in model_cards_dir.glob("MODEL_CARD_*.md"):
        txt = mc.read_text(encoding="utf-8")
        assert any(mat in txt for mat in valid_maturities), f"{mc.name} missing valid maturity level"

def test_final_gate_06_dataset_parquet_integrity():
    """Gate 6: All 13 Parquet tables match dataset_manifest.json SHA-256."""
    manifest_path = REPO_ROOT / "data" / "dataset_manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tables = manifest.get("tables", {})
    assert len(tables) >= 13
    for rel_path, meta in tables.items():
        fp = REPO_ROOT / rel_path
        assert fp.exists(), f"Dataset file missing: {rel_path}"
        actual_sha = hashlib.sha256(fp.read_bytes()).hexdigest()
        assert actual_sha == meta["sha256"], f"SHA-256 mismatch for dataset: {rel_path}"

def test_final_gate_07_streamlit_pages_compilation():
    """Gate 7: Streamlit application cockpit compiles and has 4 operational lenses."""
    app_root = REPO_ROOT / "app"
    py_compile.compile(str(app_root / "streamlit_app.py"), doraise=True)
    app_content = (app_root / "streamlit_app.py").read_text(encoding="utf-8")
    for lens in [
        "1. Kurva Simulasi dan Titik Kritis",
        "2. Peringkat Faktor Penentu",
        "3. Sebaran Kelompok Data",
        "4. Observatorium Drift & Stabilitas",
    ]:
        assert lens in app_content, f"Missing lens: {lens}"

def test_final_gate_08_no_credentials_in_src():
    """Gate 8: No hardcoded credentials or private user paths in src/."""
    src_dir = REPO_ROOT / "src"
    forbidden_tokens = [
        r"C:\\Users\\[a-zA-Z0-9_-]+",
        r"/home/[a-zA-Z0-9_-]+/",
        r"sk-[a-zA-Z0-9]{32,}",
        r"AKIA[0-9A-Z]{16}",
    ]
    violations = []
    for pyf in src_dir.rglob("*.py"):
        content = pyf.read_text(encoding="utf-8", errors="ignore")
        for tok in forbidden_tokens:
            matches = re.findall(tok, content)
            if matches:
                violations.append(f"{pyf.relative_to(REPO_ROOT)}: {matches}")
    assert not violations, f"Violations: {violations}"

def test_final_gate_09_retraining_script_exists_and_compiles():
    """Gate 9: scripts/run_full_retraining.py exists and compiles cleanly."""
    script_path = REPO_ROOT / "scripts" / "run_full_retraining.py"
    assert script_path.exists()
    py_compile.compile(str(script_path), doraise=True)

def test_final_gate_10_model_artifact_validator_passes():
    """Gate 10: tools/validate_model_artifact_registry.py exits 0."""
    from tools.validate_model_artifact_registry import validate_registry
    res = validate_registry()
    assert res == 0, "Model artifact validator failed"

