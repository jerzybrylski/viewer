# Roadmap — lokalizacja The Genesis Order

**Cel:** przygotować bezpieczny pipeline od zweryfikowanych źródeł RPG Maker MV, przez tłumaczenie z kontekstem, po lokalny patcher Windows. Tekstów SRW nie kopiujemy do TGO; przenoszone są wyłącznie ogólne praktyki: stabilne ID, JSONL, walidacja placeholderów, branch-aware Markdown i staging bez nadpisywania oryginału.

**Aktualny gate:** statyczne skanowanie, eksport, tłumaczenia kwalifikującego się tekstu, standalone patch POC oraz Czytanka PL v1 są zbudowane. Merge 427 draftów: 45 229 rekordów, 39 917 tłumaczeń, 131 jawnie chronionych, 5 181 zachowane nielokalizowalne, 0 nierozstrzygniętych. Korpus odtworzony ze scalenia draftów jest bajt w bajt zgodny z payloadem patcha POC, więc nic nie istnieje tylko w ZIP-ie. Pozostają: decyzje redakcyjne z `EDITORIAL_DECISIONS.md`, redakcja językowa, testy fontów/łamania oraz Windows/runtime i QA w kopii gry; obrazy/wideo są wyłączone z zakresu.

## Kanoniczny przepływ

```text
źródła tekstowe (Git); binarne assety gry (poza Git)
  → statyczne skanery i jawne decyzje
  → games/the-genesis-order/translation/export-v1 (JSONL, Git)
  → Markdown context (Git) + source ZIP v1 (Git + Google Drive)
  → tłumaczenie po ID → walidacja JSONL
  → staging kopii gry → testy właściciela na Windows
```

Repozytorium śledzi narzędzia, tekstowe dane, robocze tłumaczenia oraz osobne source/patch/readalong ZIP-y. Tylko binarne assety gry pozostają poza Git. Staging kopii gry nigdy nie nadpisuje oryginału.

## Bramki i stan

| Etap | Rezultat | Stan |
|---|---|---|
| 1. Inwentaryzacja | 305 JSON + Credits, 291 map, 500 Common Events; hierarchia 78 JS; hashe i statyczny skan; bez uruchamiania gry/kodu | **Zakończone** |
| 2. Audyt tekstowych powierzchni | wiadomości, opcje, skrypty/pluginy, wartości zmiennych, CE53/54/60/222/223/224, note fields, dynamiczne wartości i media | **Zakończone dla znanych statycznych źródeł**; wszystkie wiersze `401` i opcje `102` są w zakresie tłumaczenia, wyłączenia są jawne |
| 3. Kanoniczny eksport | JSONL ze stabilnym ID, hashami, locatorami, kontekstem i tokenami | **45 229 rekordów; wszystkie kontrole pokrycia przeszły** |
| 4. Round-trip | walidator i safe write-back do kopii; testy syntetyczne | **Gotowe statycznie**; `--check` weryfikuje 45 229 rekordów / 238 źródeł |
| 5. Kontekst/pakiet źródłowy | JSONL, instrukcje, glossary/polityka, raport, manifest i Markdown źródłowy | **ZIP v1 wygenerowany i sprawdzony**: 45 229 rekordów / 497 dokumentów; archiwum śledzone w Git i wysyłane na Google Drive |
| 6. Tłumaczenie i klasyfikacja draftów | tekst widoczny dla gracza, kontekst, tokeny, właściwe wyłączenia | **Przekład pustych kwalifikujących się treści uzupełniony**: Map 46 craft prompts (+94) i końcowe naturalne teksty UI (+9); audyt pozostałych pustych pól nie znalazł dalszych zwykłych fraz do tłumaczenia. Cały corpus nadal wymaga redakcji, terminologii i testów wyświetlania |
| 7. Import/merge draftów | walidacja ID, źródeł, tokenów, konfliktów i pokrycia | **Gotowe statycznie:** 427 batchy, 45 229 rekordów, 39 917 tłumaczeń, 131 chronionych, 5 181 zachowane nielokalizowalne, 0 nierozstrzygniętych; brak konfliktów |
| 8. Patcher Windows | backup, staging, one-click patch/restore | **Proof of concept zbudowany i testowany syntetycznie**; instalację/build oraz zachowanie na Windows trzeba zweryfikować na kopii |
| 9. Finalny patch / polska dystrybucja | przetłumaczony tekst i instalowalny patch | **POC ZIP jest gotowy statycznie**; nie jest zatwierdzoną dystrybucją bez testów Windows/runtime, zgodności builda i QA |

