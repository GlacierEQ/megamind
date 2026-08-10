from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from jsonschema import ValidationError
from jsonschema.validators import validator_for


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
        """Return true only when an explicitly configured Tower root is a directory."""
        return self.tower_root is not None and self.tower_root.is_dir()

    @staticmethod
    def _technology_map_schema() -> Dict[str, Any]:
        repository_root = Path(__file__).resolve().parents[3]
        schema_path = repository_root / "schema" / "technology-map.schema.json"
        with schema_path.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        if not isinstance(schema, dict):
            raise ValueError("technology-map schema must be a JSON object")
        return schema

    def sync_technology_map(self) -> Dict[str, Any]:
        """Read a validated local generated map, or classify local language directories."""
        if not self.is_available() or self.tower_root is None:
            return {"status": "TOWER_NOT_CONFIGURED_OR_FOUND", "domains": {}}

        if self.megamind_map is not None and self.megamind_map.exists():
            try:
                with self.megamind_map.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if not isinstance(data, dict):
                    raise ValueError("technology map must be a JSON object")
                schema = self._technology_map_schema()
                validator = validator_for(schema)(schema)
                validator.validate(data)
                domains = data.get("domains")
                if not isinstance(domains, dict):
                    raise ValueError("technology map domains must be an object")
            except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
                return {
                    "status": "INVALID_LOCAL_MAP",
                    "domains": {},
                    "error": str(exc),
                }
            return {"status": "LOCAL_MAP_READ", "domains": domains}

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
