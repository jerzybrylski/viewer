# Being a DIK — kandydat na spolszczenie

Wstępna ocena: **technicznie bardzo osiągalne dla przesłanej edycji GOG Season 1**. Nie znaleziono wiarygodnego polskiego spolszczenia. To na razie kandydat, nie zatwierdzony start tłumaczenia.

## Co wiemy z plików na Drive

- Manifest GOG identyfikuje `Being a DIK - Season 1`, język `en-US`, primary EXE `BeingADIK.exe`, build ID `55720371802277951`.
- Log gry podaje Ren'Py `7.4.10.2178`; `script_version.txt` zawiera `(7, 4, 10)`.
- W `game/scripts.rpa` znaleziono 158 indeksowanych skompilowanych skryptów `.rpyc`.
- Kilka dołączonych fontów zawiera wszystkie 18 polskich liter: Museo 500, Redressed, Candara oraz Century Gothic Regular/Bold. Konkretne przypisanie fontów do dialogów wymaga dalszej analizy i testu w grze.
- Publiczne repo Ren'Py dla tego samego tytułu deklaruje fanowski projekt Thai dla Episodes 1–8 i osobny zakres telefonu. To prior art opisany przez autora, nie niezależnie zweryfikowany patch; nie używamy jego tekstu jako źródła ani nie kopiujemy przekładu.

Szczegółowa [ocena osiągalności](docs/FEASIBILITY.md), [ustalenia](docs/TECHNICAL_FINDINGS.md) i [dziennik analizy plików](docs/EXPERIMENT_LOG.md).

## Zakres i kolejny krok

Pliki na Drive potwierdzają **Season 1**, nie pełne Seasons 1–3. Najbezpieczniejszy pilot, jeśli wybierzesz tę grę, to ekstrakcja i test na Episode 1; po potwierdzeniu pipeline'u można ocenić pozostałe epizody oraz osobne DLC. Do statycznego rozpoznania podstawowe archiwum skryptów jest już dostępne na Drive. Pełne media potrzebne będą dopiero do testów runtime / scen wizualnych.

Nie rozpoczęto jeszcze tłumaczenia ani budowania patcha.
