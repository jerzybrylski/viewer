# Status — The Genesis Order

**Stan: pierwszy etap inwentaryzacji zakończony; analiza techniczna w toku.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Użytkownik uruchomił pakiet na Windowsie i przesłał raport `TGO_DIAGNOSTIC_20261028_191643.zip` na Drive.
- Raport obejmuje 17 694 pliki / 17,85 GiB, bez ostrzeżeń skanowania; pliki gry nie zostały do niego skopiowane.
- Struktura `www/js/rpg_*.js`, `www/data/*.json`, `.rpgmvp` / `.rpgmvo` oraz runtime `nw.dll` / `node.dll` mocno wskazuje na RPG Maker MV + NW.js; dokładnej wersji jeszcze nie potwierdzono.
- Raport zawiera znacznik `_Redist\fitgirl.md5`, który może wskazywać na repack. Pochodzenie kopii trzeba wyjaśnić przed kolejnym transferem skryptów/danych gry.

## Nieznane / niezweryfikowane

- Oficjalny sklep/źródło, licencja, wydanie, build i kompletność kopii; dokładna wersja RPG Maker MV.
- Język źródłowy, lokalizacje dialogów/wyborów, format tekstu w JSON-ach i zachowanie wtyczek.
- Liczba lokalizowalnych stringów; `possibleTextResourceCount=17625` jest szerokim filtrem obejmującym także media i nie jest licznikiem tekstu.
- Bezpieczny sposób budowania i instalowania patcha bez naruszenia oryginałów/zapisów.

## Następny krok

Najpierw potwierdzić, że dalszą analizę prowadzimy na legalnej kopii z oficjalnego sklepu (lub wyjaśnić obecność znacznika FitGirl). Po potwierdzeniu przygotować drugi pakiet BAT/PS1 do zebrania minimalnej, precyzyjnej próbki JS/JSON — bez filmów, obrazów, audio ani całej instalacji. Nie uruchamiać kodu gry ani nie modyfikować plików.
