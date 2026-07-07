import subprocess
import unittest

from status import normalize_status


class StatusNormalizerTest(unittest.TestCase):
    def test_variants(self):
        cases = {
            "todo": "todo",
            "TO DO": "todo",
            "in progress": "in_progress",
            "in-progress": "in_progress",
            "in_progress": "in_progress",
            "blocked": "blocked",
            "done": "done",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_status(raw), expected)

    def test_unknowns(self):
        self.assertEqual(normalize_status("waiting"), "unknown")
        self.assertEqual(normalize_status(None), "unknown")

    def test_fixture_ci_script_passes(self):
        subprocess.run(
            ["bash", "ci.sh"],
            cwd=__import__("os").environ["BENCH_WORKTREE"],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()

