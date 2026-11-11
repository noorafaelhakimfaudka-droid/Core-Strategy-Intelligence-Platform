"""Automated regression test enforcing Rule 6 (No Overclaims in Active Documentation)."""

import pytest
from tools.check_claims import scan_all

def test_zero_overclaims_across_active_repository():
    """Verify that zero forbidden overclaim phrases exist in active non-archived files."""
    findings = scan_all()
    if findings:
        report = "\n".join(f"{f['file']}:{f['line']} [{f['rule']}] -> {f['snippet']}" for f in findings)
        pytest.fail(f"Detected {len(findings)} forbidden overclaim phrases:\n{report}")

