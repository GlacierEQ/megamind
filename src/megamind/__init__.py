"""
Megamind: Sovereign Agent Registry & Piston Capability Core
"""

from .registry import MegamindRegistry
from .async_engine import AsyncPistonEngine
from .mesh import AgentMeshConnector
from .acquisition import AgentAcquisitionEngine
from .kernel import MegamindMissionKernel
from .titan import TitanMeshEngine
from .scanner import ModelArchaeologyScanner
from .tranche import MegamindRecoveryTranche
from .alpha_master import SecretAlphaMasterEngine
from .authority_half_life import AuthorityHalfLife, AuthorityToken
from .decision_intelligence import DecisionCandidate, DecisionIntelligenceEngine, IntelligentDecision

__version__ = "0.5.0"
__all__ = [
    "MegamindRegistry",
    "AsyncPistonEngine",
    "AgentMeshConnector",
    "AgentAcquisitionEngine",
    "MegamindMissionKernel",
    "TitanMeshEngine",
    "ModelArchaeologyScanner",
    "MegamindRecoveryTranche",
    "SecretAlphaMasterEngine",
    "AuthorityHalfLife",
    "AuthorityToken",
    "DecisionCandidate",
    "DecisionIntelligenceEngine",
    "IntelligentDecision",
]
