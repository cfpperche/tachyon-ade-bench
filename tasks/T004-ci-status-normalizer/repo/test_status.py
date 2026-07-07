import unittest

from status import normalize_status


class StatusTest(unittest.TestCase):
    def test_known_statuses(self):
        self.assertEqual(normalize_status("todo"), "todo")
        self.assertEqual(normalize_status("blocked"), "blocked")
        self.assertEqual(normalize_status("done"), "done")

    def test_in_progress_words(self):
        self.assertEqual(normalize_status("in progress"), "in_progress")


if __name__ == "__main__":
    unittest.main()

