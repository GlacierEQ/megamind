import pytest
from megamind import MegamindRegistry, AgentMeshConnector

def test_mesh_auto_connect():
    registry = MegamindRegistry(seed_defaults=True)
    connector = AgentMeshConnector(registry)
    conns = connector.auto_connect_swarm()
    assert len(conns) == 4
    assert any(c["source"] == "doctor_strange" and c["target"] == "doc_ock" for c in conns)
    assert any(c["source"] == "doc_ock" and c["target"] == "sherlock_alpha" for c in conns)

def test_mesh_event_dispatch():
    registry = MegamindRegistry(seed_defaults=True)
    connector = AgentMeshConnector(registry)
    connector.auto_connect_swarm()
    res = connector.dispatch_event("mission_dispatch", "doctor_strange", {"mission_id": "M-101", "intent": "BUILD_SWARM"})
    assert res["delivery_status"] == "DELIVERED"
    assert "doc_ock" in res["recipients"]
