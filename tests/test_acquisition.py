import pytest
from megamind import AgentAcquisitionEngine

def test_acquisition_engine():
    engine = AgentAcquisitionEngine()
    res = engine.mark_acquired("DEERFLOW-2.0", local_path="/tmp/deer-flow", notes="Acquired Wave 1 source genome")
    assert res["status"] == "SUCCESS"
    assert res["artifact"]["acquisition_state"] == "ACQUIRED"

    rec = engine.generate_acquisition_receipt("DEERFLOW-2.0")
    assert rec["receipt_id"] == "REC-ACQ-DEERFLOW-2.0"
    assert rec["acquisition_state"] == "ACQUIRED"
