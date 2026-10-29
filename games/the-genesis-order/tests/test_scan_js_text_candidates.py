from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import scan_js_text_candidates as scanner  # noqa: E402


class ScanJsCandidatesTests(unittest.TestCase):
    def test_lexer_skips_comments_and_decodes_static_literals(self):
        source = '''// "comment only"\nconst label = "A\\nB"; /* 'not text' */\nconst key = 'option';'''
        literals = list(scanner.iter_literals(source))
        self.assertEqual([item["value"] for item in literals], ["A\nB", "option"])
        self.assertEqual([item["line"] for item in literals], [2, 3])

    def test_dynamic_template_is_not_exported_as_static_text(self):
        literals = list(scanner.iter_literals("const label = `Hello ${name}`; const fixed = `Ready`"))
        self.assertEqual(len(literals), 2)
        self.assertTrue(literals[0]["dynamic_template"])
        self.assertIsNone(literals[0]["value"])
        self.assertEqual(literals[1]["value"], "Ready")

    def test_candidate_id_uses_locator_not_text(self):
        locator = {"file": "www/js/plugin.js", "line": 42}
        self.assertEqual(scanner.candidate_id("js_display_literal_candidate", locator),
                         scanner.candidate_id("js_display_literal_candidate", dict(locator)))
        self.assertNotEqual(scanner.candidate_id("js_display_literal_candidate", locator),
                            scanner.candidate_id("js_display_literal_candidate", {"file": "www/js/plugin.js", "line": 43}))


if __name__ == "__main__":
    unittest.main()