## Milestones po zamknięciu tłumaczeń

1. **Standalone patch ZIP — POC gotowy:** `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`, z backup/restore i one-click patcherem; nie zawiera gry. Następny gate: test na kopii docelowej instalacji Windows.
2. **Czytanki fabuły — v1 gotowe:** `reading/v1/` i `translation/packages/TGO_readalong_PL_v1.zip`; 4 394 rozdziały, mówcy, warunki, rozgałęzienia i wybory, z jawnym ostrzeżeniem o przybliżonej kolejności. Statyczny graf obejmuje 221/291 map od mapy startowej; to nie jest kanoniczna oś czasu.

## Audyt pokrycia — liczby kontrolne

- JSONL: 45 229 rekordów, 25 kategorii i `export_manifest.json`.
- 38 638 wpisów customowego CE60; 705 Arianna hints; 30 tekstów telefonu (17 skryptowych + 13 natywnych); 378 elementów UI telefonu; 649 etykiet przedmiotów; 134 image-caption values.
- Natywne teksty: 1 513 wierszy `401` poza rendererami. Wszystkie wiersze są tekstem do tłumaczenia; obejmuje to 1 122 rekordy kategorii `native_message`.
- Wybory: 2 110 opcji / 695 grup. Wszystkie opcje są pełnoprawnym tekstem do tłumaczenia; 180 zachowuje precyzyjniejszą kategorię `ui_choice`, pozostałe 1 930 to `choice_option`.
- Statyczne wartości widoczne przez `\\V[...]`: 262 niepuste rekordy; 132 whitespace-only layout values pominięte; 128 kwot/markerów chronionych `keep_source_value`.
- JavaScript: 78 plików, 563 kandydatury; 35 UI (4 engine-static, 9 parametrów pluginów, 22 static plugin UI), 528 wykluczeń, 0 otwartych.
- 34 pola `note` w Items.json zawierają tagi/metadane bez prozy. 1 570 plugin commands to polecenia sterujące lub parametry, nie jawne teksty UI. Dynamiczne nazwy urządzeń/użytkowników są danymi runtime, nie stringami lokalizacyjnymi.
- `apply_translation.py --check`: w poprzednim sprawdzeniu 45 229 rekordów / hashe 238 źródeł bez zapisu; najnowszy pełny `unittest` po odzyskaniu pracy: **88/88 passed** (patcher, Czytanka, bramka pokrycia, audyt draftów).

Source ZIP: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; SHA-256 w sąsiednim `.sha256`. Odtwarzanie: `python3 games/the-genesis-order/tools/build_translation_package.py`. ZIP nie zawiera oryginalnych assetów ani kodu gry. Tekst wtopiony w obrazy i wideo jest poza zakresem na decyzję właściciela.

Szczegóły i ograniczenia: [`STATUS.md`](STATUS.md), [`COUNT_REPORT.md`](COUNT_REPORT.md), [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md). Otwarte decyzje redakcyjne: [`EDITORIAL_DECISIONS.md`](EDITORIAL_DECISIONS.md). Metoda odzyskania korpusu: [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).

## Zasady jakości i bezpieczeństwa

1. Nie uruchamiać ani nie modyfikować kodu gry; parsery pracują statycznie.
2. Nie interpretować stringa jako UI bez konkretnego dowodu renderowania.
3. Nie nazywać wszystkich widocznych tekstów dialogiem. Zachowywać oddzielne kategorie i jawne niepewności semantyczne.
4. Stabilne ID zależą od locatora; importer nie dopasowuje po samym tekście.
5. Zachowywać formatowanie, escape’y i tokeny. Kwoty, markup i wartości będące operandami logiki mają jawne polityki ochrony.
6. Oryginał nigdy nie jest nadpisywany. Write-back tworzy nowy staging w `google_drive/`.
7. Binarne assety gry pozostają poza Gitem; śledzić wszystkie teksty i narzędzia oraz source ZIP v1.
8. Czytanki zachowują wszystkie warianty i warunki; nie wymyślać jednej kanonicznej kolejności scen.
