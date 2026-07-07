#!/usr/bin/env python3
"""Create or update a manual acquisition scan manifest."""

from __future__ import annotations

import argparse

from common import append_query, load_or_create_manifest, scan_dir, validate_product_platform, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a manual acquisition scan")
    parser.add_argument("--scan-id", required=True, help="scan id such as 20260707T210000Z")
    parser.add_argument("--product", required=True, help="product id from marketing registry")
    parser.add_argument("--platform", required=True, help="platform id from marketing source registry")
    parser.add_argument("--query", required=True, help="query used in the ad library")
    parser.add_argument("--source-url", required=True, help="source library URL queried")
    parser.add_argument("--country", help="country or region filter, if used")
    parser.add_argument("--result", default="partial", choices=["found", "not-found", "partial", "blocked"])
    parser.add_argument("--method", default="manual-url", choices=["official-api", "browser-capture", "manual-url", "manual-entry", "export"])
    parser.add_argument("--output-root", help="override scan root; defaults to marketing/scans")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    validate_product_platform(args.product, args.platform)
    path, manifest = load_or_create_manifest(args.scan_id, args.output_root)
    append_query(manifest, args.platform, args.product, args.method, args.query, args.source_url, args.result, args.country)
    (scan_dir(args.scan_id, args.output_root) / args.platform).mkdir(parents=True, exist_ok=True)
    write_json(path, manifest)
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
