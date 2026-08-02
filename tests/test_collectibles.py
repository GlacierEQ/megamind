import pytest
from megamind import MegamindRegistry

def test_load_collectible_agents():
    registry = MegamindRegistry(seed_defaults=False)
    agents = registry.load_collectible_agents()
    assert len(agents) > 0
    wave_a_agents = [a for a in agents if a.get("acquisition_priority") == "Wave A"]
    assert len(wave_a_agents) >= 5

def test_load_collectible_models():
    registry = MegamindRegistry(seed_defaults=False)
    models = registry.load_collectible_models()
    assert isinstance(models, list)
