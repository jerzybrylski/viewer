# Raport censusu i pokrycia — The Genesis Order

Stan: 2026-10-29. Jest to raport o statycznych źródłach i eksporcie, nie liczba faktycznie odtworzonych dialogów. Nie uruchamiano gry ani kodu z gry.

## Źródła wejściowe

- `data.zip`: 305 poprawnych JSON-ów oraz `Credits.txt`; komplet map `Map001.json`–`Map291.json`, `MapInfos.json` z 291 rekordami i `CommonEvents.json` z 500 zdarzeniami.
- Potwierdzony silnik: RPG Maker MV 1.6.1 + NW.js. Dane źródłowe są w ignorowanym `google_drive/the-genesis-order/`; nie są śledzone w Git.
- Odtworzona hierarchia JS: 78 plików. Oryginalne skrypty są obecnie w kopii roboczej poza repo; tekstowe źródła, narzędzia oraz tłumaczenia powinny być śledzone w Git.

## Wynik eksportu

Kanoniczny eksport `games/the-genesis-order/translation/export-v1/` ma **45 229 unikalnych rekordów**. Manifest kontroluje wszystkie poniższe główne liczniki; wszystkie kontrole przeszły.

| Kategoria | Rekordy | Interpretacja |
|---|---:|---|
| `custom_dialogue` | 38 638 | Wartości V[21] statycznie routowane przez CE60; 29 647 różnych payloadów po wydzieleniu nagłówka. |
| `arianna_hint` | 705 | Statyczny kanał CE222. |
| `phone_text` | 30 | 17 przypisań skryptowych i 13 natywnych wierszy CE54. |
| `phone_contact_ui` | 378 | Widoczne pozycje UI listy CE17. |
| `item_found_label` | 649 | Statyczne etykiety V[107] renderowane przez CE223. |
| `image_caption` | 134 | Wartości V[97]/V[98] widoczne przez static caller path CE224; media nie są analizowane. |
| `native_message` | 1 122 | Wiersze `401` poza rendererami; pełnoprawny tekst gracza do tłumaczenia. |
| `ui_choice` + `choice_option` | 180 + 1 930 | Wszystkie 2 110 opcji / 695 grup; całość pełnoprawny tekst gracza do tłumaczenia. |
| `ui.variable_value` | 262 | Statyczne wartości skryptowe docierające do widocznych `\\V[...]` w wyborach/wiadomościach. |
| Potwierdzone JS UI | 35 | 4 engine-static, 9 parametrów pluginów, 22 static plugin UI. |
| Pozostałe dane | 1 166 | Credits (239), nazwy map (291), aktorów (28), przedmiotów (477) i System (131); razem z pozostałymi kategoriami daje pełne 45 229. |

Uwaga: powyższa tabela łączy kategorie semantycznie; pojedyncze rekordy nie są normalizowane ani łączone po treści. Kategorię i locator kanoniczne zawiera `export_manifest.json` oraz poszczególne pliki JSONL.

### Natywne wiadomości i wybory

- Źródłowy census zawiera **1 521** niepustych wierszy `401`. Osiem wierszy to potwierdzone scaffoldingowe teksty rendererów (CE53/60/222/223/224) i nie są osobnymi rekordami do tłumaczenia. Pozostałe **1 513** są w eksporcie: 1 122 ogólne powierzchnie tekstowe, 378 UI telefonu i 13 natywnych pozycji kanału telefonicznego.
- Wszystkie 1 122 nie-rendererowe wiersze `401` są potwierdzonym tekstem wyświetlanym w oknie wiadomości i pełnoprawnym tekstem do tłumaczenia; rodzaj komunikatu nie zmienia zakresu.
- Wszystkie **695** grup wyboru `102` i **2 110** niepustych opcji są zachowane z kontekstem/gałęziami i pełnoprawnie należą do zakresu tłumaczenia.
- Osiem pominiętych 401 renderer rows jest osobno kontrolowanych w manifeście. CE224 ma 67 statycznie potwierdzonych call sites preładowania obrazów; dwa 401 to renderer scaffolding, a 134 static caller values są eksportowane jako captions. Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo jest poza zakresem tłumaczenia.

