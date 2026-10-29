# Instrukcje — The Genesis Order

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/EXPERIMENT_LOG.md` oraz `../../docs/WORKFLOW.md`.

## Bieżący etap

Statyczny audyt, eksport i korpus tłumaczeń są zakończone. Kanoniczny eksport w `translation/export-v1/` zawiera 45 229 rekordów. Zobacz `docs/HANDOFF_NEXT_AGENT.md`, `docs/STATUS.md`, `docs/COVERAGE_AUDIT.md` i `docs/RECOVERY_2026-10-29.md` przed dalszymi zmianami. **Stan tłumaczenia (odzyskany i zweryfikowany 2026-10-29):** wszystkie **427** partie scalone dają **39 926** niepustych tłumaczeń, **131** chronionych `keep_source_value`, **5 172** świadomie zachowanych w źródle, **0** nierozstrzygniętych rekordów i **0** konfliktów; `tools/audit_translation_coverage.py` raportuje `status: complete`. Milestone’y: patch POC `v0.1.1` i Czytanka PL v1 w `translation/packages/`. Proza widoczna dla gracza jest wyczerpana — **nie twórz nowych partii map, żeby dobijać licznik**; 45 000 nie jest osiągalne bez tłumaczenia tokenów i nazw własnych. Wszystkie nie-rendererowe wiersze `401` i opcje `102` są zatwierdzone jako tekst gracza. Source ZIP v1 pozostaje śledzony w Git i publikowany na Google Drive. Tekst wtopiony w obrazy i wideo jest poza zakresem decyzją właściciela; partie są śledzone w `translation/drafts/`, eksport źródłowy pozostaje niezmieniony. Kolejne zadania są redakcyjne: decyzje z `docs/EDITORIAL_DECISIONS.md` (tytuł gry, `Channel 4`, etykiety map, warianty craftingu i telefonu), redakcja/QA draftów, testy fontów i instalacji na kopii gry Windows. **Nie uruchamiaj gry ani jej kodu.** Tagi czcionek bez argumentu (`\fb`) obsługuje `translation_tokens_match()` — ADR 002 wariant B.

## Zasady dla TGO

- **ZAKAZ MT poza LLM (ADR 2026-10-29): ZABRONIONE jest automatyczne maszynowe tłumaczenie słownikowe/auto_translate poza LLM.** Wszystkie drafty TGO muszą być tłumaczone **wyłącznie przez LLM w kontekście sceny** (mapa/event/mówca/sąsiednie kwestie), **wolno ale dokładnie, z korektą**, z zachowaniem `1Hero` i terminologii (Toma/Anachorismos/Daemalius/Lilith). Partie `map*-auto-01` (7 200 draftów, commit 5539dc3) zostały odrzucone decyzją właściciela 2026-10-29: „Nie było zgody na tłumaczenie maszynowe. Wszystko miało być tłumaczone przez LLM w kontekście.” i zrewertowane (440217e). Każde użycie automatu wymaga revertu, bez względu na presję na liczbę 45 000.
- Nie proś o całą instalację ani media. Użytkownik przesłał już tekstowe dane, JS i fonty.
- Nie uruchamiaj kodu gry ani skryptów JS z instalacji; czytaj JSON bezpiecznym parserem, a JS analizuj statycznie. Nie nadpisuj oryginałów, zapisów ani ustawień.
- Licz osobno bloki dialogów, linie kontynuacji, opcje wyboru, UI/bazy danych i teksty w skryptach/pluginach. Nie sumuj ich bez wyjaśnienia i nie traktuj każdej linii skryptu jako tekstu do tłumaczenia.
- Czytanka musi zachować mapę/label, identyfikator sceny, mówiącego, kolejność, wybory, warunki i wywołania common events. RPG Maker jest rozgałęziony; nie zakładaj jednej kanonicznej chronologii. Oznacz gałęzie i warunki zamiast zgadywać.
- Zapisuj niepewność, duplikaty, dynamiczne stringi i miejsca wymagające testu. TGO jest wybranym projektem; rozwijaj pełny workflow, ale każdą niepotwierdzoną klasyfikację oznaczaj zamiast zgadywać.
- Dziennikuj wyniki z Drive ID, nazwą, rozmiarem i SHA-256. Tylko binarne assety gry pozostają poza Git. Wszystkie narzędzia, tekstowe dane źródłowe i każdą partię tłumaczeń, także roboczą, śledź w Git; `google_drive/` jest opcjonalną kopią/warsztatem, nie jedynym miejscem zapisu.
