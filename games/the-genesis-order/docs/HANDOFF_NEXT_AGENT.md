# Handoff — The Genesis Order PL

## Najważniejsze na następną sesję — 2026-10-30

**Zadanie:** kontynuować pełny kontekstowy audyt rodzaju w tłumaczeniu The Genesis Order, następnie ręcznie poprawiać jednoznaczne błędy. Audyt **nie jest ukończony**. Właściciel chce podejścia systemowego, ale odrzucił szeroką listę 14 tys. sygnałów jako kolejkę pierwszego wyboru; oczekuje kilkuset konkretniej uzasadnionych kandydatów. Ograniczona kolejka nie zastępuje przeglądu pozostałych kwestii. Tłumaczenie i korekty wykonuje LLM w kontekście sceny; słownikowe, regułowe i statystyczne MT są zabronione.

**Stan po commicie `9cbc502`:** w ostatniej partii poprawiono 25 rekordów (w tym jedna sąsiednia kwestia do Melissy). Rejestr `translation/reports/gender_review_decisions.jsonl` zawiera 226 `confirmed`, 59 `corrected`, 5 `deferred`; 39 627 przetłumaczonych rekordów pozostaje bez decyzji. `confirmed` dotyczy badanej formy, nie całego tekstu. `deferred` nie oznacza poprawności. W ostatnim pomiarze wąskie sito wskazało 102 hipotezy, nie potwierdzone błędy. Na dawnym, niereprezentatywnym zbiorze 34 tekstów `before` wskazało 19; próbka obejmuje także cofniętą błędną korektę, nie jest miarą rzeczywistej czułości. Pełne testy: 168 OK. Patch i Czytanka są zsynchronizowane; **nowych wersji nie testowano w grze ani nie publikowano na Drive**.

**Ostrożność:** nagłówek to wskazówka o ciele, nie pewna tożsamość. W common eventach 454 i 456 w ciele Erici mówi Daemalius; wcześniejsza zmiana `fc45bddff4fb76abcab1` na żeńską była błędna i została cofnięta. Adresat wywnioskowany z sąsiednich kwestii oraz zgodna gałąź również nie są dowodem. Czytać źródło, pełną scenę i warunki; niepewne przypadki odkładać. Nigdy nie stosować hurtowej korekty: `fix_grammatical_gender.py --apply` jest celowo zablokowane. Wyniki i liczby w dalszych sekcjach są historyczne i mogły zostać zastąpione; nie traktować starych twierdzeń o „zerze błędów” i automatycznym wyznaczaniu mówcy jako aktualnych.

**Następne kroki:**
1. Przeczytać `AGENTS.md` repozytorium i gry, końcowe sekcje `docs/GENDER_AUDIT_2026-10-30.md`, `docs/GENDER_SYSTEM_REVIEW.md` i wpisy decyzji. Zachować istniejące ID, źródło, kontekst i tokeny.
2. Wygenerować świeży inwentarz i kolejkę; pliki wyjściowe nie mogą już istnieć:
   ```bash
   python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo-inventory-next.jsonl
   python3 games/the-genesis-order/tools/focus_gender_candidates.py --input /tmp/tgo-inventory-next.jsonl --output /tmp/tgo-focus-next.jsonl
   ```
   ID sąsiadów z kolejki odszukać w inwentarzu, a gdy trzeba korzystać z pełnej sceny i `reading/v1/episodes/`. Szeroka kolejka `prepare_gender_review_batches.py` nadal jest dostępna i obejmuje teraz także `powinienem/powinnam`; nie używać starych offsetów z innego snapshotu.
3. Po indywidualnym przeglądzie zapisać decyzje z uzasadnieniem i fingerprintem. Fingerprint nie obejmuje sąsiadów: zmiana sąsiedniej kwestii wymaga ponownej oceny. Zmiany treści ograniczyć do zleconych korekt rodzaju, zsynchronizować drafty i Czytankę, przebudować patch oraz sidecary i manifest; nie modyfikować kanonicznego eksportu ani uruchamiać kodu gry.
4. Uruchomić `python3 -m unittest discover -s games/the-genesis-order/tests -q`, sprawdzić spójność archiwów, zanotować wyniki i ograniczenia. Kontynuować także wcześniejsze 618 zmian automatycznych, drugą i trzecią osobę oraz rekordy bez sygnału.

