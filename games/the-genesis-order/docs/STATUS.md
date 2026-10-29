# Status — The Genesis Order

**Stan: audyt i eksport statycznych powierzchni tekstowych zakończone; paczki ZIP nie przygotowano.** Aktualizacja: 2026-10-29.

## Wynik bieżący

- Kanoniczny, śledzony w Git eksport znajduje się w `games/the-genesis-order/translation/export-v1/`: **45 229 rekordów** w 25 plikach JSONL oraz `export_manifest.json`. Obejmuje źródłowe dane gry i 35 zatwierdzonych, statycznych rekordów UI JS; oryginalne assety `www/data/` i `www/js/` pozostają poza Gitem w ignorowanym `google_drive/`.
- Eksport przeszedł wszystkie kontrolne liczniki: stabilne, unikalne ID; kompletne hashe i locatory; kanały tekstowe, wybory, UI i dane zgodne z audytem. `apply_translation.py --check` sprawdził **45 229/45 229** rekordów oraz hashe **238** plików źródłowych, bez zapisu i bez uruchomienia kodu gry.
- Szkic Markdown został odświeżony do **497 dokumentów / 45 229 rekordów** w ignorowanym `google_drive/the-genesis-order/translation/markdown-draft-v1/`. To widok kontekstowy według kolejności źródeł, nie zatwierdzona Czytanka ani pakiet dla tłumacza.
- Pełny zestaw testów: **27/27 passed** (`python3 -m unittest discover -s games/the-genesis-order/tests -v`); wynik zapisano w `EXPERIMENT_LOG.md`. Pełny runtime gry, renderowanie polskiego tekstu i test Windows nie były uruchamiane.

## Pokrycie

| Powierzchnia / kategoria | Rekordy | Uwagi |
|---|---:|---|
| Customowy dialog CE60 | 38 638 | 29 647 różnych payloadów; tekst oddzielony statycznie od nagłówka. |
| Arianna hints | 705 | Potwierdzony przepływ przez CE222. |
| Telefon | 30 | 17 wartości skryptowych + 13 natywnych wierszy CE54; osobno od UI listy. |
| UI listy telefonu CE17 | 378 | Widoczne opcje/lista, nie klasyfikowane jako dialog. |
| Etykiety znalezionych przedmiotów | 649 | Statyczne wartości V[107] renderowane przez CE223. |
| Obrazowe podpisy CE224 | 134 | 67 statycznych wywołań; dwie komendy 401 to scaffolding renderera, nie osobny tekst. Tekst w samych obrazach nie jest analizowany. |
| Natywne wiersze 401 poza rendererami | 1 513 | Wszystkie zachowane jako widoczne powierzchnie: 1 122 o nieustalonym semantycznym podtypie, 378 elementów telefonu i 13 tekstów telefonu. Osiem wierszy rendererów jest pominiętych. |
| Wybory 102 | 2 110 | 695 grup; 180 znanych opcji UI, 1 930 pozostałych pozostawionych bez zgadywania podtypu fabuła/UI. |
| Statyczne wartości zmiennych wyświetlane przez `\\V[...]` | 262 | 134 wartości tekstowe/statusowe tłumaczalne; 61 cen i 67 markerów chronionych `keep_source_value`. 132 wartości zawierające wyłącznie białe znaki pominięto jako layout. |
| Potwierdzone UI JS | 35 | 4 `ui.engine_static`, 9 `ui.plugin_parameter`, 22 `ui.plugin_static`; statyczny skan 78 plików: 563 kandydatury, 528 wykluczeń, 0 otwartych. |

Pozostałe kategorie obejmują 239 niepustych linii Credits, 291 nazw map, 28 nazw aktorów, 477 nazw przedmiotów oraz 131 rekordów System. Eksport jest kanonicznym materiałem źródłowym; puste pole `translation` nie oznacza gotowego przekładu.

## Audyt brakujących kanałów

- Statycznie przeskanowano wszystkie 78 dostarczonych plików JS. Wszystkie 563 kandydatury otrzymały decyzję: 35 potwierdzonych powierzchni UI, 528 wykluczeń z jawnym, content-free powodem, 0 odroczonych i 0 nierozstrzygniętych. Wcześniejsze wykluczenia dotyczyły wartości kodu/konfiguracji/markup bez dowodu UI w danym locatorze — nie należy nazywać ich wiadomościami ani dialogami.
- Statyczny przegląd komend skryptowych wykrył i włączył alerty, błędy Graphics, statyczny przepływ Lovense oraz wartości tekstowe V[97]/V[98] wyświetlane w CE224. Dodatkowo przeszukano sinki wiadomości, opcji, drawText i alert w kodach eventowych 355/655; poza odrębnie śledzonymi kanałami nie wykryto statycznych literałów przy tych sinkach.
- 1 570 komend pluginowych sklasyfikowano jako sterowanie/parametry: AnimationCurve (1 321), MessageWidth (156), MessageRows (42), Play2ndBGS (17), Fadeout2ndBGS (4) i steamworks (30). To nie są pominięte teksty dialogowe; identyfikatory i parametry runtime pozostają nietranslacyjne.
- Zbadano 34 pola `note` w bazie przedmiotów: zawierają tagi/metadane, bez prozy. Pola edytora, nazwy assetów i media nie są częścią eksportu tekstu.
- Lovense: `PC`, `LAN` i `Web` są widocznymi etykietami trybu, ale importer chroni je jako wartości używane przez logikę; `Not Connected` jest eksportowany jako tłumaczalny tekst UI. Nazwy urządzeń/nicknames z zewnętrznego runtime są danymi użytkownika/urządzenia, nie statycznymi źródłami gry.

## Ograniczenia i dalsze bramki

- Semantyczny podział 1 122 natywnych wiadomości `401` i 1 930 pozostałych opcji na fabułę, tutorial, komunikat lub UI nie został zgadywany. Wszystkie są jednak dołączone jako potwierdzone powierzchnie widocznego tekstu.
- Tekst osadzony w obrazach/audio/wideo, runtime’owe nazwy urządzeń/użytkowników oraz obliczane wartości liczbowe nie są wyodrębniane jako statyczne źródła lokalizacyjne.
- Brak zweryfikowanej polskiej zwrotki, testu długości/łamania w runtime, testu na Windows, instalatora i patcha. Nie przygotowywać ZIP-a, dopóki właściciel nie uzna pokrycia za zweryfikowane.

## Powtarzalne polecenia

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
```

Szczegółowe liczniki i metody: [`COUNT_REPORT.md`](COUNT_REPORT.md). Specyfikacja rekordów: [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md). Roadmapa i bramki przed ZIP-em: [`ROADMAP_TRANSLATION.md`](ROADMAP_TRANSLATION.md).
