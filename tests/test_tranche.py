import pytest
from pathlib import Path
from megamind import MegamindRecoveryTranche

def test_recovery_tranche_sanitization(tmp_path):
    fake_config = tmp_path / "config.json"
    fake_config.write_text('{"secret": "sk-1234567890abcdef1234567890abcdef"}')

    tranche = MegamindRecoveryTranche()
    res = tranche.ingest_local_orbit(tmp_path, "TEST_ORBIT")
    assert res["status"] == "INGESTED"
    assert res["files_count"] == 1
    assert len(tranche.quarantine_log) >= 1

def test_tranche_receipt():
    tranche = MegamindRecoveryTranche()
    receipt = tranche.generate_tranche_receipt()
    assert receipt["tranche_id"] == "TRANCHE-OMEGA-999-RECOVERY"
    assert receipt["status"] == "RECOVERED_AND_QUARANTINED"
