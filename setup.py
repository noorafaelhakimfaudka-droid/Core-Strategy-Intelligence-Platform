import re
from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
readme_text = (this_directory / "README.md").read_text(encoding="utf-8", errors="ignore") if (this_directory / "README.md").exists() else ""

version_file = this_directory / "src" / "csip" / "_version.py"
match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', version_file.read_text(encoding="utf-8"))
version = match.group(1) if match else "17.0.0"

setup(
    name="csip",
    version=version,
    description="Core Strategy & Intelligence Platform (CSIP)",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)

