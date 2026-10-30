# Audyt rodzaju — rozpoczęty 2026-10-30, NIEUKOŃCZONY

## Cel i granice

Właściciel zlecił pełny kontekstowy przegląd rodzaju mówcy, adresata i osób trzecich, w tym form rozdzielnych „gdybym … zrobiła” i „żebyś … mówiła”. Nie wolno utożsamiać liczby trafień heurystyki z liczbą błędów ani braku trafienia z poprawnością. Poprzednie narzędzie nie znajdowało niektórych takich form; wcześniejsze twierdzenia o zerze błędów pierwszej osoby były zbyt szerokie. Jego 618 wcześniejszych zmian również wymaga niezależnego przeglądu. Nie uruchamiano go ponownie z `--apply`.

## Bieżący stan

- Inwentaryzacja całego **walidowanego scalenia**: 39 917 niepustych tłumaczeń we wszystkich kategoriach. Osobno istnieją wartości źródłowe bez tłumaczenia; nie są tu zaliczone do przejrzanych.
- Heurystyki oznaczyły 11 378 rekordów przynajmniej jedną flagą; pozostałych **28 539 też nie wolno uznać za przejrzane**. Nakładające się klasy: 192 `conditional_1`, 128 `conditional_2`, 2 376 `first_person`, 1 370 `second_person`, 1 927 `predicate`, 6 670 `third_or_detached`, 586 `pronoun`. To nie liczba błędów. 618 rekordów nosi ślad poprzedniej automatycznej edycji.
- Kolejka celowo ustawia wszystkim 39 917 status `unreviewed`, również już indywidualnie poprawionym niżej: to zachowawczy punkt startu, nie liczba rzeczywistych nierozpatrzonych kwestii. Nie ma jeszcze kompletnego rejestru decyzji dla każdego rekordu.
- W tym etapie ręcznie poprawiono 11 rekordów, poniżej. Dodatkowo w poprzednim etapie poprawiono cztery, w tym zgłoszoną przez właściciela Hannah → Mox. **Pełnego audytu jeszcze nie wykonano.**

## Poprawki tego etapu

| ID (końcówka) | Uzasadnienie | Zmiana |
|---|---|---|
| `1e453d51ecdd12c719e8` | Madalyn o sobie | puścił → puściła |
| `989a5b730672c05374b5` | Mox o sobie | przesunęła → przesunął |
| `b548da6db98c6e1482b3` | Duncan o sobie | zrobiła → zrobił |
| `805322718946b90a0c26` | Ella o sobie | przekonał → przekonała |
| `a74a05017f8faa31c858` | Erica o sobie | budował → budowała |
| `44e2f920fc02d2107b08` | Mox o sobie | nosiła → nosił |
| `b51aa795298dc2e34fb5` | Mox o sobie | trafiła → trafił |
| `6111effb5c551baea025` | Mox o sobie | zobaczyła → zobaczył |
| `831f21f7534cd4f71410` | Mox o sobie | pocałowała → pocałował |
| `00f7684301aab72ed57d` | Melissa o sobie | porozmawiał → porozmawiała |
| `6be01627eba58ff91c0e` | Mox zwraca się do Elli; jej następna kwestia: „Zaraz dojdę!” | doszedł → doszła |

## Odtwarzanie kolejki i dalsze prace

```
python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo_gender_inventory.jsonl
python3 -m unittest discover -s games/the-genesis-order/tests -q
```

Skrypt waliduje scalenie draftów z kanonicznym eksportem, nie zmienia tłumaczeń i nie nadpisuje wyniku. Pełna kolejka JSONL (~32 MB) zawiera ID, źródło, tekst PL, kontekst, flagi i status; grupuje według lokatora sceny i kolejności poleceń. Nie jest śledzona w Git, bo można ją odtworzyć. Kontekst i sąsiedztwo to wskazówki, nie dowód wspólnej gałęzi czy adresata. Korzystać z epizodów Czytanki, oryginalnego tekstu i `branch_path`; nie rozstrzygać mówcy ani adresata samą liczbą występujących postaci. Każdą decyzję utrwalić ze stabilnym ID, wersją tekstu i uzasadnieniem; niepewne odłożyć do runtime QA. Audyt musi objąć także rekordy bez flag, natywne dialogi, wybory, UI oraz 618 poprzednich edycji; następnie osobno zweryfikować odwracalny patch i Czytankę.

