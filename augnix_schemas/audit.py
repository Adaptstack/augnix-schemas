"""Audit entity schemas — AuditEvent (frozen, hash-chainable)."""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditEvent(BaseModel):
    """Immutable, hash-chainable audit event.

    Hash chain: each event stores the SHA-256 of the previous event's
    canonical JSON, forming a tamper-evident log.
    """

    model_config = ConfigDict(frozen=True)

    event_id: str
    tenant_id: str
    actor_id: str
    actor_type: str  # "user" | "agent" | "system"
    action: str
    resource_type: str
    resource_id: str
    session_id: str | None = None
    payload: dict[str, Any] = {}
    previous_hash: str | None = None
    occurred_at: datetime
    schema_version: str = "1.0.0"

    def compute_hash(self) -> str:
        """Return SHA-256 of the canonical JSON representation of this event."""
        canonical = self.model_dump_json(exclude={"previous_hash"})
        return hashlib.sha256(canonical.encode()).hexdigest()

    def is_chain_valid(self, previous_event: AuditEvent) -> bool:
        """Verify this event correctly chains from the previous one."""
        return self.previous_hash == previous_event.compute_hash()
