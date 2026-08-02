from pathlib import Path
from typing import Dict, Any

class TowerAdapter:
    """Adapter for ingesting technology placement contracts from The Tower of Babel."""

    def __init__(self, tower_root: Path = Path("/Users/kcbflux/the-tower-of-babel")):
        self.tower_root = tower_root
        self.megamind_map = tower_root / "generated" / "megamind.technology-map.json"

    def is_available(self) -> bool:
        """Check if Tower of Babel integration surface is present."""
        return self.megamind_map.exists()

    def sync_technology_map(self) -> Dict[str, Any]:
        """Ingest generated megamind technology map from Tower."""
        if not self.is_available():
            return {"status": "TOWER_NOT_FOUND", "domains": {}}
        import json
        with open(self.megamind_map, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"status": "SYNCHRONIZED", "domains": data.get("domains", {})}
