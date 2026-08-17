#!/usr/bin/env python3
"""Minimal benchmark harness for Tachyon ADE Bench.

The harness is intentionally dependency-free. It prepares task worktrees,
captures product-independent verification artifacts, and performs lightweight
schema checks for tracked benchmark metadata.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
COMPETITORS = ROOT / "competitors"
TASKS = ROOT / "tasks"
RUNS = ROOT / "runs"

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import source_inspect as inspect_lib  # noqa: E402


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


def run_command(
    command: list[str],
    cwd: Path,
    check: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        check=check,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_command(["git", *args], cwd=cwd, check=check)


def collect_final_diff(worktree: Path) -> str:
    """Return a patch that includes tracked changes and untracked text files."""
    tracked = git(worktree, "diff", "--no-ext-diff", check=False).stdout
    untracked = git(worktree, "ls-files", "--others", "--exclude-standard", check=False).stdout.splitlines()
    chunks = [tracked] if tracked else []
    for relative in untracked:
        path = worktree / relative
        if not path.is_file():
            continue
        diff = run_command(["git", "diff", "--no-index", "--", "/dev/null", str(path)], cwd=worktree)
        if diff.stdout:
            chunks.append(diff.stdout)
    return "\n".join(chunk.rstrip() for chunk in chunks if chunk).rstrip() + ("\n" if chunks else "")


def initial_metrics(prepared_at: str) -> dict:
    return {
        "intervention_burden": {
            "count": 0,
            "minutes": 0,
            "operator_decision_points": 0,
            "interventions": [],
        },
        "timing": {
            "prepared_at": prepared_at,
            "verified_at": None,
            "time_to_verified_change_seconds": None,
            "verification_elapsed_seconds": None,
        },
        "cost": {
            "usd": None,
            "input_tokens": None,
            "output_tokens": None,
            "tool_calls": None,
        },
        "artifact_completeness": {
            "has_result": True,
            "has_prompt": True,
            "has_diff": False,
            "has_verifier_stdout": False,
            "has_verifier_stderr": False,
            "has_git_status": False,
        },
        "isolation": {
            "verifier_refreshed_from_canonical": False,
            "workspace_modified": False,
            "untracked_files_count": 0,
            "suspected_scope_violations": 0,
        },
        "review_burden": {
            "changed_files": None,
            "diff_lines": None,
            "final_diff_bytes": None,
        },
        "failure_recovery": {
            "retry_count": 0,
            "rollback_count": 0,
            "recovered_from_failure": None,
        },
    }


def parse_iso(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def count_untracked(status: str) -> int:
    return sum(1 for line in status.splitlines() if line.startswith("?? "))


def count_changed_files(status: str) -> int:
    return sum(1 for line in status.splitlines() if line.strip())


def product_path(product_id: str) -> Path:
    return COMPETITORS / f"{product_id}.json"


def task_path(task_id: str) -> Path:
    return TASKS / task_id / "task.json"


def list_products(_: argparse.Namespace) -> int:
    for path in sorted(COMPETITORS.glob("*.json")):
        data = read_json(path)
        print(f"{data['id']}\t{data['name']}\t{data['class']}\t{data['runner']['kind']}")
    return 0


def list_tasks(_: argparse.Namespace) -> int:
    for path in sorted(TASKS.glob("*/task.json")):
        data = read_json(path)
        print(f"{data['id']}\t{data['title']}\t{data['category']}\t{data['difficulty']}")
    return 0


def validate_competitor(path: Path, task_ids: set[str] | None = None) -> list[str]:
    required = [
        "id",
        "name",
        "class",
        "homepage",
        "source_url",
        "license",
        "runner",
        "inclusion",
        "runtime_model",
        "research",
        "research_status",
        "updated_at",
    ]
    data = read_json(path)
    optional = {
        "pricing_model",
        "public_stack_signals",
        "capabilities_to_probe",
        "moat_hypotheses",
        "setup_notes",
        "guest_runtimes",
        "own_runtimes",
        "runtime_model_notes",
        "inspect_source",
    }
    errors = [f"{path}: missing {key}" for key in required if key not in data]
    for key in sorted(set(data) - set(required) - optional):
        errors.append(f"{path}: {key} is not allowed")
    for key in ["public_stack_signals", "capabilities_to_probe", "moat_hypotheses", "setup_notes", "guest_runtimes", "own_runtimes"]:
        if key in data and not isinstance(data[key], list):
            errors.append(f"{path}: {key} must be a list")
    inspect_source = data.get("inspect_source")
    if inspect_source is not None:
        if not isinstance(inspect_source, dict):
            errors.append(f"{path}: inspect_source must be an object")
        else:
            allowed = {"kind", "path", "notes"}
            for key in sorted(set(inspect_source) - allowed):
                errors.append(f"{path}: inspect_source.{key} is not allowed")
            if inspect_source.get("kind") not in {"owned-local", "public-git"}:
                errors.append(f"{path}: inspect_source.kind must be owned-local or public-git")
            if inspect_source.get("kind") == "owned-local":
                if not isinstance(inspect_source.get("path"), str) or not inspect_source.get("path"):
                    errors.append(f"{path}: inspect_source.path is required for owned-local")
    if data.get("id") and path.stem != data["id"]:
        errors.append(f"{path}: id must match filename")
    if data.get("class") not in {"A-local-ade", "B-enterprise-agentic-platform"}:
        errors.append(f"{path}: class must be a known benchmark class")
    if data.get("runtime_model") not in {"guest-cli", "hybrid", "first-party", "unknown"}:
        errors.append(f"{path}: runtime_model must be guest-cli, hybrid, first-party, or unknown")
    if "runtime_model_notes" in data and not isinstance(data["runtime_model_notes"], str):
        errors.append(f"{path}: runtime_model_notes must be a string")
    for list_key in ("guest_runtimes", "own_runtimes"):
        values = data.get(list_key)
        if isinstance(values, list):
            for index, item in enumerate(values):
                if not isinstance(item, str) or not item:
                    errors.append(f"{path}: {list_key}[{index}] must be a non-empty string")
    if "runner" in data and "kind" not in data["runner"]:
        errors.append(f"{path}: runner.kind is required")
    elif "runner" in data and data["runner"].get("kind") not in {"manual", "cli", "api"}:
        errors.append(f"{path}: runner.kind must be manual, cli, or api")
    research = data.get("research")
    if not isinstance(research, dict):
        errors.append(f"{path}: research must be an object")
    else:
        errors.extend(validate_competitor_research(path, research, task_ids or set()))
    return errors


def validate_competitor_research(path: Path, research: dict, task_ids: set[str]) -> list[str]:
    errors: list[str] = []
    allowed_source_kinds = {
        "official-site",
        "official-docs",
        "source-repo",
        "package-manifest",
        "app-store",
        "owned",
    }
    required = [
        "last_reviewed",
        "confidence",
        "sources",
        "positioning",
        "stack",
        "infrastructure",
        "features",
        "benchmarking",
        "moat",
    ]
    allowed_research_keys = set(required)
    errors.extend(f"{path}: research.{key} is required" for key in required if key not in research)
    for key in sorted(set(research) - allowed_research_keys):
        errors.append(f"{path}: research.{key} is not allowed")
    if not isinstance(research.get("last_reviewed"), str) or not research.get("last_reviewed"):
        errors.append(f"{path}: research.last_reviewed must be a non-empty string")
    if research.get("confidence") not in {"owned", "official-sourced", "partial-official", "seed"}:
        errors.append(f"{path}: research.confidence is invalid")
    sources = research.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{path}: research.sources must contain at least one source")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"{path}: research.sources[{index}] must be an object")
                continue
            for key in sorted(set(source) - {"url", "kind", "notes"}):
                errors.append(f"{path}: research.sources[{index}].{key} is not allowed")
            if not source.get("url") or not source.get("kind") or not source.get("notes"):
                errors.append(f"{path}: every research source needs url, kind, and notes")
                continue
            if source["kind"] not in allowed_source_kinds:
                errors.append(f"{path}: research.sources[{index}].kind is invalid")
            if not isinstance(source["url"], str) or "://" not in source["url"]:
                errors.append(f"{path}: research.sources[{index}].url must be a URI")
            if not isinstance(source["notes"], str):
                errors.append(f"{path}: research.sources[{index}].notes must be a string")
    if not isinstance(research.get("positioning"), str) or not research.get("positioning"):
        errors.append(f"{path}: research.positioning must be a non-empty string")
    if not isinstance(research.get("infrastructure"), list):
        errors.append(f"{path}: research.infrastructure must be a list")
    stack = research.get("stack")
    if not isinstance(stack, dict):
        errors.append(f"{path}: research.stack must be an object")
    else:
        for key in sorted(set(stack) - {"runtime", "frontend", "backend", "packaging", "data", "unknowns"}):
            errors.append(f"{path}: research.stack.{key} is not allowed")
        for key in ["runtime", "frontend", "backend", "packaging", "data", "unknowns"]:
            if not isinstance(stack.get(key), list):
                errors.append(f"{path}: research.stack.{key} must be a list")
    features = research.get("features")
    feature_keys = [
        "agent_support",
        "orchestration",
        "workspace_isolation",
        "review_shipping",
        "remote_mobile",
        "context_memory",
        "integrations",
    ]
    if not isinstance(features, dict):
        errors.append(f"{path}: research.features must be an object")
    else:
        for key in sorted(set(features) - set(feature_keys)):
            errors.append(f"{path}: research.features.{key} is not allowed")
        for key in feature_keys:
            if not isinstance(features.get(key), list):
                errors.append(f"{path}: research.features.{key} must be a list")
    benchmarking = research.get("benchmarking")
    if not isinstance(benchmarking, dict):
        errors.append(f"{path}: research.benchmarking must be an object")
    else:
        for key in sorted(set(benchmarking) - {"readiness", "install_surface", "parity_risks", "suggested_first_tasks"}):
            errors.append(f"{path}: research.benchmarking.{key} is not allowed")
        if benchmarking.get("readiness") not in {
            "manual-ready",
            "needs-install",
            "enterprise-gated",
            "owned-reference",
            "research-only",
        }:
            errors.append(f"{path}: research.benchmarking.readiness is invalid")
        for key in ["install_surface", "parity_risks", "suggested_first_tasks"]:
            if not isinstance(benchmarking.get(key), list):
                errors.append(f"{path}: research.benchmarking.{key} must be a list")
        suggested = benchmarking.get("suggested_first_tasks")
        if isinstance(suggested, list):
            for task_id in suggested:
                if not isinstance(task_id, str):
                    errors.append(f"{path}: research.benchmarking.suggested_first_tasks must contain strings")
                elif task_ids and task_id not in task_ids:
                    errors.append(f"{path}: research.benchmarking.suggested_first_tasks unknown task {task_id}")
    moat = research.get("moat")
    if not isinstance(moat, dict):
        errors.append(f"{path}: research.moat must be an object")
    else:
        for key in sorted(set(moat) - {"hypotheses", "evidence", "unknowns"}):
            errors.append(f"{path}: research.moat.{key} is not allowed")
        for key in ["hypotheses", "evidence", "unknowns"]:
            if not isinstance(moat.get(key), list):
                errors.append(f"{path}: research.moat.{key} must be a list")
    return errors


def validate_task(path: Path) -> list[str]:
    required = ["id", "title", "category", "difficulty", "prompt", "repo", "verify"]
    data = read_json(path)
    task_dir = path.parent
    errors = [f"{path}: missing {key}" for key in required if key not in data]
    if data.get("id") and task_dir.name != data["id"]:
        errors.append(f"{path}: id must match directory name")
    if data.get("difficulty") not in {"smoke", "small", "medium", "large"}:
        errors.append(f"{path}: difficulty must be smoke, small, medium, or large")
    if data.get("prompt") and not (task_dir / data["prompt"]).is_file():
        errors.append(f"{path}: prompt file not found")
    if data.get("repo") and not (task_dir / data["repo"]).is_dir():
        errors.append(f"{path}: repo directory not found")
    post_prepare = data.get("post_prepare")
    if post_prepare is not None:
        if not isinstance(post_prepare, str) or not post_prepare:
            errors.append(f"{path}: post_prepare must be a non-empty string")
        elif not (task_dir / post_prepare).is_dir():
            errors.append(f"{path}: post_prepare directory not found")
    command = data.get("verify", {}).get("command")
    if not isinstance(command, list) or not command:
        errors.append(f"{path}: verify.command must be a non-empty string array")
    elif any(not isinstance(part, str) for part in command):
        errors.append(f"{path}: verify.command must contain only strings")
    directory = data.get("verify", {}).get("directory")
    if not isinstance(directory, str) or not directory:
        errors.append(f"{path}: verify.directory is required")
    elif not (task_dir / directory).is_dir():
        errors.append(f"{path}: verify.directory not found")
    return errors


def check(_: argparse.Namespace) -> int:
    errors: list[str] = []
    task_ids = {read_json(path)["id"] for path in sorted(TASKS.glob("*/task.json"))}
    for path in sorted(COMPETITORS.glob("*.json")):
        errors.extend(validate_competitor(path, task_ids))
    for path in sorted(TASKS.glob("*/task.json")):
        errors.extend(validate_task(path))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("OK: competitor profiles and tasks are structurally valid")
    return 0


def prepare(args: argparse.Namespace) -> int:
    product_file = product_path(args.product)
    task_file = task_path(args.task)
    if not product_file.is_file():
        print(f"Unknown product: {args.product}", file=sys.stderr)
        return 2
    if not task_file.is_file():
        print(f"Unknown task: {args.task}", file=sys.stderr)
        return 2

    product = read_json(product_file)
    task = read_json(task_file)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{timestamp}-{args.product}-{args.task}-{uuid.uuid4().hex[:8]}"
    run_dir = RUNS / run_id
    if run_dir.exists():
        print(f"Run already exists: {run_dir}", file=sys.stderr)
        return 2

    task_dir = task_file.parent
    worktree = run_dir / "worktree"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    shutil.copytree(task_dir / task["repo"], worktree)
    verifier_dir = task.get("verify", {}).get("directory")
    if not verifier_dir:
        print(f"Task {task['id']} is missing verify.directory", file=sys.stderr)
        return 2
    shutil.copytree(task_dir / verifier_dir, run_dir / verifier_dir)
    shutil.copy2(task_dir / task["prompt"], run_dir / "prompt.md")
    shutil.copy2(task_file, run_dir / "task.json")
    shutil.copy2(product_file, run_dir / "product.json")

    init = git(worktree, "init", "-b", "main", check=False)
    if init.returncode != 0:
        git(worktree, "init")
        git(worktree, "symbolic-ref", "HEAD", "refs/heads/main")
    git(worktree, "add", ".")
    git(
        worktree,
        "-c",
        "user.name=Tachyon ADE Bench",
        "-c",
        "user.email=bench@example.invalid",
        "commit",
        "-m",
        "baseline fixture",
    )
    baseline = git(worktree, "rev-parse", "HEAD").stdout.strip()
    post_prepare_dir = task.get("post_prepare")
    if post_prepare_dir:
        shutil.copytree(task_dir / post_prepare_dir, worktree, dirs_exist_ok=True)
    initial_status = git(worktree, "status", "--short", check=False).stdout
    initial_diff = collect_final_diff(worktree)
    (artifacts / "initial-git-status.txt").write_text(initial_status, encoding="utf-8")
    (artifacts / "initial-dirty.diff").write_text(initial_diff, encoding="utf-8")

    created = utc_now()
    result = {
        "schema_version": "0.1",
        "run_id": run_id,
        "status": "prepared",
        "created_at": created,
        "updated_at": created,
        "product": {
            "id": product["id"],
            "name": product["name"],
            "class": product["class"],
        },
        "task": {
            "id": task["id"],
            "title": task["title"],
            "category": task["category"],
        },
        "benchmark_commit": current_benchmark_commit(),
        "fixture_baseline_commit": baseline,
        "human_interventions": None,
        "metrics": initial_metrics(created),
        "run_config": {
            "product_version": None,
            "runtime_model": product.get("runtime_model"),
            "guest_runtime": None,
            "own_runtime": None,
            "model": None,
            "network_policy": "unspecified",
            "time_budget_minutes": task.get("time_budget_minutes"),
            "cost_usd": None,
            "execution_surface": None,
            "notes": (
                "Fill null fields before publishing scored reports. "
                "For guest-cli/hybrid products, set guest_runtime + model; "
                "for hybrid/first-party, set own_runtime when the product agent ran the task. "
                "execution_surface: e.g. product-gui | product-cli | guest-cli-direct | install-smoke-only."
            ),
        },
        "paths": {
            "worktree": "worktree",
            "verifier": verifier_dir,
            "post_prepare": post_prepare_dir,
            "prompt": "prompt.md",
            "task": "task.json",
            "product": "product.json",
            "artifacts": "artifacts",
        },
        "verification": None,
        "events": [
            {
                "at": created,
                "type": "prepared",
                "message": (
                    "Fixture copied, baseline commit created, and post-prepare overlay applied"
                    if post_prepare_dir
                    else "Fixture copied and baseline commit created"
                ),
            }
        ],
    }
    write_json(run_dir / "result.json", result)

    print(f"Prepared run: {run_dir.relative_to(ROOT)}")
    print(f"Worktree: {worktree}")
    print(f"Prompt: {run_dir / 'prompt.md'}")
    return 0


def current_benchmark_commit() -> str | None:
    result = run_command(["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT)
    if result.returncode != 0:
        return None
    head = result.stdout.strip()
    status = run_command(["git", "status", "--short"], cwd=ROOT)
    return f"{head}-dirty" if status.stdout.strip() else head


def verify(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    result_file = run_dir / "result.json"
    task_file = run_dir / "task.json"
    worktree = run_dir / "worktree"
    artifacts = run_dir / "artifacts"
    if not result_file.is_file() or not task_file.is_file() or not worktree.is_dir():
        print(f"Invalid run directory: {run_dir}", file=sys.stderr)
        return 2

    result = read_json(result_file)
    task = read_json(task_file)
    command = task["verify"]["command"]
    verifier_dir_name = task.get("verify", {}).get("directory")
    if not verifier_dir_name:
        print(f"Task {task['id']} is missing verify.directory", file=sys.stderr)
        return 2
    source_verifier = TASKS / task["id"] / verifier_dir_name
    run_verifier = run_dir / verifier_dir_name
    if run_verifier.exists():
        shutil.rmtree(run_verifier)
    shutil.copytree(source_verifier, run_verifier)
    verify_cwd = run_verifier
    env = os.environ.copy()
    env["BENCH_WORKTREE"] = str(worktree)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started_at = dt.datetime.now(dt.timezone.utc)
    started = utc_now()
    completed = run_command(command, cwd=verify_cwd, env=env)
    ended_at = dt.datetime.now(dt.timezone.utc)
    ended = utc_now()

    artifacts.mkdir(exist_ok=True)
    (artifacts / "verify.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (artifacts / "verify.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    git_status = git(worktree, "status", "--short", check=False).stdout
    (artifacts / "git-status.txt").write_text(git_status, encoding="utf-8")
    (artifacts / "git-diff-stat.txt").write_text(git(worktree, "diff", "--stat", check=False).stdout, encoding="utf-8")
    final_diff = collect_final_diff(worktree)
    (artifacts / "final.diff").write_text(final_diff, encoding="utf-8")

    passed = completed.returncode == 0
    result["status"] = "pass" if passed else "fail"
    result["updated_at"] = ended
    result["verification"] = {
        "command": command,
        "started_at": started,
        "ended_at": ended,
        "elapsed_seconds": round((ended_at - started_at).total_seconds(), 3),
        "exit_code": completed.returncode,
        "passed": passed,
        "artifacts": {
            "stdout": "artifacts/verify.stdout.txt",
            "stderr": "artifacts/verify.stderr.txt",
            "git_status": "artifacts/git-status.txt",
            "git_diff_stat": "artifacts/git-diff-stat.txt",
            "final_diff": "artifacts/final.diff",
        },
    }
    metrics = result.setdefault("metrics", initial_metrics(result.get("created_at", started)))
    timing = metrics.setdefault("timing", initial_metrics(result.get("created_at", started))["timing"])
    timing["verified_at"] = ended
    timing["verification_elapsed_seconds"] = round((ended_at - started_at).total_seconds(), 3)
    prepared_at = parse_iso(timing.get("prepared_at") or result.get("created_at", started))
    if prepared_at:
        timing["time_to_verified_change_seconds"] = round((ended_at - prepared_at).total_seconds(), 3)
    metrics["artifact_completeness"] = {
        "has_result": True,
        "has_prompt": (run_dir / "prompt.md").is_file(),
        "has_diff": bool(final_diff.strip()),
        "has_verifier_stdout": (artifacts / "verify.stdout.txt").is_file(),
        "has_verifier_stderr": (artifacts / "verify.stderr.txt").is_file(),
        "has_git_status": (artifacts / "git-status.txt").is_file(),
    }
    metrics["isolation"] = {
        "verifier_refreshed_from_canonical": True,
        "workspace_modified": bool(git_status.strip()),
        "untracked_files_count": count_untracked(git_status),
        "suspected_scope_violations": 0,
    }
    metrics["review_burden"] = {
        "changed_files": count_changed_files(git_status),
        "diff_lines": len(final_diff.splitlines()) if final_diff else 0,
        "final_diff_bytes": len(final_diff.encode("utf-8")),
    }
    result.setdefault("events", []).append(
        {
            "at": ended,
            "type": "verified",
            "message": "Verifier passed" if passed else "Verifier failed",
        }
    )
    write_json(result_file, result)

    print(f"Verification {'passed' if passed else 'failed'} for {run_dir.relative_to(ROOT)}")
    print(f"Exit code: {completed.returncode}")
    return completed.returncode


def _resolve_run_dir(value: str) -> Path:
    run_dir = Path(value)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    return run_dir


def _inspect_source_args(args: argparse.Namespace) -> tuple[dict, Path | None, str | None]:
    if args.fixture:
        fixture_product = {
            "id": args.product or args.fixture.replace("_", "-"),
            "name": f"Fixture {args.fixture}",
            "class": "A-local-ade",
            "license": "MIT",
            "source_url": None,
            "runtime_model": "guest-cli",
        }
        if args.product:
            product_file = product_path(args.product)
            if product_file.is_file():
                fixture_product = read_json(product_file)
        return fixture_product, inspect_lib.fixture_path(args.fixture), None
    if not args.product:
        raise ValueError("--product is required unless --fixture is set")
    product_file = product_path(args.product)
    if not product_file.is_file():
        raise FileNotFoundError(f"Unknown product: {args.product}")
    product = read_json(product_file)
    if args.checkout:
        return product, Path(args.checkout).expanduser(), None
    local = inspect_lib.owned_local_checkout(product)
    if local is not None:
        return product, local, None
    if not inspect_lib.is_inspectable(product):
        raise ValueError(
            f"{args.product} is not inspectable (need OSI+source_url or inspect_source.owned-local). "
            "Use --checkout or --fixture."
        )
    return product, None, product.get("source_url")


def list_inspectable(_: argparse.Namespace) -> int:
    rows = inspect_lib.list_inspectable_products()
    for row in rows:
        origin = row.get("checkout") or row.get("source_url")
        print(f"{row['id']}\t{row['name']}\t{row['source_kind']}\t{row['license_token']}\t{origin}")
    print(f"# {len(rows)} inspectable products", file=sys.stderr)
    return 0


def inspect_check(_: argparse.Namespace) -> int:
    errors = inspect_lib.validate_feature_catalog()
    if not INSPECT_PROMPT_OK():
        errors.append("inspect/prompts/inspect-features.md is missing")
    for name in ("mini-ade", "empty-ade"):
        if not (inspect_lib.FIXTURES / name).is_dir():
            errors.append(f"missing inspect fixture: {name}")
    rows = inspect_lib.list_inspectable_products()
    if len(rows) < 1:
        errors.append("no inspectable products in competitors/")
    for row in rows:
        if row.get("source_kind") == "public-git" and not row.get("source_url"):
            errors.append(f"{row['id']}: public-git inspectable row missing source_url")
        if row.get("source_kind") == "owned-local" and not row.get("checkout"):
            errors.append(f"{row['id']}: owned-local inspectable row missing checkout")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        f"OK: inspection catalog valid; {len(rows)} inspectable products; "
        "inspector runtimes: claude-code, codex, grok-build"
    )
    return 0


def INSPECT_PROMPT_OK() -> bool:
    return inspect_lib.INSPECT_PROMPT.is_file()


def _prepare_inspect_dir(args: argparse.Namespace) -> Path:
    product, checkout_src, source_url = _inspect_source_args(args)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = args.product or args.fixture or "inspect"
    run_id = args.run_id or f"{timestamp}-{label}-inspect-{uuid.uuid4().hex[:8]}"
    run_dir = RUNS / run_id
    inspect_lib.prepare_inspect_run(
        run_dir=run_dir,
        product=product,
        checkout_src=checkout_src,
        source_url=source_url,
        ref=getattr(args, "ref", None),
    )
    return run_dir


def inspect_prepare(args: argparse.Namespace) -> int:
    try:
        run_dir = _prepare_inspect_dir(args)
    except (ValueError, FileNotFoundError, FileExistsError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Prepared inspect run: {run_dir.relative_to(ROOT)}")
    print(f"Checkout: {run_dir / 'checkout'}")
    print(f"Prompt: {run_dir / 'prompt.md'}")
    print("Detectors: detectors.json (hints). For Claude/Codex/Grok use --mode agent and write inspection.json")
    return 0


def inspect_scan(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(args.run_dir)
    try:
        inspection = inspect_lib.write_static_inspection(run_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Wrote {run_dir / 'inspection.json'} ({inspection['inspector']['kind']})")
    print(inspect_lib.format_matrix([{"id": inspection["product_id"], "features": inspection["features"]}]))
    return 0


def inspect_verify(args: argparse.Namespace) -> int:
    run_dir = _resolve_run_dir(args.run_dir)
    try:
        result = inspect_lib.verify_inspect_run(run_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    passed = result.get("verification", {}).get("passed")
    errors = result.get("verification", {}).get("errors") or []
    rel = run_dir.relative_to(ROOT) if run_dir.is_relative_to(ROOT) else run_dir
    if passed:
        print(f"Inspection verification passed for {rel}")
        return 0
    print(f"Inspection verification failed for {rel}", file=sys.stderr)
    for error in errors:
        print(error, file=sys.stderr)
    return 1


def inspect_run(args: argparse.Namespace) -> int:
    try:
        run_dir = _prepare_inspect_dir(args)
    except (ValueError, FileNotFoundError, FileExistsError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Prepared inspect run: {run_dir.relative_to(ROOT)}")
    if args.mode == "agent":
        print("Agent mode: open this directory in Claude Code, Codex, or Grok Build.")
        print("Provide prompt.md exactly. Write inspection.json only.")
        print(f"Then: python3 harness/bench.py inspect-verify {run_dir.relative_to(ROOT)}")
        return 0
    scan_ns = argparse.Namespace(run_dir=str(run_dir))
    scanned = inspect_scan(scan_ns)
    if scanned != 0:
        return scanned
    return inspect_verify(scan_ns)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tachyon ADE Bench harness")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("check", help="validate tracked benchmark metadata").set_defaults(func=check)
    subcommands.add_parser("list-products", help="list product profiles").set_defaults(func=list_products)
    subcommands.add_parser("list-tasks", help="list benchmark tasks").set_defaults(func=list_tasks)

    prepare_parser = subcommands.add_parser("prepare", help="prepare an isolated run directory")
    prepare_parser.add_argument("--product", required=True, help="product id from competitors/")
    prepare_parser.add_argument("--task", required=True, help="task id from tasks/")
    prepare_parser.add_argument("--run-id", help="stable run directory name")
    prepare_parser.set_defaults(func=prepare)

    verify_parser = subcommands.add_parser("verify", help="run a task verifier for a prepared run")
    verify_parser.add_argument("run_dir", help="run directory, for example runs/local-smoke")
    verify_parser.set_defaults(func=verify)

    subcommands.add_parser(
        "list-inspectable",
        help="list OSI-licensed products with a public source_url",
    ).set_defaults(func=list_inspectable)

    subcommands.add_parser(
        "inspect-check",
        help="validate the source-inspection catalog and inspectable roster",
    ).set_defaults(func=inspect_check)

    prepare_inspect = subcommands.add_parser(
        "inspect-prepare",
        help="clone or copy an OSS checkout and run static detectors",
    )
    prepare_inspect.add_argument("--product", help="product id from competitors/")
    prepare_inspect.add_argument("--run-id", help="stable run directory name")
    prepare_inspect.add_argument(
        "--fixture",
        help="use inspect/fixtures/<name> instead of cloning (mini-ade, empty-ade)",
    )
    prepare_inspect.add_argument("--checkout", help="existing source tree to copy")
    prepare_inspect.add_argument("--ref", help="git branch or tag when cloning")
    prepare_inspect.set_defaults(func=inspect_prepare)

    scan_inspect = subcommands.add_parser(
        "inspect-scan",
        help="write inspection.json from static detectors",
    )
    scan_inspect.add_argument("run_dir", help="inspect run directory")
    scan_inspect.set_defaults(func=inspect_scan)

    verify_inspect = subcommands.add_parser(
        "inspect-verify",
        help="verify inspection.json citations against the checkout",
    )
    verify_inspect.add_argument("run_dir", help="inspect run directory")
    verify_inspect.set_defaults(func=inspect_verify)

    inspect_one = subcommands.add_parser(
        "inspect",
        help="prepare + static scan + verify one product or fixture",
    )
    inspect_one.add_argument("--product", help="product id from competitors/")
    inspect_one.add_argument("--run-id", help="stable run directory name")
    inspect_one.add_argument("--fixture", help="inspect/fixtures/<name>")
    inspect_one.add_argument("--checkout", help="existing source tree to copy")
    inspect_one.add_argument("--ref", help="git branch or tag when cloning")
    inspect_one.add_argument(
        "--mode",
        choices=("static", "agent"),
        default="static",
        help="static writes inspection.json; agent stops after prepare for Claude/Codex/Grok",
    )
    inspect_one.set_defaults(func=inspect_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
