"""Policy entity schemas — PolicyRule, PolicyType, PolicyAction,
PolicyEvalResult, PolicyDecision, PredicateTrace."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class PolicyType(StrEnum):
    content_filter = "content_filter"
    rate_limit = "rate_limit"
    pii_handling = "pii_handling"
    compliance = "compliance"
    access_control = "access_control"
    topic_restriction = "topic_restriction"


class PolicyAction(StrEnum):
    allow = "allow"
    block = "block"
    redact = "redact"
    escalate = "escalate"
    log = "log"


class PredicateTrace(BaseModel):
    model_config = ConfigDict(frozen=True)

    predicate_id: str
    tenant_id: str
    expression: str
    result: bool
    matched_value: Any = None
    evaluated_at: datetime
    schema_version: str = "1.0.0"


class PolicyEvalResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    eval_id: str
    tenant_id: str
    policy_id: str
    action: PolicyAction
    triggered: bool
    predicate_traces: list[PredicateTrace] = []
    evaluated_at: datetime
    schema_version: str = "1.0.0"


class PolicyDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision_id: str
    tenant_id: str
    session_id: str
    final_action: PolicyAction
    eval_results: list[PolicyEvalResult] = []
    decided_at: datetime
    schema_version: str = "1.0.0"


class PolicyRule(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    tenant_id: str
    name: str
    policy_type: PolicyType
    action: PolicyAction
    predicate: dict[str, Any]
    priority: int = 0
    enabled: bool = True
    metadata: dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    schema_version: str = "1.0.0"
