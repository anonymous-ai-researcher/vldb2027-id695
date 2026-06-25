"""
Access control for Lethe (paper Section 5.1 and Appendix A).

A shared index serves a set of principals U (users or roles). An access
policy assigns each vector p an authorized set A(p); principal u may retrieve
p exactly when u in A(p). Permissions form a lattice (L, <=) of roles. This
module also models vector-granular cryptographic shredding: each vector has a
content key, and destroying that key makes the plaintext unrecoverable
(paper: Physical axis, valid when the revoked set equals all of U).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AccessPolicy:
    """Per-vector authorized sets plus a per-vector key table.

    The key table models crypto-shredding: a vector whose key has been
    destroyed cannot be decrypted by anyone, which is how Lethe makes a
    globally erased vector physically unrecoverable.
    """

    authorized: dict[int, set[str]] = field(default_factory=dict)
    _keys: dict[int, bytes] = field(default_factory=dict)
    _destroyed: set[int] = field(default_factory=set)

    def grant(self, vector_id: int, principal: str) -> None:
        self.authorized.setdefault(vector_id, set()).add(principal)

    def can_access(self, vector_id: int, principal: str) -> bool:
        if vector_id in self._destroyed:
            return False
        allowed = self.authorized.get(vector_id)
        if allowed is None:
            return True  # default-visible unless an explicit predicate exists
        return principal in allowed

    # --------------------------------------------------------- crypto-shred
    def set_key(self, vector_id: int, key: bytes) -> None:
        self._keys[vector_id] = key

    def destroy_key(self, vector_id: int) -> None:
        """Destroy a vector's content key (irreversible).

        After this call the vector's bytes are unrecoverable: no snapshot,
        cache, or backup can decrypt them. This realizes the Physical axis.
        """
        self._keys.pop(vector_id, None)
        self._destroyed.add(vector_id)

    def key_exists(self, vector_id: int) -> bool:
        return vector_id in self._keys and vector_id not in self._destroyed
