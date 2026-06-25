"""
Evaluation metrics for Lethe (paper Section 4 and Section 7).

These are the quantities reported throughout the paper:

* operational_leakage: the fraction of traversal events (score / insert /
  expand) that touch a revoked vector. Zero for Lethe by construction; large
  for tombstone- and post-filter-style baselines (the "zombie" effect).
* result_leakage: the fraction of a returned top-k that are revoked vectors.
  Zero by construction for any method that filters results.
* drift10: the fraction of the authorized top-10 that differs from an oracle
  per-view rebuild (lower is better).
* recall10: Recall@10 against the exact authorized top-k (higher is better).
"""
from __future__ import annotations

from typing import Iterable, Sequence

from .index import QueryTrace


def operational_leakage(trace: QueryTrace) -> float:
    """Fraction of traversal events that distance-score, insert, or expand a
    revoked vector (paper Section 4)."""
    total = trace.distance_scored + trace.frontier_inserted + trace.expanded
    if total == 0:
        return 0.0
    revoked = (
        trace.distance_scored_revoked
        + trace.frontier_inserted_revoked
        + trace.expanded_revoked
    )
    return revoked / total


def result_leakage(results: Sequence[int], revoked_ids: set[int]) -> float:
    """Fraction of the returned list that are revoked vectors."""
    if not results:
        return 0.0
    return sum(1 for r in results if r in revoked_ids) / len(results)


def drift_at_k(
    method_topk: Sequence[int], oracle_topk: Sequence[int], k: int = 10
) -> float:
    """Top-k drift: 1 - |intersection| / k versus the oracle rebuild."""
    a = set(method_topk[:k])
    b = set(oracle_topk[:k])
    if not b:
        return 0.0
    return 1.0 - len(a & b) / k


def recall_at_k(
    method_topk: Sequence[int], exact_topk: Sequence[int], k: int = 10
) -> float:
    """Recall@k against the exact authorized nearest neighbors."""
    a = set(method_topk[:k])
    b = set(exact_topk[:k])
    if not b:
        return 0.0
    return len(a & b) / len(b)
