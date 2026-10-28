# Instrukcje — The Genesis Order

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz `../../docs/WORKFLOW.md`.

## Bieżący etap

Użytkownik przesłał `www/data/` i `www/js/` bez multimediów. Silnik potwierdzono jako RPG Maker MV 1.6.1 + NW.js. Pobieraj tylko konkretne pliki potrzebne do analizy; pozostałe nadal są na Drive. Folder fontów `www/fonts/` jest kolejną potrzebną małą próbką.

## Zasady dla TGO

- Nie proś o całą instalację ani media. Do renderowania potrzebne są wyłącznie `.ttf` i `.otf` z `www/fonts/`.
- Nie uruchamiaj kodu gry ani skryptów JS z instalacji; czytaj JSON bezpiecznym parserem, a JS analizuj statycznie. Nie nadpisuj oryginałów, zapisów ani ustawień.
- Dane eventów zawierają natywne wiadomości, ale też wiele plugin/script commandów. Nie utożsamiaj surowej liczby tekstów/kodów z liczbą lokalizowalnych stringów.
- Dziennikuj wyniki z Drive ID, nazwą, rozmiarem i SHA-256. Rozdzielaj potwierdzone / wnioski / niewiadome.
- Nie kopiuj do repo treści gry ani danych osobowych z transcriptu. Assety lokalne pozostają w ignorowanym `google_drive/`.
- Tłumaczenie nie jest rozpoczęte. Najpierw zbuduj i zwaliduj pełny eksport tekstów, strukturę kontekstu i tokenów; patch dopiero po decyzji o zakresie.
