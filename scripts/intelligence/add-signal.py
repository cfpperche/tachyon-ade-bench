#!/usr/bin/env python3
"""Append a competitive-intelligence signal to a signal file."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SIGNALS = ROOT / "intelligence" / "current" / "signals.json"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


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


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = " ".join(value.split())
    return text or None


def clean_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    cleaned = [clean_text(value) for value in values]
    return sorted({value for value in cleaned if value})


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "signal"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add a competitive-intelligence signal")
    parser.add_argument("--signals-file", default=str(DEFAULT_SIGNALS))
    parser.add_argument("--id")
    parser.add_argument("--product", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--observed-at", default=today())
    parser.add_argument("--summary", required=True)
    parser.add_argument("--details")
    parser.add_argument("--evidence-path")
    parser.add_argument("--confidence", required=True, choices=["high", "medium", "low"])
    parser.add_argument("--freshness", required=True, choices=["current", "watch", "stale"])
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--impact", required=True, choices=["sales", "benchmark", "roadmap", "acquisition", "objection", "moat", "pricing"])
    parser.add_argument("--objection")
    parser.add_argument("--tachyon-response", required=True)
    parser.add_argument("--next-action")
    return parser


def validate(path: Path) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "intelligence" / "check-intelligence.py"),
        "--signals-file",
        str(path),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    args = build_parser().parse_args()
    path = Path(args.signals_file)
    data = read_json(path)
    signals = data.setdefault("signals", [])
    if not isinstance(signals, list):
        raise SystemExit(f"{path}: signals must be a list")
    signal_id = args.id or f"{args.product}-{args.category}-{slugify(args.summary)}"
    signals.append(
        {
            "category": args.category,
            "confidence": args.confidence,
            "details": clean_text(args.details),
            "evidence_path": clean_text(args.evidence_path),
            "freshness": args.freshness,
            "id": signal_id,
            "impact": args.impact,
            "next_action": clean_text(args.next_action),
            "objection": clean_text(args.objection),
            "observed_at": args.observed_at,
            "product_id": args.product,
            "source_type": args.source_type,
            "source_url": args.source_url,
            "summary": args.summary,
            "tachyon_response": args.tachyon_response,
            "tags": clean_list(args.tag),
        }
    )
    data["updated_at"] = utc_now()
    write_json(path, data)
    validate(path)
    print(f"Wrote signal {signal_id} to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
