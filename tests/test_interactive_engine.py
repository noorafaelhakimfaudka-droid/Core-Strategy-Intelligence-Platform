"""Unit tests for CSIP Universal Interactive Decision Lab engines.

Validates:
- OmniRouter natural language parsing and intent classification
- ScenarioDuelEngine trade-off calculations, what-if simulations, and duels
- TextConstellationEngine topic clustering and 2D celestial coordinate projection
- UniversalCSVXRay role detection, auto-cleaning, clustering, and factor discovery (SKKNI UK-03 to UK-07)
"""

from __future__ import annotations

import pandas as pd
import pytest

from csip.experimental.omni_router import OmniRouter, parse_user_query
from csip.experimental.scenario_duel import ScenarioDuelEngine
from csip.experimental.text_constellation import TextConstellationEngine
from csip.experimental.universal_csv_xray import UniversalCSVXRay


def test_omni_router_modes_and_parameters():
    """Verify OmniRouter correctly classifies modes and extracts numerical parameters."""
    router = OmniRouter()

    # Bedah mode
    r_bedah = router.parse("Mengapa orang rela antre lama?")
    assert r_bedah["mode"] == "bedah"

    # Pengandaian mode with numbers
    r_whatif = router.parse("Bagaimana jika subsidi ongkir dipotong 25 persen tapi waktu tiba bertambah 2 hari?")
    assert r_whatif["mode"] == "pengandaian"
    assert r_whatif["parameters"]["subsidy_pct"] == 25.0
    assert r_whatif["parameters"]["delay_days_delta"] == 2.0

    # Duel mode
    r_duel = router.parse("Pilihan A: Subsidi ongkir vs Pilihan B: Perbaikan kurir")
    assert r_duel["mode"] == "adu"

    # Text mode
    r_text = router.parse("Barang cepat sampai.\nPelayanan ramah.\nKemasan rapi.\nSangat puas.")
    assert r_text["mode"] == "teks"


def test_scenario_duel_engine():
    """Verify ScenarioDuelEngine calculations and outputs across all 3 modes."""
    duel = ScenarioDuelEngine()

    # Dissect phenomenon
    phenom = duel.dissect_phenomenon()
    assert len(phenom["delay_days"]) > 20
    assert len(phenom["satisfaction"]) == len(phenom["delay_days"])
    assert phenom["breaking_point_day"] == 3.0
    assert len(phenom["key_factors"]) == 5

    # What-if simulation
    sim = duel.simulate_what_if(subsidy_pct=20.0, delay_days_delta=-1.0)
    assert sim["simulated_volume"] > 0
    assert len(sim["weeks"]) == 12
    assert len(sim["expected_trajectory"]) == 12
    assert "guardrail_status" in sim

    # Option duel
    duel_res = duel.duel_two_options()
    assert "option_a" in duel_res
    assert "option_b" in duel_res
    assert "winner" in duel_res
    assert len(duel_res["weeks"]) == 12


def test_text_constellation_engine():
    """Verify TextConstellationEngine sentiment scoring and 2D celestial coordinates."""
    tc = TextConstellationEngine()
    sample_text = (
        "Barang cepat tiba dan sangat puas dengan kualitasnya\n"
        "Paket terlambat seminggu dan kemasan rusak parah\n"
        "Ongkos kirim terasa sangat mahal untuk jarak dekat\n"
        "Pelayanan penjual luar biasa dan sangat direkomendasikan"
    )
    res = tc.process_text_corpus(sample_text)
    assert res["total_opinions"] >= 4
    assert 1.0 <= res["average_sentiment"] <= 5.0
    for pt in res["points"]:
        assert "x" in pt and "y" in pt
        assert "color" in pt
        assert pt["color"].startswith("#")


def test_universal_csv_xray_pipeline():
    """Verify UniversalCSVXRay fulfills SKKNI UK-03 to UK-07 on arbitrary tabular data."""
    xray = UniversalCSVXRay()
    sample_df = xray.generate_sample_csv(n_rows=200)

    # Ingest and X-Ray
    res = xray.analyze(sample_df)
    assert res["row_count"] == 200
    assert res["column_count"] >= 5

    # Roles detected
    roles = res["roles"]
    assert roles["value_col"] is not None
    assert roles["time_col"] is not None

    # Clustering
    clusters = res["clusters"]
    assert clusters["k"] >= 2
    assert len(clusters["labels"]) == 200
    assert len(clusters["pca_x"]) == 200

    # Factor discovery
    factors = res["factors"]
    assert len(factors) >= 1
    assert factors[0]["pengaruh_pct"] > 0

