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

## Kontynuacja — przegląd wybranych „powinienem / powinnam”

Po sprawdzeniu źródła i sąsiednich kwestii poprawiono **25 rekordów**, w tym dwie pary powtórzeń z osobnymi ID i warunkami stron. Przykłady: Mox mówi „Powinienem ostrzec ojca Solomona”, Arianna „Powinnam była zażądać remontu”, Carol „nie powinnam była pozwolić”, a Brian „Powinienem był wiedzieć”. W rozmowie z Judy zmieniono też „zostawić cię samego” na „samą”; w sąsiedniej scenie Mox mówi do Melissy „jakbyś chciała wkurzyć Andreę”. Wszystkie zmiany przed/po, ID i uzasadnienia są w rejestrze decyzji. Nie rozstrzygano pozostałych kandydatów hurtowo.

Wąskie sito po zmianie zwraca 102 hipotezy (74 adresat, 8 pierwsza osoba, 11 orzecznik, 9 `sam/sama`), a nie potwierdzone błędy. Szerokie sito uzupełniono o flagę `powinienem/powinnam`, której wcześniej brakowało; historyczne wyniki liczbowe szerokiej kolejki w poprzednim rozdziale dotyczą poprzedniej wersji. W rejestrze: 226 confirmed, 59 corrected, 5 deferred, a 39 627 rekordów bez decyzji; potwierdzenie jest ograniczone do rozpatrywanej formy. Kolejka jest niepełna i audyt nadal trwa.

Patch SHA-256 `731605d4048f96c9d46bc3fae640b65c97237402af2fc299837ae8b182816538`, Czytanka `4b3183d56ac1216727f41ed8795090c5313c3cc6b91adbfa856f770a5e2f3ba2`. Patch i Czytanka są zsynchronizowane z draftami; 168 testów OK. Nie uruchamiano gry ani nie publikowano nowych paczek na Drive.

## Kontynuacja — przegląd całej wąskiej kolejki (102 hipotezy)

Tym razem przeglądnięto **wszystkie 102 hipotezy** wąskiego sita (`focus_gender_candidates.py`) na świeżym inwentarzu z commita `9cbc502`, czytając każdą scenę w całości — nie tylko sąsiednie kwestie. Do tego celu dodano narzędzie tylko do odczytu `tools/show_gender_scene.py` (inwentarz → scena w kolejności poleceń, nagłówek, mapa mówcy, EN i PL; zero zapisów, pilnuje tego `tests/test_show_gender_scene.py`). Rezultat: **70 korekt, 31 potwierdzeń i 1 odłożenie** — plus **jedna korekta sąsiedniej kwestii** w tej samej scenie (map 33, event 48, strona 8).

### Co się okazało

- **Fałszywe alarmy bywają liczne, ale nie dominują:** 31 z 102 hipotez było poprawnych. Najczęstsze przyczyny: „Sam/Sama” odnosiło się do adresata, do rzeczy (pająk, penis), do rzeczownika w utartym wyrażeniu („otwarta księga”, „ciepły bałwan”) albo do trzeciej osoby (Andrea/Nellie), a nie do mówcy.
- **Opętanie nadal myli heurystykę:** w CE456 „Byłeś wybrańcem” i w CE454 „Skąd się wziąłeś?” są poprawne, bo mówi Daemalius w ciele Erici; hipoteza wskazywała Ericę jako adresatkę. Bez czytania sceny te dwie kwestie zostałaby „naprawione” w złą stronę.
- **Nagłówek ≠ adresat:** 51 korekt dotyczy drugiej osoby, gdzie adresatem okazywał się mężczyzna, gdy hipoteza wskazywała kobietę (lub odwrotnie) — rozstrzygały dopiero następne kwestie tej samej wymiany (odpowiedź z formą osobową, wołacz, imię).
- **Powtórzone identyczne źródła mają osobne decyzje:** dwa razy „Dobrze, że zwracałeś uwagę” (CE492 i EV110), dwa razy „Myślałem, że wiedziałaś…” (EV027, strony 5 i 6), trzy razy ta sama kwestia Elli w trzech różnych scenach (map 190 / EV009, map 192 / EV004, map 193 / EV004 — po jednym ID na scenę). Każde wystąpienie dostało własny wpis w rejestrze.
- **Jedno odłożenie:** `eb528be8f3a7a510c15d` (Kimberly w studiu) — wypowiedź dotyczy Melissy albo obojga rozmówców („Ustalcie wspólną wersję”), a „Rozbiłeś Gildię” może odnosić się do Moxa; sąsiedztwo nie rozstrzyga adresata ani liczby, więc tekst zostaje bez zmian.
- **Poza kolejką, przy okazji czytania sceny:** `d6d8d21aa612f12c74a5` („Czemu jesteś taka naburmuszona?” Dawida do Moxa) → „taki naburmuszony”. To jedyna zmiana spoza 102 hipotez i jest zapisana w rejestrze z uzasadnieniem.

