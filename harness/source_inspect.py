"""Source-inspection harness for open-source ADE checkouts.

Deterministic detectors plus a vendor-neutral agent protocol (Claude Code,
Codex, Grok Build). Marketing text in competitor profiles is not evidence.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
COMPETITORS = ROOT / "competitors"

INSPECT = ROOT / "inspect"
FEATURE_CATALOG = INSPECT / "catalog" / "features.json"
INSPECT_PROMPT = INSPECT / "prompts" / "inspect-features.md"
FIXTURES = INSPECT / "fixtures"
INSPECTION_SCHEMA = ROOT / "schemas" / "inspection-result.schema.json"

OSI_LICENSE_IDS = {
    "0BSD",
    "Apache-2.0",
    "AGPL-3.0",
    "AGPL-3.0-only",
    "AGPL-3.0-or-later",
    "BlueOak-1.0.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "EPL-2.0",
    "GPL-2.0",
    "GPL-2.0-only",
    "GPL-2.0-or-later",
    "GPL-3.0",
    "GPL-3.0-only",
    "GPL-3.0-or-later",
    "ISC",
    "LGPL-2.1",
    "LGPL-2.1-only",
    "LGPL-3.0",
    "LGPL-3.0-only",
    "MIT",
    "MPL-2.0",
    "Unlicense",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".turbo",
    ".cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "out",
    "target",
    "vendor",
    "coverage",
    "Pods",
}

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp4",
    ".wasm",
    ".zip",
    ".gz",
    ".tar",
    ".lock",
    ".map",
    ".pdf",
    ".bin",
}

DOC_NAMES = {
    "readme",
    "readme.md",
    "changelog",
    "changelog.md",
    "contributing.md",
    "code_of_conduct.md",
    "security.md",
    "authors",
    "notice",
}

DOC_DIRS = {"docs", "doc", "documentation", "website", "www"}
CONFIG_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "cargo.toml",
    "go.mod",
    "go.sum",
    "pyproject.toml",
    "tsconfig.json",
    "deno.json",
    "composer.json",
}
CONFIG_SUFFIXES = {".yml", ".yaml", ".toml", ".ini", ".cfg", ".json"}
SKIP_FILE_NAMES = {
    "vite.config.ts",
    "vite.config.js",
    "vite.config.mts",
    "vite.config.mjs",
    "turbo.json",
    "nx.json",
    "project.json",
}
SKIP_PATH_PREFIXES = (
    "formula/",
    "homebrew/",
    "third_party/",
    "vendor/",
)

CODE_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".swift",
    ".rb",
    ".php",
    ".cs",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".zig",
    ".vue",
    ".svelte",
    ".sh",
}

MAX_FILE_BYTES = 512_000
MAX_HITS_PER_PATTERN = 6
INSPECTOR_RUNTIMES = ("claude-code", "codex", "grok-build")
VERDICTS = ("present", "partial", "absent", "unknown")
LAYERS = ("code", "docs", "config")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = run_command(["git", *args], cwd=cwd)
    if check and completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "git failed")
    return completed


def license_token(license_field: str | None) -> str | None:
    if not license_field or not isinstance(license_field, str):
        return None
    head = license_field.split(";")[0]
    head = head.split("(")[0].strip()
    return head or None


def is_osi_open_source(license_field: str | None) -> bool:
    token = license_token(license_field)
    return token in OSI_LICENSE_IDS if token else False


def expand_checkout_path(raw: str | None) -> Path | None:
    if not raw or not isinstance(raw, str):
        return None
    return Path(raw).expanduser()


def owned_local_checkout(profile: dict) -> Path | None:
    inspect_source = profile.get("inspect_source")
    if not isinstance(inspect_source, dict):
        return None
    if inspect_source.get("kind") != "owned-local":
        return None
    path = expand_checkout_path(inspect_source.get("path"))
    if path is None or not path.is_dir():
        return None
    return path


def is_inspectable(profile: dict) -> bool:
    if owned_local_checkout(profile) is not None:
        return True
    return bool(profile.get("source_url")) and is_osi_open_source(profile.get("license"))


def load_feature_catalog(path: Path | None = None) -> dict:
    return read_json(path or FEATURE_CATALOG)


def list_inspectable_products(competitors_dir: Path | None = None) -> list[dict]:
    root = competitors_dir or COMPETITORS
    rows: list[dict] = []
    for path in sorted(root.glob("*.json")):
        data = read_json(path)
        if not is_inspectable(data):
            continue
        local = owned_local_checkout(data)
        rows.append(
            {
                "id": data["id"],
                "name": data["name"],
                "license": data.get("license"),
                "license_token": license_token(data.get("license")),
                "source_url": data.get("source_url"),
                "source_kind": "owned-local" if local else "public-git",
                "checkout": str(local) if local else None,
                "runtime_model": data.get("runtime_model"),
            }
        )
    return rows


def classify_path(relative: str) -> str | None:
    posix = relative.replace("\\", "/")
    lowered = posix.lower()
    if lowered.startswith(SKIP_PATH_PREFIXES):
        return None
    parts = [part.lower() for part in posix.split("/") if part]
    name = parts[-1] if parts else ""
    if name in SKIP_FILE_NAMES:
        return None
    if name in {"license", "license.md", "copying", "copying.md"}:
        return None
    if any(part in SKIP_DIRS or part.startswith(".") for part in parts[:-1]):
        return None
    if any(part in DOC_DIRS for part in parts[:-1]) or name in DOC_NAMES or name.endswith(".md"):
        return "docs"
    suffix = Path(name).suffix.lower()
    if name in CONFIG_NAMES or (suffix in CONFIG_SUFFIXES and suffix not in CODE_SUFFIXES):
        return "config"
    if suffix in CODE_SUFFIXES:
        return "code"
    if suffix in SKIP_SUFFIXES:
        return None
    return None


def iter_text_files(checkout: Path) -> Iterable[tuple[str, Path, str, str]]:
    for dirpath, dirnames, filenames in os.walk(checkout):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS and not name.startswith(".")]
        root = Path(dirpath)
        for name in filenames:
            path = root / name
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(checkout).as_posix()
            except ValueError:
                continue
            layer = classify_path(relative)
            if layer is None:
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size <= 0 or size > MAX_FILE_BYTES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            yield relative, path, layer, text


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _line_number(starts: list[int], position: int) -> int:
    lo, hi = 0, len(starts) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if starts[mid] <= position:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi + 1


def _line_at(text: str, starts: list[int], line_no: int) -> str:
    begin = starts[line_no - 1]
    end = starts[line_no] - 1 if line_no < len(starts) else len(text)
    if end < begin:
        return ""
    line = text[begin:end]
    return line[:-1] if line.endswith("\r") else line


def compile_catalog(catalog: dict) -> list[dict]:
    compiled: list[dict] = []
    for feature in catalog.get("features", []):
        patterns = []
        for pattern in feature.get("patterns", []):
            patterns.append(
                {
                    "id": pattern["id"],
                    "weight": pattern.get("weight", "medium"),
                    "regex": re.compile(pattern["regex"], re.IGNORECASE | re.MULTILINE),
                }
            )
        compiled.append({**feature, "compiled": patterns})
    return compiled


def scan_checkout(checkout: Path, catalog: dict | None = None) -> dict:
    catalog = catalog or load_feature_catalog()
    compiled = compile_catalog(catalog)
    hits_by_feature: dict[str, list[dict]] = {feature["id"]: [] for feature in compiled}
    files_scanned = 0
    for relative, _path, layer, text in iter_text_files(checkout):
        files_scanned += 1
        line_starts = None
        for feature in compiled:
            bucket = hits_by_feature[feature["id"]]
            for pattern in feature["compiled"]:
                remaining = MAX_HITS_PER_PATTERN
                for match in pattern["regex"].finditer(text):
                    if remaining <= 0:
                        break
                    if line_starts is None:
                        line_starts = _line_starts(text)
                    line_no = _line_number(line_starts, match.start())
                    line = _line_at(text, line_starts, line_no)
                    bucket.append(
                        {
                            "path": relative,
                            "line": line_no,
                            "snippet": line.strip()[:240],
                            "layer": layer,
                            "pattern_id": pattern["id"],
                            "weight": pattern["weight"],
                        }
                    )
                    remaining -= 1
    features: dict[str, dict] = {}
    for feature in compiled:
        hits = hits_by_feature[feature["id"]]
        verdict = verdict_from_hits(hits, feature.get("present_requires", "code"))
        features[feature["id"]] = {
            "verdict": verdict,
            "notes": _notes_for(feature["id"], verdict, hits),
            "evidence": [
                {
                    "path": hit["path"],
                    "line": hit["line"],
                    "snippet": hit["snippet"],
                    "layer": hit["layer"],
                    "pattern_id": hit["pattern_id"],
                }
                for hit in _preferred_hits(hits)
            ],
        }
    return {
        "schema_version": "inspect-0.1",
        "files_scanned": files_scanned,
        "feature_ids": [feature["id"] for feature in compiled],
        "features": features,
    }


def _preferred_hits(hits: list[dict], limit: int = 5) -> list[dict]:
    rank = {"code": 0, "config": 1, "docs": 2}
    weight = {"strong": 0, "medium": 1, "weak": 2}
    ordered = sorted(
        hits,
        key=lambda hit: (
            rank.get(hit["layer"], 9),
            weight.get(hit["weight"], 9),
            hit["path"],
            hit["line"],
        ),
    )
    return ordered[:limit]


def verdict_from_hits(hits: list[dict], present_requires: str = "code") -> str:
    if not hits:
        return "absent"
    code_hits = [hit for hit in hits if hit["layer"] == "code"]
    strong_code = [hit for hit in code_hits if hit.get("weight") == "strong"]
    medium_or_strong_code = [hit for hit in code_hits if hit.get("weight") in {"strong", "medium"}]
    if present_requires == "code":
        if strong_code or len(medium_or_strong_code) >= 2:
            return "present"
        if code_hits:
            return "partial"
        return "partial"
    if hits:
        return "present"
    return "absent"


def _notes_for(feature_id: str, verdict: str, hits: list[dict]) -> str:
    if verdict == "absent":
        return "No catalog pattern matched in the scanned checkout."
    layers = sorted({hit["layer"] for hit in hits})
    code_n = sum(1 for hit in hits if hit["layer"] == "code")
    if verdict == "present":
        return f"Code evidence for {feature_id} ({code_n} code hits; layers={','.join(layers)})."
    if code_n:
        return f"Weak or single-signal code match for {feature_id}; treating as partial."
    return f"Docs/config-only matches for {feature_id}; not treated as present."


def checkout_commit(checkout: Path) -> str | None:
    if not (checkout / ".git").exists() and not (checkout / ".git").is_file():
        result = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=checkout)
        if result.returncode != 0 or result.stdout.strip() != "true":
            return None
    result = git(checkout, "rev-parse", "HEAD", check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _copy_regular_file(src: str, dst: str, *, follow_symlinks: bool = True) -> None:
    path = Path(src)
    try:
        if path.is_socket() or path.is_fifo() or path.is_char_device():
            return
        shutil.copy2(src, dst, follow_symlinks=False)
    except OSError:
        return


def materialize_checkout(
    dest: Path,
    *,
    source_url: str | None = None,
    checkout: Path | None = None,
    ref: str | None = None,
) -> dict:
    if dest.exists():
        raise FileExistsError(f"checkout already exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    method = "copy"
    if checkout is not None:
        if not checkout.is_dir():
            raise FileNotFoundError(f"checkout path not found: {checkout}")
        shutil.copytree(
            checkout,
            dest,
            ignore=shutil.ignore_patterns(
                ".git",
                ".tachyon",
                "node_modules",
                "dist",
                "out",
                ".turbo",
                ".next",
                "coverage",
            ),
            ignore_dangling_symlinks=True,
            copy_function=_copy_regular_file,
        )
    elif source_url:
        method = "clone"
        command = ["git", "clone", "--depth", "1"]
        if ref:
            command.extend(["--branch", ref])
        command.extend([source_url, str(dest)])
        completed = run_command(command, cwd=dest.parent)
        if completed.returncode != 0:
            raise RuntimeError(
                f"git clone failed for {source_url}: {completed.stderr.strip() or completed.stdout.strip()}"
            )
    else:
        raise ValueError("materialize_checkout requires source_url or checkout")
    return {
        "method": method,
        "source_url": source_url,
        "commit": checkout_commit(dest),
        "path": "checkout",
        "ref": ref,
    }


def build_inspection(
    product_id: str,
    scan: dict,
    *,
    inspector_kind: str = "static",
    inspector_runtime: str | None = "static",
    model: str | None = None,
    checkout_meta: dict | None = None,
) -> dict:
    return {
        "schema_version": "inspect-0.1",
        "product_id": product_id,
        "inspector": {
            "kind": inspector_kind,
            "runtime": inspector_runtime,
            "model": model,
        },
        "checkout": checkout_meta or {},
        "generated_at": utc_now(),
        "files_scanned": scan.get("files_scanned"),
        "features": scan["features"],
    }


def validate_feature_catalog(catalog: dict | None = None) -> list[str]:
    catalog = catalog or load_feature_catalog()
    errors: list[str] = []
    features = catalog.get("features")
    if not isinstance(features, list) or not features:
        return ["feature catalog must list features"]
    seen: set[str] = set()
    for index, feature in enumerate(features):
        prefix = f"features[{index}]"
        if not isinstance(feature, dict):
            errors.append(f"{prefix} must be an object")
            continue
        feature_id = feature.get("id")
        if not isinstance(feature_id, str) or not re.fullmatch(r"[a-z0-9_]+", feature_id):
            errors.append(f"{prefix}.id is invalid")
        elif feature_id in seen:
            errors.append(f"{prefix}.id duplicates {feature_id}")
        else:
            seen.add(feature_id)
        for key in ("group", "title", "definition"):
            if not isinstance(feature.get(key), str) or not feature.get(key):
                errors.append(f"{prefix}.{key} must be a non-empty string")
        patterns = feature.get("patterns")
        if not isinstance(patterns, list) or not patterns:
            errors.append(f"{prefix}.patterns must be a non-empty list")
            continue
        pattern_ids: set[str] = set()
        for p_index, pattern in enumerate(patterns):
            p_prefix = f"{prefix}.patterns[{p_index}]"
            if not isinstance(pattern, dict):
                errors.append(f"{p_prefix} must be an object")
                continue
            pattern_id = pattern.get("id")
            if not isinstance(pattern_id, str) or not pattern_id:
                errors.append(f"{p_prefix}.id is required")
            elif pattern_id in pattern_ids:
                errors.append(f"{p_prefix}.id duplicates {pattern_id}")
            else:
                pattern_ids.add(pattern_id)
            if pattern.get("weight") not in {"strong", "medium", "weak"}:
                errors.append(f"{p_prefix}.weight must be strong, medium, or weak")
            try:
                re.compile(pattern.get("regex", ""), re.IGNORECASE)
            except re.error as exc:
                errors.append(f"{p_prefix}.regex is invalid: {exc}")
    runtimes = catalog.get("inspector_runtimes", [])
    if list(runtimes) != list(INSPECTOR_RUNTIMES):
        errors.append("inspector_runtimes must be claude-code, codex, grok-build")
    return errors


def citation_errors(inspection: dict, checkout: Path) -> list[str]:
    errors: list[str] = []
    features = inspection.get("features")
    if not isinstance(features, dict):
        return ["inspection.features must be an object"]
    for feature_id, row in features.items():
        if not isinstance(row, dict):
            errors.append(f"features.{feature_id} must be an object")
            continue
        verdict = row.get("verdict")
        if verdict not in VERDICTS:
            errors.append(f"features.{feature_id}.verdict is invalid")
        evidence = row.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"features.{feature_id}.evidence must be a list")
            continue
        if verdict in {"present", "partial"} and not evidence:
            errors.append(f"features.{feature_id}: {verdict} requires evidence")
        for index, item in enumerate(evidence):
            prefix = f"features.{feature_id}.evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            rel = item.get("path")
            line_no = item.get("line")
            snippet = item.get("snippet")
            layer = item.get("layer")
            if not isinstance(rel, str) or not rel or rel.startswith("/") or ".." in Path(rel).parts:
                errors.append(f"{prefix}.path must be a relative checkout path")
                continue
            if layer not in LAYERS:
                errors.append(f"{prefix}.layer is invalid")
            if not isinstance(line_no, int) or line_no < 1:
                errors.append(f"{prefix}.line must be a positive integer")
                continue
            if not isinstance(snippet, str) or not snippet.strip():
                errors.append(f"{prefix}.snippet must be a non-empty string")
                continue
            target = checkout / rel
            if not target.is_file():
                errors.append(f"{prefix}: missing file {rel}")
                continue
            try:
                lines = target.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                errors.append(f"{prefix}: cannot read {rel}")
                continue
            if line_no > len(lines):
                errors.append(f"{prefix}: line {line_no} out of range in {rel}")
                continue
            haystack = lines[line_no - 1]
            needle = snippet.strip()
            if needle not in haystack and needle.casefold() not in haystack.casefold():
                errors.append(f"{prefix}: snippet not found on {rel}:{line_no}")
    return errors


def validate_inspection(inspection: dict, catalog: dict, checkout: Path) -> list[str]:
    errors: list[str] = []
    if inspection.get("schema_version") != "inspect-0.1":
        errors.append("schema_version must be inspect-0.1")
    if not isinstance(inspection.get("product_id"), str) or not inspection.get("product_id"):
        errors.append("product_id is required")
    inspector = inspection.get("inspector")
    if not isinstance(inspector, dict):
        errors.append("inspector must be an object")
    else:
        if inspector.get("kind") not in {"static", "agent"}:
            errors.append("inspector.kind must be static or agent")
        runtime = inspector.get("runtime")
        if runtime not in {None, "static", *INSPECTOR_RUNTIMES}:
            errors.append("inspector.runtime must be static, claude-code, codex, or grok-build")
        if inspector.get("kind") == "agent" and runtime not in INSPECTOR_RUNTIMES:
            errors.append("agent inspector.runtime must be claude-code, codex, or grok-build")
    expected = [feature["id"] for feature in catalog.get("features", [])]
    features = inspection.get("features")
    if not isinstance(features, dict):
        errors.append("features must be an object")
    else:
        missing = [feature_id for feature_id in expected if feature_id not in features]
        extra = [feature_id for feature_id in features if feature_id not in expected]
        if missing:
            errors.append(f"missing feature verdicts: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown feature ids: {', '.join(extra)}")
    errors.extend(citation_errors(inspection, checkout))
    return errors


def fixture_path(name: str) -> Path:
    path = FIXTURES / name
    if not path.is_dir():
        raise FileNotFoundError(f"unknown inspect fixture: {name}")
    return path


def format_matrix(rows: list[dict], feature_ids: list[str] | None = None) -> str:
    if not rows:
        return "No inspectable products."
    wanted = feature_ids or [
        "dag_orchestration",
        "task_graph",
        "worktree_isolation",
        "guest_claude_code",
        "guest_codex",
        "guest_grok",
    ]
    header = ["product", *wanted]
    table = [header]
    for row in rows:
        features = row.get("features") or {}
        table.append(
            [row.get("id", "?"), *[features.get(fid, {}).get("verdict", "-") for fid in wanted]]
        )
    widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]
    lines = []
    for index, line in enumerate(table):
        rendered = "  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(line))
        lines.append(rendered)
        if index == 0:
            lines.append("  ".join("-" * width for width in widths))
    return "\n".join(lines)


def prepare_inspect_run(
    *,
    run_dir: Path,
    product: dict,
    checkout_src: Path | None,
    source_url: str | None,
    ref: str | None,
    catalog: dict | None = None,
) -> dict:
    if run_dir.exists():
        raise FileExistsError(f"Run already exists: {run_dir}")
    catalog = catalog or load_feature_catalog()
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    checkout = run_dir / "checkout"
    meta = materialize_checkout(
        checkout,
        source_url=source_url,
        checkout=checkout_src,
        ref=ref,
    )
    shutil.copy2(INSPECT_PROMPT, run_dir / "prompt.md")
    write_json(run_dir / "product.json", product)
    write_json(run_dir / "feature-catalog.json", catalog)
    scan = scan_checkout(checkout, catalog)
    write_json(run_dir / "detectors.json", scan)
    created = utc_now()
    result = {
        "schema_version": "inspect-0.1",
        "kind": "source-inspect",
        "run_id": run_dir.name,
        "status": "prepared",
        "created_at": created,
        "updated_at": created,
        "product": {
            "id": product["id"],
            "name": product.get("name"),
            "class": product.get("class"),
            "license": product.get("license"),
            "source_url": product.get("source_url"),
        },
        "inspector": {
            "kind": None,
            "runtime": None,
            "model": None,
        },
        "checkout": meta,
        "paths": {
            "checkout": "checkout",
            "prompt": "prompt.md",
            "detectors": "detectors.json",
            "inspection": "inspection.json",
            "catalog": "feature-catalog.json",
            "product": "product.json",
            "artifacts": "artifacts",
        },
        "events": [{"at": created, "type": "prepared", "message": "Checkout materialized and detectors ran"}],
    }
    write_json(run_dir / "result.json", result)
    return result


def write_static_inspection(run_dir: Path, *, model: str | None = None) -> dict:
    result = read_json(run_dir / "result.json")
    if result.get("kind") != "source-inspect":
        raise ValueError(f"{run_dir} is not a source-inspect run")
    scan = read_json(run_dir / "detectors.json")
    product_id = result["product"]["id"]
    inspection = build_inspection(
        product_id,
        scan,
        inspector_kind="static",
        inspector_runtime="static",
        model=model,
        checkout_meta=result.get("checkout"),
    )
    write_json(run_dir / "inspection.json", inspection)
    now = utc_now()
    result["updated_at"] = now
    result["inspector"] = inspection["inspector"]
    result.setdefault("events", []).append(
        {"at": now, "type": "scanned", "message": "Static detectors wrote inspection.json"}
    )
    write_json(run_dir / "result.json", result)
    return inspection


def verify_inspect_run(run_dir: Path) -> dict:
    result_file = run_dir / "result.json"
    inspection_file = run_dir / "inspection.json"
    checkout = run_dir / "checkout"
    catalog_file = run_dir / "feature-catalog.json"
    if not result_file.is_file() or not checkout.is_dir():
        raise FileNotFoundError(f"Invalid inspect run directory: {run_dir}")
    result = read_json(result_file)
    if result.get("kind") != "source-inspect":
        raise ValueError(f"{run_dir} is not a source-inspect run")
    if not inspection_file.is_file():
        raise FileNotFoundError("inspection.json is missing; run inspect-scan or an agent first")
    catalog = read_json(catalog_file) if catalog_file.is_file() else load_feature_catalog()
    inspection = read_json(inspection_file)
    errors = validate_inspection(inspection, catalog, checkout)
    now = utc_now()
    passed = not errors
    result["status"] = "pass" if passed else "fail"
    result["updated_at"] = now
    result["inspector"] = inspection.get("inspector", result.get("inspector"))
    result["verification"] = {
        "passed": passed,
        "error_count": len(errors),
        "errors": errors,
        "ended_at": now,
    }
    result.setdefault("events", []).append(
        {
            "at": now,
            "type": "verified",
            "message": "Inspection citations verified" if passed else "Inspection verification failed",
        }
    )
    write_json(result_file, result)
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(exist_ok=True)
    (artifacts / "inspect-verify.txt").write_text(
        "OK\n" if passed else "\n".join(errors) + "\n",
        encoding="utf-8",
    )
    return result
