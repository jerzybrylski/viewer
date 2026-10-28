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
- Użytkownik przesłał pełne `www/data/` w `data.zip`: 305 JSON + `Credits.txt`, w tym wszystkie 291 map. ZIP został zweryfikowany i statycznie przetworzony; `www/js` pozostaje poza pełnym tekstowym censussem. Folder `www/data` ma około 52,7 MB, a wszystkie `.js` w `www/js` około 7,7 MB według inwentarza.

### Pierwsza próbka struktury tekstu

- Przetestowano poprawność JSON dla `System.json`, `MapInfos.json`, `CommonEvents.json`, map 001/002/003 oraz mapy startowej 038.
- `CommonEvents.json`: 500 wspólnych zdarzeń i 139 144 polecenia RPG Maker; wykryto 602 bloki Show Text (kod 101), 746 poleceń kontynuacji (401), z których 611 zawiera niepuste linie tekstu, oraz 202 bloki wyborów (102) z 816 opcjami. Łącznie to 1 427 niepustych pól tekstowych (611 linii dialogu + 816 opcji), 30 143 znaki źródłowe. To pełne liczenie tego jednego pliku, nie całej gry, i nie jest liczbą unikalnych stringów po deduplikacji.
- Wspólne zdarzenia zawierają też dziesiątki tysięcy linii skryptowych/pluginowych (kody 355/655) oraz polecenia pluginów. Część tekstów może być tworzona dynamicznie, więc zwykły eksport kodów 101/401 nie zapewni kompletności.
- Pełny census wszystkich map i common events: 1 521 niepustych komend tekstowych `401` (766 różnych surowych tekstów), 695 grup wyborów `102` i 2 110 tekstowych opcji (376 różnych etykiet). Wszystkie 291 map i 500 common events zostały przetworzone, a wszystkie zapisane warunki/odnogi uwzględniono bez ich ewaluowania. Dokładne wyniki i oddzielny census pól UI/baz danych: [`COUNT_REPORT.md`](COUNT_REPORT.md); per mapa/per common event: [`COUNT_BY_MAP.csv`](COUNT_BY_MAP.csv), [`COUNT_BY_COMMON_EVENT.csv`](COUNT_BY_COMMON_EVENT.csv).

## Wtyczki, fonty i układ tekstu

- `plugins.js` ma 56 wpisów, z czego 53 są włączone.
- Aktywne wtyczki wpływające na lokalizację/renderowanie obejmują m.in. `YEP_MessageCore`, `YEP_LoadCustomFonts`, `Eli_FontManager`, `RS_MessageAlign`, `TSR_TextColorAddOn`, `YEP_X_MessageSpeedOpt` i `Choices`.
- Konfiguracja YEP_MessageCore ma word wrapping włączony, domyślną szerokość okna 810 px, 4 wiersze, `GameFont` 32 px i obrys 4 px. Wtyczki fontowe używają dodatkowych rodzin; faktyczny wygląd polskich znaków trzeba testować.
- Aktywny YEP_LoadCustomFonts odwołuje się do 10 plików fontów z `www/fonts/`; użytkownik przesłał ten katalog i 11 fontów `.ttf`/`.otf` (ok. 2,53 MB) zostały sprawdzone statycznie.
- Cmap 18 polskich liter (`ąćęłńóśźżĄĆĘŁŃÓŚŹŻ`): pełne 18/18 mają Akong_agi, Chapbook-Regular, Cinzel-Black, Cinzel-Regular, SpecialElite, mplus-1m-regular i texgyreadventor-regular; tylko `óÓ` (2/18) mają JosefinSans-Regular, JosefinSans-SemiBold i underworld; UglyTypist ma 0/18.
- `gamefont.css` mapuje rodzinę `GameFont` na `JosefinSans-SemiBold.ttf`, której cmap zawiera tylko `óÓ`. YEP_MessageCore domyślnie używa `GameFont`; to ryzyko brakujących polskich znaków, ale przeglądarkowy fallback/runtime nie był testowany. `mplus-1m-regular.ttf` ma komplet glifów, lecz nie pojawia się na liście plików YEP_LoadCustomFonts.
- Tytułowa `TitleFont` jest przypisana przez Eli_FontManager do Cinzel-Regular (18/18). Cmap potwierdza glify, nie wygląd, fallback, metryki ani łamanie wierszy.

## Nieznane / kolejne prace

- Język źródłowy, dokładne wydanie/build i kompletność instalacji.
- Teksty lokalizowalne w komendach skryptowych/pluginowych, ustawieniach wtyczek, JavaScript i treściach tworzonych dynamicznie; pełne pokrycie lokalizacyjne jest szersze niż census dialogów/wyborów.
- Rzeczywiste renderowanie/fallback polskich liter, pomiary długości tekstu i testy okien w grze; cmap nie zastępuje testu runtime.
- Bezpieczna metoda patchowania, zapisy, osiągnięcia i test Windows.

Przetwarzanie dotychczasowych plików było statyczne: JSON parsowano, JS przeszukiwano jako tekst; nie uruchamiano gry ani kodu z jej plików. Assety i pobrane pliki pozostają poza Git w ignorowanym `google_drive/`.
