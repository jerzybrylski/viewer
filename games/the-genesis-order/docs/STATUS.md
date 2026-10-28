# Status — The Genesis Order

**Stan: silnik i format potwierdzone; analiza tekstu rozpoczęta na próbce.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Raport Windows: 17 694 pliki / 17,85 GiB, bez ostrzeżeń; brak assetów w samym raporcie.
- Użytkownik wrzucił na Drive `www/data/` i `www/js/` oraz główny `package.json`; nie ma tam mediów. Lokalnie pobrano wybrane JSON-y i skrypty JS do statycznej analizy.
- Silnik: **RPG Maker MV 1.6.1 + NW.js** (marker wersji w `rpg_core.js`, entry point w `package.json`).
- `System.json` ustawia mapę startową 38; `MapInfos.json` opisuje 291 map. `CommonEvents.json` ma 500 zdarzeń i ponad 139 tys. poleceń eventów.
- 56 wpisów pluginów, 53 aktywne. Wiadomości korzystają m.in. z YEP MessageCore, custom-font managerów, zawijania tekstu i wtyczek ustawiających format wiadomości.
- Aktywny plugin fontowy wymienia 10 plików czcionek w `www/fonts/`. Tego katalogu nie ma w obecnym uploadzie.
- Użytkownik wyjaśnia, że `_Redist\\fitgirl.md5` to pozostałość; źródło i build kopii nadal nie są potwierdzone. Nie wpływa to na identyfikację formatu plików.

## Nieznane / niezweryfikowane

- Język źródłowy, dokładny build/produkt i kompletność kopii.
- Liczba wszystkich unikalnych tekstów: próbka `CommonEvents.json` zawiera wiele natywnych pól dialogu, ale również dziesiątki tysięcy poleceń skryptowych/pluginowych, a pozostałe mapy nie zostały jeszcze przetworzone.
- Pokrycie polskich znaków w fontach oraz wygląd polskiego tekstu w runtime.
- Bezpieczny patch, save migration, osiągnięcia i test Windows.

## Następny krok

Użytkownik dosyła wyłącznie `www/fonts/` (pliki `.ttf` i `.otf`, bez innych mediów). Następnie można przygotować bezpieczny parser/raport tekstów z JSON-ów, rozdzielając dialog, wybory, nazwy/opisy baz danych i pola skryptowe. Dotychczas nie uruchamiano gry ani nie budowano patcha.
