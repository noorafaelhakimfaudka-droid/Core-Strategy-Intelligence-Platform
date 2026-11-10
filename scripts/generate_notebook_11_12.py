"""Generate Notebooks 11 and 12 for Milestone 10."""

import json
from pathlib import Path


def create_notebook_11():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# CSIP Module 11: Alternative World Simulation & Counterfactual Policy Analysis\n",
                    "**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**\n",
                    "\n",
                    "### SKKNI Data Science Competency Standards\n",
                    "- **[UK-08 Membangun Skenario Model]**: Perancangan 6 skenario intervensi kebijakan (S0 s.d. S5).\n",
                    "- **[UK-11 Mengembangkan Solusi]**: Proyeksi kelayakan ekonomi, biaya subsidi, GMV lift, dan net profit platform.\n",
                    "\n",
                    "### Policy Intervention Portfolio\n",
                    "1. **S0 Baseline**: Status quo execution.\n",
                    "2. **S1 Freight Subsidy**: Universal flat 15% freight subsidy across all transactions.\n",
                    "3. **S2 Carrier SLA Overhaul**: Partner carrier logistics optimization cutting delay by 3 days.\n",
                    "4. **S3 Targeted Friction Subsidy**: Selective 25% subsidy allocated exclusively to High Friction Cohort (Cluster 0).\n",
                    "5. **S4 Macro Shock**: Severe inflation (+20% freight) and carrier disruption (+4 days delay).\n",
                    "6. **S5 Combined Blitz**: Dual intervention (-15% freight, -3 days delay).\n",
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
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "from IPython.display import Image, display\n",
                    "\n",
                    "# Load Scenario Simulation Results\n",
                    "results_path = REPO_ROOT / 'artifacts' / 'reports' / 'scenario_simulation_results.json'\n",
                    "with open(results_path, 'r') as f:\n",
                    "    sim_data = json.load(f)\n",
                    "\n",
                    "print(f\"Loaded {len(sim_data)} Counterfactual Policy Scenarios (12-Week Horizon).\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Scenario Comparison Table (Deltas vs S0 Baseline)\n",
                    "We inspect the projected cumulative trade-offs between customer acquisition, satisfaction improvement, and financial sustainability."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "summary_rows = []\n",
                    "for s_id, s in sim_data.items():\n",
                    "    cmp = s.get('comparison_to_s0', {})\n",
                    "    summary_rows.append({\n",
                    "        'Scenario ID': s_id,\n",
                    "        'Name': s['name'],\n",
                    "        'Cumul Volume': int(round(s['cumulative_volume'])),\n",
                    "        'Delta Orders': int(round(cmp.get('delta_volume_orders', 0))),\n",
                    "        'Delta Orders (%)': f\"{cmp.get('delta_volume_pct', 0):+.2f}%\",\n",
                    "        'Review Rate (%)': f\"{s['avg_negative_review_rate']*100:.2f}%\",\n",
                    "        'Delta Review (pp)': f\"{cmp.get('delta_negative_review_pp', 0):+.2f} pp\",\n",
                    "        'Subsidy Cost (BRL)': f\"R$ {s['subsidy_cost_brl']:,.2f}\",\n",
                    "        'Net Profit (BRL)': f\"R$ {cmp.get('net_incremental_profit_brl', 0):,.2f}\",\n",
                    "        'Guardrail': 'PASS' if not s['guardrail']['is_out_of_distribution'] else 'OOD WARN',\n",
                    "    })\n",
                    "\n",
                    "summary_df = pd.DataFrame(summary_rows)\n",
                    "display(summary_df)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Visual Comparative Policy Trajectories\n",
                    "Inspection of the 12-week evolution of volume, dissatisfaction risk, and financial return."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "display(Image(filename=str(REPO_ROOT / 'artifacts' / 'reports' / 'figures' / 'scenario_simulations.png')))"
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

    out_file = Path("notebooks/11_alternative_world_simulation.ipynb")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {out_file}")


def create_notebook_12():
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# CSIP Module 12: Uncertainty Quantification & Extrapolation Guardrails\n",
                    "**Computational Society Intelligence Platform (CSIP) — Behavioral Decision Intelligence (BDI)**\n",
                    "\n",
                    "### SKKNI Data Science Competency Standards\n",
                    "- **[UK-10 Mengevaluasi Hasil Pemodelan]**: Kuantifikasi ketidakpastian proyeksi simulasi via Multi-Trajectory Residual Bootstrapping.\n",
                    "- **Claim Governance**: Deteksi Out-of-Distribution (OOD) dan penurunan Evidence Grade otomatis (Grade B ke Grade C/D).\n",
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
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "results_path = REPO_ROOT / 'artifacts' / 'reports' / 'scenario_simulation_results.json'\n",
                    "with open(results_path, 'r') as f:\n",
                    "    sim_data = json.load(f)\n",
                    "\n",
                    "print('Loaded simulation uncertainty profiles.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Prediction Interval Ordering & Dispersion Analysis\n",
                    "We verify that the generated Prediction Intervals satisfy the monotonic ordering:\n",
                    "$$P_{02.5} \\le P_{05.0} \\le P_{50.0} (\\text{Median}) \\le P_{95.0} \\le P_{97.5}$$"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "for s_id in ['S0_baseline', 'S2_carrier_sla', 'S4_macro_shock']:\n",
                    "    s = sim_data[s_id]\n",
                    "    intv = s['intervals']\n",
                    "    vol_p025 = np.array(intv['p025'])[1:, 0]\n",
                    "    vol_p50 = np.array(intv['median'])[1:, 0]\n",
                    "    vol_p975 = np.array(intv['p975'])[1:, 0]\n",
                    "    \n",
                    "    is_monotonic = bool(np.all(vol_p025 <= vol_p50) and np.all(vol_p50 <= vol_p975))\n",
                    "    print(f\"Scenario {s_id:20s}: Monotonic PI Ordering Verified = {is_monotonic}\")\n",
                    "    print(f\"  - Week 12 Volume 95% PI: [{vol_p025[-1]:.0f}, {vol_p975[-1]:.0f}] (Median: {vol_p50[-1]:.0f})\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Extrapolation Guardrail Audit\n",
                    "We audit which scenarios stay within historical convex bounds and which trigger OOD warnings."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "guardrail_rows = []\n",
                    "for s_id, s in sim_data.items():\n",
                    "    g = s['guardrail']\n",
                    "    guardrail_rows.append({\n",
                    "        'Scenario': s_id,\n",
                    "        'Out of Distribution': g['is_out_of_distribution'],\n",
                    "        'Max Z-Score': round(g['max_z_score'], 2),\n",
                    "        'Evidence Grade': g['evidence_grade'],\n",
                    "        'Violations Count': len(g['violations']),\n",
                    "    })\n",
                    "\n",
                    "display(pd.DataFrame(guardrail_rows))"
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

    out_file = Path("notebooks/12_uncertainty_quantification.ipynb")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {out_file}")


if __name__ == "__main__":
    create_notebook_11()
    create_notebook_12()
