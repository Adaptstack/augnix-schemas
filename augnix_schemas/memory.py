"""Memory entity schemas — MemoryWrite, MemoryTier, StorageLocation, VisibilityDeclaration."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class MemoryTier(StrEnum):
    working = "working"
    episodic = "episodic"
    semantic = "semantic"
    procedural = "procedural"
    external = "external"


class StorageLocation(StrEnum):
    redis = "redis"
    postgres = "postgres"
    vector_db = "vector_db"
    object_store = "object_store"


class VisibilityDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str
    tier: MemoryTier
    readable_by: list[str] = []
    writable_by: list[str] = []
    expires_after_seconds: int | None = None
    schema_version: str = "1.0.0"


class MemoryWrite(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    tenant_id: str
    agent_id: str
    session_id: str | None = None
    tier: MemoryTier
    storage_location: StorageLocation
    key: str
    value: Any
    visibility: VisibilityDeclaration
    metadata: dict[str, Any] = {}
    written_at: datetime
    expires_at: datetime | None = None
    schema_version: str = "1.0.0"
