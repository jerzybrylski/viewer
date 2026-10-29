"""Testy audytu redakcyjnego.

Najważniejsze, czego tu pilnujemy: narzędzie **nie może** „poprawiać” rzeczy,
które są poprawne — celowej emfazy `!!`, spacji przeniesionej ze źródła ani
powtórzeń gramatycznych typu „na nie nie wylej”. Każda taka pomyłka byłaby
cichą zmianą treści w 39 917 tłumaczeniach.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import audit_editorial_quality as qa  # noqa: E402


def row(record_id: str, translation: str, source: str = "") -> dict:
    return {"id": record_id, "translation": translation, "source_text": source, "category": "custom_dialogue"}


class RepeatedWordTests(unittest.TestCase):
    def test_flags_real_duplicate(self):
        self.assertEqual(qa.repeated_word("nauczyłam się cię nie nie doceniać"), "nie nie")

    def test_ignores_grammatical_jej_jej(self):
        self.assertIsNone(qa.repeated_word("nie pozwolę jej jej opublikować"))

    def test_reports_but_reviewed_items_stay_silent(self):
        reviewed = row("tgo:custom_dialogue:6bacf88cd88d60bb1204", "Tylko niczego na nie nie wylej.")
        report = qa.analyse([reviewed])
        self.assertEqual(report["issues"].get("repeated_word", {"count": 0})["count"], 0)
        self.assertGreaterEqual(report["reviewed_as_correct"], 1)


class FixSafetyTests(unittest.TestCase):
    def test_strips_trailing_space_only_when_source_has_none(self):
        changes, _ = qa.fix([row("a", "Zasz? ", "Zasz?")])
        self.assertEqual(changes, {"a": "Zasz?"})
        changes, _ = qa.fix([row("b", "Zwykłe ", "Zwykłe ")])
        self.assertEqual(changes, {})

    def test_collapses_double_spaces_inside_text(self):
        changes, _ = qa.fix([row("a", "To  jest  test")])
        self.assertEqual(changes["a"], "To jest test")

    def test_never_touches_intentional_emphasis(self):
        for text in ("<center>\\c[18]!! UWAGA !!\\c[0]<br>", "Serio?? Nie wierzę!!"):
            with self.subTest(text=text):
                changes, _ = qa.fix([row("a", text)])
                self.assertEqual(changes, {})

    def test_removes_space_before_plain_punctuation(self):
        changes, _ = qa.fix([row("a", "Poczekaj , zaraz wracam .")])
        self.assertEqual(changes["a"], "Poczekaj, zaraz wracam.")


class AnalysisTests(unittest.TestCase):
    def test_counts_english_leftover_but_not_polish_homographs(self):
        report = qa.analyse([row("a", "Grzeczny chłopiec. Chcę was oboje."),
                             row("b", "you know")])
        self.assertEqual(report["issues"]["english_leftover"]["count"], 1)
        self.assertEqual(report["issues"]["english_leftover"]["samples"][0]["id"], "b")

    def test_reports_name_variants_and_lengths(self):
        report = qa.analyse([row("a", "To fragment Toma Leolo."), row("b", "To fragment Tomy Leolo.")])
        self.assertEqual(report["name_variants"]["Toma Leolo"], {"Toma Leolo": 1, "Tomy Leolo": 1})
        self.assertGreater(report["length"]["max"], 0)

    def test_published_report_is_clean(self):
        """Opublikowany raport musi mieć zero niezałatwionych usterek."""
        report = json.loads((ROOT / "translation" / "reports" / "editorial_qa_v1.json").read_text(encoding="utf-8"))
        for name, data in report["issues"].items():
            if name.startswith("dash_em"):
                continue
            with self.subTest(issue=name):
                self.assertEqual(data["count"], 0, f"niezałatwiona klasa: {name}")


if __name__ == "__main__":
    unittest.main()
