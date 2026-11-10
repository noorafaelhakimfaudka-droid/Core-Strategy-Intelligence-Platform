"""CSIP: Computational Society Intelligence Platform.

Behavioral Decision Intelligence (BDI) MVP Module.
Master Edition — SKKNI, BNSP & Industry Portfolio Compliant.

Core Principles:
1. Business & Technical Alignment > Blind Coding (SKKNI Unit 1 & 2)
2. Evidence > Assumption (Claim Levels L0-L3, Evidence Grades A-D)
3. Validation > Complexity (Zero Data Leakage, Out-of-Time Evaluation)
4. Explanation > Superficial Correlation (Alternative Hypothesis Testing)
5. Reproducibility > One-time Results (Deterministic Pipeline & Audit Registry)
6. Honest Uncertainty > False Confidence (Prediction Intervals & Guardrails)
7. Data Science Rigor > Unnecessary AI Hype (Pure ML/DL/Stats Foundations)
"""

__version__ = "0.1.0"
__author__ = "CSIP Data Science Team"

# 11 Unit Kompetensi SKKNI BNSP Registry
SKKNI_UNITS = {
    "UK-01": "Menentukan Objektif Bisnis",
    "UK-02": "Menentukan Tujuan Teknis Data Science",
    "UK-03": "Menelaah Data",
    "UK-04": "Memvalidasi Data",
    "UK-05": "Menentukan Objek Data",
    "UK-06": "Membersihkan Data",
    "UK-07": "Mengkonstruksi Data",
    "UK-08": "Membangun Skenario Model",
    "UK-09": "Membangun Model",
    "UK-10": "Mengevaluasi Hasil Pemodelan",
    "UK-11": "Melakukan Proses Review Pemodelan",
}

# Scientific Claim Hierarchy (PRD Section 7.1)
CLAIM_LEVELS = {
    "L0": "Descriptive — Menggambarkan distribusi dan pola teramati dalam sampel data.",
    "L1": "Predictive — Model memprediksi target out-of-sample lebih baik dari baseline.",
    "L2": "Associational — Variabel X berhubungan statistik dengan Y terkontrol confounder.",
    "L3": "Causal — Efek perubahan intervensi X terhadap Y teridentifikasi secara kausal.",
}

# Evidence Grading Standard (PRD Section 7.2)
EVIDENCE_GRADES = {
    "Grade A": "Kuat & Tervalidasi (Lolos seluruh gates, stabil lintas waktu, mengalahkan baseline).",
    "Grade B": "Cukup / Bersyarat (Didukung bukti valid dengan asumsi/keterbatasan terdefinisi).",
    "Grade C": "Eksploratif / Lemah (Ukuran sampel kecil atau sensitif terhadap asumsi).",
    "Grade D": "Tidak Terbukti / Gagal (Hipotesis ditolak, masuk Failure Register).",
}

__all__ = [
    "SKKNI_UNITS",
    "CLAIM_LEVELS",
    "EVIDENCE_GRADES",
    "__version__",
]