**Artefakty:** patch `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, SHA-256 `731605d4048f96c9d46bc3fae640b65c97237402af2fc299837ae8b182816538`; Czytanka `translation/packages/TGO_readalong_PL_v1.zip`, SHA-256 `4b3183d56ac1216727f41ed8795090c5313c3cc6b91adbfa856f770a5e2f3ba2`. Bieżąca gałąź `arena/9b9f33dc-viewer`, draft PR https://github.com/jerzybrylski/viewer/pull/8. Nie zmieniać gałęzi.

---

## Wcześniejsze wpisy — zapis historyczny

Stan: 2026-10-30. Statyczne tłumaczenie wszystkich kwalifikujących się rekordów oraz oba wskazane milestone’y są zbudowane. Patch **działa w grze** (POTWIERDZONE przez właściciela 2026-10-29 i ponownie 2026-10-30 na bieżącej paczce: polskie znaki, opcje PL, poprawne zawijanie). To nadal proof of concept w zakresie QA treści: nie ma pełnego przejścia gry, testu save/load ani weryfikacji na innych buildach. Nie uruchamiać kodu gry ani nie nadpisywać instalacji użytkownika.

> **Najpierw przeczytaj [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).** Praca poprzedniego agenta nie była w Git i została odzyskana z patcha i ZIP-ów; tam jest metoda, hashe i dowody spójności. Nie powtarzaj odzyskiwania.

## Stan i liczby

- Kanoniczny eksport `translation/export-v1/`: **45 229** rekordów; pozostaje źródłem i nie jest modyfikowany przez merge.
- Wszystkie **427** partii draftów scalają się bez konfliktów: **39 917** niepustych tłumaczeń, **131** jawnie chronionych wartości, **5 181** zachowane rekordy nielokalizowalne, **0** nierozstrzygniętych tłumaczalnych rekordów.
- Pełne testy: `python3 -m unittest discover -s games/the-genesis-order/tests -q` — **148/148 OK**.
- Scalenie draftów odtwarza bajt w bajt `payload/translations.jsonl` z patcha POC (SHA-256 `8c926724c35413b6b3ab4a5cfbda5c06b4332ed03be7e5d20f47c9adfd7c0722`) — nic nie istnieje tylko w ZIP-ie.
- Tekst wtopiony w obrazy/wideo pozostaje poza zakresem. Zachowuj stabilne ID, source, kontekst, tokeny i `keep_source_value`; tłumaczenia słownikowe/statystyczne są zabronione — stosuj kontekst sceny i ADR projektu.

## Rodzaj gramatyczny (2026-10-30)

Właściciel zgłosił z gry, że „tłumaczenie nie trzyma rodzajów”: Judy mówi o sobie po męsku, bohater mówi o niej po męsku. To był skutek metody — drafty powstawały bez wiedzy o mówcy. `tools/fix_grammatical_gender.py` ustawia rodzaj i jest już **wykonany na korpusie**: **618 rekordów / 679 form / 229 plików** (536 form 1. osoby z czasownikami, 21 „bym”, 116 form 2. osoby, 5 „byś”, 1 „sam/sama”); drugi przebieg daje 0 zmian. Stan: **0** kwestii kobiecych z męską pierwszą osobą i **0** męskich z żeńską.

Zasady, których nie wolno „poprawiać” w drugą stronę: pierwsza osoba bierze płeć mówcy z `custom_header`; druga osoba — płeć adresata, ale tylko przy jednoznacznej obsadzie sceny; narrator i mówca nieznany nie są adresatami; trzecia osoba nie jest ruszana automatycznie (coreferencja). Reszta jest w `translation/reports/gender_fix_v1.json` → `residual` i w [`GENDER_AUDIT.md`](GENDER_AUDIT.md): 169 kwestii bez mówcy z 1. osobą, 2 122 z 2. osobą bez dowodu adresata w zdaniu, 192 „sam/sama”, 50 zdań z 3. osobą do przeglądu. To materiał do QA w grze, nie do automatycznej zmiany.

## Weryfikacja po sesji (2026-10-30, wpis (4) w dzienniku)

- **Liczby są przeliczone, nie przepisane:** 427 partii, **39 917** tłumaczeń, **131** chronionych, **5 181** zachowanych w źródle, **0** konfliktów. Różnica wobec starszych dokumentów (39 926 / 5 172) to **9 rekordów** z decyzji R-01/R-07/R-08, które wróciły do źródła. Nie „poprawiaj” tego z powrotem.
- **Testy: 148/148 OK.** Wcześniejsze wpisy w `EXPERIMENT_LOG.md` podają 124/124, 144/144, a jeden (sekcja „(2)”) 147/147 — ten ostatni opisywał stan, którego nie ma w repo; jest tam jawna korekta.
- **Naprawione zabezpieczenie `iść`:** `tools/fix_grammatical_gender.py` ma teraz `ist_compound_stem()` z zamkniętą listą przedrostków (`weszłam ↔ wszedłem`, `zeszłam ↔ zszedłem`, `odeszłam ↔ odszedłem`, `podeszłam ↔ podszedłem`, `przyszłam ↔ przyszedłem`…). Wyraz na `-szłam`, który nie jest złożeniem „iść” (np. `usłyszłam`), jest **zostawiany bez zmian** — nie zgadujemy.
- **Artefakty bez zmian:** kontrola narzędzia daje 0 zmian w korpusie, więc patch `e647f76e…`, Czytanka `ea11cdeb…`, manifest i sidecary pozostają aktualne; nie przebudowywano ich i nie publikowano ponownie.

## Gotowe artefakty

1. **Standalone patch POC:** `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, SHA-256 `e647f76efdc72d90e4b137020702dcda9d91eee08f311e392a8c04899abb1ae0`. Manifest i fingerprinty 238 plików źródłowych są też w repo jako `translation/reports/patch_manifest_v0.1.1.json` i `translation/reports/source_fingerprints_v0.1.1.json` — to jedyna kopia, której nie da się odtworzyć bez oryginałów gry, więc nie usuwaj jej. Zawiera 39 917 tłumaczeń, fingerprinty 238 źródeł, backup/restore i one-click patcher; nie zawiera plików gry. Patcher nie wymaga podawania ścieżki: `APPLY.bat`/`COFNIJ.bat` uruchamiają `patcher.py` bez argumentów, a `patcher/locator.py` pamięta ostatnią instalację, przeszukuje biblioteki Steam i typowe foldery gier, przy kilku trafieniach pokazuje listę, a w ostateczności otwiera okno wyboru folderu. ZIP/CRC i testy syntetyczne przechodzą. **Nie testowano Windows ani gry.**
2. **Czytanka PL v1:** katalog `reading/v1/`, standalone ZIP `translation/packages/TGO_readalong_PL_v1.zip`, SHA-256 `ea11cdeb56f014e970a7d871cd01fb28f595f4610012ed06be21c5ca834c3085`. Zawiera pełny skrypt, **4 394** osobne epizody i `reading_order.tsv` (4 134 map/event/page + 260 Common Events), a także indeks 55 mówców i 291 lokacji. Uwzględnia statycznie rozpoznanych mówców, warunki, rozgałęzienia, wybory i jawne placeholders dla danych dynamicznych. Mówcy niepewni są oznaczeni, nigdy zgadywani.
3. **Ograniczenie chronologii:** BFS od mapy startowej 38 znajduje potencjalne ścieżki do **221/291** map, bez ewaluacji warunków/przełączników/runtime. Common Events sortowane są według pierwszego statycznego wywołania. README Czytanki ostrzega, że kolejność jest przybliżona, a nie kanoniczna; sceny opcjonalne mogą być poza kolejnością pojedynczego przejścia.

