"""
Lethe: verifiable per-view erasure for graph vector indexes.

Reference implementation accompanying the paper. The public API is:

    from lethe import LetheIndex, LetheConfig
    from lethe.metrics import operational_leakage, drift_at_k, recall_at_k

See the top-level README and ``scripts/`` for end-to-end reproduction.
"""
from .index import LetheIndex, LetheConfig, QueryTrace
from .access import AccessPolicy
from .overlay import BypassOverlay
from .erasure_log import ErasureLog

__all__ = [
    "LetheIndex",
    "LetheConfig",
    "QueryTrace",
    "AccessPolicy",
    "BypassOverlay",
    "ErasureLog",
]

__version__ = "1.0.0"
