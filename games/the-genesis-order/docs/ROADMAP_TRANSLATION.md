# Roadmap — lokalizacja The Genesis Order

**Cel:** przygotować bezpieczny pipeline od zweryfikowanych źródeł RPG Maker MV, przez tłumaczenie z kontekstem, po lokalny patcher Windows. Tekstów SRW nie kopiujemy do TGO; przenoszone są wyłącznie ogólne praktyki: stabilne ID, JSONL, walidacja placeholderów, branch-aware Markdown i staging bez nadpisywania oryginału.

**Aktualny gate:** statyczne skanowanie i eksport są zakończone. Właściciel zatwierdził wszystkie nie-rendererowe wiersze `401` i wszystkie opcje `102` jako pełnoprawny tekst do tłumaczenia. Source ZIP v1 jest śledzony w repozytorium i udostępniony na Google Drive. Tekst wtopiony w obrazy i wideo jest poza zakresem na decyzję właściciela. Ostatni zweryfikowany merge step11: **20 610 niepustych tłumaczeń**, **131 chronionych rekordów**, **24 488 pól oczekujących**. Dla najnowszego żądania realizowany jest kolejny przyrost 10 000 (cel 30 610 łącznie): dotąd powstało **5 004 osobne, niescalone drafty** (Map 9/23/24/116: 1 001; Map 41/55: 557; Map 44: 203; Map 82: 328; Map 54: 370; Map 6: 230; Map 26: 359; 57 Common Events: 1 956), więc do celu pozostaje 4 996. Tłumaczenia wymagają redakcji i nie są patchem gry.

## Kanoniczny przepływ

```text
źródła tekstowe (Git); binarne assety gry (poza Git)
  → statyczne skanery i jawne decyzje
  → games/the-genesis-order/translation/export-v1 (JSONL, Git)
  → Markdown context (Git) + source ZIP v1 (Git + Google Drive)
  → tłumaczenie po ID → walidacja JSONL
  → staging kopii gry → testy właściciela na Windows
```

Repozytorium śledzi wszystkie narzędzia, tekstowe dane źródłowe i robocze tłumaczenia oraz source ZIP v1. Tylko binarne assety gry pozostają poza Git. Staging kopii gry nigdy nie nadpisuje oryginału.

## Bramki i stan

| Etap | Rezultat | Stan |
|---|---|---|
| 1. Inwentaryzacja | 305 JSON + Credits, 291 map, 500 Common Events; hierarchia 78 JS; hashe i statyczny skan; bez uruchamiania gry/kodu | **Zakończone** |
| 2. Audyt tekstowych powierzchni | wiadomości, opcje, skrypty/pluginy, wartości zmiennych, CE53/54/60/222/223/224, note fields, dynamiczne wartości i media | **Zakończone dla znanych statycznych źródeł**; wszystkie wiersze `401` i opcje `102` są w zakresie tłumaczenia, wyłączenia są jawne |
| 3. Kanoniczny eksport | JSONL ze stabilnym ID, hashami, locatorami, kontekstem i tokenami | **45 229 rekordów; wszystkie kontrole pokrycia przeszły** |
| 4. Round-trip | walidator i safe write-back do kopii; testy syntetyczne | **Gotowe statycznie**; `--check` weryfikuje 45 229 rekordów / 238 źródeł |
| 5. Kontekst/pakiet źródłowy | JSONL, instrukcje, glossary/polityka, raport, manifest i Markdown źródłowy | **ZIP v1 wygenerowany i sprawdzony**: 45 229 rekordów / 497 dokumentów; archiwum śledzone w Git i wysyłane na Google Drive |
| 6. Rozpoczęcie tłumaczenia | zatwierdzone zasady językowe, glosariusz, partie i kontrola terminologii | **W toku**; step11 ma 20 610 zweryfikowanych niepustych tłumaczeń; bieżący przyrost do celu 30 610 ma 5 004 niescalone drafty (pozostaje 4 996), w tym 3 048 dialogów map i 1 956 w 57 Common Events; redakcja i testy gry/wyświetlania nadal potrzebne |
| 7. Import tłumaczenia | walidacja ID, tokenów, braków, nadmiarów i konfliktów | **Częściowo**: step11 zweryfikował 45 229 rekordów, 20 610 tłumaczeń, 131 chronionych wartości i 24 488 oczekujących; nowe 5 004 drafty sprawdzono względem kanonicznych ID, metadanych i tokenów, ale pozostają niescalone; pełna weryfikacja hashy źródeł wymaga ich lokalnego pobrania |
| 8. Patcher Windows | wykrycie kopii/builda, backup, atomowy staging, raport/rollback, testy syntetyczne | **Nie rozpoczęto**; wymaga tłumaczenia i docelowego layoutu |
| 9. Finalny patch / polska dystrybucja | przetłumaczony tekst i instalowalny patch | **Nie istnieją**; osobna bramka po tłumaczeniu/QA |