## Publikacja na Google Drive

Folder `TGO/translation/packages/` (`1FYzfQsDJKBaI_GBjlA8qhtS9I9h5_5KM`): patch `1I_IAEk7lqvXTlBbWWiHKIJJHbA12VF6L` (MD5 `f334eb89…`) + sidecar `1t3ppvwrEAy5pzP7TyO7sfwaUCpIqNfdg`, Czytanka `1eUuZTR2LM1ZJtmYkUpQPecI4iwKjr_mv` (MD5 `939a1646…`) + sidecar `1gE35EpQ8eGtz94oElvNXjYDpFjN3fHO_`. MD5 na Drive zgadzają się z plikami w Git; poprzednie wydania są w koszu. Przy każdej przebudowie paczek **podmień też sidecar** — stary `.sha256` obok nowego ZIP-a jest gorszy niż brak pliku.

## Źródła / odtwarzanie

Statyczne źródła gry są w ignorowanym `google_drive/tgo_source/`; drafty i canonical export są śledzone w repo. Nie zmieniaj `export-v1/` i nie zapisuj merge nad draftami. Patcher i Czytankę odtwarzaj do pustych ścieżek (narzędzia celowo odmawiają nadpisywania):

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/audit_translation_coverage.py
python3 games/the-genesis-order/tools/audit_draft_coverage.py --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md
python3 games/the-genesis-order/tools/build_standalone_patch.py
python3 games/the-genesis-order/tools/build_readalong.py
```

Szczegółowy zakres i ograniczenia: `STATUS.md`, `ROADMAP_TRANSLATION.md`, `COUNT_REPORT.md` i `TRANSLATION_POLICY.md`.

## Następne zadania (w tej kolejności)

> **Wszystkie decyzje redakcyjne są zamknięte** (R-01…R-11 w [`EDITORIAL_DECISIONS.md`](EDITORIAL_DECISIONS.md)). Właściciel uznał pozostałe uwagi redakcyjne za nieistotne i **nie chce już zmian w treści korpusu**; jedyny dopuszczony wyjątek (rodzaj gramatyczny) został wykonany 2026-10-30. Nie zaczynaj kolejnej redakcji korpusu bez jego wyraźnego polecenia.

1. **QA treści w grze** — pełne przejście z patchem, test save/load, najdłuższe kwestie w wąskich okienkach UI, wybory i komunikaty błędów. To jedyny otwarty zakres jakości; raportuj właścicielowi konkretne zdania zamiast zmieniać je „na wyczucie”.
2. **Zgłoszenia właściciela po grze** — każdą poprawkę dostarczaj jako nowy batch draftów pod stabilnym `id`, potem przebuduj oba artefakty (niżej) i podbij hashe.
3. **28 rekordów `needs_review`** — 24 opcje wyboru z samym imieniem z `\\c[n]\\v[n]` oraz 4 wartości telefonu/natywne (`Madalyn.`, `Morgan #142`, `Morgan.`, `Amulet K.`). Zostają w źródle; tłumaczyć tylko na wyraźne polecenie, nie hurtem.
4. **Przebudowa artefaktów po każdej zmianie treści:** `build_standalone_patch.py`, `build_readalong.py`, nowe `.sha256`, wpis w `EXPERIMENT_LOG.md`, testy. Kolejność i tryby offline opisane niżej.
5. **Audyt redakcyjny:** `python3 tools/audit_editorial_quality.py` (raport do `translation/reports/editorial_qa_v1.json` i `docs/EDITORIAL_QA.md`; `--fix` poprawia tylko spacje/interpunkcję). Whitelist `REVIEWED` w narzędziu zawiera trafienia sprawdzone ręcznie — dopisuj tam każdy nowy fałszywy alarm **z uzasadnieniem**, nie wyłączaj całej klasy.

