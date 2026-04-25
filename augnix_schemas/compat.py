"""Backward-compatibility checker for JSON Schema evolution.

Usage:
    violations = validate_no_breaking_change(old_schema, new_schema)
    if violations:
        raise ValueError(f"Breaking changes detected: {violations}")
"""
from __future__ import annotations

from typing import Any

BreakingViolation = str


def validate_no_breaking_change(
    old_schema: dict[str, Any],
    new_schema: dict[str, Any],
) -> list[BreakingViolation]:
    """Return a list of breaking-change violations between two JSON Schemas.

    Rules enforced:
    - Removing a required field          → REJECT
    - Changing a field type              → REJECT
    - Adding a required field without default → REJECT
    - Removing an enum value             → REJECT
    - Adding an optional field           → ALLOW
    - Adding a new enum value            → ALLOW
    """
    violations: list[BreakingViolation] = []

    old_props: dict[str, Any] = old_schema.get("properties", {})
    new_props: dict[str, Any] = new_schema.get("properties", {})
    old_required: set[str] = set(old_schema.get("required", []))
    new_required: set[str] = set(new_schema.get("required", []))

    # 1. Required field removed entirely
    for field in old_required:
        if field not in new_props:
            violations.append(
                f"BREAKING: required field '{field}' was removed"
            )

    # 2. Field type changed
    for field, old_prop in old_props.items():
        if field not in new_props:
            continue
        new_prop = new_props[field]
        old_type = _extract_type(old_prop)
        new_type = _extract_type(new_prop)
        if old_type != new_type:
            violations.append(
                f"BREAKING: field '{field}' type changed from '{old_type}' to '{new_type}'"
            )

    # 3. New required field added without a default (not present in old schema)
    for field in new_required - old_required:
        if field not in old_props:
            violations.append(
                f"BREAKING: new required field '{field}' added with no default value"
            )

    # 4. Enum value removed
    for field, old_prop in old_props.items():
        if field not in new_props:
            continue
        old_enum = set(old_prop.get("enum") or [])
        new_enum = set(new_props[field].get("enum") or [])
        if old_enum:
            removed = old_enum - new_enum
            for val in sorted(removed):
                violations.append(
                    f"BREAKING: enum value '{val}' removed from field '{field}'"
                )

    return violations


def _extract_type(prop: dict[str, Any]) -> str:
    """Normalise a JSON Schema property to a comparable type string."""
    if "type" in prop:
        return str(prop["type"])
    if "$ref" in prop:
        return str(prop["$ref"])
    if "anyOf" in prop:
        return "anyOf:" + "|".join(
            _extract_type(p) for p in sorted(prop["anyOf"], key=str)
        )
    if "allOf" in prop:
        return "allOf:" + "|".join(
            _extract_type(p) for p in sorted(prop["allOf"], key=str)
        )
    return "unknown"
