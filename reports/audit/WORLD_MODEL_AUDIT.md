# CSIP World Model Empirical Audit Report
## Parameter Recovery, Transition Matrix Inspection, and Holdout Backtest Results
### Standard: SKKNI No. 299 Tahun 2020 | Unit: J.62DMI00.010.1 & J.62DMI00.011.1

- **Document ID**: `CSIP-AUDIT-WORLD-2026-V7`
- **Version**: 7.0.0
- **Model Checkpoint**: `artifacts/models/world_model_state_transition.joblib`
- **Evaluation Log**: `artifacts/reports/world_model_evaluation.json`
- **Status**: EMPIRICALLY VERIFIED & DEFENDED

---

## 1. Executive Summary

The CSIP World Model dynamic state-space transition engine was audited across synthetic parameter recovery, empirical matrix condition, and out-of-sample chronological holdout backtesting.

### Key Audit Findings:
- **Synthetic Parameter Recovery**: **PASSED**. Mean relative parameter error is **0.0033 (0.33%)** and maximum error is **0.0160 (1.60%)**, confirming that the Ridge estimator correctly identifies state-space dynamics under ground-truth simulation.
- **Empirical Transition Fit**: Fitted on 87 weekly panel observations (86 state transitions).
- **Out-of-Sample Holdout Performance (Weeks 65–87)**:
  - `mean_freight_ratio`: **7.55% WAPE** (RMSE: 0.0275)
  - `mean_delivery_delay`: **19.80% WAPE** (RMSE: 3.59 days)
  - `weekly_order_volume`: **19.85% WAPE** (RMSE: 390.99 orders)
  - `negative_review_rate`: **27.17% WAPE** (RMSE: 0.0311)
- **Zero Forward Leakage**: Chronological holdout strictly ensures that parameters estimated on Weeks 1–64 never saw future transitions from Weeks 65–87.

---

## 2. Transition Matrix ($\Phi$) Structure and Interpretation

The estimated transition matrix $\Phi \in \mathbb{R}^{4 \times 4}$ on standardized coordinates reveals key systemic feedback mechanisms:

| Dependent ($t+1$) \ Input ($t$) | $S_{1}$: Order Volume | $S_{2}$: Delivery Delay | $S_{3}$: Freight Ratio | $S_{4}$: Negative Review Rate |
| :--- | ---: | ---: | ---: | ---: |
| **$S_{1}$: Order Volume** | **+0.742** | -0.114 | -0.082 | -0.095 |
| **$S_{2}$: Delivery Delay** | +0.086 | **+0.621** | +0.043 | +0.138 |
| **$S_{3}$: Freight Ratio** | -0.052 | +0.031 | **+0.891** | +0.019 |
| **$S_{4}$: Negative Review Rate**| -0.041 | **+0.384** | +0.127 | **+0.512** |

### System Dynamics Insights:
1. **Autoregressive Persistence**: All diagonal terms are positive ($\Phi_{ii} \in [0.51, 0.89]$), indicating sustained inertia in weekly volume, shipping costs, and customer review sentiment.
2. **Logistics Delay Spillover to Reviews**: The off-diagonal term $\Phi_{4,2} = +0.384$ demonstrates that positive spikes in weekly delivery delay directly inflate the subsequent week's negative review rate.
3. **Volume Demand Dampening**: Delivery delays and review spikes exert negative feedback on subsequent order volume ($\Phi_{1,2} = -0.114, \Phi_{1,4} = -0.095$).

---

## 3. Detailed Backtesting Evaluation Table

| State Variable | In-Sample WAPE (Weeks 1–87) | In-Sample RMSE | Out-of-Sample WAPE (Weeks 65–87) | Out-of-Sample RMSE | Out-of-Sample MAPE |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `weekly_order_volume` | 16.48% | 299.44 | **19.85%** | 390.99 | 57.45% |
| `mean_delivery_delay` | 13.00% | 2.33 days | **19.80%** | 3.59 days | 21.37% |
| `mean_freight_ratio` | 4.53% | 0.0182 | **7.55%** | 0.0275 | 7.53% |
| `negative_review_rate` | 16.14% | 0.0251 | **27.17%** | 0.0311 | 29.62% |

---

## 4. Verification Conclusion

The CSIP World Model provides an empirically defensible, mathematically validated state-space simulator. The model satisfies all requirements of SKKNI units `J.62DMI00.008.1` (Membangun Skenario Model) and `J.62DMI00.009.1` (Membangun Model), with verified out-of-sample holdout performance and transparent non-causal sensitivity boundaries.
