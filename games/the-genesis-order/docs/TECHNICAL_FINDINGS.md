# Ustalenia techniczne — The Genesis Order

Daty, źródła i hashe plików znajdują się w [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md). Rozróżniamy fakty z raportu/plików, wnioski oraz niewiadome. Nie kopiujemy do dokumentacji dialogów ani treści gry.

## Inwentaryzacja Windows (2026-10-28)

- Raport obejmuje 17 694 pliki / 19 169 362 931 B (17,85 GiB), bez ostrzeżeń skanowania. Nie zawiera bajtów plików gry.
- Użytkownik wyjaśnia, że `_Redist\fitgirl.md5` to pozostałość niezwiązana z projektem; źródło/sklep/build kopii nadal nie są potwierdzone.
- Największe grupy: 7 352 `.mp4` (16,79 GB), 6 808 `.rpgmvp` (2,01 GB), 2 992 `.rpgmvo` (136,6 MB). Nie są potrzebne do analizy tekstu.
- `possibleTextResourceCount=17625` to szeroki filtr obejmujący również media; nie oznacza liczby dialogów/stringów.

## Potwierdzone z plików JS/JSON z Drive

- Struktura `www/js/rpg_*.js`, `www/data/*.json`, rozszerzenia `.rpgmvp`/`.rpgmvo` i runtime NW.js potwierdzają **RPG Maker MV + NW.js**.
- Marker w `www/js/rpg_core.js` podaje **RPG Maker MV 1.6.1**. To wersja silnika, nie numer wydania/build gry.
- Główny `package.json` ustawia `main` na `www/index.html`. `System.json` podaje start map ID 38 i `versionId=96719260` (wewnętrzny identyfikator projektu, nie potwierdzony numer produktu/builda). `MapInfos.json` zawiera 291 wpisów map.
- Na Drive użytkownik przesłał `www/data/` (305 JSON + `Credits.txt`) i `www/js/`; lokalnie pobrano tylko próbkę potrzebną do pierwszej analizy, nie cały zestaw. Folder `www/data` ma około 52,7 MB, a wszystkie `.js` w `www/js` około 7,7 MB według inwentarza.

### Pierwsza próbka struktury tekstu

- Przetestowano poprawność JSON dla `System.json`, `MapInfos.json`, `CommonEvents.json`, map 001/002/003 oraz mapy startowej 038.
- `CommonEvents.json`: 500 wspólnych zdarzeń i 139 144 polecenia RPG Maker; wykryto 602 nagłówki Show Text (kod 101), 746 linii tekstu (401) i 202 bloki wyborów (102). Detektor znalazł 1 427 niepustych pól tekstu/wyborów o łącznej długości ok. 30 tys. znaków. To wyłącznie Common Events, nie liczba unikalnych stringów całej gry.
- Wspólne zdarzenia zawierają też dziesiątki tysięcy linii skryptowych/pluginowych (kody 355/655) oraz polecenia pluginów. Część tekstów może być tworzona dynamicznie, więc zwykły eksport kodów 101/401 nie zapewni kompletności.
- Próbne mapy potwierdzają, że dialogi i wybory są zapisane bezpośrednio w JSON. Mapa startowa 038 ma niewielką liczbę pól dialogowych; dalsze mapy nie zostały jeszcze przeanalizowane.

## Wtyczki, fonty i układ tekstu

- `plugins.js` ma 56 wpisów, z czego 53 są włączone.
- Aktywne wtyczki wpływające na lokalizację/renderowanie obejmują m.in. `YEP_MessageCore`, `YEP_LoadCustomFonts`, `Eli_FontManager`, `RS_MessageAlign`, `TSR_TextColorAddOn`, `YEP_X_MessageSpeedOpt` i `Choices`.
- Konfiguracja YEP_MessageCore ma word wrapping włączony, domyślną szerokość okna 810 px, 4 wiersze, `GameFont` 32 px i obrys 4 px. Wtyczki fontowe używają dodatkowych rodzin; faktyczny wygląd polskich znaków trzeba testować.
- Aktywny YEP_LoadCustomFonts odwołuje się do 10 plików fontów z `www/fonts/`. Inwentarz wykazał 11 fontów `.ttf`/`.otf` (ok. 2,53 MB), ale folderu fontów nie ma w obecnym uploadzie. Do analizy pokrycia Unicode i przypisań przyda się sam katalog `www/fonts/` — tylko `.ttf`/`.otf`.

## Nieznane / kolejne prace

- Język źródłowy, dokładne wydanie/build i kompletność instalacji.
- Całkowita liczba unikalnych tekstów ze wszystkich 291 map i bazowych JSON-ów; pełne JS/JSON nie zostały jeszcze przetworzone.
- Teksty w skryptach/plugin commands, ustawieniach wtyczek i treściach tworzonych dynamicznie; kompletność ekstrakcji.
- Polskie cmap fontów, mapowanie stylów i renderowanie/łamanie tekstu w grze.
- Bezpieczna metoda patchowania, zapisy, osiągnięcia i test Windows.

Przetwarzanie dotychczasowych plików było statyczne: JSON parsowano, JS przeszukiwano jako tekst; nie uruchamiano gry ani kodu z jej plików. Assety i pobrane pliki pozostają poza Git w ignorowanym `google_drive/`.
