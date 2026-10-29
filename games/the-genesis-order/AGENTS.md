# Instrukcje — The Genesis Order

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz `../../docs/WORKFLOW.md`.

## Bieżący etap

Statyczny audyt i eksport są zakończone. Kanoniczny eksport w `translation/export-v1/` zawiera 45 229 rekordów. Zobacz `docs/HANDOFF_NEXT_AGENT.md` oraz `docs/STATUS.md` przed dalszymi zmianami. Wszystkie nie-rendererowe wiersze `401` i wszystkie opcje `102` są zatwierdzone jako pełnoprawny tekst gracza do tłumaczenia. Source ZIP v1 ma być śledzony w Git i publikowany na Google Drive. Tekst wtopiony w obrazy i wideo jest poza zakresem decyzją właściciela; tłumaczenie pól w JSONL nie rozpoczęło się.

## Zasady dla TGO

- Nie proś o całą instalację ani media. Użytkownik przesłał już tekstowe dane, JS i fonty.
- Nie uruchamiaj kodu gry ani skryptów JS z instalacji; czytaj JSON bezpiecznym parserem, a JS analizuj statycznie. Nie nadpisuj oryginałów, zapisów ani ustawień.
- Licz osobno bloki dialogów, linie kontynuacji, opcje wyboru, UI/bazy danych i teksty w skryptach/pluginach. Nie sumuj ich bez wyjaśnienia i nie traktuj każdej linii skryptu jako tekstu do tłumaczenia.
- Czytanka musi zachować mapę/label, identyfikator sceny, mówiącego, kolejność, wybory, warunki i wywołania common events. RPG Maker jest rozgałęziony; nie zakładaj jednej kanonicznej chronologii. Oznacz gałęzie i warunki zamiast zgadywać.
- Zapisuj niepewność, duplikaty, dynamiczne stringi i miejsca wymagające testu. TGO jest wybranym projektem; rozwijaj pełny workflow, ale każdą niepotwierdzoną klasyfikację oznaczaj zamiast zgadywać.
- Dziennikuj wyniki z Drive ID, nazwą, rozmiarem i SHA-256. Oryginalne assety, media, pełne surowe skany i staging pozostają w ignorowanym `google_drive/`; zatwierdzony eksport tekstów JSON, narzędzia i dokumentacja są śledzone w Git zgodnie z decyzją właściciela.
