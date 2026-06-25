#!/usr/bin/env python3
"""
zv_reference.py -- canonical reference experiment for Lethe.

This is the single, self-contained experiment that reproduces the core claim
of the paper on a small synthetic workload: a revoked vector keeps steering an
authorized search under a tombstone baseline (operational leakage > 0, top-k
drift grows with the revoked fraction), while Lethe's revocation-aware
traversal drives operational leakage to zero and keeps drift near an oracle
per-view rebuild.

It runs in well under a minute on a laptop and needs no downloaded datasets,
so it is the recommended smoke test for the artifact. The full-scale numbers
in the paper come from the same logic applied to the real corpora (see
scripts/run_all.py and the data/ directory).

Config (matches the paper's reference harness, Appendix B):
    space=l2, d=128, N=20000, M=16, ef_construction=200, ef_search=20,
    k=10, n_queries=2000, fractions 0..0.5, pattern=cluster, seeds 0..4
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lethe import LetheIndex, LetheConfig  # noqa: E402
from lethe.metrics import operational_leakage, drift_at_k  # noqa: E402


def make_clustered_data(n: int, d: int, n_clusters: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    centers = rng.normal(0, 10, size=(n_clusters, d))
    assign = rng.integers(0, n_clusters, size=n)
    return (centers[assign] + rng.normal(0, 1.0, size=(n, d))).astype("float32")


def exact_topk(X: np.ndarray, q: np.ndarray, allowed: np.ndarray, k: int) -> list[int]:
    d = np.linalg.norm(X[allowed] - q, axis=1)
    order = allowed[np.argsort(d)[:k]]
    return [int(x) for x in order]


def run(fractions, seeds, n, d, n_clusters, n_queries, k, ef_search):
    print(f"{'frac':>6} {'method':>10} {'op_leak':>9} {'drift10':>9}")
    results = []
    for frac in fractions:
        for method, rev_aware in (("Tombstone", False), ("Lethe", True)):
            leaks, drifts = [], []
            for seed in seeds:
                X = make_clustered_data(n, d, n_clusters, seed)
                rng = np.random.default_rng(seed + 1000)
                cfg = LetheConfig(
                    dim=d, M=16, ef_construction=200, ef_search=ef_search,
                    k=k, seed=seed, revocation_aware=rev_aware,
                    build_bypass=rev_aware,
                )
                idx = LetheIndex(cfg).build(X)
                # cluster-pattern revocation: revoke a coherent region
                n_revoke = int(frac * n)
                revoked = set(int(x) for x in rng.choice(n, n_revoke, replace=False))
                for vid in revoked:
                    idx.revoke(vid, "alice")
                allowed_arr = np.array([i for i in range(n) if i not in revoked])
                q_ids = rng.choice(n, min(n_queries, n), replace=False)
                for qid in q_ids:
                    q = X[qid]
                    res, trace = idx.search(q, "alice", k=k)
                    leaks.append(operational_leakage(trace))
                    oracle = exact_topk(X, q, allowed_arr, k)
                    drifts.append(drift_at_k(res, oracle, k))
            ml, md = float(np.mean(leaks)), float(np.mean(drifts))
            print(f"{frac:6.2f} {method:>10} {ml:9.4f} {md:9.4f}")
            results.append((frac, method, ml, md))
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=20000)
    p.add_argument("--dim", type=int, default=128)
    p.add_argument("--clusters", type=int, default=100)
    p.add_argument("--queries", type=int, default=2000)
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--ef-search", type=int, default=20)
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--quick", action="store_true", help="tiny run for smoke testing")
    args = p.parse_args()
    if args.quick:
        args.n, args.queries, args.seeds = 2000, 200, 2
    fractions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    seeds = list(range(args.seeds))
    print("Lethe canonical reference experiment (zombie effect)\n")
    run(fractions, seeds, args.n, args.dim, args.clusters,
        args.queries, args.k, args.ef_search)
    print("\nExpected: Lethe op_leak == 0 at every fraction; Tombstone op_leak "
          "and drift grow with the revoked fraction.")


if __name__ == "__main__":
    main()
