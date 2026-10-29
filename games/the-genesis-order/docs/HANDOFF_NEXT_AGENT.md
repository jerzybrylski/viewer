# Handoff dla kolejnego agenta — The Genesis Order

Stan: 2026-10-29. Statyczny eksport jest zweryfikowany, a na prośbę właściciela utworzono źródłowy ZIP v1. Nie ma jeszcze tłumaczenia ani patcha gry.

## Stan repo i artefaktów

- Pracuj tylko na `arena/df0bbe3f-viewer` (PR #1 jest otwarty); nie zmieniaj gałęzi.
- Commit `b2118af` zawierał poprzedni zweryfikowany eksport i dokumentację. Pakiet/nowy builder opisane w tej aktualizacji są dalszą pracą na tej samej gałęzi.
- Kanoniczny eksport Git: `games/the-genesis-order/translation/export-v1/`, **45 229 rekordów**, 25 JSONL + manifest; wszystkie coverage checks przechodzą.
- Source ZIP: `google_drive/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; SHA-256 zapisany w sąsiednim `.sha256`. ZIP integrity sprawdzony; zawiera 531 pozycji: kanoniczne JSONL, 497 kontekstowych dokumentów Markdown, instrukcję, manifest, glossary/politykę i raport zakresu. **Nie zawiera oryginalnych assetów ani kodu gry.** ZIP pozostaje poza Gitem.
- Walidacja bieżącej pracy: pełne `unittest` 27/27; Markdown import-check: 45 229 rekordów, 0 brakujących ID; `build_translation_package.py` utworzył i zweryfikował 531-entry ZIP. Wcześniejszy `apply_translation.py --check` przeszedł dla 45 229 rekordów / 238 źródeł; przy ponowieniu w tej sesji nie można go odtworzyć, bo ignorowane `google_drive/the-genesis-order/data/CommonEvents.json` nie jest obecne.
- Nie uruchamiano gry ani kodu gry. Pola tłumaczenia są puste.

## Pokrycie — istotne liczby

- JS: 78 plików, 563 kandydatury = 35 potwierdzonych UI, 528 wykluczeń z jawnym powodem, 0 nierozstrzygniętych.
- CE60: 38 638; CE222: 705; telefon: 30; CE223: 649; CE224: 134 statyczne captions.
- 2 110 opcji wyboru / 695 grup: 180 znanych UI, 1 930 pozostawiono bez zgadywania semantycznego podtypu.
- 1 513 nie-rendererowych `401`: 1 122 bez semantycznego podtypu, reszta to jawne UI/telefon. Wszystkie są w pakiecie jako widoczne powierzchnie tekstu.
- Vary: 262 wartości statyczne; 128 cen/markerów chronionych plus 3 etykiety Lovense chronione, 134 wartości tłumaczalne. 132 wartości whitespace-only pominięto.
- 34 pola `Items.note` zawierają wyłącznie tagi/metadane. 1 570 plugin commands to sterowanie/parametry; nie wykryto pominiętego, bezpośredniego statycznego tekstu UI w tych poleceniach.

## Otwarte zadania

### 1. Podtypy semantyczne — nie blokują już źródłowego ZIP-a

- [ ] Zdecydować, czy przed przekazaniem tłumaczowi dodatkowo podzielić 1 122 wiersze `401` i 1 930 opcji na dialog/tutorial/powiadomienie/UI. W source ZIP są zachowane, lecz bez zgadywania podtypu.
- [ ] Jeśli klasyfikacja jest wymagana, przejrzeć kontekst i treść, przypisać statusy z poziomem pewności; nie zmieniać/usuwać rekordów.
- [ ] Rozstrzygnąć, czy rozszerzać zakres o tekst w mediach i dynamiczne dane z urządzeń/użytkowników. Obecny pakiet jasno wyłącza te źródła.

### 2. Przygotowanie tłumaczenia

- [ ] Potwierdzić build gry, język źródłowy i polskie konwencje nazewnicze/terminologiczne. Źródłowy language/build nie są formalnie potwierdzone.
- [ ] Uzupełnić glosariusz i finalną politykę tłumaczenia na podstawie decyzji właściciela.
- [ ] Tłumaczyć wyłącznie po stabilnym `id`; nie zmieniać locatorów, source hashes, `source_text` ani tokenów.
- [ ] Zachować wszystkie 131 rekordów `keep_source_value` dokładnie; importer Markdown/JSONL odrzuca zmiany.

### 3. QA zwrotki i patcher Windows

- [ ] Po tłumaczeniu uruchomić Markdown import-check i `apply_translation.py --check`; rozliczyć brakujące ID, duplikaty, tokeny i konflikty.
- [ ] Ustalić docelowy build/layout, checksumy, backup/rollback, zapis atomowy oraz wpływ na save'y/osiągnięcia.
- [ ] Testować patcher najpierw na kopiach syntetycznych; test runtime/Windows wymaga kopii i zgody właściciela.
- [ ] ZIP patcha/finalnej polskiej dystrybucji jest osobną bramką — source ZIP z tego handoffu nie jest patchem.

## Odtworzenie artefaktów

Do przebudowy samego Markdown/ZIP wystarczy kanoniczny eksport Git. Ponowny eksport z assetów wymaga lokalnych oryginałów w ignorowanym `google_drive/the-genesis-order/`.

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/markdown_translation.py import --check
python3 games/the-genesis-order/tools/build_translation_package.py
```

Nie dodawać do Git żadnej ścieżki `google_drive/` ani ZIP-a. Nie kopiować tekstów SRW do TGO.
