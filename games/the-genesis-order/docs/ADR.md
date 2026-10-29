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

## ADR 002 — 2026-10-29: sygnatura markup v2 dla tagów bez argumentu (PROPOZYCJA)

**Status:** propozycja — **wymaga decyzji właściciela**. Nie zmieniono walidatora ani eksportu.
**Data:** 2026-10-29

### Problem (POTWIERDZONE)

Tokenizer v1 (`export_translation.TOKEN_RE`) zapisuje `\<słowo>` razem z tekstem, który następuje po nim bez separatora. Tag bez argumentu `\fb`, użyty jako przełącznik stylu przed treścią, jest więc pamiętany jako `\fbCraft` / `\fbYou`. `apply_translation.validate_record` wymaga identycznej listy tokenów w źródle i tłumaczeniu, więc każda polska wersja tych wiadomości jest odrzucana („Markup/token mismatch”).

- Dotyczy **94 z 45 229** rekordów, wszystkie `native_message`, mapa `Crafting` (Map 46): 47 × „Craft this item?” i 47 × „You have items missing from this recipe.”.
- Wszystkie 94 rekordy są do dziś puste; żaden istniejący draft nie zależy od tej sygnatury.
- `tokens_v2` różni się od v1 wyłącznie na tych 94 rekordach i wyłącznie przez rozdzielenie `\fb` od pierwszego słowa — potwierdza to `tools/markup_signature.py` i test `tests/test_markup_signature.py`.
- Gotowe zwrotki leżą w `translation/pending/crafting-ui-map46-01.jsonl` (nie w `drafts/`).

### Opcje

| Opcja | Zmiana | Koszt | Ryzyko |
|---|---|---|---|
| A. Eksport v2 | nowa wersja `export-v1` → `export-v2` z `markup_tokens` policzonymi `tokens_v2` dla 94 rekordów; v1 zostaje jako archiwum | przeliczenie 94 wierszy, nowy manifest, ponowny `apply_translation --check` | zmiana kanonicznego artefaktu; wymaga świadomej zgody |
| B. Reguła walidatora | `validate_record` dopuszcza jawne tagi bez argumentu (`\fb`) także wtedy, gdy v1 skleił je z tekstem | zmiana tylko w walidatorze + testy | dwa różne pojęcia tokenów (v1 w eksporcie, v2 w walidacji) — trzeba to jawnie udokumentować |
| C. Pozostawienie po angielsku | brak zmian | 0 | 94 widoczne w grze wiadomości pozostają po angielsku |

### Rekomendacja agenta

**Opcja A.** Jest jednorazowa, mierzalna (94 rekordy), nie zmienia zachowania walidatora i pozwala zachować jedno pojęcie tokenu w całym repo. Warunek: właściciel akceptuje powstanie `export-v2` i nowy manifest; source ZIP v1 pozostaje niezmieniony jako archiwum, a source ZIP v2 powstanie dopiero po zakończeniu tłumaczenia.

### Konsekwencje każdej decyzji

- Do czasu decyzji partie `drafts/` pozostają bez zmian, a licznik pokrycia pokazuje 39 821 niepustych tłumaczeń i 94 rekordy zablokowane, nie „brakujące”.
- Po decyzji A lub B: 94 rekordy przechodzą do `drafts/`, pokrycie rośnie do 39 915, a `docs/COVERAGE_AUDIT.md` przestaje pokazywać kubełek `blocked_by_signature`.
- Opcja C wymaga wpisania ograniczenia do dokumentacji wydania (znane ograniczenia patcha).
