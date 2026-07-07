#!/usr/bin/env python3
"""Validate tracked acquisition-intelligence metadata.

This intentionally avoids third-party JSON Schema dependencies. The schemas in
schemas/marketing document the contract; this script enforces the parts needed
for repository checks and CI.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MARKETING = ROOT / "marketing"
COMPETITORS = ROOT / "competitors"

CHANNEL_CLASSES = {"primary-paid", "secondary-paid", "adjacent-signal"}
AUTOMATION_LEVELS = {"automatable", "semi_automatable", "manual_required", "not_supported"}
CADENCES = {"weekly", "monthly", "manual"}
SCAN_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z$")
DATE_TIME_HINT = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def competitor_ids() -> set[str]:
    return {path.stem for path in COMPETITORS.glob("*.json")}


def require_keys(path: Path, data: dict[str, Any], keys: set[str]) -> list[str]:
    return [f"{path}: missing {key}" for key in sorted(keys - set(data))]


def reject_extra(path: Path, data: dict[str, Any], allowed: set[str]) -> list[str]:
    return [f"{path}: {key} is not allowed" for key in sorted(set(data) - allowed)]


def expect_string_list(path: Path, owner: str, values: Any, allow_empty: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(values, list):
        return [f"{path}: {owner} must be a list"]
    if not allow_empty and not values:
        errors.append(f"{path}: {owner} must not be empty")
    for index, value in enumerate(values):
        if not isinstance(value, str):
            errors.append(f"{path}: {owner}[{index}] must be a string")
    return errors


def validate_advertisers(path: Path, products: set[str]) -> list[str]:
    data = read_json(path)
    errors: list[str] = []
    errors.extend(require_keys(path, data, {"schema_version", "updated_at", "advertisers"}))
    errors.extend(reject_extra(path, data, {"schema_version", "updated_at", "advertisers"}))
    advertisers = data.get("advertisers")
    if not isinstance(advertisers, list) or not advertisers:
        return errors + [f"{path}: advertisers must be a non-empty list"]
    seen: set[str] = set()
    for index, item in enumerate(advertisers):
        label = f"advertisers[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: {label} must be an object")
            continue
        allowed = {"product_id", "display_name", "included", "aliases", "notes"}
        errors.extend(require_keys(path, item, allowed))
        errors.extend(reject_extra(path, item, allowed))
        product_id = item.get("product_id")
        if not isinstance(product_id, str) or not product_id:
            errors.append(f"{path}: {label}.product_id must be a non-empty string")
        elif product_id not in products:
            errors.append(f"{path}: {label}.product_id unknown competitor {product_id}")
        elif product_id in seen:
            errors.append(f"{path}: duplicate advertiser product_id {product_id}")
        else:
            seen.add(product_id)
        if not isinstance(item.get("display_name"), str) or not item.get("display_name"):
            errors.append(f"{path}: {label}.display_name must be a non-empty string")
        if not isinstance(item.get("included"), bool):
            errors.append(f"{path}: {label}.included must be boolean")
        aliases = item.get("aliases")
        if not isinstance(aliases, dict):
            errors.append(f"{path}: {label}.aliases must be an object")
            continue
        alias_keys = {"names", "domains", "handles", "github_orgs"}
        errors.extend(require_keys(path, aliases, alias_keys))
        errors.extend(reject_extra(path, aliases, alias_keys))
        for key in alias_keys:
            errors.extend(expect_string_list(path, f"{label}.aliases.{key}", aliases.get(key), allow_empty=key != "names"))
    return errors


def validate_sources(path: Path) -> tuple[list[str], set[str]]:
    data = read_json(path)
    errors: list[str] = []
    platforms: set[str] = set()
    errors.extend(require_keys(path, data, {"schema_version", "updated_at", "sources"}))
    errors.extend(reject_extra(path, data, {"schema_version", "updated_at", "sources"}))
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        return errors + [f"{path}: sources must be a non-empty list"], platforms
    for index, item in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: {label} must be an object")
            continue
        allowed = {
            "platform",
            "channel_class",
            "display_name",
            "source_url",
            "automation_level",
            "cadence",
            "query_fields",
            "limitations",
        }
        errors.extend(require_keys(path, item, allowed))
        errors.extend(reject_extra(path, item, allowed))
        platform = item.get("platform")
        if not isinstance(platform, str) or not platform:
            errors.append(f"{path}: {label}.platform must be a non-empty string")
        elif platform in platforms:
            errors.append(f"{path}: duplicate platform {platform}")
        else:
            platforms.add(platform)
        if item.get("channel_class") not in CHANNEL_CLASSES:
            errors.append(f"{path}: {label}.channel_class is invalid")
        if item.get("automation_level") not in AUTOMATION_LEVELS:
            errors.append(f"{path}: {label}.automation_level is invalid")
        if item.get("cadence") not in CADENCES:
            errors.append(f"{path}: {label}.cadence is invalid")
        if not isinstance(item.get("source_url"), str) or "://" not in item["source_url"]:
            errors.append(f"{path}: {label}.source_url must be a URI")
        errors.extend(expect_string_list(path, f"{label}.query_fields", item.get("query_fields"), allow_empty=False))
        errors.extend(expect_string_list(path, f"{label}.limitations", item.get("limitations"), allow_empty=False))
    return errors, platforms


def validate_manifest(path: Path, products: set[str], platforms: set[str]) -> list[str]:
    data = read_json(path)
    errors: list[str] = []
    allowed = {"schema_version", "scan_id", "started_at", "completed_at", "tool_version", "git_commit", "queries", "limitations"}
    errors.extend(require_keys(path, data, allowed - {"completed_at"}))
    errors.extend(reject_extra(path, data, allowed))
    scan_id = data.get("scan_id")
    if not isinstance(scan_id, str) or not SCAN_ID_RE.match(scan_id):
        errors.append(f"{path}: scan_id must look like 20260707T200000Z")
    elif path.parent.name != scan_id:
        errors.append(f"{path}: scan_id must match parent directory")
    if not isinstance(data.get("started_at"), str) or not DATE_TIME_HINT.match(data["started_at"]):
        errors.append(f"{path}: started_at must be an ISO date-time string")
    if not isinstance(data.get("queries"), list):
        errors.append(f"{path}: queries must be a list")
    else:
        for index, query in enumerate(data["queries"]):
            label = f"queries[{index}]"
            if not isinstance(query, dict):
                errors.append(f"{path}: {label} must be an object")
                continue
            if query.get("platform") not in platforms:
                errors.append(f"{path}: {label}.platform unknown {query.get('platform')}")
            if query.get("product_id") not in products:
                errors.append(f"{path}: {label}.product_id unknown {query.get('product_id')}")
            if query.get("result") not in {"found", "not-found", "partial", "blocked", None}:
                errors.append(f"{path}: {label}.result is invalid")
    errors.extend(expect_string_list(path, "limitations", data.get("limitations"), allow_empty=True))
    return errors


def validate_normalized_scan(path: Path, products: set[str], platforms: set[str]) -> list[str]:
    data = read_json(path)
    errors: list[str] = []
    required = {"schema_version", "scan_id", "product_id", "platform", "observed_at", "observations"}
    errors.extend(require_keys(path, data, required))
    errors.extend(reject_extra(path, data, required))
    if data.get("product_id") not in products:
        errors.append(f"{path}: product_id unknown {data.get('product_id')}")
    if data.get("platform") not in platforms:
        errors.append(f"{path}: platform unknown {data.get('platform')}")
    if not isinstance(data.get("observations"), list):
        return errors + [f"{path}: observations must be a list"]
    for index, item in enumerate(data["observations"]):
        label = f"observations[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: {label} must be an object")
            continue
        for key in ["event_type", "scan_id", "product_id", "platform", "ad_fingerprint", "observed_at", "source_url", "advertiser_name", "status"]:
            if key not in item:
                errors.append(f"{path}: {label}.{key} is required")
        if item.get("event_type") != "ad_seen":
            errors.append(f"{path}: {label}.event_type must be ad_seen")
        if item.get("product_id") != data.get("product_id"):
            errors.append(f"{path}: {label}.product_id must match scan product_id")
        if item.get("platform") != data.get("platform"):
            errors.append(f"{path}: {label}.platform must match scan platform")
        if item.get("scan_id") != data.get("scan_id"):
            errors.append(f"{path}: {label}.scan_id must match scan_id")
        if item.get("status") not in {"active", "inactive", "unknown"}:
            errors.append(f"{path}: {label}.status is invalid")
    return errors


def main() -> int:
    errors: list[str] = []
    products = competitor_ids()
    advertiser_file = MARKETING / "registry" / "advertisers.json"
    source_file = MARKETING / "registry" / "sources.json"
    if not advertiser_file.is_file():
        errors.append(f"{advertiser_file}: file is required")
    else:
        errors.extend(validate_advertisers(advertiser_file, products))
    if not source_file.is_file():
        errors.append(f"{source_file}: file is required")
        platforms: set[str] = set()
    else:
        source_errors, platforms = validate_sources(source_file)
        errors.extend(source_errors)

    for manifest in sorted((MARKETING / "scans").glob("*/manifest.json")):
        errors.extend(validate_manifest(manifest, products, platforms))
    for normalized in sorted((MARKETING / "scans").glob("*/*/*.normalized.json")):
        errors.extend(validate_normalized_scan(normalized, products, platforms))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("OK: marketing registry and scans are structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
