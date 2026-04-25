"""Knowledge entity schemas — KnowledgeSource, DocumentChunk,
EmbeddingRecord, RetrievalResult, GroundingComposition."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class KnowledgeSource(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_id: str
    tenant_id: str
    name: str
    source_type: Literal["pdf", "url", "database", "api", "file", "confluence"]
    uri: str
    metadata: dict[str, Any] = {}
    indexed_at: datetime | None = None
    chunk_count: int = 0
    schema_version: str = "1.0.0"


class DocumentChunk(BaseModel):
    model_config = ConfigDict(frozen=True)

    chunk_id: str
    tenant_id: str
    source_id: str
    content: str
    chunk_index: int
    token_count: int
    metadata: dict[str, Any] = {}
    created_at: datetime
    schema_version: str = "1.0.0"


class EmbeddingRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    embedding_id: str
    tenant_id: str
    chunk_id: str
    model: str
    vector: list[float]
    dimensions: int
    created_at: datetime
    schema_version: str = "1.0.0"


class RetrievalResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    result_id: str
    tenant_id: str
    query: str
    chunk_id: str
    source_id: str
    content: str
    score: float
    metadata: dict[str, Any] = {}
    retrieved_at: datetime
    schema_version: str = "1.0.0"


class GroundingComposition(BaseModel):
    model_config = ConfigDict(frozen=True)

    composition_id: str
    tenant_id: str
    session_id: str
    query: str
    results: list[RetrievalResult]
    composed_context: str
    token_count: int
    composed_at: datetime
    schema_version: str = "1.0.0"
