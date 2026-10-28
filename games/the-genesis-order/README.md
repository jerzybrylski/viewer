# The Genesis Order — projekt spolszczenia

Inwentaryzacja i pierwszy transfer zasobów tekstowo-technicznych zostały wykonane. Potwierdziliśmy **RPG Maker MV 1.6.1 + NW.js**; wstępna analiza tekstu ruszyła, ale tłumaczenie ani patch nie są jeszcze rozpoczęte.

## Stan

Użytkownik umieścił na Drive foldery `www/data/`, `www/js/` oraz główny `package.json`, bez filmów, obrazów i audio. Lokalnie pobrano i statycznie przeanalizowano wybrany podzbiór JSON/JS. Pełne zasoby pozostają na Drive; niczego z nich nie dodano do Git.

Aktywne wtyczki modyfikują okno dialogu, fonty, zawijanie tekstu, wybory i wyrównanie. `CommonEvents.json` ma 500 wspólnych zdarzeń i bardzo dużo poleceń skryptowych/pluginowych, więc ekstrakcja musi rozróżniać natywne teksty od kodu i treści dynamicznych.

## Następny krok

Prześlij tylko `www/fonts/` — pliki `.ttf` i `.otf`. Inwentarz wykazał 11 czcionek, a aktywna konfiguracja fontów wskazuje 10 nazw plików. Po analizie cmap można przygotować kompletny, niezmieniający gry raport tekstów z JSON-ów i ocenić zakres translacji.

Szczegóły: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).
