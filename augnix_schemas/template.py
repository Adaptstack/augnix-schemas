"""Template entity schemas — TemplateStatus, TemplateVisibility, AgentTemplate.

Correction 1.C3 (April 2026) — new file.
Consumed by template-service (MVP 2A) for versioned, tenant-scoped,
governed agent prompt templates.

Every Agent is created from a Template.  System templates (is_system=True,
tenant_id=None) are visible to all tenants.  Tenant templates are private
by default and can be promoted to marketplace visibility by the tenant.
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class TemplateStatus(StrEnum):
    """Lifecycle state of an AgentTemplate.

    State machine:
      draft → submitted → approved → published → deprecated
      (any state) → deprecated  (owner/admin can deprecate at any time)
    """

    draft = "draft"               # being authored — not visible outside tenant
    submitted = "submitted"       # submitted for compliance review
    approved = "approved"         # approved by reviewer — ready to publish
    published = "published"       # live — visible to intended audience
    deprecated = "deprecated"     # retired — agents can still run but no new instantiations


class TemplateVisibility(StrEnum):
    """Who can see and instantiate this template.

    system      : Augnix-provided, visible to ALL tenants (is_system=True)
    tenant      : visible only within the owning tenant
    marketplace : published to the Augnix marketplace — any tenant can use
    private     : visible only to the creator (sub-tenant isolation)
    """

    system = "system"
    tenant = "tenant"
    marketplace = "marketplace"
    private = "private"


class AgentTemplate(BaseModel):
    """A versioned, governed blueprint for creating Agents.

    The 4 layer dicts (identity, behavior, execution, governance) mirror the
    AgentManifest structure.  They are stored as JSONB in Postgres and
    validated against Schema Registry before a template is published.

    tenant_id=None means this is a system template owned by Augnix.
    All system templates have is_system=True and visibility=system.
    """

    model_config = ConfigDict(frozen=True)

    # ── Identity ──────────────────────────────────────────────────────────────
    id: str
    tenant_id: str | None = None             # None = Augnix system template
    name: str
    description: str

    # ── Classification ────────────────────────────────────────────────────────
    type: Literal["chat", "voice", "async", "webhook"]
    industry: str = "general"               # e.g. "bfsi", "healthcare", "retail"
    use_case: str = "general"               # e.g. "collections", "kyc", "support"
    risk_level: Literal["low", "medium", "high", "critical"] = "medium"

    # ── Versioning + lifecycle ────────────────────────────────────────────────
    version: str = "1.0.0"
    status: TemplateStatus = TemplateStatus.draft
    visibility: TemplateVisibility = TemplateVisibility.tenant
    is_system: bool = False                 # True = owned by Augnix, undeletable

    # ── 4-layer manifest blueprint ────────────────────────────────────────────
    identity: dict[str, Any]               # AgentIdentity-shaped dict
    behavior: dict[str, Any]               # AgentBehavior-shaped dict
    execution: dict[str, Any]              # AgentExecution-shaped dict
    governance: dict[str, Any]             # AgentGovernance-shaped dict

    # ── Provenance ────────────────────────────────────────────────────────────
    created_by: str | None = None
    approved_by: str | None = None         # reviewer who approved for publish

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at: datetime
    updated_at: datetime | None = None
    published_at: datetime | None = None   # set when status → published

    schema_version: str = "1.0.0"
