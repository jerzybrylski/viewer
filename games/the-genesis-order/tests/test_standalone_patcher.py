import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "patcher"))
sys.path.insert(0, str(ROOT / "tools"))
import patcher as standalone
from export_translation import record


class StandalonePatcherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.install = self.root / "game"
        (self.install / "www" / "data").mkdir(parents=True)
        (self.install / "www" / "index.html").write_text("<html></html>", encoding="utf-8")
        self.items_bytes = b'[null,{"name":"Old"}]\n'
        self.system_bytes = b'[]\n'
        (self.install / "www" / "data" / "Items.json").write_bytes(self.items_bytes)
        (self.install / "www" / "data" / "System.json").write_bytes(self.system_bytes)

        self.package = self.root / "package"
        payload = self.package / "payload"
        payload.mkdir(parents=True)
        self.translations = payload / "translations.jsonl"
        self.fingerprints = payload / "source_fingerprints.json"
        self.manifest_path = payload / "patch_manifest.json"
        row = record(
            category="database.items.name", status="confirmed_text_surface", text="Old",
            source_file="data/Items.json",
            source_hash=hashlib.sha256(self.items_bytes).hexdigest(),
            locator={"file": "data/Items.json", "json_path": "/1/name"},
            context={}, structure={},
        )
        row["translation"] = "Nowy"
        self.translations.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
        self.fingerprints.write_text(json.dumps({
            "data/Items.json": hashlib.sha256(self.items_bytes).hexdigest(),
            "data/System.json": hashlib.sha256(self.system_bytes).hexdigest(),
        }), encoding="utf-8")
        self.manifest_path.write_text(json.dumps({
            "schema": "tgo-standalone-patch-v1",
            "patch_version": "test-0.1",
            "translations_sha256": self.digest(self.translations),
            "fingerprints_sha256": self.digest(self.fingerprints),
            "source_file_count": 2,
            "translated_record_count": 1,
        }), encoding="utf-8")
        self.old_paths = (standalone.PATCH_MANIFEST, standalone.TRANSLATIONS, standalone.FINGERPRINTS)
        standalone.PATCH_MANIFEST = self.manifest_path
        standalone.TRANSLATIONS = self.translations
        standalone.FINGERPRINTS = self.fingerprints

    def tearDown(self):
        standalone.PATCH_MANIFEST, standalone.TRANSLATIONS, standalone.FINGERPRINTS = self.old_paths
        self.temp.cleanup()

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_apply_backup_rollback_and_idempotence(self):
        result = standalone.install(self.install)
        self.assertEqual(result["status"], "installed")
        target = self.install / "www" / "data" / "Items.json"
        self.assertEqual(json.loads(target.read_text(encoding="utf-8"))[1]["name"], "Nowy")
        backup = self.install / ".tgo-pl-originals" / "test-0.1" / "www" / "data" / "Items.json"
        self.assertEqual(backup.read_bytes(), self.items_bytes)
        self.assertEqual(standalone.install(self.install)["status"], "already_installed")
        result = standalone.rollback(self.install)
        self.assertEqual(result["status"], "rolled_back")
        self.assertEqual(target.read_bytes(), self.items_bytes)
        self.assertTrue(backup.exists())
        self.assertEqual(standalone.rollback(self.install)["status"], "already_rolled_back")

    def test_rejects_source_mismatch_before_backup(self):
        target = self.install / "www" / "data" / "Items.json"
        target.write_bytes(b'[null,{"name":"Modified"}]\n')
        with self.assertRaisesRegex(ValueError, "nie pasują"):
            standalone.install(self.install)
        self.assertFalse((self.install / ".tgo-pl-originals").exists())
        self.assertEqual(target.read_bytes(), b'[null,{"name":"Modified"}]\n')

    def test_rollback_refuses_user_modified_patched_file(self):
        standalone.install(self.install)
        target = self.install / "www" / "data" / "Items.json"
        target.write_bytes(b'[null,{"name":"User edit"}]\n')
        with self.assertRaisesRegex(ValueError, "zmienił się"):
            standalone.rollback(self.install)
        self.assertIn(b"User edit", target.read_bytes())

    def test_rollback_recovers_interrupted_install_state(self):
        standalone.install(self.install)
        state_path = self.install / standalone.STATE_NAME
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "installing"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        result = standalone.rollback(self.install)
        self.assertEqual(result["status"], "rolled_back")
        self.assertEqual((self.install / "www" / "data" / "Items.json").read_bytes(), self.items_bytes)


class PatcherCliLocatingTests(unittest.TestCase):
    """CLI bez wpisywania ścieżki: autodetekcja, pamięć i tryb locate."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.install = self.root / "The Genesis Order"
        (self.install / "www" / "data").mkdir(parents=True)
        (self.install / "www" / "index.html").write_text("<html></html>", encoding="utf-8")
        (self.install / "www" / "data" / "System.json").write_text("[]\n", encoding="utf-8")
        self.config = self.root / "config" / "config.json"
        self.env = dict(os.environ, TGO_PATCH_CONFIG=str(self.config))

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "patcher" / "patcher.py"), *args],
            capture_output=True, text=True, encoding="utf-8", env=self.env, timeout=120,
        )

    def test_locate_persists_path_and_finds_it_without_arguments(self):
        first = self.run_cli("locate", "--no-gui", "--yes", "--search-root", str(self.root))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("located", first.stdout)
        saved = json.loads(self.config.read_text(encoding="utf-8"))
        self.assertEqual(Path(saved["game_path"]), self.install)

    def test_forget_clears_memory(self):
        self.run_cli("locate", "--no-gui", "--yes", "--search-root", str(self.root))
        forgotten = self.run_cli("--forget")
        self.assertEqual(forgotten.returncode, 0, forgotten.stderr)
        saved = json.loads(self.config.read_text(encoding="utf-8"))
        self.assertNotIn("game_path", saved)

    def test_without_memory_and_without_candidate_it_fails_cleanly(self):
        empty = self.root / "pusty"
        empty.mkdir()
        result = self.run_cli("locate", "--no-gui", "--yes", "--search-root", str(empty))
        self.assertEqual(result.returncode, 2)
        self.assertIn("--game", result.stderr)

    def test_help_documents_automatic_lookup(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--no-gui", result.stdout)
        self.assertIn("locate", result.stdout)


if __name__ == "__main__":
    unittest.main()
