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
- `unrpyc` v2.0.3 (Git HEAD `3ae8334ed71a05535927dcc559663d3aca51215b`) zdekompilował testowo `math_test2.rpyc` i `chat_replies_magnar.rpyc`; przy pierwszym pojawiło się ostrzeżenie narzędzia, że plik wygląda na Ren'Py 7, podczas gdy ta wersja dekompilatora targetuje Ren'Py 8. Nie testowano jeszcze całego archiwum ani odtwarzania gry.
- Nie testowano patcha ani wyświetlania na Windowsie.
