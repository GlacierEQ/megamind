import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import jsonschema

PISTON_TIERS = {
    "Tier-0": ["MICROWAVE", "SUPERNOVA", "CORE-THINK", "BODYBUILDER"],
    "Tier-1": ["SHERLOCK-ALPHA", "SONIC", "GHOST", "PHANTOM"],
    "Tier-2": ["VIPER", "WRAITH", "SPECTER", "SHADOW"]
}

DEFAULT_AGENTS = [
    {
        "agent_id": "doctor_strange",
        "name": "Doctor Strange",
        "role": "Environmental Harmonics & Multiversal Router",
        "pistons": ["CORE-THINK", "SPECTER"],
        "model_preference": "gemini-3.6-flash-high"
    },
    {
        "agent_id": "doc_ock",
        "name": "Doc Ock",
        "role": "Multi-Armed Piston Fusion & Execution Engine",
        "pistons": ["MICROWAVE", "SUPERNOVA", "VIPER"],
        "model_preference": "gemini-3.6-flash-high"
    },
    {
        "agent_id": "morpheus",
        "name": "Morpheus",
        "role": "Behavioral Evolution & Intent Mapping Engine",
        "pistons": ["PHANTOM", "GHOST", "SHADOW"],
        "model_preference": "gemini-3.6-flash-high"
    },
    {
        "agent_id": "sherlock_alpha",
        "name": "Sherlock Alpha",
        "role": "Forensic Intelligence & Proof-of-Delay Audit",
        "pistons": ["SHERLOCK-ALPHA", "BODYBUILDER"],
        "model_preference": "gemini-3.6-flash-high"
    },
    {
        "agent_id": "wraith_specter",
        "name": "Wraith Specter",
        "role": "Memory-Mapped UI & Volatile Execution",
        "pistons": ["WRAITH", "SONIC"],
        "model_preference": "gemini-3.6-flash-high"
    }
]

class MegamindRegistry:
    def __init__(self, seed_defaults: bool = True):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.technology_map: Dict[str, Any] = {}
        self.schema_dir = Path(__file__).parent.parent.parent / "schema"

        if seed_defaults:
            self.load_default_agents()

    def load_default_agents(self):
        """Seed registry with standard 5 sovereign agents covering all 12 Pistons."""
        for agent in DEFAULT_AGENTS:
            self.register_agent(**agent)

    def validate_agent(self, agent_def: Dict[str, Any]) -> bool:
        """Validate agent definition against JSON schema."""
        schema_path = self.schema_dir / "agent.schema.json"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            jsonschema.validate(instance=agent_def, schema=schema)
        return True

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
        self.validate_agent(agent_def)
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
