# Handoff dla kolejnego agenta — The Genesis Order

Stan: 2026-10-29. Kanoniczny statyczny eksport i source ZIP v1 są gotowe. Pełny audyt wszystkich 424 plików draftów scalił i zweryfikował 45 229 rekordów kanonicznych: **39 820 niepustych tłumaczeń po ID**, **131 rekordów chronionych** i **5 278 pustych niechronionych pól**. Poprzednia projekcja 39 931 zawyżała wynik o 111 wskutek powtórzonych ID. Uzgodniono 40 rozbieżnych etykiet map w starszym `inventory-names-01.jsonl` według nowszego `inventory-names-02.jsonl`; obecnie nie ma konfliktów między niepustymi wariantami. Z 5 278 pustych pól 3 742 to rozpoznane slash-prefixed kontrolne stringi; pozostaje najwyżej **1 536 kandydatów** do ręcznej oceny, niekoniecznie tekstów do tłumaczenia. Partie nadal wymagają redakcji; patcha gry jeszcze nie ma.

## Stan repo i artefaktów

- Pracuj na gałęzi bieżącej sesji Arena; nie zmieniaj gałęzi.
- Kanoniczny eksport: `games/the-genesis-order/translation/export-v1/`, 45 229 rekordów, 25 JSONL + manifest. Wszystkie wiersze `401` poza rendererami oraz wszystkie opcje `102` są zatwierdzone jako pełnoprawny tekst gracza do tłumaczenia.
- Source ZIP v1: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; ZIP i `.sha256` są śledzone w Git. Identyczny ZIP umieszczono na Google Drive w `TGO/translation/packages/`.
- ZIP obejmuje canonical JSONL, kontekstowy Markdown (497 dokumentów), instrukcję PL, manifest, glossary/politykę i raport zakresu. Nie zawiera oryginalnych assetów ani kodu gry.
- Oryginalne źródła są dostępne na Google Drive: folder `TGO/www/data/` zawiera 306 plików, w tym `CommonEvents.json`. W bieżącym workspace źródła nie są zsynchronizowane do lokalnego ignorowanego `google_drive/`; nie prosić właściciela o ponowny upload. Przy potrzebie ponownego hashowania źródeł pobrać/synchronizować je z Drive.
- Pełne `unittest` uruchomione w tej sesji: **37/37 passed**, w tym test najnowszych piętnastu partii dialogowych. Wcześniejszy Markdown import-check zweryfikował 45 229 rekordów i 0 brakujących ID; builder source ZIP sprawdza manifest coverage, zgodność liczby rekordów, unikalność ID i integralność archiwum.
- Nie uruchamiano gry ani kodu gry. Source ZIP i kanoniczny eksport pozostają źródłowe. Pełny scalony stan zweryfikowano ponownie ze wszystkich śledzonych draftów, bez zapisywania eksportu ani patcha: 39 820 niepustych tłumaczeń, 131 chronionych i 5 278 pustych niechronionych. Skład i szczegółowe liczniki partii opisuje `translation/drafts/README.md`; historyczne liczniki przyrostów nie zastępują pełnego, deduplikowanego scalenia. Wcześniejsza lista roboczych kandydatów naturalnych dialogów map jest wyczerpana; pozostałe puste pola należy ocenić kategoriami, zamiast liczyć je jako potwierdzone dialogi.

## Zatwierdzony zakres i liczniki

- Wszystkie **1 122** nie-rendererowe wiersze `401` są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia.
- Wszystkie **2 110** opcji `102` w **695** grupach są pełnoprawnym tekstem widocznym dla gracza i do tłumaczenia; decyzja właściciela zatwierdza pełne włączenie ich do zakresu.
- Łącznie 1 513 nie-rendererowych `401`: 1 122 wiadomości + 378 UI telefonu + 13 natywnych tekstów telefonu; osiem renderer scaffolds jest pominiętych.
- JS: 78 plików, 563 kandydatury = 35 potwierdzonych UI, 528 wykluczeń z jawnym powodem, 0 nierozstrzygniętych.
- Pozostałe główne kategorie: CE60 38 638; Arianna hints 705; CE223 649; CE224 captions 134; wartości przez `\\V[...]` 262 (z czego ceny/markery chronione); 131 chronionych rekordów `keep_source_value` łącznie.
- Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo nie jest tłumaczony. Dynamiczne dane runtime, np. nazwy urządzeń/użytkowników, nie są statycznymi stringami gry.

## Następne zadania

1. Po pełnym scaleniu pozostało 1 536 pustych pól poza 3 742 potwierdzonymi komendami slash i 131 chronionymi wartościami; jest to wyłącznie górna liczba kandydatów, nie gwarantowana liczba tłumaczalnych tekstów. Potwierdzono co najmniej 94 puste, widoczne wiersze UI craftingu na Map 46 (po 47 wystąpień pytań „Craft this item?” i „You have items missing from this recipe.”). Sklasyfikować pozostałe kandydaty po kategorii i widoczności, a tłumaczyć tylko potwierdzony tekst gracza, kontekstowo przez LLM. Wszystkie partie i ich statusy są opisane w `translation/drafts/README.md`. `inventory-names-02` jest aktualnym wariantem nazw i zawiera map labels; nie dodawać osobno `map-labels-01`. Przed kolejnym scaleniem uruchomić `tools/merge_translation_batches.py` na wszystkich partiach — test integracyjny sprawdza już brak konfliktów.
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

Binarne assety gry pozostają poza Git; tekstowe dane i tłumaczenia śledzić w repo. Nie kopiować tekstów SRW do TGO.
