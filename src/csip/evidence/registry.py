"""CSIP Evidence Registry, Hypothesis Registry & Failure Register.

Enforces Claim Levels (L0-L3) and Evidence Grades (A-D) across discoveries,
statistical hypotheses, and documented model limitations.
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
    """Scientific Claim Hierarchy."""
    L0_DESCRIPTIVE = "L0 (Descriptive)"
    L1_PREDICTIVE = "L1 (Predictive)"
    L2_ASSOCIATIONAL = "L2 (Associational)"
    L3_CAUSAL = "L3 (Causal)"


class EvidenceGrade(str, Enum):
    """Evidence Grading Standard."""
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
    pipeline_stage: str = "Discovery & EDA"
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
    pipeline_stage: str = "Hypothesis Testing"
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
    pipeline_stage: str = "Model Review & Failure Audit"


class EvidenceRegistry:
    """Central repository managing scientific claims, hypotheses, discoveries, and failure logs."""

    def __init__(self, registry_dir: Union[str, Path] = "artifacts/reports") -> None:
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)

        self.discoveries: Dict[str, DiscoveryEntry] = {}
        self.hypotheses: Dict[str, HypothesisRecord] = {}
        self.failures: List[FailureRecord] = []

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
            except Exception:
                pass

    def register_discovery(self, discovery: DiscoveryEntry) -> None:
        """Register a behavioral insight pattern."""
        self.discoveries[discovery.discovery_id] = discovery

    def register_hypothesis(self, hypothesis: HypothesisRecord) -> None:
        """Register or update a research hypothesis test record."""
        self.hypotheses[hypothesis.hypothesis_id] = hypothesis

    def record_failure(self, failure: FailureRecord) -> None:
        """Record an explicit limitation, rejected model, or failed hypothesis in Failure Register."""
        self.failures = [f for f in self.failures if f.failure_id != failure.failure_id]
        self.failures.append(failure)

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

    def save_registry_snapshot(self, filename: str = "evidence_registry_snapshot.json") -> Path:
        """Persist full evidence registry state to disk for Streamlit and diagnostic inspection."""
        out_path = self.registry_dir / filename
        data = {
            "saved_at": datetime.now().isoformat(),
            "discoveries": {k: asdict(v) for k, v in self.discoveries.items()},
            "hypotheses": {k: asdict(v) for k, v in self.hypotheses.items()},
            "failures": [asdict(f) for f in self.failures],
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return out_path
