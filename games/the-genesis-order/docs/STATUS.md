# Status — The Genesis Order

**Stan: silnik i format potwierdzone; przed tłumaczeniem przechodzimy do pełnej inwentaryzacji tekstów.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Raport Windows: 17 694 pliki / 17,85 GiB, bez ostrzeżeń; raport nie zawierał assetów.
- Użytkownik przesłał `www/data/`, `www/js/`, główny `package.json` oraz `www/fonts/`; brak filmów, obrazów i audio. Pobrano do statycznej analizy wybrany podzbiór JSON/JS/fontów; nic nie dodano do Git.
- Silnik: **RPG Maker MV 1.6.1 + NW.js**.
- `System.json` wskazuje mapę startową 38; `MapInfos.json` opisuje 291 map. `CommonEvents.json` zawiera 500 zdarzeń i ponad 139 tys. event commands.
- 56 wpisów pluginów, 53 aktywne. Wtyczki rozszerzają okno wiadomości, fonty, zawijanie i wybory.
- Sprawdzono cmap 11 fontów: siedem ma komplet polskich liter, trzy tylko `óÓ`, jeden nie ma żadnej z 18 badanych liter. Domyślne `GameFont` wskazuje na JosefinSans-SemiBold, który ma tylko `óÓ`; runtime fallback nie był testowany.
- Użytkownik wyjaśnia, że `_Redist\fitgirl.md5` to pozostałość; źródło i build kopii nadal nie są potwierdzone.

## Nieznane / niezweryfikowane

- Łączna liczba lokalizowalnych linii/dialogów/wyborów w TGO; dokładny licznik jest obecnie tylko dla `CommonEvents.json` (611 niepustych linii dialogu, 816 opcji), bez deduplikacji i bez pozostałych map/plików.
- Teksty i warunki w pozostałych mapach, plugin commands i skryptach dynamicznych; jeszcze nie przetworzono całego zbioru.
- Rzeczywiste wyświetlanie polskich znaków, fallback, długości i łamanie tekstu w runtime.
- Bezpieczny patch, save migration, osiągnięcia i test Windows.

## Następny krok

Dokończyć bezpośredni upload tekstowych danych jako jednego ZIP-a zawierającego `Map001.json`–`Map291.json` oraz `CommonEvents.json` (opcjonalnie `MapInfos.json`; bez mediów i bez BAT/PS1). Następnie policzyć pełny census JSON-ów (dialog, kontynuacje, wybory i tekstowe pola skryptowe) z jasnym podziałem na pewne i niepewne teksty. Przygotować Czytankę jako strukturę chronologiczną z rozgałęzieniami, nie zakładając jednego kanonicznego wyboru. Dopiero potem decydować o tłumaczeniu i formacie wdrożenia.
