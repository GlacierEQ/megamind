import pytest
from megamind import MegamindRegistry

def test_registry_seeding():
    registry = MegamindRegistry(seed_defaults=True)
    assert len(registry.agents) == 5
    agent = registry.get_agent("doctor_strange")
    assert agent is not None
    assert agent["name"] == "Doctor Strange (Supreme Orchestrator)"

def test_agent_registration():
    registry = MegamindRegistry(seed_defaults=False)
    agent = registry.register_agent(
        agent_id="test_agent",
        name="Test Agent",
        role="Verification Unit",
        pistons=["CORE-THINK", "GHOST"]
    )
    assert agent["agent_id"] == "test_agent"
    assert len(registry.agents) == 1

def test_summary():
    registry = MegamindRegistry(seed_defaults=False)
    registry.register_agent("agent_1", "One", "Role 1", ["MICROWAVE"])
    summary = registry.get_summary()
    assert summary["total_registered_agents"] == 1
    assert "pistons_matrix" in summary
