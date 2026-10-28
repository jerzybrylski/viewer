# The Genesis Order — projekt spolszczenia

Inwentaryzacja i pierwszy transfer zasobów tekstowo-technicznych są zakończone. Potwierdziliśmy **RPG Maker MV 1.6.1 + NW.js**. Przed tłumaczeniem przygotujemy pełny licznik tekstów i próbkę Czytanki.

## Stan

Użytkownik przesłał na Drive `www/data/`, `www/js/`, główny `package.json` oraz `www/fonts/`, bez filmów, obrazów i audio. Pobrano tylko wybrany podzbiór plików do statycznej analizy; niczego z nich nie dodano do Git.

`CommonEvents.json` zawiera natywne dialogi i wybory, lecz także dużo poleceń pluginowych/skryptowych. Dlatego podamy oddzielnie pewne liczniki dialogów/wyborów i teksty wymagające dalszej inspekcji. Czytanka może zachować wszystkie gałęzie, ale nie istnieje jeden wspólny porządek liniowy dla wszystkich wyborów.

## Następny etap

1. Zweryfikować font coverage i ryzyko fallbacku (wstępny cmap wskazuje na problem domyślnego `GameFont`).
2. Zbudować pełny, walidowany licznik tekstów z map/zdarzeń, wyborów, baz danych i miejsc z pluginów.
3. Przygotować przykładowy fragment Czytanki z ID mapy/sceny, mówiącym, tekstem i oznaczonymi wyborami/warunkami.
4. Domyślnie zachować wszystkie rozgałęzienia i warunki; jeśli będzie potrzebna, dodać osobno wybraną ścieżkę przejścia jako skrót, bez zastępowania pełnej Czytanki.

Szczegóły: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).
