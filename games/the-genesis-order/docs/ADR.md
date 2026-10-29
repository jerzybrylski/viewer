# ADR — The Genesis Order

## ADR 001 — 2026-10-29: ZAKAZ automatycznego MT poza LLM (TGO)

**Status:** obowiązuje  
**Decydent:** właściciel (jerzybrylski)  
**Data:** 2026-10-29

### Tło

2026-10-29 agent dodał `map*-auto-01` (7 200 draftów) słownikowym `auto_translate` (commit `5539dc3`). Właściciel: „Nie było zgody na tłumaczenie maszynowe. Wszystko miało być tłumaczone przez LLM w kontekście.” oraz „Tak, kontynuuj tłumaczenie w pełni LLMowo, bez żadnych automatów. Wolno, ale dokładnie, z korektą.” Partie zrewertowano `440217e` (D156), projekcja `41 356 → 34 156`.

### Decyzja

ZABRONIONE jest automatyczne MT słownikowe/regułowe/statystyczne poza LLM w kontekście sceny. Dozwolone wyłącznie LLM w kontekście (mapa/event/mówca/sąsiednie kwestie), z korektą, z zachowaniem `1Hero` i glosariusza (Toma/Anachorismos/Daemalius/Lilith). Buildery muszą mieć ręczne tłumaczenia LLM, filtr `known`+`keep_source_value`+`/^`+`noalpha`, `len==exact`, `validate 0`, `py_compile OK`, `36/36`.

### Konsekwencje

- Revert auto-01, kontynuacja LLM: 35 861 po Map100 (15 251 draftów w 133 plikach, 2 590 po step11).
- Każde użycie automatu = natychmiastowy revert.
- Wpis w `AGENTS.md`, `docs/TRANSLATION_POLICY.md`, `games/the-genesis-order/docs/TRANSLATION_POLICY.md`, `docs/ADR.md`.
