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
- Użytkownik przesłał pełne `www/data/` w `data.zip`: 305 JSON + `Credits.txt`, w tym wszystkie 291 map. ZIP został zweryfikowany i statycznie przetworzony. Osobno odtworzono i statycznie przeskanowano 78 plików `www/js`; skan 563 kandydatur rozstrzygnięto jako 35 UI, 528 wykluczeń, 0 otwartych. Runtime/dynamiczne dane i media pozostają poza statycznym tekstowym censussem. Folder `www/data` ma około 52,7 MB, a wszystkie `.js` w `www/js` około 7,7 MB według inwentarza.

### Pierwsza próbka struktury tekstu

- Przetestowano poprawność JSON dla `System.json`, `MapInfos.json`, `CommonEvents.json`, map 001/002/003 oraz mapy startowej 038.
- `CommonEvents.json`: 500 wspólnych zdarzeń i 139 144 polecenia RPG Maker; wykryto 602 bloki Show Text (kod 101), 746 poleceń kontynuacji (401), z których 611 zawiera niepuste linie tekstu, oraz 202 bloki wyborów (102) z 816 opcjami. Łącznie to 1 427 niepustych pól tekstowych (611 linii dialogu + 816 opcji), 30 143 znaki źródłowe. To pełne liczenie tego jednego pliku, nie całej gry, i nie jest liczbą unikalnych stringów po deduplikacji.
- Wspólne zdarzenia zawierają też dziesiątki tysięcy linii skryptowych/pluginowych (kody 355/655) oraz polecenia pluginów. Część tekstów może być tworzona dynamicznie, więc zwykły eksport kodów 101/401 nie zapewni kompletności.
- Pierwszy census `401` miał **1 521** niepustych natywnych wierszy; 8 to scaffoldingowe renderery CE53/60/222/223/224, a pozostałe **1 513** są wyeksportowane jako pełnoprawny tekst do tłumaczenia: 1 122 wiadomości, 378 UI listy telefonu i 13 natywnych tekstów telefonu. CE60 zawiera osobno 38 638 dodatkowych wpisów z literalnych V[21] (29 647 różnych payloadów). CE224 ma 67 call sites preładowania obrazów i 134 wyeksportowane static caller values V[97]/V[98]. Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo jest poza zakresem. Wybory: 695 grup `102` / 2 110 opcji, wszystkie pełnoprawny tekst do tłumaczenia. Dodatkowy static flow audit wykrył 262 niepuste wartości komendy 122 renderowane przez `\\V[...]`; 128 kwot/markerów są chronione. Wszystkie 291 map i 500 common events przetworzono statycznie, zachowując warunki/odnogi bez ewaluacji. Szczegóły: [`COUNT_REPORT.md`](COUNT_REPORT.md); liczniki per mapa/per common event: [`COUNT_BY_MAP.csv`](COUNT_BY_MAP.csv), [`COUNT_BY_COMMON_EVENT.csv`](COUNT_BY_COMMON_EVENT.csv). Liczniki wybranych customowych kanałów odtwarza [`tools/count_custom_text.py`](../tools/count_custom_text.py).

## Wtyczki, fonty i układ tekstu

- `plugins.js` ma 56 wpisów, z czego 53 są włączone.
- Aktywne wtyczki wpływające na lokalizację/renderowanie obejmują m.in. `YEP_MessageCore`, `YEP_LoadCustomFonts`, `Eli_FontManager`, `RS_MessageAlign`, `TSR_TextColorAddOn`, `YEP_X_MessageSpeedOpt` i `Choices`.
- Konfiguracja YEP_MessageCore ma word wrapping włączony, domyślną szerokość okna 810 px, 4 wiersze, `GameFont` 32 px i obrys 4 px. Wtyczki fontowe używają dodatkowych rodzin; faktyczny wygląd polskich znaków trzeba testować.
- Aktywny YEP_LoadCustomFonts odwołuje się do 10 plików fontów z `www/fonts/`; użytkownik przesłał ten katalog i 11 fontów `.ttf`/`.otf` (ok. 2,53 MB) zostały sprawdzone statycznie.
- Cmap 18 polskich liter (`ąćęłńóśźżĄĆĘŁŃÓŚŹŻ`): pełne 18/18 mają Akong_agi, Chapbook-Regular, Cinzel-Black, Cinzel-Regular, SpecialElite, mplus-1m-regular i texgyreadventor-regular; tylko `óÓ` (2/18) mają JosefinSans-Regular, JosefinSans-SemiBold i underworld; UglyTypist ma 0/18.
- `gamefont.css` mapuje rodzinę `GameFont` na `JosefinSans-SemiBold.ttf`, której cmap zawiera tylko `óÓ`. YEP_MessageCore domyślnie używa `GameFont`; to ryzyko brakujących polskich znaków, ale przeglądarkowy fallback/runtime nie był testowany. `mplus-1m-regular.ttf` ma komplet glifów, lecz nie pojawia się na liście plików YEP_LoadCustomFonts.
- Tytułowa `TitleFont` jest przypisana przez Eli_FontManager do Cinzel-Regular (18/18). Cmap potwierdza glify, nie wygląd, fallback, metryki ani łamanie wierszy.

