"""Wąska kolejka jest tylko hipotezą, nie automatyczną korektą."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import focus_gender_candidates as focus
from test_gender_review_batches import row


class FocusGenderTest(unittest.TestCase):
    def test_first_person_and_detached_conditional(self):
        for text in ('Chciałam wiedzieć.', 'Gdybym cię nie znała, pomyślałbym.', 'Powinnam to wiedzieć.'):
            self.assertIn('pierwsza_osoba', [e['kind'] for e in focus.evidence(row('a', text, 1))])
        for text in ('Działam.', 'Chciałem wiedzieć.', 'Gdybym to wiedział.'):
            self.assertNotIn('pierwsza_osoba', [e['kind'] for e in focus.evidence(row('a', text, 1))])

    def test_addressee_and_predicate_hypotheses(self):
        r = row('a', 'Nadal będziesz mi winien pieniądze.', 1, header='JoAnOp')
        self.assertIn('adresat_z_sasiedztwa', [e['kind'] for e in focus.evidence(r, 'Erica')])
        self.assertFalse(focus.evidence(r, 'Mox'))
        r['translation'] = 'Jestem ci winien za pomoc.'
        self.assertNotIn('adresat_z_sasiedztwa', [e['kind'] for e in focus.evidence(r, 'Erica')])
        r['translation'] = 'Jestem bogata.'
        self.assertIn('orzecznik', [e['kind'] for e in focus.evidence(r)])

    def test_sam_can_refer_to_addressee(self):
        r = row('a', 'Sam się o to prosiłeś.', 1, header='HnFlOp')
        self.assertNotIn('sam_sama', [e['kind'] for e in focus.evidence(r)])

    def test_incompatible_branches_and_conflicting_neighbors(self):
        a = row('a', 'Cześć.', 1, header='HnFlOp')
        b = row('b', 'Wróciłaś.', 2)
        c = row('c', 'Cześć.', 3, header='ErFlOp')
        self.assertIsNone(focus.neighboring_speakers([a, b, c], 1)[0])
        self.assertEqual(focus.neighboring_speakers([a, b], 1)[0], 'Hannah')
        a['context']['branch_path'] = [{'kind': 'choice_branch', 'choice_group_id': 'g', 'option_index': 0}]
        b['context']['branch_path'] = [{'kind': 'choice_branch', 'choice_group_id': 'g', 'option_index': 1}]
        self.assertIsNone(focus.neighboring_speakers([a, b], 1)[0])

    def test_no_mutation_and_no_reviewed(self):
        rows = [row('a', 'Chciałam.', 1), row('b', 'Chciałam.', 2, status='confirmed')]
        original = [dict(r) for r in rows]
        candidates, _ = focus.focus(rows)
        self.assertEqual([r['id'] for r in candidates], ['a'])
        self.assertEqual(rows, original)


if __name__ == '__main__':
    unittest.main()
