#!/usr/bin/env python3
"""
run_all.py -- one command to reproduce the artifact.

    python3 scripts/run_all.py            # smoke test + table reproduction
    python3 scripts/run_all.py --full     # also run the canonical experiment

Stage 1 reproduces the paper's headline table numbers from the released CSVs
(fast, no compute). Stage 2 (optional) runs the canonical reference experiment
that re-derives the zombie effect from scratch on synthetic data.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(cmd):
    print(f"\n$ {' '.join(cmd)}\n" + "-" * 60)
    return subprocess.call([sys.executable, *cmd])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--full", action="store_true",
                   help="also run the canonical experiment from scratch")
    args = p.parse_args()

    print("=" * 60)
    print("Lethe artifact -- reproduction driver")
    print("=" * 60)

    print("\n[1/2] Reproducing paper table numbers from released data ...")
    rc = run([str(HERE / "reproduce_tables.py")])
    if rc != 0:
        sys.exit(rc)

    if args.full:
        print("\n[2/2] Running the canonical reference experiment ...")
        run([str(HERE / "zv_reference.py"), "--quick"])
    else:
        print("\n[2/2] Skipped (pass --full to run the canonical experiment).")

    print("\nDone. See README.md for the full reproduction guide.")


if __name__ == "__main__":
    main()
