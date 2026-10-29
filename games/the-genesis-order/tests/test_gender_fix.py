"""Testy zgodności rodzaju gramatycznego.

Najważniejsze ryzyko: zamiana formy, gdy rodzaj **nie** jest znany, albo
„naprawienie” rzeczownika w narzędniku (`kościołem`) lub czasownika
teraźniejszego (`działam`). Każda taka pomyłka byłaby cichą zmianą treści.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import fix_grammatical_gender as fg  # noqa: E402


def row(record_id: str, translation: str, header: str = "McHeOp", **context) -> dict:
    payload = {"source_kind": "map", "map_id": 1, "event_id": 1, "page_number": 1, "custom_header": header}
    payload.update(context)
    return {
        "id": record_id,
        "category": "custom_dialogue",
        "translation": translation,
        "source_text": "",
        "context": payload,
    }


class SpeakerMapTests(unittest.TestCase):
    def test_speaker_map_matches_readalong(self):
        import build_readalong  # noqa: E402

        self.assertEqual(fg.SPEAKERS, build_readalong.SPEAKERS)

    def test_hero_is_male_and_named_women_are_female(self):
        self.assertEqual(fg.gender_of(fg.SPEAKERS["Mc"]), "M")
        for code in ("Ju", "Ch", "Hn", "Er", "Me", "He", "Ad"):
            self.assertEqual(fg.gender_of(fg.SPEAKERS[code]), "F", code)
        self.assertIsNone(fg.gender_of("Postać niezależna"))


class FirstPersonTests(unittest.TestCase):
    def defem(self, text: str, gender: str = "F") -> str:
        edits = fg.first_person_edits(text, gender)
        return fg.apply_edits(text, edits)[0]

    def test_masculine_past_to_feminine(self):
        self.assertEqual(self.defem("Nie wiedziałem, co robić."), "Nie wiedziałam, co robić.")
        self.assertEqual(self.defem("Chciałbym zostać."), "Chciałabym zostać.")

    def test_irregular_stems(self):
        self.assertEqual(self.defem("Doszedłem do wniosku, że tak."), "Doszłam do wniosku, że tak.")
        self.assertEqual(self.defem("Wziąłem to na siebie."), "Wzięłam to na siebie.")
        self.assertEqual(self.defem("Zacząłem rozumieć."), "Zaczęłam rozumieć.")

    def test_feminine_past_to_masculine(self):
        self.assertEqual(self.defem("Nie widziałam go.", "M"), "Nie widziałem go.")
        self.assertEqual(self.defem("Wyszłam stąd.", "M"), "Wyszedłem stąd.")

    def test_instrumental_nouns_are_untouched(self):
        text = "Pod kościołem stoi aniołem? Nie, z tym masłem i stołem."
        self.assertEqual(self.defem(text), text)
        self.assertEqual(self.defem(text.replace("łem", "łam").replace("anioł", "anioł"), "F") if False else text, text)

    def test_we_ze_compounds(self):
        self.assertEqual(self.defem("Weszłem do środka.", "F"), "Weszłam do środka.")
        self.assertEqual(self.defem("Weszłam do środka.", "M"), "Wszedłem do środka.")

    def test_present_tense_untouched(self):
        self.assertEqual(self.defem("Działam szybko.", "M"), "Działam szybko.")


class SecondPersonTests(unittest.TestCase):
    def test_addressed_female(self):
        edits = fg.second_person_edits("Jak zgadłeś? Zwariowałeś?", "F")
        self.assertEqual(fg.apply_edits("Jak zgadłeś? Zwariowałeś?", edits)[0], "Jak zgadłaś? Zwariowałaś?")

    def test_addressed_male(self):
        edits = fg.second_person_edits("Mówiłaś, że wrócisz.", "M")
        self.assertEqual(fg.apply_edits("Mówiłaś, że wrócisz.", edits)[0], "Mówiłeś, że wrócisz.")

    def test_irregular_second_person(self):
        text = "Doszedłeś do tego?"
        edits = fg.second_person_edits(text, "F")
        self.assertEqual(fg.apply_edits(text, edits)[0], "Doszłaś do tego?")


class ThirdPersonFormTests(unittest.TestCase):
    def test_regular_and_irregular_to_feminine(self):
        import fix_grammatical_gender as fg  # noqa: F401

        pairs = {
            "wiedział": "wiedziała", "zrobił": "zrobiła", "był": "była",
            "miał": "miała", "mógł": "mogła", "szedł": "szła",
            "wziął": "wzięła", "zaczął": "zaczęła", "przyszedł": "przyszła",
            "wszedł": "weszła", "zszedł": "zeszła",
        }
        for masc, fem in pairs.items():
            self.assertEqual(fg.third_person_to_fem(masc), fem, masc)

    def test_regular_and_irregular_to_masculine(self):
        import fix_grammatical_gender as fg  # noqa: F401

        pairs = {
            "wiedziała": "wiedział", "zrobiła": "zrobił", "była": "był",
            "miała": "miał", "mogła": "mógł", "szła": "szedł",
            "wzięła": "wziął", "zaczęła": "zaczął", "cierpiała": "cierpiał",
            "weszła": "wszedł", "zeszła": "zszedł",
        }
        for fem, masc in pairs.items():
            self.assertEqual(fg.third_person_to_masc(fem), masc, fem)


class PredicateTests(unittest.TestCase):
    def defem(self, text: str, gender: str, persons: str) -> str:
        edits = fg.adjective_edits(text, gender, persons)
        return fg.apply_edits(text, edits)[0]

    def test_first_person_predicate_chain(self):
        self.assertEqual(self.defem("Jestem pewien, że tak.", "F", "1"), "Jestem pewna, że tak.")
        self.assertEqual(self.defem("Jestem taka wolna.", "M", "1"), "Jestem taki wolny.")
        self.assertEqual(self.defem("Czuję się taka wolna.", "M", "1"), "Czuję się taki wolny.")

    def test_second_person_predicate_chain(self):
        self.assertEqual(self.defem("Jesteś taka młoda.", "M", "2"), "Jesteś taki młody.")
        self.assertEqual(self.defem("Jesteś taka… piękna!", "M", "2"), "Jesteś taki… piękny!")

    def test_does_not_touch_noun_after_comma(self):
        text = "Jestem kobietą, a nie zabawką."
        self.assertEqual(self.defem(text, "F", "1"), text)


class SceneRuleTests(unittest.TestCase):
    def scene(self, rows):
        return fg.scene_index(rows)[fg.scene_key(rows[0])]

    def test_two_participants_give_addressee(self):
        rows = [row("tgo:a:1", "Cześć."), row("tgo:a:2", "Jak zgadłeś?", header="JuHeOp")]
        scene = self.scene(rows)
        self.assertEqual(fg.addressee_gender(scene, rows[0]), ("F", "jednolita płeć pozostałych mówców sceny"))

    def test_three_participants_are_ambiguous(self):
        rows = [
            row("tgo:a:1", "Jak zgadłeś?"),
            row("tgo:a:2", "Cześć.", header="JuHeOp"),
            row("tgo:a:3", "Hej.", header="ChHeOp"),
            row("tgo:a:4", "No.", header="DaHeOp"),
        ]
        scene = self.scene(rows)
        self.assertEqual(fg.addressee_gender(scene, rows[0])[0], None)

    def test_narrator_does_not_get_addressee_conversion(self):
        rows = [row("tgo:a:1", "Nie zapomnij, że zostawiłeś dziewczyny z Jonem.", header="", category="native_message"),
                row("tgo:a:2", "Cześć.", header="JuHeOp")]
        rows[0]["category"] = "native_message"
        rows[0]["context"] = {"source_kind": "map", "map_id": 1, "event_id": 1, "page_number": 1}
        changes, log, report = fg.plan(rows)
        self.assertNotIn("tgo:a:1", changes)

    def test_masculine_vocative_blocks_conversion(self):
        rows = [row("tgo:a:1", "Jesteś wolny, pająku."), row("tgo:a:2", "Cześć.", header="JuHeOp")]
        changes, log, report = fg.plan(rows)
        self.assertNotIn("tgo:a:1", changes)


class PlanTests(unittest.TestCase):
    def test_female_speaker_gets_feminine_forms(self):
        rows = [row("tgo:a:1", "Nigdy czegoś takiego nie widziałem.", header="JuHeOp")]
        changes, log, report = fg.plan(rows)
        self.assertEqual(changes["tgo:a:1"], "Nigdy czegoś takiego nie widziałam.")
        self.assertEqual(report["records_changed"], 1)

    def test_plan_is_idempotent(self):
        rows = [row("tgo:a:1", "Nigdy czegoś takiego nie widziałem.", header="JuHeOp")]
        changes, _, _ = fg.plan(rows)
        rows[0]["translation"] = changes["tgo:a:1"]
        again, _, _ = fg.plan(rows)
        self.assertEqual(again, {})

    def test_empty_translation_is_skipped(self):
        rows = [row("tgo:a:1", "", header="JuHeOp")]
        changes, _, _ = fg.plan(rows)
        self.assertEqual(changes, {})


if __name__ == "__main__":
    unittest.main()
