#!/usr/bin/env python3
"""Sync claimed items from docs/product/capabilities.json into competitors/tachyon.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "docs" / "product" / "capabilities.json"
PROFILE_PATH = ROOT / "competitors" / "tachyon.json"

CAPABILITY_AXES = (
    "agent_support",
    "orchestration",
    "workspace_isolation",
    "review_shipping",
    "remote_mobile",
    "context_memory",
    "integrations",
)


def main() -> int:
    caps_doc = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    features: dict[str, list[str]] = {}
    for axis in CAPABILITY_AXES:
        items = caps_doc.get("capabilities", {}).get(axis) or []
        names: list[str] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            status = item.get("status")
            name = item.get("name")
            if not name:
                continue
            # Export claimed items; keep not-claimed sentinels so axes stay explicit
            if status in {"claimed", "not-claimed"}:
                names.append(str(name))
        features[axis] = names

    profile.setdefault("research", {})
    profile["research"]["features"] = features

    positioning = caps_doc.get("positioning")
    if isinstance(positioning, str) and positioning.strip():
        profile["research"]["positioning"] = " ".join(positioning.split())

    updated = caps_doc.get("updated_at")
    if isinstance(updated, str) and updated:
        profile["updated_at"] = updated
        profile["research"]["last_reviewed"] = updated

    sources = profile["research"].setdefault("sources", [])
    owned_doc = {
        "url": "https://github.com/cfpperche/tachyon-ade-bench/tree/main/docs/product",
        "kind": "owned",
        "notes": (
            "Owned canonical product surface (docs/product): overview, capabilities, "
            "architecture, workflows, limits, and capabilities.json SSOT."
        ),
    }
    urls = {s.get("url") for s in sources if isinstance(s, dict)}
    if owned_doc["url"] not in urls:
        sources.insert(0, owned_doc)
    else:
        for source in sources:
            if source.get("url") == owned_doc["url"]:
                source["notes"] = owned_doc["notes"]
                source["kind"] = "owned"

    if caps_doc.get("confidence") == "owned":
        profile["research"]["confidence"] = "owned"

    setup = profile.setdefault("setup_notes", [])
    sync_note = (
        "Edit docs/product/capabilities.json first, then run "
        "scripts/product/sync-tachyon-profile.py."
    )
    if sync_note not in setup:
        setup.append(sync_note)

    PROFILE_PATH.write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    sizes = {key: len(value) for key, value in features.items()}
    print(f"OK: synced claimed capabilities into {PROFILE_PATH.relative_to(ROOT)}")
    print(f"     feature group sizes: {sizes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
