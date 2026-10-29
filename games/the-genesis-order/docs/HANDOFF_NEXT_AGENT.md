# Handoff dla kolejnego agenta — The Genesis Order

Stan: 2026-10-29. Kanoniczny statyczny eksport i source ZIP v1 są gotowe. Istnieje pierwsza robocza partia UI, ale patcha gry jeszcze nie ma.

## Stan repo i artefaktów

- Pracuj na gałęzi bieżącej sesji Arena; nie zmieniaj gałęzi.
- Kanoniczny eksport: `games/the-genesis-order/translation/export-v1/`, 45 229 rekordów, 25 JSONL + manifest. Wszystkie wiersze `401` poza rendererami oraz wszystkie opcje `102` są zatwierdzone jako pełnoprawny tekst gracza do tłumaczenia.
- Source ZIP v1: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; ZIP i `.sha256` są śledzone w Git. Identyczny ZIP umieszczono na Google Drive w `TGO/translation/packages/`.
- ZIP obejmuje canonical JSONL, kontekstowy Markdown (497 dokumentów), instrukcję PL, manifest, glossary/politykę i raport zakresu. Nie zawiera oryginalnych assetów ani kodu gry.
- Oryginalne źródła są dostępne na Google Drive: folder `TGO/www/data/` zawiera 306 plików, w tym `CommonEvents.json`. W bieżącym workspace źródła nie są zsynchronizowane do lokalnego ignorowanego `google_drive/`; nie prosić właściciela o ponowny upload. Przy potrzebie ponownego hashowania źródeł pobrać/synchronizować je z Drive.
- Pełne `unittest`: 27/27; Markdown import-check: 45 229 rekordów, 0 brakujących ID; builder source ZIP sprawdza manifest coverage, zgodność liczby rekordów, unikalność ID i integralność archiwum.
- Nie uruchamiano gry ani kodu gry. W source ZIP i kanonicznym eksporcie pola `translation` są puste; pierwsza zwrotka robocza jest osobna.

## Zatwierdzony zakres i liczniki

- Wszystkie **1 122** nie-rendererowe wiersze `401` są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia.
- Wszystkie **2 110** opcji `102` w **695** grupach są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia; decyzja właściciela zatwierdza pełne włączenie ich do zakresu.
- Łącznie 1 513 nie-rendererowych `401`: 1 122 wiadomości + 378 UI telefonu + 13 natywnych tekstów telefonu; osiem renderer scaffolds jest pominiętych.
- JS: 78 plików, 563 kandydatury = 35 potwierdzonych UI, 528 wykluczeń z jawnym powodem, 0 nierozstrzygniętych.
- Pozostałe główne kategorie: CE60 38 638; Arianna hints 705; CE223 649; CE224 captions 134; wartości przez `\\V[...]` 262 (z czego ceny/markery chronione); 131 chronionych rekordów `keep_source_value` łącznie.
- Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo nie jest tłumaczony. Dynamiczne dane runtime, np. nazwy urządzeń/użytkowników, nie są statycznymi stringami gry.

## Następne zadania

1. Kontynuować polską terminologię i tłumaczenie pełnego zatwierdzonego eksportu po stabilnym `id`. Robocza partia UI 01 (130 rekordów, 127 niepustych pól, 3 chronione puste) jest w `google_drive/the-genesis-order/translation/draft-ui-v1/` i [na Drive](https://drive.google.com/file/d/192Umg5H5xVGzoAtyMN8fDJ6HSrreO1A7/view?usp=drivesdk). Druga partia to 65 wskazówek: [Drive](https://drive.google.com/file/d/1n2r4gLCZMwkbzqpCenDJNJOF-AbKn-OM/view?usp=drivesdk). Kolejne 35 wskazówek: [Drive](https://drive.google.com/file/d/1Sd5I5LLJeRX217dSIc-cNuWVNWIcrjk-/view?usp=drivesdk). Lokalny pełny zbiór po scaleniu: `google_drive/the-genesis-order/translation/merged-ui-hints-02-2026-10-29.jsonl`, 227 niepustych, 131 chronionych i 44 871 tłumaczalnych oczekujących. Używać `tools/merge_translation_batches.py` do wykrywania konfliktów, nie nadpisywać istniejącej pracy.
2. Nie zmieniać ID, locatorów, source hashes, `source_text` ani tokenów. Zachować wszystkie rekordy `keep_source_value` dokładnie.
3. Po tłumaczeniu uruchomić Markdown import-check i `apply_translation.py --check`; rozliczyć braki, duplikaty, tokeny i konflikty.
4. Ustalić docelowy build/layout i zaprojektować patcher Windows z backupem/rollbackiem; testować najpierw na kopiach syntetycznych.
5. ZIP patcha/finalnej polskiej dystrybucji jest osobną bramką. Source ZIP v1 zawiera tekst źródłowy, nie tłumaczenie ani patch.

## Odtworzenie artefaktów

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/markdown_translation.py import --check
python3 games/the-genesis-order/tools/build_translation_package.py
```

Oryginalne assety pozostają poza Git; nie kopiować ich ani stagingu do repo. Nie kopiować tekstów SRW do TGO.
