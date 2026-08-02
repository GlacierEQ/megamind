import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class MegamindRegistry:
    """Sovereign Agent Registry managing 12 Pistons Matrix, Stealth organs, and collectible engines."""

    def __init__(self, seed_defaults: bool = True, registry_dir: Optional[Path] = None):
        if registry_dir is None:
            registry_dir = Path(__file__).parent.parent.parent / "registry"
        self.registry_dir = registry_dir
        self.agents: Dict[str, Dict[str, Any]] = {}
        if seed_defaults:
            self._seed_default_agents()

    def _seed_default_agents(self):
        self.agents = {
            "doctor_strange": {
                "agent_id": "doctor_strange",
                "name": "Doctor Strange (Supreme Orchestrator)",
                "pistons": ["MICROWAVE", "SUPERNOVA", "CORE-THINK"],
                "infinity_stones": ["Time Stone", "Mind Stone"],
                "status": "ACTIVE"
            },
            "doc_ock": {
                "agent_id": "doc_ock",
                "name": "Doc Ock (Multi-Armed Mechanical Harness)",
                "pistons": ["BODYBUILDER", "SHERLOCK-ALPHA"],
                "infinity_stones": ["Power Stone", "Space Stone"],
                "status": "ACTIVE"
            },
            "morpheus": {
                "agent_id": "morpheus",
                "name": "Morpheus (Matrix Vision Operator)",
                "pistons": ["SONIC", "GHOST"],
                "infinity_stones": ["Reality Stone"],
                "status": "ACTIVE"
            },
            "sherlock_alpha": {
                "agent_id": "sherlock_alpha",
                "name": "Sherlock Alpha (Forensic & Legal Engine)",
                "pistons": ["PHANTOM", "VIPER"],
                "infinity_stones": ["Soul Stone"],
                "status": "ACTIVE"
            },
            "wraith_specter": {
                "agent_id": "wraith_specter",
                "name": "Wraith Specter (Stealth Audit & Security Core)",
                "pistons": ["WRAITH", "SPECTER", "SHADOW"],
                "infinity_stones": ["Mind Stone", "Space Stone"],
                "status": "ACTIVE"
            }
        }

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return self.agents.get(agent_id)

    def register_agent(self, agent_id: str, name: str, role: str = "", pistons: Optional[List[str]] = None) -> Dict[str, Any]:
        agent = {
            "agent_id": agent_id,
            "name": name,
            "role": role,
            "pistons": pistons or ["CORE-THINK"],
            "status": "ACTIVE"
        }
        self.agents[agent_id] = agent
        return agent

    def load_collectible_agents(self) -> List[Dict[str, Any]]:
        path = self.registry_dir / "collectible_agents.yml"
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            items = []
            for key in ["wave_a_immediate", "wave_b_models_and_training", "wave_c_architectural_enrichment"]:
                items.extend(data.get(key, []))
            return items

    def load_collectible_models(self) -> List[Dict[str, Any]]:
        path = self.registry_dir / "collectible_models.yml"
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("models", [])

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_registered_agents": len(self.agents),
            "pistons_matrix": {
                "RING_-3_HARDWARE_INTEGRATION": ["MICROWAVE", "SUPERNOVA", "CORE-THINK"],
                "MECHANICAL_SWARM_OPERATORS": ["BODYBUILDER", "SHERLOCK-ALPHA", "SONIC"],
                "STEALTH_SURVEILLANCE_LAYER": ["GHOST", "PHANTOM", "VIPER"],
                "RESONANCE_AUDIT_GUARDIANS": ["WRAITH", "SPECTER", "SHADOW"]
            },
            "collectible_agents_count": len(self.load_collectible_agents()),
            "collectible_models_count": len(self.load_collectible_models())
        }
