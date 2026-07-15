#!/usr/bin/env python3
"""Validate docs/product/capabilities.json structure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "docs" / "product" / "capabilities.json"

CAPABILITY_AXES = (
    "agent_support",
    "orchestration",
    "workspace_isolation",
    "review_shipping",
    "remote_mobile",
    "context_memory",
    "integrations",
)
ALLOWED_STATUS = {"claimed", "placeholder", "not-claimed"}
ALLOWED_CONFIDENCE = {"owned", "official-sourced", "partial-official", "seed"}


def main() -> int:
    if not JSON_PATH.is_file():
        print(f"missing {JSON_PATH}", file=sys.stderr)
        return 2

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print(f"{JSON_PATH}: root must be an object", file=sys.stderr)
        return 1

    errors: list[str] = []
    if data.get("product_id") != "tachyon":
        errors.append("product_id must be 'tachyon'")
    if not data.get("updated_at"):
        errors.append("updated_at is required")
    if data.get("confidence") not in ALLOWED_CONFIDENCE:
        errors.append("confidence must be a known research confidence level")

    caps = data.get("capabilities")
    if not isinstance(caps, dict):
        errors.append("capabilities must be an object")
        caps = {}

    for axis in CAPABILITY_AXES:
        if axis not in caps:
            errors.append(f"capabilities missing axis '{axis}'")
            continue
        items = caps[axis]
        if not isinstance(items, list):
            errors.append(f"capabilities.{axis} must be a list")
            continue
        for i, item in enumerate(items):
            label = f"capabilities.{axis}[{i}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            if not item.get("name"):
                errors.append(f"{label}.name is required")
            if item.get("status") not in ALLOWED_STATUS:
                errors.append(f"{label}.status must be one of {sorted(ALLOWED_STATUS)}")

    placeholders = data.get("placeholders") or []
    if not isinstance(placeholders, list):
        errors.append("placeholders must be a list when present")
    else:
        for i, item in enumerate(placeholders):
            label = f"placeholders[{i}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            if item.get("axis") not in CAPABILITY_AXES:
                errors.append(f"{label}.axis must be a known capability axis")
            if item.get("status") not in ALLOWED_STATUS:
                errors.append(f"{label}.status invalid")

    if errors:
        print("FAIL: capabilities.json")
        for err in errors:
            print(f"  - {err}")
        return 1

    claimed = 0
    for axis in CAPABILITY_AXES:
        for item in caps.get(axis) or []:
            if isinstance(item, dict) and item.get("status") == "claimed":
                claimed += 1
    print(
        f"OK: capabilities.json ({claimed} claimed items across {len(CAPABILITY_AXES)} axes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
