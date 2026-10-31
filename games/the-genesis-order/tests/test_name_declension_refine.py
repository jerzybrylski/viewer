"""Testy dokończenia odmiany imion (R-13) — reguły, poprawki kuratorskie, raport."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

TGO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TGO / "tools"))

import refine_name_declension as refine  # noqa: E402

REPORT = TGO / "translation" / "reports" / "declension_refine_v1.json"
DRAFTS = TGO / "translation" / "drafts"
SCRIPT = TGO / "reading" / "v1" / "chronological_script_PL.md"


class RulesTest(unittest.TestCase):
    def check(self, before: str, after: str) -> None:
        self.assertEqual(refine.transform(before)[0], after)

    def test_noun_government(self):
        self.check("Znalazłeś kolejne kawałki Toma Leolo?",
                   "Znalazłeś kolejne kawałki Tomy Leolo?")
        self.check("Za pomocą Toma?", "Za pomocą Tomy?")
        self.check("Używała fragmentu posągu Toma!", "Używała fragmentu posągu Tomy!")
        self.check("I to powstrzyma Lillian przed użyciem Toma?",
                   "I to powstrzyma Lillian przed użyciem Tomy?")

    def test_verb_government(self):
        self.check("Spokojnie. Szuka Toma Leolo?", "Spokojnie. Szuka Tomy Leolo?")
        self.check("Czarownice używały Toma, by wyrywać dusze ludzi.",
                   "Czarownice używały Tomy, by wyrywać dusze ludzi.")
        self.check("Czarownice z Casuli strzegły Toma Leolo.",
                   "Czarownice z Casuli strzegły Tomy Leolo.")

    def test_prepositions(self):
        self.check("Myślisz, że ma związek z Toma Leolo?",
                   "Myślisz, że ma związek z Tomą Leolo?")
        self.check("Jestem niemal pewien, że chodzi o Toma Leolo.",
                   "Jestem niemal pewien, że chodzi o Tomę Leolo.")

    def test_curated_decisions(self):
        self.check("Żaden Toma nie jest wart utraty życia.",
                   "Żadna Toma nie jest warta utraty życia.")
        self.check("Nie odbierzecie nam Toma Leolo!", "Nie odbierzecie nam Tomy Leolo!")
        self.check("z powrotem Toma Leolo", "z powrotem Tomę Leolo")
        self.check("Mówiła o szukaniu… Toma i amuletów…",
                   "Mówiła o szukaniu… Tomy i amuletów…")

    def test_native_phone_hints(self):
        self.check("<br><center>Zdobądź\\c[14] Melissa \\c[0]numer telefonu, aby odblokować",
                   "<br><center>Zdobądź numer telefonu \\c[14]Melissy\\c[0], aby odblokować")
        self.check("<br><center>Zdobądź\\c[14] Hannah \\c[0]numer telefonu, aby odblokować",
                   "<br><center>Zdobądź numer telefonu \\c[14]Hannah\\c[0], aby odblokować")

    def test_unknown_government_is_left_alone(self):
        for text in ("To Toma!", "Gdzie jest Toma?", "Toma Leolo to bożek.",
                     "Jestem pewien, że Toma Leolo istnieje.", "To nie Toma."):
            with self.subTest(text=text):
                self.assertEqual(refine.transform(text)[0], text)

    def test_idempotent(self):
        text = "Znalazłeś kawałki Toma Leolo? Za pomocą Toma?"
        once = refine.transform(text)[0]
        self.assertEqual(refine.transform(once)[0], once)


class CorpusTest(unittest.TestCase):
    def read_drafts(self) -> list[dict]:
        rows = []
        for path in sorted(DRAFTS.rglob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def test_fixed_forms_are_in_corpus(self):
        # Znaczniki renderera (\\c[n]) rozdzielają słowa, więc porównujemy tekst widoczny dla gracza.
        markup = re.compile(r"(?:\\\\)?\\c\[\d+\]")
        texts = [markup.sub("", row.get("translation") or "") for row in self.read_drafts()]
        joined = "\n".join(texts)
        for expected in ("kawałki Tomy Leolo", "Za pomocą Tomy?", "Szuka Tomy Leolo?",
                         "z Tomą Leolo", "o Tomę Leolo", "Żadna Toma nie jest warta",
                         "numer telefonu Melissy", "numer telefonu Hannah",
                         "numer telefonu Carol", "sprowadzono z powrotem Tomę Leolo"):
            with self.subTest(fragment=expected):
                self.assertIn(expected, joined)
        for gone in ("kawałki Toma Leolo?", "Za pomocą Toma?", "Zdobądź Melissa"):
            with self.subTest(fragment=gone):
                self.assertNotIn(gone, joined)

    def test_report_matches_corpus_state(self):
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(report["schema"], "tgo-declension-refine-v1")
        self.assertEqual(report["changed_rows"], 22)
        self.assertEqual(report["changed_occurrences"], 12)
        self.assertEqual(report["pending_occurrences"], 610)
        self.assertEqual(len(report["changes"]), 12)
        for change in report["changes"]:
            self.assertNotEqual(change["before"], change["after"])
            self.assertNotIn(change["before"], (change["after"],))

    @unittest.skipUnless(SCRIPT.is_file(), "brak wygenerowanej Czytanki")
    def test_reading_carries_the_fixes(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Zdobądź numer telefonu Melissy", text)
        self.assertIn("kawałki Tomy Leolo", text)
        self.assertNotIn("Zdobądź Melissa numer telefonu", text)


if __name__ == "__main__":
    unittest.main()
