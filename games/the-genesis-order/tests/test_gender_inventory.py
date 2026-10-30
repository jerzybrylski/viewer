"""Wyszukiwanie kandydatów nie jest automatycznym sprawdzaniem rodzaju."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import inventory_gender_review as audit


class GenderInventoryTest(unittest.TestCase):
    def test_conditional_and_second_person_signals(self):
        self.assertIn('conditional_1', audit.tags('Gdybym ją przesunęła…'))
        self.assertIn('conditional_2', audit.tags('Nie proszę, żebyś cokolwiek mówiła.'))
        self.assertIn('first_person', audit.tags('Widziałam ją.'))
        self.assertIn('second_person', audit.tags('Widziałeś ją.'))

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
