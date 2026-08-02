import pytest
from megamind import MegamindRegistry

def test_load_collectible_agents():
    registry = MegamindRegistry(seed_defaults=False)
    agents = registry.load_collectible_agents()
    assert len(agents) == 12

def test_load_collectible_models():
    registry = MegamindRegistry(seed_defaults=False)
    models = registry.load_collectible_models()
    assert len(models) == 9
