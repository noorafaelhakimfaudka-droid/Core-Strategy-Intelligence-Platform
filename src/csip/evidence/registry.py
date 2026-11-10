"""CSIP Evidence Registry, Hypothesis Registry & SKKNI Traceability.

SKKNI Compliance:
- [UK-01 Objektif Bisnis] & [UK-02 Tujuan Teknis DS]: Business & technical goal tracking.
- [UK-10 Mengevaluasi Hasil Pemodelan]: Review of empirical evidence and model performance.
- [UK-11 Melakukan Proses Review Pemodelan]: Failure register, claim level governance, and audit trails.

Enforces Claim Levels (L0-L3) and Evidence Grades (A-D) as mandated by PRD Section 7.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd


class ClaimLevel(str, Enum):
    """Scientific Claim Hierarchy (PRD Section 7.1)."""
    L0_DESCRIPTIVE = "L0 (Descriptive)"
    L1_PREDICTIVE = "L1 (Predictive)"
    L2_ASSOCIATIONAL = "L2 (Associational)"
    L3_CAUSAL = "L3 (Causal)"


class EvidenceGrade(str, Enum):
    """Evidence Grading Standard (PRD Section 7.2)."""
    GRADE_A = "Grade A (Kuat & Tervalidasi)"
    GRADE_B = "Grade B (Cukup / Bersyarat)"
    GRADE_C = "Grade C (Eksploratif / Lemah)"
    GRADE_D = "Grade D (Tidak Terbukti / Gagal)"


class HypothesisStatus(str, Enum):
    """Hypothesis lifecycle status."""
    UNTESTED = "UNTESTED"
    SUPPORTED = "SUPPORTED"
    REJECTED = "REJECTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    INDISTINGUISHABLE = "INDISTINGUISHABLE"


@dataclass
class DiscoveryEntry:
    """An empirical behavioral pattern discovered via EDA or clustering."""
    discovery_id: str
    title: str
    description: str
    discovered_at: str
    grain: str
    key_metrics: Dict[str, Any]
    skkni_unit: str = "UK-03 Menelaah Data"
    claim_level: str = ClaimLevel.L0_DESCRIPTIVE.value
    evidence_grade: str = EvidenceGrade.GRADE_B.value
    notes: Optional[str] = None


@dataclass
class HypothesisRecord:
    """Structured record of a tested research hypothesis."""
    hypothesis_id: str
    statement: str
    analysis_type: str
    test_statistic_name: str
    test_statistic_value: Optional[float]
    p_value: Optional[float]
    p_value_adjusted: Optional[float]
    effect_size: Optional[float]
    confidence_interval_95: Optional[List[float]]
    status: str = HypothesisStatus.UNTESTED.value
    claim_level: str = ClaimLevel.L2_ASSOCIATIONAL.value
    evidence_grade: str = EvidenceGrade.GRADE_C.value
    skkni_unit: str = "UK-08 Membangun Skenario Model"
    falsification_tested: bool = False
    alternative_explanations_tested: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class FailureRecord:
    """Record of a failed model, rejected hypothesis, or structural limitation."""
    failure_id: str
    component_type: str  # "model", "hypothesis", "data_quality", "simulation"
    description: str
    root_cause: str
    impact_assessment: str
    mitigation_action: str
    recorded_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    skkni_unit: str = "UK-11 Melakukan Proses Review Pemodelan"


@dataclass
class SKKNITraceabilityItem:
    """Single item tracing SKKNI unit to code, notebooks, and evidence."""
    unit_code: str
    unit_title: str
    implementation_in_csip: str
    code_locations: List[str]
    notebook_locations: List[str]
    report_artifacts: List[str]
    status: str = "IMPLEMENTED"  # IMPLEMENTED, TESTED, VERIFIED, FAILED


class EvidenceRegistry:
    """Central repository managing scientific claims, hypotheses, discoveries, and audit trails."""

    def __init__(self, registry_dir: Union[str, Path] = "artifacts/reports") -> None:
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)

        self.discoveries: Dict[str, DiscoveryEntry] = {}
        self.hypotheses: Dict[str, HypothesisRecord] = {}
        self.failures: List[FailureRecord] = []
        self.skkni_matrix: Dict[str, SKKNITraceabilityItem] = {}

        self._initialize_default_skkni_matrix()
        self._load_existing_snapshot()

    def _load_existing_snapshot(self, filename: str = "evidence_registry_snapshot.json") -> None:
        """Load previously saved registry state if present on disk."""
        snapshot_file = self.registry_dir / filename
        if snapshot_file.exists():
            try:
                with open(snapshot_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in data.get("discoveries", {}).items():
                    self.discoveries[k] = DiscoveryEntry(**v)
                for k, v in data.get("hypotheses", {}).items():
                    self.hypotheses[k] = HypothesisRecord(**v)
                for f_dict in data.get("failures", []):
                    self.failures.append(FailureRecord(**f_dict))
                for k, v in data.get("skkni_matrix", {}).items():
                    self.skkni_matrix[k] = SKKNITraceabilityItem(**v)
            except Exception:
                pass

    def _initialize_default_skkni_matrix(self) -> None:
        """Seed the 11 SKKNI BNSP competence units traceability mapping."""
        units_spec = [
            (
                "UK-01",
                "Menentukan Objektif Bisnis",
                "Perumusan masalah retensi, friksi ongkir, dan kepuasan pengiriman.",
                ["config/business_objectives.yaml", "config/analysis_plan.yaml"],
                ["notebooks/01_business_and_data_understanding.ipynb"],
                ["reports/skkni_bnsp_traceability_matrix.md"],
            ),
            (
                "UK-02",
                "Menentukan Tujuan Teknis Data Science",
                "Target teknis PR-AUC, ROC-AUC, MAE, Silhouette, dan batas baseline.",
                ["config/models.yaml", "config/business_objectives.yaml"],
                ["notebooks/01_business_and_data_understanding.ipynb"],
                ["reports/skkni_bnsp_traceability_matrix.md"],
            ),
            (
                "UK-03",
                "Menelaah Data",
                "Profiling relasional 9 tabel Olist, distribusi, dan eksplorasi EDA.",
                ["src/csip/data/loader.py"],
                ["notebooks/01_business_and_data_understanding.ipynb", "notebooks/03_exploratory_data_analysis.ipynb"],
                ["data/data_dictionary.md"],
            ),
            (
                "UK-04",
                "Memvalidasi Data",
                "Pemeriksaan skema, duplikasi PK, dan kronologi timestamp.",
                ["src/csip/data/loader.py", "tests/test_data_validation.py"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["reports/data_quality_report.md"],
            ),
            (
                "UK-05",
                "Menentukan Objek Data",
                "Pemisahan 4 grain analitik dan mitigasi right-censoring delta_w=90 hari.",
                ["config/data.yaml", "config/analysis_plan.yaml"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["reports/skkni_bnsp_traceability_matrix.md"],
            ),
            (
                "UK-06",
                "Membersihkan Data",
                "Penyaringan status delivered, deduplikasi koordinat dan ulasan, imputasi.",
                ["src/csip/cleaning/"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["reports/data_quality_report.md"],
            ),
            (
                "UK-07",
                "Mengkonstruksi Data",
                "Rekayasa fitur ekonomi, pengalaman, histori as-of, dan interaksi non-linear.",
                ["config/features.yaml", "src/csip/features/", "tests/test_feature_leakage.py"],
                ["notebooks/04_feature_engineering_and_construction.ipynb"],
                ["reports/skkni_bnsp_traceability_matrix.md"],
            ),
            (
                "UK-08",
                "Membangun Skenario Model",
                "Perancangan matriks eksperimen E0-E9, hipotesis H1-H6, dan temporal split.",
                ["config/models.yaml", "config/scenarios.yaml", "config/analysis_plan.yaml"],
                ["notebooks/06_hypothesis_investigation.ipynb"],
                ["reports/hypothesis_report.md"],
            ),
            (
                "UK-09",
                "Membangun Model",
                "Pelatihan model statistik (B1), ML klasik (B2, B3), dan Deep Learning (B4).",
                ["src/csip/models/"],
                ["notebooks/07_supervised_ml_and_competency_lab.ipynb", "notebooks/08_neural_network_and_deep_learning.ipynb"],
                ["artifacts/models/"],
            ),
            (
                "UK-10",
                "Mengevaluasi Hasil Pemodelan",
                "Evaluasi holdout temporal, PR-AUC, kalibrasi, SHAP, dan verifikasi World Model.",
                ["src/csip/evaluation/", "src/csip/scenarios/"],
                ["notebooks/09_model_evaluation_and_explainability.ipynb", "notebooks/11_alternative_world_simulation.ipynb"],
                ["reports/model_evaluation_and_review_report.md"],
            ),
            (
                "UK-11",
                "Melakukan Proses Review Pemodelan",
                "Audit klaim L0-L3, ablation study, Failure Register, dan verifikasi Streamlit.",
                ["src/csip/evidence/registry.py", "tests/test_artifact_parity.py"],
                ["notebooks/13_model_review_and_failure_analysis.ipynb", "notebooks/14_final_research_and_bnsp_report.ipynb"],
                ["reports/evidence_and_failure_register.md"],
            ),
        ]

        for code, title, desc, code_locs, nb_locs, rpt_locs in units_spec:
            self.skkni_matrix[code] = SKKNITraceabilityItem(
                unit_code=code,
                unit_title=title,
                implementation_in_csip=desc,
                code_locations=code_locs,
                notebook_locations=nb_locs,
                report_artifacts=rpt_locs,
                status="IMPLEMENTED",
            )

    def register_discovery(self, discovery: DiscoveryEntry) -> None:
        """Register a behavioral insight pattern."""
        self.discoveries[discovery.discovery_id] = discovery

    def register_hypothesis(self, hypothesis: HypothesisRecord) -> None:
        """Register or update a research hypothesis test record."""
        self.hypotheses[hypothesis.hypothesis_id] = hypothesis

    def record_failure(self, failure: FailureRecord) -> None:
        """Record an explicit limitation, rejected model, or failed hypothesis in Failure Register."""
        # Avoid duplicate failure_id
        self.failures = [f for f in self.failures if f.failure_id != failure.failure_id]
        self.failures.append(failure)

    def update_skkni_status(self, unit_code: str, status: str) -> None:
        """Update implementation/verification status of an SKKNI unit."""
        if unit_code in self.skkni_matrix:
            self.skkni_matrix[unit_code].status = status

    def export_hypotheses_df(self) -> pd.DataFrame:
        """Convert hypothesis records to a pandas DataFrame."""
        rows = [asdict(h) for h in self.hypotheses.values()]
        return pd.DataFrame(rows)

    def export_discoveries_df(self) -> pd.DataFrame:
        """Convert discoveries to a pandas DataFrame."""
        rows = [asdict(d) for d in self.discoveries.values()]
        return pd.DataFrame(rows)

    def export_failures_df(self) -> pd.DataFrame:
        """Convert failures to a pandas DataFrame."""
        rows = [asdict(f) for f in self.failures]
        return pd.DataFrame(rows)

    def export_skkni_matrix_df(self) -> pd.DataFrame:
        """Convert SKKNI traceability matrix to a pandas DataFrame."""
        rows = []
        for item in self.skkni_matrix.values():
            d = asdict(item)
            d["code_locations"] = ", ".join(d["code_locations"])
            d["notebook_locations"] = ", ".join(d["notebook_locations"])
            d["report_artifacts"] = ", ".join(d["report_artifacts"])
            rows.append(d)
        return pd.DataFrame(rows)

    def save_registry_snapshot(self, filename: str = "evidence_registry_snapshot.json") -> Path:
        """Persist full evidence registry state to disk for Streamlit and audit inspection."""
        out_path = self.registry_dir / filename
        data = {
            "saved_at": datetime.now().isoformat(),
            "discoveries": {k: asdict(v) for k, v in self.discoveries.items()},
            "hypotheses": {k: asdict(v) for k, v in self.hypotheses.items()},
            "failures": [asdict(f) for f in self.failures],
            "skkni_matrix": {k: asdict(v) for k, v in self.skkni_matrix.items()},
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return out_path

