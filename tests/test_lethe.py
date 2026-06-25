"""
Tests for the Lethe reference implementation.

These check the load-bearing invariants the paper proves:

* Lethe achieves zero operational leakage (revocation-aware traversal).
* A tombstone-style baseline leaks (the zombie effect exists).
* The erasure log is tamper-evident (any edit is detected on replay).
* Crypto-shredding makes a vector inaccessible to everyone.

Run with:  pytest tests/
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lethe import LetheIndex, LetheConfig  # noqa: E402
from lethe.metrics import operational_leakage  # noqa: E402


@pytest.fixture
def data():
    rng = np.random.default_rng(0)
    return rng.standard_normal((2000, 128)).astype("float32")


def _build(data, revocation_aware):
    cfg = LetheConfig(dim=128, k=10, seed=0,
                      revocation_aware=revocation_aware,
                      build_bypass=revocation_aware)
    idx = LetheIndex(cfg).build(data)
    for vid in range(200):
        idx.revoke(vid, "alice")
    return idx


def test_lethe_zero_operational_leakage(data):
    idx = _build(data, revocation_aware=True)
    leaks = [operational_leakage(idx.search(data[q], "alice")[1])
             for q in range(50, 100)]
    assert max(leaks) == 0.0, "Lethe must have zero operational leakage"


def test_tombstone_leaks(data):
    idx = _build(data, revocation_aware=False)
    leaks = [operational_leakage(idx.search(data[q], "alice")[1])
             for q in range(50, 100)]
    assert max(leaks) > 0.0, "tombstone baseline should exhibit the zombie effect"


def test_erasure_log_tamper_evident(data):
    idx = _build(data, revocation_aware=True)
    assert idx.log.verify()
    assert idx.log.tamper_detected_after_edit(0, "vector_id", 999999)


def test_crypto_shred_blocks_access(data):
    idx = _build(data, revocation_aware=True)
    idx.crypto_shred(0)
    assert not idx.access.key_exists(0)
    assert not idx.access.can_access(0, "anyone")


def test_results_exclude_revoked(data):
    idx = _build(data, revocation_aware=True)
    revoked = set(range(200))
    res, _ = idx.search(data[5], "alice", k=10)
    assert not (set(res) & revoked), "a revoked vector must never be returned"
