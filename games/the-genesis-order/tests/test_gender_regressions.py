"""Ręcznie zweryfikowane przypadki rodzaju; nie zastępują audytu scen."""
import json
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    '731681528f0229140315': 'Nie proszę, żebyś cokolwiek mówił.',
    '772aac3f30b35ea1f16c': 'Gdybym cię nie znał, pomyślałbym, że próbujesz mi zaimponować.',
    'e6206f90f7f810868ff3': 'Gdybym to wiedział, powiedziałbym ci.',
    'fc45bddff4fb76abcab1': 'Otworzyłam szczelinę do Piekła… A raczej zmuszono mnie, bym ją otworzyła.',
}


class GenderRegressions(unittest.TestCase):
    def test_drafts_and_patch_contain_reviewed_forms(self):
        found = {}
        for path in (ROOT / 'translation/drafts').rglob('*.jsonl'):
            for line in path.read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                key = row['id'].rsplit(':', 1)[-1]
                if key in CASES:
                    self.assertNotIn(key, found)
                    found[key] = row['translation']
        self.assertEqual(found, CASES)
        archive = ROOT / 'translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip'
        with zipfile.ZipFile(archive) as zipped:
            payload = zipped.read('TGO_PL_translation_patch_POC_v0.1.1/payload/translations.jsonl')
        shipped = {}
        for line in payload.splitlines():
            row = json.loads(line)
            key = row['id'].rsplit(':', 1)[-1]
            if key in CASES:
                shipped[key] = row['translation']
        self.assertEqual(shipped, CASES)

    def test_readalong_contains_reviewed_forms(self):
        text = (ROOT / 'reading/v1/chronological_script_PL.md').read_text(encoding='utf-8')
        for expected in CASES.values():
            self.assertIn(expected, text)
