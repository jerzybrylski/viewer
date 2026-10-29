# Zasady lokalizacji — The Genesis Order

## Stan

Eksport źródłowy znajduje się w `games/the-genesis-order/translation/export-v1/` i pozostaje bez zmian. Wszystkie 427 draftów scalają się bez konfliktów: 39 926 niepustych tłumaczeń, 131 jawnie chronionych wartości, 5 172 zachowane rekordy nielokalizowalne i 0 nierozstrzygniętych rekordów do tłumaczenia. Audyt nie wykazał dalszych zwykłych fraz gracza do tłumaczenia; pozostałe ryzyka to redakcja i testy wyświetlania. Source ZIP v1 jest pakietem źródłowym; osobno zbudowano patch POC oraz Czytankę v1. Żaden artefakt nie został zweryfikowany w Windows/runtime.

## Zasady wejściowe

- Tłumaczyć tylko rekordy z kanonicznego JSONL po ich `id`; nie zmieniać ID, `source_text`, hashy, locatorów ani kontekstu.
- Przed tłumaczeniem obejrzeć kategorię, warunki strony, gałąź, sąsiednie wybory i `visibility_evidence`. `confirmed_text_surface` dowodzi, że tekst jest widoczny, ale nie przesądza, czy to dialog, tutorial, komunikat, czy UI.
- Zachować dokładnie wszystkie tokeny w `markup_tokens`, placeholdery RPG Maker, kolejność escape’ów, znaczniki HTML i formaty. Nie dopisywać ani nie usuwać placeholderów bez osobnej reguły/testu.
- Rekordy z `context.translation_policy=keep_source_value` muszą zachować źródło dokładnie. Dotyczy to między innymi cen/markerów i wartości będących operandami runtime; importer odrzuci zmienioną wartość.
- Nazwy, tytuły, ksywki i terminy fabularne wymagają wspólnego glosariusza oraz zatwierdzonej konwencji zapisu. Nie zakładamy odmiany, rodzaju ani relacji bez kontekstu.
- Nie normalizować wielkości liter, interpunkcji, spacji lub apostrofów automatycznie. Puste źródłowe placeholdery layoutowe są pominięte w eksporcie.

## ZAKAZ automatycznego MT poza LLM — ADR 2026-10-29

**Decyzja właściciela 2026-10-29: ZABRONIONE jest jakiekolwiek automatyczne maszynowe tłumaczenie (słownikowe `auto_translate`, regułowe, statystyczne) poza tłumaczeniem przez LLM w kontekście.**

- Odrzucone partie `map*-auto-01` (5 664 `custom_dialogue` + 1 293 pozostałych kategorii + 243 `noalpha` = **7 200 draftów**, commit `5539dc3`) jako tłumaczenie maszynowe bez zgody; zrewertowane `440217e` (`D156`, zachowano 3 pliki `1Hero`).
- Obowiązuje tryb: **„Tak, kontynuuj tłumaczenie w pełni LLMowo, bez żadnych automatów. Wolno, ale dokładnie, z korektą.”** — każdy rekord tłumaczony przez LLM z uwzględnieniem mapy/eventu/mówcy i sąsiednich kwestii, z korektą, z zachowaniem `1Hero` i glosariusza (Toma/Anachorismos/Daemalius/Lilith) oraz terminologii projektu.
- Buildery `translation/.build-*.py` muszą zawierać tłumaczenia LLM (nie generowane słownikowo), filtrować `known` + `keep_source_value` + `/^` + `noalpha`, odmawiać nadpisu (`Refusing` jeśli OUTPUT istnieje), wymagać `len==exact` + `validate 0` + `py_compile OK` + pełnego przejścia aktualnego zestawu `unittest`.
- Naruszenie zasady (użycie automatu dla przyspieszenia do 45 000) wymaga natychmiastowego revertu, niezależnie od liczby. Aspiracja 45 000 realizowana wyłącznie przez LLM.
- Dowód i data: decyzja ustna 2026-10-29, wpisana do `AGENTS.md` / `docs/TRANSLATION_POLICY.md` / `games/the-genesis-order/AGENTS.md` i ADR poniżej; partia MT oznaczona w `EXPERIMENT_LOG.md` jako odrzucona.

## Walidacja i bezpieczeństwo

- JSONL jest kanoniczny. Markdown w `translation/markdown-draft-v1/` jest widokiem roboczym po stabilnych ID, nie osobnym źródłem prawdy; robocze tłumaczenia zawsze śledź w Git.
- Przed stagingiem uruchomić testy i `apply_translation.py --check`. Import/patch trafia do nowej kopii pod ignorowanym `google_drive/`; nigdy nie nadpisuje assetów wejściowych.
- Nie uruchamiać gry ani JS przez narzędzia ekstrakcji/importu. Test renderingu i polskich fontów wymaga osobnej zgody oraz kopii gry.
- Wszystkie nie-rendererowe wiersze `401` i wszystkie opcje `102` są pełnoprawnym tekstem gracza do tłumaczenia, bez filtrowania według dialog/UI. To zatwierdzona decyzja zakresowa. Tekst wtopiony w obrazy i wideo pozostaje poza zakresem na decyzję właściciela.
- Source ZIP v1 zawiera pełny zatwierdzony statyczny zakres, a jego pola `translation` są puste: to nieaktualizowana paczka źródłowa, nie polskie tłumaczenie ani patch gry. Osobne robocze partie tłumaczeń są śledzone w `translation/drafts/`.

Nie kopiować tekstów SRW ani założeń o silniku/limitach SRW do TGO. Przenosić można jedynie ogólne rozwiązania organizacyjne i walidacyjne.
