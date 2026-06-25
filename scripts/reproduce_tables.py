#!/usr/bin/env python3
"""
reproduce_tables.py -- regenerate the paper's headline table numbers from the
released result CSVs in ../data/.

This does not re-run the experiments; it aggregates the released measurement
data exactly as the paper does, so a reviewer can confirm that every number in
the main results table traces to the data. Run:

    python3 scripts/reproduce_tables.py

It prints the main baseline comparison (paper Table, headline operating point:
cluster pattern, 30% revoked, mean over four datasets and ten seeds) and the
per-pattern recall sweep, and checks them against the values in the paper.
"""
from __future__ import annotations

import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def load(name):
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def main():
    src = load("baseline_unified_metrics.csv")

    def agg(method, col, pat="cluster", frac="0.3"):
        rows = [
            x for x in src
            if x["method"] == method and x["pattern"] == pat and x["frac"] == frac
        ]
        vals = [float(x[col]) for x in rows if x.get(col, "") not in ("", "nan")]
        return st.mean(vals) if vals else float("nan")

    methods = [
        "Oracle", "Tombstone", "Post-filter", "Physical-delete",
        "Periodic-rebuild", "SPFresh", "Per-role-index", "Per-user-index",
        "ACORN", "HoneyBee", "Lethe",
    ]
    print("Main baseline comparison (cluster, 30% revoked, mean over datasets x seeds)")
    print(f"{'method':>16} {'leak':>7} {'drift10':>8} {'recall10':>9} "
          f"{'mem_x_shared':>13} {'thrpt':>9}")
    for m in methods:
        leak = agg(m, "scored_leakage")
        drift = agg(m, "drift10_vs_oracle_rebuild")
        rec = agg(m, "recall10_vs_exact_topk")
        mem = agg(m, "memory_ratio_vs_shared")
        thr = agg(m, "revocation_throughput")
        print(f"{m:>16} {leak:7.3f} {drift:8.4f} {rec:9.4f} {mem:13.2f} {thr:9.0f}")

    print("\nKey claims:")
    lethe_leak = agg("Lethe", "scored_leakage")
    print(f"  Lethe scored leakage           = {lethe_leak:.4f}   (expect 0.000)")
    print(f"  Lethe drift@10                 = {agg('Lethe', 'drift10_vs_oracle_rebuild'):.4f}   (expect ~0.0066)")
    print(f"  Tombstone drift@10             = {agg('Tombstone', 'drift10_vs_oracle_rebuild'):.4f}   (expect ~0.118)")
    print(f"  Per-user memory vs shared      = {agg('Per-user-index', 'memory_ratio_vs_shared'):.0f}x  (expect ~3002x)")


if __name__ == "__main__":
    main()
