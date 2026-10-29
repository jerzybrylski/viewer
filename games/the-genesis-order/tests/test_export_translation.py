from __future__ import annotations

import importlib.util
import hashlib
import json
import tempfile
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import curate_js_translation as curator  # noqa: E402
import scan_js_text_candidates as js_scanner  # noqa: E402

MODULE_PATH = TOOLS / "export_translation.py"
SPEC = importlib.util.spec_from_file_location("tgo_export_translation", MODULE_PATH)
assert SPEC and SPEC.loader
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)
MANIFEST_PATH = Path(__file__).resolve().parents[1] / "tools" / "build_source_manifest.py"
MANIFEST_SPEC = importlib.util.spec_from_file_location("tgo_build_source_manifest", MANIFEST_PATH)
assert MANIFEST_SPEC and MANIFEST_SPEC.loader
manifest_builder = importlib.util.module_from_spec(MANIFEST_SPEC)
MANIFEST_SPEC.loader.exec_module(manifest_builder)


class ExportTranslationTests(unittest.TestCase):
    def test_ids_are_stable_and_locator_based(self):
        first = {"file": "data/Map001.json", "command_index": 12}
        same = {"command_index": 12, "file": "data/Map001.json"}
        changed = {"file": "data/Map001.json", "command_index": 13}
        self.assertEqual(exporter.canonical_id("message", first),
                         exporter.canonical_id("message", same))
        self.assertNotEqual(exporter.canonical_id("message", first),
                            exporter.canonical_id("message", changed))
        self.assertNotIn("sample", exporter.canonical_id("message", first))
        # Approved category names retain IDs already issued in the earlier source bundle.
        self.assertEqual(exporter.canonical_id("native_message", first),
                         exporter.canonical_id("native_message_unclassified", first))
        self.assertEqual(exporter.canonical_id("choice_option", first),
                         exporter.canonical_id("choice_unclassified", first))

    def test_json_pointer_escapes_reserved_characters(self):
        self.assertEqual(exporter.pointer("a/b", "x~y"), "/a~1b/x~0y")

    def test_speaker_match_requires_unique_face_asset_mapping(self):
        header = {"faceName": "FixtureFace", "faceIndex": 2}
        unique = exporter.speaker_for(
            header,
            {("FixtureFace", 2): [{"actor_id": 7, "name": "Fixture Actor"}]},
        )
        self.assertEqual(unique["actor_id"], 7)
        self.assertEqual(unique["confidence"], "unique_actor_face_match")

        ambiguous = exporter.speaker_for(
            header,
            {("FixtureFace", 2): [
                {"actor_id": 7, "name": "Fixture Actor"},
                {"actor_id": 8, "name": "Another Fixture Actor"},
            ]},
        )
        self.assertEqual(ambiguous["confidence"], "face_asset_only")
        self.assertNotIn("actor_id", ambiguous)
        self.assertIsNone(exporter.speaker_for({}, {}))

    def test_review_curation_reports_excluded_and_unreviewed_candidates(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "www/js/fixture.js"
            source.parent.mkdir(parents=True)
            source.write_text('const fixture = "synthetic";\n', encoding="utf-8")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            candidate_rows = []
            for offset, text in enumerate(("Fixture UI", "Fixture symbol", "Fixture pending")):
                locator = {"file": "www/js/fixture.js", "line": 1,
                           "char_offset": offset, "literal_index_in_file": offset + 1}
                candidate_rows.append(js_scanner.make_record(
                    "js_display_literal_candidate", text, "www/js/fixture.js", digest,
                    locator, {"plugin_name": "Fixture", "plugin_status": "enabled",
                              "nearby_display_api_names": ["drawText"], "heuristic_only": True},
                ))
            candidates = root / "candidates.jsonl"
            candidates.write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in candidate_rows),
                encoding="utf-8",
            )
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({
                "schema": "tgo-js-review-decisions-v1",
                "decisions": {candidate_rows[0]["id"]: {
                    "classification": "confirmed_ui_text", "category": "ui.plugin_static",
                    "reason": "Synthetic visible-text fixture."}},
                "deferred": {},
                "excluded": {candidate_rows[1]["id"]: "fixture_nontext"},
                "exclusion_reasons": {"fixture_nontext": "Synthetic internal-token fixture."},
            }), encoding="utf-8")
            output = root / "reviewed.jsonl"
            with patch.object(curator, "SOURCE_ROOT", root):
                result = curator.curate(candidates, output, decisions)
            manifest = json.loads(output.with_name("reviewed_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(result["candidate_count"], 3)
            self.assertEqual(result["records"], 1)
            self.assertEqual(result["excluded_candidates"], 1)
            self.assertEqual(result["unreviewed_candidates"], 1)
            self.assertFalse(manifest["complete_for_candidate_scan"])
            self.assertEqual(manifest["unreviewed_candidates"], 1)

    def test_markup_tokens_are_preserved_in_order(self):
        self.assertEqual(
            exporter.tokens(r"\N[2] joined \C[4]team\C[0] <b>ready</b> %1$s"),
            [r"\N[2]", r"\C[4]", r"\C[0]", "<b>", "</b>", "%1$s"],
        )

    def test_plugins_assignment_is_parsed_as_json_not_executed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "plugins.js"
            path.write_text(
                '// static fixture\nvar $plugins = [{"name":"Example","status":true}];\n',
                encoding="utf-8",
            )
            self.assertEqual(
                manifest_builder.plugin_rows(path),
                [{"name": "Example", "status": True}],
            )

    def test_script_channel_carries_choice_branch_and_page_conditions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "Map001.json"
            path.write_text("{}", encoding="utf-8")
            commands = [
                {"code": 102, "parameters": [["Choose"], 0, 0, 2]},
                {"code": 402, "parameters": [0, "Choose"]},
                {"code": 355, "parameters": ["$gameVariables.setValue(21, 'PERSON.sample')"]},
                {"code": 117, "parameters": [60]},
                {"code": 404, "parameters": []},
            ]
            event = {"id": 7, "name": "Fixture", "list": commands}
            page = {"conditions": {"switch1Valid": True, "switch1Id": 5}, "list": commands}
            with patch.object(exporter, "SOURCE_ROOT", root):
                rows = exporter.script_channel_records(
                    path=path, source_kind="map", map_id=1, map_name="Fixture",
                    event=event, page_number=2, page=page, source_hash="0" * 64,
                )
            self.assertEqual(len(rows), 1)
            context = rows[0]["context"]
            self.assertEqual(context["page_conditions"]["switch1Id"], 5)
            self.assertEqual(context["branch_path"][0]["kind"], "choice_branch")
            self.assertEqual(context["branch_path"][0]["option_index"], 0)

    def test_ce224_static_caption_values_are_extracted_not_renderer_markup(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "Map001.json"
            path.write_text("{}", encoding="utf-8")
            commands = [
                {"code": 355, "parameters": ['$gameVariables.setValue(97, "Fixture title");']},
                {"code": 655, "parameters": ['$gameVariables.setValue(98, "Fixture caption");']},
                {"code": 117, "parameters": [224]},
            ]
            event = {"id": 7, "name": "Fixture", "list": commands}
            with patch.object(exporter, "SOURCE_ROOT", root):
                rows = exporter.script_channel_records(
                    path=path, source_kind="map", map_id=1, map_name="Fixture",
                    event=event, page_number=1, page={"conditions": {}, "list": commands},
                    source_hash="0" * 64,
                )
                renderer, skipped = exporter.command_records(
                    path=path, source_kind="common_event", map_id=None, map_name="",
                    event={"id": 224, "name": "Fixture renderer", "list": [
                        {"code": 101, "parameters": ["", 0, 2, 1]},
                        {"code": 401, "parameters": [r"\\V[97]"]},
                        {"code": 401, "parameters": [r"\\V[98]"]},
                    ]}, page_number=None, page=None, source_hash="0" * 64,
                    face_index={},
                )
            self.assertEqual([row["source_text"] for row in rows], ["Fixture title", "Fixture caption"])
            self.assertEqual([row["category"] for row in rows], ["image_caption", "image_caption"])
            self.assertEqual([row["classification"] for row in rows], ["confirmed_ui", "confirmed_ui"])
            self.assertEqual(renderer, [])
            self.assertEqual(len(skipped), 2)

    def test_choice_branch_context_and_message_locator(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "Map001.json"
            path.write_text("{}", encoding="utf-8")
            commands = [
                {"code": 101, "parameters": ["HeroFace", 0, 0, 2]},
                {"code": 401, "parameters": [r"Test line \N[1]"]},
                {"code": 102, "parameters": [["Go", "Stay"], 0, 0, 2]},
                {"code": 402, "parameters": [0, "Go"]},
                {"code": 401, "parameters": ["Branch line"]},
                {"code": 404, "parameters": []},
            ]
            event = {"id": 3, "name": "Fixture", "list": commands}
            with patch.object(exporter, "SOURCE_ROOT", root):
                records, skipped = exporter.command_records(
                    path=path, source_kind="map", map_id=1, map_name="Fixture map",
                    event=event, page_number=1, page={"conditions": {}, "list": commands},
                    source_hash="0" * 64, face_index={},
                )
            self.assertEqual(skipped, [])
            message = next(item for item in records if item["source"]["locator"].get("command_index") == 4)
            self.assertEqual(message["source"]["locator"]["json_path"], "/list/4/parameters/0")
            self.assertEqual(message["context"]["branch_path"][0]["option_index"], 0)
            self.assertEqual(message["classification"], "confirmed_text_surface")
            self.assertEqual(message["context"]["translation_scope"], "full_player_facing_text")
            self.assertNotIn("semantic_subtype", message["context"])
            options = [item for item in records if item["category"] == "choice_option"]
            self.assertEqual([item["source"]["locator"]["option_index"] for item in options], [0, 1])
            self.assertTrue(all(item["classification"] == "confirmed_text_surface" for item in options))
            self.assertTrue(all(item["context"]["translation_scope"] == "full_player_facing_text" for item in options))
            self.assertTrue(all(item["context"]["visibility_evidence"] for item in options))
            self.assertTrue(all("semantic_subtype" not in item["context"] for item in options))
            self.assertEqual(len({item["id"] for item in records}), len(records))

    def test_static_variable_values_reaching_choices_are_extracted(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "Map001.json"
            path.write_text("{}", encoding="utf-8")
            commands = [
                {"code": 122, "parameters": [111, 111, 0, 4, "'Fixture option'"]},
                {"code": 122, "parameters": [116, 116, 0, 4, '\"$200\"']},
                {"code": 102, "parameters": [[r"\v[111] \c[14]\v[116]"], 0, 0, 1]},
                {"code": 401, "parameters": [r"Buy \\v[111] for \v[116]?"]},
            ]
            event = {"id": 7, "name": "Fixture", "list": commands}
            with patch.object(exporter, "SOURCE_ROOT", root):
                rows = exporter.variable_display_records(
                    path=path, source_kind="map", map_id=1, map_name="Fixture",
                    event=event, page_number=1, page={"conditions": {}, "list": commands},
                    source_hash="0" * 64,
                )
            self.assertEqual([row["source_text"] for row in rows], ["Fixture option", "$200"])
            self.assertEqual(rows[0]["source"]["writeback"], "event_script_expression")
            self.assertEqual(rows[0]["context"]["visible_sinks"][0]["surface"], "choice_menu")
            self.assertNotIn("translation_policy", rows[0]["context"])
            self.assertEqual(rows[1]["context"]["translation_policy"], "keep_source_value")

    def test_nonliteral_variable_expression_is_not_exported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "Map001.json"
            path.write_text("{}", encoding="utf-8")
            commands = [
                {"code": 122, "parameters": [111, 111, 0, 4, "getOptionLabel()"]},
                {"code": 102, "parameters": [[r"\v[111]"], 0, 0, 1]},
            ]
            with patch.object(exporter, "SOURCE_ROOT", root):
                rows = exporter.variable_display_records(
                    path=path, source_kind="map", map_id=1, map_name="Fixture",
                    event={"id": 7, "name": "Fixture", "list": commands},
                    page_number=1, page={"conditions": {}, "list": commands},
                    source_hash="0" * 64,
                )
            self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
