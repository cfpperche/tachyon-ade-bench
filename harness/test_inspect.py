#!/usr/bin/env python3
"""Tests for the source-inspection harness. Run: python3 harness/test_inspect.py"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ROOT = HARNESS_DIR.parent
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

import source_inspect as inspect_lib  # noqa: E402

BENCH = [sys.executable, str(HARNESS_DIR / "bench.py")]
EXPECTED_OSS = {
    "compozy",
    "emdash",
    "fusion",
    "herdr",
    "kandev",
    "openade",
    "orca",
    "paseo",
    "synara",
    "t3-code",
    "warp",
}
CLOSED_OR_UNKNOWN = {
    "agentsroom",
    "augment-code",
    "conductor",
    "falou",
    "github-copilot-app",
    "hive",
    "hiveterm",
    "jetbrains-air",
    "kiro",
    "maestri",
    "overclock",
    "tachyon",
    "xirp",
}


def bench(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*BENCH, *args],
        cwd=str(cwd or ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class LicenseRosterTests(unittest.TestCase):
    def test_osi_token_strips_qualifiers(self) -> None:
        self.assertEqual(inspect_lib.license_token("AGPL-3.0 (client); commercial"), "AGPL-3.0")
        self.assertEqual(
            inspect_lib.license_token("AGPL-3.0-or-later (commercial license negotiable)"),
            "AGPL-3.0-or-later",
        )
        self.assertTrue(inspect_lib.is_osi_open_source("MIT"))
        self.assertFalse(inspect_lib.is_osi_open_source("BUSL-1.1"))
        self.assertFalse(inspect_lib.is_osi_open_source("unknown"))
        self.assertFalse(inspect_lib.is_osi_open_source("proprietary"))

    def test_cataloged_oss_roster(self) -> None:
        rows = inspect_lib.list_inspectable_products()
        ids = {row["id"] for row in rows}
        self.assertTrue(EXPECTED_OSS.issubset(ids))
        public = {row["id"] for row in rows if row.get("source_kind") == "public-git"}
        self.assertEqual(public, EXPECTED_OSS)
        closed_public = CLOSED_OR_UNKNOWN - {"tachyon"}
        self.assertTrue(ids.isdisjoint(closed_public))
        for row in rows:
            if row["source_kind"] == "public-git":
                self.assertTrue(str(row["source_url"]).startswith("http"))
        if Path("~/tachyon").expanduser().is_dir():
            self.assertIn("tachyon", ids)
            owned = next(row for row in rows if row["id"] == "tachyon")
            self.assertEqual(owned["source_kind"], "owned-local")


class DetectorFixtureTests(unittest.TestCase):
    def test_mini_ade_code_features_present(self) -> None:
        scan = inspect_lib.scan_checkout(inspect_lib.fixture_path("mini-ade"))
        features = scan["features"]
        self.assertGreater(scan["files_scanned"], 0)
        self.assertEqual(features["dag_orchestration"]["verdict"], "present")
        self.assertEqual(features["worktree_isolation"]["verdict"], "present")
        self.assertEqual(features["guest_claude_code"]["verdict"], "present")
        self.assertEqual(features["guest_codex"]["verdict"], "present")
        self.assertEqual(features["guest_grok"]["verdict"], "present")
        dag_layers = {item["layer"] for item in features["dag_orchestration"]["evidence"]}
        self.assertIn("code", dag_layers)
        self.assertTrue(any(item["path"].startswith("src/") for item in features["dag_orchestration"]["evidence"]))

    def test_empty_ade_docs_only_is_partial(self) -> None:
        scan = inspect_lib.scan_checkout(inspect_lib.fixture_path("empty-ade"))
        features = scan["features"]
        for feature_id in (
            "dag_orchestration",
            "worktree_isolation",
            "guest_claude_code",
            "guest_codex",
            "guest_grok",
        ):
            self.assertEqual(features[feature_id]["verdict"], "partial", feature_id)
            layers = {item["layer"] for item in features[feature_id]["evidence"]}
            self.assertEqual(layers, {"docs"}, feature_id)
        self.assertEqual(features["mcp_integrations"]["verdict"], "absent")
        dag_paths = {item["path"] for item in features["dag_orchestration"]["evidence"]}
        self.assertNotIn("vite.config.ts", dag_paths)

    def test_build_graph_depends_on_is_not_agent_dag(self) -> None:
        self.assertIsNone(inspect_lib.classify_path("vite.config.ts"))
        self.assertIsNone(inspect_lib.classify_path("Formula/kandev.rb"))


class CitationVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checkout = inspect_lib.fixture_path("mini-ade")
        self.catalog = inspect_lib.load_feature_catalog()
        self.scan = inspect_lib.scan_checkout(self.checkout, self.catalog)

    def test_static_inspection_verifies(self) -> None:
        inspection = inspect_lib.build_inspection("mini-ade", self.scan)
        errors = inspect_lib.validate_inspection(inspection, self.catalog, self.checkout)
        self.assertEqual(errors, [])

    def test_invented_file_is_rejected(self) -> None:
        inspection = inspect_lib.build_inspection("mini-ade", self.scan)
        inspection["features"]["dag_orchestration"]["evidence"] = [
            {
                "path": "src/does-not-exist.ts",
                "line": 1,
                "snippet": "DAG",
                "layer": "code",
            }
        ]
        errors = inspect_lib.validate_inspection(inspection, self.catalog, self.checkout)
        self.assertTrue(any("missing file" in error for error in errors))

    def test_snippet_must_occur_on_cited_line(self) -> None:
        inspection = inspect_lib.build_inspection("mini-ade", self.scan)
        inspection["features"]["dag_orchestration"]["evidence"] = [
            {
                "path": "src/dag.ts",
                "line": 1,
                "snippet": "this-snippet-is-not-on-line-1",
                "layer": "code",
            }
        ]
        errors = inspect_lib.validate_inspection(inspection, self.catalog, self.checkout)
        self.assertTrue(any("snippet not found" in error for error in errors))

    def test_agent_runtime_must_be_supported(self) -> None:
        inspection = inspect_lib.build_inspection(
            "mini-ade",
            self.scan,
            inspector_kind="agent",
            inspector_runtime="cursor",
        )
        errors = inspect_lib.validate_inspection(inspection, self.catalog, self.checkout)
        self.assertTrue(any("inspector.runtime" in error for error in errors))

    def test_supported_agent_runtimes_validate(self) -> None:
        for runtime in ("claude-code", "codex", "grok-build"):
            inspection = inspect_lib.build_inspection(
                "mini-ade",
                self.scan,
                inspector_kind="agent",
                inspector_runtime=runtime,
                model="test-model",
            )
            errors = inspect_lib.validate_inspection(inspection, self.catalog, self.checkout)
            self.assertEqual(errors, [], runtime)


class CloneAndCliTests(unittest.TestCase):
    def test_materialize_clones_local_git_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origin = Path(tmp) / "origin"
            dest = Path(tmp) / "checkout"
            shutil.copytree(inspect_lib.fixture_path("mini-ade"), origin)
            subprocess.run(["git", "init", "-b", "main"], cwd=origin, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=origin, check=True, capture_output=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Inspect Test",
                    "-c",
                    "user.email=inspect@example.invalid",
                    "commit",
                    "-m",
                    "fixture",
                ],
                cwd=origin,
                check=True,
                capture_output=True,
            )
            meta = inspect_lib.materialize_checkout(dest, source_url=str(origin))
            self.assertEqual(meta["method"], "clone")
            self.assertTrue((dest / "src" / "dag.ts").is_file())
            self.assertTrue(meta["commit"])

    def test_cli_static_inspect_fixture(self) -> None:
        run_id = "test-inspect-mini-ade"
        run_dir = ROOT / "runs" / run_id
        if run_dir.exists():
            shutil.rmtree(run_dir)
        try:
            prepared = bench(
                "inspect",
                "--fixture",
                "mini-ade",
                "--product",
                "orca",
                "--run-id",
                run_id,
                "--mode",
                "static",
            )
            self.assertEqual(prepared.returncode, 0, prepared.stderr + prepared.stdout)
            inspection = json.loads((run_dir / "inspection.json").read_text(encoding="utf-8"))
            self.assertEqual(inspection["inspector"]["kind"], "static")
            self.assertEqual(inspection["features"]["dag_orchestration"]["verdict"], "present")
            self.assertEqual(inspection["product_id"], "orca")
            result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "pass")
            self.assertTrue((run_dir / "prompt.md").is_file())
            prompt = (run_dir / "prompt.md").read_text(encoding="utf-8")
            for name in ("Claude Code", "Codex", "Grok Build"):
                self.assertIn(name, prompt)
        finally:
            if run_dir.exists():
                shutil.rmtree(run_dir)

    def test_cli_agent_prepare_then_verify(self) -> None:
        run_id = "test-inspect-agent-grok"
        run_dir = ROOT / "runs" / run_id
        if run_dir.exists():
            shutil.rmtree(run_dir)
        try:
            prepared = bench(
                "inspect",
                "--fixture",
                "empty-ade",
                "--run-id",
                run_id,
                "--mode",
                "agent",
            )
            self.assertEqual(prepared.returncode, 0, prepared.stderr)
            self.assertFalse((run_dir / "inspection.json").is_file())
            scan = json.loads((run_dir / "detectors.json").read_text(encoding="utf-8"))
            inspection = inspect_lib.build_inspection(
                "empty-ade",
                scan,
                inspector_kind="agent",
                inspector_runtime="grok-build",
                model="grok-4.6",
            )
            (run_dir / "inspection.json").write_text(
                json.dumps(inspection, indent=2) + "\n",
                encoding="utf-8",
            )
            verified = bench("inspect-verify", f"runs/{run_id}")
            self.assertEqual(verified.returncode, 0, verified.stderr + verified.stdout)
            result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["inspector"]["runtime"], "grok-build")
            self.assertEqual(result["status"], "pass")
        finally:
            if run_dir.exists():
                shutil.rmtree(run_dir)

    def test_list_inspectable_and_check(self) -> None:
        listed = bench("list-inspectable")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        ids = {line.split("\t", 1)[0] for line in listed.stdout.splitlines() if line.strip()}
        self.assertTrue(EXPECTED_OSS.issubset(ids))
        if Path("~/tachyon").expanduser().is_dir():
            self.assertIn("tachyon", ids)
        checked = bench("inspect-check")
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn("claude-code, codex, grok-build", checked.stdout)


if __name__ == "__main__":
    unittest.main()
