from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import apply_translation as applier  # noqa: E402
import export_translation as exporter  # noqa: E402


class ApplyTranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.out = self.root / "out"
        self.inputs = self.root / "translated.jsonl"
        (self.source / "data").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_bundle(self, rows):
        self.inputs.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )

    def test_json_command_import_writes_new_copy_only(self):
        rel = "data/Map001.json"
        original = {
            "events": [None, {"id": 1, "pages": [{"conditions": {}, "list": [
                {"code": 101, "parameters": ["", 0, 0, 2]},
                {"code": 401, "parameters": ["Source sentence"]},
            ]}]}]
        }
        source_path = self.source / rel
        source_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
        raw = source_path.read_bytes()
        locator = {"file": rel, "event_id": 1, "page_number": 1,
                   "command_index": 1, "command_code": 401,
                   "json_path": "/list/1/parameters/0"}
        row = exporter.record(
            category="native_message_unclassified", status="needs_review",
            text="Source sentence", source_file=rel,
            source_hash=hashlib.sha256(raw).hexdigest(), locator=locator,
            context={}, structure={"command_code": 401},
        )
        row["translation"] = "Target sentence"
        self.write_bundle([row])
        report = applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = json.loads((self.out / rel).read_text(encoding="utf-8"))
        self.assertEqual(patched["events"][1]["pages"][0]["list"][1]["parameters"][0], "Target sentence")
        self.assertEqual(source_path.read_bytes(), raw)
        self.assertEqual(report["records_translated"], 1)

    def test_script_channel_import_preserves_header_and_quote(self):
        rel = "data/CommonEvents.json"
        original = [None, {"id": 1, "name": "Fixture", "list": [
            {"code": 355, "parameters": ["$gameVariables.setValue(21, 'SPEAKER.source')"]},
            {"code": 117, "parameters": [60]},
        ]}]
        source_path = self.source / rel
        source_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
        raw = source_path.read_bytes()
        locator = {"file": rel, "event_id": 1, "page_number": None,
                   "command_index": 0, "command_code": 355,
                   "parameter_index": 0, "assignment_index": 0,
                   "script_literal_offset": 39, "variable_id": 21,
                   "routed_common_event_id": 60}
        row = exporter.record(
            category="custom_dialogue", status="confirmed_dialogue",
            text="source", source_file=rel,
            source_hash=hashlib.sha256(raw).hexdigest(), locator=locator,
            context={"custom_header": "SPEAKER"},
            structure={"command_code": 355, "variable_id": 21,
                       "routed_common_event_id": 60, "raw_value": "SPEAKER.source",
                       "header": "SPEAKER", "separator": ".",
                       "script_literal": "'SPEAKER.source'"},
        )
        row["translation"] = "target"
        self.write_bundle([row])
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = json.loads((self.out / rel).read_text(encoding="utf-8"))
        script = patched[1]["list"][0]["parameters"][0]
        self.assertIn("'SPEAKER.target'", script)
        self.assertEqual(source_path.read_bytes(), raw)

    def test_protected_runtime_code_labels_cannot_be_translated_in_place(self):
        rel = "www/js/plugins/Labels.js"
        row = exporter.record(
            category="ui.plugin_static", status="confirmed_ui_text", text="PC",
            source_file=rel, source_hash="0" * 64,
            locator={"file": rel, "line": 1, "char_offset": 0,
                     "literal_index_in_file": 1},
            context={"translation_policy": "keep_source_value"}, structure={},
        )
        self.assertIsNone(applier.validate_record(row, False))
        row["translation"] = "Komputer"
        with self.assertRaisesRegex(ValueError, "protected from translation"):
            applier.validate_record(row, False)
        row["translation"] = "PC"
        self.assertEqual(applier.validate_record(row, False), "PC")

    def test_event_script_expression_writeback_is_safe_and_preserves_source(self):
        rel = "data/Map001.json"
        original = {
            "events": [None, {"id": 1, "pages": [{"conditions": {}, "list": [
                {"code": 122, "parameters": [111, 111, 0, 4, "'Source label'"]},
                {"code": 102, "parameters": [[r"\v[111]"], 0, 0, 1]},
            ]}]}]
        }
        source_path = self.source / rel
        source_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
        raw = source_path.read_bytes()
        with patch.object(exporter, "SOURCE_ROOT", self.source):
            row = exporter.variable_display_records(
                path=source_path, source_kind="map", map_id=1, map_name="Fixture",
                event=original["events"][1], page_number=1,
                page=original["events"][1]["pages"][0],
                source_hash=hashlib.sha256(raw).hexdigest(),
            )[0]
        row["translation"] = "Przetłumaczona etykieta"
        self.write_bundle([row])
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = json.loads((self.out / rel).read_text(encoding="utf-8"))
        expression = patched["events"][1]["pages"][0]["list"][0]["parameters"][4]
        self.assertEqual(expression, "'Przetłumaczona etykieta'")
        self.assertEqual(source_path.read_bytes(), raw)

    def test_token_loss_is_rejected(self):
        locator = {"file": "data/Items.json", "json_path": "/1/name"}
        row = exporter.record(
            category="database.items.name", status="confirmed_text_surface",
            text=r"Item \N[1]", source_file="data/Items.json",
            source_hash="0" * 64, locator=locator, context={}, structure={},
        )
        row["translation"] = "Item"
        with self.assertRaisesRegex(ValueError, "Markup/token mismatch"):
            applier.validate_record(row, False)

    def test_static_js_literals_are_patched_in_staging_copy_only(self):
        rel = "www/js/plugins/Labels.js"
        source_path = self.source / rel
        source_path.parent.mkdir(parents=True)
        text = "var labels = ['First', 'Second'];\r\n"
        source_path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        raw = source_path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        rows = []
        for source_text, translation in (("First", "A much longer first label"), ("Second", "Deuxième")):
            offset = text.index("'" + source_text + "'")
            locator = {"file": rel, "line": 1, "char_offset": offset, "literal_index_in_file": len(rows) + 1}
            row = exporter.record(
                category="ui.plugin_static", status="confirmed_ui_text",
                text=source_text, source_file=rel, source_hash=digest,
                locator=locator, context={}, structure={},
            )
            row["translation"] = translation
            rows.append(row)
        self.write_bundle(rows)
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = (self.out / rel).read_bytes()
        self.assertTrue(patched.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"'A much longer first label', 'Deuxi\xc3\xa8me'", patched)
        self.assertEqual(source_path.read_bytes(), raw)

    def test_static_template_literal_is_patched_as_plain_string(self):
        rel = "www/js/plugins/Labels.js"
        source_path = self.source / rel
        source_path.parent.mkdir(parents=True, exist_ok=True)
        text = "window.alert(`Static warning\nsecond line`);\n"
        source_path.write_text(text, encoding="utf-8")
        raw = source_path.read_bytes()
        literal = next(item for item in applier.iter_literals(text) if item["raw"].startswith("`"))
        self.assertFalse(literal["dynamic_template"])
        locator = {"file": rel, "line": 1, "char_offset": literal["start"],
                   "literal_index_in_file": 1}
        row = exporter.record(
            category="ui.plugin_static", status="confirmed_ui_text",
            text=literal["value"], source_file=rel,
            source_hash=hashlib.sha256(raw).hexdigest(), locator=locator,
            context={}, structure={"source_literal_kind": "template"},
        )
        row["translation"] = "Translated warning\nsecond line"
        self.write_bundle([row])
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = (self.out / rel).read_text(encoding="utf-8")
        self.assertIn('window.alert("Translated warning\\nsecond line");', patched)
        self.assertEqual(source_path.read_bytes(), raw)

    def test_plugin_parameter_is_patched_by_static_json_path(self):
        rel = "www/js/plugins.js"
        source_path = self.source / rel
        source_path.parent.mkdir(parents=True)
        raw = b'var $plugins = [{"name":"Plug","status":true,"parameters":{"Option Text":"Caption","Other":"x"}}];\r\n'
        source_path.write_bytes(raw)
        locator = {"file": rel, "plugin_index": 0, "plugin_name": "Plug",
                   "parameter_key": "Option Text", "json_path": "/$plugins/0/parameters/Option Text"}
        row = exporter.record(
            category="ui.plugin_parameter", status="confirmed_ui_text",
            text="Caption", source_file=rel, source_hash=hashlib.sha256(raw).hexdigest(),
            locator=locator, context={}, structure={},
        )
        self.assertEqual(row["source"]["writeback"], "plugin_parameter")
        row["translation"] = "Translated caption"
        self.write_bundle([row])
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        patched = (self.out / rel).read_bytes()
        self.assertIn(b'"Option Text":"Translated caption"', patched)
        self.assertIn(b'"Other":"x"', patched)
        self.assertEqual(source_path.read_bytes(), raw)

    def test_plain_text_line_writeback_preserves_line_endings(self):
        rel = "data/Credits.txt"
        source_path = self.source / rel
        raw = b"First line\r\nSecond line\nThird line"
        source_path.write_bytes(raw)
        locator = {"file": rel, "line_number": 2}
        row = exporter.record(
            category="credits", status="confirmed_text_surface", text="Second line",
            source_file=rel, source_hash=hashlib.sha256(raw).hexdigest(),
            locator=locator, context={"line_number": 2}, structure={},
        )
        self.assertEqual(row["source"]["writeback"], "text_file_line")
        row["translation"] = "Druga linia"
        self.write_bundle([row])
        applier.apply_records([self.inputs], self.source, self.out, False, False)
        self.assertEqual((self.out / rel).read_bytes(), b"First line\r\nDruga linia\nThird line")
        self.assertEqual(source_path.read_bytes(), raw)

    def test_stale_source_hash_is_rejected(self):
        rel = "data/Map001.json"
        source_path = self.source / rel
        source_path.write_text("{\"field\":\"old\"}", encoding="utf-8")
        row = exporter.record(
            category="test", status="confirmed_text_surface", text="old",
            source_file=rel, source_hash="0" * 64,
            locator={"file": rel, "json_path": "/field"},
            context={}, structure={},
        )
        row["translation"] = "new"
        self.write_bundle([row])
        with self.assertRaisesRegex(ValueError, "Source file hash mismatch"):
            applier.apply_records([self.inputs], self.source, self.out, True, False)


if __name__ == "__main__":
    unittest.main()
