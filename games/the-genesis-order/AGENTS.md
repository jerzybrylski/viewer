# Instrukcje — The Genesis Order

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz `../../docs/WORKFLOW.md`.

## Bieżący etap

Statyczny audyt i eksport są zakończone. Kanoniczny eksport w `translation/export-v1/` zawiera 45 229 rekordów. Zobacz `docs/HANDOFF_NEXT_AGENT.md`, `docs/STATUS.md` i `docs/COVERAGE_AUDIT.md` przed dalszymi zmianami. **Stan tłumaczenia (pomiar 2026-10-29, `tools/audit_draft_coverage.py`):** 39 821 unikalnych ID z niepustym tłumaczeniem, 5 277 pustych rekordów do rozstrzygnięcia, 131 chronionych wartości; dodatkowo 94 rekordy craftingu zablokowane sygnaturą markup v1 czekają w `translation/pending/` (ADR 002). Proza widoczna dla gracza jest wyczerpana — **nie twórz nowych partii map, żeby dobijać licznik**; 45 000 nie jest osiągalne bez tłumaczenia tokenów i nazw własnych. Wszystkie nie-rendererowe wiersze `401` i opcje `102` są zatwierdzone jako tekst gracza. Source ZIP v1 pozostaje śledzony w Git i publikowany na Google Drive. Tekst wtopiony w obrazy i wideo jest poza zakresem decyzją właściciela; partie są śledzone w `translation/drafts/`, eksport źródłowy pozostaje niezmieniony. Kolejne zadania: decyzja o ADR 002 i nazwach własnych, uzgodnienie 40 etykiet map (`Channel 4` wciąż po angielsku w `inventory-names-02`/`map-labels-01`), redakcja/QA istniejących draftów, a potem patcher Windows.

## Zasady dla TGO

- **ZAKAZ MT poza LLM (ADR 2026-10-29): ZABRONIONE jest automatyczne maszynowe tłumaczenie słownikowe/auto_translate poza LLM.** Wszystkie drafty TGO muszą być tłumaczone **wyłącznie przez LLM w kontekście sceny** (mapa/event/mówca/sąsiednie kwestie), **wolno ale dokładnie, z korektą**, z zachowaniem `1Hero` i terminologii (Toma/Anachorismos/Daemalius/Lilith). Partie `map*-auto-01` (7 200 draftów, commit 5539dc3) zostały odrzucone decyzją właściciela 2026-10-29: „Nie było zgody na tłumaczenie maszynowe. Wszystko miało być tłumaczone przez LLM w kontekście.” i zrewertowane (440217e). Każde użycie automatu wymaga revertu, bez względu na presję na liczbę 45 000.
- Nie proś o całą instalację ani media. Użytkownik przesłał już tekstowe dane, JS i fonty.
- Nie uruchamiaj kodu gry ani skryptów JS z instalacji; czytaj JSON bezpiecznym parserem, a JS analizuj statycznie. Nie nadpisuj oryginałów, zapisów ani ustawień.
- Licz osobno bloki dialogów, linie kontynuacji, opcje wyboru, UI/bazy danych i teksty w skryptach/pluginach. Nie sumuj ich bez wyjaśnienia i nie traktuj każdej linii skryptu jako tekstu do tłumaczenia.
- Czytanka musi zachować mapę/label, identyfikator sceny, mówiącego, kolejność, wybory, warunki i wywołania common events. RPG Maker jest rozgałęziony; nie zakładaj jednej kanonicznej chronologii. Oznacz gałęzie i warunki zamiast zgadywać.
- Zapisuj niepewność, duplikaty, dynamiczne stringi i miejsca wymagające testu. TGO jest wybranym projektem; rozwijaj pełny workflow, ale każdą niepotwierdzoną klasyfikację oznaczaj zamiast zgadywać.
- Dziennikuj wyniki z Drive ID, nazwą, rozmiarem i SHA-256. Tylko binarne assety gry pozostają poza Git. Wszystkie narzędzia, tekstowe dane źródłowe i każdą partię tłumaczeń, także roboczą, śledź w Git; `google_drive/` jest opcjonalną kopią/warsztatem, nie jedynym miejscem zapisu.
