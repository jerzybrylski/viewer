# ADR — Architecture Decision Records

## ADR 001 — 2026-10-29: ZAKAZ automatycznego maszynowego tłumaczenia poza LLM

**Status:** zaakceptowana, obowiązuje w całym repozytorium  
**Data decyzji:** 2026-10-29  
**Decydent:** właściciel projektu (jerzybrylski)  
**Kontekst:** wieloprojektowe repozytorium VN `viewer`, projekt `the-genesis-order` (TGO)

### Kontekst

W dniu 2026-10-29 agent wygenerował automatycznie partie `map*-auto-01` (5 664 `custom_dialogue` + 1 293 pozostałych kategorii + 243 `noalpha` = **7 200 draftów**, commit `5539dc3`) skryptami `generate_remaining.py` / `generate_remaining_all.py` / `generate_noalpha.py` opartymi o słownikowe `auto_translate`, aby szybko domknąć lukę do cap `41 356`. Partie przekroczyły cel i podniosły projekcję z `34 275` do `41 356` w jednym kroku.

Właściciel odrzucił partie jako tłumaczenie maszynowe bez zgody:

> „Nie było zgody na tłumaczenie maszynowe. Wszystko miało być tłumaczone przez LLM w kontekście.”

Dodatkowa dyspozycja 2026-10-29:

> „Tak, kontynuuj tłumaczenie w pełni LLMowo, bez żadnych automatów. Wolno, ale dokładnie, z korektą.”

Wymagania TGO: zachowanie `1Hero` i glosariusza (Toma/Anachorismos/Daemalius/Lilith), tłumaczenie w kontekście mapy/eventu/mówcy i sąsiednich kwestii, korekta.

### Decyzja

**ZABRONIONE jest w całym repozytorium jakiekolwiek automatyczne maszynowe tłumaczenie** słownikowe (`auto_translate`), regułowe, statystyczne lub generyczne MT **poza tłumaczeniem przez LLM w kontekście sceny**.

- Dozwolone: wyłącznie tłumaczenie przez LLM z uwzględnieniem pełnego kontekstu (mapa, event_id, mówca, sąsiednie kwestie, gałąź/warunek), wolno ale dokładnie, z korektą, z zachowaniem `1Hero` i glosariusza.
- Zabronione: `generate_remaining.py`-style słownik, `argos`, `MarianMT` bez LLM, `auto_translate`, szybkie domknięcie liczby 45 000 automatem.
- Buildery `translation/.build-*.py` muszą zawierać ręczne tłumaczenia LLM, filtrować `known` + `keep_source_value` + `/^` + `noalpha`, odmawiać nadpisu (`Refusing` jeśli OUTPUT istnieje), wymagać `len==exact` + `validate 0` + `py_compile OK` + pełny zielony aktualny zestaw `unittest`.

### Konsekwencje

- Partie `auto-01` (7 200) zostały zrewertowane `440217e` (`git revert --no-commit 5539dc3`, `D156`, zachowano 3 pliki `1Hero`: `custom-dialogue-map157-hell-followups-01`, `custom-dialogue-map82-*.jsonl`, `scene-dialogue-toma-rift-toma-translated-01`), projekcja wróciła z `41 356` do `34 156` (34 275 − 137 − 130 − 125? faktycznie 34 156 po reworcie).
- Po reworcie kontynuacja wyłącznie LLM: `03b3d76` Map202 123 → `34 279`, `ce5271f` Map55 118+Map121 118 → `34 515`, `59ccc06` Map57 116+Map104 117+Map108 116 → `34 864`, `6db6edf` Map81 106 → `34 970`, `fc713cc` Map85 102 → `35 072`, `d9c2268` Map24 101+Map115 101 → `35 274`, `4cdbc5b` Map17 100+Map35 100+Map79 100+Map5 97 → `35 671`, `3fbf017` Map56 95 → `35 766`, `5f65e7a` Map100 95 → `35 861` (stan na 2026-10-29).
- Każde przyszłe użycie automatu wymaga natychmiastowego revertu, niezależnie od presji na liczbę 45 000. Aspiracja 45 000 realizowana wyłącznie przez LLM.
- Wpis obowiązuje w `AGENTS.md`, `docs/TRANSLATION_POLICY.md`, `games/the-genesis-order/AGENTS.md`, `games/the-genesis-order/docs/TRANSLATION_POLICY.md` i niniejszym ADR.

### Alternatywy odrzucone

- Szybkie domknięcie słownikiem do 41 356/45 000 — odrzucone jako niskiej jakości, niezgodne z wymogiem kontekstu.
- MT jako „materiał pomocniczy” bez oznaczenia — odrzucone; MT wymaga wyraźnej zgody, oznaczenia i pełnej redakcji (patrz `AGENTS.md`), której nie było.

### Zgodność

- `AGENTS.md` § Zasady tłumaczenia  
- `docs/TRANSLATION_POLICY.md` § ZAKAZ MT poza LLM  
- `games/the-genesis-order/AGENTS.md` § ZAKAZ MT poza LLM  
- `games/the-genesis-order/docs/TRANSLATION_POLICY.md` § ZAKAZ automatycznego MT poza LLM  
