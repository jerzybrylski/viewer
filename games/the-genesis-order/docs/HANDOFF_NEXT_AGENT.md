# Handoff — The Genesis Order PL

Stan: 2026-10-30. Statyczne tłumaczenie wszystkich kwalifikujących się rekordów oraz oba wskazane milestone’y są zbudowane. Patch **działa w grze** (POTWIERDZONE przez właściciela 2026-10-29 i ponownie 2026-10-30 na bieżącej paczce: polskie znaki, opcje PL, poprawne zawijanie). To nadal proof of concept w zakresie QA treści: nie ma pełnego przejścia gry, testu save/load ani weryfikacji na innych buildach. Nie uruchamiać kodu gry ani nie nadpisywać instalacji użytkownika.

> **Najpierw przeczytaj [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).** Praca poprzedniego agenta nie była w Git i została odzyskana z patcha i ZIP-ów; tam jest metoda, hashe i dowody spójności. Nie powtarzaj odzyskiwania.

## Stan i liczby

- Kanoniczny eksport `translation/export-v1/`: **45 229** rekordów; pozostaje źródłem i nie jest modyfikowany przez merge.
- Wszystkie **427** partii draftów scalają się bez konfliktów: **39 917** niepustych tłumaczeń, **131** jawnie chronionych wartości, **5 181** zachowane rekordy nielokalizowalne, **0** nierozstrzygniętych tłumaczalnych rekordów.
- Pełne testy: `python3 -m unittest discover -s games/the-genesis-order/tests -q` — **144/144 OK**.
- Scalenie draftów odtwarza bajt w bajt `payload/translations.jsonl` z patcha POC (SHA-256 `8c926724c35413b6b3ab4a5cfbda5c06b4332ed03be7e5d20f47c9adfd7c0722`) — nic nie istnieje tylko w ZIP-ie.
- Tekst wtopiony w obrazy/wideo pozostaje poza zakresem. Zachowuj stabilne ID, source, kontekst, tokeny i `keep_source_value`; tłumaczenia słownikowe/statystyczne są zabronione — stosuj kontekst sceny i ADR projektu.

## Rodzaj gramatyczny (2026-10-30)

Właściciel zgłosił z gry, że „tłumaczenie nie trzyma rodzajów”: Judy mówi o sobie po męsku, bohater mówi o niej po męsku. To był skutek metody — drafty powstawały bez wiedzy o mówcy. `tools/fix_grammatical_gender.py` ustawia rodzaj i jest już **wykonany na korpusie**: **618 rekordów / 679 form / 229 plików** (536 form 1. osoby z czasownikami, 21 „bym”, 116 form 2. osoby, 5 „byś”, 1 „sam/sama”); drugi przebieg daje 0 zmian. Stan: **0** kwestii kobiecych z męską pierwszą osobą i **0** męskich z żeńską.

Zasady, których nie wolno „poprawiać” w drugą stronę: pierwsza osoba bierze płeć mówcy z `custom_header`; druga osoba — płeć adresata, ale tylko przy jednoznacznej obsadzie sceny; narrator i mówca nieznany nie są adresatami; trzecia osoba nie jest ruszana automatycznie (coreferencja). Reszta jest w `translation/reports/gender_fix_v1.json` → `residual` i w [`GENDER_AUDIT.md`](GENDER_AUDIT.md): 169 kwestii bez mówcy z 1. osobą, 2 122 z 2. osobą bez dowodu adresata w zdaniu, 192 „sam/sama”, 50 zdań z 3. osobą do przeglądu. To materiał do QA w grze, nie do automatycznej zmiany.

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
