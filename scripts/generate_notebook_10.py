"""Generate Notebook 10 for Milestone 9 (System & World Model)."""

import json
from pathlib import Path


def create_notebook_10():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# CSIP Module 10: System Dynamics & World Model State Transition\n",
                    "**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**\n",
                    "\n",
                    "### SKKNI Data Science Competency Standards\n",
                    "- **[UK-08 Membangun Skenario Model]**: Perumusan model dinamika sistem state-space dan pengujian skenario intervensi.\n",
                    "- **[UK-09 Membangun Model]**: Estimasi parameter Vector AutoRegressive State Transition Matrix $\\Phi$.\n",
                    "- **[UK-10 Mengevaluasi Hasil Pemodelan]**: Uji Identifiabilitas Struktural (Synthetic Parameter Recovery) dan Historical Replay Backtest.\n",
                    "\n",
                    "### Mathematical Formulation\n",
                    "$$\\mathbf{S}_{t+1} = \\mathbf{C} + \\mathbf{\\Phi} \\mathbf{S}_t + \\mathbf{\\Gamma} \\mathbf{A}_t + \\boldsymbol{\\epsilon}_t$$\n",
                    "where:\n",
                    "- $\\mathbf{S}_t \\in \\mathbb{R}^4$: State vector `[weekly_order_volume, mean_delivery_delay, mean_freight_ratio, negative_review_rate]`\n",
                    "- $\\mathbf{A}_t$: Action / policy intervention vector\n",
                    "- $\\boldsymbol{\\epsilon}_t \\sim \\mathcal{N}(\\mathbf{0}, \\mathbf{\\Sigma})$: Innovation disturbance vector with empirical residual covariance\n",
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
                    "import joblib\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "from IPython.display import Image, display\n",
                    "\n",
                    "from csip.world.state_transition import WorldStateTransitionModel\n",
                    "\n",
                    "# Load Model & Evaluation\n",
                    "model = WorldStateTransitionModel.load(REPO_ROOT / 'artifacts' / 'models' / 'world_model_state_transition.joblib')\n",
                    "with open(REPO_ROOT / 'artifacts' / 'reports' / 'world_model_evaluation.json') as f:\n",
                    "    eval_report = json.load(f)\n",
                    "\n",
                    "print(f\"Fitted World Model Dimensions: d = {model.d}\")\n",
                    "print(f\"State Variables: {model.state_cols}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Structural Identifiability: Synthetic Parameter Recovery Test\n",
                    "Before deploying the World Model for counterfactual policy simulation, we verify that the estimator can accurately recover known ground-truth transition dynamics $\\mathbf{\\Phi}^*$ without structural bias or ill-conditioning."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "synth = eval_report['synthetic_recovery']\n",
                    "print(f\"Synthetic Recovery Status: {'PASSED' if synth['recovered'] else 'FAILED'}\")\n",
                    "print(f\"- Max Relative Error: {synth['max_rel_error']:.4f} (Threshold: <= {synth['tolerance']:.2f})\")\n",
                    "print(f\"- Mean Relative Error: {synth['mean_rel_error']:.4f}\")\n",
                    "\n",
                    "phi_star = np.array(synth['phi_star'])\n",
                    "phi_hat = np.array(synth['phi_hat'])\n",
                    "\n",
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)\n",
                    "im1 = ax1.imshow(phi_star, cmap='Blues', vmin=-0.2, vmax=0.8)\n",
                    "ax1.set_title('Ground-Truth Phi* Matrix')\n",
                    "for i in range(4):\n",
                    "    for j in range(4):\n",
                    "        ax1.text(j, i, f'{phi_star[i, j]:.2f}', ha='center', va='center')\n",
                    "\n",
                    "im2 = ax2.imshow(phi_hat, cmap='Blues', vmin=-0.2, vmax=0.8)\n",
                    "ax2.set_title('Recovered Estimated Phi Matrix')\n",
                    "for i in range(4):\n",
                    "    for j in range(4):\n",
                    "        ax2.text(j, i, f'{phi_hat[i, j]:.2f}', ha='center', va='center')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Empirical State Transition Matrix $\\mathbf{\\Phi}$\n",
                    "We inspect the learned inter-temporal cross-variable transition parameters governing macro system evolution."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "phi_df = pd.DataFrame(model.phi_matrix_, index=model.state_cols, columns=[f'{c}_lag1' for c in model.state_cols])\n",
                    "display(phi_df.round(4))\n",
                    "\n",
                    "print('Eigenvalues of Transition Matrix Phi (Stability Check):')\n",
                    "eigenvals = np.linalg.eigvals(model.phi_matrix_)\n",
                    "for ev in eigenvals:\n",
                    "    print(f\"- Magnitude: {abs(ev):.4f} (Stable: {abs(ev) < 1.0})\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Historical Replay Backtesting (2017–2018)\n",
                    "We evaluate the predictive accuracy of the World Model across 87 historical weeks."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "metrics_df = pd.DataFrame(eval_report['backtest_metrics']).T\n",
                    "display(metrics_df[['wape', 'mape', 'rmse']].round(4))\n",
                    "\n",
                    "display(Image(filename=str(REPO_ROOT / 'artifacts' / 'reports' / 'figures' / 'world_model_historical_replay.png')))"
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

    out_file = Path("notebooks/10_system_and_world_modeling.ipynb")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {out_file}")


if __name__ == "__main__":
    create_notebook_10()
