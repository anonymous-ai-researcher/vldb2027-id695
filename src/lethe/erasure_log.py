"""
Append-only erasure log for Lethe (paper Section 5.3 and Appendix F.4).

Every revocation and key-destruction event is appended to a hash-chained log.
Each entry carries the hash of the previous entry, so any tampering with a
past record breaks the chain and is detected on replay. This realizes the
Verifiable axis: an auditor can replay the log and confirm that the index's
state is exactly the result of the recorded operations, and that no recorded
operation was altered or dropped.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def _hash_entry(prev_hash: str, payload: dict[str, Any]) -> str:
    h = hashlib.sha256()
    h.update(prev_hash.encode())
    h.update(json.dumps(payload, sort_keys=True).encode())
    return h.hexdigest()


@dataclass
class ErasureLog:
    """Hash-chained, append-only log of erasure operations."""

    entries: list[dict[str, Any]] = field(default_factory=list)
    _GENESIS: str = "0" * 64

    def append(self, **payload: Any) -> str:
        prev = self.entries[-1]["hash"] if self.entries else self._GENESIS
        entry_hash = _hash_entry(prev, payload)
        self.entries.append({"payload": payload, "prev": prev, "hash": entry_hash})
        return entry_hash

    def verify(self) -> bool:
        """Replay the chain and confirm no entry was tampered with."""
        prev = self._GENESIS
        for e in self.entries:
            if e["prev"] != prev:
                return False
            if _hash_entry(prev, e["payload"]) != e["hash"]:
                return False
            prev = e["hash"]
        return True

    def tamper_detected_after_edit(self, index: int, field_: str, value: Any) -> bool:
        """Helper for the audit negative tests: mutate one entry and confirm
        the chain no longer verifies."""
        import copy

        clone = copy.deepcopy(self)
        clone.entries[index]["payload"][field_] = value
        return not clone.verify()

    def __len__(self) -> int:
        return len(self.entries)