### Rozkład 71 zmian

| Klasa formy | Liczba |
|---|---:|
| druga osoba (adresat) | 51 |
| orzecznik przymiotnikowy (`pewien/pewna`, `gotowy/gotowa`, `dobra/dobry`, `zła/zły`, `godny/godna`, `dorosłaś/dorosłeś`) | 9 |
| `powinienem / powinnam` | 8 |
| `sam / sama` | 3 |

Zmiany objęły **49 plików draftów**, bez ruszania ID, źródła, kontekstu i tokenów. Pełne `before`, fingerprint i uzasadnienie każdej decyzji są w `translation/reports/gender_review_decisions.jsonl`.

### Stan rejestru i kolejek

- Rejestr: **393 decyzje** — 257 `confirmed`, 130 `corrected`, 6 `deferred`; **39 524** przetłumaczone rekordy bez decyzji. `confirmed` nadal dotyczy wyłącznie rozpatrzonej formy, nie całego zdania, i nie unieważnia sąsiedztwa (fingerprint nie obejmuje sąsiadów).
- Z 618 rekordów wcześniejszej automatycznej korekty: 206 `confirmed`, 13 `corrected`, 3 `deferred`, **396** nadal bez decyzji.
- Wąskie sito po zmianach zwraca **1 hipotezę** — to właśnie odłożona kwestia Kimberly, a nie „zero błędów”. Puste sito nie jest dowodem kompletności: obejmuje tylko wybrane wzorce.
- Szerokie sito: 39 530 rekordów kwalifikujących się do przeglądu, 14 158 z sygnałem w 13 280 grupach, **25 372 bez sygnału** nadal wymagają przeglądu.

### Artefakty i testy

