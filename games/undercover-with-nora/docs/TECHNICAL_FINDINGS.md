# Ustalenia techniczne — Undercover with Nora

## POTWIERDZONE

- Log z kopii zgłasza **Undercover With Nora v1.0.0**, build `2026-10-12 12:39:58 UTC`, Ren'Py **8.3.3.24111502**; osobny `script_version.txt` podaje `(8, 3, 3)`.
- Główne archiwum gry to `game/01001110.rpa`, nagłówek **RPA-3.0**, rozmiar **4 457 540 B**.
- Indeks RPA zawiera **23** skompilowane skrypty `.rpyc`: `ep01`–`ep10` oraz 13 skryptów wspierających. Wszystkie 23 statycznie wypakowano i zdekompilowano bez błędów.
- W dziesięciu skryptach odcinków zliczono **15 031** instrukcji dialogowych; wspólny `script.rpy` zawiera dodatkowe 5. Razem **15 036**. Rozbicie i metoda są zapisane w [`COUNT_REPORT.md`](COUNT_REPORT.md).
- Zliczono osobno 54 jawne bloki `menu` i 121 tekstowych etykiet opcji w modułach odcinków.
- Teksty źródłowe w zbadanych skryptach są angielskie.

## NIEZNANE / NIEZWERYFIKOWANE

- Czy przekazany build v1.0.0 odpowiada dokładnie instalacji sklepowej lub innemu buildowi użytkownika.
- Pełna ilość tekstów UI, ekranów, przycisków i treści dynamicznych poza jawnymi instrukcjami dialogu oraz opcjami `menu`.
- Renderowanie polskich znaków, font coverage, limity, zawijanie i działanie placeholderów w runtime.
- Możliwy wpływ patchowania na zapisy, osiągnięcia i zgodność buildów.

Analizę wykonano statycznie na kopii archiwum. Nie uruchamiano oryginalnego launchera, gry ani zdekompilowanych skryptów.
