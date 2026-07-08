#!/usr/bin/env python3
"""Validate tracked competitive-intelligence signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
COMPETITORS = ROOT / "competitors"
DEFAULT_SIGNALS = ROOT / "intelligence" / "current" / "signals.json"

CATEGORIES = {
    "battlecard",
    "positioning",
    "feature",
    "stack",
    "pricing",
    "packaging",
    "traffic",
    "seo",
    "paid_search",
    "backlink",
    "share_of_search",
    "market",
    "review",
    "objection",
    "source_watch",
}
SOURCE_TYPES = {
    "official-site",
    "official-docs",
    "source-repo",
    "package-manifest",
    "app-store",
    "owned",
    "manual-research",
    "tool-export",
    "ad-library",
    "search-tool",
    "market-intel-tool",
    "pricing-watch",
    "snapshot",
}
CONFIDENCE = {"high", "medium", "low"}
FRESHNESS = {"current", "watch", "stale"}
IMPACT = {"sales", "benchmark", "roadmap", "acquisition", "objection", "moat", "pricing"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]+$")
DATE_HINT = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def competitor_ids() -> set[str]:
    return {path.stem for path in COMPETITORS.glob("*.json")}


def expect_string(path: Path, label: str, value: Any, errors: list[str], *, uri: bool = False) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: {label} must be a non-empty string")
    elif uri and "://" not in value:
        errors.append(f"{path}: {label} must be a URI")


def expect_string_or_null(path: Path, label: str, value: Any, errors: list[str]) -> None:
    if value is not None and not isinstance(value, str):
        errors.append(f"{path}: {label} must be a string or null")


def expect_string_list(path: Path, label: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: {label} must be a list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}: {label}[{index}] must be a non-empty string")


def validate_signal(path: Path, signal: Any, index: int, products: set[str], seen: set[str]) -> list[str]:
    errors: list[str] = []
    label = f"signals[{index}]"
    if not isinstance(signal, dict):
        return [f"{path}: {label} must be an object"]
    required = {
        "id",
        "product_id",
        "category",
        "source_type",
        "source_url",
        "observed_at",
        "summary",
        "confidence",
        "freshness",
        "tags",
        "impact",
        "tachyon_response",
    }
    allowed = required | {"details", "evidence_path", "objection", "next_action"}
    for key in sorted(required - set(signal)):
        errors.append(f"{path}: {label}.{key} is required")
    for key in sorted(set(signal) - allowed):
        errors.append(f"{path}: {label}.{key} is not allowed")

    signal_id = signal.get("id")
    if not isinstance(signal_id, str) or not ID_RE.match(signal_id):
        errors.append(f"{path}: {label}.id is invalid")
    elif signal_id in seen:
        errors.append(f"{path}: duplicate signal id {signal_id}")
    else:
        seen.add(signal_id)

    product_id = signal.get("product_id")
    if product_id not in products:
        errors.append(f"{path}: {label}.product_id unknown {product_id}")
    if signal.get("category") not in CATEGORIES:
        errors.append(f"{path}: {label}.category is invalid")
    if signal.get("source_type") not in SOURCE_TYPES:
        errors.append(f"{path}: {label}.source_type is invalid")
    if signal.get("confidence") not in CONFIDENCE:
        errors.append(f"{path}: {label}.confidence is invalid")
    if signal.get("freshness") not in FRESHNESS:
        errors.append(f"{path}: {label}.freshness is invalid")
    if signal.get("impact") not in IMPACT:
        errors.append(f"{path}: {label}.impact is invalid")
    if not isinstance(signal.get("observed_at"), str) or not DATE_HINT.match(signal["observed_at"]):
        errors.append(f"{path}: {label}.observed_at must start with YYYY-MM-DD")

    expect_string(path, f"{label}.source_url", signal.get("source_url"), errors, uri=True)
    expect_string(path, f"{label}.summary", signal.get("summary"), errors)
    expect_string(path, f"{label}.tachyon_response", signal.get("tachyon_response"), errors)
    expect_string_list(path, f"{label}.tags", signal.get("tags"), errors)
    for optional in ["details", "evidence_path", "objection", "next_action"]:
        expect_string_or_null(path, f"{label}.{optional}", signal.get(optional), errors)
    return errors


def validate_file(path: Path) -> list[str]:
    data = read_json(path)
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{path}: root must be an object"]
    for key in ["schema_version", "updated_at", "signals"]:
        if key not in data:
            errors.append(f"{path}: missing {key}")
    for key in sorted(set(data) - {"schema_version", "updated_at", "signals"}):
        errors.append(f"{path}: {key} is not allowed")
    expect_string(path, "schema_version", data.get("schema_version"), errors)
    expect_string(path, "updated_at", data.get("updated_at"), errors)
    signals = data.get("signals")
    if not isinstance(signals, list):
        return errors + [f"{path}: signals must be a list"]
    products = competitor_ids()
    seen: set[str] = set()
    for index, signal in enumerate(signals):
        errors.extend(validate_signal(path, signal, index, products, seen))
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate competitive-intelligence signals")
    parser.add_argument("--signals-file", default=str(DEFAULT_SIGNALS))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    path = Path(args.signals_file)
    if not path.is_file():
        print(f"{path}: file is required", file=sys.stderr)
        return 1
    errors = validate_file(path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("OK: competitive-intelligence signals are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
