import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRANSLATION = ROOT / 'games/the-genesis-order/translation'
sys.path.insert(0, str(ROOT / 'games/the-genesis-order/tools'))

import apply_translation as applier  # noqa: E402
import export_translation as exporter  # noqa: E402
import markup_signature as signature  # noqa: E402


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


class MarkupSignatureTests(unittest.TestCase):
    def test_no_argument_tag_is_split_from_text(self):
        self.assertEqual(signature.tokens_v2('\\fbCraft this item?'), ['\\fb'])
        self.assertEqual(signature.tokens_v2('\\fb\\c[19]Bold'), ['\\fb', '\\c[19]'])
        self.assertEqual(signature.tokens_v2('\\fb'), ['\\fb'])

    def test_other_tags_keep_v1_behaviour(self):
        text = '\\fn<Special Elite>\\TA[2]\\c[15]$150<br>\\TA[0]'
        self.assertEqual(signature.tokens_v2(text), exporter.tokens(text))

    def test_preserve_requires_all_tokens(self):
        self.assertTrue(signature.preserves_v2_signature('\\fbCraft this item?',
                                                         '\\fbWytworzyć przedmiot?'))
        self.assertFalse(signature.preserves_v2_signature('\\fbCraft this item?',
                                                          'Wytworzyć przedmiot?'))
        self.assertFalse(signature.preserves_v2_signature('Hello\\!', 'Cześć'))

    def test_canonical_impact_is_limited_to_the_known_block(self):
        rows = [row for path in sorted((TRANSLATION / 'export-v1').glob('*.jsonl'))
                for row in read_jsonl(path)]
        report = signature.signature_impact(rows)
        self.assertEqual(report['records'], 45229)
        self.assertEqual(report['changed_records'], 94)
        self.assertEqual(report['changed_categories'], ['native_message'])
        self.assertEqual(len(set(report['changed_ids'])), 94)


class PendingCraftingBatchTests(unittest.TestCase):
    """Records that v1 cannot validate but v2 can, kept outside `drafts/` on purpose."""

    @classmethod
    def setUpClass(cls):
        cls.canonical = {row['id']: row
                         for path in sorted((TRANSLATION / 'export-v1').glob('*.jsonl'))
                         for row in read_jsonl(path)}
        cls.path = TRANSLATION / 'pending/crafting-ui-map46-01.jsonl'
        cls.rows = read_jsonl(cls.path)

    def test_batch_shape(self):
        self.assertEqual(len(self.rows), 94)
        self.assertEqual(len({row['id'] for row in self.rows}), 94)
        self.assertEqual({row['category'] for row in self.rows}, {'native_message'})
        self.assertEqual({(row['context'] or {}).get('map_name') for row in self.rows},
                         {'Crafting'})

    def test_rows_match_canonical_and_keep_v2_tokens(self):
        for row in self.rows:
            with self.subTest(id=row['id']):
                self.assertIn(row['id'], self.canonical)
                self.assertEqual(
                    {key: value for key, value in row.items() if key != 'translation'},
                    {key: value for key, value in self.canonical[row['id']].items()
                     if key != 'translation'},
                )
                self.assertTrue(row['translation'].strip())
                self.assertNotEqual(row['translation'], row['source_text'])
                self.assertTrue(signature.preserves_v2_signature(row['source_text'],
                                                                 row['translation']))

    def test_v1_rejects_this_batch_by_token_signature(self):
        for row in self.rows:
            with self.subTest(id=row['id']):
                with self.assertRaisesRegex(ValueError, 'Markup/token mismatch'):
                    applier.validate_record(row, require_complete=True)

    def test_wording_is_consistent(self):
        wording = {row['source_text']: row['translation'] for row in self.rows}
        self.assertEqual(len(wording), 2)
        self.assertEqual(wording[
            '\\fs[22]<br> <br>\\fs[25]\\fn<Josefin Sans SemiBold>\\fbCraft this item?'],
            '\\fs[22]<br> <br>\\fs[25]\\fn<Josefin Sans SemiBold>\\fbWytworzyć przedmiot?')
        self.assertEqual(wording[
            '\\fs[22]<br> <br>\\fs[25]\\fn<Josefin Sans SemiBold>\\fbYou have items missing from this recipe.'],
            '\\fs[22]<br> <br>\\fs[25]\\fn<Josefin Sans SemiBold>\\fbBrakuje przedmiotów z tej receptury.')


class PhoneFragmentBatchTests(unittest.TestCase):
    def test_single_fragment_is_valid_and_unique(self):
        export = TRANSLATION / 'export-v1'
        canonical = {row['id']: row for path in sorted(export.glob('*.jsonl'))
                     for row in read_jsonl(path)}
        rows = read_jsonl(TRANSLATION / 'drafts/phone-select-item-fragment-01.jsonl')
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertIn(row['id'], canonical)
        self.assertEqual(applier.validate_record(row, require_complete=True),
                         row['translation'])
        self.assertEqual(row['source_text'], 'He’s going to be<br>')
        self.assertEqual(row['translation'], 'On będzie<br>')
        others = [other['id'] for path in (TRANSLATION / 'drafts').rglob('*.jsonl')
                  if path.name != 'phone-select-item-fragment-01.jsonl'
                  for other in read_jsonl(path)
                  if (other.get('translation') or '').strip()]
        self.assertNotIn(row['id'], others)


if __name__ == '__main__':
    unittest.main()
