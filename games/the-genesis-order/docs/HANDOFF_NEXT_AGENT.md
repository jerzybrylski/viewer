# Handoff dla kolejnego agenta — The Genesis Order

Stan: 2026-10-29. Kanoniczny statyczny eksport i source ZIP v1 są gotowe. Odtwarzalny pomiar `tools/audit_draft_coverage.py` (wszystkie 425 plików draftów, także podkatalogi) daje **39 821** unikalnych ID z niepustym tłumaczeniem, **5 277** pustych rekordów do rozstrzygnięcia i **131** chronionych `keep_source_value` w 45 229 rekordach. Statyczna proza widoczna dla gracza jest więc w praktyce wyczerpana: 39 821 + 94 rekordy zablokowane sygnaturą markup v1 (ADR 002) = **39 915**. Aspiracja 45 000 jest nieosiągalna bez tłumaczenia tokenów sterujących, nazw własnych i komend — nie dobijaj licznika sztucznymi partiami. Pełny rozkład pustych rekordów i lista 30 pozycji czekających na decyzję właściciela: [`COVERAGE_AUDIT.md`](COVERAGE_AUDIT.md).

## Stan repo i artefaktów

- Pracuj na gałęzi bieżącej sesji Arena; nie zmieniaj gałęzi.
- Kanoniczny eksport: `games/the-genesis-order/translation/export-v1/`, 45 229 rekordów, 25 JSONL + manifest. Wszystkie wiersze `401` poza rendererami oraz wszystkie opcje `102` są zatwierdzone jako pełnoprawny tekst gracza do tłumaczenia.
- Source ZIP v1: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; ZIP i `.sha256` są śledzone w Git. Identyczny ZIP umieszczono na Google Drive w `TGO/translation/packages/`.
- ZIP obejmuje canonical JSONL, kontekstowy Markdown (497 dokumentów), instrukcję PL, manifest, glossary/politykę i raport zakresu. Nie zawiera oryginalnych assetów ani kodu gry.
- Oryginalne źródła są dostępne na Google Drive: folder `TGO/www/data/` zawiera 306 plików, w tym `CommonEvents.json`. W bieżącym workspace źródła nie są zsynchronizowane do lokalnego ignorowanego `google_drive/`; nie prosić właściciela o ponowny upload. Przy potrzebie ponownego hashowania źródeł pobrać/synchronizować je z Drive.
- Pełne `unittest` uruchomione w tej sesji: **51/51 passed**, w tym audyt pokrycia draftów, test sygnatury markup v2, odkrywanie zagnieżdżonych partii i test ostatniego fragmentu telefonu. Wcześniejszy Markdown import-check zweryfikował 45 229 rekordów i 0 brakujących ID; builder source ZIP sprawdza manifest coverage, zgodność liczby rekordów, unikalność ID i integralność archiwum.
- Nie uruchamiano gry ani kodu gry. Source ZIP i kanoniczny eksport pozostają źródłowe; partie do step11 zawierają UI, 705 wskazówek, wybory, powtarzalny dialog, 20 scen common events (1 922 wiersze), 15 Common Events ze step10 (1 014), Common Event 25 (304), 50 nowych follow-upów Common Events ze step11 (2 730), Map 20 (985), Map 31 (700), Map 3 (728), Map 24 (168), Map 23 (219), Map 116 (135) i Map 9 (101) oraz pozostałe kategorie. Pełny scalony stan: `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl` (ignorowany artefakt): 20 610 niepustych, 131 chronionych i 24 488 oczekujących; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`. Po step11 dodano dotąd **12 661 draftów w 110 plikach**. Pierwsza partia 5 004 obejmuje Map 9/23/24/116 (1 001), Map 41/55 (557), Map 44 (203), Map 82 (328), Map 54 (370), Map 6 (230), Map 26 (359) i Common Events (1 956 w 57 eventach); druga partia 5 136 obejmuje Mapy 201/15/157/16/144/13/4/21/33/141/11/76/62/49/78/30/28/125/27/32/87. Ostatnie 2 521 to cztery partie Common Events (792), Map 12 (140), Map 19 (185), Map 25 (148), Map 34 (143), Map 52 (135), Map 61 (156), Map 94 (139), Map 101 (142), Map 114 (178), Map 151 (192) i Map 203 (171); wszystkie 792 zinwentaryzowane naturalne wiersze Common Events są już opracowane. Roboczy podzbiór map ma teraz 6 549 kandydatów, ale nie wszystkie muszą być tekstem gracza. Lista plików i ID znajduje się w `translation/drafts/README.md`. Wszystkie partie są osobne i niescalone; nie traktować ich jako część licznika step11.

## Zatwierdzony zakres i liczniki

- Wszystkie **1 122** nie-rendererowe wiersze `401` są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia.
- Wszystkie **2 110** opcji `102` w **695** grupach są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia; decyzja właściciela zatwierdza pełne włączenie ich do zakresu.
- Łącznie 1 513 nie-rendererowych `401`: 1 122 wiadomości + 378 UI telefonu + 13 natywnych tekstów telefonu; osiem renderer scaffolds jest pominiętych.
- JS: 78 plików, 563 kandydatury = 35 potwierdzonych UI, 528 wykluczeń z jawnym powodem, 0 nierozstrzygniętych.
- Pozostałe główne kategorie: CE60 38 638; Arianna hints 705; CE223 649; CE224 captions 134; wartości przez `\\V[...]` 262 (z czego ceny/markery chronione); 131 chronionych rekordów `keep_source_value` łącznie.
- Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo nie jest tłumaczony. Dynamiczne dane runtime, np. nazwy urządzeń/użytkowników, nie są statycznymi stringami gry.

## Następne zadania

1. **Nie tłumaczyć już nowych partii map.** Statyczna proza jest wyczerpana; zamiast licznika uruchamiać `tools/audit_draft_coverage.py` i pracować na liście 30 pozycji z `needs_review` oraz na konfliktach etykiet.
2. **Decyzja właściciela w sprawie ADR 002** (sygnatura markup v2 dla `\fb`): po akceptacji przenieść `translation/pending/crafting-ui-map46-01.jsonl` (94 rekordy) do `drafts/` i przeliczyć pokrycie. Do tego czasu nie ruszać walidatora.
3. **Uzgodnić 40 etykiet map** (PR #5) i poprawić pozostawione po angielsku `Channel 4` w `inventory-names-02.jsonl` oraz `map-labels-01.jsonl`; potwierdzić decyzję o nazwach własnych (`Madalyn.`, `Morgan.`, `Amulet K.`, `Morgan #142`, `WoNoChurch`, `The Genesis Order`, 24 opcje postaci).
4. **Redakcja i QA** 39 821 draftów po stabilnym `id`: spójność terminologii z glosariuszem, długości linii, tokeny, powtarzalne powiedzenia; potem Markdown import-check i `apply_translation.py --check` na skompletowanym pliku.
5. **Patcher Windows** (etap 8 roadmapy): docelowy build/layout, backup, atomowy staging, raport/rollback, testy na kopiach syntetycznych; test in-game dopiero z wynikiem od właściciela.
6. ZIP patcha/finalnej polskiej dystrybucji pozostaje osobną bramką; source ZIP v1 zawiera tekst źródłowy, nie tłumaczenie.

## Odtworzenie artefaktów

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/markdown_translation.py import --check
python3 games/the-genesis-order/tools/build_translation_package.py
```

Binarne assety gry pozostają poza Git; tekstowe dane i tłumaczenia śledzić w repo. Nie kopiować tekstów SRW do TGO.
