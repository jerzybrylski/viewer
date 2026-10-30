"""Wyszukiwanie kandydatów nie jest automatycznym sprawdzaniem rodzaju."""
import json
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import inventory_gender_review as audit


class GenderInventoryTest(unittest.TestCase):
    def test_conditional_and_second_person_signals(self):
        self.assertIn('conditional_1', audit.tags('Gdybym ją przesunęła…'))
        self.assertIn('conditional_2', audit.tags('Nie proszę, żebyś cokolwiek mówiła.'))
        self.assertIn('first_person', audit.tags('Widziałam ją.'))
        self.assertIn('second_person', audit.tags('Widziałeś ją.'))

    def test_ledger_entries_match_shipped_payload(self):
        root = Path(__file__).resolve().parents[1]
        ledger = root / 'translation/reports/gender_review_decisions.jsonl'
        decisions = [json.loads(line) for line in ledger.read_text(encoding='utf8').splitlines() if line.strip()]
        ids = [item['id'] for item in decisions]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(item['status'] in {'confirmed', 'corrected', 'deferred'} and item['basis'] for item in decisions))
        archive = root / 'translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip'
        with zipfile.ZipFile(archive) as zipped:
            data = zipped.read('TGO_PL_translation_patch_POC_v0.1.1/payload/translations.jsonl')
        rows = {row['id']: row for line in data.splitlines() if (row := json.loads(line))['id'] in ids}
        self.assertEqual(set(rows), set(ids))
        for item in decisions:
            self.assertEqual(audit.fingerprint(rows[item['id']]), item['fingerprint'])

    def test_decision_stales_if_text_or_context_changes(self):
        row = {'id': 'a', 'category': 'custom_dialogue', 'source_text': 'Hi',
               'translation': 'Cześć', 'context': {'event_id': 1}}
        decision = {'id': 'a', 'status': 'confirmed', 'fingerprint': audit.fingerprint(row), 'basis': 'scena'}
        result, summary = audit.inventory([row], set(), {'a': decision})
        self.assertEqual(summary['review_status_counts'], {'confirmed': 1})
        self.assertEqual(result[0]['review_status'], 'confirmed')
        changed = {**row, 'translation': 'Hej'}
        result, _ = audit.inventory([changed], set(), {'a': decision})
        self.assertEqual(result[0]['review_status'], 'stale')
        changed = {**row, 'context': {'event_id': 2}}
        result, _ = audit.inventory([changed], set(), {'a': decision})
        self.assertEqual(result[0]['review_status'], 'stale')

    def test_unflagged_is_not_reviewed_and_categories_are_not_excluded(self):
        rows = [
            {'id': 'a', 'category': 'custom_dialogue', 'translation': 'Dzień dobry.', 'context': {}},
            {'id': 'b', 'category': 'choice_option', 'translation': 'Gdybym wiedział.', 'context': {}},
            {'id': 'c', 'category': 'native_message', 'translation': '', 'context': {}},
        ]
        result, summary = audit.inventory(rows, {'b'})
        self.assertEqual(summary['translated_records'], 2)
        self.assertEqual(summary['unflagged_not_reviewed'], 1)
        self.assertEqual(summary['previous_automatic_edits_in_inventory'], 1)
        self.assertTrue(all(item['review_status'] == 'unreviewed' for item in result))
