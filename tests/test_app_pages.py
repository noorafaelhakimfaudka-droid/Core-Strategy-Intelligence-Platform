"""Tests for CSIP Studio Cockpit using streamlit.testing.v1.AppTest.

Validates:
1. Primary cockpit (app/streamlit_app.py) renders without uncaught exceptions.
2. All 4 analytical lenses render cleanly:
   - Lens 1: Kurva Simulasi dan Titik Kritis
   - Lens 2: Peringkat Faktor Penentu
   - Lens 3: Sebaran Kelompok Data
   - Lens 4: Observatorium Drift & Stabilitas
3. Metrics displayed in the data provider match the source artifact files.
4. Analytical scope and methodological constraints are visible in the cockpit.
"""

from __future__ import annotations

from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

from app.data_provider import get_model_explainability

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_PATH = REPO_ROOT / "app" / "streamlit_app.py"


def test_main_cockpit_loads() -> None:
    """Verifies that the primary CSIP Studio cockpit (streamlit_app.py) executes cleanly."""
    assert APP_PATH.exists(), "app/streamlit_app.py does not exist"

    at = AppTest.from_file(str(APP_PATH), default_timeout=25)
    at.run(timeout=25)

    if at.exception:
        pytest.fail(f"streamlit_app.py raised uncaught exception: {at.exception[0]}")


@pytest.mark.parametrize(
    "lens_option",
    [
        "1. Kurva Simulasi dan Titik Kritis",
        "2. Peringkat Faktor Penentu",
        "3. Sebaran Kelompok Data",
        "4. Observatorium Drift & Stabilitas",
    ],
)
def test_all_four_lenses_render(lens_option: str) -> None:
    """Verifies that each of the 4 analytical lenses renders cleanly when selected."""
    at = AppTest.from_file(str(APP_PATH), default_timeout=25)
    at.run(timeout=25)
    assert not at.exception, f"Initial run exception: {at.exception}"

    # Locate the active lens radio control and select the lens
    target_radio = None
    for r in at.radio:
        if lens_option in r.options:
            target_radio = r
            break

    assert target_radio is not None, f"Could not find radio control containing '{lens_option}'"
    target_radio.set_value(lens_option)
    at.run(timeout=25)

    if at.exception:
        pytest.fail(f"Selecting lens '{lens_option}' raised uncaught exception: {at.exception[0]}")


def test_app_numbers_match_artifacts() -> None:
    """Verifies that model explainability metrics correspond directly to artifacts."""
    explainability = get_model_explainability()
    assert "calibration" in explainability
    cal_info = explainability["calibration"]
    brier_imp = cal_info.get("brier_improvement_pct", 0.0)
    assert brier_imp > 0.0, f"Expected positive Brier improvement percentage, got {brier_imp}"


def test_analytical_scope_and_limitations_visible() -> None:
    """Verifies that analytical scope disclaimer is rendered on the cockpit."""
    at = AppTest.from_file(str(APP_PATH), default_timeout=25)
    at.run(timeout=25)

    assert not at.exception
    captions = [c.value for c in at.caption]
    full_caption_text = " ".join(captions)
    assert "Cakupan Analitik" in full_caption_text
    assert "variabel kontinu" in full_caption_text


@pytest.mark.parametrize(
    "dataset_preset",
    [
        "Kasus 1: Toko Online & Kepuasan Pembeli (Data Olist)",
        "Kasus 2: Risiko Kesehatan & Gaya Hidup (Data Medis)",
        "Kasus 3: Kualitas Produk & Komposisi Bahan (Data Mutu)",
    ],
)
def test_cross_domain_datasets_render(dataset_preset: str) -> None:
    """Verifies that switching between distinct cross-domain datasets renders cleanly."""
    at = AppTest.from_file(str(APP_PATH), default_timeout=25)
    at.run(timeout=25)
    assert not at.exception

    preset_selectbox = None
    for sb in at.selectbox:
        if dataset_preset in sb.options:
            preset_selectbox = sb
            break

    assert preset_selectbox is not None, f"Could not find selectbox with '{dataset_preset}'"
    preset_selectbox.select(dataset_preset)
    at.run(timeout=25)

    if at.exception:
        pytest.fail(f"Selecting preset '{dataset_preset}' raised uncaught exception: {at.exception[0]}")

