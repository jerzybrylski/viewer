import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import audit_draft_coverage as audit
import export_translation as exporter


def make_row(text, index, *, category='native_message',
             source_file='data/CommonEvents.json', context=None):
    # Distinct command indexes give every fixture row its own stable ID.
    return exporter.record(
        category=category, status='confirmed_text_surface', text=text,
        source_file=source_file, source_hash='a' * 64,
        locator={'file': source_file, 'json_path': f'/list/{index}/parameters/0',
                 'event_id': 1, 'command_index': index},
        context=context or {}, structure={})


class AuditDraftCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.export = self.root / 'export'
        self.drafts = self.root / 'drafts'
        self.export.mkdir()
        self.drafts.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write(path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')

    def build(self):
        self.covered = make_row('Hello there.', 0)
        self.nested = make_row('Nested batch line.', 1)
        self.conflict = make_row('Conflicting line.', 2)
        self.protected = make_row('PC', 3, category='ui.plugin_static',
                                  source_file='data/System.json',
                                  context={'translation_policy': 'keep_source_value'})
        self.command = make_row('/success', 4, category='custom_dialogue')
        self.markup = make_row('\\fn<Cinzel-Black>\\fs[70]<br>', 5)
        self.template = make_row('Text goes here<br>Text goes here<br>', 6)
        self.credits = make_row('Backer One, Backer Two<br>', 7, category='credits')
        self.name = make_row('Hannah', 8, category='image_caption',
                             source_file='data/Items.json')
        self.identifier = make_row('ECU', 9)
        self.blocked = make_row('\\fbCraft this item?', 10)
        self.review = make_row('Craft this optional item?', 11)
        self.identical = make_row('Left in English.', 12)
        rows = [self.covered, self.nested, self.conflict, self.protected, self.command,
                self.markup, self.template, self.credits, self.name, self.identifier,
                self.blocked, self.review, self.identical]
        self.write(self.export / 'all.jsonl', rows)
        self.write(self.drafts / 'batch-01.jsonl',
                   [dict(self.covered, translation='Witaj.'),
                    dict(self.nested, translation=''),
                    dict(self.conflict, translation='Wersja A.'),
                    dict(self.identical, translation='Left in English.')])
        self.write(self.drafts / 'nested' / 'batch-02.jsonl',
                   [dict(self.nested, translation='Zagnieżdżona linia.'),
                    dict(self.conflict, translation='Wersja B.')])
        return audit.audit(self.export, self.drafts)

    def test_nested_draft_folders_are_read(self):
        report = self.build()
        self.assertEqual(report['draft_files'], 2)
        self.assertEqual(report['draft_rows'], 6)
        self.assertEqual(report['covered_ids'], 4)
        blank_ids = {item['id'] for items in report['buckets'].values() for item in items}
        self.assertNotIn(self.nested['id'], blank_ids)

    def test_conflict_reports_both_files(self):
        report = self.build()
        self.assertEqual(len(report['conflicts']), 1)
        conflict = report['conflicts'][0]
        self.assertEqual(conflict['id'], self.conflict['id'])
        self.assertEqual({entry['file'] for entry in conflict['values']},
                         {'batch-01.jsonl', 'nested/batch-02.jsonl'})

    def test_blank_buckets(self):
        report = self.build()
        buckets = report['buckets']
        self.assertEqual([item['id'] for item in buckets['protected']], [self.protected['id']])
        self.assertEqual([item['id'] for item in buckets['command']], [self.command['id']])
        self.assertEqual([item['id'] for item in buckets['markup_only']], [self.markup['id']])
        self.assertEqual([item['id'] for item in buckets['template_placeholder']],
                         [self.template['id']])
        self.assertEqual([item['id'] for item in buckets['credits_roster']], [self.credits['id']])
        self.assertEqual([item['id'] for item in buckets['proper_name']], [self.name['id']])
        self.assertEqual([item['id'] for item in buckets['identifier']], [self.identifier['id']])
        self.assertEqual([item['id'] for item in buckets['blocked_by_signature']],
                         [self.blocked['id']])
        self.assertEqual([item['id'] for item in buckets['needs_review']], [self.review['id']])

    def test_identical_translation_is_flagged(self):
        report = self.build()
        self.assertEqual([item['id'] for item in report['identical_translations']],
                         [self.identical['id']])

    def test_markdown_report_contains_sections(self):
        text = audit.render_markdown(self.build())
        self.assertIn('## Kubełki pustych rekordów', text)
        self.assertIn('## Konflikty niepustych wariantów', text)
        self.assertIn('`blocked_by_signature`', text)


if __name__ == '__main__':
    unittest.main()
