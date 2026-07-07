#!/usr/bin/env python3
"""Plan a reproducible acquisition scan manifest from registries."""

from __future__ import annotations

import argparse
from urllib.parse import quote, urlencode

from common import MARKETING, append_query, load_or_create_manifest, read_json, scan_dir, write_json


PRIMARY_PLATFORMS = {"meta", "google", "linkedin", "x"}
GENERIC_DOMAINS = {"github.com", "gitlab.com", "npmjs.com"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan acquisition scan queries from marketing registries")
    parser.add_argument("--scan-id", required=True, help="scan id such as 20260707T230000Z")
    parser.add_argument("--platform", action="append", help="platform id to include; repeatable")
    parser.add_argument("--product", action="append", help="product id to include; repeatable")
    parser.add_argument("--country", default="US", help="country/region filter for platforms that support it")
    parser.add_argument("--method", default="manual-url", choices=["manual-url", "browser-capture", "official-api", "export"])
    parser.add_argument("--output-root", help="override scan root; defaults to marketing/scans")
    parser.add_argument("--dry-run", action="store_true", help="print planned rows without writing files")
    parser.add_argument("--limit-primary", action="store_true", help="include only primary paid platforms")
    return parser


def registries() -> tuple[list[dict], list[dict]]:
    advertisers = read_json(MARKETING / "registry" / "advertisers.json").get("advertisers", [])
    sources = read_json(MARKETING / "registry" / "sources.json").get("sources", [])
    return advertisers, sources


def domain_host(value: str) -> str:
    return value.removeprefix("https://").removeprefix("http://").split("/")[0].lower()


def first(values: list[str]) -> str | None:
    return values[0] if values else None


def source_url(platform: str, query: str, country: str | None) -> str:
    encoded_query = quote(query, safe="")
    if platform == "meta":
        return "https://www.facebook.com/ads/library/?" + urlencode(
            {
                "active_status": "active",
                "ad_type": "all",
                "country": "ALL",
                "is_targeted_country": "false",
                "media_type": "all",
                "q": query,
                "search_type": "keyword_unordered",
            }
        )
    if platform == "google":
        return f"https://adstransparency.google.com/?region={country or 'US'}&domain={encoded_query}"
    if platform == "linkedin":
        return f"https://www.linkedin.com/search/results/companies/?keywords={encoded_query}"
    if platform == "x":
        return f"https://ads.twitter.com/ads-repository?query={encoded_query}"
    if platform == "tiktok":
        return f"https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en?search={encoded_query}"
    if platform == "reddit":
        return f"https://business.reddithelp.com/s/article/ads-inspiration-library?query={encoded_query}"
    if platform == "product-hunt":
        return f"https://www.producthunt.com/search?q={encoded_query}"
    if platform == "github-sponsors":
        return f"https://github.com/sponsors/{encoded_query}"
    return f"https://www.google.com/search?q={quote(platform + ' ' + query)}"


def query_for_platform(advertiser: dict, source: dict) -> tuple[str, str]:
    aliases = advertiser["aliases"]
    names = aliases.get("names", [])
    domains = aliases.get("domains", [])
    handles = aliases.get("handles", [])
    github_orgs = aliases.get("github_orgs", [])
    platform = source["platform"]
    fields = source.get("query_fields", [])

    if platform == "google" and "domain" in fields and domains:
        domain = domains[0]
        host = domain_host(domain)
        if host in GENERIC_DOMAINS and "/" in domain:
            return domain, "generic-domain-context"
        return host, "domain"
    if platform == "github-sponsors" and github_orgs:
        return github_orgs[0], "github_org"
    if "handle" in fields and handles:
        return handles[0], "handle"
    if "domain" in fields and domains:
        domain = domains[0]
        host = domain_host(domain)
        if host not in GENERIC_DOMAINS:
            return host, "domain"
    if names:
        return names[0], "name"
    fallback = first(domains) or advertiser["product_id"]
    return fallback, "fallback"


def planned_rows(args: argparse.Namespace) -> list[dict]:
    advertisers, sources = registries()
    requested_products = set(args.product or [])
    requested_platforms = set(args.platform or [])
    rows: list[dict] = []
    for advertiser in advertisers:
        if not advertiser.get("included", False):
            continue
        if requested_products and advertiser["product_id"] not in requested_products:
            continue
        for source in sources:
            platform = source["platform"]
            if requested_platforms and platform not in requested_platforms:
                continue
            if args.limit_primary and platform not in PRIMARY_PLATFORMS:
                continue
            query, query_kind = query_for_platform(advertiser, source)
            result = "partial"
            if source.get("automation_level") == "not_supported":
                result = "blocked"
            rows.append(
                {
                    "platform": platform,
                    "product_id": advertiser["product_id"],
                    "method": args.method,
                    "query": query,
                    "country": args.country if platform == "google" else None,
                    "source_url": source_url(platform, query, args.country),
                    "result": result,
                    "query_kind": query_kind,
                }
            )
    return rows


def print_rows(rows: list[dict]) -> None:
    print("platform\tproduct_id\tquery_kind\tquery\tresult\tsource_url")
    for row in rows:
        print(
            "\t".join(
                [
                    row["platform"],
                    row["product_id"],
                    row["query_kind"],
                    row["query"],
                    row["result"],
                    row["source_url"],
                ]
            )
        )


def main() -> int:
    args = build_parser().parse_args()
    rows = planned_rows(args)
    if args.dry_run:
        print_rows(rows)
        return 0

    path, manifest = load_or_create_manifest(args.scan_id, args.output_root)
    manifest.setdefault("limitations", []).extend(
        [
            "Planned scan manifest only; rows are review targets, not proof that a platform query rendered results.",
            "Generic repository domains are kept with path context and must not be attributed to the generic host.",
        ]
    )
    manifest["limitations"] = sorted(set(manifest["limitations"]))
    for row in rows:
        append_query(
            manifest,
            row["platform"],
            row["product_id"],
            row["method"],
            row["query"],
            row["source_url"],
            row["result"],
            row["country"],
        )
        (scan_dir(args.scan_id, args.output_root) / row["platform"]).mkdir(parents=True, exist_ok=True)
    write_json(path, manifest)
    print(f"Wrote {path} with {len(rows)} planned rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
