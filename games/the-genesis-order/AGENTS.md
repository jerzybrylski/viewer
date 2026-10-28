# Instrukcje — The Genesis Order

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz `../../docs/WORKFLOW.md`.

## Bieżący etap

Użytkownik przesłał `www/data/`, `www/js/` i `www/fonts/` bez multimediów. Silnik potwierdzono jako RPG Maker MV 1.6.1 + NW.js. Przed tłumaczeniem użytkownik chce rzetelnego oszacowania zakresu dla TGO i Being a DIK oraz chronologicznych Czytanek z oznaczeniem scen, mówiących i wyborów.

## Zasady dla TGO

- Nie proś o całą instalację ani media. Użytkownik przesłał już tekstowe dane, JS i fonty.
- Nie uruchamiaj kodu gry ani skryptów JS z instalacji; czytaj JSON bezpiecznym parserem, a JS analizuj statycznie. Nie nadpisuj oryginałów, zapisów ani ustawień.
- Licz osobno bloki dialogów, linie kontynuacji, opcje wyboru, UI/bazy danych i teksty w skryptach/pluginach. Nie sumuj ich bez wyjaśnienia i nie traktuj każdej linii skryptu jako tekstu do tłumaczenia.
- Czytanka musi zachować mapę/label, identyfikator sceny, mówiącego, kolejność, wybory, warunki i wywołania common events. RPG Maker jest rozgałęziony; nie zakładaj jednej kanonicznej chronologii. Oznacz gałęzie i warunki zamiast zgadywać.
- Zapisuj niepewność, duplikaty, dynamiczne stringi i miejsca wymagające testu. Nie zaczynaj tłumaczenia przed akceptacją zakresu.
- Dziennikuj wyniki z Drive ID, nazwą, rozmiarem i SHA-256. Nie kopiuj dialogów ani assetów do Git; lokalne pliki pozostają w ignorowanym `google_drive/`.
