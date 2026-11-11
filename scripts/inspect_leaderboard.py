import json
from pathlib import Path

board_path = Path("artifacts/reports/ml_leaderboard.json")
data = json.load(open(board_path, encoding="utf-8"))

print("=== 1. NEGATIVE REVIEW PREDICTION ===")
print(f"{'Exp ID':18s} | {'Model':20s} | {'Split':10s} | {'Feature Set':28s} | {'PR-AUC':7s} | {'ROC-AUC':7s} | {'F1':6s} | {'Brier':6s}")
print("-" * 115)
for d in data:
    if d["target_name"] == "negative_review_flag":
        print(f"{d['experiment_id']:18s} | {d['model_name']:20s} | {d['split_name']:10s} | {d['feature_set_name']:28s} | {d.get('pr_auc', 0.0):.4f}  | {d.get('roc_auc', 0.0):.4f}  | {d.get('f1_score', 0.0):.4f} | {d.get('brier_score', 0.0):.4f}")

print("\n=== 2. REPEAT PURCHASE COHORT PREDICTION ===")
print(f"{'Exp ID':18s} | {'Model':20s} | {'Split':10s} | {'Feature Set':28s} | {'PR-AUC':7s} | {'ROC-AUC':7s} | {'F1':6s} | {'Brier':6s}")
print("-" * 115)
for d in data:
    if d["target_name"] == "repeat_purchase_flag":
        print(f"{d['experiment_id']:18s} | {d['model_name']:20s} | {d['split_name']:10s} | {d['feature_set_name']:28s} | {d.get('pr_auc', 0.0):.4f}  | {d.get('roc_auc', 0.0):.4f}  | {d.get('f1_score', 0.0):.4f} | {d.get('brier_score', 0.0):.4f}")

print("\n=== 3. DELIVERY DELAY REGRESSION ===")
print(f"{'Exp ID':18s} | {'Model':20s} | {'Split':10s} | {'Feature Set':28s} | {'RMSE':7s} | {'MAE':7s} | {'R2':6s}")
print("-" * 105)
for d in data:
    if d["target_name"] == "delivery_delay_days":
        print(f"{d['experiment_id']:18s} | {d['model_name']:20s} | {d['split_name']:10s} | {d['feature_set_name']:28s} | {d.get('rmse', 0.0):.4f}  | {d.get('mae', 0.0):.4f}  | {d.get('r2', 0.0):.4f}")


