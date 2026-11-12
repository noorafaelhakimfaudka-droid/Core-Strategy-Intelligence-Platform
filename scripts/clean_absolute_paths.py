import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

reports_to_clean = [
    ROOT / "FINAL_CSIP_AUDIT_REPORT.md",
    ROOT / "reports" / "competency" / "canonical_mapping_validation.md",
    ROOT / "reports" / "reproducibility" / "reproducibility_report.md",
    ROOT / "reports" / "changelog_v5.md",
    ROOT / "README.md",
]

for rpt in reports_to_clean:
    if not rpt.exists():
        continue
    content = rpt.read_text(encoding="utf-8")
    # Replace file:///C:/Users/... with relative path or clean link
    content = re.sub(r'file:///C:/Users/[^)\s"]+scratch/csip/', '', content)
    content = re.sub(r'file:///C:/Users/[^)\s"]+', lambda m: m.group(0).split('/')[-1], content)
    content = re.sub(r'[A-Za-z]:\\Users\\[^\\]+\\Downloads\\CSIP_Source_Code(_V\d+)?\.zip', 'CSIP_Source_Code_V5.zip', content)
    content = re.sub(r'[A-Za-z]:[/\\]Users[/\\][^/\\]+[/\\]\.gemini[/\\]antigravity[/\\]scratch[/\\]csip[/\\]?', '', content)
    rpt.write_text(content, encoding="utf-8")
    print(f"Cleaned: {rpt.name}")

print("Path cleaning completed.")
