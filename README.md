# Megamind

**Local agent registry, schema, capability-taxonomy, and orchestration reference toolkit.**

`megamind` provides a Python package for registering agent records, loading repository-owned YAML registries, validating/working with local schemas, and exercising local orchestration/reference mechanisms.

It does **not** establish that every named agent, piston, sibling repository, model provider, connector, or hardware target is live, deployed, connected, or externally authorized.

## Verified repository surfaces

- [`src/megamind/registry.py`](src/megamind/registry.py) — in-memory agent registration plus YAML registry loading.
- [`schema/`](schema/) — JSON schemas for agents, pistons, technology maps, and collectible records.
- [`registry/`](registry/) — repository-owned YAML configuration/reference data.
- [`src/megamind/`](src/megamind/) — local registry, kernel, mesh, acquisition, scanner, tranche, async, and adapter code.
- [`tests/`](tests/) — repository-local regression tests.
- [`src/megamind/adapters/tower.py`](src/megamind/adapters/tower.py) — optional local-file adapter that requires an explicit path or `MEGAMIND_TOWER_ROOT`; no workstation path or live sibling integration is assumed.

## Quickstart

```python
from megamind import MegamindRegistry

registry = MegamindRegistry(seed_defaults=False)
registry.register_agent(
    agent_id="verification_unit",
    name="Verification Unit",
    role="Repository-local verification",
    pistons=["CORE-THINK"],
)

print(registry.get_summary())
```

The built-in default agent/piston names are taxonomy/reference labels used by the local registry. Labels such as `HARDWARE`, `STEALTH`, or named fictional roles are **not evidence of hardware operation, surveillance, autonomous authority, or production deployment**.

## Optional Tower adapter

```python
from pathlib import Path
from megamind.adapters.tower import TowerAdapter

adapter = TowerAdapter(Path("/path/to/the-tower-of-babel"))
result = adapter.sync_technology_map()
```

The adapter only reads an explicitly configured local directory. A repository link or local map read does not prove runtime connectivity between Megamind and another repository.

## Native proof

```bash
python -m pip install -e ".[dev]"
pytest -q
```

The Public Truth Gate runs the complete test suite on Python 3.11 and 3.13, validates package/version identity, parses repository YAML, validates JSON schema syntax, and binds pull-request proof to the exact source head and base ancestry.

## Evidence boundary

This public repository does **not** claim:

- live operation of a GlacierEQ-wide agent fleet;
- production control over sibling repositories;
- automatic availability of Tower, AKOS, Pro-Mastermind, model providers, MCP servers, or external connectors;
- hardware integration from piston/taxonomy labels;
- provider credentials, proprietary access, or external authority;
- that configuration files named `secret`, `stealth`, or similar contain privileged external access merely because of their names.

Sibling repositories can be architecture references or separately verified capability donors. Their state must be established by their own current proof.

## Version

Package metadata and `megamind.__version__` are both `0.5.0`.

## License

MIT © GlacierEQ
