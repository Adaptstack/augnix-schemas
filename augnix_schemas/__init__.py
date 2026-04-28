"""augnix-schemas — shared API, event, and contract schemas for Augnix AI Studio."""

from .agent import (
    AgentBehavior,
    AgentConfig,
    AgentExecution,
    AgentGovernance,
    AgentIdentity,
    AgentManifest,
    AgentReleaseState,
    GuardrailsConfig,  # Correction 1.C1
)
from .audit import AuditEvent
from .compat import validate_no_breaking_change
from .disposition import Disposition, DispositionCriticality
from .events import (
    ALL_EVENT_TYPES,
    AgentCreatedEvent,
    AgentVersionCreatedEvent,
    AgentVersionPromotedEvent,
    AgentVersionPublishedEvent,
    AgentVersionValidatedEvent,
    HumanApprovalRequestedEvent,
    HumanApprovalResolvedEvent,
    KnowledgeIndexedEvent,
    PlatformEvent,
    PolicyBlockedEvent,
    QuotaThresholdReachedEvent,
    RetrievalExecutedEvent,
    SessionCancelledEvent,
    SessionCompletedEvent,
    SessionFailedEvent,
    SessionStartedEvent,
    SessionStateChangedEvent,
    ToolFailedEvent,
    ToolInvokedEvent,
)
from .knowledge import (
    DocumentChunk,
    EmbeddingRecord,
    GroundingComposition,
    KnowledgeSource,
    RetrievalResult,
)
from .memory import MemoryTier, MemoryWrite, StorageLocation, VisibilityDeclaration
from .policy import (
    PolicyAction,
    PolicyDecision,
    PolicyEvalResult,
    PolicyRule,
    PolicyType,
    PredicateTrace,
)
from .session import Message, MessageRole, Session, SessionEvent, SessionState
from .tool import ToolCall, ToolDefinition, ToolResult, ToolSideEffectClass, ToolTrustClass

__all__ = [
    # agent
    "AgentBehavior",
    "AgentConfig",
    "AgentExecution",
    "AgentGovernance",
    "AgentIdentity",
    "AgentManifest",
    "AgentReleaseState",
    "GuardrailsConfig",  # Correction 1.C1
    # audit
    "AuditEvent",
    # compat
    "validate_no_breaking_change",
    # disposition
    "Disposition",
    "DispositionCriticality",
    # events
    "ALL_EVENT_TYPES",
    "AgentCreatedEvent",
    "AgentVersionCreatedEvent",
    "AgentVersionPromotedEvent",
    "AgentVersionPublishedEvent",
    "AgentVersionValidatedEvent",
    "HumanApprovalRequestedEvent",
    "HumanApprovalResolvedEvent",
    "KnowledgeIndexedEvent",
    "PlatformEvent",
    "PolicyBlockedEvent",
    "QuotaThresholdReachedEvent",
    "RetrievalExecutedEvent",
    "SessionCancelledEvent",
    "SessionCompletedEvent",
    "SessionFailedEvent",
    "SessionStartedEvent",
    "SessionStateChangedEvent",
    "ToolFailedEvent",
    "ToolInvokedEvent",
    # knowledge
    "DocumentChunk",
    "EmbeddingRecord",
    "GroundingComposition",
    "KnowledgeSource",
    "RetrievalResult",
    # memory
    "MemoryTier",
    "MemoryWrite",
    "StorageLocation",
    "VisibilityDeclaration",
    # policy
    "PolicyAction",
    "PolicyDecision",
    "PolicyEvalResult",
    "PolicyRule",
    "PolicyType",
    "PredicateTrace",
    # session
    "Message",
    "MessageRole",
    "Session",
    "SessionEvent",
    "SessionState",
    # tool
    "ToolCall",
    "ToolDefinition",
    "ToolResult",
    "ToolSideEffectClass",
    "ToolTrustClass",
]