## Zasady i pułapki

- ADR 001: żadnego automatycznego MT poza LLM w kontekście sceny; każdy builder ma ręczne tłumaczenia, filtr `known` + `keep_source_value` + `/^` + `noalpha`, `len==exact`, `validate 0`, `py_compile`, pełny zielony zestaw testów i odmowę nadpisania pliku.
- ADR 002 (**przyjęty, wariant B**): `translation_tokens_match()` normalizuje kody czcionek bez argumentu (`\fb`, `\fi`, `\fr`), gdy następuje po nich litera. **Nie twórz `export-v2`** i nie zmieniaj `export-v1/`, żeby „naprawić” tokeny.
- `translation/pending/` i `tools/markup_signature.py` **nie istnieją** — usunięte wraz z przyjęciem ADR 002. Nie odtwarzaj ich.
- Drafty czytaj **rekurencyjnie** (`rglob`); partie leżą też w `hints/`, `ui-01/` i `follow-ups/`.
- Nigdy nie uruchamiaj `.build-*.py` na istniejącym pliku wyjściowym; determinizm sprawdzaj na kopii katalogu.
- Commit i push po każdym zamkniętym etapie. Poprzedni agent stracił całą pracę przez brak pusha.

## Przebudowa obu paczek bez źródeł gry (POTWIERDZONE)

