import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import export_translation as exporter
import merge_translation_batches as merger


REPO_ROOT = Path(__file__).resolve().parents[3]
TRANSLATION = REPO_ROOT / 'games/the-genesis-order/translation'


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.canonical = self.root / 'canonical.jsonl'
        self.batch = self.root / 'batch.jsonl'
        self.out = self.root / 'private' / 'result.jsonl'
        self.row = exporter.record(category='database.items.name', status='confirmed_text_surface',
            text='Item %1', source_file='data/Items.json', source_hash='a' * 64,
            locator={'file': 'data/Items.json', 'json_path': '/1/name'}, context={}, structure={})
        self.write(self.canonical, [self.row])

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write(path, rows):
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))

    def merge(self, batches=None):
        return merger.merge_batches(self.canonical, batches or [self.batch], self.out, self.root / 'private')

    def test_merge_and_no_overwrite(self):
        row = dict(self.row, translation='Przedmiot %1')
        self.write(self.batch, [row])
        report = self.merge()
        self.assertEqual(report['with_translation'], 1)
        self.assertEqual(json.loads(self.out.read_text())['translation'], 'Przedmiot %1')
        with self.assertRaises(FileExistsError):
            self.merge()

    def test_reject_changed_source_and_missing_token(self):
        self.write(self.batch, [dict(self.row, source_text='Changed', translation='X')])
        with self.assertRaisesRegex(ValueError, 'metadata changed'):
            self.merge()
        self.write(self.batch, [dict(self.row, translation='Przedmiot')])
        with self.assertRaisesRegex(ValueError, 'Additional control'):
            self.merge()
        self.assertFalse(self.out.exists())

    def test_conflict_and_identical_repeat(self):
        other = self.root / 'other.jsonl'
        self.write(self.batch, [dict(self.row, translation='Przedmiot %1')])
        self.write(other, [dict(self.row, translation='Rzecz %1')])
        with self.assertRaisesRegex(ValueError, 'Conflicting translations'):
            self.merge([self.batch, other])
        self.write(other, [dict(self.row, translation='Przedmiot %1')])
        self.assertEqual(self.merge([self.batch, other])['with_translation'], 1)

    def test_tracked_output_allowed_and_canonical_protected(self):
        self.write(self.batch, [dict(self.row, translation='Przedmiot %1')])
        tracked = self.root / 'games/the-genesis-order/translation'
        with patch.object(merger, 'REPO_ROOT', self.root):
            result = merger.merge_batches(self.canonical, [self.batch], tracked / 'drafts/merged.jsonl', self.root / 'private')
            self.assertEqual(result['with_translation'], 1)
            with self.assertRaisesRegex(ValueError, 'canonical source export'):
                merger.merge_batches(self.canonical, [self.batch], tracked / 'export-v1/merged.jsonl', self.root / 'private')

    def test_nested_batch_folders_are_found(self):
        nested = self.root / 'drafts' / 'hints'
        nested.mkdir(parents=True)
        self.write(nested / 'nested.jsonl', [dict(self.row, translation='Przedmiot %1')])
        self.assertEqual(merger.merge_batches(self.canonical, [self.root / 'drafts'],
                                              self.out, self.root / 'private')['with_translation'], 1)

    def test_reject_output_outside_private_root(self):
        self.write(self.batch, [self.row])
        with self.assertRaisesRegex(ValueError, 'under the translation workspace'):
            merger.merge_batches(self.canonical, [self.batch], self.root / 'out', self.root / 'private')

    def test_current_full_draft_corpus_is_reconciled(self):
        batches = sorted((TRANSLATION / 'drafts').rglob('*.jsonl'))
        self.assertEqual(len(batches), 427)
        with tempfile.TemporaryDirectory(dir=TRANSLATION) as temp_dir:
            output = Path(temp_dir) / 'full-merge.jsonl'
            report = merger.merge_batches(
                TRANSLATION / 'export-v1', batches, output,
                REPO_ROOT / 'google_drive',
            )
        self.assertEqual(report['records'], 45_229)
        self.assertEqual(report['with_translation'], 39_917)
        self.assertEqual(report['protected'], 131)
        self.assertEqual(report['pending_translatable'], 5_181)

    def test_patch_payload_is_reproducible_from_tracked_drafts(self):
        """ZIP patcha musi dać się odtworzyć wyłącznie z plików w Git.

        Liczymy payload dokładnie tak, jak robi to builder (same przetłumaczone
        wiersze, ten sam porządek i serializacja) i porównujemy z hashem
        zapisanym w manifeście opublikowanej paczki.
        """
        manifest = json.loads(
            (TRANSLATION / 'reports' / 'patch_manifest_v0.1.1.json').read_text(encoding='utf-8'))
        batches = sorted((TRANSLATION / 'drafts').rglob('*.jsonl'))
        with tempfile.TemporaryDirectory(dir=TRANSLATION) as temp_dir:
            merged = Path(temp_dir) / 'merged.jsonl'
            merger.merge_batches(TRANSLATION / 'export-v1', batches, merged,
                                 REPO_ROOT / 'google_drive')
            digest = hashlib.sha256()
            rows = 0
            with merged.open(encoding='utf-8') as stream:
                for line in stream:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    if not (row.get('translation') or '').strip():
                        continue
                    digest.update((json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8'))
                    rows += 1
        self.assertEqual(rows, manifest['translated_record_count'])
        self.assertEqual(digest.hexdigest(), manifest['translations_sha256'])


if __name__ == '__main__':
    unittest.main()
