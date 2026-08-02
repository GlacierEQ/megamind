import sys
import argparse
import json
from .registry import MegamindRegistry
from .mesh import AgentMeshConnector
from .acquisition import AgentAcquisitionEngine
from .kernel import MegamindMissionKernel
from .titan import TitanMeshEngine
from .adapters.tower import TowerAdapter
from .adapters.akos import AKOSAdapter

def main():
    parser = argparse.ArgumentParser(description="Megamind Sovereign Agent Registry & Piston CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Command: status
    status_parser = subparsers.add_parser("status", help="Show Megamind operational state")

    # Command: list-agents
    agents_parser = subparsers.add_parser("list-agents", help="List registered sovereign agents and piston assignments")

    # Command: titan-mesh
    titan_parser = subparsers.add_parser("titan-mesh", help="Show Primordial Mesh Titan BLACKLINE OMEGA-999 codex state")

    # Command: audit-titan
    audit_titan_parser = subparsers.add_parser("audit-titan", help="Audit Titan Stealth operators and Mastermind command layer")

    # Command: connect-mesh
    connect_parser = subparsers.add_parser("connect-mesh", help="Auto-connect sovereign agents into an APEX multi-agent mesh")

    # Command: list-connections
    list_conn_parser = subparsers.add_parser("list-connections", help="List active inter-agent channels and connections")

    # Command: run-mission
    mission_parser = subparsers.add_parser("run-mission", help="Execute complete vertical slice Voice Memory Mission")
    mission_parser.add_argument("--transcript", default="Voice memo recording sample", help="Simulated audio transcript")

    # Command: list-collectibles
    collectibles_parser = subparsers.add_parser("list-collectibles", help="List collectible agent engines and model bodies")

    # Command: acquire
    acquire_parser = subparsers.add_parser("acquire", help="Mark a collectible agent engine as ACQUIRED")
    acquire_parser.add_argument("artifact_id", help="ID of collectible artifact")
    acquire_parser.add_argument("--path", default="", help="Local storage path")
    acquire_parser.add_argument("--notes", default="", help="Acquisition notes")

    # Command: acquire-model
    acquire_model_parser = subparsers.add_parser("acquire-model", help="Mark a collectible model body as ACQUIRED in Model Vault")
    acquire_model_parser.add_argument("artifact_id", help="ID of model body artifact")
    acquire_model_parser.add_argument("--path", default="", help="Local checkpoint storage path")

    # Command: receipt
    receipt_parser = subparsers.add_parser("receipt", help="Generate formal acquisition receipt for artifact")
    receipt_parser.add_argument("artifact_id", help="ID of collectible artifact")

    # Command: audit-models
    audit_parser = subparsers.add_parser("audit-models", help="Audit model vault bodies and acquisition states")

    # Command: sync-tower
    sync_parser = subparsers.add_parser("sync-tower", help="Sync technology map with Tower of Babel")

    # Command: list-pistons
    pistons_parser = subparsers.add_parser("list-pistons", help="List 12 Pistons Matrix")

    args = parser.parse_args()

    registry = MegamindRegistry(seed_defaults=True)
    connector = AgentMeshConnector(registry)
    acquirer = AgentAcquisitionEngine()
    kernel = MegamindMissionKernel(registry)
    titan = TitanMeshEngine()

    if args.command == "status":
        print("🧠 [MEGAMIND] Sovereign Agent & Piston Registry State:")
        print(json.dumps(registry.get_summary(), indent=2))

    elif args.command == "list-agents":
        print("🤖 [MEGAMIND AGENTS] Registered Sovereign Profiles:")
        for agent_id in registry.agents:
            agent = registry.get_agent(agent_id)
            print(f"  • [{agent['agent_id']:<15}] {agent['name']:<20} | Pistons: {', '.join(agent['pistons'])}")

    elif args.command == "titan-mesh":
        print("🏛️ [PRIMORDIAL MESH TITAN] Codex BLACKLINE OMEGA-999:")
        print(json.dumps(titan.codex_data, indent=2))

    elif args.command == "audit-titan":
        print("⚔️ [TITAN STEALTH OPERATORS & COMMAND LAYER AUDIT]")
        print(f"Codex Name: {titan.codex_data.get('codex_name')}")
        print(f"Recovery Status: {titan.codex_data.get('recovery_status')}")
        print("\n--- 9 Titan Stealth Operators ---")
        for op in titan.get_operators():
            derived = f"(Derived from {op['derived_from']})" if op.get("derived_from") else "(Titan Specialist)"
            print(f"  • {op['name']:<22} | Role: {op['role']:<38} | {derived}")
        print("\n--- Mastermind Command Layer (9 Roles) ---")
        for c in titan.get_command_layer():
            print(f"  - Command Role: {c['role']}")
        print("\n--- Continue Routes ---")
        for r in titan.get_continue_routes():
            print(f"  - Route: {r['id']:<30} | Locality: {r['locality']}")

    elif args.command == "connect-mesh":
        conns = connector.auto_connect_swarm()
        print(f"🔗 [MEGAMIND MESH] Connected {len(conns)} Sovereign Agent Channels:")
        for c in conns:
            print(f"  • {c['source']:<15} ──[{c['channel']}]──► {c['target']}")

    elif args.command == "list-connections":
        conns = connector.auto_connect_swarm()
        print("🌐 [ACTIVE INTER-AGENT CHANNELS]")
        for channel, members in connector.channels.items():
            print(f"  • Channel [{channel}]: {', '.join(members)}")

    elif args.command == "run-mission":
        print("🚀 [MEGAMIND MISSION KERNEL] Executing Voice Memory Mission...")
        res = kernel.execute_voice_memory_mission("/tmp/sample_audio.wav", simulated_transcript=args.transcript)
        print(json.dumps(res, indent=2))

    elif args.command == "list-collectibles":
        print("🏆 [MEGAMIND COLLECTIBLE ENGINES & MODELS]")
        print("\n--- Agent Engines & Frameworks ---")
        agents = registry.load_collectible_agents()
        for item in agents:
            print(f"  • [{item['acquisition_priority']}] {item['name']:<30} | {item['acquisition_state']:<22} | Role: {item['megamind_role']}")
        print("\n--- Downloadable Model Bodies ---")
        models = registry.load_collectible_models()
        for item in models:
            print(f"  • [{item['acquisition_priority']}] {item['name']:<35} | {item['acquisition_state']:<22} | Params: {item['parameter_count']}")

    elif args.command == "acquire":
        res = acquirer.mark_acquired(args.artifact_id, local_path=args.path, notes=args.notes)
        if res.get("status") == "SUCCESS":
            art = res["artifact"]
            print(f"✅ [MEGAMIND AGENT ACQUISITION] Successfully acquired: {art['name']} ({art['artifact_id']})")
        else:
            print(f"❌ [MEGAMIND ACQUISITION] Failed to acquire artifact: {args.artifact_id}")

    elif args.command == "acquire-model":
        res = acquirer.mark_model_acquired(args.artifact_id, local_path=args.path)
        if res.get("status") == "SUCCESS":
            art = res["artifact"]
            print(f"💎 [MEGAMIND MODEL VAULT ACQUISITION] Successfully acquired model: {art['name']} ({art['artifact_id']})")
        else:
            print(f"❌ [MEGAMIND ACQUISITION] Failed to acquire model artifact: {args.artifact_id}")

    elif args.command == "receipt":
        rec = acquirer.generate_acquisition_receipt(args.artifact_id)
        print("📄 [MEGAMIND ACQUISITION RECEIPT]")
        print(json.dumps(rec, indent=2))

    elif args.command == "audit-models":
        print("🔍 [MEGAMIND MODEL VAULT AUDIT]")
        models = registry.load_collectible_models()
        print(f"Total Collectible Model Families: {len(models)}")
        p0_models = [m for m in models if m.get("acquisition_priority") == "P0"]
        print(f"P0 Priority Models: {len(p0_models)}")
        for m in models:
            print(f"  - {m['name']} ({m['parameter_count']}) -> License: {m['license']} | State: {m.get('acquisition_state')}")

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