`data/` gry nie jest w repozytorium, a sandbox nie ma wyjścia sieciowego do Google, więc przebudowa wymaga dwóch jawnych
trybów offline. Oba są już zaimplementowane i przetestowane:

```bash
cd games/the-genesis-order
# 1) patch — czyta fingerprinty źródeł z export-v1 (nie potrzebuje data/)
python3 tools/build_standalone_patch.py --output /tmp/patch.zip
cp /tmp/patch.zip translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip

# 2) Czytanka — potrzebuje tylko System.json, CommonEvents.json i MapInfos.json;
#    numerację rozdziałów i indeks lokacji dziedziczy z poprzedniego wydania
python3 tools/build_readalong.py --source-root /ścieżka/do/data \
    --output /tmp/reading --zip /tmp/reading.zip \
    --previous-order reading/v1/reading_order.tsv \
    --locations-index reading/v1/index_locations_PL.md
```

Po podmianie plików w repo trzeba przeliczyć `translation/reports/coverage_audit_v1.json`
(`python3 tools/audit_translation_coverage.py`), wstawić manifest z ZIP-a do `translation/reports/patch_manifest_v0.1.1.json`
i uruchomić testy — `tests/test_patch_artifacts.py` pilnuje, żeby ZIP, sidecar, raporty i `reading/v1` nie rozjechały się z Git.

## Aktualizacja: zgłoszenie Hannah → Mox (2026-10-30)

Właściciel wskazał „Nie proszę, żebyś cokolwiek mówiła” w odpowiedzi na kwestię Moxa. Poprawiono ją i trzy inne jednoznaczne konstrukcje warunkowe; szczegóły i ID w końcowym wpisie `EXPERIMENT_LOG.md`. Wcześniejsze stwierdzenie „0 kwestii” dotyczyło wyłącznie wzorców rozpoznawanych przez skrypt, nie całego korpusu. **Audyt kontekstowy rodzajów pozostaje otwarty**. Aktualny patch SHA-256 `9697ac198428cc00606b56978dcedbe68ca239f387a4b705de88c48bb228156c`, Czytanka `13bd38c8dd15a4721ceff308b6e5a53adda9374fab5414248f568ce0ef612fc7`; supersedują starsze hashe w tym dokumencie. Nowej paczki nie testowano w grze i nie publikowano na Drive. 150 testów OK. Czytankę zaktualizowano punktowo i przepakowano, a nie odtworzono ze źródeł gry.

## Audyt rodzaju — kolejna sesja, NIEUKOŃCZONY

Właściciel zlecił pełny przegląd wszystkich rodzajów. Rozpoczęto go, poprawiając kolejnych 11 jednoznacznych błędów i tworząc odtwarzalny inwentarz 39 917 tłumaczeń. Liczby, ID, ograniczenia, polecenie i aktualne hashe: `GENDER_AUDIT_2026-10-30.md`. Kolejka oznacza wszystko jako nieprzejrzane i jest tylko początkiem: konieczne są przegląd kontekstowy i trwały rejestr decyzji, w tym poprzednich 618 automatycznych zmian oraz rekordów bez flag. Nie ogłaszać audytu skończonym. 152 testy OK; nowy patch nie testowany w grze i nie opublikowany na Drive.

### Jon → Erica i rejestr decyzji

Poprawiono zgłoszone „będziesz mi winien” na „winna” oraz siedem dalszych błędów. Trwały rejestr `translation/reports/gender_review_decisions.jsonl`: 8 `corrected`, 21 `confirmed`, 3 `deferred`; dalsze 39 885 rekordów nie mają decyzji w rejestrze. Szczegóły, ograniczenia fingerprintów, aktualne hashe i następne kroki w `GENDER_AUDIT_2026-10-30.md`. Kolejkę odtwarza `tools/inventory_gender_review.py`; dane z innych scen/gałęzi nie mogą być dowodem adresata bez analizy. Kontynuować, nie deklarować pełnego audytu. 154 testy OK, nowego ZIP-a nie sprawdzono w grze ani na Drive.

### Kontynuacja audytu kontekstowego

