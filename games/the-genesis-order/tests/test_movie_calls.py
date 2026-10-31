from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_readalong as readalong  # noqa: E402
import scan_movie_calls as scanner  # noqa: E402


def message(text: str) -> list[dict]:
    return [
        {"code": 101, "parameters": ["", 0, 0, 2, ""]},
        {"code": 401, "parameters": [text]},
    ]


class MovieScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        common = [
            {
                "id": 300,
                "name": "SCN - Opening",
                "list": [
                    {"code": 355, "parameters": ["$gameScreen.playMovie('AdChng1')"]},
                    {"code": 655, "parameters": ["  });"]},
                    *message("Po klipie."),
                ],
            },
            {
                "id": 301,
                "name": "SCN - Dynamic",
                "list": [{"code": 355, "parameters": ["playMovie($gameVariables.value(12))"]}],
            },
            {
                "id": 302,
                "name": "SCN - Review",
                "list": [{"code": 356, "parameters": ["MoviePlayer", "play", "AdChng2"]}],
            },
            {"id": 303, "name": "Bez wideo", "list": message("Zwykły tekst.")},
        ]
        (self.root / "CommonEvents.json").write_text(json.dumps(common), encoding="utf-8")
        map_doc = {
            "events": [
                {"id": 1, "name": "EV001", "pages": [{"list": [
                    {"code": 355, "parameters": ['$gameScreen.playVideo("Clips/Intro.mp4")']},
                ]}]},
                {"id": 2, "name": "EV002", "pages": [{"list": message("Tekst bez klipu.")}]},
            ]
        }
        (self.root / "Map002.json").write_text(json.dumps(map_doc), encoding="utf-8")
        (self.root / "MapInfos.json").write_text("[]", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_confirmed_dynamic_and_candidate_calls_are_separated(self) -> None:
        report = scanner.scan(self.root, None)
        summary = report["summary"]
        self.assertEqual(summary["files_scanned"], 2)
        self.assertEqual(summary["playback_calls"], 3)
        self.assertEqual(summary["confirmed_calls"], 2)
        self.assertEqual(summary["dynamic_calls"], 1)
        self.assertEqual(summary["review_candidates"], 1)
        self.assertEqual(sorted(report["movie_files"]), ["AdChng1", "Intro.mp4"])

        common_call = next(call for call in report["calls"] if call["source_kind"] == "common_event")
        # Nazwa literalna bez rozszerzenia zostaje bez zmian — nie dopisujemy ".mp4" za grę.
        self.assertEqual(common_call["movie_file"], "AdChng1")
        self.assertEqual(common_call["event_id"], 300)
        self.assertEqual(common_call["command_index"], 0)

        map_call = next(call for call in report["calls"] if call["source_kind"] == "map")
        self.assertEqual(map_call["movie_file"], "Intro.mp4", "ścieżka ma zostać zredukowana do nazwy pliku")
        self.assertEqual((map_call["map_id"], map_call["event_id"], map_call["page_number"]), (2, 1, 1))

    def test_plugin_command_without_movie_extension_is_a_candidate(self) -> None:
        report = scanner.scan(self.root, None)
        candidate = report["candidates"][0]
        self.assertEqual(candidate["command_code"], 356)
        self.assertEqual(candidate["movie_file"], "AdChng2")
        self.assertIn("MoviePlayer", candidate["evidence"])
        self.assertEqual(report["plugin_commands"]["MoviePlayer"], 1)

    def test_dynamic_argument_is_marked_and_not_guessed(self) -> None:
        report = scanner.scan(self.root, None)
        dynamic = next(call for call in report["calls"] if call["dynamic"])
        self.assertEqual(dynamic["event_id"], 301)
        self.assertIsNone(dynamic["movie_file"])

    def test_zip_input_matches_directory_input(self) -> None:
        archive_path = self.root / "data.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            for name in ("CommonEvents.json", "Map002.json", "MapInfos.json"):
                archive.write(self.root / name, f"data/{name}")
        from_dir = scanner.scan(self.root, None)
        from_zip = scanner.scan(self.root, archive_path)
        self.assertEqual(from_dir["calls"], from_zip["calls"])
        self.assertEqual(from_dir["summary"], from_zip["summary"])
        self.assertEqual(from_zip["source"]["mode"], "zip")

    def test_output_file_is_never_overwritten(self) -> None:
        out = self.root / "movie_calls.json"
        out.write_text("{}", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            scanner.main(["--data-dir", str(self.root), "--out", str(out)])

    def test_scanner_writes_nothing_into_the_source(self) -> None:
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        scanner.scan(self.root, None)
        after = {path.name: path.read_bytes() for path in self.root.iterdir()}
        self.assertEqual(before, after)


class MovieCallsInReadingTests(unittest.TestCase):
    def write_inventory(self, calls: list[dict]) -> Path:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        path = Path(self.temp.name) / "movie_calls.json"
        path.write_text(json.dumps({
            "schema": "tgo-movie-calls-v1",
            "movie_files": sorted({call["movie_file"] for call in calls if call.get("movie_file")}),
            "calls": calls,
        }), encoding="utf-8")
        return path

    def row(self, index: int, text: str = "Kwestia") -> dict:
        return {
            "category": "custom_dialogue",
            "context": {"custom_header": "Ch angry", "command_index": index},
            "translation": text, "source_text": text, "id": f"tgo:test:{index}",
        }

    def call(self, index: int, name: str | None, *, dynamic: bool = False, kind: str = "map") -> dict:
        return {
            "source_kind": kind, "map_id": 1 if kind == "map" else None,
            "event_id": 2, "page_number": 1 if kind == "map" else None,
            "command_index": index, "movie_file": name, "dynamic": dynamic,
            "evidence": "playMovie(...)" if dynamic else f"playMovie('{name}')",
        }

    def test_marker_is_placed_before_the_first_line_after_the_command(self) -> None:
        content, stats = readalong.render_episode(
            ("map", 1, 2, 1), [self.row(10), self.row(20, "Druga")], {}, {}, [], [],
            map_name="Test", movie_calls=[self.call(15, "AdChng1.mp4")],
        )
        self.assertEqual(stats["movie_calls"], 1)
        # Klip jest po pierwszej kwestii, a przed drugą — dokładnie tam, gdzie stoi polecenie.
        self.assertLess(content.index("**Chloe:** Kwestia"), content.index("AdChng1.mp4"))
        self.assertLess(content.index("AdChng1.mp4"), content.index("**Chloe:** Druga"))

    def test_marker_never_replaces_dialogue_or_branches(self) -> None:
        content, stats = readalong.render_episode(
            ("map", 1, 2, 1), [self.row(10)], {}, {}, [], [],
            map_name="Test", movie_calls=[self.call(20, "Outro.mp4")],
        )
        self.assertIn("**Chloe:** Kwestia", content)
        self.assertIn("`Outro.mp4`", content)
        self.assertEqual(stats["included"], 1)
        self.assertLess(content.index("**Chloe:** Kwestia"), content.index("`Outro.mp4`"))

    def test_dynamic_call_is_shown_without_inventing_a_file(self) -> None:
        content, _ = readalong.render_episode(
            ("common_event", None, 300, None), [self.row(10)], {}, {}, [], [],
            common_name="SCN", movie_calls=[self.call(0, None, dynamic=True, kind="common_event")],
        )
        self.assertIn("nazwa nieustalona statycznie", content)
        self.assertNotIn(".mp4`", content)

    def test_episode_with_only_a_movie_is_not_dropped(self) -> None:
        content, stats = readalong.render_episode(
            ("map", 1, 2, 1), [], {}, {}, [], [],
            map_name="Przejście", movie_calls=[self.call(3, "Fade.mp4")],
        )
        self.assertIn("## Mapa 001 — Przejście", content)
        self.assertIn("`Fade.mp4`", content)
        self.assertEqual((stats["included"], stats["movie_calls"]), (0, 1))

    def test_inventory_loading_validates_schema_and_groups_by_scene(self) -> None:
        path = self.write_inventory([self.call(5, "A.mp4"), self.call(7, "B.mp4", kind="common_event")])
        grouped, report = readalong.load_movie_calls(path)
        self.assertEqual(report["schema"], "tgo-movie-calls-v1")
        self.assertEqual(len(grouped[("map", 1, 2, 1)]), 1)
        self.assertEqual(len(grouped[("common_event", None, 2, None)]), 1)

        broken = Path(self.temp.name) / "broken.json"
        broken.write_text("{}", encoding="utf-8")
        with self.assertRaises(ValueError):
            readalong.load_movie_calls(broken)

    def test_polish_plural_forms(self) -> None:
        self.assertEqual(readalong.plural_pl(1, "wywołanie", "wywołania", "wywołań"), "wywołanie")
        self.assertEqual(readalong.plural_pl(3, "wywołanie", "wywołania", "wywołań"), "wywołania")
        self.assertEqual(readalong.plural_pl(5, "wywołanie", "wywołania", "wywołań"), "wywołań")
        self.assertEqual(readalong.plural_pl(12, "wywołanie", "wywołania", "wywołań"), "wywołań")
        self.assertEqual(readalong.plural_pl(22, "wywołanie", "wywołania", "wywołań"), "wywołania")

    def test_movie_index_lists_files_with_chapters(self) -> None:
        text = readalong.movie_index([
            (1, "Map 1 event 2 page 1", self.call(5, "A.mp4")),
            (2, "Common Event 300 SCN", self.call(9, "A.mp4", kind="common_event")),
            (3, "Map 3 event 1 page 1", self.call(1, None, dynamic=True)),
        ])
        self.assertIn("**`A.mp4`** — 2 wywołania w 2 rozdziałach", text)
        self.assertIn("rozdział 0001", text)
        self.assertIn("bez statycznej nazwy pliku", text)


if __name__ == "__main__":
    unittest.main()
