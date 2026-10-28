# Porównanie kandydatów na pierwszą VN

Stan na 2026-10-28. Porównanie dotyczy dowodów technicznych, nie jakości fabuły ani preferencji użytkownika.

| Kryterium | The Genesis Order | Being a DIK (przesłane GOG Season 1) |
|---|---|---|
| Pliki od użytkownika | Otrzymana inwentaryzacja metadanych z Windowsa; mała próbka JS/JSON została przygotowana do etapu 2 | Dostępne archiwa, fonty i manifest GOG w Drive |
| Silnik / format | Mocny wniosek: RPG Maker MV + NW.js; wersja/build niepotwierdzone | Ren'Py 7.4.10.2178; RPA-3.0; 158 indeksowanych `.rpyc` |
| Źródło tekstu | Język źródłowy niepotwierdzony | English `en-US` według manifestu GOG |
| Priory art | Nie oceniano dla konkretnej wersji | Repo autora deklaruje workflow Ren'Py i worked example Thai dla tej samej gry; nie odtworzono niezależnie patcha |
| Następny test | Uruchomić pakiet 2 na kopii z autoryzowanym dostępem i przeanalizować wynik | Dwa krótkie `.rpyc` przeszły test `unrpyc`; jeden wynik zawiera ostrzeżenie Ren'Py 7, całość 158 plików niezweryfikowana |
| Główne ryzyko zakresu | 17,85 GiB, z czego przeważają filmy i zasoby `.rpgmvp`/`.rpgmvo`; źródło/build niepotwierdzone | Tytuł jest duży; telefon/UI i Season 2/3 mogą wymagać dodatkowego zakresu; obecny manifest obejmuje Season 1 |

## Wniosek roboczy

Jeśli priorytetem jest **najmniejsze ryzyko techniczne pierwszego pilota**, *Being a DIK* jest obecnie lepiej rozpoznany: istnieją dokładne pliki Season 1, próbnie zdekompilowane skrypty i prior art dla Ren'Py na tej samej grze. *The Genesis Order* ma już silnie rozpoznany prawdopodobny silnik, a pakiet 2 zbiera wąską próbkę potrzebną do potwierdzenia formatu i wersji.

Ostatecznego wyboru nie dokonano. Rozmiar danych TGO nie równa się rozmiarowi tłumaczenia — dominują media, a liczby tekstu jeszcze nie znamy.
