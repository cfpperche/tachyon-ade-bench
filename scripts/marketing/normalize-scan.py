#!/usr/bin/env python3
"""Normalize a raw acquisition scan into stable ad observations."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
VERSION = "0.1"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: raw scan must be a JSON object")
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


def clean_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    cleaned = [clean_text(value) for value in values]
    return sorted({value for value in cleaned if value})


def landing_domain(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    return parsed.netloc.lower() or None


def fingerprint(platform: str, advertiser: str, ad: dict[str, Any]) -> str:
    landing = clean_text(ad.get("landing_url")) or ""
    creative = clean_text(ad.get("creative_hash")) or clean_text(ad.get("creative_url")) or ""
    payload = {
        "platform": platform,
        "advertiser": clean_text(advertiser) or "",
        "headline": clean_text(ad.get("headline")) or "",
        "body": clean_text(ad.get("body")) or "",
        "cta": clean_text(ad.get("cta")) or "",
        "landing_domain": landing_domain(landing),
        "creative": creative,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize(args: argparse.Namespace) -> dict[str, Any]:
    raw_path = Path(args.raw_file)
    raw = read_json(raw_path)
    observed_at = clean_text(raw.get("observed_at")) or utc_now()
    ads = raw.get("ads")
    if not isinstance(ads, list):
        raise SystemExit(f"{raw_path}: ads must be a list")
    raw_ref = str(raw_path.relative_to(ROOT)) if raw_path.is_absolute() and raw_path.is_relative_to(ROOT) else str(raw_path)
    observations: list[dict[str, Any]] = []
    for index, ad in enumerate(ads):
        if not isinstance(ad, dict):
            raise SystemExit(f"{raw_path}: ads[{index}] must be an object")
        advertiser = clean_text(ad.get("advertiser_name"))
        source_url = clean_text(ad.get("source_url")) or clean_text(raw.get("source_url"))
        if not advertiser or not source_url:
            raise SystemExit(f"{raw_path}: ads[{index}] needs advertiser_name and source_url")
        landing_url = clean_text(ad.get("landing_url"))
        status = clean_text(ad.get("status")) or "unknown"
        if status not in {"active", "inactive", "unknown"}:
            raise SystemExit(f"{raw_path}: ads[{index}].status must be active, inactive, or unknown")
        observation = {
          "event_type": "ad_seen",
          "scan_id": args.scan_id,
          "product_id": args.product,
          "platform": args.platform,
          "platform_ad_id": clean_text(ad.get("platform_ad_id")),
          "ad_fingerprint": fingerprint(args.platform, advertiser, ad),
          "observed_at": observed_at,
          "source_url": source_url,
          "advertiser_name": advertiser,
          "status": status,
          "headline": clean_text(ad.get("headline")),
          "body": clean_text(ad.get("body")),
          "cta": clean_text(ad.get("cta")),
          "landing_url": landing_url,
          "landing_domain": landing_domain(landing_url),
          "countries": clean_list(ad.get("countries")),
          "creative_type": clean_text(ad.get("creative_type")),
          "creative_url": clean_text(ad.get("creative_url")),
          "creative_hash": clean_text(ad.get("creative_hash")),
          "claims": clean_list(ad.get("claims")),
          "positioning_tags": clean_list(ad.get("positioning_tags")),
          "raw_ref": raw_ref,
          "notes": clean_text(ad.get("notes")) or "",
        }
        observations.append(observation)
    observations.sort(key=lambda item: item["ad_fingerprint"])
    return {
        "schema_version": VERSION,
        "scan_id": args.scan_id,
        "product_id": args.product,
        "platform": args.platform,
        "observed_at": observed_at,
        "observations": observations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize a raw acquisition scan")
    parser.add_argument("--scan-id", required=True, help="scan id such as 20260707T200000Z")
    parser.add_argument("--platform", required=True, help="platform id from marketing/registry/sources.json")
    parser.add_argument("--product", required=True, help="product id from competitors/")
    parser.add_argument("--raw-file", required=True, help="raw scan JSON file")
    parser.add_argument("--output", help="output normalized JSON path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    normalized = normalize(args)
    output = Path(args.output) if args.output else ROOT / "marketing" / "scans" / args.scan_id / args.platform / f"{args.product}.normalized.json"
    write_json(output, normalized)
    print(f"Wrote {output.relative_to(ROOT) if output.is_absolute() and output.is_relative_to(ROOT) else output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
