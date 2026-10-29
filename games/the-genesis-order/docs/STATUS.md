# Status — The Genesis Order

**Stan: audyt i eksport zakończone; trwa robocze tłumaczenie wielu kategorii.** To nie jest patch gry ani przetłumaczona dystrybucja. Aktualizacja: 2026-10-29.

## Wynik bieżący

- Kanoniczny, śledzony w Git eksport: `games/the-genesis-order/translation/export-v1/`, **45 229 rekordów**, 25 JSONL i `export_manifest.json`; wszystkie kontrolne liczniki pokrycia przechodzą.
- `apply_translation.py --check` wcześniej zweryfikował **45 229/45 229** rekordów i hashe **238** plików źródłowych. W bieżącym workspace oryginały nie są zsynchronizowane, ale są na Google Drive (306 plików pod `TGO/www/data/`); brak lokalnego pliku nie oznacza braku uploadu.
- Markdown: **497 dokumentów / 45 229 rekordów**. Source ZIP: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; archiwum jest śledzone w Git i publikowane na Google Drive w `TGO/translation/packages/`. ZIP nie zawiera assetów źródłowych ani kodu gry.
- Pakiet obejmuje canonical JSONL, kontekstowy Markdown, instrukcję PL, manifest, glossary/politykę i raport zakresu. To pełny zatwierdzony pakiet statycznych tekstów źródłowych do tłumaczenia, nie patch ani gotowa polska dystrybucja.
- Pełne testy uruchomione 2026-10-29: **36/36 passed**, w tym nowy audyt piętnastu partii follow-upów gracza; builder sprawdza zgodność rekordów, coverage flag i integralność ZIP-a.
- Kanoniczny eksport i source ZIP pozostają źródłowe. Pełny audyt 2026-10-29 scalił wszystkie **424** pliki draftów i zweryfikował **45 229** rekordów: **39 820** niepustych tłumaczeń po ID, **131** rekordów chronionych i **5 278** pustych niechronionych pól. Wcześniejsza projekcja 39 931 była zawyżona o 111 przez powtórzone ID. W `inventory-names-01.jsonl` uzgodniono 40 konfliktowych etykiet map z nowszym `inventory-names-02.jsonl`; pełne scalenie nie wykrywa już rozbieżnych niepustych wariantów, a metadane i tokeny przechodzą walidację. Wśród pustych pól jest **3 742** rozpoznanych komend slash w `custom_dialogue`; po ich pominięciu pozostaje najwyżej **1 536** kandydatów do ręcznej oceny — nie wszystkie są tekstem do tłumaczenia. Potwierdzono co najmniej 94 nieprzetłumaczone wiersze widocznego UI craftingu na Map 46: po 47 wystąpień pytań „Craft this item?” i „You have items missing from this recipe.” Drafty wymagają redakcji; nie zmieniono eksportu kanonicznego ani source ZIP. Nie zbudowano patchera Windows i nie uruchamiano gry/runtime.

## Pokrycie

| Powierzchnia / kategoria | Rekordy | Uwagi |
|---|---:|---|
| Customowy dialog CE60 | 38 638 | 29 647 różnych payloadów; tekst oddzielony statycznie od nagłówka. |
| Arianna hints | 705 | Potwierdzony przepływ przez CE222. |
| Telefon | 30 | 17 wartości skryptowych + 13 natywnych wierszy CE54; osobno od UI listy. |
| UI listy telefonu CE17 | 378 | Widoczne pozycje UI, nie klasyfikowane jako dialog. |
| Etykiety znalezionych przedmiotów | 649 | Statyczne wartości V[107] renderowane przez CE223. |
| Obrazowe podpisy CE224 | 134 | 67 statycznych wywołań; dwie komendy 401 to scaffolding renderera. Tekst w samych obrazach nie jest analizowany. |
| Natywne wiersze 401 poza rendererami | 1 513 | Wszystkie zachowane jako tekst do tłumaczenia: 1 122 wiadomości, 378 UI telefonu, 13 natywnych tekstów telefonu. Osiem rendererów pominiętych. |
| Wybory 102 | 2 110 | 695 grup; wszystkie opcje to pełnoprawny tekst do tłumaczenia. |
| Statyczne wartości zmiennych przez `\\V[...]` | 262 | 134 tekstowe/statusowe tłumaczalne; 61 cen + 67 markerów chronionych. 132 whitespace-only wartości pominięte jako layout. |
| Potwierdzone UI JS | 35 | 4 engine-static, 9 parametrów pluginów, 22 static plugin UI; skan 78 plików: 563 kandydatury, 528 wykluczeń, 0 nierozstrzygniętych. |

Pozostałe kategorie obejmują 239 niepustych linii Credits, 291 nazw map, 28 nazw aktorów, 477 nazw przedmiotów oraz 131 rekordów System. W pakiecie jest **131 chronionych wartości** łącznie (128 cen/markerów + 3 etykiety Lovense używane przez logikę).

## Audyt dodatkowych kanałów

- Wszystkie 563 kandydatury JS otrzymały decyzję: 35 potwierdzonych UI, 528 wykluczeń z jawnym content-free powodem, 0 odroczonych i 0 nierozstrzygniętych. Wykluczenia to wartości kodu/konfiguracji/markup bez dowodu UI w danym locatorze, nie „wiadomości techniczne”.
- Statyczny przegląd event scripts objął alerty, błędy Graphics, komunikaty/opcje/drawText i przepływ Lovense. Poza śledzonymi kanałami nie wykryto dodatkowych statycznych literałów przy sinkach wiadomości/opcji/drawText w kodach 355/655.
- 1 570 plugin commands sklasyfikowano jako sterowanie/parametry: AnimationCurve 1 321, MessageWidth 156, MessageRows 42, Play2ndBGS 17, Fadeout2ndBGS 4 i steamworks 30.
- Zbadano 34 pola `Items.note`: tagi/metadane, bez prozy. Nazwy assetów, media i editor-only labels nie są źródłowym tekstem pakietu.
- Lovense: widoczne `PC`/`LAN`/`Web` pozostają chronione jako runtime-operandy, `Not Connected` jest tłumaczalne. Nazwy urządzeń/nicknames to dynamiczne dane zewnętrzne.

## Zakres i dalsze prace

- Wszystkie **1 122** nie-rendererowe wiersze `401` i **2 110** opcji są pełnoprawnymi tekstami widocznymi dla gracza i w całości należą do zakresu tłumaczenia.
- Tekst wtopiony w obrazy i wideo jest poza zakresem na wyraźną decyzję właściciela. Runtime’owe nazwy urządzeń/użytkowników i obliczane liczby są danymi dynamicznymi, nie statycznymi źródłami lokalizacyjnymi.
- Źródłowy język i konkretny build nie są formalnie potwierdzone. Nie ma kompletnej polskiej zwrotki, testów fontów/łamania w runtime, instalatora ani patcha.
- ZIP v1 to source package; nie zmienia gry i nie jest finalną paczką spolszczenia. Binarne assety gry pozostają poza Git; tekstowe dane, robocze tłumaczenia, dokumentacja i narzędzia są śledzone w Git.

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
