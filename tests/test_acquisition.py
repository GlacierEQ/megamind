import pytest
from megamind import AgentAcquisitionEngine

def test_acquisition_engine():
    engine = AgentAcquisitionEngine()
    res = engine.mark_acquired("deer-flow-2.0", local_path="/tmp/deer-flow", notes="Acquired Wave 1 source genome")
    assert res["status"] == "SUCCESS"
    assert res["artifact"]["acquisition_state"] == "acquired"

    receipt = engine.generate_acquisition_receipt("deer-flow-2.0")
    assert receipt["receipt_id"] == "REC-DEER-FLOW-2.0"
    assert receipt["verification_status"] == "HARDENED"
