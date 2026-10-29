# Roadmap — lokalizacja The Genesis Order

**Cel:** przygotować bezpieczny pipeline od zweryfikowanych źródeł RPG Maker MV, przez tłumaczenie z kontekstem, po lokalny patcher Windows. Tekstów SRW nie kopiujemy do TGO; przenoszone są wyłącznie ogólne praktyki: stabilne ID, JSONL, walidacja placeholderów, branch-aware Markdown i staging bez nadpisywania oryginału.

**Aktualny gate:** statyczne skanowanie, kuratela i eksport są zakończone. Na prośbę właściciela przygotowano i sprawdzono source ZIP v1 w ignorowanym `google_drive/`. Wszystkie rekordy z nierozstrzygniętym podtypem są dołączone i oznaczone, bez zgadywania. Nie ma jeszcze tłumaczenia ani patcha gry.

## Kanoniczny przepływ

```text
oryginalne assety (lokalnie/google_drive, ignorowane)
  → statyczne skanery i jawne decyzje
  → games/the-genesis-order/translation/export-v1 (JSONL, Git)
  → Markdown context + source ZIP (regenerowalne, prywatne)
  → tłumaczenie po ID → walidacja JSONL
  → staging kopii gry → testy właściciela na Windows
```

Repozytorium zawiera narzędzia, dokumentację, testy i jawnie zatwierdzone teksty JSON. Oryginalne `www/data/`, `www/js/`, fonty, media, archiwum wejściowe, ZIP źródłowy i przetłumaczone stagingi pozostają poza Gitem.

## Bramki i stan

| Etap | Rezultat | Stan |
|---|---|---|
| 1. Inwentaryzacja | 305 JSON + Credits, 291 map, 500 Common Events; hierarchia 78 JS; hashe i statyczny skan; bez uruchamiania gry/kodu | **Zakończone** |
| 2. Audyt tekstowych powierzchni | wiadomości, opcje, skrypty/pluginy, wartości zmiennych, CE53/54/60/222/223/224, note fields, dynamiczne wartości i media | **Zakończone dla znanych statycznych źródeł**; niezgadywane podtypy i wyłączenia jawnie opisane |
| 3. Kanoniczny eksport | JSONL ze stabilnym ID, hashami, locatorami, kontekstem i tokenami | **45 229 rekordów; wszystkie kontrole pokrycia przeszły** |
| 4. Round-trip | walidator i safe write-back do kopii; testy syntetyczne | **Gotowe statycznie**; `--check` weryfikuje 45 229 rekordów / 238 źródeł |
| 5. Kontekst/pakiet źródłowy | JSONL, instrukcje, glossary/polityka, raport, manifest i Markdown źródłowy | **ZIP v1 wygenerowany i sprawdzony**: 45 229 rekordów / 497 dokumentów; pozostaje prywatny w ignorowanym `google_drive/` |
| 6. Rozpoczęcie tłumaczenia | zatwierdzone zasady językowe, glosariusz, partie i kontrola terminologii | **Nie rozpoczęto**; tłumaczenia puste |
| 7. Import tłumaczenia | walidacja ID, tokenów, braków, nadmiarów i konfliktów | **Parser i walidator istnieją**; brak zwrotki do sprawdzenia |
| 8. Patcher Windows | wykrycie kopii/builda, backup, atomowy staging, raport/rollback, testy syntetyczne | **Nie rozpoczęto**; wymaga tłumaczenia i docelowego layoutu |
| 9. Finalny patch / polska dystrybucja | przetłumaczony tekst i instalowalny patch | **Nie istnieją**; osobna bramka po tłumaczeniu/QA |

## Audyt pokrycia — liczby kontrolne

- JSONL: 45 229 rekordów, 25 kategorii i `export_manifest.json`.
- 38 638 wpisów customowego CE60; 705 Arianna hints; 30 tekstów telefonu (17 skryptowych + 13 natywnych); 378 elementów UI telefonu; 649 etykiet przedmiotów; 134 image-caption values.
- Natywne teksty: 1 513 wierszy `401` poza rendererami. Wszystkie są zachowane jako widoczne powierzchnie tekstu; podtyp 1 122 wierszy nie jest rozstrzygnięty.
- Wybory: 2 110 opcji / 695 grup; 180 rozpoznanych jako znane UI, pozostałe 1 930 bez zgadywania semantyki.
- Statyczne wartości widoczne przez `\\V[...]`: 262 niepuste rekordy; 132 whitespace-only layout values pominięte; 128 kwot/markerów chronionych `keep_source_value`.
- JavaScript: 78 plików, 563 kandydatury; 35 UI (4 engine-static, 9 parametrów pluginów, 22 static plugin UI), 528 wykluczeń, 0 otwartych.
- 34 pola `note` w Items.json zawierają tagi/metadane bez prozy. 1 570 plugin commands to polecenia sterujące lub parametry, nie jawne teksty UI. Dynamiczne nazwy urządzeń/użytkowników są danymi runtime, nie stringami lokalizacyjnymi.
- `apply_translation.py --check`: 45 229 rekordów, hashe 238 źródeł, bez zapisu; Markdown import-check: 45 229 rekordów, brak brakujących ID; pełny zestaw unit tests wcześniej: 27/27 passed.

Source ZIP: `google_drive/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; SHA-256 w sąsiednim `.sha256`. Odtwarzanie: `python3 games/the-genesis-order/tools/build_translation_package.py`. ZIP nie zawiera oryginalnych assetów ani kodu gry.

Szczegóły i ograniczenia: [`STATUS.md`](STATUS.md), [`COUNT_REPORT.md`](COUNT_REPORT.md), [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md).

## Zasady jakości i bezpieczeństwa

1. Nie uruchamiać ani nie modyfikować kodu gry; parsery pracują statycznie.
2. Nie interpretować stringa jako UI bez konkretnego dowodu renderowania.
3. Nie nazywać wszystkich widocznych tekstów dialogiem. Zachowywać oddzielne kategorie i jawne niepewności semantyczne.
4. Stabilne ID zależą od locatora; importer nie dopasowuje po samym tekście.
5. Zachowywać formatowanie, escape’y i tokeny. Kwoty, markup i wartości będące operandami logiki mają jawne polityki ochrony.
6. Oryginał nigdy nie jest nadpisywany. Write-back tworzy nowy staging w `google_drive/`.
7. Nie kopiować źródłowych mediów, stagingu ani ZIP-a do Git. Source ZIP v1 może zawierać wyłącznie śledzony eksport i kontekst tekstowy.
8. Czytanki zachowują wszystkie warianty i warunki; nie wymyślać jednej kanonicznej kolejności scen.
