import pytest
from megamind import TitanMeshEngine

def test_titan_mesh_engine():
    titan = TitanMeshEngine()
    operators = titan.get_operators()
    assert len(operators) == 9
    op_names = [o["name"] for o in operators]
    assert "Shadow Orchestrator" in op_names
    assert "Ghost Integrator" in op_names
    assert "Phantom Deployer" in op_names
    assert "Wraith Guardian" in op_names
    assert "Specter Analyst" in op_names
    assert "Vapor Synthesizer" in op_names
    assert "Mirage Communicator" in op_names
    assert "Eclipse Validator" in op_names
    assert "Void Optimizer" in op_names

def test_titan_command_layer():
    titan = TitanMeshEngine()
    cmd_layer = titan.get_command_layer()
    assert len(cmd_layer) == 9

def test_titan_continue_routes():
    titan = TitanMeshEngine()
    routes = titan.get_continue_routes()
    assert len(routes) == 4
    route_ids = [r["id"] for r in routes]
    assert "continue-openrouter" in route_ids
    assert "continue-ollama" in route_ids

def test_titan_mission_dispatch():
    titan = TitanMeshEngine()
    res = titan.dispatch_titan_mission("BLACKLINE OMEGA-999 MISSION")
    assert res["status"] == "DISPATCHED"
    assert len(res["active_titan_operators"]) == 9
