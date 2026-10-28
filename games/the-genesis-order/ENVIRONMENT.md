# Środowisko — The Genesis Order

## Raport z kopii użytkownika

- Skan wykonano lokalnie na Windows 10 build `10.0.16299`, PowerShell `5.1.16299.98`; narzędzie nie zgłosiło błędów skanowania.
- Zgłoszony katalog gry: `D:\Games\The Genesis Order`.
- Raport nie zawierał bajtów plików gry, tylko ścieżki/rozmiary/rozszerzenia/czasy oraz metadane i log. Nie wykonywaliśmy gry ani jej kodu w sandboxie.
- W raporcie EXE `Game.exe` nie ma podanej FileVersion/ProductVersion. Sklep i build pozostają nieznane.

## Agent sandbox

- Linux, Python 3.11; PowerShell i lokalna kopia gry nie są dostępne.
- Wczytano metadane ZIP/CSV/JSON/TXT wyłącznie przez biblioteki odczytu. Nie uruchamiano żadnego pliku z gry ani nie ekstraktowano jej assetów.
- ZIP raportu i lokalne pliki robocze znajdują się w ignorowanym przez Git katalogu `google_drive/`.
