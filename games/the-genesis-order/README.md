# The Genesis Order — projekt spolszczenia

Inwentaryzacja danych tekstowych jest zakończona, a pełny statyczny census eventowych dialogów i wyborów z dostarczonego `www/data/` jest gotowy. Potwierdziliśmy **RPG Maker MV 1.6.1 + NW.js**. Przed tłumaczeniem pozostają osobna inspekcja tekstów skryptowych/pluginowych i UI oraz branch-aware Czytanka.

## Stan

Użytkownik przesłał na Drive `www/data/`, `www/js/`, główny `package.json` oraz `www/fonts/`, bez filmów, obrazów i audio. Pobrano tylko wybrany podzbiór plików do statycznej analizy; niczego z nich nie dodano do Git.

Pełne liczniki eventowych dialogów i wyborów obejmują wszystkie 291 map oraz 500 common events, z zachowaniem zapisanych warunków i rozgałęzień. Dialog, standardowe wybory i pola UI/baz danych są raportowane osobno; 72 623 komendy skryptowe i 1 570 pluginowych wymagają osobnej inspekcji. Czytanka może zachować wszystkie gałęzie, ale nie istnieje jeden wspólny porządek liniowy dla wszystkich wyborów.

## Następny etap

1. Przejrzeć potencjalne teksty w komendach skryptowych/pluginowych oraz UI jako osobny zakres; nie mieszać ich z głównym licznikiem dialogów.
2. Sprawdzić font coverage i ryzyko fallbacku (wstępny cmap wskazuje na problem domyślnego `GameFont`).
3. Przygotować branch-aware Czytankę z ID mapy/eventu, mówiącym, dialogiem, warunkami i oznaczonymi wyborami.
4. Jeśli będzie potrzebna, dodać osobno wybraną ścieżkę przejścia jako skrót, bez zastępowania pełnej Czytanki.

Raport: [pełny census](docs/COUNT_REPORT.md), [liczniki per mapa](docs/COUNT_BY_MAP.csv), [liczniki per common event](docs/COUNT_BY_COMMON_EVENT.csv). Dodatkowe ustalenia: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).
