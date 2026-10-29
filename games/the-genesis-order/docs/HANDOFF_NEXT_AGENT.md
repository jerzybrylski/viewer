# Handoff — The Genesis Order PL

Stan: 2026-10-29. Statyczne tłumaczenie wszystkich kwalifikujących się rekordów oraz oba wskazane milestone’y są zbudowane. To nadal proof of concept: gra, instalator Windows, glify/łamanie tekstu i działanie w runtime nie były testowane. Nie uruchamiać kodu gry ani nie nadpisywać instalacji użytkownika.

> **Najpierw przeczytaj [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).** Praca poprzedniego agenta nie była w Git i została odzyskana z patcha i ZIP-ów; tam jest metoda, hashe i dowody spójności. Nie powtarzaj odzyskiwania.

## Stan i liczby

- Kanoniczny eksport `translation/export-v1/`: **45 229** rekordów; pozostaje źródłem i nie jest modyfikowany przez merge.
- Wszystkie **427** partii draftów scalają się bez konfliktów: **39 917** niepustych tłumaczeń, **131** jawnie chronionych wartości, **5 181** zachowane rekordy nielokalizowalne, **0** nierozstrzygniętych tłumaczalnych rekordów.
- Pełne testy: `python3 -m unittest discover -s games/the-genesis-order/tests -q` — **88/88 OK**.
- Scalenie draftów odtwarza bajt w bajt `payload/translations.jsonl` z patcha POC (SHA-256 `d90191df69ca4194b6d59071ce6a4a40a3dfa5ac52c5a5b20f5ff9b726a44458`) — nic nie istnieje tylko w ZIP-ie.
- Tekst wtopiony w obrazy/wideo pozostaje poza zakresem. Zachowuj stabilne ID, source, kontekst, tokeny i `keep_source_value`; tłumaczenia słownikowe/statystyczne są zabronione — stosuj kontekst sceny i ADR projektu.

## Gotowe artefakty

1. **Standalone patch POC:** `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, SHA-256 `f60a2ff512e397ffa1d730bc0d48a5949fbc2541ef7516e9302998cd8d512277`. Manifest i fingerprinty 238 plików źródłowych są też w repo jako `translation/reports/patch_manifest_v0.1.1.json` i `translation/reports/source_fingerprints_v0.1.1.json` — to jedyna kopia, której nie da się odtworzyć bez oryginałów gry, więc nie usuwaj jej. Zawiera 39 917 tłumaczeń, fingerprinty 238 źródeł, backup/restore i one-click patcher; nie zawiera plików gry. Patcher nie wymaga podawania ścieżki: `APPLY.bat`/`COFNIJ.bat` uruchamiają `patcher.py` bez argumentów, a `patcher/locator.py` pamięta ostatnią instalację, przeszukuje biblioteki Steam i typowe foldery gier, przy kilku trafieniach pokazuje listę, a w ostateczności otwiera okno wyboru folderu. ZIP/CRC i testy syntetyczne przechodzą. **Nie testowano Windows ani gry.**
2. **Czytanka PL v1:** katalog `reading/v1/`, standalone ZIP `translation/packages/TGO_readalong_PL_v1.zip`, SHA-256 `74a3b096a07e92de32f6b5ac42e9f297cf4a33adf2db21fdd92359f60ec04c4f`. Zawiera pełny skrypt, **4 394** osobne epizody i `reading_order.tsv` (4 134 map/event/page + 260 Common Events), a także indeks 55 mówców i 291 lokacji. Uwzględnia statycznie rozpoznanych mówców, warunki, rozgałęzienia, wybory i jawne placeholders dla danych dynamicznych. Mówcy niepewni są oznaczeni, nigdy zgadywani.
3. **Ograniczenie chronologii:** BFS od mapy startowej 38 znajduje potencjalne ścieżki do **221/291** map, bez ewaluacji warunków/przełączników/runtime. Common Events sortowane są według pierwszego statycznego wywołania. README Czytanki ostrzega, że kolejność jest przybliżona, a nie kanoniczna; sceny opcjonalne mogą być poza kolejnością pojedynczego przejścia.

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

1. **Decyzje redakcyjne właściciela** — [`EDITORIAL_DECISIONS.md`](EDITORIAL_DECISIONS.md), 11 pozycji z rekomendacjami. Najpilniejsze: tytuł gry („Zakon Genesis” vs oryginał), `Channel 4`, `TEXT`/`TEKST` (możliwy klucz w kodzie gry), placeholdery TEST MAP.
2. **Redakcja językowa 39 917 draftów** po stabilnym `id`: spójność z glosariuszem, długości linii, powtarzalne powiedzenia. **Największy konkretny dług: odmiana imion** — imiona na `-a` są odmienione tylko w 21–50% wystąpień (Erica 140/318, Andrea 108/294, Ella 88/263), więc w korpusie obok siebie stoją „sypialni Andrei” i „z Andrea”. Tabela i decyzja: R-09 w `EDITORIAL_DECISIONS.md`. Audyt wskazuje też 617 tłumaczeń identycznych ze źródłem — po odfiltrowaniu imion i wykrzyknień zostaje 37 wielowyrazowych, wszystkie to nazwy własne, pseudonimy i linki.
3. **28 rekordów w kubełku `needs_review`** — 24 opcje wyboru, które są samym imieniem z `\c[n]\v[n]`, oraz 4 wartości telefonu/natywne: `Madalyn.`, `Morgan #142`, `Morgan.`, `Amulet K.` ([`COVERAGE_AUDIT.md`](COVERAGE_AUDIT.md)). Przejrzeć pojedynczo i zdecydować, czy zostają w źródle, nie tłumaczyć hurtem.
4. **Przebudowa artefaktów po redakcji:** `build_standalone_patch.py`, `build_readalong.py` (ok. 9 s przy dostępnych źródłach), aktualizacja `.sha256` i wpis w `EXPERIMENT_LOG.md`.
5. **Testy patchera na kopii wspieranego builda Windows:** sprawdzić backup/restore, placeholdery, glify, UI i niezmienność oryginału. Nie publikować POC jako zatwierdzonego spolszczenia przed tym QA.

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
