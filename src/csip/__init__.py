"""CSIP: Core Strategy & Intelligence Platform.

Behavioral Decision Intelligence (BDI) Engine.

Core Principles:
1. Business & Technical Alignment > Blind Coding
2. Evidence > Assumption (Claim Levels L0-L3, Evidence Grades A-D)
3. Validation > Complexity (Strict Temporal & Feature Isolation, Out-of-Time Evaluation)
4. Explanation > Superficial Correlation (Alternative Hypothesis Testing)
5. Reproducibility > One-time Results (Deterministic Pipeline & Model Registry)
6. Honest Uncertainty > False Confidence (Prediction Intervals & Guardrails)
7. Data Science Rigor > Unnecessary Hype (ML, Deep Learning & Econometric Foundations)
"""

from csip._version import __version__

__author__ = "Rafael Hakim Souissa"

# Scientific Claim Hierarchy
CLAIM_LEVELS = {
    "L0": "Descriptive — Menggambarkan distribusi dan pola teramati dalam sampel data.",
    "L1": "Predictive — Model memprediksi target out-of-sample lebih baik dari baseline.",
    "L2": "Associational — Variabel X berhubungan statistik dengan Y terkontrol confounder.",
    "L3": "Causal — Efek perubahan intervensi X terhadap Y teridentifikasi secara kausal.",
}

# Evidence Grading Standard
EVIDENCE_GRADES = {
    "Grade A": "Kuat & Tervalidasi (Lolos seluruh uji validasi, stabil lintas waktu, mengalahkan baseline).",
    "Grade B": "Cukup / Bersyarat (Didukung bukti valid dengan asumsi/keterbatasan terdefinisi).",
    "Grade C": "Eksploratif / Lemah (Ukuran sampel kecil atau sensitif terhadap asumsi).",
    "Grade D": "Tidak Terbukti / Gagal (Hipotesis ditolak, tercatat dalam Failure Register).",
}

__all__ = [
    "CLAIM_LEVELS",
    "EVIDENCE_GRADES",
    "__version__",
]
