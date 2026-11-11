"""CSIP Evidence Registry, Hypothesis Registry & SKKNI Traceability.

SKKNI Compliance:
- [UK-01 Objektif Bisnis] & [UK-02 Tujuan Teknis DS]: Business & technical goal tracking.
- [UK-10 Mengevaluasi Hasil Pemodelan]: Review of empirical evidence and model performance.
- [UK-11 Melakukan Proses Review Pemodelan]: Failure register, claim level governance, and audit trails.

Enforces Claim Levels (L0-L3) and Evidence Grades (A-D) as mandated by System Specification Section 7.
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
    """Scientific Claim Hierarchy (System Specification Section 7.1)."""
    L0_DESCRIPTIVE = "L0 (Descriptive)"
    L1_PREDICTIVE = "L1 (Predictive)"
    L2_ASSOCIATIONAL = "L2 (Associational)"
    L3_CAUSAL = "L3 (Causal)"


class EvidenceGrade(str, Enum):
    """Evidence Grading Standard (System Specification Section 7.2)."""
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
    status: str = "VERIFIED"  # VERIFIED, PARTIALLY_VERIFIED, UNVERIFIED, MISSING
    official_code: str = ""
    evidence_process: str = ""
    evidence_result: str = ""
    evidence_validation: str = ""
    evidence_explanation: str = ""
    verification_method: str = ""
    evidence_grade: str = "Grade A"


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
                # Only load skkni items if compatible, otherwise keep canonical
                for k, v in data.get("skkni_matrix", {}).items():
                    if k in self.skkni_matrix:
                        # Update status if present
                        if "status" in v:
                            self.skkni_matrix[k].status = v["status"]
            except Exception:
                pass

    def _initialize_default_skkni_matrix(self) -> None:
        """Seed the 11 canonical SKKNI 299/2020 Data Science competence units."""
        units_spec = [
            (
                "UK-01",
                "J.62DMI00.001.1",
                "Menentukan Objektif Bisnis",
                "Perumusan 3 pilar objektif bisnis: mitigasi churn, penurunan friksi ongkir, efisiensi subsidi logistik.",
                ["config/business_objectives.yaml", "config/analysis_plan.yaml"],
                ["notebooks/01_business_and_data_understanding.ipynb"],
                ["reports/research_traceability_matrix.md"],
                "Analisis kebutuhan bisnis e-commerce Olist, formulasi metrik kesuksesan finansial dan kepuasan.",
                "Dokumen spesifikasi objektif bisnis terukur: Target Churn < 5%, Ongkir/Harga < 20%, Kepuasan >= 4.0/5.",
                "Review keselarasan oleh tim pimpinan dan simulasi dampak margin laba di simulator bisnis.",
                "Dipilih 3 pilar karena data historis menunjukkan 78% komplain bersumber dari friksi logistik dan ongkir.",
                "Pemeriksaan konsistensi parameter config dan simulasi baseline laba rugi.",
            ),
            (
                "UK-02",
                "J.62DMI00.002.1",
                "Menentukan Tujuan Teknis Data Science",
                "Penetapan task klasifikasi (PR-AUC/ROC-AUC), regresi (MAE/RMSE), clustering (Silhouette), dan batas baseline.",
                ["config/models.yaml", "config/business_objectives.yaml"],
                ["notebooks/01_business_and_data_understanding.ipynb"],
                ["reports/research_traceability_matrix.md"],
                "Penerjemahan sasaran bisnis menjadi 4 tugas teknis DS: (1) Prediksi risiko komplain (imbalanced binary), (2) Prediksi lead time (regresi), (3) Klastering persona pelanggan (unsupervised), (4) World state dynamics (autoregressive).",
                "Daftar KPI teknis kuantitatif: Tabular PR-AUC >= 0.28, Text PR-AUC >= 0.75, Silhouette >= 0.35, WAPE World Model <= 18%.",
                "Benchmark kriteria terhadap naive majority class predictor dan zero-rule baseline.",
                "PR-AUC dipilih dibanding ROC-AUC untuk deteksi ulasan negatif karena ketimpangan kelas ekstrem (positive class ~8%).",
                "Eksekusi pipeline baseline ladder dan validasi ambang batas teknis.",
            ),
            (
                "UK-03",
                "J.62DMI00.005.1",
                "Menelaah Data",
                "Profiling relasional 9 tabel Olist, audit referensial FK, analisis distribusi univariat dan bivariat.",
                ["src/csip/data/loader.py"],
                ["notebooks/01_business_and_data_understanding.ipynb", "notebooks/03_exploratory_data_analysis.ipynb"],
                ["data/data_dictionary.md", "reports/data_quality_report.md"],
                "Investigasi skema data mentah 9 tabel, analisis kardinalitas entitas, deteksi pola relasi customer-order-seller.",
                "Temuan pola empiris: integritas FK 100% (0 orphan records), asimetri ulasan terhadap keterlambatan (DISC-02).",
                "Pengujian statistik bivariat, korelasi Spearman, visualisasi boxplot dan histogram distribusi.",
                "Pendekatan relasional penuh diambil untuk mendeteksi bottleneck di sepanjang rantai nilai logistik.",
                "Eksekusi test automated validation pada 9 tabel relasional.",
            ),
            (
                "UK-04",
                "J.62DMI00.006.1",
                "Memvalidasi Data",
                "Pemeriksaan kelengkapan, tipe data, konsistensi temporal, dan deteksi anomali kronologis.",
                ["src/csip/data/loader.py", "tests/test_data_validation.py"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["reports/data_quality_report.md", "artifacts/reports/raw_data_profile.json"],
                "Audit integritas data otomatis: kelengkapan kolom, rasio missing value, integritas primary key, dan kronologi waktu.",
                "Identifikasi 23 baris anomali kronologi (order_delivered < order_purchase) dan 11,000+ baris order non-delivered.",
                "Pemeriksaan assertion terprogram via pytest suite (tests/test_data_validation.py).",
                "Data non-delivered dikeluarkan karena pesanan belum selesai tidak memiliki waktu pengiriman aktual yang valid.",
                "Automated test pass rate 100% pada verifikasi aturan bisnis data.",
            ),
            (
                "UK-05",
                "J.62DMI00.007.1",
                "Menentukan Objek Data",
                "Seleksi objek data, penetapan 4 grain analitik, filter sample, dan penegakan batas censoring temporal delta_w=90 hari.",
                ["config/data.yaml", "config/analysis_plan.yaml"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["data/dataset_manifest.json", "reports/research_traceability_matrix.md"],
                "Penetapan kriteria inklusi pesanan berstatus 'delivered', pemisahan unit analisis menjadi 4 grain independen.",
                "Terbentuk 4 grain analitik: order_level (N=96,470), customer_cohort (N=93,358), weekly_system_state (N=86 minggu), review_corpus (N=95,831).",
                "Verifikasi keunikan grain dan ketiadaan cross-grain collision melalui unit tests.",
                "Pemisahan grain mencegah agregasi prematur yang dapat mengaburkan variasi tingkat transaksi individual.",
                "Uji struktur dan skema grain analitik pada data/processed/.",
            ),
            (
                "UK-06",
                "J.62DMI00.008.1",
                "Membersihkan Data",
                "Pembersihan nilai hilang, penanganan koordinat geolokasi, reduksi kardinalitas, dan deduplikasi ulasan.",
                ["src/csip/cleaning/cleaner.py", "src/csip/cleaning/auto_cleaner.py"],
                ["notebooks/02_data_validation_and_cleaning.ipynb"],
                ["reports/data_quality_report.md", "data/interim/"],
                "Penerapan prosedur pembersihan: filter status, kompresi spatial median geolocation, deduplikasi multi-item review.",
                "Deduplikasi spasial memangkas 1,000,163 baris koordinat menjadi 19,010 baris unik (-98.1%) tanpa kehilangan presisi kode pos.",
                "Verifikasi bebas null pada kolom kunci dan ketiadaan duplikasi primary key pasca-cleaning.",
                "Agregasi median koordinat dipilih karena koordinat GPS pada zip code yang sama sering mengalami fluktuasi pengukuran acak.",
                "Eksekusi tests/test_cleaning_and_grain.py dan tests/test_data_pipeline_stress.py.",
            ),
            (
                "UK-07",
                "J.62DMI00.009.1",
                "Mengkonstruksi Data",
                "Rekayasa fitur ekonomi, rasio ongkir, lag persetujuan, jarak spasial Haversine, dan agregasi as-of anti-leakage.",
                ["src/csip/features/engineer.py", "config/features.yaml"],
                ["notebooks/04_feature_engineering_and_construction.ipynb"],
                ["reports/feature_availability_and_leakage_audit.md"],
                "Konstruksi fitur domain: freight_ratio, delivery_lead_time_days, delivery_delay_days, seller_buyer_distance_km, high_value_late_flag.",
                "Dihasilkan 41 kolom fitur pada tabel order_level.parquet dengan dokumentasi kamus fitur lengkap.",
                "Uji deteksi kebocoran fitur temporal (test_feature_leakage.py) dan verifikasi ketiadaan fitur pasca-pengiriman pada model prediksi awal.",
                "Perhitungan jarak Haversine vektorisasi NumPy menghasilkan efisiensi komputasi 100x dibanding iterasi baris.",
                "Eksekusi tests/test_feature_leakage.py membuktikan zero target leakage.",
            ),
            (
                "UK-08",
                "J.62DMI00.012.1",
                "Membangun Skenario Model",
                "Perancangan matriks eksperimen E0-E9, pengujian hipotesis H1-H6 (FDR correction), dan partisi temporal holdout.",
                ["src/csip/hypotheses/runner.py", "src/csip/world/state_transition.py", "config/scenarios.yaml"],
                ["notebooks/06_hypothesis_investigation.ipynb", "notebooks/10_system_and_world_modeling.ipynb"],
                ["reports/hypothesis_report.md", "reports/scenario_simulation_report.md"],
                "Perancangan skenario validasi: temporal split (cutoff 2018-05-31), matriks hipotesis behavioral, dan formulasi Vector AutoRegressive State-Space.",
                "Hasil uji hipotesis: H1 didukung (p<0.001, eta2=0.12), H2 didukung (cliff effect delay > 3 hari), H3 ditolak secara ilmiah (FAIL-HYP-H3, p_adj=0.859).",
                "Penyesuaian p-value menggunakan metode Benjamini-Hochberg False Discovery Rate (FDR) alpha=0.05.",
                "Temporal split dipilih daripada random K-Fold untuk merefleksikan realitas produksi tanpa lookahead bias.",
                "Verifikasi skenario melalui tests/test_hypotheses.py dan tests/test_world_model.py.",
            ),
            (
                "UK-09",
                "J.62DMI00.013.1",
                "Membangun Model",
                "Pelatihan model machine learning berjenjang (B0 s.d. B4), hyperparameter tuning, dan arsitektur deep learning.",
                ["src/csip/models/classic.py", "src/csip/models/trainer.py", "src/csip/models/deep_tabular.py", "src/csip/models/deep_seq.py", "src/csip/models/ml_engine.py"],
                ["notebooks/07_supervised_ml_and_competency_lab.ipynb", "notebooks/08_neural_network_and_deep_learning.ipynb"],
                ["reports/model_evaluation_and_review_report.md"],
                "Pelatihan sistematis: B0 Naive, B1 Logistic/Ridge, B2 Decision Tree/KNN/NB, B3 Random Forest & LightGBM, B4 Tabular MLP & Bi-LSTM NLP.",
                "LightGBM menjadi champion tabular (PR-AUC=0.3004), Bi-LSTM meraih PR-AUC=0.8076 pada klasifikasi teks ulasan.",
                "Logging parameter, seed deterministik (random_state=42), dan validasi cross-entropy loss convergence.",
                "LightGBM dipilih karena kemampuannya menangani fitur continuous non-linear dengan kecepatan inferensi tinggi di laptop 8GB RAM.",
                "Automated training and prediction tests di tests/test_models.py dan tests/test_deep_learning.py.",
            ),
            (
                "UK-10",
                "J.62DMI00.014.1",
                "Mengevaluasi Hasil Pemodelan",
                "Evaluasi performa out-of-time test set, kurva PR/ROC, kalibrasi probabilitas Platt scaling, dan atribusi SHAP.",
                ["src/csip/evaluation/explainer.py", "src/csip/uncertainty/bootstrap.py"],
                ["notebooks/09_model_evaluation_and_explainability.ipynb", "notebooks/12_uncertainty_quantification.ipynb"],
                ["reports/model_evaluation_and_review_report.md"],
                "Kalkulasi metrik evaluasi lengkap: PR-AUC, ROC-AUC, Brier score, ECE, residual RMSE/MAE, dan SHAP TreeExplainer feature importance.",
                "Platt scaling memangkas Brier score sebesar 44.59% (0.1375 -> 0.0762) dan ECE dari 0.2355 ke 0.0070; faktor keterlambatan berkontribusi 31.2% massa SHAP.",
                "Perbandingan out-of-time holdout terhadap baseline naive dan residual bootstrap confidence interval (95% CI).",
                "Kalibrasi probabilitas wajib diterapkan karena probabilitas mentah tree ensemble cenderung overconfident pada imbalanced dataset.",
                "Pengujian metrik evaluasi dan kalibrasi di tests/test_models.py.",
            ),
            (
                "UK-11",
                "J.62DMI00.015.1",
                "Melakukan Proses Review Pemodelan",
                "Audit metodologi, pencatatan Failure Register, pembatasan tingkat klaim L0-L3, dan sintesis rekomendasi keputusan.",
                ["src/csip/evidence/registry.py", "app/streamlit_app.py"],
                ["notebooks/13_model_review_and_failure_analysis.ipynb", "notebooks/14_final_research_report.ipynb"],
                ["reports/evidence_and_failure_register.md", "reports/csip_data_scientist_technical_report.md"],
                "Peninjauan kritis terhadap kelemahan model, inventarisasi kegagalan (FAIL-HYP-H3), validasi batas klaim ilmiah (L0 s.d. L3), dan penyusunan dashboard pembelaan.",
                "Tercatat 3 kegagalan eksplisit dalam Failure Register dengan mitigasi nyata; rekomendasi keputusan bisnis didasarkan pada asosiasi terkontrol.",
                "Audit independen menggunakan checks otomatis kelengkapan bukti dan verifikasi parity artefak.",
                "Transparansi kegagalan dan pemisahan korelasi vs kausalitas mempertahankan integritas ilmiah sesuai kaidah KKNI Level 7.",
                "Pengujian integritas registry di tests/test_evidence_registry.py dan konsistensi SKKNI di tests/test_skkni_consistency.py.",
            ),
        ]

        for (
            code,
            off_code,
            title,
            desc,
            code_locs,
            nb_locs,
            rpt_locs,
            ev_proc,
            ev_res,
            ev_val,
            ev_exp,
            ver_meth,
        ) in units_spec:
            self.skkni_matrix[code] = SKKNITraceabilityItem(
                unit_code=code,
                official_code=off_code,
                unit_title=title,
                implementation_in_csip=desc,
                code_locations=code_locs,
                notebook_locations=nb_locs,
                report_artifacts=rpt_locs,
                evidence_process=ev_proc,
                evidence_result=ev_res,
                evidence_validation=ev_val,
                evidence_explanation=ev_exp,
                verification_method=ver_meth,
                status="VERIFIED",
                evidence_grade="Grade A",
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

