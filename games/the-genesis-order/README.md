# The Genesis Order — projekt spolszczenia

Pierwsza, bezpieczna inwentaryzacja lokalnej kopii użytkownika jest zakończona. Układ plików mocno wskazuje na RPG Maker MV + NW.js; dokładna wersja i język źródłowy nie są jeszcze potwierdzone.

## Stan

**Etap 2 przygotowany; czekamy na małą próbkę plików.** Raport `TGO_DIAGNOSTIC_20261028_191643.zip` znajduje się na Drive, ID `1gwWlg0ywzYY8k0gjWDi77iTNGl70zmaL`. Zawiera tylko inwentarz/metadane — żadnych plików gry.

W inwentarzu znajduje się `_Redist\fitgirl.md5`; użytkownik twierdzi, że to pozostałość niezwiązana z projektem. Nie traktujemy tego jako dowodu pochodzenia kopii, ale sklep/wydanie nadal nie są potwierdzone. Nowy pakiet uruchamiaj wyłącznie na kopii, do której masz autoryzowany dostęp.

## Pakiet 2

Pobierz [TGO_STAGE2_REQUEST_v1.0.0.zip z Google Drive](https://drive.google.com/file/d/1TNI-ZixJyXj9FP7RXwOE969GqwOOcv4-/view?usp=drivesdk), rozpakuj i uruchom `URUCHOM_ETAP2.bat`. Skrypt kopiuje tylko małą listę plików konfiguracyjnych/silnika oraz mapę startową wskazaną w `System.json`. Nie kopiuje całej gry, filmów, obrazów, audio, zapisów ani ustawień użytkownika i niczego nie zmienia w instalacji. Prześlij na Drive wyłącznie wynikowy `TGO_STAGE2_SAMPLE_*.zip`.

Szczegóły: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).

Nie rozpoczęto jeszcze ekstrakcji pełnego tekstu, tłumaczenia ani budowy patcha.