## Wstawki wideo w scenariuszu (2026-10-31)

**POTWIERDZONE na danych gry.** Skan 292 plików `www/data` (305 JSON map + `CommonEvents.json`, 470 493 polecenia, źródło: `data.zip` z Drive, SHA-256 `c9deca5c733cbbc92306e41a8afa0157e38758283a9c7662960349f9b9fd5842`) wskazuje jedno API odtwarzania:

- `ysp.VideoPlayer.newVideo('Nazwa', slot)` tworzy klip w slocie,
- `ysp.VideoPlayer.playVideoById(slot)` uruchamia go,
- `ysp.VideoPlayer.setLoopById(slot)` zapętla,
- `stopVideoById`, `releaseVideo`, `isReady` to sterowanie i odpytywanie stanu, nie start odtwarzania,
- `loadVideo('Nazwa')` to wstępne ładowanie (preload), nie odtwarzanie.

Wzorzec jest jednorodny: **każdy** z 3 812 bloków odtwarzania zawiera `newVideo` + `playVideoById` w tym samym bloku skryptowym (`355` + `655`), a `setLoopById` występuje w 3 188 z nich. Nie ma bloków `newVideo` bez `play`, ani `playVideoById` bez `newVideo`.

**Rozkład:** 3 812 wywołań w 305 rozdziałach (2 678 w Common Events, 1 134 w eventach map), 3 696 różnych nazw plików. Katalog `www/movies` zawiera 7 354 pozycje: 7 352 `.mp4` i 2 `.webm`; większość klipów ma bliźniaka z sufiksem `-l` (wersja niskiej jakości), więc unikalnych klipów HQ jest 3 678. Rozmiary użytych klipów: 0,62–44,45 MB, mediana 2,02 MB; 275 nazw ma plik poniżej 1,5 MB (krótkie wstawki, m.in. `AdChng1.mp4`–`AdChng7.mp4`).

**Rozbieżność danych (NIEZGODNOŚĆ, nie poprawiana):** 24 nazwy z poleceń nie mają odpowiednika w plikach tej kopii — cała rodzina `BC-Ar-Bo1O2…BC-Ar-Bo15O2` i `BC-Ar-OT1O2…BC-Ar-OT9O2` (pliki istnieją jako `BC-Ar-Bo1.mp4` itd., bez sufiksu `O2`). Czytanka pokazuje nazwę z kodu i adnotację „pliku nie ma w inwentarzu tej kopii”; nie dopisujemy ani nie usuwamy sufiksu bez dowodu.

**Narzędzia:** `tools/scan_movie_calls.py` (skan tylko-do-odczytu, wynik `tgo-movie-calls-v1`, tryb `--compact` do śledzenia w Git) oraz `--movie-calls` w `tools/build_readalong.py`, który wstawia znaczniki `> **🎬 Wstawka wideo:** \`plik\`` na pozycji `command_index`, tworzy `index_movies_PL.md` i dodaje rozdziały zawierające wyłącznie klip. Ścieżka lokalna na Windows: `tools/intake/SCAN_MOVIES_TGO.ps1` (nieuruchamiana, **niezweryfikowana**).

**OGRANICZENIA:** skan pokrywa wyłącznie polecenia eventów; stan slotów `ysp.VideoPlayer` jest odtwarzany statycznie w obrębie strony eventu, bez wykonania warunków i bez runtime. Klipy uruchamiane z kodu JS/pluginów albo zależne od stanu gry poza eventem mogą pozostać poza inwentarzem. Gry nie uruchamiano, mediów nie kopiowano.

## Nieznane / kolejne prace

- Dokładny produktowy build instalacji właściciela oraz kompletność plików względem tego builda.
- Wszystkie wyeksportowane wiersze `401` i opcje `102` są zatwierdzone jako tekst do tłumaczenia; zakres opisano w `COUNT_REPORT.md`.
- Renderowanie/fallback polskich liter, pomiary długości, łamanie wierszy i zachowanie okien wymagają osobnego, zatwierdzonego testu runtime na kopii.
- Patcher standalone istnieje jako POC z backup/restore; nie przeszedł testów Windows/docelowego builda. Migracji save'ów ani obsługi osiągnięć nie przygotowano.
- Tekst osadzony w obrazach/audio/wideo oraz wartości dostarczane dynamicznie przez urządzenia/użytkownika nie są statycznym tekstem źródłowym.

Przetwarzanie jest statyczne: JSON parsowano, JS skanowano jako tekst; nie uruchamiano gry ani kodu z jej plików. Binarne assety gry pozostają poza Git; tekstowe dane i narzędzia podlegają śledzeniu w Git. Aktualny eksport znajduje się w `games/the-genesis-order/translation/export-v1/`.
