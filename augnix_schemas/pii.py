"""PII entity schemas — PIIEntityType, PIIEntity, PIIDetectionResult.

Correction 1.C3 (April 2026) — new file.
Consumed by pii-service (MVP 5) for named-entity detection, tokenisation,
and vault storage.  Every service that persists or forwards user-supplied
text to a model MUST call pii-service first.

Indian PII types (DPDP Act 2023 + IT Act compliance):
  aadhaar, pan, account_number, biometric, passport
Global PII types (GDPR / general):
  phone, email, address, name, dob
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class PIIEntityType(StrEnum):
    """Type of PII entity detected by pii-service.

    Indian PII types are explicitly called out to ensure DPDP Act compliance.
    """

    # ── Indian PII (DPDP Act 2023) ────────────────────────────────────────────
    aadhaar = "aadhaar"                # 12-digit Aadhaar number
    pan = "pan"                        # 10-char PAN card (ABCDE1234F pattern)
    account_number = "account_number"  # Bank account number
    biometric = "biometric"            # Biometric identifiers
    passport = "passport"              # Indian passport number

    # ── Universal PII ─────────────────────────────────────────────────────────
    phone = "phone"                    # Phone / mobile number (incl. +91)
    email = "email"                    # Email address
    address = "address"                # Physical address
    name = "name"                      # Full / partial personal name
    dob = "dob"                        # Date of birth


class PIIEntity(BaseModel):
    """A single PII entity detected in a text span.

    original_value is populated ONLY inside the vault — it is always
    None in API responses and Kafka events.  Callers receive entity_ref
    (an opaque token) which can be resolved by pii-service on demand.
    """

    model_config = ConfigDict(frozen=True)

    entity_ref: str                          # opaque vault token — e.g. "pii::aadhaar::a3f9..."
    entity_type: PIIEntityType
    original_value: str | None = None       # None outside the vault — NEVER log this
    redacted_value: str                      # e.g. "[AADHAAR REDACTED]", "***@***.com"
    confidence: float                        # 0.0–1.0 detection confidence
    offset_start: int                        # character offset in original text
    offset_end: int                          # character offset in original text


class PIIDetectionResult(BaseModel):
    """Result of a single pii-service detection call.

    text_hash: SHA-256 of the original text — raw text is NEVER stored.
    redacted_text: original text with all PII spans replaced by redacted_value.
    entities: list of all detected PII entities (original_value always None here).
    """

    model_config = ConfigDict(frozen=True)

    tenant_id: str
    text_hash: str                          # SHA-256 — never store raw text
    entities: list[PIIEntity]
    redacted_text: str                      # safe-to-store/log version of the input
    detected_at: datetime
    schema_version: str = "1.0.0"
