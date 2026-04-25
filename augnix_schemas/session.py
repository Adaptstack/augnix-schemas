"""Session entity schemas — Session, SessionEvent, SessionState, Message, MessageRole."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class MessageRole(StrEnum):
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"


class SessionState(StrEnum):
    active = "active"
    paused = "paused"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class Message(BaseModel):
    model_config = ConfigDict(frozen=True)

    message_id: str
    tenant_id: str
    session_id: str
    role: MessageRole
    content: str
    tool_call_id: str | None = None
    tool_name: str | None = None
    metadata: dict[str, Any] = {}
    created_at: datetime
    schema_version: str = "1.0.0"


class SessionEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: str
    tenant_id: str
    session_id: str
    event_type: str
    payload: dict[str, Any] = {}
    occurred_at: datetime
    schema_version: str = "1.0.0"


class Session(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    tenant_id: str
    project_id: str
    agent_id: str
    agent_version: str
    state: SessionState = SessionState.active
    messages: list[Message] = []
    events: list[SessionEvent] = []
    metadata: dict[str, Any] = {}
    started_at: datetime
    ended_at: datetime | None = None
    schema_version: str = "1.0.0"
