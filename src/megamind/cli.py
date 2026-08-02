import sys
import argparse
import json
from .registry import MegamindRegistry
from .adapters.tower import TowerAdapter
from .adapters.akos import AKOSAdapter

def main():
    parser = argparse.ArgumentParser(description="Megamind Sovereign Agent Registry & Piston CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Command: status
    status_parser = subparsers.add_parser("status", help="Show Megamind operational state")

    # Command: list-agents
    agents_parser = subparsers.add_parser("list-agents", help="List registered sovereign agents and piston assignments")

    # Command: sync-tower
    sync_parser = subparsers.add_parser("sync-tower", help="Sync technology map with Tower of Babel")

    # Command: list-pistons
    pistons_parser = subparsers.add_parser("list-pistons", help="List 12 Pistons Matrix")

    args = parser.parse_args()

    registry = MegamindRegistry(seed_defaults=True)

    if args.command == "status":
        print("🧠 [MEGAMIND] Sovereign Agent & Piston Registry State:")
        print(json.dumps(registry.get_summary(), indent=2))

    elif args.command == "list-agents":
        print("🤖 [MEGAMIND AGENTS] Registered Sovereign Profiles:")
        for agent_id in registry.agents:
            agent = registry.get_agent(agent_id)
            print(f"  • [{agent['agent_id']:<15}] {agent['name']:<20} | Pistons: {', '.join(agent['pistons'])}")

    elif args.command == "sync-tower":
        adapter = TowerAdapter()
        res = adapter.sync_technology_map()
        print(f"🏗️ [TOWER ADAPTER] Sync Status: {res.get('status')}")
        print(f"Total Discovered Language Domains: {len(res.get('domains', {}))}")
        for domain, details in list(res.get("domains", {}).items()):
            print(f"  - Domain: {domain:<12} | Status: {details.get('status')}")

    elif args.command == "list-pistons":
        print("⚡ [12 PISTONS MATRIX] Capability Tiers:")
        for tier, pistons in registry.get_summary()["pistons_matrix"].items():
            print(f"  [{tier}]: {', '.join(pistons)}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
