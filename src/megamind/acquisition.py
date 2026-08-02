import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentAcquisitionEngine:
    """Engine for acquiring collectible agent bodies, frameworks, and model vault items."""

    def __init__(self, registry_dir: Optional[Path] = None):
        if registry_dir is None:
            registry_dir = Path(__file__).parent.parent.parent / "registry"
        self.registry_dir = registry_dir
        self.collectible_agents_path = self.registry_dir / "collectible_agents.yml"
        self.collectible_models_path = self.registry_dir / "collectible_models.yml"

    def get_collectible_agents(self) -> List[Dict[str, Any]]:
        if not self.collectible_agents_path.exists():
            return []
        with open(self.collectible_agents_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            items = []
            for key in ["wave_a_immediate", "wave_b_models_and_training", "wave_c_architectural_enrichment"]:
                items.extend(data.get(key, []))
            return items

    def get_wave_summary(self) -> Dict[str, Any]:
        if not self.collectible_agents_path.exists():
            return {}
        with open(self.collectible_agents_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return {
                "wave_a_count": len(data.get("wave_a_immediate", [])),
                "wave_b_count": len(data.get("wave_b_models_and_training", [])),
                "wave_c_count": len(data.get("wave_c_architectural_enrichment", [])),
                "total_systems": data.get("total_collectible_systems", 9)
            }

    def mark_acquired(self, artifact_id: str, local_path: str = "", notes: str = "") -> Dict[str, Any]:
        agents = self.get_collectible_agents()
        target = next((a for a in agents if a["artifact_id"] == artifact_id), None)
        if target:
            target["acquisition_state"] = "ACQUIRED"
            if local_path:
                target["local_path"] = local_path
            return {"status": "SUCCESS", "artifact": target}
        return {"status": "NOT_FOUND", "artifact_id": artifact_id}

    def mark_model_acquired(self, artifact_id: str, local_path: str = "") -> Dict[str, Any]:
        return self.mark_acquired(artifact_id, local_path)

    def generate_acquisition_receipt(self, artifact_id: str) -> Dict[str, Any]:
        res = self.mark_acquired(artifact_id)
        if res.get("status") == "SUCCESS":
            art = res["artifact"]
            return {
                "receipt_id": f"REC-ACQ-{artifact_id}",
                "artifact_name": art["name"],
                "acquisition_priority": art.get("acquisition_priority", "Wave A"),
                "megamind_role": art.get("megamind_role"),
                "acquisition_state": "ACQUIRED",
                "verifier": "Megamind Sovereign Acquisition Engine"
            }
        return {"status": "FAILED", "reason": "Artifact not found"}
