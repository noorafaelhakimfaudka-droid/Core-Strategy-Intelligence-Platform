# CSIP V6 World Model & Scenario Simulator Audit

**Auditor**: Statistical Validation Specialist & Senior Research Methodologist  
**Date**: November 2026  
**Status**: STAGE 1 AUDIT COMPLETE  

---

## 1. Model Formulation Discrepancy (Finding F-04)

### Documented Formula:
$$S_{t+1} = C + \Phi S_t + \Gamma A_t + \Psi E_t + \varepsilon_t$$
where $A_t$ is action, $E_t$ is exogenous shocks.

### Actual Implemented Code:
```python
# Ridge fit on lag-1 state only:
self.regressor.fit(x_scaled, y_scaled) # x_scaled = S_t, y_scaled = S_{t+1}
# During simulation:
if action is not None:
    next_scaled += action
```
- The action $A_t$ was NOT estimated from historical action data (e.g. historical freight subsidy campaigns or SLA changes).
- Instead, the action was treated as an exogenous shock added directly to the state prediction.

---

## 2. Scientific Framing Remediation
1. **Clarify Distinction**:
   - $\Phi$: Empirically estimated autoregressive state transition matrix (estimated via Ridge regression with L2 regularization on weekly time-series panel).
   - $\Delta_{\text{action}}$: User-specified Policy Scenario Levers (counterfactual "what-if" perturbations).
2. **Backtesting Overhaul**:
   - Current backtest evaluated in-sample on the same training data.
   - V6 will implement **Chronological Holdout Validation**:
     - Training Panel: Weeks 1 to 60.
     - Out-of-Sample Evaluation Panel: Weeks 61 to 80.
     - Compute WAPE, MAPE, and RMSE on unseen future weeks.
