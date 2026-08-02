import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

class SecretAlphaMasterEngine:
    """Engine for managing the Secret Alpha & Exceptional Model Master List."""

    def __init__(self, master_list_path: Optional[Path] = None):
        if master_list_path is None:
            master_list_path = Path(__file__).parent.parent.parent / "registry" / "secret_alpha_master_list.yml"
        self.master_list_path = master_list_path
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if self.master_list_path.exists():
            with open(self.master_list_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def get_revealed_aliases(self) -> List[Dict[str, Any]]:
        return self.data.get("revealed_stealth_aliases", [])

    def get_cloaked_releases(self) -> List[Dict[str, Any]]:
        return self.data.get("cloaked_releases", [])

    def get_preservation_targets(self) -> List[Dict[str, Any]]:
        return self.data.get("exceptional_preservation_targets", [])

    def get_internal_stealth_lineages(self) -> List[Dict[str, Any]]:
        return self.data.get("recovered_internal_stealth_lineages", [])

    def get_master_audit_summary(self) -> Dict[str, Any]:
        return {
            "total_revealed_stealth_aliases": len(self.get_revealed_aliases()),
            "total_cloaked_releases": len(self.get_cloaked_releases()),
            "total_preservation_targets": len(self.get_preservation_targets()),
            "total_external_master_records": len(self.get_revealed_aliases()) + len(self.get_cloaked_releases()) + len(self.get_preservation_targets()),
            "total_internal_stealth_lineages": len(self.get_internal_stealth_lineages())
        }
