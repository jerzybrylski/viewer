# Porównanie kandydatów na projekt lokalizacji VN

Stan na 2026-10-28. Porównanie dotyczy technicznych dowodów z dostarczonych kopii, nie jakości fabuły ani preferencji użytkownika. Żaden tytuł nie został wybrany do rozpoczęcia tłumaczenia.

| Kryterium | The Genesis Order | Being a DIK (GOG Season 1) | Undercover with Nora |
|---|---|---|---|
| Silnik / format | RPG Maker MV 1.6.1 + NW.js; 305 JSON w `www/data`, 78 JS w `www/js` | Ren'Py 7.4.10.2178; RPA-3.0; 158 indeksowanych `.rpyc` | Ren'Py 8.3.3.24111502; RPA-3.0; 23 skrypty `.rpyc`, w tym ep01–ep10 |
| Zakres przekazanych danych | `www/data/`, `www/js/`, `www/fonts/`; pobrano tylko wybrany podzbiór | Dostępne archiwa i manifest GOG; dużych mediów nie przekazano | `game/01001110.rpa`, `script_version.txt`, log; kopia v1.0.0 |
| Język źródłowy | Niepotwierdzony | English `en-US` według manifestu GOG | Angielski w zdekompilowanych skryptach |
| Licznik dialogów / wyborów | Częściowo: `CommonEvents.json` ma 611 niepustych linii dialogu i 816 opcji w 202 blokach; pozostała większość gry niepoliczona | Pełnego licznika brak; 2 z 158 skryptów zdekompilowano próbnie | Pełny statyczny licznik skryptów: **15 036** instrukcji dialogowych; dodatkowo **54** bloki `menu` z **121** tekstowymi opcjami |
| Pewność / ograniczenia | To dokładne zliczenie jednego pliku, nie całej gry; font fallback wymaga testu | Niezweryfikowany pozostały korpus, w tym UI/telefon i dynamiczne teksty | 23/23 skryptów z RPA zdekompilowano; licznik obejmuje jawne dialogi wszystkich gałęzi, nie UI/screeny ani wiersze po zawinięciu |
| Najbliższy etap | Policzyć wszystkie mapy/zasoby tekstowe, sprawdzić font fallback, przygotować branch-aware Czytankę | Zdekompilować i policzyć 158 skryptów, przygotować branch-aware Czytankę | Jeśli tytuł zostanie wybrany: osobno policzyć UI/screeny i przygotować branch-aware Czytankę |
| Główne ryzyko zakresu | 17,85 GiB całej kopii; przeważają media i zasoby graficzne, a eventy zawierają skrypty/pluginy | Obecny materiał obejmuje tylko Season 1; telefon/UI i Seasons 2/3 mogą poszerzyć zakres | Wynik dotyczy wyłącznie v1.0.0; UI/screeny, dynamiczne treści, fonty i import nie są jeszcze ocenione |

## Wniosek roboczy

*Undercover with Nora* ma obecnie najlepiej określony **licznik dialogów**: wszystkie 23 skrypty z jedynego dostarczonego archiwum zostały statycznie zdekompilowane, a jawne instrukcje dialogowe policzone per odcinek. To nie oznacza, że cały zakres lokalizacji (UI, screeny i pozostałe teksty) jest już policzony ani że build v1.0.0 został przetestowany w runtime.

Dla TGO i Being a DIK pełne liczniki pozostają do wykonania. Użytkownik nie wskazał jeszcze tytułu do rozpoczęcia tłumaczenia; przed takim etapem należy porównać zakres wszystkich trzech projektów i zachować rozgałęzienia w Czytankach.
