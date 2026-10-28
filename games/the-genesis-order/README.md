# The Genesis Order — projekt spolszczenia

Projekt rozpoczęty od **bezpiecznej inwentaryzacji lokalnej kopii użytkownika**. Nie ustalono jeszcze wydania, sklepu ani struktury plików; nie zakładamy silnika ani formatu tekstu.

## Stan

**Czekamy na raport inwentaryzacyjny z Windowsa.** Użytkownik potwierdził Windows. Pierwszy pakiet `TGO_INVENTORY_REQUEST.zip` został przesłany na Drive; jego ID to `1Tl3Pmu8PHb5aQXpA5Ah2OKvL0qO96TBe`. Skrypt nie był uruchomiony na komputerze użytkownika.

Szczegóły: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).

## Kolejność prac

1. Użytkownik rozpakowuje i uruchamia `tools/intake/URUCHOM.bat`.
2. Na pulpicie powstaje `TGO_DIAGNOSTIC_....zip`, który użytkownik przesyła na Google Drive.
3. Analizujemy wynik: wersja, katalogi, typy/rozmiary i możliwe zasoby tekstowe.
4. Na podstawie danych przygotowujemy drugi BAT/PS1, który zbierze tylko konkretne pliki potrzebne do rozpoznania.
5. Po otrzymaniu próbki ustalamy ekstrakcję, identyfikatory tekstu, kontekst scen/wyborów, kodowanie i ograniczenia renderowania.

## Pierwszy pakiet

Źródła skryptów są w [`tools/intake/`](tools/intake/). Archiwum wysłane na Drive zawiera `.bat`, `.ps1` i instrukcję. Wynik inwentaryzacji obejmuje ścieżki względne, rozmiary, rozszerzenia, metadane EXE i listę potencjalnych zasobów. **Nie kopiuje treści plików gry ani nie modyfikuje instalacji.**

Nie przesyłaj całego katalogu gry. Przekaż wyłącznie ZIP raportu wygenerowany przez skrypt.
