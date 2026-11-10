"""Generate Notebooks 08 and 09 for Milestone 8."""

import json
from pathlib import Path


def create_notebook_08():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# CSIP Module 08: Deep Learning & Neural Network Benchmarks\n",
                    "**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**\n",
                    "\n",
                    "### SKKNI Data Science Competency Standards\n",
                    "- **[UK-09 Membangun Model]**: Penerapan arsitektur Deep Learning (Tabular MLP dengan Entity Embeddings dan NLP Text Bi-LSTM).\n",
                    "- **Modul 14 & 15**: Multi-Layer Perceptron (MLP), Batch Normalization, Dropout, Word Embeddings, Bidirectional LSTM.\n",
                    "\n",
                    "---"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "from pathlib import Path\n",
                    "\n",
                    "# Set repo root\n",
                    "REPO_ROOT = Path('.').resolve().parent if Path('.').resolve().name == 'notebooks' else Path('.').resolve()\n",
                    "sys.path.insert(0, str(REPO_ROOT / 'src'))\n",
                    "\n",
                    "import json\n",
                    "import torch\n",
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "from csip.models.deep_tabular import TabularMLPClassifier, TabularEmbeddingMLP\n",
                    "from csip.models.deep_seq import TextBiLSTMClassifier\n",
                    "\n",
                    "print(f'PyTorch Version: {torch.__version__}')\n",
                    "print(f'Device available: cpu (Threads: {torch.get_num_threads()})')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Load ML Leaderboard & Deep Learning Metrics\n",
                    "We inspect the comparative performance of Deep Learning models (B4) against the Classical ML Baselines (B0–B3)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "leaderboard_path = REPO_ROOT / 'artifacts' / 'reports' / 'ml_leaderboard.json'\n",
                    "with open(leaderboard_path, 'r') as f:\n",
                    "    leaderboard = json.load(f)\n",
                    "\n",
                    "ldf = pd.DataFrame(leaderboard)\n",
                    "review_models = ldf[ldf['target'] == 'negative_review_flag'].drop_duplicates(subset=['model_name'])\n",
                    "display(review_models[['model_name', 'baseline_tier', 'test_pr_auc', 'test_roc_auc', 'test_f1', 'test_brier']])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Tabular MLP vs Classical Gradient Boosting\n",
                    "- **Finding**: LightGBM achieves PR-AUC = 0.3004, while Tabular MLP with Entity Embeddings achieves PR-AUC = 0.2875.\n",
                    "- **Empirical Insight**: Gradient boosted trees continue to dominate tabular structured data with heterogeneous numerical and categorical distributions on moderate sample sizes (~70k), while Deep Learning demonstrates solid competitive performance with continuous embeddings."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Inspect Tabular MLP Saved Checkpoint\n",
                    "mlp_ckpt = torch.load(REPO_ROOT / 'artifacts' / 'models' / 'tabular_mlp_negative_review.pt', weights_only=False)\n",
                    "print('Tabular MLP Architecture Summary:')\n",
                    "print(f\"- Continuous features: {mlp_ckpt['num_continuous']}\")\n",
                    "print(f\"- Embedding sizes: {mlp_ckpt['embedding_sizes']}\")\n",
                    "print(f\"- Hidden dimensions: {mlp_ckpt['hidden_dims']}\")\n",
                    "\n",
                    "plt.figure(figsize=(7, 4), dpi=100)\n",
                    "plt.plot(range(1, len(mlp_ckpt['loss_history']) + 1), mlp_ckpt['loss_history'], 'o-', color='#3498db')\n",
                    "plt.xlabel('Epoch')\n",
                    "plt.ylabel('BCE Loss')\n",
                    "plt.title('Tabular MLP Training Loss Convergence')\n",
                    "plt.grid(True, linestyle=':', alpha=0.6)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Sequence Modeling with Text Bi-LSTM\n",
                    "For natural language text in Portuguese review comments, sequence models process lexical semantics."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "bilstm_ckpt = torch.load(REPO_ROOT / 'artifacts' / 'models' / 'text_bilstm_review_sentiment.pt', weights_only=False)\n",
                    "print('Text Bi-LSTM Architecture Summary:')\n",
                    "print(f\"- Vocab size: {len(bilstm_ckpt['word2idx'])}\")\n",
                    "print(f\"- Max sequence length: {bilstm_ckpt['max_seq_len']}\")\n",
                    "print(f\"- Embedding dimension: {bilstm_ckpt['embedding_dim']}\")\n",
                    "print(f\"- Hidden dimension: {bilstm_ckpt['hidden_dim']}\")\n",
                    "\n",
                    "plt.figure(figsize=(7, 4), dpi=100)\n",
                    "plt.plot(range(1, len(bilstm_ckpt['loss_history']) + 1), bilstm_ckpt['loss_history'], 's-', color='#e74c3c')\n",
                    "plt.xlabel('Epoch')\n",
                    "plt.ylabel('BCE Loss')\n",
                    "plt.title('Text Bi-LSTM Training Loss Convergence')\n",
                    "plt.grid(True, linestyle=':', alpha=0.6)\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.14.7"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    out_file = Path("notebooks/08_neural_network_and_deep_learning.ipynb")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {out_file}")


