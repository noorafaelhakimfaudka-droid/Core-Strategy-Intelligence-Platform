import json
from pathlib import Path

NB_DIR = Path("notebooks")
notebooks = sorted(NB_DIR.glob("*.ipynb"))

print(f"Auditing {len(notebooks)} notebooks in notebooks/...")
manifest = []

for nb_path in notebooks:
    try:
        nb_data = json.loads(nb_path.read_text(encoding="utf-8"))
        cells = nb_data.get("cells", [])
        code_cells = [c for c in cells if c.get("cell_type") == "code"]
        md_cells = [c for c in cells if c.get("cell_type") == "markdown"]
        cells_with_output = [c for c in code_cells if c.get("outputs")]
        
        info = {
            "notebook_name": nb_path.name,
            "path": str(nb_path.as_posix()),
            "total_cells": len(cells),
            "code_cells": len(code_cells),
            "markdown_cells": len(md_cells),
            "executed_cells": len(cells_with_output),
            "execution_coverage": round(len(cells_with_output) / max(1, len(code_cells)), 2),
            "status": "VALID" if len(cells) > 0 else "EMPTY"
        }
        manifest.append(info)
        print(f"  {nb_path.name:45s} | Cells: {len(cells):2d} (Code: {len(code_cells):2d}, MD: {len(md_cells):2d}, Executed: {len(cells_with_output):2d})")
    except Exception as e:
        print(f"  ERROR reading {nb_path.name}: {e}")
        manifest.append({
            "notebook_name": nb_path.name,
            "status": "ERROR",
            "error": str(e)
        })

out_manifest = {
    "version": "6.0.0",
    "total_notebooks": len(manifest),
    "notebooks": manifest
}

with open(NB_DIR / "notebook_manifest.json", "w", encoding="utf-8") as f:
    json.dump(out_manifest, f, indent=2)

print(f"\nSaved notebook manifest to {NB_DIR / 'notebook_manifest.json'}")
