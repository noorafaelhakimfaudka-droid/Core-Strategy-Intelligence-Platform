import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

print("=== RECONCILING CALIBRATION METHODOLOGY & MODEL CARDS ===")

# 1. Unify Calibration wording to Platt Scaling in documentation
files_to_reconcile = [
    ROOT / "competency" / "PORTFOLIO_ASSESSMENT_GUIDE.md",
    ROOT / "competency" / "STRUCTURED_INSTRUCTION_GUIDE.md",
    ROOT / "competency" / "ASSESSOR_EVIDENCE_GUIDE.md",
    ROOT / "reports" / "architecture_readiness_report.md",
    ROOT / "reports" / "canonical_skkni_299_2020_mapping.md",
    ROOT / "reports" / "evidence" / "evidence_validation_report.md",
    ROOT / "reports" / "evidence" / "evidence_traceability_matrix.md",
    ROOT / "reports" / "participant_decision_log.md",
    ROOT / "reports" / "assessment" / "participant_decision_log.md",
]

for fp in files_to_reconcile:
    if fp.exists():
        txt = fp.read_text(encoding="utf-8")
        orig_txt = txt
        # Replace Isotonic with Platt Scaling where describing negative review calibration
        txt = re.sub(r"kalibrasi\s+Isotonic", "kalibrasi Platt Scaling", txt, flags=re.IGNORECASE)
        txt = re.sub(r"Isotonic\s+Regression", "Platt Scaling (Logistic Sigmoid on Log-Odds)", txt)
        txt = re.sub(r"Platt/Isotonic scaling", "Platt Scaling", txt)
        if txt != orig_txt:
            fp.write_text(txt, encoding="utf-8")
            print(f"Updated calibration references in {fp.relative_to(ROOT)}")

# 2. Update all Model Cards in reports/model_cards/
model_cards_dir = ROOT / "reports" / "model_cards"

maturity_map = {
    "MODEL_CARD_NEGATIVE_REVIEW_LIGHTGBM.md": {
        "maturity": "CONDITIONALLY_ELIGIBLE_FOR_PILOT",
        "maturity_desc": "Offline out-of-time test validated (PR-AUC 0.3061, calibrated Brier 0.0762, ECE 0.0070). Conditionally eligible for human-in-the-loop pilot triage in customer support operations. Prospective shadow testing required before autonomous action."
    },
    "MODEL_CARD_DELIVERY_DELAY_LIGHTGBM.md": {
        "maturity": "CONDITIONALLY_ELIGIBLE_FOR_PILOT",
        "maturity_desc": "Offline out-of-time test validated (MAE 4.8256 days, R^2 = 0.3926). Conditionally eligible for operational pilot alerting to logistics dispatchers; carrier SLA integration monitoring required."
    },
    "MODEL_CARD_TEXT_BILSTM_SENTIMENT.md": {
        "maturity": "BENCHMARK_VALIDATED",
        "maturity_desc": "Offline test validated on written Portuguese customer reviews subset (PR-AUC 0.3120, ROC-AUC 0.7240). Validated as an NLP benchmark; requires low-latency inference optimization before pilot deployment."
    },
    "MODEL_CARD_REPEAT_PURCHASE_POST_DELIVERY_LIGHTGBM.md": {
        "maturity": "RESEARCH_ONLY",
        "maturity_desc": "Post-delivery cohort behavior benchmark (PR-AUC 0.0245, ROC-AUC 0.5284). Retained strictly for empirical comparison and longitudinal customer behavior research."
    },
    "MODEL_CARD_REPEAT_PURCHASE_CHECKOUT_LIGHTGBM.md": {
        "maturity": "RESEARCH_ONLY",
        "maturity_desc": "Checkout-time basket prediction benchmark. Formally REJECTED for operational deployment due to 95% bootstrap confidence interval [0.472, 0.531] spanning chance baseline 0.50 (ROC-AUC 0.5021). Valid negative finding."
    },
    "MODEL_CARD_WORLD_MODEL.md": {
        "maturity": "BENCHMARK_VALIDATED",
        "maturity_desc": "Macroeconomic Vector AutoRegressive (VAR) state-space model (WAPE 15.83% vs persistence baseline 22.41%). Validated for scenario analysis and counterfactual simulation; not approved as an autonomous controller."
    }
}

for mc in model_cards_dir.glob("*.md"):
    if mc.name == "MODEL_SELECTION_DECISION_REPORT.md":
        txt = mc.read_text(encoding="utf-8")
        txt = re.sub(r"-\s*\*\*Version\*\*:\s*1[345]\.0(?:\.0)?", "- **Version**: 16.0.0", txt)
        txt = re.sub(r"APPROVED_FOR_DEPLOYMENT", "CONDITIONALLY_ELIGIBLE_FOR_PILOT", txt)
        txt = re.sub(r"APPROVED FOR DEPLOYMENT", "CONDITIONALLY ELIGIBLE FOR PILOT", txt)
        mc.write_text(txt, encoding="utf-8")
        print(f"Updated {mc.name}")
        continue

    txt = mc.read_text(encoding="utf-8")
    # Update Version to 16.0.0
    txt = re.sub(r"-\s*\*\*Version\*\*:\s*1[345]\.0(?:\.0)?", "- **Version**: 16.0.0", txt)
    txt = re.sub(r"CSIP Version 1[345]", "CSIP Version 16", txt)
    
    # Update maturity status
    meta = maturity_map.get(mc.name)
    if meta:
        mat_status = meta["maturity"]
        mat_desc = meta["maturity_desc"]
        
        # Check if deployment maturity section exists or add/update it
        if "### Deployment Maturity" in txt or "### 9. Deployment Maturity" in txt or "Maturity Level" in txt:
            txt = re.sub(
                r"###\s*(?:\d+\.\s*)?Deployment Maturity[\s\S]*?(?=###|$)",
                f"### Deployment Maturity Level\n- **Status**: `{mat_status}`\n- **Operational Governance Assessment**: {mat_desc}\n\n",
                txt
            )
        else:
            # Append deployment maturity before limitations or at end
            maturity_section = f"\n### Deployment Maturity Level\n- **Status**: `{mat_status}`\n- **Operational Governance Assessment**: {mat_desc}\n"
            txt += maturity_section
            
    mc.write_text(txt, encoding="utf-8")
    print(f"Updated model card: {mc.name} (Version 16.0.0, Maturity={meta['maturity'] if meta else 'N/A'})")

# 3. Update sidecars git_or_release_version in artifacts/models/*.joblib.json
for mj in (ROOT / "artifacts" / "models").glob("*.json"):
    data = json.loads(mj.read_text(encoding="utf-8"))
    data["git_or_release_version"] = "v16.0.0"
    mj.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated model sidecar: {mj.name} to v16.0.0")

print("\nModel cards and calibration reconciled successfully.")
