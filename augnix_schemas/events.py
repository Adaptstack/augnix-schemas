"""All 18 platform events as typed Pydantic models (frozen=True).

Event naming convention: <domain>.<noun>.<verb_past>
Every event carries: event_id, event_type, tenant_id, occurred_at, schema_version.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class _BaseEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: str
    tenant_id: str
    occurred_at: datetime
    schema_version: str = "1.0.0"


# ── Agent lifecycle ───────────────────────────────────────────────────────────

class AgentCreatedEvent(_BaseEvent):
    event_type: Literal["agent.created"] = "agent.created"
    agent_id: str
    project_id: str
    agent_type: str
    created_by: str


class AgentVersionCreatedEvent(_BaseEvent):
    event_type: Literal["agent.version.created"] = "agent.version.created"
    agent_id: str
    version: str
    created_by: str


class AgentVersionValidatedEvent(_BaseEvent):
    event_type: Literal["agent.version.validated"] = "agent.version.validated"
    agent_id: str
    version: str
    validated_by: str


class AgentVersionPublishedEvent(_BaseEvent):
    event_type: Literal["agent.version.published"] = "agent.version.published"
    agent_id: str
    version: str
    manifest_hash: str
    signature: str
    published_by: str


class AgentVersionPromotedEvent(_BaseEvent):
    event_type: Literal["agent.version.promoted"] = "agent.version.promoted"
    agent_id: str
    version: str
    promoted_by: str


# ── Session lifecycle ─────────────────────────────────────────────────────────

class SessionStartedEvent(_BaseEvent):
    event_type: Literal["session.started"] = "session.started"
    session_id: str
    agent_id: str
    agent_version: str
    project_id: str


class SessionStateChangedEvent(_BaseEvent):
    event_type: Literal["session.state.changed"] = "session.state.changed"
    session_id: str
    previous_state: str
    new_state: str


class SessionCompletedEvent(_BaseEvent):
    event_type: Literal["session.completed"] = "session.completed"
    session_id: str
    duration_ms: int
    message_count: int


class SessionFailedEvent(_BaseEvent):
    event_type: Literal["session.failed"] = "session.failed"
    session_id: str
    error_code: str
    error_message: str


class SessionCancelledEvent(_BaseEvent):
    event_type: Literal["session.cancelled"] = "session.cancelled"
    session_id: str
    cancelled_by: str


# ── Tool runtime ──────────────────────────────────────────────────────────────

class ToolInvokedEvent(_BaseEvent):
    event_type: Literal["tool.invoked"] = "tool.invoked"
    session_id: str
    call_id: str
    tool_id: str
    tool_name: str
    arguments: dict[str, Any] = {}


class ToolFailedEvent(_BaseEvent):
    event_type: Literal["tool.failed"] = "tool.failed"
    session_id: str
    call_id: str
    tool_id: str
    tool_name: str
    error_code: str
    error_message: str


# ── Policy ────────────────────────────────────────────────────────────────────

class PolicyBlockedEvent(_BaseEvent):
    event_type: Literal["policy.blocked"] = "policy.blocked"
    session_id: str
    policy_id: str
    policy_type: str
    reason: str


# ── Knowledge / retrieval ─────────────────────────────────────────────────────

class KnowledgeIndexedEvent(_BaseEvent):
    event_type: Literal["knowledge.indexed"] = "knowledge.indexed"
    source_id: str
    document_count: int
    chunk_count: int
    index_name: str


class RetrievalExecutedEvent(_BaseEvent):
    event_type: Literal["retrieval.executed"] = "retrieval.executed"
    session_id: str
    query: str
    result_count: int
    duration_ms: int


# ── Platform / quota ──────────────────────────────────────────────────────────

class QuotaThresholdReachedEvent(_BaseEvent):
    event_type: Literal["quota.threshold.reached"] = "quota.threshold.reached"
    quota_type: str
    current_usage: int
    limit: int
    threshold_pct: int


# ── HITL ──────────────────────────────────────────────────────────────────────

class HumanApprovalRequestedEvent(_BaseEvent):
    event_type: Literal["human.approval.requested"] = "human.approval.requested"
    session_id: str
    request_id: str
    requested_by: str
    context: dict[str, Any] = {}


class HumanApprovalResolvedEvent(_BaseEvent):
    event_type: Literal["human.approval.resolved"] = "human.approval.resolved"
    session_id: str
    request_id: str
    resolved_by: str
    decision: str  # "approved" | "rejected"
    notes: str | None = None


# ── Union type for all platform events ───────────────────────────────────────

PlatformEvent = (
    AgentCreatedEvent
    | AgentVersionCreatedEvent
    | AgentVersionValidatedEvent
    | AgentVersionPublishedEvent
    | AgentVersionPromotedEvent
    | SessionStartedEvent
    | SessionStateChangedEvent
    | SessionCompletedEvent
    | SessionFailedEvent
    | SessionCancelledEvent
    | ToolInvokedEvent
    | ToolFailedEvent
    | PolicyBlockedEvent
    | KnowledgeIndexedEvent
    | RetrievalExecutedEvent
    | QuotaThresholdReachedEvent
    | HumanApprovalRequestedEvent
    | HumanApprovalResolvedEvent
)

ALL_EVENT_TYPES: list[type[_BaseEvent]] = [
    AgentCreatedEvent,
    AgentVersionCreatedEvent,
    AgentVersionValidatedEvent,
    AgentVersionPublishedEvent,
    AgentVersionPromotedEvent,
    SessionStartedEvent,
    SessionStateChangedEvent,
    SessionCompletedEvent,
    SessionFailedEvent,
    SessionCancelledEvent,
    ToolInvokedEvent,
    ToolFailedEvent,
    PolicyBlockedEvent,
    KnowledgeIndexedEvent,
    RetrievalExecutedEvent,
    QuotaThresholdReachedEvent,
    HumanApprovalRequestedEvent,
    HumanApprovalResolvedEvent,
]
