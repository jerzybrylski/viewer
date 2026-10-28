# Status — The Genesis Order

**Stan: pełny statyczny census eventowych dialogów i standardowych wyborów dla przekazanego `www/data/` gotowy; projekt pozostaje kandydatem.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Dostarczony `data.zip` zawiera 305 poprawnych JSON-ów i `Credits.txt`; zweryfikowano CRC i komplet map `Map001.json`–`Map291.json` bez przerw w ID.
- Silnik: RPG Maker MV 1.6.1 + NW.js. `MapInfos.json` opisuje 291 map, `CommonEvents.json` zawiera 500 zdarzeń. `System.json` podaje `versionId=96719260`, wewnętrzny identyfikator projektu, nie produktowy numer wydania.
- Statyczny census wszystkich map i common events: 1 521 niepustych wierszy dialogu (766 różnych surowych tekstów), 695 bloków wyboru i 2 110 opcji (376 różnych tekstów). Rozgałęzienia i warunki są uwzględnione.
- Pola UI/baz danych raportowane są oddzielnie; skryptowe i pluginowe event commands wymagają osobnego przeglądu.
- W cmap 11 fontów: 7 zawiera wszystkie 18 badanych polskich liter. Domyślny `GameFont` wskazuje na JosefinSans-SemiBold, który ma tylko `óÓ`; runtime fallback nie był testowany.
- `_Redist\\fitgirl.md5` to według użytkownika pozostałość niezwiązana z projektem; źródło i build kopii nie są potwierdzone.

## Nieznane / niezweryfikowane

- Teksty lokalizowalne zakodowane w 72 623 komendach skryptowych (`355`/`655`) oraz 1 570 komendach pluginowych (`356`); nie uruchamiano ani nie interpretowano kodu.
- Pełny zakres UI z pluginów i JavaScriptu, wiadomości generowane dynamicznie oraz teksty w mediach.
- Rzeczywiste renderowanie polskich znaków, fallback, długości i łamanie tekstu w runtime.
- Bezpieczny patch, save migration, osiągnięcia i test Windows.

## Następny krok przed tłumaczeniem

Przejrzeć potencjalne teksty z komend skryptowych/pluginowych oraz UI jako osobną kategorię; następnie przygotować branch-aware Czytankę z ID mapy/eventu, mówiącym, tekstem, warunkami i wyborami. Nie ma jednej kanonicznej trasy. Dopiero po porównaniu zakresów decydować o tytule i formacie wdrożenia. Tłumaczenia nie rozpoczęto.

Szczegółowe wyniki w [`COUNT_REPORT.md`](COUNT_REPORT.md); liczniki per mapa i common event znajdują się w [`COUNT_BY_MAP.csv`](COUNT_BY_MAP.csv) i [`COUNT_BY_COMMON_EVENT.csv`](COUNT_BY_COMMON_EVENT.csv).
