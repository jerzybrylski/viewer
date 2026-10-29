"""Testy lokalizatora instalacji: autodetekcja, pamięć ścieżki i fallback.

Testy nie dotykają prawdziwego dysku użytkownika ani jego konfiguracji —
każdy przypadek pracuje na katalogu tymczasowym, a `Config` dostaje własną
ścieżkę pliku. GUI jest zaślepką, więc testy działają bez wyświetlacza.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "patcher"))

import locator  # noqa: E402


def make_install(base: Path, name: str = "The Genesis Order") -> Path:
    """Utwórz minimalną, poprawną atrapę instalacji TGO."""
    root = base / name
    (root / "www" / "data").mkdir(parents=True)
    (root / "www" / "index.html").write_text("<html></html>", encoding="utf-8")
    (root / "www" / "data" / "System.json").write_text("[]\n", encoding="utf-8")
    return root


class FakeGui(locator.ConsoleGui):
    def __init__(self, answers=None, folder=None, choice=None):
        super().__init__()
        self.answers = list(answers or [])
        self.folder = folder
        self.choice = choice
        self.messages: list[str] = []

    def say(self, message):
        self.messages.append(message)

    def ask_yes_no(self, question, default=True):
        return self.answers.pop(0) if self.answers else default

    def pick_folder(self, initial):
        return self.folder

    def choose(self, candidates):
        return self.choice


class DetectionTests(unittest.TestCase):
    def test_recognises_install_and_rejects_other_folders(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            install = make_install(base)
            self.assertTrue(locator.is_install_root(install))
            self.assertFalse(locator.is_install_root(base))
            self.assertFalse(locator.is_install_root(base / "nie-ma-takiego"))

    def test_finds_nested_installation_within_depth_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            install = make_install(base / "Games" / "Steam" / "common")
            found = locator.find_installations([base])
            self.assertEqual(found, [install])

    def test_respects_depth_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            make_install(base / "a" / "b" / "c" / "d" / "e")
            self.assertEqual(locator.find_installations([base], max_depth=2), [])

    def test_skips_noise_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            make_install(base / "node_modules")
            self.assertEqual(locator.find_installations([base]), [])

    def test_parses_steam_library_vdf(self):
        text = (
            '"libraryfolders"\n{\n'
            '\t"0"\n\t{\n\t\t"path"\t\t"C:\\\\Program Files (x86)\\\\Steam"\n\t}\n'
            '\t"1"\n\t{\n\t\t"path"\t\t"D:\\\\SteamLibrary"\n\t}\n'
            "}\n"
        )
        self.assertEqual(locator.vdf_library_paths(text),
                         [r"C:\Program Files (x86)\Steam", r"D:\SteamLibrary"])

    def test_duplicate_candidates_are_collapsed(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            install = make_install(base)
            found = locator.find_installations([base, base, install])
            self.assertEqual(found, [install])


class MemoryTests(unittest.TestCase):
    def test_remembers_and_forgets_path(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            install = make_install(base)
            config = locator.Config(base / "cfg" / "config.json")
            self.assertIsNone(config.remembered())
            config.save(install, patch_version="0.1.1-poc", action="apply")
            self.assertEqual(config.remembered(), install)
            data = json.loads((base / "cfg" / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(data["schema"], locator.CONFIG_SCHEMA)
            self.assertEqual(data["last_patch_version"], "0.1.1-poc")
            self.assertTrue(config.forget())
            self.assertIsNone(config.remembered())

    def test_ignores_stale_or_broken_memory(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            config = locator.Config(base / "config.json")
            config.path.write_text(json.dumps({"game_path": str(base / "usuniete")}), encoding="utf-8")
            self.assertIsNone(config.remembered())
            config.path.write_text("{to nie json", encoding="utf-8")
            self.assertIsNone(config.remembered())

    def test_env_override_changes_config_location(self):
        with tempfile.TemporaryDirectory() as temp:
            previous = locator.os.environ.get(locator.ENV_CONFIG_PATH)
            locator.os.environ[locator.ENV_CONFIG_PATH] = str(Path(temp) / "c.json")
            try:
                self.assertEqual(locator.default_config_path(), Path(temp) / "c.json")
            finally:
                if previous is None:
                    locator.os.environ.pop(locator.ENV_CONFIG_PATH, None)
                else:
                    locator.os.environ[locator.ENV_CONFIG_PATH] = previous


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.config = locator.Config(self.base / "cfg" / "config.json")

    def tearDown(self):
        self.temp.cleanup()

    def test_explicit_path_wins_and_is_remembered(self):
        install = make_install(self.base / "gry")
        gui = FakeGui()
        resolved = locator.resolve_install(install, config=self.config, gui=gui, interactive=False)
        self.assertEqual(resolved, install)
        self.assertEqual(self.config.remembered(), install)

    def test_existing_memory_is_used_without_searching(self):
        install = make_install(self.base / "gry")
        self.config.save(install, "", "apply")
        gui = FakeGui(answers=[True])
        resolved = locator.resolve_install(None, config=self.config, gui=gui,
                                           extra_roots=[self.base / "gry"])
        self.assertEqual(resolved, install)
        self.assertFalse(any("Szukam instalacji" in message for message in gui.messages))

    def test_declining_memory_falls_back_to_search_and_picker(self):
        old = make_install(self.base / "stare")
        self.config.save(old, "", "apply")
        other = make_install(self.base / "inne")
        gui = FakeGui(answers=[False, True])
        resolved = locator.resolve_install(None, config=self.config, gui=gui, extra_roots=[self.base])
        self.assertEqual(resolved, other)

    def test_single_candidate_requires_confirmation_when_interactive(self):
        install = make_install(self.base / "gry")
        gui = FakeGui(answers=[False], folder=install)
        resolved = locator.resolve_install(None, config=self.config, gui=gui, extra_roots=[self.base])
        self.assertEqual(resolved, install)

    def test_picker_result_is_validated(self):
        make_install(self.base / "gry")
        gui = FakeGui(answers=[False], folder=self.base / "nie-gra")
        with self.assertRaises(ValueError):
            locator.resolve_install(None, config=self.config, gui=gui, extra_roots=[self.base])

    def test_cancelled_picker_changes_nothing(self):
        make_install(self.base / "gry")
        gui = FakeGui(answers=[False], folder=None)
        with self.assertRaises(ValueError):
            locator.resolve_install(None, config=self.config, gui=gui, extra_roots=[self.base])
        self.assertIsNone(self.config.remembered())

    def test_non_interactive_without_candidate_raises_instead_of_blocking(self):
        (self.base / "pusty").mkdir()
        with self.assertRaises(ValueError):
            locator.resolve_install(None, config=self.config, gui=FakeGui(),
                                    interactive=False, extra_roots=[self.base / "pusty"])

    def test_non_interactive_accepts_unambiguous_candidate(self):
        install = make_install(self.base / "gry")
        resolved = locator.resolve_install(None, config=self.config, gui=FakeGui(),
                                           interactive=False, extra_roots=[self.base])
        self.assertEqual(resolved, install)

    def test_multiple_candidates_are_offered_as_a_choice(self):
        first = make_install(self.base / "a")
        second = make_install(self.base / "b")
        gui = FakeGui(choice=second)
        resolved = locator.resolve_install(None, config=self.config, gui=gui,
                                           extra_roots=[self.base], assume_yes=True)
        self.assertEqual(resolved, second)
        self.assertIn(first, [Path(p) for p in locator.find_installations([self.base])])

    def test_invalid_explicit_path_does_not_raise_when_interactive(self):
        install = make_install(self.base / "gry")
        gui = FakeGui(answers=[True])
        resolved = locator.resolve_install(self.base / "zly", config=self.config, gui=gui,
                                           extra_roots=[self.base])
        self.assertEqual(resolved, install)


if __name__ == "__main__":
    unittest.main()
