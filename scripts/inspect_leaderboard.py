import json
from pathlib import Path

board_path = Path("artifacts/reports/ml_leaderboard.json")
data = json.load(open(board_path, encoding="utf-8"))

print(f"{'Exp ID':18s} | {'Model':20s} | {'Split':10s} | {'Feature Set':26s} | {'PR-AUC':7s} | {'ROC-AUC':7s} | {'F1':6s} | {'Brier':6s}")
print("-" * 115)
for d in data:
    if d["target_name"] == "negative_review_flag":
        print(f"{d['experiment_id']:18s} | {d['model_name']:20s} | {d['split_name']:10s} | {d['feature_set_name']:26s} | {d['pr_auc']:.4f}  | {d['roc_auc']:.4f}  | {d['f1_score']:.4f} | {d['brier_score']:.4f}")
