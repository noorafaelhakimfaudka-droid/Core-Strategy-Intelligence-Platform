"""Survival Analysis, Probability Calibration & Decision Curve Analysis Engine.

Provides:
1. KaplanMeierEstimator: Non-parametric survival curve estimation per customer segment.
2. ConcordanceIndex: Harrell's C-index for right-censored time-to-event outcomes.
3. DiscreteTimeHazardModel: Logistic regression hazard model across discrete follow-up intervals.
4. ProbabilityCalibrator: Platt scaling & Isotonic regression fit strictly on CV/validation splits,
   computing Expected Calibration Error (ECE), Brier Skill Score (BSS), and reliability diagrams.
5. DecisionCurveAnalysis: Net benefit calculation across decision thresholds and top-k% lift.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score


class KaplanMeierEstimator:
    """Non-parametric Kaplan-Meier survival curve estimator with right-censoring support."""

    def __init__(self):
        self.survival_table: Optional[pd.DataFrame] = None
        self.timeline: Optional[np.ndarray] = None
        self.survival_probabilities: Optional[np.ndarray] = None

    def fit(self, durations: np.ndarray, events: np.ndarray) -> "KaplanMeierEstimator":
        """Fits Kaplan-Meier estimator on time-to-event data.

        durations: Follow-up duration in days (positive numbers)
        events: 1 if target event observed (e.g. repeat purchase), 0 if right-censored
        """
        durations = np.asarray(durations)
        events = np.asarray(events)

        unique_times = np.sort(np.unique(durations[events == 1]))
        if len(unique_times) == 0:
            self.timeline = np.array([0, np.max(durations)])
            self.survival_probabilities = np.array([1.0, 1.0])
            return self

        n_at_risk = []
        n_events = []
        surv_prob = 1.0
        probabilities = [surv_prob]
        times = [0.0]

        for t in unique_times:
            # Customers at risk just prior to time t
            at_risk = np.sum(durations >= t)
            event_count = np.sum((durations == t) & (events == 1))
            if at_risk > 0:
                surv_prob *= 1.0 - (event_count / at_risk)
            times.append(float(t))
            probabilities.append(float(surv_prob))
            n_at_risk.append(int(at_risk))
            n_events.append(int(event_count))

        self.timeline = np.array(times)
        self.survival_probabilities = np.array(probabilities)
        self.survival_table = pd.DataFrame({
            "timeline": unique_times,
            "at_risk": n_at_risk,
            "events": n_events,
            "survival_prob": self.survival_probabilities[1:],
        })
        return self

    def predict_survival_at(self, t: float) -> float:
        """Returns S(t) probability of remaining without event beyond time t."""
        if self.timeline is None or self.survival_probabilities is None:
            raise ValueError("KaplanMeierEstimator not fitted yet.")
        idx = np.searchsorted(self.timeline, t, side="right") - 1
        idx = max(0, min(idx, len(self.survival_probabilities) - 1))
        return float(self.survival_probabilities[idx])

    def predict_risk_at(self, t: float) -> float:
        """Cumulative risk F(t) = 1 - S(t)."""
        return 1.0 - self.predict_survival_at(t)


def calculate_concordance_index(
    durations: np.ndarray,
    predicted_risks: np.ndarray,
    events: np.ndarray,
) -> float:
    """Computes Harrell's C-index for right-censored time-to-event outcomes.

    Pairs (i, j) where duration_i < duration_j and event_i == 1 are comparable.
    Concordant if predicted_risk_i > predicted_risk_j.
    """
    durations = np.asarray(durations)
    predicted_risks = np.asarray(predicted_risks)
    events = np.asarray(events)

    concordant = 0
    discordant = 0
    tied_risk = 0

    n = len(durations)
    for i in range(n):
        if events[i] != 1:
            continue
        for j in range(n):
            if durations[i] < durations[j]:
                if predicted_risks[i] > predicted_risks[j]:
                    concordant += 1
                elif predicted_risks[i] < predicted_risks[j]:
                    discordant += 1
                else:
                    tied_risk += 1

    total_pairs = concordant + discordant + tied_risk
    if total_pairs == 0:
        return 0.5
    return (concordant + 0.5 * tied_risk) / total_pairs


class DiscreteTimeHazardModel:
    """Logistic regression hazard model over binned temporal follow-up intervals."""

    def __init__(self, interval_edges: List[float] = [0, 30, 60, 90]):
        self.interval_edges = interval_edges
        self.models: Dict[int, LogisticRegression] = {}

    def fit(
        self,
        X: pd.DataFrame,
        durations: np.ndarray,
        events: np.ndarray,
    ) -> "DiscreteTimeHazardModel":
        durations = np.asarray(durations)
        events = np.asarray(events)

        for k in range(len(self.interval_edges) - 1):
            t_low = self.interval_edges[k]
            t_high = self.interval_edges[k + 1]

            # In interval k, at risk are those who survived past t_low
            at_risk_mask = durations >= t_low
            if np.sum(at_risk_mask) < 20:
                continue

            # Event occurred in this interval
            interval_event = (events == 1) & (durations >= t_low) & (durations <= t_high)
            y_k = interval_event[at_risk_mask].astype(int)
            X_k = X.loc[at_risk_mask]

            if len(np.unique(y_k)) > 1:
                clf = LogisticRegression(C=1.0, max_iter=500, random_state=42)
                clf.fit(X_k, y_k)
                self.models[k] = clf

        return self

    def predict_hazard(self, X: pd.DataFrame, interval_idx: int) -> np.ndarray:
        if interval_idx not in self.models:
            return np.zeros(len(X))
        return self.models[interval_idx].predict_proba(X)[:, 1]


class ProbabilityCalibrator:
    """Platt scaling calibrator fit strictly on validation split with ECE and BSS metrics."""

    def __init__(self):
        self.calibrator = LogisticRegression(C=1.0, max_iter=500, random_state=42)
        self.is_fitted = False

    def fit(self, val_probs: np.ndarray, y_val: np.ndarray) -> "ProbabilityCalibrator":
        """Fits sigmoid calibration strictly on validation predictions."""
        val_probs = np.clip(val_probs, 1e-6, 1.0 - 1e-6)
        log_odds = np.log(val_probs / (1.0 - val_probs)).reshape(-1, 1)
        self.calibrator.fit(log_odds, y_val)
        self.is_fitted = True
        return self

    def calibrate(self, probs: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Calibrator not fitted yet.")
        probs = np.clip(probs, 1e-6, 1.0 - 1e-6)
        log_odds = np.log(probs / (1.0 - probs)).reshape(-1, 1)
        return self.calibrator.predict_proba(log_odds)[:, 1]

    @staticmethod
    def compute_ece(
        y_true: np.ndarray,
        y_prob: np.ndarray,
        n_bins: int = 10,
    ) -> float:
        """Computes Expected Calibration Error (ECE)."""
        bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
        ece = 0.0
        n_total = len(y_true)

        for i in range(n_bins):
            bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
            if i == n_bins - 1:
                bin_mask |= y_prob == bin_edges[i + 1]

            n_bin = np.sum(bin_mask)
            if n_bin > 0:
                acc = np.mean(y_true[bin_mask])
                conf = np.mean(y_prob[bin_mask])
                ece += (n_bin / n_total) * np.abs(acc - conf)

        return float(ece)

    @staticmethod
    def compute_brier_skill_score(
        y_true: np.ndarray,
        y_prob: np.ndarray,
    ) -> float:
        """Computes Brier Skill Score (BSS) vs naive base rate persistence: 1 - (Brier / Brier_ref)."""
        brier = brier_score_loss(y_true, y_prob)
        base_rate = np.mean(y_true)
        brier_ref = brier_score_loss(y_true, np.full_like(y_true, base_rate, dtype=float))
        if brier_ref == 0:
            return 0.0
        return float(1.0 - (brier / brier_ref))


def compute_decision_curve_analysis(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    thresholds: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """Computes Net Benefit across decision probability thresholds for Decision Curve Analysis."""
    if thresholds is None:
        thresholds = np.linspace(0.02, 0.50, 25)

    n = len(y_true)
    prevalence = np.mean(y_true)

    rows = []
    for pt in thresholds:
        tp = np.sum((y_prob >= pt) & (y_true == 1))
        fp = np.sum((y_prob >= pt) & (y_true == 0))

        # Net benefit formula
        net_benefit_model = (tp / n) - (fp / n) * (pt / (1.0 - pt))
        net_benefit_all = prevalence - (1.0 - prevalence) * (pt / (1.0 - pt))
        net_benefit_none = 0.0

        rows.append({
            "threshold": round(float(pt), 4),
            "net_benefit_model": round(float(net_benefit_model), 6),
            "net_benefit_treat_all": round(float(net_benefit_all), 6),
            "net_benefit_treat_none": 0.0,
        })

    return pd.DataFrame(rows)


def compute_top_k_lift(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    k_percentiles: List[float] = [0.05, 0.10, 0.20],
) -> Dict[str, float]:
    """Computes lift at top k% predicted risk instances."""
    base_prevalence = float(np.mean(y_true))
    n = len(y_true)
    sorted_idx = np.argsort(-y_prob)

    lifts = {}
    for k in k_percentiles:
        top_n = max(1, int(n * k))
        top_y = y_true[sorted_idx[:top_n]]
        top_precision = float(np.mean(top_y))
        lift = top_precision / base_prevalence if base_prevalence > 0 else 1.0
        lifts[f"lift_top_{int(k*100)}pct"] = round(float(lift), 3)

    return lifts

