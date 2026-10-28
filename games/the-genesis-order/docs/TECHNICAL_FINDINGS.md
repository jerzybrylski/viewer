# Ustalenia techniczne — The Genesis Order

Źródła i dokładne wykonane kroki są w [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md). Oznaczenia: **potwierdzone** = widać w raporcie inwentaryzacyjnym; **wniosek** = silna wskazówka z nazw/układu plików, jeszcze nie zweryfikowana zawartością.

## Potwierdzone z raportu Windows (2026-10-28)

- Skan objął `D:\Games\The Genesis Order`; raport podaje Windows 10 build `10.0.16299`, PowerShell `5.1.16299.98` i zero błędów skanowania. Nazwa konta ani nazwa komputera z logu nie są kopiowane do dokumentacji.
- Inwentarz: **17 694 pliki**, 19 169 362 931 B (17,85 GiB). Folder `www` zawiera 17 564 pliki i ok. 19,0 GB.
- Główne grupy rozszerzeń:

| Rozszerzenie | Liczba | Łączny rozmiar | Interpretacja wstępna |
|---|---:|---:|---|
| `.mp4` | 7 352 | 16 785 208 166 B | dominujące filmy; niepotrzebne do pierwszej próbki tekstu |
| `.rpgmvp` | 6 808 | 2 008 136 905 B | prawdopodobnie zasoby graficzne RPG Maker w formacie/encryption extension |
| `.rpgmvo` | 2 992 | 136 578 987 B | prawdopodobnie zasoby audio RPG Maker |
| `.json` | 307 | 52 703 413 B | prawdopodobne dane gry, w tym `www/data/` |
| `.js` | 78 | 7 727 711 B | silnik i wtyczki JavaScript |
| `.ttf` / `.otf` | 11 | 2 534 176 B | fonty; trzeba sprawdzić cmap i przypisania dopiero na wybranej, autoryzowanej kopii |

- Raport nie zawiera plików gry; zawiera CSV ścieżek/rozmiarów/czasów, podsumowanie, metadane EXE i log. Nie otwierano ani nie uruchamiano plików z instalacji.

## Silnik — mocny wniosek z nazw i układu, jeszcze nie potwierdzenie wersji

- Układ zawiera `www/js/rpg_core.js`, `rpg_managers.js`, `rpg_objects.js`, `rpg_scenes.js`, `rpg_sprites.js`, `rpg_windows.js`, katalog `www/data/` z plikami `Map###.json` i typowe rozszerzenia `.rpgmvp` / `.rpgmvo`.
- Obok są pliki runtime NW.js (`nw.dll`, `node.dll`, `resources.pak`); to mocno wskazuje na **RPG Maker MV uruchamiany przez NW.js**, prawdopodobnie z licznymi modyfikacjami/wtyczkami.
- Dokładna wersja RPG Makera, wersja gry, sklep/build i język źródłowy **nie są ustalone**. `Game.exe` nie ma w raporcie numeru FileVersion ani ProductVersion. Potwierdzenie wymaga minimalnej próbki konkretnych plików tekstowych/configuracyjnych.

## Ważne ograniczenie licznika

Pole `possibleTextResourceCount=17625` oraz CSV „possible text resources” są szerokim filtrem nazw/rozszerzeń. Lista zawiera również tysiące `.mp4`, `.rpgmvp` i `.rpgmvo`; **nie jest** liczbą plików zawierających dialogi ani liczbą stringów do tłumaczenia. Na tym etapie nie znamy liczby tekstów.

## Pochodzenie kopii — do wyjaśnienia przed kolejnym transferem plików

- Inwentarz zawiera `_Redist\fitgirl.md5`. To silny sygnał, że badana instalacja może pochodzić z repacka FitGirl; sama nazwa pliku nie rozstrzyga pochodzenia ani licencji.
- Nie wysyłamy teraz próbek danych/skryptów tej instalacji dalej i nie przygotowujemy patcha, dopóki użytkownik nie potwierdzi autoryzowanego źródła kopii. Jeśli użytkownik ma legalną kopię ze sklepu, dalszą próbkę należy zebrać z tej oficjalnej instalacji.

## Kolejny etap po potwierdzeniu źródła

Przygotować drugi, wąsko zakrojony pakiet, który skopiuje tylko wskazane pliki JavaScript/JSON potrzebne do identyfikacji wersji, wtyczek i małej próbki map/zdarzeń. Nie zbierać filmów, obrazów, audio ani całego katalogu `www`; nadal nie modyfikować gry. Dokładną listę ustalić po potwierdzeniu autoryzowanej kopii.
