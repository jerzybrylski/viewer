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
    # Nagłówek Erica wskazuje ciało; w scenie mówi Daemalius.
    'fc45bddff4fb76abcab1': 'Otworzyłem szczelinę do Piekła… A raczej zmuszono mnie, bym ją otworzył.',
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
    'b85b3157f8693c481d1c': 'Nie myślałaś chyba, że przyjdę nieprzygotowany?',
    'bcf7057b4048b621fa3b': 'Wróciłeś po kawałki?',
    'ec3d9c8b8435db8fe730': 'Och! Ale jesteśmy niegrzeczni!',
    '319431f0cc23d669a940': 'Trzeba było o tym pomyśleć, zanim założyłeś kajdanki.',
    '534e3783b66a9268a4b3': 'Wciąż nie wiesz, kiedy trzymać język za zębami… Może chcesz zostać ukarana.',
    'b0d06fae7aa8280dd2af': 'Masz Tomę. Dałem ci to, czego potrzebowałaś, więc puść Judy.',
    'bc0a7c67383dd0bbc1c4': 'Siostro… Nie widziałem tej twarzy od dziesięcioleci.',
    '0637a5f45ab867cdf577': 'Oddałem ci duszę, a ty wykorzystałaś ją, by sprowadzić Lilith na ten świat? Gdzie twoja lojalność?',
    '8f439e4428239d8b2619': 'Mieliśmy działać razem! Miałaś moją duszę! Dlaczego uwięziłaś mnie w tym kamieniu?',
    '17cd9e74af03bf68be65': 'Zadarłaś z niewłaściwym demonem!',
    '4efea59625145e305e3f': 'Och, Heather… Odkąd cię zobaczyłem, marzę, żeby dotknąć twojego ciała.',
    '4e4c3750fcc1d3bec31b': 'Nie zamierzam brać łapówek. Jestem w to zaangażowany tylko dlatego, że chcę wiedzieć, co dzieje się w rezydencji…',
    '37b388a1d2c7a43dadef': 'Eee… Niczego nie widziałeś.',
    '57b98b0dcff229da0aa4': 'Jak zawsze piękna.',
    'e45029b4b9ee9c7538b9': 'Masz mnie za idiotę? Co planujesz zrobić?',
    'cf4117322af096480ff1': 'Nie powiedziałeś im, że przyjdę?',
    'd598afd8b9e319055625': 'Co? Przecież wszyscy się przyjaźnimy.',
    '6f17daf4a48c9e3eb989': 'Nigdy nie byłam skłonna do modlitwy, ale chyba teraz warto zacząć.',
    '2ac50544bcb806cb9383': 'Myślałam, że miałeś iść do łóżka?',
    'ab94109fb68c4a39a738': 'Przysięgam, widziałem, jak coś tędy przeszło. Powinienem ostrzec ojca Solomona, że widziałem coś w pobliżu.',
    '37f31d8f2c6352536917': 'Powinienem już iść i zostawić was samych.',
    '48e4f232fafa276c467b': 'To nieprawda. Madalyn mnie oszukała. Nie powinienem był tego robić.',
    'debf2ed88bf76d6d9c69': 'Powinienem był wiedzieć, że narobisz kłopotów, Nellie.',
    '010e377fec6ef1b4bccb': 'Powinnam była zażądać remontu tego pokoju.',
    '84aabcb5a58b0547c0cc': 'Powinnam była zażądać remontu tego pokoju.',
    '5f4ae66f85c882e46017': 'W ogóle nie powinnam była pozwolić jej ich zatrzymać.',
    '76122d65516e20cb9248': 'W ogóle nie powinnam była pozwolić jej ich zatrzymać.',
    '4cebb82563feaa817574': 'Powinnam cię aresztować.',
    '5b4d4fe051f2b5aef215': 'Cholera. Może powinnam zdobyć nakaz przeszukania.',
    '104cdb56955b2370e3fc': 'Chyba powinnam już iść.',
    '18fa7986eba50d8c526b': 'Haha. Może powinnam przy niej nie zdejmować spodni.',
    '261df7f47b0d74431004': 'Co jest z wami dwojgiem? Jest coś, o czym powinnam wiedzieć?',
    '28e679b1e42f0c03a619': 'Chyba powinnam już iść.',
    '449691e37577ab141521': 'Eee, nie powinienem?',
    '4af19fe4126b34b652ad': 'Może powinienem dać jej chwilę, żeby się uspokoiła.',
    '6f9304fe2828ec2022e8': 'Tak, Lillian. Powinienem już iść.',
    '705c200ab22b936e4013': 'Ja… Nie wiem, czy powinienem mówić.',
    '7758e130fac2633aa75c': 'Nie powinienem mówić. Ale ma sprzeczne myśli.',
    '8b5e041b316387582cca': 'Chyba powinienem się odwdzięczyć.',
    'b21ff18b7ff251c08715': 'To ty mi powiedz. Jest coś, o czym powinnam wiedzieć?',
    'b768b4aadb1becb3bf90': 'Robi się późno. Może powinienem już zostawić cię samą.',
    'd960175e497002f4f948': 'Jeśli nie masz nic przeciwko, powinienem już iść.',
    'e0587f4ba1b35ae10007': 'Jeśli chcesz iść na wędrówkę, może powinienem iść z tobą.',
    '014ec417113dcd263344': 'Spokojnie. Zachowujesz się, jakbyś chciała wkurzyć Andreę.',
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
