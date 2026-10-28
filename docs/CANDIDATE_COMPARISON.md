# Porównanie kandydatów na projekt lokalizacji VN

Stan na 2026-10-28. Porównanie dotyczy technicznych dowodów z dostarczonych kopii, nie jakości fabuły ani preferencji użytkownika. Żaden tytuł nie został wybrany do rozpoczęcia tłumaczenia.

| Kryterium | The Genesis Order | Being a DIK (GOG Season 1) | Undercover with Nora |
|---|---|---|---|
| Silnik / format | RPG Maker MV 1.6.1 + NW.js; 305 JSON w `www/data`, 78 JS w `www/js` | Ren'Py 7.4.10.2178; RPA-3.0; 158 indeksowanych `.rpyc` | Ren'Py 8.3.3.24111502; RPA-3.0; 23 skrypty `.rpyc`, w tym ep01–ep10 |
| Zakres przekazanych danych | `www/data/`, `www/js/`, `www/fonts/`; pobrano tylko wybrany podzbiór | Dostępne archiwa i manifest GOG; dużych mediów nie przekazano | `game/01001110.rpa`, `script_version.txt`, log; kopia v1.0.0 |
| Język źródłowy | Niepotwierdzony | English `en-US` według manifestu GOG | Angielski w zdekompilowanych skryptach |
| Licznik dialogów / wyborów | Częściowo: `CommonEvents.json` ma 611 niepustych linii dialogu i 816 opcji w 202 blokach; 291 map niepoliczonych | Skrypty: **16 669** instrukcji `Say` / **14 650** różnych tekstów; **521** menu / **1 266** opcji. Telefon: dodatkowo **487** wiadomości/feedu i **400** odpowiedzi gracza (te osobno) | Pełny statyczny licznik skryptów: **15 036** instrukcji dialogowych; dodatkowo **54** bloki `menu` z **121** tekstowymi opcjami |
| Pewność / ograniczenia | To dokładne zliczenie jednego pliku, nie całej gry; pozostałe mapy trzeba policzyć; font fallback wymaga testu | 158/158 skryptów statycznie przetworzono; 133 mają ostrzeżenie starszego Ren’Py bytecode. UI i pozostałe teksty ekranów telefonu nadal poza censussem | 23/23 skryptów z RPA zdekompilowano; licznik obejmuje jawne dialogi wszystkich gałęzi, nie UI/screeny ani wiersze po zawinięciu |
| Najbliższy etap | Dokończyć census 291 map z tekstowego JSON-pakietu, sprawdzić font fallback, przygotować branch-aware Czytankę | Osobno zinwentaryzować UI/pozostałe teksty telefonu, przygotować branch-aware Czytankę | Jeśli tytuł zostanie wybrany: osobno policzyć UI/screeny i przygotować branch-aware Czytankę |
| Główne ryzyko zakresu | 17,85 GiB całej kopii; przeważają media i zasoby graficzne, a eventy zawierają skrypty/pluginy | Obecny materiał obejmuje tylko Season 1; telefon/UI i Seasons 2/3 mogą poszerzyć zakres | Wynik dotyczy wyłącznie v1.0.0; UI/screeny, dynamiczne treści, fonty i import nie są jeszcze ocenione |

## Wniosek roboczy

*Undercover with Nora* ma obecnie najlepiej określony **licznik dialogów**: wszystkie 23 skrypty z jedynego dostarczonego archiwum zostały statycznie zdekompilowane, a jawne instrukcje dialogowe policzone per odcinek. *Being a DIK* ma pełny statyczny census 158 skryptów Season 1 oraz osobno policzone statyczne wiadomości i wybory telefonu; UI pozostaje osobnym zakresem, a 133 starsze bytecode pliki mają ostrzeżenie zgodności narzędzia. Dla TGO licznik jest nadal częściowy: komplet map trzeba jeszcze przetworzyć z przesłanych danych tekstowych. Żaden tytuł nie został wybrany do rozpoczęcia tłumaczenia.
