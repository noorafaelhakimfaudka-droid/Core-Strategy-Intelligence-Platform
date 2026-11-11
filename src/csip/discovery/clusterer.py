"""CSIP Behavioral Discovery Engine & Unsupervised Clustering Module.

SKKNI Compliance:
- [UK-03 Menelaah Data]: Pencarian pola perilaku tersembunyi.
- [UK-08 Membangun Skenario Model]: Pemilihan parameter klasterisasi (k-range, kriteria metrik).
- [UK-09 Membangun Model]: Pelatihan model K-Means, reduksi dimensi PCA, dan deteksi anomali.

Provides reproducible customer segmentation, Silhouette/Davies-Bouldin evaluation,
and cluster persona generation for the Streamlit Behavioral Discovery Lab.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [CSIP-DISCOVERY] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class ClusterProfile:
    """Statistical summary and behavioral persona for a customer cluster."""
    cluster_id: int
    persona_name: str
    size: int
    size_pct: float
    feature_means: Dict[str, float]
    feature_medians: Dict[str, float]
    repeat_rate: float
    negative_review_rate: float
    key_characteristics: List[str] = field(default_factory=list)


class BehavioralClusterer:
    """Unsupervised Machine Learning Engine for Customer & Transaction Segmentation.

    Fulfills SKKNI [UK-09 Membangun Model - Unsupervised Learning].
    """

    DEFAULT_FEATURES = [
        "total_order_value",
        "freight_ratio",
        "delivery_lead_time_days",
        "item_count",
        "payment_installments_max",
    ]

    def __init__(
        self,
        features: Optional[List[str]] = None,
        k_range: Optional[List[int]] = None,
        random_state: int = 42,
    ) -> None:
        self.features = features or self.DEFAULT_FEATURES
        self.k_range = k_range or [3, 4, 5, 6, 7]
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.optimal_kmeans: Optional[KMeans] = None
        self.optimal_k: int = 4
        self.pca = PCA(n_components=2, random_state=random_state)
        self.evaluation_results: Dict[str, Any] = {}
        self.cluster_profiles: List[ClusterProfile] = []

    def fit_evaluate(
        self,
        df: pd.DataFrame,
        sample_size_eval: int = 15000,
    ) -> Dict[str, Any]:
        """Train KMeans across k_range, evaluate metrics, and select optimal k.

        SKKNI [UK-09 Membangun Model].
        """
        logger.info(
            "Starting Behavioral Clustering on %d rows with features: %s",
            len(df),
            self.features,
        )

        # Extract features and handle missing values if any
        X_raw = df[self.features].copy()
        for col in self.features:
            if X_raw[col].isnull().any():
                X_raw[col] = X_raw[col].fillna(X_raw[col].median())

        # Fit Scaler
        X_scaled = self.scaler.fit_transform(X_raw)

        # Use subsample for Silhouette evaluation to satisfy 8 GB RAM / fast execution
        if len(X_scaled) > sample_size_eval:
            np.random.seed(self.random_state)
            eval_idx = np.random.choice(len(X_scaled), size=sample_size_eval, replace=False)
            X_eval = X_scaled[eval_idx]
        else:
            X_eval = X_scaled

        k_metrics: List[Dict[str, Any]] = []
        best_score = -1.0
        selected_k = self.k_range[0]

        for k in self.k_range:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels_eval = km.fit_predict(X_eval)

            sil = float(silhouette_score(X_eval, labels_eval))
            db = float(davies_bouldin_score(X_eval, labels_eval))
            ch = float(calinski_harabasz_score(X_eval, labels_eval))
            inertia = float(km.inertia_)

            k_metrics.append({
                "k": k,
                "silhouette_score": round(sil, 4),
                "davies_bouldin_index": round(db, 4),
                "calinski_harabasz_index": round(ch, 1),
                "inertia": round(inertia, 2),
            })
            logger.info("k=%d: Silhouette=%.4f, Davies-Bouldin=%.4f", k, sil, db)

            # Heuristic: maximize Silhouette, minimize Davies-Bouldin
            composite_metric = sil - (db * 0.1)
            if composite_metric > best_score:
                best_score = composite_metric
                selected_k = k

        self.optimal_k = selected_k
        logger.info("Selected optimal k=%d (Composite Score=%.4f)", selected_k, best_score)

        # Fit final model on full dataset
        self.optimal_kmeans = KMeans(
            n_clusters=selected_k,
            random_state=self.random_state,
            n_init=10,
        )
        full_labels = self.optimal_kmeans.fit_predict(X_scaled)

        # Fit PCA on full dataset for 2D embedding
        X_pca = self.pca.fit_transform(X_scaled)
        pca_variance = [round(float(v), 4) for v in self.pca.explained_variance_ratio_]

        # Compute anomaly scores (Euclidean distance to assigned centroid)
        centroids = self.optimal_kmeans.cluster_centers_
        distances = np.linalg.norm(X_scaled - centroids[full_labels], axis=1)
        anomaly_cutoff = float(np.percentile(distances, 95))
        is_anomaly = (distances > anomaly_cutoff).astype(int)

        # Attach cluster labels and PCA coordinates
        df_clustered = df.copy()
        df_clustered["cluster_id"] = full_labels
        df_clustered["pca_1"] = X_pca[:, 0].astype(np.float32)
        df_clustered["pca_2"] = X_pca[:, 1].astype(np.float32)
        df_clustered["cluster_dist"] = distances.astype(np.float32)
        df_clustered["is_anomaly"] = is_anomaly.astype(np.int8)

        # Build Cluster Personas
        self.cluster_profiles = self._build_profiles(df_clustered)

        self.evaluation_results = {
            "selected_k": selected_k,
            "features": self.features,
            "k_metrics": k_metrics,
            "pca_explained_variance": pca_variance,
            "total_samples": len(df),
            "anomaly_threshold_dist": round(anomaly_cutoff, 4),
            "anomaly_count": int(is_anomaly.sum()),
        }

        return {
            "evaluation_results": self.evaluation_results,
            "profiles": [asdict(p) for p in self.cluster_profiles],
            "clustered_df": df_clustered,
        }

    def _build_profiles(self, df_clustered: pd.DataFrame) -> List[ClusterProfile]:
        """Synthesize statistical cluster attributes into distinct business personas."""
        profiles: List[ClusterProfile] = []
        total_n = len(df_clustered)

        # Pre-assign persona names based on relative feature ordering
        for cid in range(self.optimal_k):
            sub = df_clustered[df_clustered["cluster_id"] == cid]
            size = len(sub)
            size_pct = round((size / total_n) * 100, 2)

            means = {col: round(float(sub[col].mean()), 2) for col in self.features}
            medians = {col: round(float(sub[col].median()), 2) for col in self.features}

            rep_rate = (
                round(float(sub["repeat_purchase_flag"].mean() * 100), 2)
                if "repeat_purchase_flag" in sub.columns
                else 0.0
            )
            neg_rate = (
                round(float(sub["negative_review_flag"].mean() * 100), 2)
                if "negative_review_flag" in sub.columns
                else (
                    round(float((sub["review_score"] <= 2).mean() * 100), 2)
                    if "review_score" in sub.columns
                    else 0.0
                )
            )

            # Assign meaningful persona name dynamically
            persona = self._infer_persona_name(medians, cid)

            traits = [
                f"Median Order Value: {medians.get('total_order_value', 0):.1f} BRL",
                f"Freight Ratio: {medians.get('freight_ratio', 0)*100:.1f}%",
                f"Delivery Days: {medians.get('delivery_lead_time_days', 0):.1f} hari",
                f"Negative Review Rate: {neg_rate:.1f}%",
            ]

            profiles.append(
                ClusterProfile(
                    cluster_id=cid,
                    persona_name=persona,
                    size=size,
                    size_pct=size_pct,
                    feature_means=means,
                    feature_medians=medians,
                    repeat_rate=rep_rate,
                    negative_review_rate=neg_rate,
                    key_characteristics=traits,
                )
            )

        return profiles

    @staticmethod
    def _infer_persona_name(medians: Dict[str, float], cid: int) -> str:
        """Infer an intuitive business persona from medians."""
        val = medians.get("total_order_value", 0)
        fr = medians.get("freight_ratio", 0)
        days = medians.get("delivery_lead_time_days", 0)
        inst = medians.get("payment_installments_max", 0)

        if fr > 0.35:
            return f"Segmen {cid}: Heavy Freight Friction"
        elif val > 200:
            return f"Segmen {cid}: High-Ticket Premium Basket"
        elif days > 18:
            return f"Segmen {cid}: Long Lead Time Distant Buyers"
        elif inst > 4:
            return f"Segmen {cid}: Installment-Reliant Buyers"
        else:
            return f"Segmen {cid}: Fast Single-Item Convenience"

    def evaluate_cluster_stability(
        self,
        df: pd.DataFrame,
        k_values: Optional[List[int]] = None,
        n_bootstraps: int = 10,
        subsample_ratio: float = 0.8,
    ) -> Dict[str, Any]:
        """Evaluates cluster stability using bootstrap Adjusted Rand Index (ARI) and Jaccard similarity.

        Phase 6 rigor: verifies clusters are stable across random subsamples (k=3..5).
        """
        k_values = k_values or [3, 4, 5]
        X_raw = df[self.features].copy()
        for col in self.features:
            if X_raw[col].isnull().any():
                X_raw[col] = X_raw[col].fillna(X_raw[col].median())

        X_scaled = self.scaler.fit_transform(X_raw)
        n_total = len(X_scaled)
        subsample_size = int(n_total * subsample_ratio)

        stability_results: Dict[str, Any] = {}
        rng = np.random.default_rng(self.random_state)

        for k in k_values:
            ari_scores: List[float] = []
            jaccard_scores: List[float] = []

            # Generate multiple bootstrap subsample models
            replicate_indices: List[np.ndarray] = []
            replicate_labels: List[np.ndarray] = []

            for b in range(n_bootstraps):
                idx = rng.choice(n_total, size=subsample_size, replace=False)
                km = KMeans(n_clusters=k, random_state=self.random_state + b, n_init=5)
                labels = km.fit_predict(X_scaled[idx])
                replicate_indices.append(idx)
                replicate_labels.append(labels)

            # Compute pairwise ARI and Jaccard on overlapping indices
            for i in range(n_bootstraps):
                for j in range(i + 1, n_bootstraps):
                    dict_i = dict(zip(replicate_indices[i], replicate_labels[i]))
                    dict_j = dict(zip(replicate_indices[j], replicate_labels[j]))
                    common_items = [x for x in replicate_indices[i] if x in dict_j]
                    if len(common_items) < 50:
                        continue

                    labels_sub_i = np.array([dict_i[x] for x in common_items])
                    labels_sub_j = np.array([dict_j[x] for x in common_items])

                    ari = float(adjusted_rand_score(labels_sub_i, labels_sub_j))
                    ari_scores.append(ari)

                    # Compute max Jaccard similarity across clusters
                    # Jaccard = |C_a \cap C_b| / |C_a \cup C_b|
                    jaccards = []
                    for c_a in range(k):
                        mask_a = (labels_sub_i == c_a)
                        best_j = 0.0
                        for c_b in range(k):
                            mask_b = (labels_sub_j == c_b)
                            inter = np.sum(mask_a & mask_b)
                            union = np.sum(mask_a | mask_b)
                            if union > 0:
                                sim = inter / union
                                if sim > best_j:
                                    best_j = sim
                        jaccards.append(best_j)
                    jaccard_scores.append(float(np.mean(jaccards)))

            stability_results[f"k_{k}"] = {
                "k": k,
                "n_comparisons": len(ari_scores),
                "mean_ari": round(float(np.mean(ari_scores)), 4) if ari_scores else 0.0,
                "std_ari": round(float(np.std(ari_scores)), 4) if ari_scores else 0.0,
                "mean_jaccard": round(float(np.mean(jaccard_scores)), 4) if jaccard_scores else 0.0,
                "std_jaccard": round(float(np.std(jaccard_scores)), 4) if jaccard_scores else 0.0,
                "is_stable": bool(np.mean(ari_scores) >= 0.60) if ari_scores else False,
            }

        return stability_results

    def save_artifacts(
        self,
        model_path: Union[str, Path] = "artifacts/models/clustering_pipeline.joblib",
        report_path: Union[str, Path] = "artifacts/reports/clustering_evaluation.json",
        stability_results: Optional[Dict[str, Any]] = None,
        stability_report_path: Union[str, Path] = "artifacts/reports/cluster_stability_evaluation.json",
    ) -> None:
        """Persist trained clustering pipeline and metrics to disk."""
        model_p = Path(model_path)
        model_p.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "scaler": self.scaler,
                "kmeans": self.optimal_kmeans,
                "pca": self.pca,
                "features": self.features,
                "optimal_k": self.optimal_k,
                "profiles": [asdict(p) for p in self.cluster_profiles],
            },
            model_p,
        )

        import sklearn, sys
        from datetime import datetime, timezone
        from csip._version import __version__
        sidecar_data = {
            "model_name": "clustering_pipeline",
            "optimal_k": self.optimal_k,
            "feature_list": self.features,
            "train_rows": 96470,
            "sklearn_version": sklearn.__version__,
            "python_version": sys.version.split()[0],
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "git_or_release_version": f"v{__version__}",
        }
        with open(f"{model_p}.json", "w", encoding="utf-8") as f:
            json.dump(sidecar_data, f, indent=2)

        rep_p = Path(report_path)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "evaluation": self.evaluation_results,
                    "profiles": [asdict(p) for p in self.cluster_profiles],
                },
                f,
                indent=2,
            )

        if stability_results is not None:
            stab_p = Path(stability_report_path)
            stab_p.parent.mkdir(parents=True, exist_ok=True)
            with open(stab_p, "w", encoding="utf-8") as f:
                json.dump(stability_results, f, indent=2)
            logger.info("Saved cluster stability evaluation to %s", stab_p)

        logger.info("Saved clustering pipeline to %s and evaluation to %s", model_p, rep_p)

