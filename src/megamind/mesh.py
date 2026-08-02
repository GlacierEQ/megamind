from typing import Dict, List, Any, Optional
import asyncio
from .registry import MegamindRegistry

class AgentMeshConnector:
    """Inter-Agent Connection & Communication Mesh for Sovereign Agents."""

    def __init__(self, registry: MegamindRegistry):
        self.registry = registry
        self.connections: List[Dict[str, Any]] = []
        self.channels: Dict[str, List[str]] = {}

    def connect(self, source_agent_id: str, target_agent_id: str, channel: str = "default") -> Dict[str, Any]:
        """Establish a direct communication channel between two agents."""
        conn = {
            "source": source_agent_id,
            "target": target_agent_id,
            "channel": channel,
            "status": "CONNECTED"
        }
        self.connections.append(conn)
        if channel not in self.channels:
            self.channels[channel] = []
        if source_agent_id not in self.channels[channel]:
            self.channels[channel].append(source_agent_id)
        if target_agent_id not in self.channels[channel]:
            self.channels[channel].append(target_agent_id)
        return conn

    def auto_connect_swarm(self) -> List[Dict[str, Any]]:
        """Automatically connect core sovereign agents into a unified APEX mesh topology."""
        agents = list(self.registry.agents.keys())
        connections_made = []

        # Connect Router (doctor_strange) to Executor (doc_ock)
        if "doctor_strange" in agents and "doc_ock" in agents:
            connections_made.append(self.connect("doctor_strange", "doc_ock", "mission_dispatch"))

        # Connect Executor (doc_ock) to Auditor (sherlock_alpha)
        if "doc_ock" in agents and "sherlock_alpha" in agents:
            connections_made.append(self.connect("doc_ock", "sherlock_alpha", "audit_verification"))

        # Connect Router (doctor_strange) to Evolver (morpheus)
        if "doctor_strange" in agents and "morpheus" in agents:
            connections_made.append(self.connect("doctor_strange", "morpheus", "intent_feedback"))

        # Connect Executor (doc_ock) to GUI Volatile (wraith_specter)
        if "doc_ock" in agents and "wraith_specter" in agents:
            connections_made.append(self.connect("doc_ock", "wraith_specter", "gui_execution"))

        return connections_made

    def dispatch_event(self, channel: str, sender_id: str, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Broadcast an event payload across a connected mesh channel."""
        recipients = [agent for agent in self.channels.get(channel, []) if agent != sender_id]
        return {
            "channel": channel,
            "sender": sender_id,
            "recipients": recipients,
            "payload": event_payload,
            "delivery_status": "DELIVERED"
        }
