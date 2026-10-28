# Porównanie kandydatów na pierwszą VN

Stan na 2026-10-28. Porównanie dotyczy dowodów technicznych, nie jakości fabuły ani preferencji użytkownika.

| Kryterium | The Genesis Order | Being a DIK (przesłane GOG Season 1) |
|---|---|---|
| Pliki od użytkownika | Raport metadanych plus `www/data/` i `www/js/`; pobrano wybraną próbkę | Dostępne archiwa, fonty i manifest GOG w Drive |
| Silnik / format | RPG Maker MV 1.6.1 + NW.js; 305 JSON w `www/data`, 78 JS w `www/js` | Ren'Py 7.4.10.2178; RPA-3.0; 158 indeksowanych `.rpyc` |
| Źródło tekstu | Język źródłowy niepotwierdzony | English `en-US` według manifestu GOG |
| Priory art | Nie oceniano dla konkretnej wersji | Repo autora deklaruje workflow Ren'Py i worked example Thai dla tej samej gry; nie odtworzono niezależnie patcha |
| Następny test | Pełny licznik tekstów/wyborów i Czytanka; częściowy licznik `CommonEvents.json`: 611 niepustych linii dialogu, 816 opcji w 202 blokach; sprawdzić font fallback | Pełny licznik 158 skryptów `.rpyc` i Czytanka; obecnie zdekompilowano tylko dwa skrypty |
| Główne ryzyko zakresu | 17,85 GiB, z czego przeważają filmy i zasoby `.rpgmvp`/`.rpgmvo`; w eventach są tysiące poleceń skryptowych/pluginowych | Tytuł jest duży; telefon/UI i Season 2/3 mogą wymagać dodatkowego zakresu; obecny manifest obejmuje Season 1 |

## Wniosek roboczy

Jeśli priorytetem jest **najmniejsze ryzyko techniczne pierwszego pilota**, *Being a DIK* jest obecnie lepiej rozpoznany: istnieją dokładne pliki Season 1, próbnie zdekompilowane skrypty i prior art dla Ren'Py na tej samej grze. *The Genesis Order* ma już silnie rozpoznany prawdopodobny silnik, a pakiet 2 zbiera wąską próbkę potrzebną do potwierdzenia formatu i wersji.

Ostatecznego wyboru nie dokonano. Rozmiar danych TGO nie równa się rozmiarowi tłumaczenia — dominują media, a liczby tekstu jeszcze nie znamy.