Poprawiono siedem kolejnych błędów i zapisano 77 potwierdzonych rozstrzygnięć kontekstowych; szczegóły i aktualne hashe w końcowej sekcji `GENDER_AUDIT_2026-10-30.md`. Rejestr: 98 confirmed, 15 corrected, 3 deferred, 39 801 bez decyzji; spośród 618 dawnych automatycznych zmian 535 pozostaje bez decyzji i jedna odłożona. Odtwarzać kolejkę z `inventory_gender_review.py`, weryfikować sceny i odrębnie mówcę/adresata, aktualizować rejestr i testy. Audyt nie jest skończony; paczki nie zostały potwierdzone w grze ani opublikowane na Drive.

### Krytyczne: opętanie i nagłówki

CE454 i CE456: `Er` to ciało Erici, faktycznie mówi Daemalius; zastosowano męską pierwszą osobę i żeńską drugą wobec Lilith. Wcześniejsza ręczna korekta `fc45bddff4fb76abcab1` na żeńską była błędna i została cofnięta. Nie określać tożsamości automatycznie z nagłówka. `fix_grammatical_gender.py --apply` zablokowano, aby zapobiec ponownemu uszkodzeniu. Pełny kontekst, ID i aktualne hashe na końcu `GENDER_AUDIT_2026-10-30.md`. Rejestr 188 confirmed, 30 corrected, 5 deferred, 39 694 unreviewed. Testy 155 OK; nowy ZIP nie jest sprawdzony w grze ani opublikowany na Drive. Kontynuować audyt; nie ogłaszać ukończenia.

### Dalszy przegląd

38 kolejnych dawnych form pierwszej osoby potwierdzono, cztery rekordy poprawiono; rejestr liczy 226 confirmed, 34 corrected, 5 deferred, 39 652 bez decyzji. Aktualne hashe i ID są w końcowej sekcji `GENDER_AUDIT_2026-10-30.md`. 155 testów OK, patch nie jest testowany w grze ani publikowany na Drive. Kontynuować przegląd scen oraz poprzednich zmian; nie utożsamiać nagłówka ciała z rzeczywistą tożsamością w opętaniu.

### Systemowa kolejka partii

Na prośbę właściciela dodano `tools/prepare_gender_review_batches.py`, który z odtwarzalnego inwentarza tworzy priorytetyzowane grupy identycznych źródeł/przekładów z indywidualnymi ID, sąsiedztwem i warunkami. Polecenia, wyniki i ważne ograniczenia (w tym brak automatycznej walidacji hasha sąsiedztwa i brak dowodu kompletności) w `GENDER_SYSTEM_REVIEW.md`. Na obecnym stanie 14 178 rekordów ma sygnały, 25 479 bez sygnału nadal wymagają przeglądu; nie są to liczniki błędów. Kontynuować partiami, decyzje i tłumaczenia rozstrzygać w kontekście, nie stosować automatycznych zamian. Korpus ani ZIP-y nie zmienione; 163 testy OK. Audyt nieukończony.

### Aktualizacja: wąskie sito rodzaju (2026-10-30)
Użytkownik oczekiwał kilkuset konkretniej uzasadnionych kandydatów zamiast 14 178 szerokich sygnałów. `tools/focus_gender_candidates.py` daje 126 hipotez bez limitu i bez zmian tekstu, ale ma jawne fałszywe alarmy i tylko 19/34 w niereprezentatywnym teście historycznym. Szczegóły, komendy i ograniczenia w `docs/GENDER_SYSTEM_REVIEW.md`. Najpierw czytać scenę i weryfikować mówcę, gałąź oraz adresata; wąska kolejka nie zastępuje pełnego audytu ani szerszej kolejki. Brak nowych korekt korpusu lub przebudowy paczek w tej zmianie.

### Aktualizacja: przegląd wąskiej kolejki (2026-10-30)
Poprawiono kontekstowo 25 rekordów (24 z kolejki + jedna sąsiednia kwestia do Melissy). ID, wcześniejsze formy i kontekst w rejestrze decyzji; pełne omówienie i hashe w `GENDER_AUDIT_2026-10-30.md`. W rejestrze 226 confirmed, 59 corrected, 5 deferred; 39 627 bez decyzji. Wąskie sito na nowym inwentarzu: 102 hipotezy, bez gwarancji ani pełnego pokrycia. W szerokim sicie dodano sygnał `powinienem/powinnam`, więc należy wygenerować nowy inwentarz i kolejki. Patch i Czytanka zsynchronizowane, 168 testów OK; testu w grze i publikacji Drive nie było. Kontynuować kontekstową weryfikację, w tym sceny opętania i rekordy bez sygnału.
