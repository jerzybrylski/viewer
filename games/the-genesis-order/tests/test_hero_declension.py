"""Testy odmiany imienia bohatera w Czytance (`1Hero` → Mox w przypadkach)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TGO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TGO / "tools"))

import hero_declension as hero  # noqa: E402
import build_readalong  # noqa: E402
import audit_hero_declension  # noqa: E402

REPORT = TGO / "translation" / "reports" / "hero_declension_v1.json"
SCRIPT = TGO / "reading" / "v1" / "chronological_script_PL.md"
DRAFTS = TGO / "translation" / "drafts"


class FormsTest(unittest.TestCase):
    def test_declension_table(self):
        self.assertEqual(hero.HERO_FORMS["gen"], "Moxa")
        self.assertEqual(hero.HERO_FORMS["dat"], "Moxowi")
        self.assertEqual(hero.HERO_FORMS["acc"], "Moxa")
        self.assertEqual(hero.HERO_FORMS["ins"], "Moxem")
        self.assertEqual(hero.HERO_FORMS["loc"], "Moxie")
        self.assertEqual(hero.HERO_FORMS["nom"], "Mox")
        self.assertEqual(hero.HERO_FORMS["voc"], "Mox")

    def test_unambiguous_prepositions(self):
        cases = {
            "Nie bądź niemiła dla 1Hero.": "dla Moxa",
            "Musimy zyskać dla 1Hero na czasie.": "dla Moxa",
            "Zwłaszcza wobec 1Hero.": "wobec Moxa",
            "Ściółka jest mokra dzięki 1Hero.": "dzięki Moxowi",
            "Ale… przy 1Hero?": "przy Moxie",
            "Moje życie seksualne z 1Hero to nie twoja sprawa.": "z Moxem",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected, hero.decline_text(text)[0])

    def test_ambiguous_prepositions(self):
        cases = {
            "To wyszło z 1Hero?": "z Moxa",           # z + źródło → dopełniacz
            "Chodzi o 1Hero, prawda?": "o Moxa",      # „chodzi o” → biernik
            "Mówiłam o 1Hero.": "o Moxie",            # mówienie o kimś → miejscownik
            "podkochuje się w 1Hero": "w Moxie",
            "Zbliżenia na 1Hero.": "na Moxa",
            "znaleźć zastępstwo za 1Hero": "za Moxa",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected, hero.decline_text(text)[0])

    def test_verbs(self):
        cases = {
            "Panie, chroń 1Hero.": "chroń Moxa",
            "Hej, może Henry mógłby pomóc 1Hero?": "pomóc Moxowi",
            "Nie słuchaj 1Hero.": "słuchaj Moxa",
            "Demony porwały 1Hero.": "porwały Moxa",
            "Skąd znasz 1Hero?": "znasz Moxa",
            "Pomogłam 1Hero.": "Pomogłam Moxowi",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertIn(expected, hero.decline_text(text)[0])

    def test_vocative_and_subject_stay_base(self):
        for text in ("Cześć, 1Hero.", "1Hero!", "1Hero, chodź tu.", "1Hero idzie do domu."):
            with self.subTest(text=text):
                result, decisions = hero.decline_text(text)
                self.assertNotIn("1Hero", result)
                self.assertEqual(decisions[0]["case"] in {"nom", "voc"}, True)

    def test_unknown_governor_is_reported_not_guessed(self):
        text = "Wręczam 1Hero nagrodę."
        result, decisions = hero.decline_text(text)
        self.assertEqual(decisions[0]["resolved"], False)
        self.assertIn("1Hero", text)
        self.assertIn("Mox", result)  # mianownik, bez zgadywania przypadku

    def test_multiple_occurrences_and_no_placeholder_left(self):
        text = "Idę z 1Hero, a 1Hero zostaje."
        result, decisions = hero.decline_text(text)
        self.assertEqual(len(decisions), 2)
        self.assertEqual(result, "Idę z Moxem, a Mox zostaje.")
        self.assertNotIn("1Hero", result)

    def test_markup_is_ignored(self):
        text = "Wszystko z \\c[27]1Hero\\c[0] jest w porządku."
        result, _ = hero.decline_text(text)
        self.assertIn("z \\c[27]Moxem", result)


class AuditToolTest(unittest.TestCase):
    def test_relative_drafts_path_is_displayed(self):
        relative = Path("games/the-genesis-order/translation/drafts")
        if not relative.is_dir():
            self.skipTest("uruchom z katalogu głównego repo")
        shown = audit_hero_declension.display_path(relative)
        self.assertEqual(shown, "translation/drafts")


class ReadingTest(unittest.TestCase):
    def test_build_readalong_uses_declension(self):
        self.assertEqual(build_readalong.hero_text("Idę z 1Hero."), "Idę z Moxem.")
        self.assertEqual(build_readalong.hero_text("Nie bądź niemiła dla 1Hero."),
                         "Nie bądź niemiła dla Moxa.")

    @unittest.skipUnless(SCRIPT.is_file(), "brak wygenerowanej Czytanki")
    def test_no_undeclined_hero_after_preposition(self):
        import re
        pattern = re.compile(
            r"\b(do|od|u|dla|bez|obok|koło|około|wobec|zamiast|oprócz|według|poza|wśród|"
            r"podczas|naprzeciw|o|przy|ku|dzięki|wbrew|z|ze|nad|pod|przed|za|w|we|na|po|"
            r"między|przez)\s+Mox\b"
        )
        offenders = [line for line in SCRIPT.read_text(encoding="utf-8").splitlines()
                     if pattern.search(line)]
        self.assertEqual(offenders, [])

    @unittest.skipUnless(SCRIPT.is_file(), "brak wygenerowanej Czytanki")
    def test_script_has_no_placeholder(self):
        self.assertNotIn("1Hero", SCRIPT.read_text(encoding="utf-8"))


@unittest.skipUnless(REPORT.is_file(), "brak raportu odmiany")
class ReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_counts(self):
        report = self.report
        self.assertEqual(report["schema"], "tgo-hero-declension-report-v1")
        self.assertEqual(report["records_with_placeholder"], 2431)
        self.assertEqual(report["occurrences"], 2433)
        self.assertEqual(report["records_changed_in_reading"], 67)
        self.assertEqual(report["unresolved_count"], 2)

    def test_every_change_is_declined_form(self):
        forms = {"Moxa", "Moxowi", "Moxem", "Moxie"}
        for change in self.report["changes"]:
            self.assertIn("1Hero", change["before"])
            self.assertNotIn("1Hero", change["after"])
            self.assertTrue(any(form in change["after"] for form in forms), change["after"])

    def test_drafts_keep_placeholder(self):
        """Drafty muszą zachować `1Hero` — gra podstawia tam imię gracza."""
        offenders = []
        for path in sorted(DRAFTS.rglob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                text = row.get("translation")
                if not isinstance(text, str):
                    continue
                if "Moxa" in text or "Moxowi" in text or "Moxem" in text or "Moxie" in text:
                    offenders.append(row.get("id"))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
