import pytest
import asyncio
from megamind import MegamindRegistry, AsyncPistonEngine

@pytest.mark.asyncio
async def test_async_parallel_swarm():
    registry = MegamindRegistry()
    engine = AsyncPistonEngine(registry)

    def dummy_task(x):
        return x * 2

    task_specs = [
        {"piston_id": "MICROWAVE", "fn": dummy_task, "args": [10]},
        {"piston_id": "GHOST", "fn": dummy_task, "args": [20]},
        {"piston_id": "SUPERNOVA", "fn": dummy_task, "args": [30]},
    ]

    results = await engine.execute_parallel_swarm(task_specs)
    assert len(results) == 3
    assert results[0]["result"] == 20
    assert results[1]["result"] == 40
    assert results[2]["result"] == 60
