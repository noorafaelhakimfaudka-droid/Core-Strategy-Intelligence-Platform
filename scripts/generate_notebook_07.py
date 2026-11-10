"""Generate Notebook 07: Supervised Machine Learning & Competency Laboratory [SKKNI Unit 8 & 9]."""

from pathlib import Path
import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def create_notebook_07():
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
        nbf.v4.new_markdown_cell("""# NOTEBOOK 07: SUPERVISED MACHINE LEARNING & COMPETENCY LAB (B0 — B3)
## Computational Society Intelligence Platform (CSIP) — Modul MVP: BDI
**Kepatuhan SKKNI**:
- `[UK-08 Membangun Skenario Model]` (Skenario E0-E6 & Baseline Ladder B0-B3)
- `[UK-09 Membangun Model]` (Supervised Learning: Regresi, Klasifikasi, Tree, KNN, Naive Bayes, LightGBM)
- `[UK-10 Mengevaluasi Hasil Pemodelan]` (Evaluasi PR-AUC, ROC-AUC, Brier Score, & MAE/RMSE)

---

### 1. Desain Eksperimen & Baseline Ladder (B0 — B3)
Setiap tugas pemodelan diuji melalui tangga pembanding model (*Baseline Ladder*) untuk membuktikan bahwa kompleksitas model benar-benar terjustifikasi:
- **B0 — Naive Baseline**: Majority Class Classifier & Mean Regressor.
- **B1 — Statistical Baseline**: Logistic Regression (balanced) & Ridge Regression.
- **B2 — Classical Benchmarks (Competency Lab)**: Decision Tree, K-Nearest Neighbors (KNN), Gaussian Naive Bayes.
- **B3 — Ensemble Trees**: Random Forest & LightGBM.
- **Evaluasi Temporal**: Model dilatih pada data historis awal (s/d Maret 2018), divalidasi pada kuartal 2 (April–Juni 2018), dan diuji pada *Locked Holdout Test Set* (Juli–Agustus 2018).
"""),
        nbf.v4.new_code_cell("""import sys
from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Load Leaderboard Hasil Pelatihan Model
with open(PROJECT_ROOT / "artifacts" / "reports" / "ml_leaderboard.json", "r") as f:
    leaderboard_data = json.load(f)

leaderboard_df = pd.DataFrame(leaderboard_data)
print(f"Total Eksperimen Terlatih: {len(leaderboard_df)} skenario")
"""),
        nbf.v4.new_markdown_cell("""### 2. Papan Peringkat Klasifikasi: Risiko Ulasan Negatif (`negative_review_flag`)
Menampilkan performa model B0 s/d B3 pada data uji terkunci (*Locked Temporal Test Set*).
"""),
        nbf.v4.new_code_cell("""test_reviews = leaderboard_df[
    (leaderboard_df["target_name"] == "negative_review_flag") &
    (leaderboard_df["split_name"] == "test")
].sort_values(by="pr_auc", ascending=False).reset_index(drop=True)

display(test_reviews[["model_name", "pr_auc", "roc_auc", "f1_score", "brier_score", "balanced_accuracy"]])
"""),
        nbf.v4.new_markdown_cell("""### 3. Visualisasi Kurva Komparasi PR-AUC (Baseline Ladder B0 — B3)
Menampilkan visualisasi perbandingan PR-AUC untuk membuktikan bahwa model ensemble B3 (LightGBM/RF) secara meyakinkan mengungguli Naive (B0) dan Klasik (B2).
"""),
        nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
bars = ax.barh(
    test_reviews["model_name"],
    test_reviews["pr_auc"],
    color=["#1f77b4" if "B3" in m else "#aec7e8" for m in test_reviews["model_name"]],
    edgecolor="black",
    alpha=0.85
)

ax.set_title("Komparasi Model Klasifikasi: PR-AUC pada Locked Test Split", fontsize=13, fontweight="bold")
ax.set_xlabel("PR-AUC", fontsize=11)
ax.grid(axis="x", linestyle=":", alpha=0.6)
ax.invert_yaxis()

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.005, bar.get_y() + bar.get_height() / 2, f"{w:.4f}", va="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.show()
"""),
        nbf.v4.new_markdown_cell("""### 4. Papan Peringkat Klasifikasi: Pembelian Ulang (`repeat_purchase_flag`)
Menelaah kemampuan model memprediksi pembelian ulang dalam jendela 90 hari berbasis Transaksi Pertama (First-Order Isolation).
"""),
        nbf.v4.new_code_cell("""repeat_models = leaderboard_df[
    (leaderboard_df["target_name"] == "repeat_purchase_flag")
].sort_values(by="pr_auc", ascending=False).reset_index(drop=True)

display(repeat_models[["model_name", "split_name", "pr_auc", "roc_auc", "f1_score", "brier_score"]])
"""),
        nbf.v4.new_markdown_cell("""### 5. Papan Peringkat Regresi: Estimasi Keterlambatan Pengiriman (`delivery_delay_days`)
Menelaah penurunan Mean Absolute Error (MAE) dan RMSE pada model estimasi durasi keterlambatan logistik.
"""),
        nbf.v4.new_code_cell("""reg_models = leaderboard_df[
    (leaderboard_df["target_name"] == "delivery_delay_days")
].sort_values(by="mae", ascending=True).reset_index(drop=True)

display(reg_models[["model_name", "split_name", "mae", "rmse", "r2"]])
"""),
        nbf.v4.new_markdown_cell("""### 6. Kesimpulan & Status Validation Gate G6 (Bagian Supervised ML)
1. **LightGBM (B3) Menjadi Juara (Champion Model)**:
   - Mencapai $PR\text{-}AUC$ tertinggi pada deteksi ulasan buruk dan penurunan $MAE$ signifikan pada regresi keterlambatan.
2. **Competency Lab Terpenuhi Lengkap**:
   - Algoritma Decision Tree, KNN, dan Gaussian Naive Bayes berhasil dilatih dan dievaluasi secara adil pada matriks data terstandarisasi.
3. Seluruh pipeline model terlatih telah tersimpan di `artifacts/models/` dan siap diakses antarmuka Streamlit Halaman 5.
""")
    ]

    nb.cells = cells
    out_path = NOTEBOOKS_DIR / "07_supervised_ml_and_competency_lab.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    create_notebook_07()

