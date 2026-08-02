"""
Megamind: Sovereign Agent Registry & Piston Capability Core
"""

from .registry import MegamindRegistry
from .async_engine import AsyncPistonEngine
from .mesh import AgentMeshConnector
from .acquisition import AgentAcquisitionEngine
from .kernel import MegamindMissionKernel
from .titan import TitanMeshEngine

__version__ = "0.5.0"
__all__ = [
    "MegamindRegistry",
    "AsyncPistonEngine",
    "AgentMeshConnector",
    "AgentAcquisitionEngine",
    "MegamindMissionKernel",
    "TitanMeshEngine"
]
