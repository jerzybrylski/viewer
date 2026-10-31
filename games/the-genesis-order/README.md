# The Genesis Order — lokalizacja PL

Projekt lokalizacyjny RPG Maker MV 1.6.1 + NW.js. Statyczny audyt i przekład kwalifikującego się tekstu są zakończone; standalone patch i branch-aware Czytanka są zbudowane jako proof of concept. Testy w runtime/Windows pozostają do wykonania.

## Bieżący stan

- Kanoniczne JSONL ze stabilnymi ID: [`translation/export-v1/`](translation/export-v1/), **45 229 rekordów**, wszystkie kontrolne liczniki pokrycia przechodzą.
- Statyczny JS audit: 78 plików, 563 kandydatury, 35 potwierdzonych statycznych powierzchni UI, 528 wykluczeń z jawnym powodem, 0 otwartych.
- Wszystkie nie-rendererowe wiersze `401` oraz opcje `102` zostały uwzględnione w przekładzie; tekst wtopiony w obrazy i wideo jest poza zakresem.
- Merge wszystkich **427** draftów: 45 229 rekordów, **39 917 tłumaczeń**, 131 jawnie chronionych, 5 181 zachowane nielokalizowalne i 0 nierozstrzygniętych; bez konfliktów. Raport: [`translation/reports/coverage_audit_v1.json`](translation/reports/coverage_audit_v1.json).
- **Pomiar z draftów (odtwarzalny):** `tools/audit_draft_coverage.py` czyta wszystkie **427** plików `translation/drafts/`, także `hints/`, `ui-01/` i `follow-ups/`, i porównuje je z kanonicznym eksportem — te same liczby, **0** konfliktów i **0** nierozstrzygniętych. Bramka `tools/audit_translation_coverage.py` raportuje `status: complete`. Rozkład pustych rekordów (komendy, nazwy własne, czysty markup): [`docs/COVERAGE_AUDIT.md`](docs/COVERAGE_AUDIT.md).
- Aspiracja 45 000 jest zamknięta jako nieosiągalna bez tłumaczenia tokenów sterujących i nazw własnych — pozostałe puste rekordy są techniczne, nazwowe albo chronione. Drafty wymagają redakcji; gry nie uruchamiano.

## Artefakty

- Standalone patch POC: [`translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip`](translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip) z one-click patcherem i backup/restore; bez plików gry. Nie testowano Windows/runtime. Jego payload odtwarza się bajt w bajt ze scalenia draftów.
- Czytanka PL v1: [`reading/v1/`](reading/v1/) i [`translation/packages/TGO_readalong_PL_v1.zip`](translation/packages/TGO_readalong_PL_v1.zip); 4 394 epizody, indeksy 55 mówców i 291 lokacji, 221/291 potencjalnie osiągalnych map w statycznym BFS. Kolejność nie jest kanoniczna.
- Source ZIP v1: [`translation/packages/TGO_source_translation_package_v1.zip`](translation/packages/TGO_source_translation_package_v1.zip) — pełny zatwierdzony statyczny zakres, kopia publikowana na Google Drive.
- Wstawki wideo: statyczny skaner [`tools/scan_movie_calls.py`](tools/scan_movie_calls.py) i tryb `--movie-calls` w [`tools/build_readalong.py`](tools/build_readalong.py) dodają do Czytanki znaczniki `🎬 Wstawka wideo` oraz `index_movies_PL.md` w katalogu wydania Czytanki. **Wymaga jednorazowego skanu `www/data` z instalacji**; do tego czasu znaczniki nie są jeszcze wstawione. Skan lokalny: [`tools/intake/INSTRUKCJA_WIDEO.txt`](tools/intake/INSTRUKCJA_WIDEO.txt).

## Dane i granice Gita

Repozytorium śledzi narzędzia, dokumentację, tekstowe dane źródłowe i wszystkie robocze tłumaczenia, w tym [`translation/drafts/`](translation/drafts/). Binarne assety gry są poza Git. Ignorowany `google_drive/` służy m.in. do tymczasowego bezpiecznego stagingu; nie zastępuje Git jako miejsca przechowywania pracy.

## Odtwarzanie

Źródła statyczne do odtworzenia patcha i Czytanki muszą być dostępne w ignorowanym `google_drive/tgo_source/`. Bez nich `reading/v1/` i patch nie odbudują się — dlatego gotowe wyniki są śledzone.

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/build_translation_package.py
python3 games/the-genesis-order/tools/audit_translation_coverage.py
python3 games/the-genesis-order/tools/audit_draft_coverage.py --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md
python3 games/the-genesis-order/tools/build_standalone_patch.py
python3 games/the-genesis-order/tools/scan_movie_calls.py --data-dir google_drive/tgo_source --out /tmp/tgo_movie_calls.json
python3 games/the-genesis-order/tools/build_readalong.py --movie-calls /tmp/tgo_movie_calls.json
```

Eksporter weryfikuje zatwierdzony JS JSONL z `google_drive/the-genesis-order/translation/export-v1/reviewed_js_ui.jsonl` i zapisuje kanoniczny eksport w repo. Markdown domyślnie powstaje pod śledzonym `translation/`; staging kopii gry pod `google_drive/`.

## Dokumentacja projektu

- [Status i pokrycie](docs/STATUS.md)
- [Handoff dla kolejnego agenta](docs/HANDOFF_NEXT_AGENT.md)
- [Roadmapa i bramki](docs/ROADMAP_TRANSLATION.md)
- [Decyzje redakcyjne do zatwierdzenia](docs/EDITORIAL_DECISIONS.md)
- [Odzyskiwanie pracy (2026-10-29)](docs/RECOVERY_2026-10-29.md)
- [Audyt pokrycia draftów](docs/COVERAGE_AUDIT.md)
- [Format JSONL i write-back](docs/TRANSLATION_FORMAT.md)
- [Zasady tłumaczenia](docs/TRANSLATION_POLICY.md)
- [Raport census](docs/COUNT_REPORT.md)
- [Ustalenia techniczne](docs/TECHNICAL_FINDINGS.md)
- [Dziennik eksperymentów](docs/EXPERIMENT_LOG.md)
