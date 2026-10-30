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
    '1e453d51ecdd12c719e8': 'Chcesz, żebym ją puściła?',
    '989a5b730672c05374b5': 'Może gdybym ją przesunął, słyszelibyśmy lepiej.',
    'b548da6db98c6e1482b3': 'Co ja bym bez ciebie zrobił, Nellie?',
    '805322718946b90a0c26': 'Pewnie nie ma sposobu, żebym cię przekonała do oddania tego?',
    'a74a05017f8faa31c858': 'Gdybym ja budowała to miejsce, na pewno zrobiłabym drogę ucieczki.',
    '44e2f920fc02d2107b08': 'To worek nawozu, ale jest za ciężki, żebym go nosił…',
    'b51aa795298dc2e34fb5': 'Gdybym go trafił, leżałby nieprzytomny!',
    '6111effb5c551baea025': 'Haha! Chętnie bym to zobaczył.',
    '831f21f7534cd4f71410': 'A gdyby wypadło na ciebie? Chcesz, żebym cię pocałował?',
    '00f7684301aab72ed57d': 'Chętnie bym z nią porozmawiała.',
    '6be01627eba58ff91c0e': 'Chcę, żebyś dla mnie doszła.',
    'b293c6c1c4ecf9a593a2': 'Nawet jeśli trafisz do więzienia, nadal będziesz mi winna pieniądze.',
    '0724f59b187952bcfe79': 'Mało brakowało, a byś mnie zabiła.',
    '6107621dcc1a42c5b14b': 'Jeśli zadajesz się z przywódczyniami gangów, nie chcę, żebyś kręciła się koło mnie.',
    'e7ecd71c8b880a6f51c3': 'Mówiłem, żebyś się cofnęła!',
    'c9cf57b12f673e7b22c6': 'Dobra robota. Jestem ci winien przysługę.',
    '318d6be44e989ae84fce': 'Jestem ci winna przysługę.',
    '004b101d7150c5bf5af8': 'Jestem ci winna przysługę.',
    'da85a14ff34c9b0573b3': 'To co z tą przysługą, którą jesteś mi winna?',
    'bff363d1ef4587740825': 'Znalazłeś jakieś baterie?',
    '0c61171540385c7b127a': 'Mówiłaś, że to miejsce jest nawiedzone. Nie byłaś tak daleka od prawdy, jak myślałem.',
    'b475e41cafd81b039306': 'Sama mówiłaś, że chcesz działać…',
    '57c9fd33f3b925191a82': 'Ja będę bogata. To była moja robota.',
    '80f1339b592193226eb3': 'Sam niewiele wiem, ale słyszałem, że krąży wirus zwiększający popęd seksualny.',
    'a69f5a23d51d2a760972': 'Owszem. A z tego, co słyszę, ty i Chloe też podziwialiście stąd widoki.',
    '6e980340b70fea0bc53a': 'Powinnam była wiedzieć, żeby ci nie mówić, Carol.',
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
