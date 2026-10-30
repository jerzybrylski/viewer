"""Partie są kolejką kandydatów, nie automatyczną korektą."""
import json
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import prepare_gender_review_batches as batches
import inventory_gender_review as inventory


def row(id, text, index, *, header='McFlOp', branch=None, scene=1, status='unreviewed', source='source'):
    return {'id': id, 'category': 'custom_dialogue', 'source_text': source,
            'translation': text, 'review_status': status,
            'context': {'source_kind': 'common_event', 'event_id': scene,
                        'command_index': index, 'custom_header': header, 'branch_path': branch or []}}


class ReviewBatchTest(unittest.TestCase):
    def test_known_examples_are_candidates_without_modification(self):
        for r in [row('a', 'Gdybym cię nie znała, pomyślałbym.', 1),
                  row('b', 'Nie proszę, żebyś cokolwiek mówiła.', 2, header='HnFlOp'),
                  row('c', 'Nadal będziesz mi winien pieniądze.', 3, header='JoAnOp'),
                  row('d', 'Ty i Chloe podziwiałyście stąd widoki.', 4, header='CaFlOp'),
                  row('e', 'Masz mnie za idiotkę?', 5, header='DmAnOp')]:
            original = r['translation']
            self.assertTrue(batches.signals(r))
            self.assertEqual(original, r['translation'])

    def test_separates_incompatible_branches_and_scenes(self):
        one = [{'kind': 'choice_branch', 'choice_group_id': 'g', 'option_index': 0}]
        other = [{'kind': 'choice_branch', 'choice_group_id': 'g', 'option_index': 1}]
        rows = [row('a', 'Wstęp.', 1), row('b', 'Gdybym to wiedziała.', 2, branch=one),
                row('c', 'Inna gałąź.', 3, branch=other), row('d', 'Następna.', 4, branch=one),
                row('e', 'Nie ta scena.', 3, branch=one, scene=2)]
        result, _ = batches.build_batches(rows)
        b = next(x for x in result if x['occurrences'][0]['id'] == 'b')
        self.assertEqual([x['id'] for x in b['occurrences'][0]['neighbors']], ['a', 'd'])

    def test_missing_scene_is_not_treated_as_a_shared_scene(self):
        a = row('a', 'Gdybym wiedziała.', 1)
        b = row('b', 'Druga kwestia.', 2)
        a['context'] = {'source_kind': None, 'custom_header': 'McFlOp'}
        b['context'] = {'source_kind': None, 'custom_header': 'HnFlOp'}
        result, _ = batches.build_batches([a, b])
        self.assertEqual(result[0]['occurrences'][0]['neighbors'], [])

    def test_duplicates_keep_all_ids_and_evidence(self):
        rows = [row('a', 'Chciałam wiedzieć.', 1, scene=1),
                row('b', 'Chciałam wiedzieć.', 1, scene=2)]
        groups, summary = batches.build_batches(rows)
        self.assertEqual(len(groups), 1)
        self.assertEqual(summary['candidate_records'], 2)
        self.assertEqual({x['id'] for x in groups[0]['occurrences']}, {'a', 'b'})
        self.assertNotEqual(groups[0]['occurrences'][0]['context']['event_id'],
                            groups[0]['occurrences'][1]['context']['event_id'])

    def test_context_snapshot_changes_when_neighbor_changes(self):
        rows = [row('a', 'Dzień dobry.', 1), row('b', 'Gdybym wiedziała.', 2)]
        first, _ = batches.build_batches(rows)
        rows[0]['translation'] = 'Co się dzieje?'
        second, _ = batches.build_batches(rows)
        self.assertNotEqual(first[0]['occurrences'][0]['context_snapshot_sha256'],
                            second[0]['occurrences'][0]['context_snapshot_sha256'])

    def test_unflagged_remains_unreviewed_and_reviewed_excluded(self):
        rows = [row('a', 'Dzień dobry.', 1), row('b', 'Chciałam.', 2, status='confirmed')]
        groups, summary = batches.build_batches(rows)
        self.assertEqual(groups, [])
        self.assertEqual(summary['unflagged_eligible_records'], 1)

    def test_historical_corrected_examples_are_candidates(self):
        # Znane przypadki nie są reprezentatywną próbką ani dowodem pełnego pokrycia.
        root = Path(__file__).resolve().parents[1]
        decisions = [json.loads(line) for line in
                     (root / 'translation/reports/gender_review_decisions.jsonl').read_text(encoding='utf8').splitlines()]
        selected = {d['id']: d for d in decisions if d['status'] == 'corrected' and 'before' in d}
        self.assertGreaterEqual(len(selected), 34)
        archive = root / 'translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip'
        with zipfile.ZipFile(archive) as zipped:
            data = zipped.read('TGO_PL_translation_patch_POC_v0.1.1/payload/translations.jsonl')
        records = {r['id']: r for line in data.splitlines() if (r := json.loads(line))['id'] in selected}
        self.assertEqual(set(records), set(selected))
        for id, decision in selected.items():
            record = records[id]
            record['translation'] = decision['before']
            record['flags'] = inventory.tags(record['translation'])
            record['previous_automatic_edit'] = False
            with self.subTest(id=id):
                self.assertTrue(batches.signals(record))

    def test_possession_is_only_a_warning_not_an_automatic_rewrite(self):
        r = row('a', 'Widziałem ją.', 1, header='ErAnOp', scene=456)
        self.assertIn('znane_opetanie_tozsamosc_mowcy', batches.signals(r))
        self.assertEqual(r['translation'], 'Widziałem ją.')
