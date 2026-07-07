#!/usr/bin/env python3
"""Record a negative acquisition-library lookup in a scan manifest."""

from __future__ import annotations

import argparse

from common import append_query, load_or_create_manifest, scan_dir, validate_product_platform, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record a not-found acquisition lookup")
    parser.add_argument("--scan-id", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--country")
    parser.add_argument("--method", default="manual-url", choices=["official-api", "browser-capture", "manual-url", "manual-entry", "export"])
    parser.add_argument("--output-root", help="override scan root; defaults to marketing/scans")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    validate_product_platform(args.product, args.platform)
    path, manifest = load_or_create_manifest(args.scan_id, args.output_root)
    append_query(manifest, args.platform, args.product, args.method, args.query, args.source_url, "not-found", args.country)
    (scan_dir(args.scan_id, args.output_root) / args.platform).mkdir(parents=True, exist_ok=True)
    write_json(path, manifest)
    print(f"Recorded not-found result in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
