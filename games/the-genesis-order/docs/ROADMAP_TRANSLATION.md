# Roadmap — lokalizacja The Genesis Order

**Cel:** przygotować bezpieczny pipeline od zweryfikowanych źródeł RPG Maker MV, przez tłumaczenie z kontekstem, po lokalny patcher Windows. Tekstów SRW nie kopiujemy do TGO; przenoszone są wyłącznie ogólne praktyki: stabilne ID, JSONL, walidacja placeholderów, branch-aware Markdown i staging bez nadpisywania oryginału.

**Aktualny gate:** statyczne skanowanie, kuratela i eksport są zakończone. Wszystkie znane, statyczne kanały tekstowe są w kanonicznym JSONL. ZIP jest wstrzymany do przeglądu użytkownika nad aktualnym manifestem pokrycia; nie ma jeszcze tłumaczeń ani patcha.

## Kanoniczny przepływ

```text
oryginalne assety (lokalnie/google_drive, ignorowane)
  → statyczne skanery i jawne decyzje
  → games/the-genesis-order/translation/export-v1 (JSONL, Git)
  → Markdown-draft / Czytanki (regenerowalne, prywatne)
  → tłumaczenie po ID → walidacja JSONL
  → staging kopii gry → testy właściciela na Windows
```

Repozytorium zawiera narzędzia, dokumentację, testy i jawnie zatwierdzone teksty JSON. Oryginalne `www/data/`, `www/js/`, fonty, media, archiwum wejściowe i przetłumaczone stagingi pozostają poza Gitem.

## Bramki i stan

| Etap | Rezultat | Stan |
|---|---|---|
| 1. Inwentaryzacja | 305 JSON + Credits, 291 map, 500 Common Events; pełna hierarchia 78 JS; hashe i statyczny skan; żadnego uruchomienia gry/kodu | **Zakończone** |
| 2. Audyt tekstowych powierzchni | wiadomości, opcje, skrypty/pluginy, wartości zmiennych, CE53/54/60/222/223/224, note fields, dynamiczne wartości oraz tekst w mediach | **Zakończone dla znanych, statycznych źródeł**; semantycznego podtypu części wiadomości/wyborów nie zgadujemy, a media/runtime zewnętrzny pozostają jasno opisane |
| 3. Kanoniczny eksport | JSONL ze stabilnym ID, hashami, locatorami, kontekstem i tokenami; kompletne liczniki | **45 229 rekordów; wszystkie kontrole pokrycia przeszły** |
| 4. Round-trip | walidator oraz safe write-back do kopii, bez zapisu do wejść; testy syntetyczne wszystkich mechanizmów | **Gotowe statycznie**; `--check` zweryfikował 45 229 rekordów / 238 źródeł |
| 5. Kontekst dla tłumacza | Markdown według źródeł z warunkami/gałęziami, stabilnym ID i polem tłumaczenia | **Szkic wygenerowany**: 497 dokumentów / 45 229 rekordów w ignorowanym `google_drive/`; nie jest kanoniczną chronologią ani ZIP-em |
| 6. Rozpoczęcie tłumaczenia | zatwierdzone zasady językowe, glosariusz, partie pracy i kontrola terminologii | **Nie rozpoczęto**; tłumaczenia są puste |
| 7. Import tłumaczenia | Markdown/JSONL → walidacja ID, tokenów, braków, nadmiarów i konfliktów | **Parser i walidator istnieją**; brak rzeczywistej zwrotki do sprawdzenia |
| 8. Patcher Windows | wykrycie kopii/builda, backup, atomowy staging, raport/cofnięcie, testy syntetyczne | **Nie rozpoczęto**; wymaga zaakceptowanej zwrotki i layoutu użytkownika |
| 9. Finalne Czytanki / ZIP | branch-aware Czytanki i paczka tłumacza | **Nie przygotowywać ZIP-a przed akceptacją pokrycia i zamknięciem wymagań** |

## Audyt pokrycia — liczby kontrolne

- JSONL: 45 229 rekordów, 25 plików JSONL i `export_manifest.json`.
- 38 638 wpisów customowego CE60; 705 Arianna hints; 30 tekstów telefonu (17 skryptowych + 13 natywnych); 378 elementów UI telefonu; 649 etykiet przedmiotów; 134 image-caption values.
- Natywne teksty: 1 513 wierszy `401` poza 8 scaffoldingowymi rendererami. Wszystkie włączone rekordy są powierzchniami widocznego tekstu; podtyp 1 122 wiadomości nie jest rozstrzygnięty.
- Wybory: 2 110 opcji / 695 grup; 180 rozpoznanych jako znane UI, pozostałe 1 930 bez zgadywania semantyki.
- Statyczne wartości widoczne przez `\\V[...]`: 262 niepuste rekordy; 132 whitespace-only layout values pominięte; 128 kwot/markerów zablokowanych `keep_source_value`.
- JavaScript: 78 plików, 563 kandydatury; 35 UI (4 engine-static, 9 parametrów pluginów, 22 static plugin UI), 528 wykluczeń, 0 otwartych.
- 34 pola `note` w Items.json zawierają tagi/metadane bez prozy. 1 570 plugin commands to polecenia sterujące lub parametry, nie jawne teksty UI. Dynamiczne nazwy urządzeń/użytkowników są danymi runtime, nie stringami lokalizacyjnymi.
- `apply_translation.py --check`: 45 229 rekordów, hashe 238 źródeł, bez zapisu; Markdown import-check: 45 229 rekordów, brak brakujących ID; pełny zestaw `unittest`: 27/27 passed.

Szczegóły i ograniczenia w [`STATUS.md`](STATUS.md), [`COUNT_REPORT.md`](COUNT_REPORT.md) i [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md). Wcześniejsze wykluczenia nie były „technicznymi wiadomościami”: obejmowały wartości kodu/konfiguracji bez dowodu widocznego UI w badanym locatorze.

## Zasady jakości i bezpieczeństwa

1. Nie uruchamiać ani nie modyfikować kodu gry; parsery pracują statycznie.
2. Nie interpretować stringa jako UI bez konkretnego dowodu renderowania.
3. Nie nazywać wszystkich widocznych tekstów dialogiem. Zachowywać oddzielne kategorie i jawne niepewności semantyczne.
4. Stabilne ID zależą od locatora; importer nie dopasowuje po samym tekście.
5. Zachowywać formatowanie, escape’y i tokeny. Kwoty, markup i wartości będące operandami logiki mają jawne polityki ochrony.
6. Oryginał nigdy nie jest nadpisywany. Write-back tworzy nowy staging w `google_drive/`.
7. Nie kopiować źródłowych mediów do Git ani nie generować ZIP-a przed akceptacją pokrycia.
8. Czytanki zachowują wszystkie warianty i warunki; nie wymyślać jednej kanonicznej kolejności scen.
