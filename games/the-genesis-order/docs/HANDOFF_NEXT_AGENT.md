# Handoff dla kolejnego agenta — The Genesis Order

Stan na 2026-10-29. Ten dokument opisuje **otwarte zadania** i warunki kontynuacji; nie przygotowano ZIP-a.

## Gdzie jesteśmy

- Pracuj wyłącznie na gałęzi `arena/df0bbe3f-viewer` (status PR: `pr_open`). Nie zmieniaj ani nie twórz gałęzi.
- Kanoniczny eksport znajduje się w `games/the-genesis-order/translation/export-v1/`: **45 229 rekordów**, 25 JSONL + `export_manifest.json`. Kontrole manifestu przechodzą; ID są unikalne.
- Ostatnia walidacja: pełne `unittest` **27/27 passed**; `apply_translation.py --check`: 45 229 rekordów, 238 źródeł zweryfikowanych, bez zapisu; Markdown import-check: 45 229 rekordów, 0 brakujących ID.
- Szkic Markdown: 497 dokumentów / 45 229 rekordów w ignorowanym `google_drive/the-genesis-order/translation/markdown-draft-v1/` — **nie kopiować do Gita** (około 83 MB).
- Dokumentacja, narzędzia, decyzje kuratorskie i JSONL są staged w Git zgodnie z ostatnią decyzją właściciela. Oryginalne pliki gry, media, pełne skany i staging pozostają pod ignorowanym `google_drive/`. Nie commitowano ani nie pushowano.
- Nie uruchamiano gry ani kodu gry. Nie rozpoczęto tłumaczenia. Nie wygenerowano ZIP-a.

## Zakres, który został domknięty statycznie

- Skan 78 plików JS: 563 kandydatury = 35 potwierdzonych statycznych UI, 528 wykluczeń z jawnym powodem, 0 odroczonych i 0 nierozstrzygniętych. UI: 4 `ui.engine_static`, 9 `ui.plugin_parameter`, 22 `ui.plugin_static`.
- Kanały danych/skryptów są uwzględnione, m.in. CE60 (38 638 wpisów), CE222 (705), telefon (30), CE223 (649), CE224 (134 static captions) i Lovense. `PC`/`LAN`/`Web` są chronione jako wartości runtime; `Not Connected` pozostaje tłumaczalne.
- Dodano 262 niepuste statyczne wartości komendy 122 renderowane przez widoczne `\\V[...]`: 134 wpisy tekstowe/statusowe tłumaczalne i 128 chronionych (61 cen + 67 markerów). 132 whitespace-only wartości pominięto jako layout.
- Wszystkie 2 110 opcji wyboru i 1 513 nie-rendererowych wierszy 401 są uwzględnione jako powierzchnie tekstu. 34 pola `Items.note` zawierają tylko tagi/metadane; 1 570 plugin commands sklasyfikowano jako sterowanie/parametry, nie bezpośrednie teksty UI.
- Szczegóły i aktualne liczniki: `translation/export-v1/export_manifest.json`, `docs/STATUS.md`, `docs/COUNT_REPORT.md`, `docs/TRANSLATION_FORMAT.md`.

## Otwarte zadania — kolejność

### 1. Uzyskać decyzję właściciela o granicy semantycznej przed ZIP-em

- [ ] Uzgodnić, czy przed pakietem trzeba semantycznie podzielić **1 122** ogólne wiersze `401` i **1 930** opcji na dialog, tutorial, komunikat i UI. Wszystkie są już w JSONL; nierozstrzygnięty podtyp nie oznacza brakujących rekordów.
- [ ] Potwierdzić, czy media-embedded text ma pozostać poza zakresem (obrazy/audio/wideo), oraz czy dynamiczne nazwy urządzeń/użytkowników mają pozostać nietłumaczone. Obecny audyt traktuje je jako media albo zewnętrzne dane runtime, nie statyczne teksty źródłowe.
- [ ] Nie generować ZIP-a automatycznie. Przygotować go dopiero po wyraźnej akceptacji pokrycia i zakresu przez właściciela.

### 2. Ustalić zasady lokalizacji i rozpocząć tłumaczenie dopiero po akceptacji

- [ ] Potwierdzić język źródłowy i docelowy dla konkretnego builda oraz konwencje: imiona, odmiana/rodzaje, terminy, cenzura/ton i nazwy UI.
- [ ] Uzupełnić glosariusz i zasady w `docs/TRANSLATION_POLICY.md` oraz `docs/GLOSSARY.md` na podstawie decyzji właściciela, nie zgadywać.
- [ ] Rozpoczynać tłumaczenie po stabilnym `id` z `translation/export-v1`; nie zmieniać `source_text`, locatorów ani ID.
- [ ] Chronione rekordy `context.translation_policy=keep_source_value` muszą pozostać identyczne. Obejmują ceny/markery i wartości sterujące; walidatory JSONL i Markdown je odrzucają po zmianie.

### 3. Wykonać zwrotkę i QA tłumaczenia

- [ ] Po wypełnieniu tłumaczeń uruchomić Markdown import-check oraz `apply_translation.py --check`; zachować wszystkie tokeny/escape’y i rozliczyć braki, duplikaty oraz konflikty.
- [ ] Dodać testy na realnych, ale ograniczonych rekordach każdej używanej kategorii — szczególnie `event_script_expression`, `keep_source_value`, JS/pluginowe UI, template literal i wielowierszowe JSON — bez modyfikacji assetów wejściowych.
- [ ] Zachować staging wyłącznie w nowym katalogu pod ignorowanym `google_drive/`; nigdy nie nadpisywać oryginału.

### 4. Późniejszy patcher Windows

- [ ] Ustalić dokładny build/layout kopii użytkownika i politykę hashy; bieżące `versionId` nie jest potwierdzonym numerem wydania.
- [ ] Zaprojektować instalację lokalną z wykrywaniem kopii, backupem, atomowym zapisem, raportem i rollbackiem; rozważyć save’y/osiągnięcia.
- [ ] Testować najpierw na kopiach syntetycznych. Test w grze/Windows wymaga zgody i potwierdzenia wykonania przez właściciela.
- [ ] ZIP patchera/tłumacza jest osobną bramką; brak zgody oznacza brak archiwum.

## Bezpieczne polecenia odtworzenia

Źródłowe assety muszą istnieć lokalnie w ignorowanym `google_drive/the-genesis-order/`. Eksporter nie uruchamia kodu gry.

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/markdown_translation.py import --check
```

Po zmianach sprawdzić `git status`, `git diff --cached --check` oraz upewnić się, że żaden `google_drive/` ani ZIP nie trafił do stagingu. Nie kopiować tekstów SRW do TGO.
