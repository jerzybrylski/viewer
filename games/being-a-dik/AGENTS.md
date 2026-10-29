# Instrukcje — Being a DIK

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/FEASIBILITY.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz wspólne `../../docs/WORKFLOW.md` i `../../docs/TRANSLATION_POLICY.md`.

## Stan i granice

- Tytuł jest **kandydatem**, a nie zatwierdzonym projektem tłumaczeniowym. Właściciel jeszcze nie wybrał między nim a The Genesis Order.
- Pliki przekazane na Drive identyfikują wydanie GOG Season 1. Nie zakładaj obecności Seasons 2/3 ani bieżącego builda, jeśli nie ma na to danych.
- Nie ma polskiego tekstu źródłowego ani potwierdzonego polskiego patcha. Źródłem ma być tekst z konkretnej kopii angielskiej.
- Nie kopiuj tekstu ani przekładu z istniejącego Thai/Chinese patcha. Repo `for-the-plot` jest jedynie technicznym prior art dla Ren'Py.
- W katalogu `google_drive/` są tymczasowe, ignorowane kopie RPA/fontów z Drive. Nie dodawaj ich do Git, nie uruchamiaj gry ani kodu użytkownika.

## Wnioski techniczne do zachowania

- Potwierdzony engine: Ren'Py 7.4.10.2178; tekstowe skrypty są skompilowanymi `.rpyc` w `RPA-3.0`.
- Dla rozpakowania/dekompilacji dobierz wersje narzędzi kompatybilne z Ren'Py 7 (Python 2 bytecode). Używaj kopii archiwów, nie dopisuj `.rpy` do instalacji użytkownika.
- In-game phone, dynamiczne treści, GUI/ekrany, minigry i nazwy mogą wymagać osobnych adapterów poza zwykłym filtrem dialogów. Inwentaryzuj te powierzchnie przed deklarowaniem pełnego pokrycia.
- Font cmap nie jest testem renderowania. Nie twierdź, że wszystkie ekrany poprawnie pokazują polskie znaki przed sprawdzeniem przypisanych stylów i runtime.