def create_notebook_09():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# CSIP Module 09: Model Evaluation & Explainability (SHAP & Calibration)\n",
                    "**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**\n",
                    "\n",
                    "### SKKNI Data Science Competency Standards\n",
                    "- **[UK-10 Mengevaluasi Hasil Pemodelan]**: Evaluasi diagnostik performa, kalibrasi probabilitas out-of-time (Brier score & ECE), dan atribusi fitur berbasis SHAP.\n",
                    "- **Modul 16**: Interpretable ML, SHAP TreeExplainer, dan Reliability Diagrams.\n",
                    "\n",
                    "### Claim Governance\n",
                    "- **SHAP attributions** represent Level L1 (Predictive) / L2 (Associational) evidence.\n",
                    "- They describe model feature reliance, NOT Level L3 Causal mechanisms.\n",
                    "\n",
                    "---"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "from pathlib import Path\n",
                    "\n",
                    "REPO_ROOT = Path('.').resolve().parent if Path('.').resolve().name == 'notebooks' else Path('.').resolve()\n",
                    "sys.path.insert(0, str(REPO_ROOT / 'src'))\n",
                    "\n",
                    "import json\n",
                    "import pandas as pd\n",
                    "from IPython.display import Image, display\n",
                    "\n",
                    "# Load Explainability Report\n",
                    "report_path = REPO_ROOT / 'artifacts' / 'reports' / 'model_explainability.json'\n",
                    "with open(report_path, 'r') as f:\n",
                    "    report = json.load(f)\n",
                    "\n",
                    "print(f\"Target: {report['target']}\")\n",
                    "print(f\"Champion Model: {report['champion_model']}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Global Feature Attribution (SHAP TreeExplainer)\n",
                    "We inspect the top features driving negative review risk according to mean absolute SHAP values."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "shap_df = pd.DataFrame(report['shap_attribution']['top_features'])\n",
                    "display(shap_df.head(10))\n",
                    "\n",
                    "display(Image(filename=str(REPO_ROOT / 'artifacts' / 'reports' / 'figures' / 'shap_summary_plot.png')))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Probability Calibration & Reliability Diagram\n",
                    "Under severe class imbalance, predicted probabilities are often uncalibrated.\n",
                    "We inspect the out-of-time test set calibration before and after Platt scaling."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "calib = report['calibration']\n",
                    "print('Calibration Metrics (Locked Out-of-Time Test Split):')\n",
                    "print(f\"- Raw Brier Score: {calib['uncalibrated_brier']:.4f}\")\n",
                    "print(f\"- Calibrated Brier Score: {calib['calibrated_brier']:.4f} (Improvement: {calib['brier_improvement_pct']:.2f}%)\")\n",
                    "print(f\"- Raw ECE: {calib['uncalibrated_ece']:.4f}\")\n",
                    "print(f\"- Calibrated ECE: {calib['calibrated_ece']:.4f}\")\n",
                    "\n",
                    "display(Image(filename=str(REPO_ROOT / 'artifacts' / 'reports' / 'figures' / 'calibration_curves.png')))"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.14.7"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    out_file = Path("notebooks/09_model_evaluation_and_explainability.ipynb")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {out_file}")


if __name__ == "__main__":
    create_notebook_08()
    create_notebook_09()
