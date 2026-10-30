"""Podgląd sceny jest tylko do odczytu i nie zmienia inwentarza."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import show_gender_scene as scene


def row(id, text, index, *, header='McFlOp', scene_id=7, translation=None):
    return {'id': id, 'category': 'custom_dialogue', 'source_text': text,
            'translation': translation if translation is not None else text,
            'context': {'source_kind': 'common_event', 'event_id': scene_id,
                        'command_index': index, 'custom_header': header,
                        'speaker_status': 'header_requires_mapping'}}


class ShowGenderSceneTest(unittest.TestCase):
    def setUp(self):
        self.rows = [row('a', 'Pierwsza.', 3), row('b', 'Druga.', 1, header='LiMaOpNo1'),
                     row('c', 'Inna scena.', 2, scene_id=8)]

    def test_scene_is_sorted_by_command_index_and_marked(self):
        lines = scene.render(self.rows, self.rows[0], window=4)
        positions = [line for line in lines if line.startswith(('>> #', '   #'))]
        self.assertEqual([line.split('#')[1].split()[0] for line in positions], ['1', '3'])
        self.assertTrue(any(line.startswith('>> #   3') for line in lines))
        self.assertIn('     PL: Pierwsza.', lines)

    def test_only_scene_excludes_other_locators(self):
        lines = scene.render(self.rows, self.rows[0], only_scene=True)
        self.assertFalse(any('Inna scena.' in line for line in lines))
        self.assertTrue(any('Lillian' in line for line in lines))

    def test_render_does_not_modify_rows(self):
        before = json.dumps(self.rows, ensure_ascii=False, sort_keys=True)
        scene.render(self.rows, self.rows[0], window=6)
        self.assertEqual(before, json.dumps(self.rows, ensure_ascii=False, sort_keys=True))

    def test_load_and_find_work_on_inventory_file(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'inventory.jsonl'
            path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in self.rows) + '\n',
                            encoding='utf-8')
            loaded = scene.load(path)
            self.assertEqual(len(loaded), 3)
            self.assertEqual(scene.find(loaded, target_id='b', locator_key=None)['translation'], 'Druga.')
            self.assertEqual(scene.find(loaded, target_id=None, locator_key='ce:8')['id'], 'c')
            self.assertIsNone(scene.find(loaded, target_id='zzz', locator_key=None))


class RelatedToolingGuardTest(unittest.TestCase):
    def test_scene_tool_has_no_write_calls(self):
        source = (Path(__file__).resolve().parents[1] / 'tools' / 'show_gender_scene.py').read_text(encoding='utf-8')
        for forbidden in ('write_text', 'write_bytes', '.unlink(', 'shutil', "'w'", '"w"'):
            self.assertNotIn(forbidden, source)
