# Roadmap — lokalizacja The Genesis Order

**Cel:** przygotować bezpieczny pipeline od zweryfikowanych źródeł RPG Maker MV, przez tłumaczenie z kontekstem, po lokalny patcher Windows. Tekstów SRW nie kopiujemy do TGO; przenoszone są wyłącznie ogólne praktyki: stabilne ID, JSONL, walidacja placeholderów, branch-aware Markdown i staging bez nadpisywania oryginału.

**Aktualny gate:** eksport i pakiet źródłowy v1 są zamknięte. Odtwarzalny audyt `tools/audit_draft_coverage.py` (425 plików draftów, także `hints/` i `ui-01/`) daje **39 821** unikalnych ID z niepustym tłumaczeniem, **5 277** pustych rekordów do rozstrzygnięcia i **131** chronionych wartości w 45 229 rekordach. Proza widoczna dla gracza jest w praktyce wyczerpana: 39 821 + 94 rekordy zablokowane sygnaturą markup v1 (ADR 002) = **39 915**. Aspiracja 45 000 była nierealna bez tłumaczenia tokenów sterujących i nazw własnych — została zamknięta jako cel; liczniki nie są już miarą postępu. Otwarte są: decyzja o ADR 002, uzgodnienie 40 etykiet map (PR #5, w tym angielskie `Channel 4`), 30 pozycji nazwowych do decyzji właściciela, redakcja/QA 39 821 draftów oraz patcher Windows. Drafty nie są patchem gry.

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
| 6. Rozpoczęcie tłumaczenia | zatwierdzone zasady językowe, glosariusz, partie i kontrola terminologii | **Zakończone dla statycznej prozy**: 39 821 niepustych tłumaczeń + 94 zablokowane sygnaturą (ADR 002). Pozostałe puste rekordy są techniczne, nazwowe albo chronione — patrz `COVERAGE_AUDIT.md`. Drafty wymagają redakcji i testów wyświetlania |
| 7. Import tłumaczenia | walidacja ID, tokenów, braków, nadmiarów i konfliktów | **Częściowo**: step11 zweryfikował 45 229 rekordów, 20 610 tłumaczeń, 131 chronionych wartości i 24 488 oczekujących; nowe 2 521 wierszy z 15 batchy przechodzą test zgodności z kanonicznym eksportem, tokenów/placeholderów, kompletności i unikalności, bez overlapu z wcześniejszymi draftami. Partie nadal pozostają rozdzielone i niescalone; pełna weryfikacja hashy źródeł wymaga ich lokalnego pobrania |
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
- `apply_translation.py --check`: 45 229 rekordów i hashe 238 źródeł bez zapisu w poprzednim sprawdzeniu; Markdown import-check: 45 229 rekordów, brak brakujących ID; pełny zestaw unit tests uruchomiony 2026-10-29: **36/36 passed**, w tym test piętnastu najnowszych partii dialogowych.

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
