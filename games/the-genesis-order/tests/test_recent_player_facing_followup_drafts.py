import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRANSLATION = ROOT / 'games/the-genesis-order/translation'
TOOLS = ROOT / 'games/the-genesis-order/tools'
sys.path.insert(0, str(TOOLS))

import apply_translation as applier  # noqa: E402


BATCH_COUNTS = {
    'custom-dialogue-common-event-npc-barks-followups-01.jsonl': 205,
    'custom-dialogue-common-event-npc-barks-followups-02.jsonl': 200,
    'custom-dialogue-common-event-dialogue-followups-03.jsonl': 195,
    'custom-dialogue-common-event-story-followups-04.jsonl': 192,
    'custom-dialogue-map151-hell-followups-02.jsonl': 192,
    'custom-dialogue-map19-followups-01.jsonl': 185,
    'custom-dialogue-map114-followups-01.jsonl': 178,
    'custom-dialogue-map203-courtroom-followups-01.jsonl': 171,
    'custom-dialogue-map61-gym-followups-01.jsonl': 156,
    'custom-dialogue-map25-dinner-followups-01.jsonl': 148,
    'custom-dialogue-map34-commissioner-followups-01.jsonl': 143,
    'custom-dialogue-map101-heather-sleepover-followups-01.jsonl': 142,
    'custom-dialogue-map12-arianna-followups-01.jsonl': 140,
    'custom-dialogue-map94-church-followups-01.jsonl': 139,
    'custom-dialogue-map52-ella-chloe-followups-01.jsonl': 135,
}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


class RecentPlayerFacingFollowupDraftTests(unittest.TestCase):
    def test_recent_batches_are_complete_canonical_dialogue(self):
        export = TRANSLATION / 'export-v1'
        canonical = {
            row['id']: row
            for path in sorted(export.glob('*.jsonl'))
            for row in read_jsonl(path)
        }
        drafts = TRANSLATION / 'drafts'
        recent_names = set(BATCH_COUNTS)
        existing_ids = {
            row['id']
            for path in drafts.rglob('*.jsonl')
            if path.name not in recent_names
            for row in read_jsonl(path)
            if isinstance(row.get('translation'), str) and row['translation'].strip()
        }
        seen = set()

        for filename, expected_count in BATCH_COUNTS.items():
            path = drafts / filename
            rows = read_jsonl(path)
            self.assertEqual(len(rows), expected_count, filename)
            for row in rows:
                with self.subTest(batch=filename, id=row.get('id')):
                    self.assertIn(row['id'], canonical)
                    self.assertEqual(
                        {key: value for key, value in row.items() if key != 'translation'},
                        {key: value for key, value in canonical[row['id']].items() if key != 'translation'},
                    )
                    self.assertEqual(row.get('category'), 'custom_dialogue')
                    self.assertEqual(row.get('classification'), 'confirmed_dialogue')
                    self.assertIn((row.get('context') or {}).get('source_kind'), {'map', 'common_event'})
                    self.assertNotEqual((row.get('context') or {}).get('translation_policy'), 'keep_source_value')
                    self.assertTrue(row.get('source_text', '').strip())
                    self.assertFalse(row['source_text'].lstrip().startswith('/'))
                    self.assertTrue(row.get('translation', '').strip())
                    self.assertEqual(applier.validate_record(row, require_complete=True), row['translation'])
                    self.assertNotIn(row['id'], existing_ids)
                    self.assertNotIn(row['id'], seen)
                    seen.add(row['id'])

        self.assertEqual(len(seen), sum(BATCH_COUNTS.values()))


if __name__ == '__main__':
    unittest.main()
