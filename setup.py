from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
readme_text = (this_directory / "README.md").read_text(encoding="utf-8", errors="ignore") if (this_directory / "README.md").exists() else ""

setup(
    name="csip",
    version="0.1.0",
    description="Core Strategy & Intelligence Platform (CSIP)",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)
