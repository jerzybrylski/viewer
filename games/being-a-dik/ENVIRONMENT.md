# Środowisko — Being a DIK

## Kopia z Drive

- Manifest GOG: `Being a DIK - Season 1`, product/game ID `1181224050`, build ID `55720371802277951`, język `en-US`.
- Primary executable: `BeingADIK.exe`; w manifeście jest też `BeingADIK-32.exe`.
- `game/script_version.txt`: `(7, 4, 10)`.
- `log.txt`: Ren'Py `7.4.10.2178`; zapis wykonania na Windows 10, build `10.0.16299` z 2026-10-27. Jest to metadana z przesłanego logu, nie potwierdzenie aktualnego środowiska użytkownika.
- Brak potwierdzonego numeru wersji zawartości gry poza manifestem Season 1/build ID.

## Narzędzia

- Sandbox: Linux, Python 3.11.2; brak Ren'Py runtime, brak PowerShell i brak lokalnej kompletnej gry.
- RPA indeksy odczytano bez uruchamiania gry ani modułów z jej plików; do odczytu font cmap użyto FontTools 4.68.0.
- Indeksy RPA-3.0 odczytano własnym statycznym parserem; skrypty do testu wyekstrahowano w `/tmp` bez uruchamiania gry.
- `unrpyc` v2.0.3 (Git HEAD `3ae8334ed71a05535927dcc559663d3aca51215b`) statycznie przetworzył 158/158 `.rpyc` i pozwolił bez błędu odczytać wszystkie węzły AST. 133 pliki zgłosiły ostrzeżenie o starszym bytecode Ren'Py 7 wobec targetu Ren'Py 8; wyniki AST są kompletne technicznie, ale semantyczna zgodność starszych plików nie była niezależnie potwierdzana. Nie uruchamiano gry.
- Nie testowano patcha ani wyświetlania na Windowsie.
