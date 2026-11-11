import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ZIP = Path(r"C:\Users\asus\Downloads\CSIP_Source_Code_V6.zip")

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".system_generated",
}

EXCLUDED_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
}

def create_zip():
    OUTPUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    total_size = 0
    
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                if any(file.endswith(ext) for ext in EXCLUDED_EXTS):
                    continue
                full_path = Path(root) / file
                rel_path = full_path.relative_to(ROOT)
                zf.write(full_path, arcname=str(rel_path))
                count += 1
                total_size += full_path.stat().st_size
                
    mb_size = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"Packaged {count} files ({total_size / (1024 * 1024):.2f} MB uncompressed) into:")
    print(f"  {OUTPUT_ZIP} ({mb_size:.2f} MB)")

if __name__ == "__main__":
    create_zip()
