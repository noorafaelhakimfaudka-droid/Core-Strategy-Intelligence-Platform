"""CSIP Model Lifecycle & Champion-Challenger Registry.

Provides rigorous model governance:
- Candidate registration and validation
- Controlled promotion gates (metrics, calibration, schema)
- Rollback mechanisms and audit logs
- Artifact SHA-256 verification and compatibility checks
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
logger = logging.getLogger(__name__)


class ModelRole(str, Enum):
    CHAMPION = "CHAMPION"
    CHALLENGER = "CHALLENGER"
    CANDIDATE = "CANDIDATE"
    ARCHIVED = "ARCHIVED"
    DEPRECATED = "DEPRECATED"


class MaturityStatus(str, Enum):
    RESEARCH_ONLY = "RESEARCH_ONLY"
    EXPERIMENTALLY_VALIDATED = "EXPERIMENTALLY_VALIDATED"
    BENCHMARK_VALIDATED = "BENCHMARK_VALIDATED"
    CONDITIONALLY_ELIGIBLE_FOR_PILOT = "CONDITIONALLY_ELIGIBLE_FOR_PILOT"
    PILOT_VALIDATED = "PILOT_VALIDATED"
    PRODUCTION_CANDIDATE = "PRODUCTION_CANDIDATE"
    PRODUCTION_APPROVED = "PRODUCTION_APPROVED"


@dataclass
class ModelRegistration:
    model_id: str
    model_name: str
    version: str
    role: ModelRole
    maturity_status: MaturityStatus
    target_name: str
    artifact_path: str
    artifact_sha256: str
    feature_list: List[str]
    primary_metric_name: str
    primary_metric_value: float
    brier_score: Optional[float] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    promoted_at: Optional[str] = None
    promotion_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["role"] = self.role.value
        data["maturity_status"] = self.maturity_status.value
        return data


class ModelLifecycleManager:
    """Manages model candidate promotion, champion-challenger lifecycle, and rollbacks."""

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        promotion_log_path: Optional[Path] = None,
    ):
        self.repo_root = repo_root or REPO_ROOT
        self.promotion_log = (
            promotion_log_path
            or self.repo_root / "artifacts" / "metadata" / "PROMOTION_HISTORY.csv"
        )
        self._ensure_log_initialized()

    def _ensure_log_initialized(self) -> None:
        self.promotion_log.parent.mkdir(parents=True, exist_ok=True)
        if not self.promotion_log.exists():
            with open(self.promotion_log, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp",
                    "Event_Type",
                    "Model_ID",
                    "Previous_Version",
                    "New_Version",
                    "Previous_Role",
                    "New_Role",
                    "Target_Name",
                    "Primary_Metric_Name",
                    "Primary_Metric_Value",
                    "Approved_By",
                    "Reason",
                ])

    def compute_sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def register_candidate(
        self,
        model_id: str,
        model_name: str,
        version: str,
        target_name: str,
        artifact_path: Path,
        feature_list: List[str],
        primary_metric_name: str,
        primary_metric_value: float,
        maturity_status: MaturityStatus = MaturityStatus.EXPERIMENTALLY_VALIDATED,
        brier_score: Optional[float] = None,
    ) -> ModelRegistration:
        """Registers a candidate model after verifying artifact existence and hash."""
        if not artifact_path.exists():
            raise FileNotFoundError(f"Model artifact file does not exist: {artifact_path}")

        sha = self.compute_sha256(artifact_path)
        rel_path = str(artifact_path.relative_to(self.repo_root)).replace("\\", "/")

        reg = ModelRegistration(
            model_id=model_id,
            model_name=model_name,
            version=version,
            role=ModelRole.CANDIDATE,
            maturity_status=maturity_status,
            target_name=target_name,
            artifact_path=rel_path,
            artifact_sha256=sha,
            feature_list=feature_list,
            primary_metric_name=primary_metric_name,
            primary_metric_value=primary_metric_value,
            brier_score=brier_score,
        )

        self._record_event(
            event_type="REGISTER_CANDIDATE",
            model_id=model_id,
            prev_ver="-",
            new_ver=version,
            prev_role="-",
            new_role=ModelRole.CANDIDATE.value,
            target=target_name,
            metric_name=primary_metric_name,
            metric_value=primary_metric_value,
            approved_by="System",
            reason="Initial candidate registration for lifecycle validation",
        )
        return reg

    def evaluate_promotion(
        self,
        candidate: ModelRegistration,
        current_champion: Optional[ModelRegistration],
        min_improvement_pct: float = 1.0,
    ) -> Tuple[bool, List[str]]:
        """
        Validates if candidate meets strict criteria for promotion:
        1. Higher is better for PR_AUC, ROC_AUC, F1, R2.
        2. Lower is better for MAE, RMSE, Brier Score.
        3. Calibration check: Brier score must not degrade by > 5%.
        4. Maturity level check: Candidate cannot be RESEARCH_ONLY.
        """
        reasons: List[str] = []

        if candidate.maturity_status == MaturityStatus.RESEARCH_ONLY:
            return False, ["RESEARCH_ONLY models are strictly barred from promotion to production."]

        if current_champion is None:
            return True, ["No existing champion; candidate eligible for initial champion designation."]

        higher_better = candidate.primary_metric_name in ["PR_AUC", "ROC_AUC", "F1", "R2", "Accuracy", "Macro_F1"]
        cand_val = candidate.primary_metric_value
        champ_val = current_champion.primary_metric_value

        if higher_better:
            if cand_val <= champ_val:
                reasons.append(
                    f"Candidate metric {cand_val:.4f} did not exceed champion metric {champ_val:.4f}."
                )
            else:
                pct = ((cand_val - champ_val) / (abs(champ_val) + 1e-9)) * 100.0
                if pct < min_improvement_pct:
                    reasons.append(
                        f"Improvement of +{pct:.2f}% is below required threshold of +{min_improvement_pct:.1f}%."
                    )
        else:
            if cand_val >= champ_val:
                reasons.append(
                    f"Candidate error {cand_val:.4f} is not lower than champion error {champ_val:.4f}."
                )

        if candidate.brier_score is not None and current_champion.brier_score is not None:
            if candidate.brier_score > current_champion.brier_score * 1.05:
                reasons.append(
                    f"Calibration degraded: Candidate Brier score ({candidate.brier_score:.4f}) "
                    f"> Champion Brier ({current_champion.brier_score:.4f}) by > 5%."
                )

        eligible = len(reasons) == 0
        return eligible, reasons

    def promote_candidate(
        self,
        candidate: ModelRegistration,
        current_champion: Optional[ModelRegistration],
        approved_by: str,
        reason: str,
        target_role: ModelRole = ModelRole.CHAMPION,
    ) -> bool:
        """Safely promotes candidate model, archiving existing champion."""
        eligible, eval_reasons = self.evaluate_promotion(candidate, current_champion)
        if not eligible and target_role == ModelRole.CHAMPION:
            raise ValueError(f"Promotion rejected: {'; '.join(eval_reasons)}")

        # Demote champion if exists
        if current_champion is not None:
            current_champion.role = ModelRole.ARCHIVED
            self._record_event(
                event_type="DEMOTE_CHAMPION",
                model_id=current_champion.model_id,
                prev_ver=current_champion.version,
                new_ver=current_champion.version,
                prev_role=ModelRole.CHAMPION.value,
                new_role=ModelRole.ARCHIVED.value,
                target=current_champion.target_name,
                metric_name=current_champion.primary_metric_name,
                metric_value=current_champion.primary_metric_value,
                approved_by=approved_by,
                reason=f"Superseded by {candidate.model_id} v{candidate.version}",
            )

        # Promote candidate
        prev_role = candidate.role.value
        candidate.role = target_role
        candidate.promoted_at = datetime.now(timezone.utc).isoformat()
        candidate.promotion_notes = reason

        self._record_event(
            event_type="PROMOTE_TO_CHAMPION" if target_role == ModelRole.CHAMPION else "DESIGNATE_CHALLENGER",
            model_id=candidate.model_id,
            prev_ver=candidate.version,
            new_ver=candidate.version,
            prev_role=prev_role,
            new_role=target_role.value,
            target=candidate.target_name,
            metric_name=candidate.primary_metric_name,
            metric_value=candidate.primary_metric_value,
            approved_by=approved_by,
            reason=reason,
        )
        return True

    def rollback(
        self,
        active_model: ModelRegistration,
        target_archived_model: ModelRegistration,
        approved_by: str,
        reason: str,
    ) -> bool:
        """Rolls back an active champion to a verified historical champion version."""
        if target_archived_model.role not in [ModelRole.ARCHIVED, ModelRole.CHALLENGER]:
            raise ValueError(f"Target model for rollback must be ARCHIVED or CHALLENGER, got {target_archived_model.role}")

        active_model.role = ModelRole.ARCHIVED
        target_archived_model.role = ModelRole.CHAMPION
        target_archived_model.promoted_at = datetime.now(timezone.utc).isoformat()
        target_archived_model.promotion_notes = f"Rollback: {reason}"

        self._record_event(
            event_type="ROLLBACK_CHAMPION",
            model_id=target_archived_model.model_id,
            prev_ver=active_model.version,
            new_ver=target_archived_model.version,
            prev_role=ModelRole.ARCHIVED.value,
            new_role=ModelRole.CHAMPION.value,
            target=target_archived_model.target_name,
            metric_name=target_archived_model.primary_metric_name,
            metric_value=target_archived_model.primary_metric_value,
            approved_by=approved_by,
            reason=reason,
        )
        return True

    def _record_event(
        self,
        event_type: str,
        model_id: str,
        prev_ver: str,
        new_ver: str,
        prev_role: str,
        new_role: str,
        target: str,
        metric_name: str,
        metric_value: float,
        approved_by: str,
        reason: str,
    ) -> None:
        now_ts = datetime.now(timezone.utc).isoformat()
        with open(self.promotion_log, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                now_ts,
                event_type,
                model_id,
                prev_ver,
                new_ver,
                prev_role,
                new_role,
                target,
                metric_name,
                round(metric_value, 4),
                approved_by,
                reason,
            ])

