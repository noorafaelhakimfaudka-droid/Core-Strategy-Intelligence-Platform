import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
standards_path = ROOT / "standards" / "canonical_skkni_299_2020.json"
canonical_registry_path = ROOT / "competency" / "CANONICAL_EVIDENCE_REGISTRY.csv"
output_csv_path = ROOT / "competency" / "SKKNI_TRACEABILITY_MATRIX.csv"

# Load standards JSON
with open(standards_path, "r", encoding="utf-8") as f:
    std_data = json.load(f)

# Load canonical registry rows
registry_rows = {}
with open(canonical_registry_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        key = (r["unit_code"], r["kuk_number"])
        registry_rows[key] = r

traceability_rows = []

for u in std_data.get("units", []):
    u_code = u["unit_code"]
    u_title = u["official_unit_title"]
    for el in u.get("competency_elements", []):
        e_code = el["element_id"]
        e_title = el["element_title"]
        for kuk in el.get("performance_criteria", []):
            kuk_no = kuk["kuk_id"]
            canonical_wording = kuk["kuk_text"].strip()
            kuk_code = f"{u_code}-{kuk_no}"
            
            # Lookup in canonical evidence registry
            reg = registry_rows.get((u_code, kuk_no), {})
            
            evidence_id = f"EVD-{u_code.split('.')[1] if '.' in u_code else u_code}-{kuk_no.replace('.', '_')}"
            evidence_path = reg.get("exact_location", "")
            evidence_type = reg.get("evidence_type", "")
            validation_status = reg.get("verification_result", "NOT_EVIDENCED")
            source_doc = reg.get("actual_source_artifact", "")
            source_loc = reg.get("exact_location", "")
            validation_notes = reg.get("expected_candidate_explanation", "")

            traceability_rows.append({
                "Unit_Code": u_code,
                "Unit_Title": u_title,
                "Element_Code": e_code,
                "Element_Title": e_title,
                "KUK_Code": kuk_code,
                "Canonical_Wording": canonical_wording,
                "Source_Document": source_doc,
                "Source_Location": source_loc,
                "Evidence_ID": evidence_id,
                "Evidence_Path": evidence_path,
                "Evidence_Type": evidence_type,
                "Validation_Status": validation_status,
                "Validation_Notes": validation_notes,
            })

print(f"Generated {len(traceability_rows)} traceability rows.")
assert len(traceability_rows) == 63, f"Expected 63 KUKs, got {len(traceability_rows)}"

fieldnames = [
    "Unit_Code",
    "Unit_Title",
    "Element_Code",
    "Element_Title",
    "KUK_Code",
    "Canonical_Wording",
    "Source_Document",
    "Source_Location",
    "Evidence_ID",
    "Evidence_Path",
    "Evidence_Type",
    "Validation_Status",
    "Validation_Notes",
]

with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(traceability_rows)

print(f"Successfully saved {output_csv_path}")
