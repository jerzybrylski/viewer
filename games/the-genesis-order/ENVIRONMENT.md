# Środowisko — The Genesis Order

## Kopia/inwentarz użytkownika

- Skan Windows 10 build `10.0.16299`, PowerShell `5.1.16299.98`; zero błędów skanowania.
- Zgłoszony katalog `D:\Games\The Genesis Order`; pełny store/build nieustalony.
- Inwentarz raportuje 17 694 pliki / 19 169 362 931 B (17,85 GiB); nie kopiował zawartości gry.
- Użytkownik przesłał na Drive `www/data/` (305 JSON + `Credits.txt`), `www/js/` oraz główny `package.json`. Nie przesłano `www/fonts/` ani multimediów.

## Agent sandbox

- Linux, Python 3.11; PowerShell/Ren'Py/game runtime nie są dostępne.
- Pobrano wybrane pliki JSON/JS do ignorowanego katalogu `google_drive/`; parsowano JSON i czytano JS statycznie. Nie uruchamiano gry ani game code.
- Nie wszystkie 305 JSON i 78 JS zostały lokalnie pobrane lub przetworzone. Nie ma testu Windows/in-game.
- Nie commituj żadnych assetów, nawet pobranych próbek; do Git trafia wyłącznie narzędzie i dokumentacja.
