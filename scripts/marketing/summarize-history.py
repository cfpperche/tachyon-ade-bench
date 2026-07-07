#!/usr/bin/env python3
"""Build acquisition history and current-state summaries from normalized scans."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
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
        raise SystemExit(f"{path}: expected JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_observations() -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for path in sorted((MARKETING / "scans").glob("*/*/*.normalized.json")):
        scan = read_json(path)
        items = scan.get("observations")
        if not isinstance(items, list):
            raise SystemExit(f"{path}: observations must be a list")
        for item in items:
            if not isinstance(item, dict):
                raise SystemExit(f"{path}: every observation must be an object")
            observations.append(item)
    observations.sort(key=lambda item: (item.get("observed_at", ""), item.get("platform", ""), item.get("product_id", ""), item.get("ad_fingerprint", "")))
    return observations


def summarize_ads(observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in observations:
        grouped.setdefault(item["ad_fingerprint"], []).append(item)
    ads: list[dict[str, Any]] = []
    for fingerprint, items in sorted(grouped.items()):
        items.sort(key=lambda item: item["observed_at"])
        first = items[0]
        latest = items[-1]
        ads.append(
            {
                "ad_fingerprint": fingerprint,
                "product_id": latest["product_id"],
                "platform": latest["platform"],
                "platform_ad_id": latest.get("platform_ad_id"),
                "advertiser_name": latest["advertiser_name"],
                "first_seen": first["observed_at"],
                "last_seen": latest["observed_at"],
                "seen_count": len(items),
                "status": latest.get("status", "unknown"),
                "latest": latest,
            }
        )
    return ads


def summarize_campaigns(ads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for ad in ads:
        grouped.setdefault((ad["product_id"], ad["platform"]), []).append(ad)
    campaigns: list[dict[str, Any]] = []
    for (product_id, platform), items in sorted(grouped.items()):
        first_seen = min(item["first_seen"] for item in items) if items else None
        last_seen = max(item["last_seen"] for item in items) if items else None
        tags: set[str] = set()
        for item in items:
            latest = item.get("latest", {})
            if isinstance(latest, dict):
                tags.update(latest.get("positioning_tags", []))
        campaigns.append(
            {
                "product_id": product_id,
                "platform": platform,
                "ad_count": len(items),
                "first_seen": first_seen,
                "last_seen": last_seen,
                "positioning_tags": sorted(tags),
            }
        )
    return campaigns


def summarize_coverage(observations: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    products: dict[str, dict[str, Any]] = {}
    platforms: dict[str, dict[str, Any]] = {}
    for item in observations:
        product = products.setdefault(item["product_id"], {"observation_count": 0, "platforms": []})
        product["observation_count"] += 1
        if item["platform"] not in product["platforms"]:
            product["platforms"].append(item["platform"])
        platform = platforms.setdefault(item["platform"], {"observation_count": 0, "products": []})
        platform["observation_count"] += 1
        if item["product_id"] not in platform["products"]:
            platform["products"].append(item["product_id"])
    for value in products.values():
        value["platforms"].sort()
    for value in platforms.values():
        value["products"].sort()
    return {
        "schema_version": VERSION,
        "generated_at": generated_at,
        "products": dict(sorted(products.items())),
        "platforms": dict(sorted(platforms.items())),
    }


def build_outputs(observations: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    ads = summarize_ads(observations)
    return {
        "history_lines": [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in observations],
        "ads": {"schema_version": VERSION, "generated_at": generated_at, "ads": ads},
        "campaigns": {"schema_version": VERSION, "generated_at": generated_at, "campaigns": summarize_campaigns(ads)},
        "coverage": summarize_coverage(observations, generated_at),
    }


def write_outputs(outputs: dict[str, Any]) -> None:
    history = MARKETING / "history" / "ads.ndjson"
    history.parent.mkdir(parents=True, exist_ok=True)
    history.write_text("\n".join(outputs["history_lines"]) + ("\n" if outputs["history_lines"] else ""), encoding="utf-8")
    write_json(MARKETING / "current" / "ads.json", outputs["ads"])
    write_json(MARKETING / "current" / "campaigns.json", outputs["campaigns"])
    write_json(MARKETING / "current" / "coverage.json", outputs["coverage"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize acquisition scan history")
    parser.add_argument("--check", action="store_true", help="validate inputs without writing generated outputs")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    observations = load_observations()
    outputs = build_outputs(observations, utc_now())
    if not args.check:
        write_outputs(outputs)
        print(f"Wrote {len(observations)} observations to marketing/history and marketing/current")
    else:
        print(f"OK: {len(observations)} marketing observations can be summarized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
