import json
from pathlib import Path
from typing import Dict, List, Any, Optional

PISTON_TIERS = {
    "Tier-0": ["MICROWAVE", "SUPERNOVA", "CORE-THINK", "BODYBUILDER"],
    "Tier-1": ["SHERLOCK-ALPHA", "SONIC", "GHOST", "PHANTOM"],
    "Tier-2": ["VIPER", "WRAITH", "SPECTER", "SHADOW"]
}

class MegamindRegistry:
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.technology_map: Dict[str, Any] = {}
        self.schema_dir = Path(__file__).parent.parent.parent / "schema"

    def register_agent(
        self,
        agent_id: str,
        name: str,
        role: str,
        pistons: List[str],
        model_preference: str = "gemini-3.6-flash-high"
    ) -> Dict[str, Any]:
        """Register a new sovereign agent definition."""
        agent_def = {
            "agent_id": agent_id,
            "name": name,
            "role": role,
            "pistons": pistons,
            "model_preference": model_preference
        }
        self.agents[agent_id] = agent_def
        return agent_def

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve registered agent specification."""
        return self.agents.get(agent_id)

    def load_technology_map(self, tech_map_path: Path) -> Dict[str, Any]:
        """Load Tower of Babel technology export map."""
        if tech_map_path.exists():
            with open(tech_map_path, "r", encoding="utf-8") as f:
                self.technology_map = json.load(f)
        return self.technology_map

    def get_summary(self) -> Dict[str, Any]:
        """Return operational state summary of Megamind."""
        return {
            "total_registered_agents": len(self.agents),
            "agents": list(self.agents.keys()),
            "pistons_matrix": PISTON_TIERS,
            "technology_domains_loaded": len(self.technology_map.get("domains", {}))
        }