## Audyt pokrycia — liczby kontrolne

- JSONL: 45 229 rekordów, 25 kategorii i `export_manifest.json`.
- 38 638 wpisów customowego CE60; 705 Arianna hints; 30 tekstów telefonu (17 skryptowych + 13 natywnych); 378 elementów UI telefonu; 649 etykiet przedmiotów; 134 image-caption values.
- Natywne teksty: 1 513 wierszy `401` poza rendererami. Wszystkie wiersze są tekstem do tłumaczenia; obejmuje to 1 122 rekordy kategorii `native_message`.
- Wybory: 2 110 opcji / 695 grup. Wszystkie opcje są pełnoprawnym tekstem do tłumaczenia; 180 zachowuje precyzyjniejszą kategorię `ui_choice`, pozostałe 1 930 to `choice_option`.
- Statyczne wartości widoczne przez `\\V[...]`: 262 niepuste rekordy; 132 whitespace-only layout values pominięte; 128 kwot/markerów chronionych `keep_source_value`.
- JavaScript: 78 plików, 563 kandydatury; 35 UI (4 engine-static, 9 parametrów pluginów, 22 static plugin UI), 528 wykluczeń, 0 otwartych.
- 34 pola `note` w Items.json zawierają tagi/metadane bez prozy. 1 570 plugin commands to polecenia sterujące lub parametry, nie jawne teksty UI. Dynamiczne nazwy urządzeń/użytkowników są danymi runtime, nie stringami lokalizacyjnymi.
- `apply_translation.py --check`: 45 229 rekordów i hashe 238 źródeł bez zapisu w poprzednim sprawdzeniu; Markdown import-check: 45 229 rekordów, brak brakujących ID; pełny zestaw unit tests uruchomiony 2026-10-29: **35/35 passed**.

Source ZIP: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; SHA-256 w sąsiednim `.sha256`. Odtwarzanie: `python3 games/the-genesis-order/tools/build_translation_package.py`. ZIP nie zawiera oryginalnych assetów ani kodu gry. Tekst wtopiony w obrazy i wideo jest poza zakresem na decyzję właściciela.

Szczegóły i ograniczenia: [`STATUS.md`](STATUS.md), [`COUNT_REPORT.md`](COUNT_REPORT.md), [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md).

## Zasady jakości i bezpieczeństwa

1. Nie uruchamiać ani nie modyfikować kodu gry; parsery pracują statycznie.
2. Nie interpretować stringa jako UI bez konkretnego dowodu renderowania.
3. Nie nazywać wszystkich widocznych tekstów dialogiem. Zachowywać oddzielne kategorie i jawne niepewności semantyczne.
4. Stabilne ID zależą od locatora; importer nie dopasowuje po samym tekście.
5. Zachowywać formatowanie, escape’y i tokeny. Kwoty, markup i wartości będące operandami logiki mają jawne polityki ochrony.
6. Oryginał nigdy nie jest nadpisywany. Write-back tworzy nowy staging w `google_drive/`.
7. Binarne assety gry pozostają poza Gitem; śledzić wszystkie teksty i narzędzia oraz source ZIP v1.
8. Czytanki zachowują wszystkie warianty i warunki; nie wymyślać jednej kanonicznej kolejności scen.
