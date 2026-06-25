"""
Bypass overlay for Lethe (paper Section 5.2 and Appendix C).

When a vector is revoked from a view, removing it from traversal can leave the
authorized subgraph poorly navigable: greedy search may no longer reach the
neighbors that lay *beyond* the revoked node. The bypass overlay repairs this
by adding shortcut edges among the revoked node's authorized neighbors, so an
authorized search routes *around* the revoked node without losing recall.

The overlay is shared across all principals that have the same *effective
view* (the same set of visible vectors), so its size is bounded by the number
of (vector, view-class) repairs rather than by the user population. This is
the property measured in the paper's memory and ablation tables.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BypassOverlay:
    """Shortcut edges added to preserve navigability after revocation."""

    edges: dict[int, set[int]] = field(default_factory=dict)
    _n_repairs: int = 0

    def repair(self, neighbors: list[int], revoked_vector: int) -> None:
        """Add bypass edges among ``neighbors`` of ``revoked_vector``.

        The reference repair connects the authorized neighbors of the revoked
        node into a small clique-like shortcut set, restoring the routes that
        previously passed through the revoked node. Pruning (paper: pruned vs.
        unpruned bypass ablation) would keep only a subset of these edges.
        """
        for a in neighbors:
            for b in neighbors:
                if a != b:
                    self.edges.setdefault(a, set()).add(b)
        self._n_repairs += 1

    def neighbors(self, vector_id: int) -> set[int]:
        return self.edges.get(vector_id, set())

    @property
    def n_edges(self) -> int:
        return sum(len(v) for v in self.edges.values())

    @property
    def n_repairs(self) -> int:
        return self._n_repairs

    def size_bytes(self, bytes_per_edge: int = 8) -> int:
        """Approximate overlay memory: one machine word per directed edge."""
        return self.n_edges * bytes_per_edge
