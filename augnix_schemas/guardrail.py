"""Guardrail entity schemas — GuardrailViolationType, GuardrailDecision.

Correction 1.C3 (April 2026) — new file.
Consumed by guardrail-service (MVP 2C) for every input/output check decision.
Persisted in the guardrail_decisions table (append-only audit log).
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict


class GuardrailViolationType(StrEnum):
    """Category of guardrail violation detected by guardrail-service.

    Used in GuardrailDecision.violation_type and as keys in blocked_intents[]
    on GuardrailsConfig.
    """

    jailbreak = "jailbreak"                         # direct jailbreak attempt
    prompt_injection = "prompt_injection"           # user-supplied injection
    indirect_injection = "indirect_injection"       # injection found in retrieved doc
    persona_bypass = "persona_bypass"               # roleplay / "act as" bypass
    system_prompt_leak = "system_prompt_leak"       # output contains system prompt
    topic_drift = "topic_drift"                     # conversation steered off-goal
    content_safety = "content_safety"              # hate / violence / NSFW in input
    output_toxicity = "output_toxicity"            # toxic content in model output


class GuardrailDecision(BaseModel):
    """Immutable record of a single guardrail check decision.

    Stored in the guardrail_decisions table by guardrail-service.
    Append-only — never updated after creation.

    input_hash: SHA-256 of the raw input text.  Raw text is NEVER stored.
    decision:   what guardrail-service told the caller to do.
    """

    model_config = ConfigDict(frozen=True)

    # ── Identity ──────────────────────────────────────────────────────────────
    session_id: str
    tenant_id: str
    agent_id: str
    agent_version: str

    # ── What was checked ──────────────────────────────────────────────────────
    check_type: Literal["input", "output"]           # which pipeline stage
    violation_type: GuardrailViolationType | None = None  # None if decision=allow

    # ── Evidence ──────────────────────────────────────────────────────────────
    input_hash: str                                  # SHA-256 — never store raw text

    # ── Decision ─────────────────────────────────────────────────────────────
    decision: Literal["allow", "block", "flag"]
    confidence: float                                # 0.0–1.0 classifier confidence
    reason: str | None = None                       # human-readable explanation

    # ── Timestamps ────────────────────────────────────────────────────────────
    decided_at: datetime

    schema_version: str = "1.0.0"