Patch przebudowany ze scalenia draftów: `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, SHA-256 `9f71e99aaaeea93d3cea15c08d96c739e47da7e2074367095e6dd7de3a37c943` (39 917 tłumaczeń, 238 fingerprintów, 427 partii). Czytanka zmieniona punktowo — 62 epizody, 71 kwestii w skrypcie — i przepakowana z zachowaniem listy wpisów: `translation/packages/TGO_readalong_PL_v1.zip`, SHA-256 `8504ac12e1cea42084ab62bbfcd07e38b8b5fb139b6b5478ff2c5ea31267b565`. Manifest i sidecary zaktualizowane.

**173 testy OK** (`python3 -m unittest discover -s games/the-genesis-order/tests -q`), w tym nowe testy podglądu sceny. Paczek **nie testowano w grze** ani nie publikowano na Drive. **Audyt pozostaje nieukończony** — nieprzejrzane są tysiące rekordów bez sygnału, 396 wcześniejszych automatycznych zmian i cała druga/trzecia osoba poza wąskim sitem.

## Kontynuacja — trzy rodziny sygnałów (362 hipotezy, 0 korekt)

Po wyczerpaniu wąskiego sita sprawdzono trzy kolejne, wąskie rodziny sygnałów z szerokiej kolejki — już nie przez `focus_gender_candidates.py`, lecz przez bezpośredni wybór rekordów po nazwie sygnału i weryfikację liniową (kwestia + mapowanie mówcy, scena tylko przy wątpliwościach):

| Sygnał | Hipotezy | Potwierdzone | Odłożone | Korekty |
|---|---:|---:|---:|---:|
| `winien_winna_podmiot_do_ustalenia` | 43 | 43 | 0 | 0 |
| `rozdzielny_tryb_pierwszej_osoby` | 181 | 175 | 6 | 0 |
| `powinienem_powinnam_podmiot_do_ustalenia` | 138 | 137 | 1 | 0 |
| **razem** | **362** | **355** | **7** | **0** |

### Wnioski

- **Te trzy heurystyki są niemal czyste.** Po 102 hipotezach wąskiego sita (70 korekt) można było oczekiwać dalszych błędów, tymczasem wszystkie 362 sprawdzone formy były zgodne z płcią mówcy lub adresata. `winien/winna` i `powinienem/powinnam` nie wymagają już dalszego przeglądu pojedynczo — wystarczy je zostawić jako sygnał kontrolny.
- **`rozdzielny_tryb_pierwszej_osoby` łapie formę po `bym/żebym/gdybym`, więc prawie zawsze trafia w poprawną pierwszą osobę** („Chciałabym”, „żebym mogła”, „gdybym wiedziała”). Sygnał myli się tylko wtedy, gdy podmiotem jest ktoś inny niż mówca — w tej partii się to nie zdarzyło.
- **Odłożenia dotyczą wyłącznie postaci bez mapowanej płci:** sześć kwestii systemowego NPC-a z CE25 (sklep/poradniki) i jedna „Ochrona”. Angielski jest tu neutralny, a scena nie daje podstaw; forma męska zostaje jako redakcyjna domyślna, ale bez wpisu `confirmed`.
- **Reszta błędu siedzi gdzie indziej.** Największe masy to `inna_forma_rodzajowa` (9 699), `mozliwy_przymiotnik_lub_rzeczownik` (4 248) i `orzecznik_do_przegladu` (1 865) oraz **28 409 rekordów bez żadnego sygnału** — dopiero tam trzeba szukać dalszych niezgodności.

### Stan po tej partii

- Rejestr: **755 decyzji** — 611 `confirmed`, 130 `corrected`, 14 `deferred`; **39 162** przetłumaczone rekordy bez decyzji.
- Z 618 wcześniejszych automatycznych zmian: bez decyzji pozostaje **396** (ta partia ich nie dotyczyła).
- Tekst tłumaczeń w tej partii **nie zmienił się**, więc patch (`9f71e99a…`) i Czytanka (`8504ac12…`) pozostają te same — nie było potrzeby przebudowy paczek.
- `confirmed` nadal znaczy „rozpatrzona forma jest poprawna”, a nie „całe zdanie jest bezbłędne”. Audyt pozostaje **nieukończony**.

## Kontynuacja — `rozdzielny_tryb_adresata` (94 hipotezy, 3 korekty)

Ostatnia niesprawdzona rodzina wąskich sygnałów: forma po `byś/żebyś/gdybyś`, czyli druga osoba. Inaczej niż przy pierwszej osobie, tu trzeba ustalić **adresata**, więc każdą kwestię porównano z odpowiedzią w tej samej wymianie (a w trzech przypadkach z całą sceną).

| Wynik | Liczba |
|---|---:|
| `confirmed` | 91 |
| `corrected` | 2 |
| `deferred` | 1 |

**Korekty:**

- `e09c348f912ef4a2eed3` (CE457, Andrea): „Chcę, żebyś **wyprał** mi mózg seksem!” → „**wyprała**”. Adresatką jest Demon 3 — mówi o sobie po żeńsku („Powinnam zlasować ci mózg”, „moje siostry”) i odpowiada na tę kwestię w następnej linii.
- `603bf710b817cd67ac81` (map 183 / event Nellie, Lillian): „…a ciało Erici będzie twoje, byś je **strzegł**” → „**strzegła**”. Adresatką jest Arianna, która w kolejnej kwestii prosi: „Najpierw oddaj mi ciało Erici”.

**Korekta spoza sygnału, znaleziona przy czytaniu tej samej sceny:** `ef785d1b24497be208b8` (map 183, Lillian) — „Jesteś **ślepy**” → „Jesteś **ślepa**”, bo Arianna mówi „Jesteś szalona”, a Lillian odpowiada jej wprost.

**Odłożenie:** `b01c024477b41be0102e` (map 183, Lillian) — „Nigdy byś jej nie znalazł”. Z wymiany nie da się ustalić, czy Lillian mówi do Moxa, Nellie czy Elli; obie formy są równie prawdopodobne, więc tekst zostaje bez zmian.

### Wniosek — pierwsza i druga osoba to nie to samo

Sąsiedni sygnał pierwszej osoby (181 hipotez) nie dał ani jednej korekty, a adresacki — 3 na 94. Powód jest strukturalny: forma po `bym` prawie zawsze dotyczy mówcy, więc heurystyka jest czysta; forma po `byś` zależy od adresata, a tego nagłówek nie koduje. **Rodziny „adresackie” trzeba nadal czytać scenami, rodzin „mówcowych” nie.**

### Stan po tej partii

- Rejestr: **850 decyzji** — 702 `confirmed`, 133 `corrected`, 15 `deferred`; **39 067** rekordów bez decyzji.
- Patch: `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, SHA-256 `a89bf8b4cbe54a57ae9ada195c57c1a5db5ec085a8d5485b3ef62410cf2f3fad` (3 748 011 B, 39 917 tłumaczeń, 238 fingerprintów, 427 partii); payload `3a0f9999…`.
- Czytanka: 2 epizody i 3 wystąpienia w skrypcie zaktualizowane, przepakowana bez zmiany listy 4 399 wpisów — SHA-256 `c0f436017091dba5bac1d196ecc7909aca4893633a1e631452a54b3961ec8b35`.
- **173 testy OK**. Paczek nie testowano w grze ani nie publikowano na Drive. Audyt pozostaje **nieukończony**.

