import pytest
from megamind.registry import MegamindRegistry

def test_load_collectible_agents():
    registry = MegamindRegistry(seed_defaults=False)
    agents = registry.load_collectible_agents()
    assert len(agents) > 0
    p0_agents = [a for a in agents if a["acquisition_priority"] == "P0"]
    assert len(p0_agents) >= 5
    agent_ids = [a["artifact_id"] for a in agents]
    assert "deer-flow-2.0" in agent_ids
    assert "agent-s3" in agent_ids
    assert "open-autoglm" in agent_ids

def test_load_collectible_models():
    registry = MegamindRegistry(seed_defaults=False)
    models = registry.load_collectible_models()
    assert len(models) > 0
    model_ids = [m["artifact_id"] for m in models]
    assert "fara-1.5-family" in model_ids
    assert "ui-tars-1.5-7b" in model_ids
    assert "os-atlas-family" in model_ids
    assert "scalecua-family" in model_ids
    assert "deepresearcher-7b" in model_ids
