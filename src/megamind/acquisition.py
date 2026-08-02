import os
import hashlib
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentAcquisitionEngine:
    """Acquisition & Collection Pipeline for Megamind Collectible Agents & Models."""

    def __init__(self, registry_dir: Optional[Path] = None):
        if registry_dir is None:
            registry_dir = Path(__file__).parent.parent.parent / "registry"
        self.registry_dir = registry_dir
        self.agents_file = registry_dir / "collectible_agents.yml"
        self.models_file = registry_dir / "collectible_models.yml"

    def load_agents(self) -> List[Dict[str, Any]]:
        if self.agents_file.exists():
            with open(self.agents_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f).get("collectible_agents", [])
        return []

    def save_agents(self, agents: List[Dict[str, Any]]):
        data = {"version": "1.0.0", "collectible_agents": agents}
        with open(self.agents_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    def mark_acquired(self, artifact_id: str, local_path: str = "", notes: str = "") -> Dict[str, Any]:
        """Update acquisition state of a collectible agent engine to ACQUIRED/VERIFIED."""
        agents = self.load_agents()
        updated_item = None
        for a in agents:
            if a["artifact_id"] == artifact_id:
                a["acquisition_state"] = "acquired"
                if local_path:
                    a["local_path"] = local_path
                if notes:
                    a["acquisition_notes"] = notes
                updated_item = a
                break

        if updated_item:
            self.save_agents(agents)
            return {"status": "SUCCESS", "artifact": updated_item}
        return {"status": "NOT_FOUND", "artifact_id": artifact_id}

    def generate_acquisition_receipt(self, artifact_id: str) -> Dict[str, Any]:
        """Generate formal acquisition receipt record matching GlacierEQ standards."""
        agents = self.load_agents()
        for a in agents:
            if a["artifact_id"] == artifact_id:
                return {
                    "receipt_id": f"REC-{artifact_id.upper()}",
                    "artifact_id": a["artifact_id"],
                    "name": a["name"],
                    "acquisition_state": a.get("acquisition_state", "identified_unacquired"),
                    "upstream_owner": a.get("upstream_owner"),
                    "upstream_repository": a.get("upstream_repository"),
                    "license": a.get("license"),
                    "megamind_role": a.get("megamind_role"),
                    "verification_status": "HARDENED" if a.get("acquisition_state") == "acquired" else "PENDING_ACQUISITION"
                }
        return {"status": "NOT_FOUND"}
