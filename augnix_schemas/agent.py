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


# ── Correction 1.C1 — GuardrailsConfig (April 2026) ──────────────────────────
# Added as part of MVP 0 correction: Template Service, Guardrail Gateway, and
# PII Service are now first-class services.  This config block is stored inside
# AgentGovernance (optional, backward-compatible) and consumed by guardrail-service
# at runtime to decide per-agent BLOCK / FLAG / ALLOW behaviour.
class GuardrailsConfig(BaseModel):
    """Per-agent guardrails policy consumed by guardrail-service (MVP 2C).

    All fields are optional with safe defaults so that agents created before
    guardrail-service was deployed continue to work without migration.

    Modes — "block": reject and return safe deflection response
            "flag":  log violation but let the request continue
            "allow": skip the check entirely (use only in trusted dev tenants)
    """

    model_config = ConfigDict(frozen=True)

    # ── Input checks ──────────────────────────────────────────────────────────
    jailbreak_detection: str = "block"           # block|flag|allow
    prompt_injection_detection: str = "block"    # block|flag|allow
    indirect_injection_scan: bool = True         # scan retrieved docs for injections
    system_prompt_leak_protection: bool = True   # block output that leaks system prompt

    # ── Output checks ─────────────────────────────────────────────────────────
    content_safety_mode: str = "block"           # block|flag|allow

    # ── Intent / topic controls ───────────────────────────────────────────────
    blocked_intents: list[str] = []              # e.g. ["persona_override", "self_harm"]
    topic_drift_threshold: float = 0.8           # cosine similarity floor vs agent goals
    confidence_floor: float = 0.6               # min classifier confidence to act on
    off_topic_action: str = "deflect"           # deflect|block|escalate

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
    # ── Correction 1.C1 — NEW optional field (fully backward-compatible) ──────
    guardrails: GuardrailsConfig | None = None   # None = guardrail-service uses its own defaults
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
