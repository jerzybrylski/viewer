# Środowisko i kopia źródłowa — Undercover with Nora

## Potwierdzone na Drive

- Folder `UWN` (ID `1B3jxpteGCDTEwNiYkkr6blCV26MWBOgx`) zawiera katalog `game`, katalog `renpy`, katalog aktualizacji, log i launchery.
- `game/` zawiera `01001110.rpa` (4 457 540 bajtów) i `script_version.txt` (`(8, 3, 3)`). W archiwum jest 23 skompilowanych skryptów `.rpyc`, w tym `ep01`–`ep10`.
- Log startowy zgłasza `Undercover With Nora v1.0.0`, build z 2026-10-12 i Ren'Py `8.3.3.24111502`.
- Nie potwierdzono, czy ta kopia jest identyczna z jakimkolwiek innym wydaniem/sklepem.

## Środowisko analizy

- Z archiwum pobrano tylko `01001110.rpa` do ignorowanego `google_drive/`; plik launchera `.exe` nie był pobierany ani uruchamiany.
- Pliki z RPA wyodrębniono do ignorowanego `google_drive/uwn/raw/` narzędziem `unrpa 2.3.0`; 23/23 `.rpyc` zdekompilowano `unrpyc 2.0.3` (commit `3ae8334`), bez błędów.
- Analiza była statyczna. Nie uruchamiano gry, kodu gry ani zdekompilowanych skryptów.
- Materiały wejściowe i wynikowe `.rpy` były dotąd przechowywane lokalnie; tekstowe dane projektu powinny być śledzone w Git.
