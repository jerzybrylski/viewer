from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import export_translation as exporter  # noqa: E402
import markdown_translation as markdown  # noqa: E402


class MarkdownTranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.input = self.root / "canonical.jsonl"
        self.out = self.root / "google_drive" / "translation" / "markdown"
        self.import_out = self.root / "google_drive" / "translation" / "translated.jsonl"
        self.row = exporter.record(
            category="custom_dialogue", status="confirmed_dialogue",
            text=r"Hello, \N[1]", source_file="data/Map001.json",
            source_hash="a" * 64,
            locator={"file": "data/Map001.json", "event_id": 7,
                     "page_number": 2, "command_index": 9,
                     "json_path": "/list/9/parameters/0"},
            context={"source_kind": "map", "map_id": 1, "map_name": "Fixture",
                     "event_id": 7, "event_name": "Fixture event", "page_number": 2,
                     "command_index": 9, "branch_path": [{"kind": "choice_branch",
                         "option_index": 0, "branch_label": "Take path"}],
                     "page_conditions": {"switch1Valid": True, "switch1Id": 4},
                     "speaker": {"name": "Fixture speaker", "confidence": "synthetic"}},
            structure={"command_code": 401},
        )
        self.input.write_text(json.dumps(self.row, ensure_ascii=False) + "\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_build_and_import_changes_only_translation_by_id(self):
        with patch.object(markdown, "REPO_ROOT", self.root):
            manifest = markdown.build_markdown(self.input, self.out)
            self.assertEqual(manifest["records"], 1)
            self.assertFalse(manifest["translator_delivery_ready"])
            doc = self.out / "maps" / "Map001.md"
            text = doc.read_text(encoding="utf-8")
            self.assertIn("not a claim about story chronology", text)
            self.assertIn("choice_branch", text)
            self.assertIn("page_conditions", text)
            translated = r"Bonjour, \N[1]"
            text = text.replace(
                "TGO-TRANSLATION: \"\"",
                "TGO-TRANSLATION: " + json.dumps(translated, ensure_ascii=False),
            )
            doc.write_text(text, encoding="utf-8")
            report = markdown.import_markdown(self.input, self.out, self.import_out)
            self.assertEqual(report["records_with_translation"], 1)
            imported = json.loads(self.import_out.read_text(encoding="utf-8"))
            self.assertEqual(imported["id"], self.row["id"])
            self.assertEqual(imported["source_text"], self.row["source_text"])
            self.assertEqual(imported["translation"], translated)

    def test_markdown_import_rejects_protected_source_value_changes(self):
        protected = exporter.record(
            category="ui.variable_value", status="confirmed_text_surface",
            text="$500", source_file="data/Map001.json", source_hash="c" * 64,
            locator={"file": "data/Map001.json", "event_id": 7,
                     "page_number": 1, "command_index": 3,
                     "command_code": 122, "expression_kind": "variable_value"},
            context={"translation_policy": "keep_source_value"},
            structure={"display_role": "price"},
        )
        self.input.write_text(json.dumps(protected, ensure_ascii=False) + "\n", encoding="utf-8")
        with patch.object(markdown, "REPO_ROOT", self.root):
            markdown.build_markdown(self.input, self.out)
            doc = self.out / "maps" / "Map001.md"
            text = doc.read_text(encoding="utf-8")
            # A protected source value intentionally needs no translation.
            markdown.import_markdown(self.input, self.out, self.import_out,
                                     require_complete=True, check_only=True)
            text = text.replace(
                "TGO-TRANSLATION: \"\"",
                "TGO-TRANSLATION: " + json.dumps("$600"),
            )
            doc.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Protected source value changed"):
                markdown.import_markdown(self.input, self.out, self.import_out, check_only=True)

    def test_import_rejects_loss_of_positional_and_punctuation_controls(self):
        row = exporter.record(
            category="custom_dialogue", status="confirmed_dialogue",
            text=r"\>Value %1\!", source_file="data/Map001.json", source_hash="a" * 64,
            locator={"file": "data/Map001.json", "event_id": 7, "page_number": 2,
                     "command_index": 9, "json_path": "/list/9/parameters/0"},
            context={"source_kind": "map", "map_id": 1, "event_id": 7, "page_number": 2},
            structure={"command_code": 401},
        )
        self.input.write_text(json.dumps(row) + "\n", encoding="utf-8")
        with patch.object(markdown, "REPO_ROOT", self.root):
            markdown.build_markdown(self.input, self.out)
            doc = self.out / "maps" / "Map001.md"
            text = doc.read_text(encoding="utf-8")
            doc.write_text(text.replace('TGO-TRANSLATION: ""',
                'TGO-TRANSLATION: ' + json.dumps(r"\>Wartość\!")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Additional control"):
                markdown.import_markdown(self.input, self.out, self.import_out, check_only=True)

    def test_import_rejects_changed_hash_and_token_loss(self):
        with patch.object(markdown, "REPO_ROOT", self.root):
            markdown.build_markdown(self.input, self.out)
            doc = self.out / "maps" / "Map001.md"
            original = doc.read_text(encoding="utf-8")
            translated = "Bonjour"
            changed = original.replace(
                "TGO-TRANSLATION: \"\"",
                "TGO-TRANSLATION: " + json.dumps(translated),
            )
            doc.write_text(changed, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Markup/token mismatch"):
                markdown.import_markdown(self.input, self.out, self.import_out)
            changed = changed.replace('sha256="' + "a" * 64 + '"', 'sha256="' + "b" * 64 + '"')
            doc.write_text(changed, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Source hash mismatch"):
                markdown.import_markdown(self.input, self.out, self.import_out)


if __name__ == "__main__":
    unittest.main()
