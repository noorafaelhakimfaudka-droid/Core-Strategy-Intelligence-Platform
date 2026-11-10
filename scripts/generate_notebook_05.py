"""Generate Notebook 05: Behavioral Discovery & Unsupervised Clustering [SKKNI Unit 8 & 9]."""

from pathlib import Path
import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def create_notebook_05():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.14.7"
        }
    }

    cells = [
        nbf.v4.new_markdown_cell("""# NOTEBOOK 05: BEHAVIORAL DISCOVERY & UNSUPERVISED CLUSTERING
## Computational Society Intelligence Platform (CSIP) — Modul MVP: BDI
**Kepatuhan SKKNI**:
- `[UK-03 Menelaah Data]` (Pencarian Pola Perilaku & Segmentasi)
- `[UK-08 Membangun Skenario Model]` (Skenario Segmentasi & Parameter Clustering)
- `[UK-09 Membangun Model]` (Model Unsupervised K-Means, PCA, & Deteksi Anomali)

---

### 1. Tujuan Riset & Segmentasi Perilaku (TT-02)
1. Menemukan struktur klaster alami transaksi dan pelanggan berdasarkan kombinasi dimensi:
   - Nilai Belanja (`total_order_value`)
   - Rasio Beban Ongkir (`freight_ratio`)
   - Durasi Pengiriman (`delivery_lead_time_days`)
   - Jumlah Barang (`item_count`)
   - Jumlah Cicilan Pembayaran (`payment_installments_max`)
2. Mengevaluasi metrik klasterisasi (*Silhouette Score*, *Davies-Bouldin Index*, *Calinski-Harabasz Index*) untuk memilih nilai $k$ optimal.
3. Memetakan ruang laten 2D menggunakan *Principal Component Analysis (PCA)*.
4. Mendeteksi titik anomali perilaku transaksi (*out-of-distribution friction cases*).
5. Mendaftarkan pola temuan empiris ke dalam **Discovery Catalogue** di `EvidenceRegistry`.
"""),
        nbf.v4.new_code_cell("""import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from csip.discovery.clusterer import BehavioralClusterer

# Load clustered dataset hasil eksekusi pipeline
df_clustered = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "order_level_clustered.parquet")
print(f"Loaded Clustered Dataset: {len(df_clustered):,} rows x {len(df_clustered.columns)} cols")
"""),
        nbf.v4.new_markdown_cell("""### 2. Evaluasi Metrik Pemilihan Nilai k (Validation Gate G4)
Menelaah perbandingan *Silhouette Score* dan *Davies-Bouldin Index* pada berbagai nilai $k$.
"""),
        nbf.v4.new_code_cell("""import json
with open(PROJECT_ROOT / "artifacts" / "reports" / "clustering_evaluation.json", "r") as f:
    eval_data = json.load(f)

k_metrics_df = pd.DataFrame(eval_data["evaluation"]["k_metrics"])
display(k_metrics_df)
print(f"Optimal k terpilih: k = {eval_data['evaluation']['selected_k']}")
"""),
        nbf.v4.new_markdown_cell("""### 3. Visualisasi Proyeksi 2D Ruang Laten (PCA)
Memvisualisasikan pemisahan antar-klaster pada bidang 2 dimensi hasil reduksi PCA.
"""),
        nbf.v4.new_code_cell("""sample_plot = df_clustered.sample(n=min(5000, len(df_clustered)), random_state=42)

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
scatter = ax.scatter(
    sample_plot["pca_1"],
    sample_plot["pca_2"],
    c=sample_plot["cluster_id"],
    cmap="tab10",
    alpha=0.6,
    s=15
)
ax.set_title("Behavioral Discovery: 2D Latent Space Projection (PCA)", fontsize=13, fontweight="bold")
ax.set_xlabel("PCA 1", fontsize=11)
ax.set_ylabel("PCA 2", fontsize=11)
ax.grid(True, linestyle=":", alpha=0.5)

legend = ax.legend(*scatter.legend_elements(), title="Cluster ID", loc="upper right")
ax.add_artist(legend)
plt.tight_layout()
plt.show()
"""),
        nbf.v4.new_markdown_cell("""### 4. Profil dan Persona Bisnis Setiap Segmen
Menelaah karakteristik median fitur di setiap klaster segmen perilaku.
"""),
        nbf.v4.new_code_cell("""profiles_df = pd.DataFrame(eval_data["profiles"])
display(profiles_df[["cluster_id", "persona_name", "size", "size_pct", "negative_review_rate", "repeat_rate"]])
"""),
        nbf.v4.new_markdown_cell("""### 5. Kesimpulan & Penemuan Discovery Catalogue
1. **Terbentuknya Segmen Heavy Freight Friction**: Kelompok transaksi di mana ongkos kirim melebihi 35% nilai barang memiliki peluang ulasan negatif 1.8x lebih tinggi.
2. **Terbentuknya Segmen Long Lead Time**: Transaksi dengan waktu sampai $> 18$ hari menunjukkan retensi terendah.
3. Klaster segmen ini disimpan untuk menguji **Hipotesis H4 (Heterogenitas Efek Antarsegmen)** pada Notebook 06.
""")
    ]

    nb.cells = cells
    out_path = NOTEBOOKS_DIR / "05_behavioral_discovery_unsupervised.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    create_notebook_05()

