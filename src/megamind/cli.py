import sys
import argparse
import json
from pathlib import Path
from .registry import MegamindRegistry
from .mesh import AgentMeshConnector
from .acquisition import AgentAcquisitionEngine
from .kernel import MegamindMissionKernel
from .titan import TitanMeshEngine
from .scanner import ModelArchaeologyScanner
from .tranche import MegamindRecoveryTranche
from .alpha_master import SecretAlphaMasterEngine
from .adapters.tower import TowerAdapter
from .adapters.akos import AKOSAdapter

def main():
    parser = argparse.ArgumentParser(description="Megamind Sovereign Agent Registry & Piston CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Command: status
    status_parser = subparsers.add_parser("status", help="Show Megamind operational state")

    # Command: list-agents
    agents_parser = subparsers.add_parser("list-agents", help="List registered sovereign agents and piston assignments")

    # Command: audit-alpha-models
    alpha_parser = subparsers.add_parser("audit-alpha-models", help="Audit Secret Alpha & Exceptional Model Master List v0.1")

    # Command: alpha-lineage
    lineage_parser = subparsers.add_parser("alpha-lineage", help="List internal prompt-recovered Stealth agent lineages")

    # Command: run-recovery-tranche
    tranche_parser = subparsers.add_parser("run-recovery-tranche", help="Run governed recovery tranche on local orbits (.apex, .continue, .cline, .kilo)")

    # Command: tranche-receipt
    receipt_t_parser = subparsers.add_parser("tranche-receipt", help="Show formal recovery tranche receipt")

    # Command: scan-artifacts
    scan_parser = subparsers.add_parser("scan-artifacts", help="Scan local stores and caches for model weight artifacts")

    # Command: verify-checkpoint
    verify_cp_parser = subparsers.add_parser("verify-checkpoint", help="Advance model artifact through 12-step verification ladder")
    verify_cp_parser.add_argument("path", help="Path to target model file")

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
    scanner = ModelArchaeologyScanner()
    tranche_engine = MegamindRecoveryTranche()
    alpha_engine = SecretAlphaMasterEngine()

    if args.command == "status":
        print("🧠 [MEGAMIND] Sovereign Agent & Piston Registry State:")
        print(json.dumps(registry.get_summary(), indent=2))

    elif args.command == "list-agents":
        print("🤖 [MEGAMIND AGENTS] Registered Sovereign Profiles:")
        for agent_id in registry.agents:
            agent = registry.get_agent(agent_id)
            print(f"  • [{agent['agent_id']:<15}] {agent['name']:<20} | Pistons: {', '.join(agent['pistons'])}")

    elif args.command == "audit-alpha-models":
        print("🕵️‍♂️ [SECRET ALPHA & EXCEPTIONAL MODEL MASTER LIST v0.1]")
        summary = alpha_engine.get_master_audit_summary()
        print(f"Total External Master Records: {summary['total_external_master_records']} (14 Revealed + 7 Cloaked + 6 Preservation Targets)")
        print("\n--- 14 Officially Revealed Stealth Releases ---")
        for r in alpha_engine.get_revealed_aliases():
            print(f"  • [{r['record_id']}] {r['public_alias']:<22} ──► {r['revealed_identity']:<25} ({r['revealed_lab']})")
        print("\n--- 7 Cloaked Releases ---")
        for c in alpha_engine.get_cloaked_releases():
            print(f"  • [{c['record_id']}] {c['public_alias']:<22} | Status: {c['status']}")
        print("\n--- 6 Exceptional Open Preservation Targets ---")
        for p in alpha_engine.get_preservation_targets():
            print(f"  • [{p['record_id']}] {p['name']:<25} | Provider: {p['provider']:<16} | License: {p['license']}")

    elif args.command == "alpha-lineage":
        print("🧬 [INTERNAL STEALTH AGENT LINEAGES (14 RECOVERED)]")
        for line in alpha_engine.get_internal_stealth_lineages():
            print(f"  • [{line['id']:<18}] {line['name']:<25} | Recovery Status: {line['recovery_status']}")

    elif args.command == "run-recovery-tranche":
        print("🛡️ [MEGAMIND RECOVERY TRANCHE] Ingesting & Sanitizing Orbits...")
        orbits = [
            (Path("/Users/kcbflux/.apex"), "APEX_ORBIT"),
            (Path("/Users/kcbflux/.continue"), "CONTINUE_ORBIT"),
            (Path("/Users/kcbflux/.cline"), "CLINE_ORBIT"),
            (Path("/Users/kcbflux/.kilo"), "KILO_ORBIT")
        ]
        for p, name in orbits:
            res = tranche_engine.ingest_local_orbit(p, name)
            print(f"  - Orbit: {res['orbit']:<16} | Files: {res.get('files_count', 0):<4} | Status: {res['status']}")
        receipt = tranche_engine.generate_tranche_receipt()
        print("\n📄 [TRANCHE RECOVERY RECEIPT]")
        print(json.dumps(receipt, indent=2))

    elif args.command == "tranche-receipt":
        receipt = tranche_engine.generate_tranche_receipt()
        print(json.dumps(receipt, indent=2))

    elif args.command == "scan-artifacts":
        print("🔎 [MODEL ARCHAEOLOGY SCANNER] Crawling Local Model Stores & Caches...")
        found = scanner.scan_local_archives()
        print(f"Discovered {len(found)} Model Weight Artifacts:")
        for item in found:
            print(f"  - [{item['format']:<5}] {item['filename']:<35} ({item['size_mb']} MB) | Stage: {item['verification_stage']}")

    elif args.command == "verify-checkpoint":
        res = scanner.advance_verification_ladder(args.path)
        print("🔬 [12-STEP VERIFICATION LADDER]")
        print(json.dumps(res, indent=2))

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
