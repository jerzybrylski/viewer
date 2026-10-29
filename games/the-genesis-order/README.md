# The Genesis Order — lokalizacja PL

Wybrany projekt lokalizacyjny. Potwierdzono RPG Maker MV 1.6.1 + NW.js. Praca obejmuje statyczny audyt źródeł, stabilny eksport tekstu, branch-aware kontekst, bezpieczny importer oraz późniejszy patcher Windows.

## Bieżący stan

- Kanoniczne JSONL ze stabilnymi ID: [`translation/export-v1/`](translation/export-v1/), **45 229 rekordów**, wszystkie kontrolne liczniki pokrycia przechodzą.
- Statyczny JS audit: 78 plików, 563 kandydatury, 35 potwierdzonych statycznych powierzchni UI, 528 wykluczeń z jawnym powodem, 0 otwartych.
- Wszystkie nie-rendererowe wiersze `401` oraz wszystkie opcje `102` są pełnoprawnym tekstem gracza do tłumaczenia, zgodnie z decyzją właściciela. Szczegółowe liczniki znajdują się w [`docs/STATUS.md`](docs/STATUS.md) i [`docs/COUNT_REPORT.md`](docs/COUNT_REPORT.md).
- Source ZIP v1 zawiera pełny zatwierdzony statyczny zakres i jest śledzony w Git; kopia jest publikowana na Google Drive. Ostatnie pełne scalenie step11 obejmuje 20 610 niepustych tłumaczeń, 131 rekordów chronionych i 24 488 tłumaczalnych pól oczekujących. Po step11 dodano 12 105 unikalnych, osobnych draftów w 106 plikach; projekcja wynosi 32 715 niepustych tłumaczeń. Bieżący cel to 45 000, ale liczymy wyłącznie faktyczny tekst widoczny dla gracza; wcześniejszy teoretyczny pułap po wyłączeniu wartości chronionych i tokenów sterujących wynosi 41 356, więc osiągnięcie celu nie jest gwarantowane. Drafty wymagają redakcji. Nie uruchomiono gry ani kodu gry i nie ma patcha.

## Dane i granice Gita

Repozytorium śledzi narzędzia, dokumentację, tekstowe dane źródłowe i wszystkie robocze tłumaczenia, w tym [`translation/drafts/`](translation/drafts/). Binarne assety gry są poza Git. Ignorowany `google_drive/` służy m.in. do tymczasowego bezpiecznego stagingu; nie zastępuje Git jako miejsca przechowywania pracy.

## Odtwarzanie

Oryginalne assety źródłowe muszą być lokalnie dostępne w ignorowanym `google_drive/the-genesis-order/`.

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/build_translation_package.py
```

Eksporter weryfikuje zatwierdzony JS JSONL z `google_drive/the-genesis-order/translation/export-v1/reviewed_js_ui.jsonl` i zapisuje kanoniczny eksport w repo. Markdown domyślnie powstaje pod śledzonym `translation/`; staging kopii gry pod `google_drive/`.

## Dokumentacja projektu

- [Status i pokrycie](docs/STATUS.md)
- [Handoff dla kolejnego agenta](docs/HANDOFF_NEXT_AGENT.md)
- [Roadmapa i bramki](docs/ROADMAP_TRANSLATION.md)
- [Format JSONL i write-back](docs/TRANSLATION_FORMAT.md)
- [Zasady tłumaczenia](docs/TRANSLATION_POLICY.md)
- [Raport census](docs/COUNT_REPORT.md)
- [Ustalenia techniczne](docs/TECHNICAL_FINDINGS.md)
- [Dziennik eksperymentów](docs/EXPERIMENT_LOG.md)
