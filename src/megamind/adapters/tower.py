from pathlib import Path
from typing import Dict, Any

class TowerAdapter:
    """Adapter for ingesting technology placement contracts from The Tower of Babel."""

    def __init__(self, tower_root: Path = Path("/Users/kcbflux/GlacierEQ_Swarm/the-tower-of-babel")):
        self.tower_root = Path(tower_root)
        self.megamind_map = self.tower_root / "generated" / "megamind.technology-map.json"

    def is_available(self) -> bool:
        """Check if Tower of Babel integration surface is present."""
        return self.tower_root.exists()

    def sync_technology_map(self) -> Dict[str, Any]:
        """Ingest generated megamind technology map or scan languages directory."""
        if not self.is_available():
            return {"status": "TOWER_NOT_FOUND", "domains": {}}

        import json
        if self.megamind_map.exists():
            with open(self.megamind_map, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {"status": "SYNCHRONIZED", "domains": data.get("domains", {})}

        languages_dir = self.tower_root / "languages"
        domains = {}
        if languages_dir.exists():
            for lang_path in sorted(languages_dir.iterdir()):
                if lang_path.is_dir():
                    domains[lang_path.name] = {
                        "language": lang_path.name,
                        "path": str(lang_path),
                        "status": "OPERATIONAL"
                    }
        return {"status": "AUTO_DISCOVERED", "domains": domains}
