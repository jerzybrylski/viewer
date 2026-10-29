"""Testy narzędzia R-09: ujednolicenie odmiany imion na ``-a``.

Narzędzie zmienia tekst, więc każdy przypadek, w którym może się pomylić, ma
tu własny test. Sprawdzamy też idempotencję: drugi przebieg musi być pusty,
bo inaczej przebudowa Czytanki zmieniałaby się przy każdym uruchomieniu.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from unify_name_declension import DECLENSION, NAME_RE, decide, transform


def cases(text: str) -> list[tuple[str, str]]:
    found = []
    for match in NAME_RE.finditer(text):
        decision = decide(text, match)
        if decision:
            found.append((match.group("name"), decision[0]))
    return found


class DeclensionRuleTests(unittest.TestCase):
    def test_whole_utterance_is_vocative(self) -> None:
        self.assertEqual(transform("Ella!"), ("Ello!", [("Ella", "voc", "vocative_whole_utterance", "Ello")]))

    def test_comma_address_is_vocative(self) -> None:
        self.assertEqual(transform("Cholera, Ella. Jesteś niesamowita.")[0],
                         "Cholera, Ello. Jesteś niesamowita.")

    def test_leading_address_is_vocative(self) -> None:
        self.assertEqual(transform("Ella, co ty wyprawiasz?")[0], "Ello, co ty wyprawiasz?")

    def test_genitive_governor_is_declined(self) -> None:
        self.assertEqual(transform("To fragment Toma Leolo.")[0], "To fragment Tomy Leolo.")

    def test_subject_stays_in_nominative(self) -> None:
        # Podmiot i orzeczenie imienne nie mogą dostać dopełniacza za darmo.
        for text in ("Ella jest zmęczona.", "Melissa poszła do domu.", "To Ella."):
            with self.subTest(text=text):
                self.assertEqual(transform(text)[0], text)

    def test_names_without_declension_table_are_untouched(self) -> None:
        # Chloe/Lilith/Carol/Hannah mają w źródle zero form odmienionych,
        # więc nie ma czego ujednolicać i nie zgadujemy.
        self.assertEqual(transform("Chloe, chodź tu!")[0], "Chloe, chodź tu!")

    def test_markup_survives_rewrite(self) -> None:
        text = r"\c[23]Cholera, \c[27]Ella\c[0]! Wracamy."
        self.assertEqual(transform(text)[0], r"\c[23]Cholera, \c[27]Ello\c[0]! Wracamy.")

    def test_is_idempotent(self) -> None:
        once = transform("Cholera, Ella. To fragment Toma.")[0]
        self.assertEqual(transform(once)[0], once)

    def test_every_table_entry_has_all_cases(self) -> None:
        for name, forms in DECLENSION.items():
            with self.subTest(name=name):
                self.assertEqual(set(forms), {"gen", "dat", "acc", "ins", "loc", "voc"})


if __name__ == "__main__":
    unittest.main()