### Zmienne, skrypty i pluginy

- Static data-flow audyt V[21] → CE60 daje 38 638 rekordów; kanały CE222 (705), CE53 (17), CE223 (649), CE224 (134) i UI telefonu są osobno nazwane. Pozostałe wartości nie są automatycznie nazywane dialogiem.
- Komenda RPG Maker 122 może ustawić tekst wewnątrz zmiennej skryptowym literałem, a widoczny komunikat/wybór może renderować tę wartość przez `\\V[n]`. Wyeksportowano **262** niepuste wartości w 394 zaobserwowanych statycznych przypisaniach do zmiennych z widocznym sinkiem; **132** wartości zawierające wyłącznie whitespace to layout placeholders i zostały pominięte. Brak nie-literalnych wyrażeń w tych 394 dopasowanych przypisaniach. 61 kwot i 67 markerów są chronione `keep_source_value`; 134 wpisy tekstowe/statusowe są tłumaczalne.
- Globalne sprawdzenie wartości skryptowych wykazało, że niepuste przypisania z tego kanału mają widoczny sink w tym samym evencie/page. 161 przypisań w innych kontekstach zawierało tylko whitespace; nie stanowią dodatkowych braków tłumaczeniowych.
- Przeszukanie kodów 355/655 pod kątem statycznych wywołań alert, message, choice, drawText i printError nie ujawniło innych statycznych literałów poza kanałami już śledzonymi. Oddzielnie zinwentaryzowano API pluginów i statyczne UI JS.
- 1 570 poleceń pluginowych (kod 356) ma sześć typów: AnimationCurve 1 321, MessageWidth 156, MessageRows 42, Play2ndBGS 17, Fadeout2ndBGS 4 i steamworks 30. To operacje sterujące/numeryczne/asset/API, nie bezpośrednie widoczne teksty do lokalizacji.
- 34 pola `Items.json.note` zawierają tagi/metadane, bez prozy. Nie są pomijane zwykłe opisy/nazwy przedmiotów — eksportuje je `database.items.name` oraz pola systemowe wskazane przez schemat.

### Statyczny JS i Lovense

- Skan 78 plików dał **563 kandydatury**: 35 potwierdzonych powierzchni UI, 528 wykluczeń z jawnych content-free powodów, 0 odroczonych i 0 nierozstrzygniętych. Kategorie: `ui.engine_static` 4, `ui.plugin_parameter` 9, `ui.plugin_static` 22.
- Wcześniejsze wykluczenia nie oznaczały wiadomości technicznych ani dialogów; to były identyfikatory, klucze, symbole, konfiguracje, formaty, ścieżki i markup bez dowodu widocznego payloadu w danym locatorze.
- Widoczny Lovense fallback `Not Connected` jest tekstem UI. Etykiety `PC`, `LAN`, `Web` są widoczne, ale chronione, bo te same wartości uczestniczą w logice. Nazwy/nicknames urządzeń są dynamicznymi danymi spoza lokalizowalnego źródła projektu.

## Pola danych — osobno od dialogu

| Źródło | Rekordy | Uwagi |
|---|---:|---|
| System | 131 | Tytuł, waluta, terms i typy/elementy systemowe. |
| Actors.name | 28 | Nazwy aktorów; brak automatycznego zgadywania mówcy z nazw assetów. |
| Items.name | 477 | Nazwy przedmiotów; 34 pola note to wyłącznie metadane. |
| MapInfos.name | 291 | Etykiety map, osobno od wiadomości. |
| Credits.txt | 239 | Niepuste linie napisów końcowych. |

## Round-trip i powtarzalność

