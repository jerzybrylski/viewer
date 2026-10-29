# Środowisko — The Genesis Order

## Kopia/inwentarz użytkownika

- Skan Windows 10 build `10.0.16299`, PowerShell `5.1.16299.98`; zero błędów.
- Zgłoszony katalog `D:\Games\The Genesis Order`; pełny store/build nieustalony.
- Inwentarz: 17 694 pliki / 19 169 362 931 B (17,85 GiB); nie kopiował zawartości gry.
- Na Drive są `www/data/` (305 JSON + `Credits.txt`), `www/js/`, `www/fonts/` i główny `package.json`; brak multimediów w przekazanym zestawie.

## Agent sandbox

- Linux, Python 3.11; PowerShell/Ren'Py/game runtime nie są dostępne.
- Oryginalne pliki JSON/JS/fonty znajdują się w ignorowanym `google_drive/`; JSON parsowano i JS/fonty analizowano statycznie. Do cmap użyto FontTools 4.68.0 w `/tmp`.
- Statycznie przetworzono wszystkie 305 JSON i 78 plików JS. Nie ma testu Windows/in-game ani runtime renderingu.
- Binarne assety gry pozostają poza Gitem; tekstowe dane, narzędzia i wszystkie tłumaczenia są śledzone w repozytorium.
