import re
import json
import tomllib
from pathlib import Path
from csip._version import __version__ as EXPECTED_VERSION

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_pyproject_version():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml not found"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    # Dynamic versioning via setuptools
    assert "version" in data.get("project", {}).get("dynamic", []), (
        "pyproject.toml must declare dynamic = ['version']"
    )
    assert data.get("tool", {}).get("setuptools", {}).get("dynamic", {}).get("version", {}).get("attr") == "csip._version.__version__", (
        "pyproject.toml dynamic version must point to csip._version.__version__"
    )

def test_setup_py_version():
    setup_path = REPO_ROOT / "setup.py"
    assert setup_path.exists(), "setup.py not found"
    content = setup_path.read_text(encoding="utf-8")
    assert "csip" in content
    import csip
    assert csip.__version__ == EXPECTED_VERSION

def test_package_init_version():
    import csip
    assert csip.__version__ == EXPECTED_VERSION, (
        f"csip.__version__ mismatch: {csip.__version__} != {EXPECTED_VERSION}"
    )

def test_dockerfile_version_label():
    docker_path = REPO_ROOT / "Dockerfile"
    assert docker_path.exists(), "Dockerfile not found"
    content = docker_path.read_text(encoding="utf-8")
    assert f'LABEL version="{EXPECTED_VERSION}"' in content, f"Dockerfile missing version label {EXPECTED_VERSION}"

def test_model_sidecars_version():
    models_dir = REPO_ROOT / "artifacts" / "models"
    json_files = list(models_dir.glob("*.json"))
    assert len(json_files) >= 5, f"Expected at least 5 model sidecars, found {len(json_files)}"
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        assert data.get("git_or_release_version") in [f"v{EXPECTED_VERSION}", EXPECTED_VERSION], (
            f"Model sidecar {jf.name} version is {data.get('git_or_release_version')} != {EXPECTED_VERSION}"
        )
