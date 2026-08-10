from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


class TowerAdapter:
    """Read an explicitly configured local Tower technology-map surface.

    The adapter does not prove a live cross-repository integration. Callers must
    provide ``tower_root`` or set ``MEGAMIND_TOWER_ROOT``. An unconfigured
    adapter fails visibly as unavailable instead of inheriting a workstation-
    specific path.
    """

    def __init__(self, tower_root: Path | str | None = None):
        configured = tower_root or os.getenv("MEGAMIND_TOWER_ROOT")
        self.tower_root = Path(configured).expanduser() if configured else None
        self.megamind_map = (
            self.tower_root / "generated" / "megamind.technology-map.json"
            if self.tower_root is not None
            else None
        )

    def is_available(self) -> bool:
        """Return true only when an explicitly configured Tower root exists."""
        return self.tower_root is not None and self.tower_root.exists()

    def sync_technology_map(self) -> Dict[str, Any]:
        """Read a local generated map, or classify local language directories."""
        if not self.is_available() or self.tower_root is None:
            return {"status": "TOWER_NOT_CONFIGURED_OR_FOUND", "domains": {}}

        if self.megamind_map is not None and self.megamind_map.exists():
            with self.megamind_map.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return {"status": "LOCAL_MAP_READ", "domains": data.get("domains", {})}

        languages_dir = self.tower_root / "languages"
        domains: Dict[str, Dict[str, str]] = {}
        if languages_dir.exists():
            for lang_path in sorted(languages_dir.iterdir()):
                if lang_path.is_dir():
                    domains[lang_path.name] = {
                        "language": lang_path.name,
                        "path": str(lang_path),
                        "status": "LOCAL_DIRECTORY_DISCOVERED",
                    }
        return {"status": "LOCAL_DIRECTORY_SCAN", "domains": domains}
