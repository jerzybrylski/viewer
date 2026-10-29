from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_translation_coverage import classify_untranslated, visible_residue


def record(category: str, source_text: str, context: dict | None = None, source_file: str = "data/Test.json") -> dict:
    return {
        "category": category,
        "source_text": source_text,
        "context": context or {},
        "source": {"file": source_file},
    }


class TranslationCoverageTests(unittest.TestCase):
    def test_renderer_controls_are_not_visible_prose(self) -> None:
        self.assertEqual(visible_residue(r"<center>\fn<Arial>\w[170]\^"), "")
        self.assertEqual(visible_residue(r"\c[17]\v[322]\c[27]Melissa"), "Melissa")

    def test_custom_emote_command_is_preserved_but_unknown_literal_is_not(self) -> None:
        self.assertEqual(
            classify_untranslated(record("custom_dialogue", "/greet")),
            ("source_preserved", "custom_dialogue_emote_or_pause_control"),
        )
        self.assertIsNone(classify_untranslated(record("custom_dialogue", "Hello there")))

    def test_numeric_and_proper_name_choice_values_are_preserved(self) -> None:
        self.assertIsNotNone(classify_untranslated(record("choice_option", r"\i[2]3")))
        self.assertIsNotNone(classify_untranslated(record("choice_option", "Melissa")))
        self.assertIsNone(classify_untranslated(record("choice_option", "Good morning")))

    def test_single_letter_quiz_answers_require_known_context(self) -> None:
        self.assertIsNotNone(classify_untranslated(record(
            "choice_option", "U", {"map_id": 17, "event_id": 68}
        )))
        self.assertIsNone(classify_untranslated(record("choice_option", "U")))

    def test_renderer_amount_and_known_names_are_preserved(self) -> None:
        self.assertIsNotNone(classify_untranslated(record("native_message", r"\c[15]$150<br>")))
        self.assertIsNotNone(classify_untranslated(record("native_message", "Madalyn.")))
        self.assertIsNone(classify_untranslated(record("native_message", "I found the key.")))

    def test_unknown_category_remains_unresolved(self) -> None:
        self.assertIsNone(classify_untranslated(record("native_message", "A sentence not yet translated.")))


if __name__ == "__main__":
    unittest.main()
