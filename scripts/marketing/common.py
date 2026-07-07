#!/usr/bin/env python3
"""Shared helpers for acquisition-intelligence scripts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MARKETING = ROOT / "marketing"
VERSION = "0.1"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text or None


def clean_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    cleaned = [clean_text(value) for value in values]
    return sorted({value for value in cleaned if value})


def load_registry_ids() -> tuple[set[str], set[str]]:
    advertisers = read_json(MARKETING / "registry" / "advertisers.json")
    sources = read_json(MARKETING / "registry" / "sources.json")
    product_ids = {item["product_id"] for item in advertisers.get("advertisers", [])}
    platforms = {item["platform"] for item in sources.get("sources", [])}
    return product_ids, platforms


def validate_product_platform(product_id: str, platform: str) -> None:
    products, platforms = load_registry_ids()
    if product_id not in products:
        raise SystemExit(f"Unknown marketing product id: {product_id}")
    if platform not in platforms:
        raise SystemExit(f"Unknown marketing platform: {platform}")


def scan_root(output_root: str | None) -> Path:
    return Path(output_root) if output_root else MARKETING / "scans"


def scan_dir(scan_id: str, output_root: str | None) -> Path:
    return scan_root(output_root) / scan_id


def git_commit() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def load_or_create_manifest(scan_id: str, output_root: str | None) -> tuple[Path, dict[str, Any]]:
    path = scan_dir(scan_id, output_root) / "manifest.json"
    if path.exists():
        return path, read_json(path)
    manifest = {
        "schema_version": VERSION,
        "scan_id": scan_id,
        "started_at": utc_now(),
        "completed_at": None,
        "tool_version": VERSION,
        "git_commit": git_commit(),
        "queries": [],
        "limitations": [
            "Manual scan helper output; platform libraries may omit spend, targeting, and performance data."
        ],
    }
    return path, manifest


def append_query(
    manifest: dict[str, Any],
    platform: str,
    product_id: str,
    method: str,
    query: str,
    source_url: str,
    result: str,
    country: str | None,
) -> None:
    entry = {
        "platform": platform,
        "product_id": product_id,
        "method": method,
        "query": query,
        "country": country,
        "source_url": source_url,
        "result": result,
    }
    if entry not in manifest.setdefault("queries", []):
        manifest["queries"].append(entry)


def raw_scan_path(scan_id: str, platform: str, product_id: str, output_root: str | None) -> Path:
    return scan_dir(scan_id, output_root) / platform / f"{product_id}.raw.json"


def normalized_scan_path(scan_id: str, platform: str, product_id: str, output_root: str | None) -> Path:
    return scan_dir(scan_id, output_root) / platform / f"{product_id}.normalized.json"
