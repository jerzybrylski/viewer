# The Genesis Order — lokalizacja PL

Wybrany projekt lokalizacyjny. Potwierdzono RPG Maker MV 1.6.1 + NW.js. Praca obejmuje statyczny audyt źródeł, stabilny eksport tekstu, branch-aware kontekst, bezpieczny importer oraz późniejszy patcher Windows.

## Bieżący stan

- Kanoniczne JSONL ze stabilnymi ID: [`translation/export-v1/`](translation/export-v1/), **45 229 rekordów**, wszystkie kontrolne liczniki pokrycia przechodzą.
- Statyczny JS audit: 78 plików, 563 kandydatury, 35 potwierdzonych statycznych powierzchni UI, 528 wykluczeń z jawnym powodem, 0 otwartych.
- Wiadomości i wybory są zachowane jako widoczne powierzchnie; nie przypisujemy fabularnego/UI podtypu bez dowodu. Szczegółowe liczniki znajdują się w [`docs/STATUS.md`](docs/STATUS.md) i [`docs/COUNT_REPORT.md`](docs/COUNT_REPORT.md).
- Testy, round-trip check, Markdown draft i dokumentacja są narzędziami workflow; nie uruchomiono gry ani kodu gry. Nie ma tłumaczeń, patcha ani ZIP-a.

## Dane i granice Gita

W repozytorium znajdują się narzędzia, testy, dokumentacja, decyzje kuratorskie i jawnie zatwierdzony eksport tekstów JSON. Oryginalne assety (`www/data/`, `www/js/`, fonty, media, archiwum) są poza Gitem, pod ignorowanym `google_drive/the-genesis-order/`. Nie kopiować całych assetów ani roboczego Markdown draft (ok. 83 MB) do repo. Staging i ewentualne tłumaczenia pozostają poza Gitem.

## Odtwarzanie

Oryginalne assety źródłowe muszą być lokalnie dostępne w ignorowanym `google_drive/the-genesis-order/`.

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
```

Eksporter weryfikuje zatwierdzony JS JSONL z `google_drive/the-genesis-order/translation/export-v1/reviewed_js_ui.jsonl` i zapisuje kanoniczny eksport w repo. Markdown i staging powstają pod `google_drive/`.

## Dokumentacja projektu

- [Status i pokrycie](docs/STATUS.md)
- [Handoff dla kolejnego agenta](docs/HANDOFF_NEXT_AGENT.md)
- [Roadmapa i bramki](docs/ROADMAP_TRANSLATION.md)
- [Format JSONL i write-back](docs/TRANSLATION_FORMAT.md)
- [Zasady tłumaczenia](docs/TRANSLATION_POLICY.md)
- [Raport census](docs/COUNT_REPORT.md)
- [Ustalenia techniczne](docs/TECHNICAL_FINDINGS.md)
- [Dziennik eksperymentów](docs/EXPERIMENT_LOG.md)
