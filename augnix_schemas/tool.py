"""Tool entity schemas — ToolDefinition, ToolCall, ToolResult,
ToolSideEffectClass, ToolTrustClass."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ToolSideEffectClass(StrEnum):
    read_only = "read_only"
    idempotent = "idempotent"
    destructive = "destructive"
    external_write = "external_write"


class ToolTrustClass(StrEnum):
    internal = "internal"
    partner = "partner"
    community = "community"
    user_provided = "user_provided"


class ToolDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    tool_id: str
    tenant_id: str
    name: str
    description: str
    version: str
    side_effect_class: ToolSideEffectClass
    trust_class: ToolTrustClass
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    endpoint: str | None = None
    timeout_ms: int = 10_000
    metadata: dict[str, Any] = {}
    schema_version: str = "1.0.0"


class ToolCall(BaseModel):
    model_config = ConfigDict(frozen=True)

    call_id: str
    tenant_id: str
    session_id: str
    tool_id: str
    tool_name: str
    arguments: dict[str, Any]
    called_at: datetime
    schema_version: str = "1.0.0"


class ToolResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    call_id: str
    tenant_id: str
    session_id: str
    tool_id: str
    success: bool
    output: Any
    error: str | None = None
    duration_ms: int
    completed_at: datetime
    schema_version: str = "1.0.0"
