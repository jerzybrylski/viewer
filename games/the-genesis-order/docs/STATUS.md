# Status — The Genesis Order

**Stan: audyt statycznych powierzchni i kanoniczny eksport zakończone; źródłowy ZIP v1 został utworzony i sprawdzony.** To nie jest patch gry ani przetłumaczona dystrybucja. Aktualizacja: 2026-10-29.

## Wynik bieżący

- Kanoniczny, śledzony w Git eksport: `games/the-genesis-order/translation/export-v1/`, **45 229 rekordów**, 25 JSONL i `export_manifest.json`; wszystkie kontrolne liczniki pokrycia przechodzą.
- Wcześniejszy `apply_translation.py --check`: **45 229/45 229** rekordów oraz hashe **238** plików źródłowych zweryfikowane, bez zapisu i bez uruchomienia kodu gry. Nie udało się odtworzyć tej kontroli w bieżącej sesji, bo ignorowany `google_drive/the-genesis-order/data/CommonEvents.json` nie jest obecny.
- Markdown: **497 dokumentów / 45 229 rekordów**. Source ZIP: `google_drive/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; hash w sąsiednim `.sha256`. ZIP integrity OK; assetów źródłowych ani kodu gry nie dołączono.
- Pakiet obejmuje canonical JSONL, kontekstowy Markdown, instrukcję PL, manifest, glossary/politykę i raport zakresu. To kompletny statyczny pakiet źródłowy z jawnie oznaczonymi niepewnościami, nie patch i nie finalna dystrybucja.
- Pełne testy przed dodaniem buildera pakietu: **27/27 passed**. Po dodaniu `build_translation_package.py` należy ponownie uruchomić testy i `--check` buildera.
- Pola `translation` są puste. Nie rozpoczęto tłumaczenia, nie zbudowano patchera Windows i nie uruchamiano gry/runtime.

## Pokrycie

| Powierzchnia / kategoria | Rekordy | Uwagi |
|---|---:|---|
| Customowy dialog CE60 | 38 638 | 29 647 różnych payloadów; tekst oddzielony statycznie od nagłówka. |
| Arianna hints | 705 | Potwierdzony przepływ przez CE222. |
| Telefon | 30 | 17 wartości skryptowych + 13 natywnych wierszy CE54; osobno od UI listy. |
| UI listy telefonu CE17 | 378 | Widoczne pozycje UI, nie klasyfikowane jako dialog. |
| Etykiety znalezionych przedmiotów | 649 | Statyczne wartości V[107] renderowane przez CE223. |
| Obrazowe podpisy CE224 | 134 | 67 statycznych wywołań; dwie komendy 401 to scaffolding renderera. Tekst w samych obrazach nie jest analizowany. |
| Natywne wiersze 401 poza rendererami | 1 513 | Wszystkie zachowane jako widoczne powierzchnie: 1 122 bez ustalonego semantycznego podtypu, 378 UI telefonu, 13 natywnych tekstów telefonu. Osiem rendererów pominiętych. |
| Wybory 102 | 2 110 | 695 grup; 180 znanych opcji UI, 1 930 bez zgadywania podtypu fabuła/UI. |
| Statyczne wartości zmiennych przez `\\V[...]` | 262 | 134 tekstowe/statusowe tłumaczalne; 61 cen + 67 markerów chronionych. 132 whitespace-only wartości pominięte jako layout. |
| Potwierdzone UI JS | 35 | 4 engine-static, 9 parametrów pluginów, 22 static plugin UI; skan 78 plików: 563 kandydatury, 528 wykluczeń, 0 nierozstrzygniętych. |

Pozostałe kategorie obejmują 239 niepustych linii Credits, 291 nazw map, 28 nazw aktorów, 477 nazw przedmiotów oraz 131 rekordów System. W pakiecie jest **131 chronionych wartości** łącznie (128 cen/markerów + 3 etykiety Lovense używane przez logikę).

## Audyt dodatkowych kanałów

- Wszystkie 563 kandydatury JS otrzymały decyzję: 35 potwierdzonych UI, 528 wykluczeń z jawnym content-free powodem, 0 odroczonych i 0 nierozstrzygniętych. Wykluczenia to wartości kodu/konfiguracji/markup bez dowodu UI w danym locatorze, nie „wiadomości techniczne”.
- Statyczny przegląd event scripts objął alerty, błędy Graphics, komunikaty/opcje/drawText i przepływ Lovense. Poza śledzonymi kanałami nie wykryto dodatkowych statycznych literałów przy sinkach wiadomości/opcji/drawText w kodach 355/655.
- 1 570 plugin commands sklasyfikowano jako sterowanie/parametry: AnimationCurve 1 321, MessageWidth 156, MessageRows 42, Play2ndBGS 17, Fadeout2ndBGS 4 i steamworks 30.
- Zbadano 34 pola `Items.note`: tagi/metadane, bez prozy. Nazwy assetów, media i editor-only labels nie są źródłowym tekstem pakietu.
- Lovense: widoczne `PC`/`LAN`/`Web` pozostają chronione jako runtime-operandy, `Not Connected` jest tłumaczalne. Nazwy urządzeń/nicknames to dynamiczne dane zewnętrzne.

## Jawne niepewności i dalsze prace

- **1 122** natywne wiersze `401` i **1 930** opcji są potwierdzonymi powierzchniami, ale nie mają przypisanego semantycznego podtypu (dialog/tutorial/powiadomienie/UI). Nie pominięto ich z ZIP-a. Można je dodatkowo sklasyfikować przed przydziałem tłumaczom, jeśli właściciel tego wymaga.
- Tekst osadzony w obrazach/audio/wideo, runtime’owe nazwy urządzeń/użytkowników i obliczane liczby nie są statycznymi źródłami lokalizacyjnymi.
- Źródłowy język i konkretny build nie są formalnie potwierdzone. Nie ma polskiej zwrotki, testów fontów/łamania w runtime, instalatora ani patcha.
- ZIP v1 to source package; nie zmienia gry i nie jest finalną paczką spolszczenia. Oryginalne assety/staging pozostają ignorowane; JSONL, dokumentacja i narzędzia są śledzone w Git.

## Odtwarzanie

```bash
python3 -m unittest discover -s games/the-genesis-order/tests -v
python3 games/the-genesis-order/tools/export_translation.py
python3 games/the-genesis-order/tools/markdown_translation.py build --replace
python3 games/the-genesis-order/tools/apply_translation.py --input games/the-genesis-order/translation/export-v1 --check
python3 games/the-genesis-order/tools/markdown_translation.py import --check
python3 games/the-genesis-order/tools/build_translation_package.py
```

Szczegółowe liczniki: [`COUNT_REPORT.md`](COUNT_REPORT.md). Format rekordów: [`TRANSLATION_FORMAT.md`](TRANSLATION_FORMAT.md). Następne zadania: [`HANDOFF_NEXT_AGENT.md`](HANDOFF_NEXT_AGENT.md).
