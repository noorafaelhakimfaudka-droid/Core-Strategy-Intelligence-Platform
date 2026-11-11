import json
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest_path = root / "data" / "dataset_manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for rel, meta in manifest.get("tables", {}).items():
    fp = root / rel
    if not fp.exists():
        print(f"MISSING: {rel}")
        continue
    actual = hashlib.sha256(fp.read_bytes()).hexdigest()
    if actual != meta.get("sha256"):
        print(f"MISMATCH: {rel} | actual={actual} | declared={meta.get('sha256')}")
    else:
        print(f"OK: {rel}")

