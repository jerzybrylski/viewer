# Dziennik eksperymentów — Undercover with Nora

## 2026-10-28 — inwentaryzacja i statyczny licznik

### Wejścia z Google Drive

- Folder `UWN`: `1B3jxpteGCDTEwNiYkkr6blCV26MWBOgx`.
- `game/01001110.rpa`, file ID `1E2sGB9g81C_yF1fAJyxGZgJ_MicZAmxI`, rozmiar **4 457 540 B**, SHA-256 `979466f74bbb0cbf622f5d2e815e30d6e0c435e6e051eac319834ebd72f66dea`.
- `game/script_version.txt`, file ID `1Gcu7GCiKtd5GA0upVKlA_HPhUJYtsqv4`, zawartość `(8, 3, 3)`.
- `log.txt`, file ID `1Fbxkkovb8AwMucTJGbBK5tQmfkYm7fqN`, podaje wersję gry `v1.0.0`, build z 2026-10-12 i Ren'Py `8.3.3.24111502`.
- Nie pobierano ani nie uruchamiano launchera `.exe`.

### Narzędzia i operacje

1. Zainstalowano `unrpa 2.3.0` do tymczasowego katalogu `/tmp/uwn-unrpa`.
2. `unrpa --list` wykazało 23 pozycje, wszystkie `.rpyc`; po wypakowaniu do ignorowanego `google_drive/uwn/raw/` zostały wypisane 23 pliki.
3. Repozytorium `CensoredUsername/unrpyc` pobrano do `/tmp/uwn-unrpyc`, commit `3ae8334`; CLI zgłosiło `Unrpyc v2.0.3`.
4. Polecenie: `python3 /tmp/uwn-unrpyc/unrpyc.py --processes 1 google_drive/uwn/raw`. Wynik: 23 skrypty przetworzone, 23 pomyślnie zdekompilowane, bez ostrzeżeń/błędów.
5. Licznik zbudowano statycznie na zdekompilowanych skryptach; analizowano deklaracje mówców i instrukcje, nie uruchamiano kodu gry.

### Wynik

- `ep01`–`ep10`: 15 031 jawnych instrukcji dialogowych; `script.rpy`: 5; łącznie **15 036**.
- Identyczne literalne treści tekstowe po prostym deduplikowaniu: **13 344**.
- W `ep01`–`ep10`: **54** bloki menu i **121** tekstowych opcji (100 odrębnych literalnych treści opcji).
- Zestawienie per odcinek i ograniczenia: [`COUNT_REPORT.md`](COUNT_REPORT.md).

### Ograniczenia

Wynik dotyczy tylko dostarczonego builda v1.0.0. Licznik dialogu nie obejmuje UI i innych niedialogowych powierzchni lokalizacji; liczba instrukcji źródłowych nie jest liczbą fizycznych wierszy po zawinięciu. Materiały z Drive i zdekompilowane skrypty pozostają poza Git w ignorowanym `google_drive/`.
