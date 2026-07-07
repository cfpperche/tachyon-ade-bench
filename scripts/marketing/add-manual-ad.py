#!/usr/bin/env python3
"""Append a manually observed ad to a raw scan and normalize it."""

from __future__ import annotations

import argparse
import subprocess
import sys

from common import (
    append_query,
    clean_list,
    clean_text,
    load_or_create_manifest,
    normalized_scan_path,
    raw_scan_path,
    validate_product_platform,
    write_json,
    read_json,
    ROOT,
    utc_now,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add a manually observed ad to an acquisition scan")
    parser.add_argument("--scan-id", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--advertiser-name", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--query", help="query used to find the ad; defaults to advertiser name")
    parser.add_argument("--platform-ad-id")
    parser.add_argument("--status", default="active", choices=["active", "inactive", "unknown"])
    parser.add_argument("--headline")
    parser.add_argument("--body")
    parser.add_argument("--cta")
    parser.add_argument("--landing-url")
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--creative-type")
    parser.add_argument("--creative-url")
    parser.add_argument("--creative-hash")
    parser.add_argument("--claim", action="append", default=[])
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--notes", default="")
    parser.add_argument("--method", default="manual-entry", choices=["official-api", "browser-capture", "manual-url", "manual-entry", "export"])
    parser.add_argument("--output-root", help="override scan root; defaults to marketing/scans")
    return parser


def normalize(scan_id: str, platform: str, product: str, raw_file: str, output: str) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "marketing" / "normalize-scan.py"),
        "--scan-id",
        scan_id,
        "--platform",
        platform,
        "--product",
        product,
        "--raw-file",
        raw_file,
        "--output",
        output,
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    args = build_parser().parse_args()
    validate_product_platform(args.product, args.platform)
    manifest_path, manifest = load_or_create_manifest(args.scan_id, args.output_root)
    append_query(
        manifest,
        args.platform,
        args.product,
        args.method,
        args.query or args.advertiser_name,
        args.source_url,
        "found",
        None,
    )
    write_json(manifest_path, manifest)

    raw_path = raw_scan_path(args.scan_id, args.platform, args.product, args.output_root)
    if raw_path.exists():
        raw = read_json(raw_path)
    else:
        raw = {"source_url": args.source_url, "observed_at": utc_now(), "ads": []}
    raw.setdefault("source_url", args.source_url)
    raw.setdefault("observed_at", utc_now())
    ads = raw.setdefault("ads", [])
    if not isinstance(ads, list):
        raise SystemExit(f"{raw_path}: ads must be a list")
    ads.append(
        {
            "platform_ad_id": clean_text(args.platform_ad_id),
            "advertiser_name": args.advertiser_name,
            "status": args.status,
            "headline": clean_text(args.headline),
            "body": clean_text(args.body),
            "cta": clean_text(args.cta),
            "landing_url": clean_text(args.landing_url),
            "countries": clean_list(args.country),
            "creative_type": clean_text(args.creative_type),
            "creative_url": clean_text(args.creative_url),
            "creative_hash": clean_text(args.creative_hash),
            "source_url": args.source_url,
            "claims": clean_list(args.claim),
            "positioning_tags": clean_list(args.tag),
            "notes": clean_text(args.notes) or "",
        }
    )
    write_json(raw_path, raw)
    normalized_path = normalized_scan_path(args.scan_id, args.platform, args.product, args.output_root)
    normalize(args.scan_id, args.platform, args.product, str(raw_path), str(normalized_path))
    print(f"Wrote {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
