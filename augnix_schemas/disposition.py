"""Disposition entity schemas — Disposition, DispositionCriticality."""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class DispositionCriticality(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Disposition(BaseModel):
    model_config = ConfigDict(frozen=True)

    disposition_id: str
    tenant_id: str
    session_id: str
    agent_id: str
    criticality: DispositionCriticality
    outcome: str
    reasoning: str | None = None
    requires_human_review: bool = False
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    metadata: dict[str, Any] = {}
    created_at: datetime
    schema_version: str = "1.0.0"
