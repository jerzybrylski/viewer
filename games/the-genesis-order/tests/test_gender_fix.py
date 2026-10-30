"""Testy naprawy rodzaju gramatycznego (tools/fix_grammatical_gender.py)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import build_readalong  # noqa: E402
import fix_grammatical_gender as gender  # noqa: E402


class UnsafeAutomationTests(unittest.TestCase):
    def test_apply_is_disabled_before_any_writes(self):
        with self.assertRaises(SystemExit) as error:
            gender.main(['--apply'])
        self.assertEqual(error.exception.code, 2)


class SpeakerMapTests(unittest.TestCase):
    def test_map_matches_readalong(self):
        """Kody mówców muszą być te same, co w Czytance — inaczej role się rozjadą."""
        for code, name in gender.SPEAKERS.items():
            self.assertEqual(build_readalong.SPEAKERS.get(code), name)

    def test_every_speaker_has_gender_or_stays_unknown(self):
        known = gender.FEMALE_SPEAKERS | gender.MALE_SPEAKERS
        self.assertFalse(gender.FEMALE_SPEAKERS & gender.MALE_SPEAKERS)
        self.assertIn("Judy", gender.FEMALE_SPEAKERS)
        self.assertIn("Mox", gender.MALE_SPEAKERS)
        self.assertNotIn("Zakapturzona postać", known)

    def test_header_parsing(self):
        row = {"context": {"custom_header": "JuWoOpNo1^"}}
        self.assertEqual(gender.speaker_of(row), "Judy")
        self.assertEqual(gender.gender_of("Judy"), "F")
        self.assertIsNone(gender.gender_of("Zakapturzona postać"))


class VerbFormTests(unittest.TestCase):
    def test_feminine_from_masculine(self):
        self.assertEqual(gender.swap_verb_form("powiedziałem", "F", "1"), "powiedziałam")
        self.assertEqual(gender.swap_verb_form("chciałbym", "F", "1"), "chciałabym")

    def test_masculine_from_feminine(self):
        self.assertEqual(gender.swap_verb_form("powiedziałam", "M", "1"), "powiedziałem")
        self.assertEqual(gender.swap_verb_form("musiała", "M", "1"), None)

    def test_second_person_stays_second_person(self):
        self.assertEqual(gender.swap_verb_form("zrobiłeś", "F", "2"), "zrobiłaś")
        self.assertEqual(gender.swap_verb_form("zrobiłaś", "M", "2"), "zrobiłeś")

    def test_irregular_stems(self):
        self.assertEqual(gender.swap_verb_form("przyszedłem", "F", "1"), "przyszłam")
        self.assertEqual(gender.swap_verb_form("wziąłem", "F", "1"), "wzięłam")
        self.assertEqual(gender.swap_verb_form("przyszedłeś", "F", "2"), "przyszłaś")

    def test_nouns_and_present_tense_untouched(self):
        self.assertIsNone(gender.swap_verb_form("kościołem", "F", "1"))
        self.assertIsNone(gender.swap_verb_form("działam", "M", "1"))

    def test_ist_compounds_feminine_to_masculine(self):
        """Złożenia „iść” wymagają „szed”, nie „sz” — inaczej wychodzi „weszłem”."""
        cases = {
            "weszłam": "wszedłem",
            "zeszłam": "zszedłem",
            "odeszłam": "odszedłem",
            "podeszłam": "podszedłem",
            "przyszłam": "przyszedłem",
            "doszłam": "doszedłem",
            "poszłam": "poszedłem",
            "obeszłam": "obeszedłem",
            "zeszłabym": "zszedłbym",
            "weszłaś": "wszedłeś",
            "przyszłaś": "przyszedłeś",
        }
        for fem, masc in cases.items():
            person = "2" if fem.endswith(("łaś", "łabyś")) else "1"
            with self.subTest(fem=fem):
                self.assertEqual(gender.swap_verb_form(fem, "M", person), masc)

    def test_ist_compounds_masculine_to_feminine(self):
        """Kierunek odwrotny: „wszedłem” → „weszłam”, a nie „wszłam”."""
        cases = {
            "wszedłem": "weszłam",
            "zszedłem": "zeszłam",
            "odszedłem": "odeszłam",
            "podszedłem": "podeszłam",
            "przeszedłem": "przeszłam",
            "wyszedłem": "wyszłam",
            "przyszedłem": "przyszłam",
        }
        for masc, fem in cases.items():
            with self.subTest(masc=masc):
                self.assertEqual(gender.swap_verb_form(masc, "F", "1"), fem)

    def test_unknown_prefix_is_not_guessed(self):
        """„usłyszłam” nie jest złożeniem „iść” — lepiej nie zmieniać niż zgadywać."""
        self.assertIsNone(gender.swap_verb_form("usłyszłam", "M", "1"))
        self.assertIsNone(gender.ist_compound_stem("usłysz", "M")[1])

    def test_ist_lookalike_does_not_block_normal_verbs(self):
        """Zwykłe czasowniki na „-łam” dalej działają zwykłą regułą."""
        self.assertEqual(gender.swap_verb_form("znalazłam", "M", "1"), "znalazłem")
        self.assertEqual(gender.swap_verb_form("powiedziałam", "M", "1"), "powiedziałem")


class PredicateTests(unittest.TestCase):
    def edits(self, text: str, gender_code: str, person: str = "1"):
        return gender.collect_edits(text, 0, gender_code, person, set())

    def test_pewien_to_pewna(self):
        edits = self.edits("Nie jestem tego pewien.", "F")
        self.assertEqual([(e["old"], e["new"]) for e in edits], [("pewien", "pewna")])

    def test_pewna_to_pewien(self):
        edits = self.edits("Nie byłem całkiem pewna.", "M")
        self.assertEqual([(e["old"], e["new"]) for e in edits], [("pewna", "pewien")])

    def test_adjective_chain(self):
        edits = self.edits("Jestem cała twoja, kochanie.", "M")
        self.assertEqual({(e["old"], e["new"]) for e in edits}, {("cała", "cały"), ("twoja", "twój")})

    def test_masculine_noun_is_not_converted(self):
        edits = self.edits("Jestem księdzem. Takie demony mnie nie przerażają.", "F")
        self.assertEqual(edits, [])

    def test_noun_governs_adjective(self):
        edits = self.edits("Jestem jedyną osobą w biurze.", "M")
        self.assertEqual(edits, [])

    def test_simile_untouched(self):
        edits = self.edits("Jestem jak ciepły, lepki bałwan.", "F")
        self.assertEqual(edits, [])

    def test_feminine_noun_for_man(self):
        edits = self.edits("Jestem detektywką.", "M")
        self.assertEqual([(e["old"], e["new"]) for e in edits], [("detektywką", "detektywem")])


class AddresseeTests(unittest.TestCase):
    def edits(self, text: str, gender_code: str):
        return gender.collect_edits(text, 0, gender_code, "2", set())

    def test_vocative_gives_gender(self):
        self.assertEqual(gender.vocative_gender("Hannah! Jak ty to zrobiłaś?"), "F")
        self.assertEqual(gender.vocative_gender("Mox, co zrobiłeś?"), "M")

    def test_second_person_follows_addressee(self):
        edits = self.edits("Jesteś gotowy?", "F")
        self.assertEqual([(e["old"], e["new"]) for e in edits], [("gotowy", "gotowa")])

    def test_hero_counts_only_in_vocative(self):
        self.assertTrue(gender.HERO_VOCATIVE_RE.search("1Hero, co zrobiłeś?"))
        self.assertFalse(gender.HERO_VOCATIVE_RE.search("1Hero mówił, że miałaś spotkanie."))


class CorpusIntegrationTests(unittest.TestCase):
    def test_apply_is_idempotent_on_sample(self):
        vocabulary = {"pewna", "pewien"}
        row = {
            "id": "tgo:test:1",
            "context": {"custom_header": "JuWoCl"},
            "translation": "Nie jestem tego pewien.",
        }
        rows = {"tgo:test:1": (Path("dummy.jsonl"), row)}
        changes, _ = gender.plan(rows, vocabulary)
        self.assertEqual(len(changes), 1)
        row["translation"] = changes[0]["after"]
        changes_again, _ = gender.plan(rows, vocabulary)
        self.assertEqual(changes_again, [])

    def test_unknown_speaker_left_alone(self):
        vocabulary = {"pewna"}
        row = {"id": "tgo:test:2", "context": {}, "translation": "Nie jestem tego pewien."}
        rows = {"tgo:test:2": (Path("dummy.jsonl"), row)}
        changes, residual = gender.plan(rows, vocabulary)
        self.assertEqual(changes, [])
        self.assertEqual(residual["bez_znanego_mowcy_z_pierwsza_osoba"][0]["id"], "tgo:test:2")


if __name__ == "__main__":
    unittest.main()
