# Status — Undercover with Nora

**Stan: pełny statyczny licznik instrukcji dialogowych dla dostarczonego builda v1.0.0; bez tłumaczenia i patcha.** Aktualizacja: 2026-10-28.

## POTWIERDZONE

- Kopia loguje wersję gry `v1.0.0` i Ren'Py `8.3.3.24111502`.
- Archiwum `01001110.rpa` jest RPA-3.0 i zawiera 23 skompilowane skrypty `.rpyc`; obejmuje moduły `ep01`–`ep10`.
- Wszystkie 23 skrypty zdekompilowano statycznie.
- Licznik skryptów historii: 15 036 wystąpień instrukcji dialogowych (15 031 w `ep01`–`ep10`, 5 w `script.rpy`). Dodatkowo policzono menu i opcje — szczegóły w [`COUNT_REPORT.md`](COUNT_REPORT.md).
- Zliczenie obejmuje tekst w wszystkich zapisanych gałęziach kodu, a nie jedną trasę przejścia.

## NIEZNANE / NIEZWERYFIKOWANE

- Zgodność tej kopii z wydaniem ze sklepu lub innym buildem.
- Pełny zakres lokalizacji poza dialogami: teksty UI/screenów, etykiety przycisków, osiągnięcia i treści danych dynamicznych.
- Rzeczywiste łamanie wierszy, font coverage, zachowanie placeholderów i wyświetlanie polskiego tekstu w runtime.
- Bezpieczna metoda importu/patchowania, save compatibility oraz test Windows.

## Następny krok

Jeśli tytuł zostanie wybrany, przygotować osobny licznik UI i pozostałych ekranów, stabilny eksport z kontekstem sceny/mówcy/gałęzi oraz próbkę Czytanki. Nie rozpoczynać tłumaczenia przed ustaleniem zakresu.
