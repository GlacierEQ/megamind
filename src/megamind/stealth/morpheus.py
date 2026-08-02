from typing import Dict, List, Any

ALLOWED_STATES = ["available", "installed", "active", "hibernated", "removed"]

class StealthMorpheus:
    """Stealth Morpheus Organ: Capability Pack Lifecycle State Engine."""

    def __init__(self):
        self.pack_states: Dict[str, str] = {}
        self.use_counts: Dict[str, int] = {}

    def get_state(self, pack_id: str) -> str:
        return self.pack_states.get(pack_id, "available")

    def transition_state(self, pack_id: str, target_state: str) -> Dict[str, Any]:
        """Transition capability pack lifecycle state with validation."""
        if target_state not in ALLOWED_STATES:
            return {
                "pack_id": pack_id,
                "status": "INVALID_STATE",
                "error": f"State {target_state} not in allowed lifecycle states"
            }

        current = self.get_state(pack_id)
        self.pack_states[pack_id] = target_state
        self.use_counts[pack_id] = self.use_counts.get(pack_id, 0) + 1

        return {
            "pack_id": pack_id,
            "previous_state": current,
            "current_state": target_state,
            "use_count": self.use_counts[pack_id],
            "status": "TRANSITIONED"
        }