- `python3 games/the-genesis-order/tools/export_translation.py` generuje kanoniczny bundle z lokalnych assetów oraz kuratorowanego `reviewed_js_ui.jsonl`.
- `python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check` zweryfikował 45 229 rekordów i **238** hashy plików wejściowych bez zapisu.
- `python3 games/the-genesis-order/tools/markdown_translation.py build --replace` tworzy 497 kontekstowych dokumentów/45 229 rekordów w ignorowanym `google_drive/`; Markdown porządkuje źródła, nie ustala kanonicznej chronologii.
- `python3 -m unittest discover -s games/the-genesis-order/tests -v` jest zestawem testów workflow. Wynik ostatniego pełnego uruchomienia zapisuje `EXPERIMENT_LOG.md`.

## Jawne ograniczenia

- Wszystkie 1 122 wiersze `401` i 1 930 opcji są pełnoprawnym tekstem gracza do tłumaczenia i muszą pozostać w pełnym zakresie.
- Tekst wtopiony w obrazy i wideo pozostaje poza zakresem na wyraźną decyzję właściciela. Runtime’owe wartości dostarczane przez użytkownika/urządzenia i obliczane liczby nie są statycznymi tekstami źródłowymi.
- Nie zweryfikowano renderowania polskich glifów, długości, łamania wierszy ani zachowania UI w działającej grze. Source ZIP v1 jest pakietem źródłowym; osobny patch POC nie jest zatwierdzoną dystrybucją i wymaga testów Windows/runtime.
- Surowe assety nie są śledzone w Git; kanoniczne wyodrębnione JSON-y, dokumentacja, narzędzia i testy są śledzone zgodnie z decyzją właściciela.


## Aktualizacja po ukończeniu przekładu i milestone’ów — 2026-10-29

- Scalenie wszystkich **427** draftów obejmuje 45 229 rekordów: **39 917** niepustych tłumaczeń, **131** jawnie chronionych rekordów `keep_source_value`, **5 181** pozostałych zachowanych rekordów nielokalizowalnych i **0** nierozstrzygniętych rekordów do tłumaczenia. Audyt: `translation/reports/coverage_audit_v1.json`.
- Standalone patch POC: `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`; 39 917 tłumaczeń, 238 fingerprintowanych źródeł, 427 batchy. Zawiera one-click patcher oraz backup/restore, bez plików gry. SHA-256 `f60a2ff512e397ffa1d730bc0d48a5949fbc2541ef7516e9302998cd8d512277`.
- Czytanka PL v1: `reading/v1/`, ZIP `translation/packages/TGO_readalong_PL_v1.zip`; **4 394** rozdziały (4 134 map/event/page i 260 Common Events), 221/291 map osiągalnych potencjalnie od startu w statycznym BFS, 833 wiersze z mówcą nieustalonym jawnie oznaczone; indeksy obejmują 55 etykiet mówców i 291 lokacji. Kolejność nie jest kanoniczna; gra/runtime nie była uruchamiana. ZIP zawiera 4 399 wpisów (4 394 epizody + 5 plików indeksowych/skryptowych); SHA-256 `74a3b096a07e92de32f6b5ac42e9f297cf4a33adf2db21fdd92359f60ec04c4f`.
- Po dodaniu testów generatora Czytanek pełny zestaw: **54/54 passed**. To statyczna walidacja, nie QA językowe ani test instalacji Windows.

### Redakcja odmiany imion (R-09, 2026-10-29)

- **Zakres:** wyłącznie imiona na `-a` z tabelą form (`Erica, Andrea, Arianna, Melissa, Ella, Toma, Diana, Tasha, Alia`).
- **Zmienione:** 383 wystąpienia w 380 rekordach, 148 plików — wołacz po przecinku 247, wołacz całej kwestii 89, wołacz na początku zdania 29, dopełniacz po rzeczowniku/przyimku 18.
- **Bez zmian:** 628 wystąpień, w których przypadek nie wynika ze składni (mianownik po `jest`, konstrukcje z `z`/`o`/`na`, nazwiska). Świadomie nie zgadujemy — raport: `translation/reports/declension_r09_report.json`.
- **Nie zmieniono:** żadnego słowa poza samym imieniem; tokeny `\c[n]` i znaczniki renderera zostają nietknięte (test regresyjny).