## Kontynuacja — wcześniejsze auto-zmiany i luka „opcji dialogowych”

### 1. Przegląd wcześniejszych automatycznych zmian (384 bez decyzji)

Zamiast czytać 384 kwestie od zera wykorzystano `change_log` z `translation/reports/gender_fix_v1.json`, który dla każdej z 618 dawnych zmian zapisuje `before`, `after`, mówcę, płeć i podstawę adresata. Dzięki temu przegląd dotyczy samej zmiany, a nie całej linii.

- **399 z 414 edycji to pierwsza osoba** (`1os_czasownik` 337, `1os_orzecznik` 60, `1os_warunkowy` 2). W tej grupie nie ma ani jednej sceny opętania (sprawdzono nazwy eventów), a narzędzie zawsze dopasowywało formę do płci mówcy z mapowania — więc ryzyko jest tu małe z definicji, a nie z lektury.
- **15 edycji drugiej osoby** opierało się na słabej przesłance „jednolita płeć pozostałych mówców sceny”. Wszystkie 15 pochodzi z EV027 (map 31, przesłuchanie w sklepie XXX). Sprawdzone w scenie: Mox pyta Alię, więc formy żeńskie („robiłaś”, „przyjechałaś”) są poprawne. Zarejestrowane jako `confirmed`.
- Pozostałe 369 pierwszosobowych zmian **pozostaje bez decyzji** — nie udajemy przeglądu, którego nie było; ich ryzyko jest ograniczone do błędnego mapowania mówcy.

### 2. Opcje dialogowe — kategoria poza wszystkimi sygnałami

Przy okazji sprawdzania EV027 wyszło, że **`choice_option` (1 416 rekordów) nie jest objęte żadnym sygnałem**: heurystyki patrzą na kwestie mówione, a opcje gracza nie mają nagłówka mówcy. Dlatego zdanie „Co robiłeś tuż przed przyjściem tutaj?” wciąż stało w scenie, w której Mox przesłuchuje wyłącznie Alię, podczas gdy odpowiadająca mu kwestia mówiona była już poprawiona na „robiłaś”.

Sprawdzono wszystkie 48 opcji w tej stronie eventu (mówcy: wyłącznie Mox i Alia) i poprawiono **18 rekordów** — wszystkie formy drugiej osoby żeńskiej: `byłeś → byłaś`, `przyjechałeś → przyjechałaś`, `robiłeś → robiłaś`, `rzucałeś → rzucałaś`, `jadłeś → jadłaś`. Pełna lista ID jest w rejestrze decyzji; basis każdego wpisu odsyła do sceny map 31 / EV027.

Kontrola po zmianie: w całym korpusie **żadna opcja dialogowa nie zawiera już formy drugiej osoby** (0 z 1 416). Opcje nie mają rodzaju gramatycznego w innych miejscach, więc ta kategoria jest wyczerpana.

### Stan po tej partii

- Rejestr: **883 decyzje** — 717 `confirmed`, 151 `corrected`, 15 `deferred`; **39 034** rekordy bez decyzji.
- Patch: SHA-256 `dcf81b8ea7b1b981e7068f2c1b5d6eaea0a2d8a73d966fc25d6bfd3cfb943087`; payload `f984bd55…`.
- Czytanka: epizod `1710_map031_event027_page01.md` i sekcja „Mapa 031 — Sklep XXX / event 27” w skrypcie; przepakowana bez zmiany listy 4 399 wpisów — SHA-256 `a80ae034b0ec3e608c2a91b302f8d73b67d5e0b5f7fd0912a4dac5c6d863bdf9`.
- **173 testy OK**. Paczek nie testowano w grze. Audyt pozostaje **nieukończony**.
