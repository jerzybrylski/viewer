from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_readalong import (
    branch_labels,
    character_index,
    clean_reading_text,
    location_index,
    map_ranks,
    speaker_for,
)


class ReadalongTests(unittest.TestCase):
    def test_dynamic_values_and_icons_are_marked_without_guessing(self) -> None:
        self.assertEqual(
            clean_reading_text(r"\V[2] / \N[3] / \P[1] / \I[64]"),
            "[wartość zmiennej 2] / [imię aktora 3] / [członek drużyny 1] / [ikona 64]",
        )

    def test_known_and_unknown_speakers(self) -> None:
        known = {"category": "custom_dialogue", "context": {"custom_header": "Ch angry"}}
        unknown = {"category": "custom_dialogue", "context": {"custom_header": "Qz mysterious"}}
        self.assertEqual(speaker_for(known)[0], "Chloe")
        self.assertEqual(speaker_for(unknown)[0], "Mówca nieustalony (Qz)")

    def test_choice_branch_uses_translated_choice_label(self) -> None:
        row = {"context": {"branch_path": [{
            "kind": "choice_branch", "choice_group_id": "g1", "option_index": 1,
            "branch_label": "Yes",
        }]}}
        self.assertEqual(
            branch_labels(row, {("g1", 1): "Tak"}, [], []),
            "wybór «Tak»",
        )

    def test_indexes_flag_unknown_speakers_and_static_reachability(self) -> None:
        people = character_index(Counter({"Chloe": 3, "Mówca nieustalony (Qz)": 1}))
        self.assertIn("Chloe", people)
        self.assertIn("nie przypisano jej postaci", people)
        places = location_index(
            {38: {}, 9: {}}, {}, {38: 0, 9: 1}, {38: 0},
            {38: {"translation": "Początek", "source_text": "START"}}, Counter({38: 2}),
        )
        self.assertIn("Mapa 038 — Początek", places)
        self.assertIn("poza grafem osiągalności", places)

    def test_map_order_expands_static_common_event_transfers(self) -> None:
        def map_doc(commands: list[dict]) -> dict:
            return {"events": [{"id": 1, "pages": [{"list": commands}]}]}

        maps = {
            38: map_doc([{"code": 117, "parameters": [300]}]),
            33: map_doc([{"code": 201, "parameters": [0, 36]}]),
            36: map_doc([]),
            9: map_doc([]),
        }
        common = {
            300: {"list": [{"code": 201, "parameters": [0, 33]}]},
        }
        ranks, _graph, distances = map_ranks(maps, common, {}, 38)
        self.assertEqual(set(distances), {38, 33, 36})
        self.assertLess(ranks[33], ranks[9])
        self.assertEqual(distances[36], 2)


class PublishedReadingStyleTests(unittest.TestCase):
    """Reguły redakcyjne Czytanki (decyzja właściciela 2026-10-29).

    Testy czytają opublikowane pliki `reading/v1`, bo to one idą do paczki.
    """

    script = Path(__file__).resolve().parents[1] / "reading" / "v1" / "chronological_script_PL.md"

    def setUp(self) -> None:
        self.text = self.script.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()

    def test_hero_placeholder_is_replaced_by_real_name(self) -> None:
        self.assertNotIn("1Hero", self.text)
        self.assertIn("**Mox:**", self.text)

    def test_no_technical_source_id_footer_in_full_script(self) -> None:
        self.assertNotIn("<sub>Źródłowe ID", self.text)

    def test_consecutive_dialogue_lines_are_not_split_by_blank_line(self) -> None:
        split_pairs = [
            (first, self.lines[index + 2])
            for index, (first, second) in enumerate(zip(self.lines, self.lines[1:]))
            if first.startswith("**") and ":** " in first
            and second == ""
            and self.lines[index + 2].startswith("**")
            and ":** " in self.lines[index + 2]
        ]
        self.assertEqual(split_pairs, [])

    def test_dialogue_lines_end_with_hard_line_break(self) -> None:
        dialogue = [line for line in self.lines if line.startswith("**") and ":** " in line]
        self.assertGreater(len(dialogue), 1000)
        self.assertEqual([line for line in dialogue if not line.endswith("  ")], [])

    def test_episode_files_keep_traceability_footer(self) -> None:
        episode = sorted((self.script.parent / "episodes").glob("*.md"))[0]
        self.assertIn("<sub>Źródłowe ID", episode.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
