from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


WORKTREE = Path(__import__("os").environ["BENCH_WORKTREE"])


class ButtonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_button = False
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            self.in_button = True
            self.buttons.append({"attrs": dict(attrs), "text": ""})

    def handle_endtag(self, tag):
        if tag == "button":
            self.in_button = False

    def handle_data(self, data):
        if self.in_button and self.buttons:
            self.buttons[-1]["text"] += data


def css_block(css, selector):
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\}}", css, re.S)
    return match.group("body") if match else ""


class ResponsiveCardTest(unittest.TestCase):
    def setUp(self):
        self.html = (WORKTREE / "index.html").read_text(encoding="utf-8")
        self.css = (WORKTREE / "styles.css").read_text(encoding="utf-8")

    def test_cards_use_responsive_grid(self):
        cards = css_block(self.css, ".cards")
        self.assertIn("display: grid", cards)
        self.assertRegex(cards, r"grid-template-columns\s*:\s*repeat\(\s*auto-(fit|fill)\s*,\s*minmax\(")

    def test_cards_can_shrink(self):
        card = css_block(self.css, ".card")
        self.assertIn("min-width: 0", card)
        self.assertNotIn("width: 288px", card)

    def test_narrow_screen_media_query_exists(self):
        self.assertRegex(self.css, r"@media\s*\(\s*max-width\s*:\s*(720|700|640|600)px\s*\)")

    def test_buttons_remain_accessible(self):
        parser = ButtonParser()
        parser.feed(self.html)
        self.assertEqual(len(parser.buttons), 3)
        for button in parser.buttons:
            name = (button["attrs"].get("aria-label") or button["text"]).strip()
            self.assertTrue(name)
            self.assertIn("Inspect", name)


if __name__ == "__main__":
    unittest.main()

