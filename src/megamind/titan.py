import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class TitanMeshEngine:
    """Primordial Mesh Titan (BLACKLINE OMEGA-999) Engine."""

    def __init__(self, codex_path: Optional[Path] = None):
        if codex_path is None:
            codex_path = Path(__file__).parent.parent.parent / "registry" / "primordial_mesh_titan.yml"
        self.codex_path = codex_path
        self.codex_data = self._load_codex()

    def _load_codex(self) -> Dict[str, Any]:
        if self.codex_path.exists():
            with open(self.codex_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def get_operators(self) -> List[Dict[str, Any]]:
        return self.codex_data.get("titan_stealth_operators", [])

    def get_command_layer(self) -> List[Dict[str, Any]]:
        return self.codex_data.get("mastermind_command_layer", [])

    def get_continue_routes(self) -> List[Dict[str, Any]]:
        return self.codex_data.get("continue_routes", [])

    def dispatch_titan_mission(self, mission_name: str) -> Dict[str, Any]:
        """Dispatch a mission across the Titan Stealth mesh and Command Layer."""
        operators = [op["name"] for op in self.get_operators()]
        command_roles = [c["role"] for c in self.get_command_layer()]

        return {
            "mission_name": mission_name,
            "codex": self.codex_data.get("codex_name"),
            "status": "DISPATCHED",
            "command_layer_roles": command_roles,
            "active_titan_operators": operators,
            "lineage_verification": "VALIDATED"
        }
