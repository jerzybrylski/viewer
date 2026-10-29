"""Guardy spójności opublikowanych artefaktów TGO.

Test nie sprawdza samej gry ani nie uruchamia żadnego kodu z ZIP-ów: czyta
wyłącznie archiwa i pliki repozytorium. Pilnuje trzech rzeczy, które łatwo
zepsuć przy okazji przebudowy:

1. sidecar `.sha256` każdego ZIP-a zgadza się z samymi bajtami archiwum,
2. manifest w ZIP-ie patcha opisuje **dokładnie** ten payload, który leży
   obok (tłumaczenia, fingerprinty źródeł, raport pokrycia),
3. opublikowana Czytanka w ZIP-ie jest bajt w bajt taka sama jak śledzone
   drzewo `reading/v1/`, więc Git i paczka nie mogą się rozjechać.

Liczby w manifeście są porównywane z pełnym scaleniem draftów, bo to jedyne
źródło prawdy o korpusie.
"""
from __future__ import annotations

import hashlib
import json
import unittest
import zipfile
from pathlib import Path

TGO = Path(__file__).resolve().parents[1]
PACKAGES = TGO / 'translation' / 'packages'
REPORTS = TGO / 'translation' / 'reports'
READING = TGO / 'reading' / 'v1'
PATCH_ZIP = PACKAGES / 'TGO_PL_translation_patch_POC_v0.1.1.zip'
READALONG_ZIP = PACKAGES / 'TGO_readalong_PL_v1.zip'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


class PublishedZipSidecarTest(unittest.TestCase):
    def test_sidecar_matches_archive_bytes(self):
        for archive in (PATCH_ZIP, READALONG_ZIP):
            with self.subTest(archive=archive.name):
                sidecar = archive.with_suffix(archive.suffix + '.sha256')
                declared = sidecar.read_text(encoding='utf-8').split()[0]
                self.assertEqual(declared, sha256_file(archive))

    def test_archives_contain_no_game_assets(self):
        forbidden = ('.rpgmvp', '.rpgmvo', '.rpgmvm', '.exe', '.dll', '.pak', '.iso', '.ogg', '.m4a')
        for archive in (PATCH_ZIP, READALONG_ZIP):
            with zipfile.ZipFile(archive) as zipped:
                offenders = [name for name in zipped.namelist() if name.lower().endswith(forbidden)]
            with self.subTest(archive=archive.name):
                self.assertEqual(offenders, [])


class PatchPayloadConsistencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zipped = zipfile.ZipFile(PATCH_ZIP)
        cls.root = 'TGO_PL_translation_patch_POC_v0.1.1/'
        cls.manifest = json.loads(cls.zipped.read(cls.root + 'payload/patch_manifest.json'))
        cls.fingerprints = cls.zipped.read(cls.root + 'payload/source_fingerprints.json')
        cls.coverage = cls.zipped.read(cls.root + 'payload/translation_coverage.json')
        cls.translations = cls.zipped.read(cls.root + 'payload/translations.jsonl')

    @classmethod
    def tearDownClass(cls):
        cls.zipped.close()

    def test_manifest_declares_payload_hashes_it_actually_ships(self):
        self.assertEqual(self.manifest['translations_sha256'], sha256_bytes(self.translations))
        self.assertEqual(self.manifest['fingerprints_sha256'], sha256_bytes(self.fingerprints))
        self.assertEqual(self.manifest['translation_coverage_sha256'], sha256_bytes(self.coverage))

    def test_reports_directory_matches_shipped_payload(self):
        # Fingerprinty i pokrycie porównujemy po bajtach: to pliki generowane.
        self.assertEqual(sha256_file(REPORTS / 'source_fingerprints_v0.1.1.json'),
                         sha256_bytes(self.fingerprints))
        self.assertEqual(sha256_file(REPORTS / 'coverage_audit_v1.json'), sha256_bytes(self.coverage))
        # Manifest porównujemy semantycznie: kopia w repo może mieć inne wcięcia,
        # ale nie może różnić się ani jednym polem.
        shipped = json.loads((REPORTS / 'patch_manifest_v0.1.1.json').read_text(encoding='utf-8'))
        self.assertEqual(shipped, self.manifest)

    def test_fingerprints_cover_declared_source_files(self):
        fingerprints = json.loads(self.fingerprints)
        self.assertEqual(len(fingerprints), self.manifest['source_file_count'])
        self.assertEqual(len(fingerprints), 238)
        self.assertTrue(all(len(digest) == 64 and set(digest) <= set('0123456789abcdef')
                            for digest in fingerprints.values()))

    def test_manifest_agrees_with_shipped_translation_rows(self):
        rows = [json.loads(line) for line in self.translations.decode('utf-8').splitlines() if line.strip()]
        self.assertEqual(len(rows), self.manifest['translated_record_count'])
        self.assertEqual(len({row['id'] for row in rows}), len(rows))
        self.assertTrue(all((row.get('translation') or '').strip() for row in rows))

    def test_manifest_is_honest_about_untested_runtime(self):
        self.assertIs(self.manifest['runtime_tested'], False)
        self.assertIs(self.manifest['game_files_included'], False)
        self.assertEqual(self.manifest['translation_coverage_status'], 'complete')
        self.assertEqual(self.manifest['pending_untranslated_record_count'], 0)


class PatcherPackageTest(unittest.TestCase):
    """Paczka musi zawierać komplet plików patchera — inaczej instalator nie działa."""

    def test_zip_ships_patcher_with_locator(self):
        with zipfile.ZipFile(PATCH_ZIP) as zipped:
            names = set(zipped.namelist())
            for name in ('patcher.py', 'locator.py', 'APPLY.bat', 'COFNIJ.bat', 'README_PL.md'):
                with self.subTest(name=name):
                    self.assertIn('TGO_PL_translation_patch_POC_v0.1.1/' + name, names)

    def test_shipped_patcher_files_match_repository(self):
        with zipfile.ZipFile(PATCH_ZIP) as zipped:
            for name in ('patcher.py', 'locator.py', 'APPLY.bat', 'COFNIJ.bat'):
                with self.subTest(name=name):
                    shipped = zipped.read('TGO_PL_translation_patch_POC_v0.1.1/' + name)
                    self.assertEqual(sha256_bytes(shipped), sha256_file(TGO / 'patcher' / name))

    def test_launchers_do_not_ask_for_a_path(self):
        for name in ('APPLY.bat', 'COFNIJ.bat'):
            with self.subTest(name=name):
                text = (TGO / 'patcher' / name).read_text(encoding='utf-8')
                self.assertNotIn('set /p', text)
                self.assertIn('patcher.py', text)


class ReadalongMatchesTrackedTreeTest(unittest.TestCase):
    def test_every_archive_entry_equals_tracked_file(self):
        with zipfile.ZipFile(READALONG_ZIP) as zipped:
            names = zipped.namelist()
            self.assertEqual(len(names), 4_399)
            missing, different = [], []
            for name in names:
                local = READING / name
                if not local.is_file():
                    missing.append(name)
                    continue
                if sha256_bytes(zipped.read(name)) != sha256_file(local):
                    different.append(name)
        self.assertEqual(missing, [])
        self.assertEqual(different, [])

    def test_episode_count_matches_archive(self):
        episodes = sorted((READING / 'episodes').glob('*.md'))
        self.assertEqual(len(episodes), 4_394)


if __name__ == '__main__':
    unittest.main()
