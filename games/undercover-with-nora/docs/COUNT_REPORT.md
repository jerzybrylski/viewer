# Oszacowanie dialogów — Undercover with Nora

**Zakres:** dostarczona kopia v1.0.0, archiwum `game/01001110.rpa` (RPA-3.0), Ren'Py 8.3.3.24111502. **Stan analizy: pełny statyczny licznik jawnych instrukcji dialogowych skryptów; nie jest to jeszcze pełny licznik wszystkich elementów lokalizacji.**

## Wynik główny

- **15 036 wystąpień instrukcji dialogowych**: 15 031 w skryptach odcinków `ep01`–`ep10` i 5 w wspólnym `script.rpy`.
- **13 344 różne dosłowne treści tekstowe** po deduplikacji identycznych literalnych treści. Deduplikacja nie normalizuje placeholderów/formatowania ani nie uwzględnia kontekstu mówiącego; do pracy tłumacza właściwą podstawą pozostają rekordy z osobnymi identyfikatorami i kontekstem.
- Dodatkowo: **54 bloki `menu` i 121 jawnych tekstowych opcji wyboru** w skryptach odcinków. Wśród samych opcji jest 100 różnych literalnych treści. Wybory są osobną kategorią, nie wliczają się do 15 036 dialogów.
- Dialogi i opcje zsumowane jako wystąpienia dają **15 157 tekstowych wystąpień**. Nie jest to licznik UI.

„Linia dialogowa” w tym raporcie oznacza pojedynczą instrukcję mówienia silnika z przypisanym obiektem postaci/narratora. Nie oznacza fizycznego wiersza w oknie po zawinięciu tekstu; wynik zależy od fontu, rozmiaru i szerokości okna.

## Podział na odcinki

| Moduł | Instrukcje dialogowe | Bloki `menu` | Jawne tekstowe opcje |
|---|---:|---:|---:|
| `ep01.rpy` | 1 475 | 2 | 4 |
| `ep02.rpy` | 1 648 | 7 | 15 |
| `ep03.rpy` | 1 348 | 9 | 18 |
| `ep04.rpy` | 1 736 | 7 | 14 |
| `ep05.rpy` | 1 244 | 5 | 11 |
| `ep06.rpy` | 1 365 | 8 | 19 |
| `ep07.rpy` | 1 287 | 6 | 17 |
| `ep08.rpy` | 1 215 | 4 | 8 |
| `ep09.rpy` | 2 644 | 5 | 12 |
| `ep10.rpy` | 1 069 | 1 | 3 |
| **Odcinki 1–10** | **15 031** | **54** | **121** |
| `script.rpy` (wspólne) | 5 | — | — |
| **Razem dialog** | **15 036** | — | — |

## Metoda i kompletność

1. Sprawdzono folder `game/` na Drive: znajdują się w nim `01001110.rpa` i `script_version.txt`; archiwum RPA indeksuje dokładnie 23 pliki, wszystkie z rozszerzeniem `.rpyc`.
2. `unrpa 2.3.0` wypakował 23 pliki skryptowe do ignorowanego katalogu roboczego. `unrpyc 2.0.3` (commit `3ae8334`) zdekompilował **23/23**, bez błędu.
3. Dialogi zliczono jako instrukcje `say` z rozpoznanym, zadeklarowanym obiektem `Character`. W skryptach odcinków wszystkie takie instrukcje mają statycznie rozpoznanego mówcę. Zliczono też pięć instrukcji w `script.rpy`. Nie znaleziono osobnych wywołań `renpy.say` generujących dodatkowe kwestie; definicja ekranu `screen say` służy do renderowania tych kwestii, nie jest kolejnym tekstem dialogu.
4. Opcje zliczono osobno w blokach `menu` jako jawne tekstowe etykiety, również te z warunkami. Dialog wprowadzający do menu pozostaje policzony jako dialog.
5. Licznik obejmuje **wszystkie zapisane rozgałęzienia i ścieżki warunkowe** w źródłowych skryptach; dialogów z tras alternatywnych nie usunięto tylko dlatego, że nie występują w jednym przejściu.

## Granice raportu

- Wynik jest kompletny dla jawnych instrukcji dialogowych w skompilowanych skryptach znajdujących się w tym archiwum i odpowiada buildowi v1.0.0 przekazanemu na Drive. Nie gwarantuje zgodności z późniejszym lub innym wydaniem.
- Licznik **nie obejmuje** etykiet UI, ustawień, ekranu telefonu/galerii, przycisków, osiągnięć, komunikatów, nazw assetów ani tekstów dostarczanych przez silnik Ren'Py. Przy pełnym planie lokalizacji należy policzyć te elementy oddzielnie.
- 121 opcji oznacza literalne etykiety w instrukcjach `menu`; tekst przycisków i interakcji zdefiniowanych w ekranach UI nie jest doliczany do tej liczby.
- Nie testowano runtime, polskich fontów, zawijania tekstu, dynamicznych podstawień ani patchowania. Nie uruchamiano gry ani zdekompilowanego kodu.
