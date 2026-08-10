from __future__ import annotations

from pathlib import Path

import megamind
from megamind.adapters.tower import TowerAdapter

ROOT = Path(__file__).resolve().parents[1]


def test_package_version_matches_project_metadata() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.5.0"' in pyproject
    assert megamind.__version__ == "0.5.0"


def test_tower_adapter_has_no_implicit_workstation_path(monkeypatch) -> None:
    monkeypatch.delenv("MEGAMIND_TOWER_ROOT", raising=False)
    adapter = TowerAdapter()
    assert adapter.tower_root is None
    assert adapter.sync_technology_map() == {
        "status": "TOWER_NOT_CONFIGURED_OR_FOUND",
        "domains": {},
    }


def test_tower_adapter_reads_only_explicit_local_root(tmp_path: Path) -> None:
    generated = tmp_path / "generated"
    generated.mkdir()
    (generated / "megamind.technology-map.json").write_text(
        '{"domains":{"python":{"language":"python"}}}', encoding="utf-8"
    )
    adapter = TowerAdapter(tmp_path)
    result = adapter.sync_technology_map()
    assert result["status"] == "LOCAL_MAP_READ"
    assert result["domains"]["python"]["language"] == "python"


def test_readme_keeps_integration_claims_bounded() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "does **not** establish" in readme
    assert "no workstation path or live sibling integration is assumed" in readme
    assert "/Users/kcbflux/" not in readme
