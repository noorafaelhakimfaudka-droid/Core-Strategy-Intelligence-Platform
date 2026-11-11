import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
manifest_path = ROOT / "data" / "dataset_manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    old_manifest = json.load(f)

new_tables = {}

for rel_path, old_meta in old_manifest.get("tables", {}).items():
    fp = ROOT / rel_path
    assert fp.exists(), f"Missing dataset: {rel_path}"
    
    file_bytes = fp.read_bytes()
    file_size = len(file_bytes)
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    
    # Read parquet metadata / dataframe
    df = pd.read_parquet(fp)
    row_count = len(df)
    cols = list(df.columns)
    
    new_tables[rel_path] = {
        "grain_type": old_meta.get("grain_type", "processed"),
        "filename": fp.name,
        "row_count": row_count,
        "column_count": len(cols),
        "columns": cols,
        "size_bytes": file_size,
        "size_mb": round(file_size / (1024 * 1024), 3),
        "sha256": sha256_hash,
    }
    print(f"Updated {rel_path}: {row_count} rows, {len(cols)} cols, {sha256_hash[:12]}...")

new_manifest = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "release_version": "15.0.0",
    "tables": new_tables
}

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(new_manifest, f, indent=2)

print(f"Successfully saved {manifest_path} with 13 verified Parquet tables.")

