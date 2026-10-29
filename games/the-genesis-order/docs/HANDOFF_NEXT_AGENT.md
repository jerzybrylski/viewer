# Handoff dla kolejnego agenta — The Genesis Order

Stan: 2026-10-29, po odzyskaniu pracy poprzedniego agenta. **Wszystko, co było warte odzyskania, jest w Git** i sprawdzone niezależnie od twierdzeń poprzednika — raport: [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).

**POTWIERDZONE liczby:** 45 229 rekordów kanonicznych, **427** partii draftów, **39 926** niepustych tłumaczeń, **131** jawnie chronionych `keep_source_value`, **5 172** świadomie zachowanych w źródle, **0** nierozstrzygniętych, **0** konfliktów. Bramka `tools/audit_translation_coverage.py` → `status: complete`. Kubełki pustych rekordów: [`COVERAGE_AUDIT.md`](COVERAGE_AUDIT.md).

**Nie zaczynaj od tłumaczenia nowych rzeczy.** Statyczna proza widoczna dla gracza jest wyczerpana. Następna wartość jest w redakcji, testach i decyzjach właściciela.

## Stan repo i artefaktów

- Pracuj na gałęzi bieżącej sesji Arena; nie zmieniaj gałęzi. Commit i push po każdym zamkniętym etapie — poprzedni agent stracił pracę, bo tego nie robił.
- Kanoniczny eksport: `translation/export-v1/`, 45 229 rekordów, 25 JSONL + manifest. Wszystkie wiersze `401` poza rendererami oraz wszystkie opcje `102` są zatwierdzone jako pełnoprawny tekst gracza.
- Partie: `translation/drafts/` (427 plików, także podkatalogi — czytaj **rekurencyjnie**), buildery `.build-*.py` (259) w `translation/`.
- Source ZIP v1: `translation/packages/TGO_source_translation_package_v1.zip` (+ `.sha256`), publikowany też na Drive.
- Patch POC: `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip` (+ `.sha256`), 39 926 tłumaczeń, 238 fingerprintów, backup/rollback. Jego `payload/translations.jsonl` odtwarza się **bajt w bajt** ze scalenia draftów (`e2898d6f…`).
- Czytanka PL v1: `reading/v1/` (4 394 epizody, 55 mówców, 291 lokacji, 221 osiągalnych statycznie) + ZIP `TGO_readalong_PL_v1.zip`.
- Oryginały gry: Google Drive `TGO/www/data/` (306 plików). Lokalnie brak — brak pliku nie oznacza braku uploadu; nie proś właściciela o ponowny upload.
- **Nie uruchamiaj gry ani jej kodu** (JS ani `.exe`). JSONL czytaj bezpiecznymi parserami. Nie nadpisuj cudzych zmian.
- Polecenia weryfikacyjne:

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -q
python3 games/the-genesis-order/tools/audit_translation_coverage.py
python3 games/the-genesis-order/tools/audit_draft_coverage.py --quiet --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md
python3 games/the-genesis-order/tools/markdown_translation.py import --check
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
```

## Reguły, których nie wolno łamać

- ADR 001: **żadnego automatycznego MT** poza LLM w kontekście sceny. Każdy builder zawiera ręczne tłumaczenia; filtr `known` + `keep_source_value` + `/^` + `noalpha`, `len==exact`, `validate 0`, `py_compile OK`, pełny zielony zestaw testów, odmowa nadpisania istniejącego pliku.
- ADR 002 (wariant B, przyjęty): `translation_tokens_match()` normalizuje kody czcionek bez argumentu (`\fb`, `\fi`, `\fr`) gdy następuje po nich litera. **Nie zmieniaj `export-v1/`**, żeby „naprawić” tokeny — to już niepotrzebne.
- Nigdy nie uruchamiaj `.build-*.py` na istniejącym pliku wyjściowym. Test determinizmu rób na kopii katalogu draftów.

## Następne zadania (w tej kolejności)

1. **Decyzje redakcyjne właściciela** — [`EDITORIAL_DECISIONS.md`](EDITORIAL_DECISIONS.md), 11 pozycji z rekomendacjami. Najpilniejsze: tytuł gry („Zakon Genesis” vs oryginał), `Channel 4`, `TEXT`/`TEKST` (ryzyko klucza w kodzie gry), placeholdery TEST MAP.
2. **Testy fontów i instalacji** (największe ryzyko projektu): czy czcionki gry mają polskie glify, jak łamie się długi tekst, czy patcher działa na kopii buildu Windows. Bez tego reszta jest teoretyczna.
3. **Redakcja językowa 39 926 draftów** po stabilnym `id`: spójność z glosariuszem (Toma/Anachorismos/Daemalius/Lilith zachowane), długości linii, powtarzalne powiedzenia, odmiana. Audyt wykazuje 617 tłumaczeń identycznych ze źródłem — po odfiltrowaniu imion i wykrzyknień zostaje 37 wielowyrazowych, wszystkie to nazwy własne i linki.
4. **31 rekordów w kubełku `needs_review`** (28 w audycie draftów + 3 nazwy z odzyskanych partii) — przejrzeć po jednym, nie tłumaczyć hurtem.
5. **Ponowna budowa artefaktów po redakcji**: `build_standalone_patch.py`, `build_readalong.py` (ok. 9 s), aktualizacja `.sha256` i wpis w `EXPERIMENT_LOG.md`.
6. Dopiero potem: publikacja/dystrybucja. Source ZIP i patch POC to nie jest zatwierdzona dystrybucja.

## Czego nie robić

- Nie odtwarzać ponownie odzyskiwania z patcha/ZIP-ów — zrobione i udowodnione (`RECOVERY_2026-10-29.md`).
- Nie wracać do `translation/pending/` ani `tools/markup_signature.py` — usunięte, zastąpione regułą walidatora.
- Nie scalać draftów na dysk bez potrzeby: pełny merge to plik 57 MB, który jest w pełni odtwarzalny.
- Nie dopisywać do `EXPERIMENT_LOG.md` historii wstecz — nowe wpisy dopisuj na końcu.
