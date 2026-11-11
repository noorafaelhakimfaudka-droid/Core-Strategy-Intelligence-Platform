# CSIP V6 Model Evaluation & Diagnostic Integrity Audit

**Auditor**: Model Evaluation & Explainability Specialist  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Metric Definition Analysis: PR-AUC vs Average Precision

### The Trapezoidal PR-AUC Trap
In `trainer.py`:
```python
prec, rec, _ = precision_recall_curve(y_eval, probs)
pr_auc = float(auc(rec, prec))
```
- The trapezoidal rule calculates:
  $$\text{AUC} = \sum_{k=1}^{n-1} \frac{p_k + p_{k+1}}{2} (r_k - r_{k+1})$$
- When evaluated on a constant predictor (e.g. `B0_naive_majority`, which predicts constant probability or zeros), the precision-recall curve consists of a single point $(r=1, p=\pi)$ connected to $(r=0, p=1)$.
- The trapezoidal area under this segment is $\frac{\pi + 1}{2}$. For $\pi \approx 0.109$, this yields $\approx 0.5545$!
- This misleadingly suggests the naive baseline achieves > 0.50 PR-AUC.

### Correct Metric: Average Precision (AP)
Scikit-learn's `average_precision_score()` uses the step-wise rectangular integration:
$$\text{AP} = \sum_{n} (R_n - R_{n-1}) P_n$$
For a random or constant classifier, Average Precision correctly equals the positive class prevalence $\pi$ (approx. $0.128$).

---

## 2. Split Protocols and Model Selection
- **Temporal Splitting**:
  - Train: $\le$ 2018-03-31 ($N \approx 63,700$)
  - Validation: 2018-04-01 to 2018-06-30 ($N \approx 19,550$)
  - Locked Holdout Test: 2018-07-01 to 2018-08-31 ($N \approx 12,570$)
- **Enforcement**:
  - Model comparison and tuning MUST be performed strictly on the Validation set.
  - The Test set must be evaluated only ONCE for candidate models to establish true out-of-time generalization error.