Po zmianach patch ma SHA-256 `17b913d4d9763056c6f6c95ac8a871262c659fb34429f0c70439162d8e3b490c`; Czytanka `ee5f0bee4253cb452420aad3aa1ecc2d8f1317a9c7abc003ca9c72ce0389a5d2`. Czytankę zmieniono punktowo i przepakowano bez plików gry. 152 testy przeszły w sandboxie. Nowych paczek nie testowano w grze ani nie opublikowano na Drive.

## Kolejna partia — Jon i Erica oraz przegląd kontekstowy

Właściciel wskazał kwestię Jona po „O co, do cholery, chodzi?” Erici. W CE306 Jon mówi do Erici, co potwierdza również „Masz tydzień, Eriko”: `b293c6c1c4ecf9a593a2` „będziesz mi winien” → „będziesz mi winna”. W dalszym przeglądzie poprawiono także: `0724f59b187952bcfe79` (Mox → Andrea: zabiła), `6107621dcc1a42c5b14b` (Brian → Nellie: kręciła), `e7ecd71c8b880a6f51c3` (Brian → Lillian: cofnęła), `da85a14ff34c9b0573b3` (Mox → Kimberly: winna), `c9cf57b12f673e7b22c6` (Brian o sobie: winien), `318d6be44e989ae84fce` (Chloe o sobie: winna) i `004b101d7150c5bf5af8` (Nellie o sobie: winna).

Powstał trwały rejestr `translation/reports/gender_review_decisions.jsonl`: **8 poprawionych, 21 potwierdzonych w zakresie badanej formy, 3 odłożone**, łącznie 32 decyzje. Pozostałe 39 885 rekordów mają w kolejce status `unreviewed`; w tym są także wcześniejsze poprawki, których nie przeniesiono do rejestru. Odłożone nie są zatwierdzone. Każda decyzja ma ID, uzasadnienie i fingerprint ID, źródła, tłumaczenia oraz kontekstu; zmiana tych pól oznacza `stale`. Fingerprint **nie obejmuje sąsiednich kwestii**, więc po ich zmianie rozstrzygnięcie też wymaga ręcznego ponownego sprawdzenia. Potwierdzenie dotyczy rozpatrywanego rodzaju, nie całkowitej poprawności zdania. Dodano również flagę `winien_winna` (34 rekordy); to kandydaci, nie liczba błędów.

Aktualny patch SHA-256 `03ecb5b767f6b87f42dc9edc1a07461fa8f558effebb72fbfae126b8b846a080`, Czytanka `47a4aec5ffc80b5003a3cd7c6aa087f1d2a2b5a98debc3d2c0aae1f51e7a657e`, nadpisują wcześniejsze hashe powyżej. Patch i Czytanka zaktualizowane w Git, nie w Drive; 154 testy OK w sandboxie. Testy nie dowodzą działania nowego ZIP-a w grze. **Pełen audyt nadal nieukończony.**

## Kontynuacja — weryfikacja poprzednich automatycznych poprawek

W tej partii przejrzano 77 uprzednio zmienionych kwestii dotyczących adresata i potwierdzono badane formy z uzasadnieniem w rejestrze. Znaleziono i ręcznie poprawiono kolejne **7** błędów (w tym trzy w kwestiach poprzednio edytowanych automatycznie):

- `bff363d1ef4587740825`: Larry → Mox „Znalazłaś” → „Znalazłeś”.
- `0c61171540385c7b127a`: Mox → Melissa „Nie byłaś tak daleki” → „daleka”.
- `b475e41cafd81b039306`: Mox → Melissa „Sam mówiłaś” → „Sama mówiłaś”.
- `57c9fd33f3b925191a82`: Erica o sobie „będę bogaty” → „bogata”.
- `80f1339b592193226eb3`: Mox o sobie „Sama niewiele wiem” → „Sam”.
- `a69f5a23d51d2a760972`: Carol o Moxie i Chloe „podziwiałyście” → „podziwialiście”.
- `6e980340b70fea0bc53a`: Chloe o sobie „Powinienem był wiedzieć” → „Powinnam była wiedzieć”.

Rejestr: 116 decyzji, w tym **98 potwierdzonych**, **15 poprawionych**, **3 odłożone**; 39 801 rekordów nie ma decyzji. Z 618 rekordów wcześniejszej automatycznej korekty 78 ma status potwierdzony, 4 poprawiony, 1 odłożony, a 535 nadal nieprzejrzany w rejestrze. Liczby rejestru nadal nie obejmują pierwszych 15 punktowych poprawek dokonanych przed jego utworzeniem. Każde potwierdzenie dotyczy określonej formy, nie całego zdania.

