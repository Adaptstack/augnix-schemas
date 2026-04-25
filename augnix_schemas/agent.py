"""Agent entity schemas — AgentManifest, AgentConfig, AgentIdentity,
AgentBehavior, AgentExecution, AgentGovernance, AgentReleaseState."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class AgentReleaseState(StrEnum):
    draft = "draft"
    validated = "validated"
    eval_passed = "eval_passed"
    published = "published"
    promoted = "promoted"
    deprecated = "deprecated"
    rolled_back = "rolled_back"
    archived = "archived"


class AgentIdentity(BaseModel):
    model_config = ConfigDict(frozen=True)

    agent_id: str
    tenant_id: str
    project_id: str
    name: str
    description: str | None = None
    type: Literal["chat", "voice", "async", "webhook"]
    labels: list[str] = []
    created_at: datetime
    created_by: str
    schema_version: str = "1.0.0"


class AgentBehavior(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str
    goals: list[str]
    instructions: str
    persona: dict[str, Any] | None = None
    safety_profile: dict[str, Any]
    output_contract: dict[str, Any] | None = None
    escalation_policy: dict[str, Any] | None = None
    prohibited_actions: list[str] = []
    schema_version: str = "1.0.0"


class AgentExecution(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str
    model_routing: dict[str, Any]
    tools: list[str] = []
    memory_policy: dict[str, Any]
    retrieval_strategy: dict[str, Any] | None = None
    timeout_ms: int = 30_000
    retry_policy: dict[str, Any] | None = None
    tool_selection_strategy: str = "auto"
    concurrency_limit: int = 1
    schema_version: str = "1.0.0"


class AgentGovernance(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str
    pii_mode: Literal["none", "mask", "redact", "tokenize"]
    audit_class: Literal["low", "medium", "high"]
    policy_refs: list[str] = []
    region_lock: str | None = None
    compliance_profile: dict[str, Any] | None = None
    approval_required: bool = False
    retention_policy: dict[str, Any] | None = None
    schema_version: str = "1.0.0"


class AgentManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str
    identity: AgentIdentity
    behavior: AgentBehavior
    execution: AgentExecution
    governance: AgentGovernance
    schema_version: str = "1.0.0"


class AgentConfig(BaseModel):
    """Top-level agent record stored in Postgres."""

    model_config = ConfigDict(frozen=True)

    id: str
    tenant_id: str
    project_id: str
    type: Literal["chat", "voice", "async", "webhook"]
    current_version: str | None = None
    release_state: AgentReleaseState = AgentReleaseState.draft
    created_at: datetime
    updated_at: datetime
    schema_version: str = "1.0.0"
