# Status — The Genesis Order

**Stan: etap 1 zakończony; celowany pakiet 2 przygotowany i udostępniony.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Użytkownik uruchomił pakiet inwentaryzacyjny na Windowsie i przesłał wynik na Drive.
- Raport obejmuje 17 694 pliki / 17,85 GiB, bez ostrzeżeń skanowania; raport nie zawiera plików gry.
- Układ `www/js/rpg_*.js`, `www/data/*.json`, `.rpgmvp` / `.rpgmvo` i runtime `nw.dll` / `node.dll` mocno wskazuje na RPG Maker MV + NW.js; dokładna wersja niepotwierdzona.
- W inwentarzu znajduje się `_Redist\fitgirl.md5`. Użytkownik wyjaśnia, że to pozostałość niezwiązana z projektem. Źródło/sklep kopii nadal nie są zapisane.
- Pakiet 2 kopiuje tylko allowlistę małych plików konfiguracyjnych/engine oraz mapę startową wskazaną w `System.json`; nie kopiuje mediów ani pełnego katalogu.

## Nieznane / niezweryfikowane

- Sklep/źródło, wydanie, build i kompletność kopii; dokładna wersja RPG Maker MV.
- Język źródłowy, teksty w plikach danych i zachowanie wtyczek.
- Liczba lokalizowalnych stringów; `possibleTextResourceCount=17625` jest szerokim filtrem obejmującym media, nie licznikiem tekstu.
- Bezpieczny sposób budowania i instalowania patcha bez naruszenia oryginałów/zapisów.

## Następny krok

Pobrać `TGO_STAGE2_REQUEST_v1.0.0.zip` z folderu TGO na Drive, rozpakować, uruchomić `URUCHOM_ETAP2.bat` na kopii, do której użytkownik ma autoryzowany dostęp, a wynikowy `TGO_STAGE2_SAMPLE_*.zip` przesłać na Drive. Pakiet jest tylko do odczytu; nie uruchamia gry ani nie zmienia instalacji.