Patch SHA-256 `31acc39b0bacd18ee8474c97059790ea446b28e5292d401b4f41512003839a12`; Czytanka `f9d3f7766b281559b26bf5e033a14f9f199ef05c8fd221a964c556f0ab878706`. Poprzednie hashe w niniejszym dokumencie są historyczne. 154 testy OK; aktualne paczki nie były testowane w grze ani publikowane na Drive. Przegląd jest kontynuowany, **nie jest ukończony**.

## Kontynuacja — opętanie i faktyczny mówca

**Istotna korekta poprzedniej decyzji:** w CE454 i CE456 nagłówek `Er` wskazuje ciało Erici, ale mówi **Daemalius**, który identyfikuje się po imieniu. W CE456 Lillian/Lilith nazywa go Daemaliusem i rozmawia z nim jak z bratem. Uprzednie założenie, że nagłówek zawsze wyznacza rodzaj mówiącego, było fałszywe. Także moja wcześniejsza poprawka `fc45bddff4fb76abcab1` na „Otworzyłam… otworzyła” była **błędna** — przywrócono formę Daemaliusa „Otworzyłem… otworzył”. W CE456 poprawiono jego pierwszą osobę oraz drugą osobę adresowaną do Lilith w ciele Lillian. Rozpoznawanie podmiotu po samym nagłówku nie wystarcza; w scenach opętania sprawdzać dialog i rzeczywistą tożsamość. Stare narzędzie `fix_grammatical_gender.py` ma teraz zablokowane `--apply`, ponieważ hurtowy zapis grozi ponownym wprowadzeniem błędów.

W tej partii naniesiono **16** zmian w rekordach (w tym częściową poprawkę `b85b3157f8693c481d1c`, gdzie adresatka nadal niepewna i status to `deferred`), zbadano 90 innych form i odłożono jeden kolejny przypadek z nieznaną płcią funkcjonariusza. Pełne przed/po i uzasadnienia są w `translation/reports/gender_review_decisions.jsonl`. W szczególności poprawki opętania: `fc45bddff4fb76abcab1`, `bc0a7c67383dd0bbc1c4`, `0637a5f45ab867cdf577`, `8f439e4428239d8b2619`, `17cd9e74af03bf68be65`, `4efea59625145e305e3f`; poza opętaniem m.in. Daemalius „idiotkę” → „idiotę”, Mox o sobie „zaangażowana” → „zaangażowany”.

Stan rejestru 223: **188 confirmed, 30 corrected, 5 deferred**; 39 694 bez decyzji. Z 618 wcześniejszych automatycznych zmian: 168 confirmed, 9 corrected, 3 deferred, 438 bez decyzji. Rejestr potwierdza wyłącznie rozpatrzone formy, a inne kwestie i wcześniejsze poprawki mogą zawierać błędy. Patch SHA-256 `92205536cb7083b5e9bc3d1f6fa73e502bf64047adc8f948d847662c93987e02`, Czytanka `a61176febb3619be399bc19711cf0fe9ca07c5cc5521a096fe294f8afc8cd674`; wcześniejsze hashe są historyczne. 155 testów OK w sandboxie; nie testowano nowej paczki w grze ani nie publikowano na Drive. Audyt nie jest ukończony.

## Kontynuacja — kolejna partia poprzednich zmian

Potwierdzono 38 kolejnych form pierwszej osoby we wcześniej automatycznie edytowanych kwestiach. Poprawiono cztery rekordy: `cf4117322af096480ff1` (Erica → Mox „powiedziałaś” → „powiedziałeś”), `d598afd8b9e319055625` (Mox o grupie z nim samym „wszystkie” → „wszyscy”), `6f17daf4a48c9e3eb989` (Diana o sobie „byłam skłonny” → „byłam skłonna”) i `2ac50544bcb806cb9383` (Hannah → Mox „miałaś” → „miałeś”). Szczegóły w rejestrze decyzji.

Stan 265 decyzji: 226 confirmed, 34 corrected, 5 deferred; 39 652 bez decyzji. Patch SHA-256 `85cd1f7b8ea384b36a004ca25ee396ea0127b1b320727721d6da31ddd6f7190b`, Czytanka `655d95ec01d86a537845407cc62e28ec43e8aa8e511a32e6c021a4803f36392e`. Wcześniejsze hashe są historyczne. 155 testów OK w sandboxie, bez testu nowej paczki w grze lub publikacji na Drive. Audyt nieukończony.
