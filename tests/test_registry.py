import pytest
from megamind.registry import MegamindRegistry
from megamind.adapters.tower import TowerAdapter
from megamind.adapters.akos import AKOSAdapter

def test_agent_registration():
    registry = MegamindRegistry()
    agent = registry.register_agent(
        agent_id="test_agent",
        name="Test Agent",
        role="Verification Unit",
        pistons=["CORE-THINK", "GHOST"]
    )
    assert agent["agent_id"] == "test_agent"
    assert registry.get_agent("test_agent") == agent

def test_summary():
    registry = MegamindRegistry()
    registry.register_agent("agent_1", "One", "Role 1", ["MICROWAVE"])
    summary = registry.get_summary()
    assert summary["total_registered_agents"] == 1
    assert "agent_1" in summary["agents"]

def test_akos_adapter():
    adapter = AKOSAdapter()
    result = adapter.bind_governance_session("agent_1", "session_123")
    assert result["governance_status"] == "BOUND"
