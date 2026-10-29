# Status — The Genesis Order

**Stan (2026-10-29): wszystkie kwalifikujące się teksty statyczne uzupełnione; proof of concept patcha standalone i Czytanki PL v1 zbudowane i sprawdzone statycznie.** Pozostają redakcja językowa oraz testy Windows/runtime/renderingu; nie jest to zatwierdzona dystrybucja.

## Wynik bieżący

- Kanoniczny, śledzony w Git eksport: `games/the-genesis-order/translation/export-v1/`, **45 229 rekordów**, 25 JSONL i `export_manifest.json`; wszystkie kontrolne liczniki pokrycia przechodzą.
- `apply_translation.py --check` wcześniej zweryfikował **45 229/45 229** rekordów i hashe **238** plików źródłowych. W bieżącym workspace oryginały nie są zsynchronizowane, ale są na Google Drive (306 plików pod `TGO/www/data/`); brak lokalnego pliku nie oznacza braku uploadu.
- Markdown: **497 dokumentów / 45 229 rekordów**. Source ZIP: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`; archiwum jest śledzone w Git i publikowane na Google Drive w `TGO/translation/packages/`. ZIP nie zawiera assetów źródłowych ani kodu gry.
- Pakiet obejmuje canonical JSONL, kontekstowy Markdown, instrukcję PL, manifest, glossary/politykę i raport zakresu. To pełny zatwierdzony pakiet statycznych tekstów źródłowych do tłumaczenia, nie patch ani gotowa polska dystrybucja.
- Pełne testy: **88/88 passed** (`python3 -m unittest discover -s games/the-genesis-order/tests -q`, ~15 s). Obejmują walidację placeholderów/escape’ów, Markdown import-check, pełne scalenie draftów, audyt pokrycia (także jawne wyjątki decyzji właściciela), patcher standalone, generator Czytanek (także reguły redakcyjne opublikowanego skryptu), odmianę imion R-09 i spójność artefaktów. Jeden z testów odtwarza `payload/translations.jsonl` ze samych draftów w Git i porównuje jego SHA-256 z manifestem — to dowód odtwarzalności, nie deklaracja.
- Audyt i merge wszystkich **427** draftów: **45 229** rekordów, **39 917** niepustych tłumaczeń, **131** jawnie chronionych wartości, **5 181** zachowane rekordy nielokalizowalne i 0 nierozstrzygniętych rekordów do tłumaczenia. Brak konfliktów; ID, metadane i tokeny są walidowane. Eksport kanoniczny pozostaje niezmieniony.
- Milestone (1), `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip` (SHA-256 `914e73fa9e9022aabbe9a5fcb5dfef553d6100b6f266e8fde9e256f8344e6789`): 39 917 tłumaczeń, 238 fingerprintowanych źródeł, backupy i one-click patcher. ZIP przechodzi kontrole statyczne; bez testu Windows/runtime. **POTWIERDZONE:** jego `payload/translations.jsonl` ma SHA-256 `d90191df69ca4194b6d59071ce6a4a40a3dfa5ac52c5a5b20f5ff9b726a44458`, identyczny z payloadem odtworzonym ze świeżego scalenia draftów w tym repo — artefakt nie zawiera nic spoza Git.
- **Publikacja na Google Drive (POTWIERDZONE, MD5 zgodne z plikami w Git):** folder `TGO/translation/packages/` (`1FYzfQsDJKBaI_GBjlA8qhtS9I9h5_5KM`) — patch `1qPjZ55tOj_6dh8l9aS710wyq-n2Kq8vc` (3 740 219 B), Czytanka `1a8hDbNlBsrGMUlNXmlNI1IIA4nq0J-Pk` (3 312 572 B) oraz ich sidecary `.sha256` `1xtyJJo-VBC7yQZEKBo6H4znKrAel4CRs` i `1_dgwmBVChbF7TVq4bT0_sMU4YyohyuqW`. Poprzednie wydania tych dwóch paczek są w koszu Drive.
- **Raporty w Git:** `translation/reports/` zawiera `coverage_audit_v1.json`, `patch_manifest_v0.1.1.json` i `source_fingerprints_v0.1.1.json` — manifest i 238 fingerprintów wyodrębniono z ZIP-a patcha, bo bez oryginałów gry nie da się ich odtworzyć.
- **Odzyskanie po poprzednim agencie (2026-10-29):** pracy nie było w Git, ale istniała w patchu z Drive (`01a188a8…`, 4 438 plików) i w dwóch ZIP-ach. Wszystko wartościowe jest teraz w repo i sprawdzone niezależnie: patcher i narzędzia z ZIP-a są bajt w bajt zgodne z plikami z patcha, a Czytanka w ZIP-ie jest identyczna z drzewem `reading/v1/`. Pełny raport: [`RECOVERY_2026-10-29.md`](RECOVERY_2026-10-29.md).
- **Decyzje redakcyjne:** [`EDITORIAL_DECISIONS.md`](EDITORIAL_DECISIONS.md) — **wszystkie 11 pozycji rozstrzygnięte.** Wykonane w korpusie: R-01 (tytuł gry po angielsku), R-02 (`Channel 4` bez zmian), R-07 (placeholdery TEST MAP po angielsku), R-08 (`TEXT` wraca), R-09 (ujednolicenie odmiany imion na `-a`). **Zostają bez zmian** (właściciel uznał je za nieistotne, 2026-10-29): R-03, R-04, R-05, R-06, R-10. **Otwarta pozostaje tylko R-11** — polskie glify w czcionkach gry; weryfikacja u właściciela po wgraniu patcha.
- **R-09 wykonane (POTWIERDZONE):** `tools/unify_name_declension.py` odmienił **383 wystąpienia w 380 rekordach (148 plików)**, wyłącznie tam, gdzie przypadek wynika ze składni (wołacz po przecinku / cała kwestia / początek zdania, dopełniacz po rzeczowniku lub przyimku). **628 wystąpień** w formach niejednoznacznych zostało bez zmian i jest wypisanych w `translation/reports/declension_r09_report.json`. Drugi przebieg narzędzia daje zero zmian. To redakcja form, nie ponowne tłumaczenie.
- **Czytanka — reguły redakcyjne właściciela (POTWIERDZONE):** bohater nazywa się **Mox** (wcześniej widoczne `1Hero`, 17 032 wystąpienia w skrypcie), kolejne kwestie dialogowe nie są już rozdzielane pustą linią, a techniczne linie `<sub>Źródłowe ID…</sub>` zniknęły z `chronological_script_PL.md` (w plikach `episodes/` zostają jako ślad źródłowy). Numeracja rozdziałów, kolejność i indeks lokacji są dziedziczone z wydania v1, bo danych map gry nie ma w Git — opisuje to `README_PL.md` paczki.
- Milestone (2), Czytanka PL v1: **4 394** rozdziały (4 134 map/event/page + 260 Common Events), pełny skrypt, osobne epizody, indeks TSV oraz indeksy 55 mówców i 291 lokacji. BFS wskazuje 221/291 map osiągalnych statycznie od startu; kolejność nie jest kanoniczna. 833 wiersze z nieustalonym mówcą są oznaczone, nie zgadywane. ZIP: 4 399 wpisów; SHA-256 `74a3b096a07e92de32f6b5ac42e9f297cf4a33adf2db21fdd92359f60ec04c4f`. Gry nie uruchamiano.

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
- Nie zweryfikowano polskich glifów, długości/łamania wierszy ani zachowania w działającej grze. Patcher jest proof of concept; wymagane są testy na kopii docelowego builda Windows oraz redakcja językowa.
- Source ZIP v1 pozostaje pakietem źródłowym, nie patcherem. Patch POC i Czytanka są osobnymi artefaktami; binarne assety gry pozostają poza Git.

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
