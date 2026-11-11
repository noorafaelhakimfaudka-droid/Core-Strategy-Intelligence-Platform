"""
Tests for Automated Data Lineage & Provenance Engine.
Verifies lineage graph creation, node integrity, and unbroken provenance chain.
"""

import json
from pathlib import Path
from csip.data.lineage import DataLineageTracker

ROOT = Path(__file__).resolve().parent.parent


def test_data_lineage_generation():
    lineage = DataLineageTracker.record_full_lineage()
    assert lineage is not None
    assert "schema_version" in lineage
    assert lineage["schema_version"] == "1.0.0"
    assert "nodes" in lineage


def test_data_lineage_nodes_presence():
    lineage = DataLineageTracker.record_full_lineage()
    nodes = lineage["nodes"]
    assert len(nodes["raw_datasets"]) == 9
    assert len(nodes["interim_datasets"]) == 8
    assert len(nodes["processed_datasets"]) == 5
    assert len(nodes["model_artifacts"]) >= 8


def test_data_lineage_file_hashes():
    lineage = DataLineageTracker.record_full_lineage()
    for category, file_dict in lineage["nodes"].items():
        for filename, meta in file_dict.items():
            assert "sha256" in meta
            assert meta["sha256"] != "FILE_NOT_FOUND", f"File {filename} in {category} not found on disk!"
            assert len(meta["sha256"]) == 64


def test_data_lineage_json_saved():
    target_file = ROOT / "artifacts" / "metadata" / "DATA_LINEAGE.json"
    assert target_file.exists()
    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["lineage_integrity"]["unbroken_chain"] is True

