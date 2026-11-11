import os
import sys
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def scan_inventory():
    categories = {}
    total_files = 0
    total_bytes = 0
    file_list = []

    for p in ROOT.rglob('*'):
        if p.is_file():
            # Skip transient pycache in scan
            if any(part in ("__pycache__", ".pytest_cache") for part in p.parts):
                continue
            rel = p.relative_to(ROOT)
            top = rel.parts[0] if len(rel.parts) > 1 else 'root'
            categories.setdefault(top, {'count': 0, 'bytes': 0})
            categories[top]['count'] += 1
            categories[top]['bytes'] += p.stat().st_size
            total_files += 1
            total_bytes += p.stat().st_size
            file_list.append((str(rel), p.stat().st_size))

    print(f"Total tracked physical files: {total_files}, Total bytes: {total_bytes:,} ({total_bytes / (1024*1024):.2f} MB)")
    for cat, info in sorted(categories.items()):
        print(f"  {cat:20s}: {info['count']:4d} files, {info['bytes'] / (1024*1024):6.2f} MB")
    return categories, total_files, total_bytes, file_list

def scan_imports():
    import ast
    src_dir = ROOT / "src" / "csip"
    modules = {}
    for py_file in src_dir.rglob("*.py"):
        rel = py_file.relative_to(src_dir)
        mod_name = str(rel.with_suffix("")).replace(os.sep, ".")
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(py_file))
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
            modules[mod_name] = sorted(imports)
        except Exception as e:
            print(f"Error parsing {py_file}: {e}")
    print(f"\nScanned {len(modules)} Python modules in src/csip.")
    return modules

def scan_models():
    model_dir = ROOT / "artifacts" / "models"
    models = list(model_dir.glob("*.joblib")) + list(model_dir.glob("*.pt"))
    print(f"\nFound {len(models)} model binaries in artifacts/models/:")
    for m in sorted(models):
        sidecar = m.with_suffix(m.suffix + ".json")
        has_sidecar = sidecar.exists()
        print(f"  - {m.name} ({m.stat().st_size:,} bytes) [sidecar: {'YES' if has_sidecar else 'NO'}]")

def scan_datasets():
    data_dir = ROOT / "data"
    print(f"\nFound datasets in data/:")
    for p in sorted(data_dir.rglob("*.csv")):
        rel = p.relative_to(ROOT)
        print(f"  - {rel} ({p.stat().st_size:,} bytes)")
    for p in sorted(data_dir.rglob("*.parquet")):
        rel = p.relative_to(ROOT)
        print(f"  - {rel} ({p.stat().st_size:,} bytes)")

if __name__ == "__main__":
    scan_inventory()
    scan_imports()
    scan_models()
    scan_datasets()

