# Dziennik eksperymentów — The Genesis Order

> **Aktualna decyzja właściciela:** wcześniejsze wzmianki o pozostawianiu tekstów lub tłumaczeń poza Git opisują ówczesny stan, nie obowiązującą zasadę. Wszystkie tekstowe dane projektu, narzędzia i robocze tłumaczenia śledzimy w Git; poza Git pozostają binarne assety gry.

## 2026-10-28 — pierwszy pakiet inwentaryzacyjny

- **Cel:** zebrać lokalny spis plików i rozmiary bez założenia silnika ani ścieżki instalacji.
- **Pakiet wejściowy:** `TGO_INVENTORY_REQUEST.zip`, SHA-256 `17305fbf058383f5c9f38472ff60640916de8a684e303096a5052d078ad0478f`; Drive file ID `1Tl3Pmu8PHb5aQXpA5Ah2OKvL0qO96TBe`.
- **Zawartość pakietu:** `URUCHOM.bat`, `COLLECT_TGO.ps1`, `INSTRUKCJA.txt`.
- **Walidacja sandbox pakietu wejściowego:** ZIP poprawny (CRC), ma trzy oczekiwane pliki; statyczne kontrole potwierdziły generator raportu i brak polecenia usuwania. Nie uruchamiano go przez PowerShell w sandboxie.

## 2026-10-28 — pierwszy wynik z Windowsa

- **Raport:** `TGO_DIAGNOSTIC_20261028_191643.zip`, Drive file ID `1gwWlg0ywzYY8k0gjWDi77iTNGl70zmaL`, rozmiar 263 365 B, SHA-256 `9d4a4d129ae1af3208bd7f14fdfdeda72d211c5849e1df1a709e3b9215af2d12`.
- ZIP zawiera pięć raportów tekstowo-strukturalnych: dwa CSV, JSON, podsumowanie TXT i transcript TXT; łączny rozmiar po rozpakowaniu 3 080 183 B. Nie zawiera plików gry.
- Zweryfikowano strukturę ZIP i odczytano CSV/JSON/TXT bez uruchamiania kodu. Raport podaje 17 694 pliki, 19 169 362 931 B, `possibleTextResourceCount=17625` oraz zero ostrzeżeń skanowania.
- Struktura ścieżek i rozszerzeń (`www/js/rpg_core.js`, `www/data/Map###.json`, `.rpgmvp`, `.rpgmvo`, `nw.dll`, `node.dll`) mocno wskazuje na RPG Maker MV + NW.js; wersji i builda nie potwierdzono.
- Pole „possible text resources” obejmuje także media (.mp4/.rpgmvp/.rpgmvo), więc nie mierzy rzeczywistego zakresu tekstu.
- W `_Redist` znajduje się wpis `fitgirl.md5`, co sugeruje repack FitGirl. To sygnał do wyjaśnienia, nie samodzielny dowód statusu prawnego. Transcript raportu zawiera nazwę konta i komputera; tych danych osobowych nie kopiujemy do repo.
- **Nie** otwierano zawartości JSON/JS z instalacji, nie uruchamiano gry, nie ekstraktowano assetów, nie modyfikowano plików ani nie budowano patcha.
- Użytkownik wyjaśnił, że wpis `fitgirl.md5` to jego zdaniem pozostałość niezwiązana z projektem. Pochodzenie/sklep kopii pozostaje niepotwierdzone; próbkowy skrypt instruuje używanie wyłącznie kopii z autoryzowanym dostępem.
- **Pakiet 2:** `TGO_STAGE2_REQUEST_v1.0.0.zip`, Drive file ID `1TNI-ZixJyXj9FP7RXwOE969GqwOOcv4-`, rozmiar 3 495 B, SHA-256 `e563a3e1d5f46cbe2dfb466895b8b214c28b13f785080211b10d36d3b8ecf216`. Zawiera wyłącznie BAT, PowerShell i instrukcję (bez assetów gry).
- Skrypt etapu 2 statycznie przejrzano: jawna allowlista, bez rekursywnego kopiowania, bez wykonywania kodu z gry i bez zapisu do katalogu gry. Sandbox nie ma Windows PowerShell 5.1, więc skrypt nie był tam uruchomiony.
- Użytkownik wybrał bezpośrednie przesłanie danych tekstowych zamiast uruchamiania pakietu 2. Pakiet nadal istnieje na Drive, lecz nie jest potrzebny do bieżącej analizy.

## 2026-10-28 — bezpośredni upload danych/JS

- Folder `www` na Drive: ID `1b1TmOhXx-a8P-pqUS8g6o18HzHVe_fsb`; podfolder `data`: ID `1dY4OpAedbcLSuh2GERf9k8HTbGY4iqLn`; `js`: ID `1A0uM6qPAmTrIoTnaXBIzBn7Gvy-W9Wo8`.
- Drive zawiera 306 elementów w `www/data` (305 JSON + `Credits.txt`) oraz katalog `www/js` z kodem silnika, `plugins.js`, `plugins/` i `libs/`. Główny `package.json` ma ID `1J32h3HCPuwB3HGPWb4oM4FI72y4er1bK` (243 B). Folderów z obrazami, audio i filmami nie pobierano.
- Lokalnie pobrano wybraną próbkę; reszta danych nadal pozostaje na Drive. Poniżej ID i SHA-256 plików pobranych do statycznej analizy:

| Plik | Drive file ID | Bytes | SHA-256 |
|---|---|---:|---|
| `package.json` | `1J32h3HCPuwB3HGPWb4oM4FI72y4er1bK` | 243 | `47e91b54ea4c934dac5ecbb4a99b72c8a40ef16e677bee8ff07ae1419ab81bf` |
| `www/data/System.json` | `11NvNtv8bkMwYCEU4KZJx2cYapzrb3fAe` | 67 244 | `a2e0e6b55dd7cbaa0688feac218e2bf461cb2edd84987a86a092e157ba861732` |
| `www/data/MapInfos.json` | `1FR_FVURDGPzZaQkUBBj2xuu_-50VSg2A` | 29 895 | `becc8069b275a296e9ea9ec393435b719d36f98982fc268ccc044d19e9fbbb52` |
| `www/data/CommonEvents.json` | `1TWpjge4k6q1X5rshp_WlUt0mIJaEQ7lK` | 8 370 942 | `37321ff8693412e5e4488eb736a63b43fcbd142410008b73f5bcb317c27e3ca9` |
| `www/data/Map001.json` | `12qtfTT7QaTOQZU3UsQagYqWkBqMcZ433` | 5 994 | `ebe917a8a2b1a81be34366ef0eb71a042667e1926045bc3f34bd9c30bd81de11` |
| `www/data/Map002.json` | `1XSRqkz2KMvHEw-XcpEhD9pPQ37XHy_CH` | 73 239 | `0858ff180c910e0516ab8df19a776443517f828ee500e9028099f6274f3d9097` |
| `www/data/Map003.json` | `1ayMPasthCixecuVUFYab0ZNt8dTmoKEt` | 569 635 | `e08f416d6d2ec4d4ed67bf67439de36ffb60a831d641c54decb2a806cc9dc86c` |
| `www/data/Map038.json` | `1nFp5cWSs6e_sC0A_GanDYKufKxFyErOQ` | 6 860 | `33489ba187a0a080a6c7de0636ded7540b1e81ec898a0dc316235f195e2c0195` |
| `www/js/plugins.js` | `1fG4EGgUKXtIE3KbNfFc9uWyn_Awjxunk` | 18 042 | `4ba4294032bcd187262d91a70df64ba1905986768d2f7e1d420b5a2fe2249521` |
| `www/js/rpg_core.js` | `1ujkl12ckVUkpyLvZMrNiFDjeHbHfcY1e` | 244 685 | `9020b78d4984b61d58565fcc1d2f4d2071fd80f5fb3b83d4de633b01e4af7c5b` |
| `www/js/rpg_managers.js` | `1EuRJwBhrTeWvm3FN_fPtrl3x8BElu29t` | 84 678 | `791082a4d5768d4a661c071dac828805119952a32d33dabfb440c2d18f0bbed7` |
| `www/js/plugins/Choices.js` | `17QjkMf1XtyP8HY9cTk36wbBrp1q3pEKA` | 1 862 | `e62d24fbedcaec26d558d9154834c59be87fd9fffed6d7e1cff08f4e4e160985` |
| `www/js/plugins/Eli_FontManager.js` | `1OU1QxkxHYdKoWJh9K-wbOkHeYuffrxse` | 15 804 | `776773de5a4fd851fed3aa2f0e9047c6d50c558ce4673f386862923232aa6d99` |
| `www/js/plugins/RS_MessageAlign.js` | `1UDFrqW3xBELlk7fOsvwzm8l3OyxQLXV5` | 14 614 | `12bb247ca2ae4acb01203277aa836f5b697c1b3c57830a60fd9b33c22d074a23` |
| `www/js/plugins/TSR_TextColorAddOn.js` | `1DixovspJYu9ULTHc_BDJd_fK91ttCnmD` | 32 600 | `afb3dea3de09cfadd9d0862e6cc99ac76cd3260206c8051bdeab5b68a70e5aa5` |
| `www/js/plugins/YEP_CoreEngine.js` | `1qPU11DY-ymw_yQ1z2Tq14luJb5s0JiUt` | 95 463 | `6cc5ca5d9213f4f471a09a12cde51310e395688260d687df398f0e54ba98ef32` |
| `www/js/plugins/YEP_LoadCustomFonts.js` | `1zK7fAsd14Kc4oaotYHOh61fAyvjPrKOW` | 4 249 | `c41839917bcdcbce8f41394d4c214cbdd5e2879ee6418cb65fc5e362f0eb1bb9` |
| `www/js/plugins/YEP_MessageCore.js` | `16FQvfsda_MJtl-iLHV_TbZvszHjMQEif` | 50 284 | `4003fc9300924845ef968c4e39a48c228879fc730b50821094f81d1ce620db36` |
| `www/js/plugins/YEP_X_MessageSpeedOpt.js` | `1PoEFRlhK0j3GTmSzoXgePjeSW3Osa8BP` | 11 807 | `91871e6308621b90d852dea3765b854494e7c8fd41464f256e5e5ab45c7f5cac` |

- Statyczne parsowanie potwierdziło 56 plugin entries / 53 enabled, silnik MV 1.6.1, 291 map, mapę startową 38 i 500 Common Events. Zliczenia pól tekstowych i ograniczenia próbek są w `TECHNICAL_FINDINGS.md`; nie wypisywano zawartości dialogów do repo.
- Nie uruchamiano JS, gry ani runtime; JSON parsowano statycznie. Nie skopiowano żadnego assetu do Git.

## 2026-10-28 — fonty i pytanie o zakres przed tłumaczeniem

- Użytkownik przesłał folder `www/fonts/`, Drive folder ID `1PL1rfnA0p6RNgJdJ_kT_zY06Lz3KPS5H`. Zawiera 11 fontów `.ttf`/`.otf` oraz `gamefont.css` (łącznie 12 plików).
- Pobrano wszystkie; identyfikatory Drive, rozmiary i hashe:

| Plik | Drive file ID | Bytes | SHA-256 |
|---|---|---:|---|
| `Akong_agi.ttf` | `1OmtKhPfZgLCCu4spjwh-TwHSFhVi7vhF` | 56 552 | `c6c67bd26b3f556947dbbce6fb6c5aacb8db98f5c65e1b9373e6a9a1691fb877` |
| `Chapbook-Regular.otf` | `1AO_V6SEskOTSng-ShBl88k4UZXACkaV7` | 172 628 | `c1a8b72c565d9ce04eeac6c5b4a18d4006052ad9a0aa84f70c9fe6165e6e7e25` |
| `Cinzel-Black.ttf` | `19cVu_2Bm7QoU4714nfLZQXdJH5Wpcg9t` | 58 616 | `2cce1b54893150f460214b19644f4be9c4eafb32fc221f1a14b856dc1f99e52b` |
| `Cinzel-Regular.ttf` | `16ywK5y9P8kw-9GmJQcb9YENfZWKZ52IZ` | 56 228 | `a73369ecaad30447f72e12d4c80f98dee5aa0e029b841d5a04a28ccd131cb0c4` |
| `gamefont.css` | `19N3d7d8TMIV4jcv4WTRgq5xr6ECYRWR6` | 254 | `b2d96e6d941ad1be97aca81aae9a5427ce8fc17770498ed0a45b40203e9b097a` |
| `JosefinSans-Regular.ttf` | `1aLZEAnTVSw8goZdbk693u0GxT2dnt_Ee` | 33 008 | `e07aa47f7e6dd461342c147d280f094b9f62a0adb52555fb3ec0e899afcf0a06` |
| `JosefinSans-SemiBold.ttf` | `1FANmh8xwp4q6xey_d27vhEBqSdXlDqAB` | 33 004 | `bce2ed51da316e20fc108befa1ba152850eca29cfc2b26f278a8d74957a677fb` |
| `mplus-1m-regular.ttf` | `1wK7ci2KL7DQjkXlPZvW7ABXGEzqZBTI3` | 1 541 768 | `7f2096495dab49c7150cd0609f2f8d6b03ebf2fa7561ea34b3cca1e09eb0bae5` |
| `SpecialElite.ttf` | `1Jd5jCmVa9SBVAZPM6Wo0EHEzing3wHjz` | 166 224 | `9ebacf4e85df65a89db88a3ec38576969490f418890fc6478fb00c2fcbdb4f4c` |
| `texgyreadventor-regular.otf` | `1fbSDpmenUpGxALifLP85H0FgTX1vPBVj` | 124 680 | `f146708de32a3ee8ec1b627004a08f31dd137cc6bc6459ef0ecfc51fef170819` |
| `UglyTypist.ttf` | `1gvWhvOGyXmIlJ-J1zMcstxhOVgJ46OG9` | 79 272 | `12c8cc0dbe28a947c527c44cb59d0a36b7890011a392be7489b3ae484342a94a` |
| `underworld.ttf` | `1eMpmbOE-fWIv2rN5CW5zXnbjbIhC6sMs` | 212 196 | `8a546cf7ce429b35292c843908f0dcc98a46d10cf436d2bed01966df048b4be1` |

- FontTools 4.68.0 cmap dla 18 polskich liter: 7/11 fontów mają pełne pokrycie, 3/11 tylko `óÓ`, a UglyTypist 0/18. `gamefont.css` przypisuje domyślny `GameFont` do JosefinSans-SemiBold (2/18); brak runtime testu fallbacku.
- Użytkownik pyta o wiarygodny przedtłumaczeniowy licznik dialogów/wyborów oraz Czytanki dla obu tytułów. Potwierdzono, że to wykonalne jako osobny etap. Obecne liczniki są częściowe; pełna wycena wymaga przetworzenia wszystkich zasobów tekstowych obu wersji.
- Czytanka powinna zachować scenę/label/mapę, mówiącego, wybory i warunki. Ponieważ obie gry mają rozgałęzienia i teksty dynamiczne, kompletna Czytanka będzie branch-aware, a nie jedną liniową „kanoniczną” trasą.
- **Następny krok:** pełny, walidowany census obu korpusów (dialogi, continuations, opcje, UI/bazy danych i teksty skryptowe osobno), a potem próbny fragment Czytanki do akceptacji formatu. Tłumaczenia jeszcze nie rozpoczęto.

## 2026-10-28 — lista map i ograniczenie eksportu przed pełnym pakietem

- Paginowana lista plików Drive potwierdza mapy `Map001.json`–`Map291.json`. Lokalnie dostępne tekstowe próbki nadal obejmują tylko `Map001`–`Map003`, `Map038` oraz `CommonEvents.json`; pełny zbiór map nie został pobrany ani policzony.
- Połączenie Drive w tej sesji pozwala odczytywać/ściągać pojedyncze pliki, ale nie eksportuje folderu z setkami JSON-ów bezpośrednio do lokalnego parsera. Nie zastępowałem brakujących danych estymacją ani liczeniem samych rozmiarów.
- Żeby dokończyć uzgodniony bezpośredni upload bez mediów i bez uruchamiania BAT/PS1, potrzebny jest jeden ZIP wyłącznie z `Map001.json`–`Map291.json` i `CommonEvents.json` (opcjonalnie `MapInfos.json`). Do tego czasu liczba 611 wierszy dialogu i 816 opcji dotyczy wyłącznie `CommonEvents.json` i nie jest pełnym wynikiem TGO.

## 2026-10-28 — pełny pakiet `www/data/` i census dialogów/wyborów

- Użytkownik przesłał `data.zip` (Drive file ID `1jvwrMJKqQDq28q2EVLb_B4jO7w6po_Sw`), 3 299 615 B, SHA-256 `c9deca5c733cbbc92306e41a8afa0157e38758283a9c7662960349f9b9fd5842`. Archiwum ma 306 elementów: 305 JSON + `Credits.txt`; CRC poprawny, brak niebezpiecznych ścieżek.
- Zweryfikowano poprawność wszystkich 305 JSON-ów, komplet `Map001`–`Map291` i 500 common events. Wszystkie pliki JSON pozostały w ignorowanym `google_drive/`; nic nie dodano do Git poza licznikami i dokumentacją bez tekstów gry.
- Pierwszy licznik event commands `401`/`102` ze wszystkich map i common events: 1 521 niepustych wierszy `401` (766 różnych surowych tekstów), 695 grup wyboru i 2 110 tekstowych opcji (376 różnych). Wówczas wiersze `401` błędnie opisano jako pełny dialog; audyt z tego samego dnia wykazał customowy kanał CE60, opisany w sekcji korekty poniżej.
- Zebrano także osobne pola systemowe/bazodanowe oraz metryki per mapa i common event; skryptowe/plugin commands pozostawiono poza dialogiem, jako potencjalnie dynamiczny zakres do oddzielnej inspekcji.
- Wygenerowano `docs/COUNT_REPORT.md`, `docs/COUNT_BY_MAP.csv` i `docs/COUNT_BY_COMMON_EVENT.csv`. Nie uruchamiano gry, nie uruchamiano żadnego kodu z danych ani nie rozpoczęto tłumaczenia.

## 2026-10-28 — korekta: customowy kanał dialogu i UI

- Użytkownik słusznie zakwestionował 1 521 jako pełny dialog. Analiza statyczna wykazała, że Common Event 60 `MESSAGE` pobiera tekst ze skryptowej `V[21]` po pierwszej kropce, zapisuje treść do `V[25]` i wyświetla ją przez `401`. Zachowując zapisane gałęzie, wykryto **38 638** wpisów i **29 647** różnych payloadów (27 602 wpisy na mapach, 11 036 w common events).
- Śledzenie najbliższego wywołania Common Eventu przed nadpisaniem zmiennej rozdzieliło 39 355 literałów `V[21]`: 38 638 do CE60, 705 do CE222 (`SHOW ARIANNA HINT`), a 12 wyłączono jako niepotwierdzone wiadomości (10 nadpisanych przed wywołaniem, po jednym skierowanym do CE61 i CE53). Nie wszystkie skryptowe stringi uznano za dialog.
- Osobno potwierdzono 17 literalnych tekstów telefonu przez CE53 (10 różnych), 649 etykiet UI znalezionych przedmiotów przez CE223 (334 różne) oraz 67 wywołań CE224. Dalszy statyczny trace wykazał, że CE224 preładuje bitmapy przez `Galv.CACHE.load`; nie jest to tekstowy payload. Dwa natywne wiersze CE224 zachowano jako `needs_review`. Natywne liczniki `401`/`102` pozostały oddzielone.
- Natywne 1 521 wierszy `401` zawierają 6 potwierdzonych rendererów/szablonów dla CE53/60/222/223; dwa wiersze CE224 zachowano jako `needs_review`. Z pozostałych 1 515 wierszy 378 należy do jawnej listy UI telefonu CE17, 13 do natywnego kanału telefonu CE54, a pozostałe 1 124 nadal nie są wszystkie sklasyfikowane. Wybory liczą 695 bloków / 2 110 opcji; w sześciu nazwanych menu/UI wspólnych zdarzeń potwierdzono podzbiór 44 bloków / 180 opcji.
- Dodano `tools/count_custom_text.py` i kolumny per mapa/common event; skrypt parsuje wyłącznie dane statycznie, nie wypisuje treści i nie uruchamia gry ani jej kodu. Zaktualizowano raporty oraz skorygowano wcześniejsze sformułowania o „pełnym censusie”.

## 2026-10-28 — rozstrzygnięcie kolejki JS (lokalne 5 plików)

- Zreprodukowano statyczny skan aktualnie dostępnych 5 plików JS: 327 kandydatur (216 literalnych kandydatur przy API wyświetlania, 111 parametrów pluginów). Każdy ID otrzymał jawny, content-free wynik: 27 potwierdzonych powierzchni UI, 300 technicznych/konfiguracyjnych/markupowych/sterujących pozycji poza zakresem przekładu w tym locatorze, 0 nieocenionych i 0 odroczonych. Decyzje nie zawierają źródłowych tekstów.
- Promocje potwierdzono statycznym przepływem do widocznych etykiet menu/opcji/ekranu tytułowego i rendererów UI; dodatkowe źródła pluginów sprawdzono tylko do odczytu. Wśród wykluczeń oddzielono klucze sterujące, asset/path/font/ustawienia, identyfikatory grup, placeholdery formatowania, markup, ASCII-keyboard i enumy logiki. Dynamiczny wynik API typu połączenia pozostaje osobną luką runtime, nie bezpiecznym literalnym celem.
- Wcześniejszy inwentarz 78 plików miał 554 kandydatury; po rozstrzygnięciu obecnego podzbioru pozostaje **227** z plików nieobecnych w bieżącej lokalnej kopii. Nie uznaje się pełnego pokrycia JS ani gotowości translator ZIP.
- Rozszerzono kurator i manifest o wyniki `confirmed / excluded / deferred / unreviewed`, kontrolę hashy wszystkich kandydatów oraz test syntetyczny. Zaktualizowano prywatny eksport do 44 827 rekordów i szkic Markdown do 495 dokumentów / 44 827 rekordów; pełny `--check` bez zapisu, testy `unittest` 20/20.


## 2026-10-29 — odtworzenie i rozstrzygnięcie pełnego skanu JS

- Przywrócono do ignorowanego `google_drive/the-genesis-order/www/js/` pełną hierarchię z Drive: 78 plików (8 root, 63 pluginy, 7 bibliotek). Hashy kandydatów w nowym skanie zweryfikowano z przywróconymi źródłami; JS nie był uruchamiany.
- Statyczny skan odtworzył dokładnie 554 kandydatury. Dodatkowe 227 zostały ocenione, a curation połączono z wcześniejszym podzbiorem: **554 total; 30 confirmed UI; 524 excluded; 0 deferred; 0 unreviewed**. UI: 4 `ui.engine_static`, 17 `ui.plugin_static`, 9 `ui.plugin_parameter`.
- Dwie nowe etykiety (`Error`/`UnknownError`) w silniku i jeden `UnknownError` w aktywnym YEP_CoreEngine są przekazywane do `Graphics.printError`, więc potwierdzono je jako widoczne UI ekranu błędu, nie dialog fabularny. Pozostałe nowe wartości to klucze TextManager/komend, alignments/formaty, kody markup, kontrolki pluginów, źródła nieaktywne lub niezaładowane oraz diagnostyka błędnego użycia statycznej klasy.
- Znaczenie poprzednich 300 wykluczeń: nie były to 300 wiadomości. Były to kandydatury kodu/ustawień/identyfikatorów/formatów bez dowodu widocznego UI w konkretnym locatorze; nie należy opisywać ich jako „300 technicznych wiadomości”.
- Prywatny eksport v1 odświeżono do **44 830 rekordów** (44 800 data + 30 JS UI); szkic Markdown ma **497 dokumentów / 44 830 rekordów**. `apply_translation.py --check` i pełny zestaw testów pozostają bramką końcową; ZIP nadal wstrzymany do audytu pozostałych dynamicznych i skryptowych powierzchni.

## 2026-10-29 — domknięcie statycznych powierzchni i aktualizacja kanonicznego eksportu

- Rozszerzono eksporter o statyczne wyrażenia stringowe z komendy 122, jeśli ich zmienne są jawnie użyte przez `\\V[...]` w komendzie widocznej wiadomości, tekstu przewijanego lub wyboru. Wykryto 394 literalne przypisania; 262 niepuste wartości weszły do kategorii `ui.variable_value`, a 132 whitespace-only wartości są placeholderami layoutu i zostały pominięte. 61 cen oraz 67 markerów otrzymało `keep_source_value`; brak nieliteralnych wyrażeń w dopasowanym zbiorze.
- Statyczny audit JS zakończono na 78 plikach / 563 kandydaturach: 35 UI (`ui.engine_static` 4, `ui.plugin_parameter` 9, `ui.plugin_static` 22), 528 wykluczeń z jawnym content-free powodem, 0 odroczonych i 0 nierozstrzygniętych. Źródłowe JS pozostały poza Gitem i żaden kod gry nie był wykonywany.
- Audyt listy 1 570 plugin commands: AnimationCurve 1 321, MessageWidth 156, MessageRows 42, Play2ndBGS 17, Fadeout2ndBGS 4, steamworks 30 — kontrola/parametry/asset/API, nie bezpośrednie statyczne UI stringi. 34 pola Items.note sprawdzono statycznie; zawierają wyłącznie tagi/metadane, bez prozy.
- Zaktualizowano bezpieczny write-back `event_script_expression`: tylko statyczny literał JS w operandzie komendy 122 może być zmieniony w staging copy. Hash/locator/source value są ponownie weryfikowane; dynamiczny expression nie jest eksportowany. Test syntetyczny potwierdza zmianę kopii i niezmienność wejścia.
- `export_translation.py` odtworzył kanoniczny, śledzony bundle w `games/the-genesis-order/translation/export-v1/`: **45 229 rekordów, 25 JSONL + manifest**, wszystkie coverage checks true, stabilne ID unikalne. Składniki kontroli obejmują 262 wartości zmiennych, 35 statycznych UI JS, 2 110 opcji, 1 122 ogólne wiersze 401, 8 rendererów pominiętych.
- `apply_translation.py --check`: 45 229 rekordów, 0 tłumaczeń, 238 source files zweryfikowanych, 0 plików zmienionych; `markdown_translation.py build --replace`: 497 dokumentów / 45 229 rekordów / 238 źródeł w ignorowanym google_drive. Markdown import `--check`: 45 229 kanonicznych rekordów, 0 tłumaczeń, 0 braków.
- Pełny zestaw `python3 -m unittest discover -s games/the-genesis-order/tests -v`: **27/27 passed**, w tym kontrola importu Markdown dla chronionych wartości; `git diff --check` bez błędów. Oryginalne assety pozostają poza Gitem; dokumentacja, narzędzia, decyzje kuratorskie oraz wyodrębnione JSONL są przeznaczone do śledzenia w repo zgodnie z najnowszą decyzją właściciela.
- Nie przygotowano ZIP-a, nie uruchamiano gry i nie rozpoczęto tłumaczenia.

## 2026-10-29 — źródłowy pakiet tłumaczeniowy v1

- Na prośbę właściciela przygotowano statyczny source ZIP v1. W późniejszej, wiążącej decyzji właściciel zatwierdził wszystkie 1 122 nie-rendererowe wiersze `401` i 1 930 opcji jako pełnoprawny tekst do tłumaczenia; obecny eksport i paczka używają neutralnych kategorii `native_message` oraz `choice_option`.
- Dodano `tools/build_translation_package.py`. Skrypt wymaga `coverage_checks_passed=true`, zgodności liczby rekordów między JSONL i Markdown, unikalnych ID, bezpiecznych ścieżek, zapisuje ZIP tylko pod `google_drive/`, sprawdza CRC ZIP-a i generuje sidecar SHA-256. Do archiwum trafiają wyłącznie eksport JSONL, Markdown, README/manifest pakietu oraz dokumenty tekstowe; bez assetów i kodu gry.
- Walidacja po dodaniu skryptu: `py_compile` OK; pełne `unittest` **27/27 passed**; Markdown import-check **45 229 rekordów / 0 braków**; builder zweryfikował `coverage_checks_passed=true`, **45 229 rekordów, 497 dokumentów, 131 chronionych wartości, 531 wpisów ZIP**. Końcowy SHA-256 i rozmiar zapisuje builder w `TGO_source_translation_package_v1.zip.sha256`.
- Ponowione `apply_translation.py --check` nie mogło wystartować, bo bieżące środowisko nie zawiera ignorowanego `google_drive/the-genesis-order/data/CommonEvents.json`. Wcześniejszy check 45 229 rekordów / 238 źródeł przeszedł; nie zmieniano eksportu JSONL.
- Nie uruchamiano gry/kodu gry. Nie wygenerowano tłumaczenia ani patcha.

## 2026-10-29 — zatwierdzony zakres tekstów i source ZIP w Git/Drive

- Właściciel zatwierdził wszystkie **1 513** nie-rendererowych wierszy `401` i wszystkie **2 110** opcji `102` jako pełnoprawny, widoczny dla gracza tekst do tłumaczenia. W eksporcie kategorie mają neutralne nazwy `native_message` i `choice_option`; usunięto podtypy sugerujące nierozstrzygnięty zakres, zachowując wydane ID.
- Potwierdzono, że tekst wtopiony w obrazy i wideo nie jest tłumaczony. Oryginalne media i kod gry pozostają poza zakresem/pakietem.
- Zaktualizowano manifest, generator eksportu, testy, format rekordów, raporty, zasady i handoff. Markdown odtworzony: 497 dokumentów / 45 229 rekordów; import-check: 0 braków.
- Pełne `unittest`: **27/27 passed**; `py_compile` i `git diff --check` przechodzą. Builder wymaga poprawnych liczników 1 513/2 110, sprawdza coverage i integralność ZIP-a.
- Source ZIP v1: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`, **8 499 321 B**, 531 wpisów, 45 229 rekordów, 497 Markdown, 131 chronionych wartości; SHA-256 `b2215cf29c33ad0f42e22852f3179985b829338be019887b13e5b8818217e2b6`.
- ZIP i sidecar `.sha256` są śledzone w Git. Identyczny artefakt i checksum przesłano na Google Drive: `TGO/translation/packages/` ([ZIP](https://drive.google.com/file/d/1G7T1-bKW9AFHR2tiwXK6xGBJCSSm2IWS/view?usp=drivesdk), [SHA-256](https://drive.google.com/file/d/1oiT5PIqOP2qqyoON2Xz1JQ0cKod0tNip/view?usp=drivesdk)).
- Nie uruchamiano gry ani kodu gry; nie ma jeszcze tłumaczenia ani patcha.

## 2026-10-29 — robocza partia UI 01

- Opracowano wstępny glosariusz i bezosobowe komunikaty UI na podstawie pól `term_path` i dowodów `visibility_evidence` w eksporcie v1, bez uruchamiania gry. Formy są robocze; font, długości i kontekst wymagają testów.
- Partia `google_drive/the-genesis-order/translation/draft-ui-v1/` to cztery kopie kanonicznych plików: `system_terms` 95/95 niepustych pól, `ui_engine_static` 4/4, `ui_plugin_parameter` 9/9, `ui_plugin_static` 19/22. Razem **130 rekordów / 127 niepustych pól** (w tym celowo niezmienione skróty/nazwy). Chronione PC, LAN i Web pozostawiono z pustymi polami; nie są brakującym tłumaczeniem. To nie jest cały zakres 45 229 rekordów.
- Sprawdzono kolejność, ID, wszystkie pola poza `translation`, duplikaty i `validate_record` (tokeny, chronione wartości, lokatory) względem kanonicznych plików: 130/130 poprawne. Pełne `apply_translation.py --input ... --check` nie powiodło się: brak lokalnego `google_drive/the-genesis-order/data/System.json`. Nie weryfikowano hashy oryginalnych źródeł w tej sesji; oryginały pozostają na Drive.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: 27/27 OK. Brak testu Windows/runtime, renderingu, polskich fontów i faktycznego write-backu. Source ZIP v1 nie był modyfikowany.
- Archiwum robocze [TGO_draft_ui_01_2026-10-29.zip](https://drive.google.com/file/d/192Umg5H5xVGzoAtyMN8fDJ6HSrreO1A7/view?usp=drivesdk), Drive ID `192Umg5H5xVGzoAtyMN8fDJ6HSrreO1A7`, 10 978 B, SHA-256 `2ca5d0545ea804ff6d4e8655ab71e5437e4a4f06b65705c7e95641d2281103aa`. Oryginalne pliki gry nie są częścią ZIP-a. To nie jest patch ani ukończona lokalizacja.

## 2026-10-29 — wskazówki, kontrola tokenów i scalanie partii

- Przetłumaczono roboczo 65 pierwszych wskazówek Arianny z eksportu `arianna_hint.jsonl`, z zachowaniem ID i kontekstów warunków. Część terminologii (kausza/zaciski) oznaczono do weryfikacji; nie ustalono chronologii ani nie potwierdzono polskich form w grze.
- Znaleziono lukę: oryginalne `markup_tokens` v1 nie uwzględniały pozycyjnych `%1`, `%2` ani escape’ów RPG Maker typu `\>`, `\!`. Bez zmiany sygnatury wydanego eksportu dodano dodatkową kontrolę w importerze Markdown i `apply_translation.py`. Dotychczasowa partia UI przeszła nową kontrolę; nie oznacza to testu runtime.
- Przy `--require-complete` puste chronione `keep_source_value` są dopuszczalne, pozostałe puste nie są. Sama kontrola częściowej zwrotki nie dowodzi pokrycia całości. Nowy `merge_translation_batches.py` sprawdza tożsamość wszystkich pól poza translation względem kanonicznego eksportu, identyfikatory, tokeny, chronione wartości oraz konflikty; odmawia nadpisania pliku wynikowego i zapisuje wyłącznie pod `google_drive/`.
- Polecenie: `python3 games/the-genesis-order/tools/merge_translation_batches.py --batch google_drive/the-genesis-order/translation/draft-ui-v1 --batch google_drive/the-genesis-order/translation/draft-hints-01.jsonl --out google_drive/the-genesis-order/translation/merged-ui-hints-2026-10-29.jsonl`. Wynik: **45 229 rekordów, 192 niepuste pola, 131 chronionych wartości, 44 906 tłumaczalnych oczekujących**. SHA-256 pełnego lokalnego JSONL: `fe2231f51b2789df7aa0c6a3cf00ed0691d607db88ad70179559cefef12ffbd1`. Licznik niepustych obejmuje także celowo zachowane skróty/nazwy.
- Partia wskazówek: [TGO_draft_hints_01_2026-10-29.jsonl](https://drive.google.com/file/d/1n2r4gLCZMwkbzqpCenDJNJOF-AbKn-OM/view?usp=drivesdk), ID `1n2r4gLCZMwkbzqpCenDJNJOF-AbKn-OM`, 90 009 B, SHA-256 `0a2f35525583222bc8a1fd72fee7b77ae317f2a65e5de7cc92d08146f97e4918`. Pełny scalony JSONL pozostaje lokalnie poza Gitem; do odtworzenia potrzebne są obie zwrotki i kanoniczny eksport.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **33/33 OK**; pełne porównanie 195 rekordów obu partii z eksportem oraz kontrola wszystkich 45 229 kanonicznych rekordów bez źródeł — OK. Nie wykonywano walidacji hashy oryginalnych assetów, write-backu ani testów Windows/runtime.

## 2026-10-29 — wskazówki, partia 02

- Kolejne 35 wskazówek przetłumaczono po stabilnych ID, z zachowaniem kontekstu i gałęzi. Wymagają redakcji oraz kontroli terminologii w grze; „hammer shovel” / „łopata-młot” pozostaje robocze.
- [TGO_draft_hints_02_2026-10-29.jsonl](https://drive.google.com/file/d/1Sd5I5LLJeRX217dSIc-cNuWVNWIcrjk-/view?usp=drivesdk), ID `1Sd5I5LLJeRX217dSIc-cNuWVNWIcrjk-`, 48 343 B, SHA-256 `8759fe6abeb3fd56425bdc0afcbd50df98a0aef4b8e56a070b4c065b4cc2984b`.
- `merge_translation_batches.py` sprawdził trzy zwrotki i utworzył nowy `google_drive/the-genesis-order/translation/merged-ui-hints-02-2026-10-29.jsonl`: 45 229 rekordów, 227 niepustych pól (łącznie ze skrótami), 131 chronionych, 44 871 tłumaczalnych oczekujących; SHA-256 `1d491ac93915e2a5dc6cfda8e6d24d7f33ae704a4f06e93ea242a2d98b79f3cd`. Poprzedniego scalonego pliku nie nadpisano. To nie jest patch ani wynik testów runtime.

## 2026-10-29 — korekta zasad Git i publikacja zwrotek

- Decyzja właściciela: wszystkie narzędzia, tekstowe dane źródłowe i robocze tłumaczenia muszą być śledzone w Git. Wyjątek dotyczący materiałów gry stanowią wyłącznie binarne assety. Drive pozostaje dodatkową kopią. Wcześniejsze wpisy o prywatnym/ignorowanym przechowywaniu opisują stan historyczny, nie obowiązującą zasadę.
- Dodano do `translation/drafts/` dotychczasowe partie UI i wskazówek, bez zmiany ich zawartości. Scalanie z tych śledzonych plików potwierdziło 45 229 rekordów, 227 niepustych pól, 131 wartości chronionych i 44 871 tłumaczalnych oczekujących; SHA-256 scalonego rezultatu `1d491ac93915e2a5dc6cfda8e6d24d7f33ae704a4f06e93ea242a2d98b79f3cd`, zgodny z wcześniejszym wynikiem.
- Import i generowanie Markdown oraz scalanie pozwalają na zapis w śledzonym `translation/`, z ochroną kanonicznego `export-v1/`; staging gry nadal nie nadpisuje źródeł. `python3 -m unittest discover -s games/the-genesis-order/tests -q`: 35/35 OK. Nie wykonywano testu gry ani ponownego sprawdzenia oryginalnych źródeł.

## 2026-10-29 — wskazówki Arianny, partia 03

- **Wejście:** kanoniczny `translation/export-v1/arianna_hint.jsonl` (SHA-256 `6057c3871232dd53fe969704aa0db9dd106063088938806f3e353e4c7e1c34c8`), dane wywodzą się z `data/CommonEvents.json` (SHA-256 `37321ff8693412e5e4488eb736a63b43fcbd142410008b73f5bcb317c27e3ca9`). Kontynuowano po pierwszych 100 już opracowanych wskazówkach; wybrano następne 35 rekordów po stabilnym ID.
- **Wynik śledzony w Git:** `translation/drafts/hints/draft-hints-03.jsonl`, 35 rekordów, 47 764 B, SHA-256 `ca01a0de0d869772353bd7c340d6eaf79d67d412046aab8499533dd02e3f4644`. Zmieniono wyłącznie pole `translation`; rekordy są wersją roboczą do redakcji. Nie zmieniano źródłowego eksportu.
- Rozszerzono roboczy glosariusz m.in. o `taca na datki`, `balsam aloesowy`, `zwykły pojemnik`, opisowe `środek do usuwania sadzy` i `słój`. Wskazówka używa pisowni `Anglecrafting`; zachowano uzgodnione robocze `Angelcraft` po stronie tłumaczenia, bez korekty źródła. Dla `station reception` pozostawiono neutralne `recepcja stacji`, bo tekst nie rozstrzyga, czy chodzi o Police Station czy CH4 Reception.
- Scalenie i walidacja rekordów: `python3 games/the-genesis-order/tools/merge_translation_batches.py --batch games/the-genesis-order/translation/drafts/ui-01 --batch games/the-genesis-order/translation/drafts/hints/draft-hints-01.jsonl --batch games/the-genesis-order/translation/drafts/hints/draft-hints-02.jsonl --batch games/the-genesis-order/translation/drafts/hints/draft-hints-03.jsonl --out google_drive/the-genesis-order/translation/merged-ui-hints-03-final-2026-10-29.jsonl`. Wynik: **45 229 rekordów, 262 niepuste tłumaczenia, 131 chronionych wartości, 44 836 tłumaczalnych pól oczekujących**; SHA-256 lokalnego, ignorowanego scalenia `b2b26b968abc035ce6915491cc4a780c76c898c2d6c46c18eeb7a1cdce4c6c27`.
- `python3 -m unittest discover -s games/the-genesis-order/tests -v`: **35/35 passed**. Nie uruchamiano gry ani kodu gry; nie wykonywano `apply_translation.py --check` z hashami oryginałów, ponieważ pliki źródłowe gry nie są zsynchronizowane w bieżącym workspace. Brak testu Windows/runtime, renderingu i fontów; nie jest to patch ani zatwierdzony przekład.

## 2026-10-29 — dalsze tłumaczenie i osiem scen

- Kontynuowano tłumaczenie po stabilnych ID, bez zmian w `translation/export-v1/`. Nowe drafty scen: Common Event 492 (61 wierszy), 429 (84), 410 (79), 407 (117), 360 (61), 333 (62), 321 (124) i 379 (80) — **668 nowych, niepustych pól**. Zawierają m.in. sceny Arianny, Carol/Chloe, Kimberly/Lillian, Ella/Judy, Toma/Lillian/Eriki, Hannah/Chloe, Eriki i Judy; wszystkie pozostają wersjami roboczymi.
- Scalone z UI, wszystkimi wskazówkami, wyborami, nazwami/etykietami, wiadomościami, powtarzalnym dialogiem i pozostałymi scenami: `google_drive/the-genesis-order/translation/merged-tgo-12692-reviewed-2026-10-29.jsonl` (ignorowane przez Git). Wynik walidatora: **45 229 rekordów, 12 692 niepuste tłumaczenia, 131 chronionych, 32 406 oczekujących**; SHA-256 `c38f7512030da5a8ae2c09a4d6b872347380def724c8d58c0777fcecc026751e`. Po lekkiej redakcji kilku kwestii trzy poprawione drafty zostały ponownie scalone; poprzedni plik scalony pozostawiono bez nadpisania. Kanoniczny eksport i source ZIP nie zostały zmienione.
- SHA-256 nowych draftów: event 492 `0c5ca84d40bdd560a29986d6e5da3314ac455b5562972acafebeb422f5fd9570`; 429 `e0508c4a2d5452524015898f4afe844790fa6503152e2260a5316e5bc32fb9de`; 410 `6ef4e7c39ec40e271497956fe16538897fc0e5c353429f475150c051d6ee9a8d`; 407 `30e1f76ea9836d7b98e131b4f2155a0ae14dacf98e78ca83276b50ae13d2ce5a`; 360 `13e8959ee5550aefc0307c0f4f46a0bbfa3446ef12dad1ddb96a087058d39251`; 333 `cfc7ae026107a5975cd17af6ba15ef538874d600337370c04b17b428189675cf`; 321 `498a250b116a2a435754467fd0064a65e45ae06beaf6f16211f87879778c45f5`; 379 `277d48bc654e137130ec408d5027359872f60fa1a6ae3a230fbd06ae251a3ab6`.
- Pełne `unittest discover -s games/the-genesis-order/tests -v`: **35/35 passed**. Dodatkowo scalacz zweryfikował ID, źródła, tokeny, chronione wartości i konflikty wszystkich partii. Nie uruchamiano gry ani kodu; nie sprawdzano hashy oryginalnych plików w workspace; nie wykonywano testów Windows/runtime, fontów ani łamania UI. Potrzebna dalsza redakcja w kontekście; to nie jest patch ani zatwierdzona lokalizacja.

## 2026-10-29 — kontynuacja tłumaczeń do celu 25 000

- Po poprzednim zweryfikowanym merge (12 692 niepuste pola) dodano **3 015** nowych, niepustych draftów: 7 dodatkowych scen common events (**834 wiersze**; 20 plików scen łącznie / 1 922 wiersze), Common Event 25 (**304**), Map 20 (**985**), Map 31 (**700**) oraz wybrane eventy Map 3 (**192**). W Map 20 i Map 31 przetłumaczono wszystkie sensowne kwestie; statusowe komendy pozostawiono nietknięte.
- Wcześniejsze scalenie step5 zawierało literówkę `Twje`; poprawiono ją do `Twoje` w drafcie i builderze, po czym utworzono nowe, aktywne scalenie `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step6.jsonl` (step5 pozostawiono bez nadpisania). Step6 zweryfikowało **45 229 rekordów, 15 707 niepustych tłumaczeń, 131 chronionych rekordów i 29 391 tłumaczalnych pól oczekujących**. SHA-256 scalenia: `9490007f25c4fde2b1446560510a59ec823f8f0e92d55f5ce0cf40ef16b32440`. Do celu 25 000 pozostało 9 293 rekordów.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 OK**; `git diff --check`: bez błędów. Scalenie waliduje identyfikatory, zgodność źródeł, tokeny, chronione wartości i konflikty. Eksport kanoniczny oraz source ZIP pozostają niezmienione; nie uruchamiano gry ani kodu gry i nie budowano patcha. Wszystkie nowe tłumaczenia nadal wymagają redakcji.

## 2026-10-29 — dalsze partie Map 3, scalenie step7

- Dodano **343** niepuste tłumaczenia w Map 3: event 22 (102), event 31 (142) oraz eventy 41/47/56 (5/80/14). Łącznie partie Map 3 obejmują teraz 535 rekordów; audyt pozostałych niechronionych dialogów wskazuje 193 wiersze w evencie 45. Wcześniej dodane eventy 37 i 39 pozostają w zestawie.
- Aktualne pełne scalenie: `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step7.jsonl`; **45 229 rekordów, 16 050 niepustych tłumaczeń, 131 chronionych wartości i 29 048 tłumaczalnych pól oczekujących**. SHA-256: `be12215bcb5ee907962d3bfd3ee65d114e59db2c8604b58130651691d3036c59`. Do celu 25 000 pozostaje 8 950.
- Buildery Map 3 przechodzą `py_compile`; `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 OK**; `git diff --check`: bez błędów. Merge sprawdza ID, źródła, tokeny, chronione wartości i konflikty. Kanoniczny eksport i source ZIP pozostają niezmienione; nie uruchamiano gry ani runtime. Drafty wymagają redakcji.

## 2026-10-29 — scalenie step8, cel 30 000

- Użytkownik podniósł aktywny cel do **30 000** niepustych tłumaczeń. Dodano **630** nowych draftów: Map 3 event 45 (193), Map 24 (111), Map 23 (180), Map 116 event 89 (78) i Map 9 event 114 (68). Sensowne kwestie Map 3 są teraz pokryte; w Mapach 23, 24, 9 i 116 przetłumaczono tylko wybrane eventy, więc pozostaje tam dużo pracy.
- Nowe scalenie `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step8.jsonl` zweryfikowało **45 229 rekordów, 16 680 niepustych tłumaczeń, 131 chronionych wartości i 28 418 tłumaczalnych pól oczekujących**. SHA-256: `409a5d795b88883e0a0e17fb6b9ec686e84917c1a204a340f2b3d96d72ceef30`. Do celu 30 000 pozostaje 13 320.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 OK**; `git diff --check` i `py_compile` builderów: bez błędów. Merge sprawdza ID, zgodność źródeł, tokeny, chronione wartości i konflikty. Eksport kanoniczny i source ZIP bez zmian; nie uruchamiano gry/runtime ani nie tworzono patcha. Drafty wymagają redakcji.

## 2026-10-29 — scalenie step9, dalsze follow-upy

- Dodano kolejne **186** draftów: Map 24 (eventy 55 i 28: 57), Map 23 (event 44: 39), Map 116 (event 4: 57) i Map 9 (event 124: 33). Łącznie od step7 przybyło 816 rekordów; tłumaczenia nadal są robocze i wymagają redakcji.
- Scalenie `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step9.jsonl` zweryfikowało **45 229 rekordów, 16 866 niepustych tłumaczeń, 131 chronionych wartości i 28 232 tłumaczalne pola oczekujące**. SHA-256: `602131c2146ef9ecea113f9c7282e10199af552d1ba3af4dde891bc63fff2ee3`. Do celu 30 000 pozostaje 13 134.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 OK**; `git diff --check` i `py_compile` builderów: bez błędów. Eksport kanoniczny i source ZIP pozostają bez zmian; patcha gry nie utworzono.

## 2026-10-29 — scalenie step10, Common Event follow-ups

- Dodano **1 014** tłumaczeń dialogowych w 15 Common Events: 438 (74), 344 (72), 477 (68), 346 (70), 447 (70), 430 (68), 348 (68), 433 (68), 326 (65), 314 (66), 372 (66), 399 (65), 323 (64), 342 (65) i 364 (65). Są to drafty wymagające redakcji.
- Scalenie `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step10.jsonl` zweryfikowało **45 229 rekordów, 17 880 niepustych tłumaczeń, 131 chronionych wartości i 27 218 pól oczekujących**. SHA-256: `8eecd334a39b914ff6f738de0761bfcba11280b3e40a99b27c9ba8bcbf318619`. Do celu 30 000 pozostaje 12 120.
- Testy `unittest`: **35/35 OK**; buildery Common Events przechodzą `py_compile`, a `git diff --check` jest czysty. Eksport kanoniczny i source ZIP bez zmian; patcha gry nie utworzono.


## 2026-10-29 — scalenie step11, 50 Common Event follow-ups

- Po step10 dodano **2 730** roboczych tłumaczeń w 50 Common Events: 313 (48), 315 (49), 320 (58), 339 (58), 341 (61), 353 (44), 355 (50), 356 (61), 357 (56), 358 (51), 362 (50), 366 (40), 373 (62), 374 (47), 375 (52), 376 (64), 378 (47), 380 (63), 381 (45), 383 (48), 385 (62), 387 (65), 390 (49), 391 (64), 392 (54), 395 (62), 397 (55), 405 (50), 412 (52), 418 (63), 420 (53), 427 (53), 428 (48), 431 (48), 432 (64), 434 (58), 435 (60), 436 (62), 437 (58), 441 (56), 446 (52), 450 (51), 453 (59), 455 (48), 457 (62), 474 (48), 479 (53), 482 (48), 493 (60) i 495 (59). Wymagają redakcji.
- Scalenie `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl` zweryfikowało **45 229 rekordów, 20 610 niepustych tłumaczeń, 131 chronionych wartości i 24 488 pól oczekujących**. SHA-256: `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`. Do celu 30 000 pozostaje **9 390**. Step11 dodaje 2 730 względem step10; wcześniejsze tłumaczenia zachowano bez zmian.
- `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 OK**; nowe buildery przechodzą `py_compile`; walidator merge sprawdził zgodność ID i metadanych, tokeny, chronione wartości i konflikty. Kanoniczny eksport oraz source ZIP v1 pozostają bez zmian; patcha gry nie utworzono i gry/runtime nie uruchamiano.

## 2026-10-29 — kontynuacja przyrostu +10 000 po step11

- Zgodnie z najnowszą instrukcją rozpoczęto nowy przyrost **10 000** tłumaczeń względem step11: docelowy licznik to 30 610. Utworzono **3 097** świeżych, unikalnych rekordów draftów: Map 9 (309), Map 23 (230), Map 24 (222), Map 116 (240), Map 41 (302), Map 55 (255) oraz 40 Common Events (1 539); do celu pozostało 6 903 nowych rekordów. Lista eventów i liczebność partii są w `translation/drafts/README.md`.
- Partie pozostają oddzielne i niescalone; step11 to nadal ostatni pełny merge (20 610 niepustych tłumaczeń, 131 chronionych wartości, 24 488 oczekujących; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`). Wszystkie 3 097 nowe ID są unikalne, nie występują w tłumaczeniach step11, a ich pola źródłowe zgadzają się z eksportem kanonicznym i przechodzą walidację markup/control tokenów.
- Testy `unittest`: **35/35 OK**; wszystkie nowe buildery przechodzą `py_compile`, `git diff --check` jest czysty. Kanoniczny eksport i source ZIP v1 nie zostały zmienione; gry/runtime nie uruchamiano.


## 2026-10-29 — kontynuacja przyrostu +10 000, kolejne mapy i Common Events

- Po step11 utworzono dalsze **1 276** roboczych tłumaczeń: Map 54 (370), Map 6 (230), Map 26 (359) oraz 12 Common Events (277, 304, 316, 334, 349, 363, 368, 384, 396, 452, 456, 470; 317). Łączny przyrost po step11 wynosi teraz **4 373 rekordy w 67 plikach**; projekcja to 24 983 niepuste tłumaczenia i 5 627 brakujących do celu 30 610. Drafty pozostają osobne i niescalone.
- Domknięto wskazane kontrole Map 41: pytanie „Isn’t mouth and bottom… Isn’t it still sex?” ma spójną polską formę „Seks ustami i tyłkiem… Czy to nadal seks?”, a kwestię o ciężkiej pracy i ciele poprawiono na naturalne „Tak działa ciężka praca. Nie mam na sobie ani grama tłuszczu…”. Builder Map 41 ponownie wygenerował 302 rekordy.
- Audyt wszystkich 4 373 draftów potwierdził unikalne ID, brak nakładania z niepustymi tłumaczeniami step11, zgodność metadanych z kanonicznym eksportem, niepuste i przycięte tłumaczenia oraz poprawność markup/control. `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 passed**; nowe buildery przechodzą `py_compile`.
- Step11 pozostaje ostatnim pełnym scaleniem (20 610 tłumaczeń; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`). Kanoniczny eksport i source ZIP v1 nie zmieniono; nie scalano nowych partii, nie uruchamiano gry/runtime i nie tworzono patcha. Wszystkie tłumaczenia wymagają redakcji.


## 2026-10-29 — Map 44 mansion follow-ups

- Dodano **203** osobne drafty z sześciu eventów Map 44: 27 (73), 102 (31), 93 (28), 24 (24), 25 (24) i 51 (23). Łączny przyrost po step11 wynosi **4 576 rekordów w 68 plikach**; z step11 daje to 25 186 niepustych tłumaczeń, a do celu 30 610 pozostają 5 424.
- Audyt tych rekordów i wszystkich wcześniejszych draftów potwierdził unikalne ID, brak nakładania z niepustymi tłumaczeniami step11, zgodność metadanych kanonicznych oraz poprawność markup/control. Wszystkie partie pozostają rozdzielone i niescalone.
- Step11 nadal jest ostatnim pełnym merge (20 610 tłumaczeń; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`). Eksport kanoniczny i source ZIP v1 bez zmian; nie uruchamiano gry/runtime i nie tworzono patcha.


## 2026-10-29 — Map 82 i Common Event follow-ups

- Dodano **428** osobnych, niepustych draftów: Map 82 (328 w 14 eventach związanych z Channel 4) oraz Common Events 340, 354, 359, 440 i 122 (łącznie 100). Przyrost po step11 wynosi teraz **5 004 rekordy w 74 plikach**; z bazowym step11 daje to 25 614 tłumaczeń i pozostawia 4 996 do celu 30 610.
- Audyt wszystkich draftów potwierdził unikalność ID, brak nakładania z niepustymi tłumaczeniami step11, zgodność metadanych z eksportem kanonicznym, niepuste/przycięte tłumaczenia oraz poprawność markup/control. `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **35/35 passed**; nowe buildery przechodzą `py_compile`.
- Partie pozostają osobne i niescalone. Step11 pozostaje ostatnim pełnym merge (20 610 tłumaczeń; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`); kanoniczny eksport i source ZIP v1 nie zostały zmienione. Nie uruchamiano gry/runtime ani nie tworzono patcha.

## 2026-10-29 — osiągnięcie przyrostu +10 000 po step11

- Dodano **5 136** kolejnych draftów w 21 partiach map: Map 201 (316), 15 (299), 157 (290), 16 (284), 144 (283), 13 (266), 4 (258), 21 (252), 33 (250), 141 (247), 11 (244), 76 (243), 62 (235), 49 (227), 78 (223), 30 (219), 28 (214), 125 (199), 27 (197), 32 (195) i 87 (195). W Map 87 wygenerowano wszystkie 195 dopuszczonych wierszy; to powoduje przekroczenie celu o 140.
- Zredagowano 24 tłumaczenia w dziesięciu draftach map (11, 27, 30, 32, 49, 62, 76, 78, 125 i 141) oraz zsynchronizowano matching entries w builderach.
- Po step11 przybyło łącznie **10 140** unikalnych, osobnych draftów w **95 plikach**; razem z baseline step11 daje to projekcję **30 750** niepustych tłumaczeń. Cel +10 000 został przekroczony o 140. Wszystkie partie pozostają niescalone i nadal wymagają redakcji.
- Końcowy audyt nowych 5 136 wierszy potwierdził unikalność i brak nakładania z 25 614 wcześniej śledzonymi ID, zgodność metadanych ze źródłem kanonicznym, niepuste/przycięte tłumaczenia oraz zachowanie markup/control tokens. Wszystkie nowe buildery przechodzą `py_compile`; pełne testy `unittest`: **35/35 passed**.
- Kanoniczny eksport oraz source ZIP v1 pozostały bez zmian. Nie scalano nowych partii, nie uruchamiano gry/runtime ani nie tworzono patcha.

## 2026-10-29 — naturalny dialog Common Events, Map 151 i Map 19

- Dodano **1 169** osobnych draftów naturalnego dialogu: Common Events (**205 + 200 + 195 + 192 = 792**), Map 151 (**192 w 26 eventach**) i Map 19 (**185 w 20 eventach**). Wszystkie 792 zinwentaryzowane naturalne wiersze Common Events są już opracowane. Wcześniejszy roboczy podzbiór map zmniejszył się z 8 278 do **7 901** wierszy; nie jest to gwarancja, że każdy pozostały wiersz jest tekstem widocznym dla gracza.
- Łączny przyrost po step11 wynosi **11 309 unikalnych draftów w 101 plikach**; wraz z bazą step11 daje to **31 919 unikalnych niepustych tłumaczeń**. Kontynuujemy ku aspiracyjnemu celowi 45 000, ale wypełniamy i liczymy wyłącznie rzeczywisty tekst gracza. Wcześniejszy teoretyczny pułap po wyłączeniu 131 chronionych rekordów i 3 742 tokenów sterujących wynosi 41 356; od obecnego stanu może więc pozostać najwyżej 9 437 kwalifikujących się rekordów, a faktyczny wynik może być niższy.
- Audyt nowych 1 169 rekordów potwierdził zgodność metadanych ze źródłem kanonicznym, niepuste tłumaczenia, poprawność markup/control tokens, brak ID chronionych, brak slash-prefixed komend, brak duplikatów w nowych partiach i brak overlapu z wcześniejszymi niepustymi draftami. Dodano test regresyjny tych właściwości; pełne `unittest`: **36/36 OK**, a wszystkie sześć builderów przechodzi `py_compile`.
- Step11 pozostaje ostatnim pełnym merge (20 610 tłumaczeń; SHA-256 `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`). Partie pozostają osobne i niescalone; kanoniczny eksport i source ZIP v1 bez zmian. Nie uruchamiano gry/runtime ani nie tworzono patcha.

## 2026-10-29 — Map 114 story follow-ups

- Dodano **178** osobnych draftów naturalnego dialogu z 10 eventów Map 114. Żaden z ich stabilnych ID nie występował wcześniej w niepustych draftach.
- Łącznie po step11 jest teraz **11 487** świeżych, unikalnych draftów w **102 osobnych plikach**, co daje projekcję **32 097** niepustych tłumaczeń. Pozostały roboczy podzbiór naturalnego dialogu map liczy **7 723** wiersze; kwalifikowalność każdego wymaga oceny, więc nie jest to obietnica osiągnięcia 45 000.
- Builder Map 114 przechodzi `py_compile` i utworzył batch 178 wierszy, odmawiając nadpisania istniejącego pliku. Pełne `unittest`: **36/36 OK**, w tym regresyjny audyt wszystkich siedmiu batchy; wszystkie siedem builderów przechodzi `py_compile`. Kanoniczny eksport i source ZIP v1 pozostają bez zmian; partie są odseparowane i wymagają redakcji.

## 2026-10-29 — Map 203 courtroom follow-ups

- Dodano **171** osobnych draftów naturalnego dialogu z 8 eventów Map 203 (rozprawa sądowa i dalsza rozmowa). Tłumaczą kwestie wypowiadane w scenie, bez nagłówków sterujących.
- Łączny przyrost po step11 wynosi teraz **11 658 unikalnych draftów w 103 osobnych plikach**, co daje projekcję **32 268** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **7 552** wiersze; każdy nadal wymaga oceny, czy faktycznie jest tekstem gracza.
- Builder Map 203 przechodzi `py_compile`, utworzył batch 171 wierszy i odmawia nadpisania istniejącego pliku. Pełne `unittest`: **36/36 OK**; regresyjny audyt wszystkich ośmiu batchy potwierdził zgodność z kanonicznym eksportem, kompletność, zachowanie tokenów i brak overlapu. Wszystkie osiem builderów przechodzi `py_compile`. Partie pozostają oddzielne i niescalone; kanoniczny eksport i source ZIP v1 bez zmian.

## 2026-10-29 — Map 61 gym i Map 25 dinner follow-ups

- Dodano **304** osobne drafty naturalnego dialogu: Map 61 (**156 w 15 eventach**) oraz Map 25 (**148 w 16 eventach**). Obie mapy mają oddzielne pliki JSONL, chociaż wspólny builder generuje je niezależnie.
- Łączny przyrost po step11 wynosi teraz **11 962 unikalne drafty w 105 osobnych plikach**, co daje projekcję **32 572** niepustych tłumaczeń. Pozostały roboczy podzbiór naturalnego dialogu map liczy **7 248** wierszy; każdy nadal wymaga oceny pod kątem tekstu widocznego dla gracza.
- Builder Map 61/25 przechodzi `py_compile`, wygenerował dwa oddzielne pliki i odmawia nadpisania istniejących batchy. Pełne `unittest`: **36/36 OK**; audyt wszystkich dziesięciu najnowszych batchy potwierdził 1 822 unikalne ID, brak overlapu, zgodność metadanych z kanonicznym eksportem i poprawność markup/control tokens. Wszystkie dziewięć builderów przechodzi `py_compile`. Kanoniczny eksport i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — Map 34 commissioner follow-ups

- Dodano **143** osobne drafty naturalnego dialogu z 5 eventów Map 34, obejmujące rozmowy w komisariacie i sprawę katedry. W dialogu nie tłumaczono nagłówków sterujących.
- Łączny przyrost po step11 wynosi teraz **12 105 unikalnych draftów w 106 osobnych plikach**, co daje projekcję **32 715** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **7 105** wierszy; każdy nadal wymaga oceny pod kątem tekstu widocznego dla gracza.
- Builder Map 34 przechodzi `py_compile` i odmawia nadpisania istniejącego batcha. Pełne `unittest`: **36/36 OK**; audyt wszystkich jedenastu najnowszych batchy potwierdził 1 965 unikalnych ID, brak overlapu, zgodność metadanych z kanonicznym eksportem i poprawność markup/control tokens. Wszystkie dziesięć builderów przechodzi `py_compile`. Kanoniczny eksport i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — Map 101 Heather sleepover follow-ups

- Dodano **142** osobne drafty naturalnego dialogu z 14 eventów Map 101, obejmujące rozmowę Heather, Chloe, Judy i 1Hero. Zachowano osobny plik JSONL; nie dodawano tekstów sterujących.
- Łączny przyrost po step11 wynosi teraz **12 247 unikalnych draftów w 107 osobnych plikach**, co daje projekcję **32 857** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **6 963** wiersze; każdy nadal wymaga oceny pod kątem tekstu widocznego dla gracza.
- Builder Map 101 przechodzi `py_compile` i odmawia nadpisania istniejącego batcha. Pełne `unittest`: **36/36 OK**; audyt wszystkich 12 najnowszych batchy potwierdził 2 107 unikalnych ID, brak overlapu, zgodność metadanych z eksportem kanonicznym i poprawność markup/control tokens. Wszystkie 11 builderów przechodzi `py_compile`. Eksport kanoniczny i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — Map 12 Arianna and church follow-ups

- Dodano **140** osobnych draftów naturalnego dialogu z 6 eventów Map 12: rozmowy z siostrą Judy, Arianną i dalsza scena planowania operacji. Pozostawiono dialog rozdzielony od poprzednich partii.
- Łączny przyrost po step11 wynosi teraz **12 387 unikalnych draftów w 108 osobnych plikach**, co daje projekcję **32 997** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **6 823** wiersze; każdy nadal wymaga oceny pod kątem tekstu widocznego dla gracza.
- Builder Map 12 przechodzi `py_compile` i odmawia nadpisania istniejącego batcha. Pełne `unittest`: **36/36 OK**; audyt wszystkich 13 najnowszych batchy potwierdził 2 247 unikalnych ID, brak overlapu, zgodność metadanych z eksportem kanonicznym i poprawność markup/control tokens. Wszystkie 12 builderów przechodzi `py_compile`. Eksport kanoniczny i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — Map 94 church roof and Tasha follow-ups

- Dodano **139** osobnych draftów naturalnego dialogu z 16 eventów Map 94, obejmujących rozmowę o przecieku w kościele i dalszy wątek Tashy. Dialog pozostaje w osobnym pliku i nie zmienia eksportu źródłowego.
- Łączny przyrost po step11 wynosi teraz **12 526 unikalnych draftów w 109 osobnych plikach**, co daje projekcję **33 136** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **6 684** wiersze; kwalifikowalność każdego wymaga oceny.
- Builder Map 94 przechodzi `py_compile` i odmawia nadpisania istniejącego batcha. Pełne `unittest`: **36/36 OK**; audyt wszystkich 14 najnowszych batchy potwierdził 2 386 unikalnych ID, brak overlapu, zgodność metadanych z eksportem kanonicznym i poprawność markup/control tokens. Wszystkie 13 builderów przechodzi `py_compile`. Eksport kanoniczny i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — Map 52 Ella and Chloe follow-ups

- Dodano **135** osobnych draftów naturalnego dialogu z 7 eventów Map 52, z dialogami Elli, Chloe i Erica. Zachowano wyłącznie linie wypowiadane przez postacie; partie pozostają odseparowane.
- Łączny przyrost po step11 wynosi teraz **12 661 unikalnych draftów w 110 osobnych plikach**, co daje projekcję **33 271** niepustych tłumaczeń. Roboczy podzbiór naturalnego dialogu map ma **6 549** wierszy; kwalifikowalność każdego wymaga oceny.
- Builder Map 52 przechodzi `py_compile` i odmawia nadpisania istniejącego batcha. Pełne `unittest`: **36/36 OK**; audyt wszystkich 15 najnowszych batchy potwierdził 2 521 unikalnych ID, brak overlapu, zgodność metadanych z eksportem kanonicznym i poprawność markup/control tokens. Wszystkie 14 builderów przechodzi `py_compile`. Eksport kanoniczny i source ZIP v1 pozostają bez zmian; partie są osobne i niescalone.

## 2026-10-29 — pełny audyt pokrycia, koniec statycznej prozy i blokada sygnatury markup

- **Cel:** ustalić odtwarzalnie, ile tekstu naprawdę pozostało, zamiast sumować kolejne partie i projekcje.
- **Narzędzia:** nowe `tools/audit_draft_coverage.py` (SHA-256 `2ec6b80591967379620390e03d5e59ce2eb5232c5b6a50f5e6da4b99e52c7396`) i `tools/markup_signature.py` (`a59121ab6282e16120bc581754d35fc5f11b338d158683800da7e26653216cc8`). Oba tylko czytają JSONL; nie uruchamiają kodu gry.
- **Polecenie:** `python3 games/the-genesis-order/tools/audit_draft_coverage.py --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md`.
- **POTWIERDZONE — pokrycie:** 45 229 rekordów kanonicznych; 425 plików draftów (w tym `hints/` i `ui-01/`), 45 742 wiersze; **39 821** unikalnych ID z niepustym tłumaczeniem; **131** chronionych `keep_source_value`; **5 277** pustych rekordów do rozstrzygnięcia; **40** konfliktów niepustych wariantów; **616** tłumaczeń identycznych ze źródłem (po odfiltrowaniu imion, wykrzyknień i linków: 37 wielowyrazowych, wszystkie to nazwy własne).
- **POTWIERDZONE — rozkład pustych rekordów:** 3 742 komendy `/...` w `custom_dialogue`; 1 072 rekordy bez ani jednej litery po usunięciu tokenów; 234 wiersze list nazw w credits; 91 imion/nazw/podpisów galerii; 7 wypełniaczy „Text goes here”; 7 kodów (`ECU`, `TEXT`, `G`, `U/L/C/S`); 94 zablokowane sygnaturą markup; 30 do decyzji właściciela.
- **POTWIERDZONE — błąd odkrywania plików:** dotychczasowe `input_paths` w `markdown_translation.py` używało `glob("*.jsonl")`, więc pełne scalenie katalogu `drafts/` pomijało 10 plików w `hints/` i `ui-01/` (830 tłumaczeń). Zmieniono na `rglob` i dodano test `test_nested_batch_folders_are_found`.
- **POTWIERDZONE — blokada sygnatury v1:** tokenizer `TOKEN_RE` skleja tag bez argumentu z następnym słowem (`\fbCraft`, `\fbYou`). `validate_record` wymaga identycznych tokenów, więc 94 rekordy `native_message` z mapy `Crafting` (Map 46) nie mogą mieć polskiego tłumaczenia. `tools/markup_signature.py` porównał 45 229 rekordów: v1 i proponowana v2 różnią się **wyłącznie na tych 94** i tylko przez rozdzielenie `\fb` od pierwszego słowa. Gotowe zwrotki zapisano w `translation/pending/crafting-ui-map46-01.jsonl` (94 wiersze, SHA-256 `98967b4e0d8f07ad72dd8db78c5676d37fa8014d349d1627be85783b936481a5`); decyzja w ADR 002 jako **propozycja**.
- **Nowa partia:** `translation/drafts/phone-select-item-fragment-01.jsonl` (1 rekord, SHA-256 `18b67a4a8e47e12e141e99bce7bc6df894ebe1389e267417800b602ed3c676ee`): `He’s going to be<br>` → `On będzie<br>` w wątku wiadomości „Charles W” (CE17 „PHONE - Select Item”, `command_index` 430), spójnie z sąsiednim `pissed, ya know?` → „Wkurzony, kumasz?”. To ostatnia statyczna proza w eksporcie.
- **Do decyzji — `Channel 4`:** starsza `inventory-names-01.jsonl` ma „Kanał 4”, a nowsze `inventory-names-02.jsonl` i `map-labels-01.jsonl` zostawiają `Channel 4`. Glosariusz roboczo zachowuje markę „Channel 4” w wskazówkach o lokacji, więc nie traktujemy tego automatycznie jako błąd; to wybór właściciela (marka vs. tłumaczenie). Nie zmieniano plików etykiet — są objęte osobnym PR #5; pozycja jest w `COVERAGE_AUDIT.md` i w handoffie.
- **Walidacja:** `python3 -m unittest discover -s games/the-genesis-order/tests -q` → **51/51 OK** (36 wcześniejszych + 15 nowych); `py_compile` nowych narzędzi bez błędów; `git diff --check` czysty.
- **NIEZNANE:** czy `\fb` jest tagiem stylu, który gra realnie renderuje — nie ma lokalnych źródeł JS, więc sprawdzenie wymaga testu w grze po stronie właściciela. Nie zmieniono eksportu kanonicznego, source ZIP, walidatora ani żadnego pliku gry; nie uruchamiano gry ani kodu gry.

## 2026-10-29 — pełny audyt i uzgodnienie korpusu draftów

- **Cel:** rozstrzygnąć rozjazd w aktualnych licznikach, konflikty wersji oraz liczbę pustych pól po wszystkich dotychczasowych partiach; nie zmieniać kanonicznego eksportu ani źródeł gry.
- **Wejścia:** `translation/export-v1/` (25 JSONL, 45 229 rekordów) i wszystkie 424 śledzone pliki JSONL z `translation/drafts/` (45 741 wystąpień wierszy, 41 277 różnych ID). Walidacja odbyła się przez `tools/merge_translation_batches.py` na wszystkich plikach; tymczasowy pełny wynik usunięto po audycie.
- **Konflikty:** wykryto 40 ID `map_label` z dwiema różnymi niepustymi wersjami. Nowszy `inventory-names-02.jsonl` i jego kopia `map-labels-01.jsonl` zawierały ten sam wariant, więc 40 przestarzałych pól w `inventory-names-01.jsonl` uzgodniono z nowszą wersją. SHA-256 uzgodnionego `inventory-names-01.jsonl`: `2980b507c71b027c7904d382ff12c191e9a24807b335218097816de519c3c192`. Po zmianie nie ma konfliktów między niepustymi tłumaczeniami. 468 nakładających się wierszy zawierały jedną pustą i jedną wypełnioną wersję; scalacz prawidłowo bierze tylko niepustą.
- **Wynik scalania:** 45 229 rekordów kanonicznych, 39 820 unikalnych niepustych tłumaczeń, 131 chronionych rekordów `keep_source_value` oraz 5 278 pustych niechronionych pól. Poprzednia projekcja 39 931 zawyżała wynik o 111 powtórzonych ID. Z pustych niechronionych pól 3 742 to rozpoznane slash-prefixed komendy `custom_dialogue`; górny limit do ręcznej klasyfikacji wynosi 1 536, ale nie jest to gwarantowany zakres tłumaczenia.
- **Pozostałe do oceny:** potwierdzono co najmniej 94 puste, widoczne wiersze UI craftingu na Map 46: po 47 wystąpień `Craft this item?` i `You have items missing from this recipe.`; dodatkowe puste rekordy wymagają klasyfikacji i nie wszystkie są tekstem do tłumaczenia. W tym audycie nie dodawano nowych przekładów.
- **Kontrole:** nie znaleziono nieznanych ID ani zmian metadanych względem źródła kanonicznego; `merge_translation_batches.py` zwalidował kompletność/tokeny wszystkich wypełnionych rekordów. Dodano test integracyjny pełnego korpusu, który chroni przed ponownym pojawieniem się konfliktów i błędnych liczników. `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **37/37 OK**; `git diff --check` czysty. Nie uruchamiano gry/runtime i nie sprawdzano hashy względem nieobecnych lokalnie assetów źródłowych.

## 2026-10-29 — domknięcie audytu luk w tekście gracza

- Dodano `native-message-map46-crafting-01.jsonl`: **94** tłumaczenia widocznych promptów UI craftingu z Map 46, z zachowaniem tokenów formatowania. Wyniki: `Craft this item?` → `Wytworzyć ten przedmiot?`; `You have items missing from this recipe.` → `Brakuje ci przedmiotów potrzebnych do tego przepisu.` Builder obejmuje wszystkie eventy Map 46, a nie tylko Event 1.
- Dodano `visible-ui-remaining-01.jsonl`: **9** ostatnich naturalnych tekstów UI — siedem powtórzeń jawnie renderowanego placeholdera z TEST MAP; druga część wiadomości telefonu `He’s going to be` → `Będzie` (ciąg dalszy istniejącej linii `Wkurzony, kumasz?`); oraz literal kanału telefonu `TEXT` → `TEKST`.
- Pozostałe puste rekordy ponownie sprawdzono po kategorii i widocznym źródle. Nie znaleziono kolejnych zwykłych angielskich fraz gracza. Pozostały m.in. nazwy/credits/handle użytkowników, symboliczne lub numeryczne opcje, metadane map używane przez edytor, właściwe nazwy i skróty, dane dynamiczne, wyłącznie formatowanie rendererów, kontrolne slash-strings oraz wielokropki/interpunkcja.
- Pełna reconciliacja **426** batchy: **45 229** rekordów kanonicznych, **39 923** unikalne niepuste tłumaczenia, **131** wartości chronionych i **5 175** pustych wartości niechronionych; brak konfliktowych niepustych wariantów. Eksport źródłowy i source ZIP pozostały niezmienione; nie uruchamiano gry/runtime ani kodu z archiwów referencyjnych.
- Zaktualizowano oczekiwaną liczbę batchy i sumy corpus w teście integracyjnym. `python3 -m unittest discover -s games/the-genesis-order/tests -q`: **39/39 OK**; `py_compile` buildera i `git diff --check` przeszły.

## 2026-10-29 — milestone patch POC i Czytanka PL v1

- Po końcowym audycie scalenie **427** partii obejmuje 45 229 rekordów: 39 926 niepustych tłumaczeń, 131 jawnie chronionych, 5 172 zachowane nielokalizowalne i 0 nierozstrzygniętych rekordów do tłumaczenia.
- Zbudowano `translation/packages/TGO_PL_translation_patch_POC_v0.1.1.zip` z 39 926 tłumaczeniami, fingerprintami 238 źródeł, backup/restore i one-click patcherem. SHA-256 `4dc807024466582b68a59e129d212dc2aa52e0bcf4dcd81c3445576b8d84513b`. Wcześniejszy zip `v0.1.0` wycofano; aktualny ZIP sprawdzono statycznie, bez plików gry.
- Zbudowano generator `tools/build_readalong.py` i output `reading/v1/`: pełny polski skrypt, epizody z dialogami/mówcami/warunkami/wyborami, `reading_order.tsv` oraz indeksy 55 mówców i 291 lokacji. Po optymalizacji grafu wywołań Common Events build trwa około 9 s; wynik: 4 394 epizody (4 134 map/event/page + 260 CE), 221/291 map potencjalnie osiągalnych od startu. Mówców nieustalonych nie zgaduje. README jasno stwierdza, że BFS i kolejność Common Events są przybliżone, a nie kanoniczne.
- Czytanka ZIP: `translation/packages/TGO_readalong_PL_v1.zip`, 4 399 wpisów, SHA-256 `3239527786f1ac28064920fb45c2273941b0914cb8ed636b1c68d2975b0eb244`; sprawdzono sidecar SHA-256, CRC i wymagane pliki.
- Dodano 5 testów generatora (placeholdery, mówcy, etykieta wyboru, osiągalność przez CE, indeksy). Pełny zestaw: **54/54 OK**; `py_compile` oraz kontrole ZIP przechodzą. Pierwszy nieoptymalizowany przebieg przekroczył 180 s; zastąpiono rekurencyjne powtarzane przejścia preobliczeniem grafu Common Events i iteracyjnym wyznaczaniem kolejności, po czym pełny build zakończył się poprawnie.
- Nie uruchamiano gry ani runtime. Patcher nie był testowany na Windows, nie weryfikowano fontów/łamania tekstu ani instalacji docelowej; milestone’y są gotowe statycznie jako POC, wymagają dalszego QA przed publikacją.

## 2026-10-29 — odzyskanie pracy poprzedniego agenta i domknięcie korpusu

- **Kontekst:** poprzedni agent zbudował pełny korpus 427 partii, patcher POC i Czytankę, ale wypchnął do Git tylko wczesny stan. Praca istniała wyłącznie w patchu `01a188a8…` i dwóch ZIP-ach na Google Drive. Szczegóły i hashe: `docs/RECOVERY_2026-10-29.md`.
- **Metoda:** patch nałożony na `2e5e2e5` w osobnym `git worktree` (`git apply --exclude='…/packages/*.zip'`; ZIP-y to w patchu tylko znaczniki binarne i pochodzą z Drive). Z odzyskanego drzewa przeniesiono narzędzia, testy, patcher, Czytankę, raporty, 259 builderów i 3 nowe partie; ZIP-y dodano z Drive po zgodności z sidecarami `.sha256`.
- **Niezależna weryfikacja, nie na słowo:**
  - świeże scalenie **427** draftów → 45 229 rekordów, **39 926** niepustych, **131** chronionych, **5 172** zachowanych w źródle, **0** konfliktów;
  - payload scalony ma SHA-256 `e2898d6f33399779f3703831287488293f32ec0cec64a06acfb37c68d154311e` — **identyczny** z `payload/translations.jsonl` w ZIP-ie patcha i z manifestem, więc artefakt nie zawiera nic spoza Git;
  - `patcher.py`, `APPLY.bat`, `COFNIJ.bat` i cztery narzędzia w ZIP-ie są **bajt w bajt** zgodne z repo; jedyna różnica to `README_PL.md` z wstrzykniętym licznikiem 39 926;
  - `reading/v1` w patchu jest **identyczne** z `TGO_readalong_PL_v1.zip` (4 399/4 399 plików);
  - `inventory-names-01.jsonl` jest **identyczny** z wersją z PR #5 (SHA-256 `2980b507…`) — 40 etykiet map, w tym decyzja o marce `Channel 4`, jest już w tym PR;
  - 259 builderów przechodzi `py_compile`; skan `subprocess|urllib|socket|eval` nie znalazł wywołań (jedno trafienie to słowo „socket” w tłumaczeniu).
- **Sprzątanie własnego obejścia:** usunięto `translation/pending/`, `tools/markup_signature.py` i `tests/test_markup_signature.py`. Odzyskana reguła `translation_tokens_match()` rozwiązuje ten sam problem w samym walidatorze, więc ADR 002 przyjęto jako **wariant B** (bez tworzenia `export-v2`, bez zmiany kanonicznego eksportu). Usunięto też mój draft `phone-select-item-fragment-01.jsonl`, bo ten rekord jest w odzyskanym `visible-ui-remaining-01.jsonl` — dwa pliki dałyby konflikt.
- **Dokumentacja:** nowe `docs/EDITORIAL_DECISIONS.md` (11 pozycji do decyzji: tytuł gry, `Channel 4`, 40 etykiet map, warianty craftingu i telefonu, `TEXT`/`TEKST`, odmiana imion, placeholdery TEST MAP, fonty) i `docs/RECOVERY_2026-10-29.md`; zaktualizowane `STATUS.md`, `HANDOFF_NEXT_AGENT.md`, `ROADMAP_TRANSLATION.md`, `AGENTS.md`, `README.md` (projektu i repo), `PROJECTS.md`, `TRANSLATION_FORMAT.md`, `drafts/README.md`. Historyczne wpisy dziennika zachowane bez zmian.
- **Kontrole:** `python3 -m unittest discover -s games/the-genesis-order/tests -q` → **69/69 OK**; `tools/audit_translation_coverage.py` → `status: complete`; `audit_draft_coverage.py` → 427 plików, 0 konfliktów. Nie uruchamiano gry ani kodu gry.
- **Supersesja wcześniejszych wpisów:** liczby 36/36, 51/51 i 54/54 w powyższych wpisach są zapisem chwili, w której je uzyskano. Wpisy z `translation/pending/`, `tools/markup_signature.py` i propozycją ADR 002 opisują stan sprzed decyzji; obowiązuje wariant B opisany w ADR 002 i w wpisie wyżej.

## 2026-10-29 — analiza spójności redakcyjnej korpusu (po odzyskaniu)

- **Cel:** sprawdzić, nie zakładać. Każde twierdzenie w `EDITORIAL_DECISIONS.md` zostało zweryfikowane w korpusie, nie przepisane z pamięci.
- **Odmiana imion (POTWIERDZONE, policzone):** imiona na `-a` są odmienione tylko w części wystąpień — Erica 178 mianownik / 140 odmienionych, Andrea 186/108, Ella 175/88, Melissa 139/46, Arianna 61/26, Toma 88/88, Diana 42/11. Imiona na spółgłoskę (`Chloe` 449, `Lilith` 106, `Carol` 325, `Hannah` 606, `Judy` 514) nie mają ani jednej formy odmienionej. To największy konkretny dług redakcyjny: w korpusie stoją obok siebie „Klucz do głównej sypialni Andrei” i „z Andrea”.
- **`Channel 4` (POTWIERDZONE):** we wszystkich **63** przetłumaczonych wystąpieniach nazwa zostaje po angielsku („w wieżowcu Channel 4”), a etykieta mapy to dosłownie `Channel 4`. W draftach **nie ma już żadnego** „Kanał 4”.
- **Tytuł gry (POTWIERDZONE):** `system.gameTitle` → „Zakon Genesis”, ale w scenie „SCN - Ending” zdanie `The Genesis Order will continue being updated on the 2nd and 15th…` zachowuje angielską nazwę — to jedyna niespójność tej decyzji.
- **Etykiety map (POTWIERDZONE):** `inventory-names-01.jsonl` zawiera wszystkie **291** etykiet (288 przetłumaczonych, 3 bez zmian: `Channel 4`, `START`, `Test`); w ostatnim uzgodnieniu przepisano **40** wierszy.
- **Stuby mapy testowej (POTWIERDZONE):** 7 rekordów `Text goes here` to `native_message` z TEST MAP EV001, a `TEXT` to `phone_text` z TEST MAP EV021 — oba to placeholdery dewelopera, nie produkcyjne UI. Wpływa to na priorytet decyzji R-07/R-08.
- **Crafting i telefon (POTWIERDZONE):** 94 rekordy Map 46 mają spójne „Wytworzyć ten przedmiot?” / „Brakuje ci przedmiotów potrzebnych do tego przepisu.”; fragment telefonu `He’s going to be<br>` poprzedza linię `pissed, ya know?` → „Wkurzony, kumasz?”, więc razem czytają się jako „Będzie wkurzony, kumasz?”.
- **Wynik:** `docs/EDITORIAL_DECISIONS.md` przepisany na podstawie tych pomiarów (11 pozycji, każda z dowodem i rekomendacją). Progu „wszystko przetłumaczone” to nie zmienia: 39 926 tłumaczeń, 0 nierozstrzygniętych. Nie zmieniano żadnego draftu ani eksportu.

## 2026-10-29 — manifest i fingerprinty źródeł wyjęte z ZIP-a do Git

- **Powód:** przegląd kompletności ZIP-a patcha POC wykazał, że `payload/patch_manifest.json` (1,6 KB) i `payload/source_fingerprints.json` (21,5 KB, 238 hashy `data/*.json`) istniały **wyłącznie w archiwum**. Pozostałe wpisy ZIP-a są albo identyczne z repo (patcher, BAT-y, narzędzia), albo odtwarzalne (translations.jsonl ze scalenia draftów), a README różni się tylko wstrzykniętym licznikiem.
- **Działanie:** oba pliki wyodrębniono bez modyfikacji do `translation/reports/patch_manifest_v0.1.1.json` i `translation/reports/source_fingerprints_v0.1.1.json`. SHA-256 fingerprintów `22aaa094c93fc85d8c40082ed23c634082220744130914914926ab33cf005d23` zgadza się z polem `fingerprints_sha256` w manifeście, więc to autentyczny artefakt, nie rekonstrukcja.
- **Znaczenie:** to jedyna kopia dająca się zweryfikować tylko przy źródłach gry; bez niej patcher nie miałby czym potwierdzić wersji builda, a strata ZIP-a oznaczałaby utratę danych nieodtwarzalnych. Teraz każdy bajt ZIP-a jest albo w Git, albo dowodnie odtwarzalny z Git.
- **Kontrole:** `unittest` 69/69 OK; brak zmian w draftach i eksporcie.

## 2026-10-29 — testy artefaktów: ZIP ↔ repo ↔ liczby

- **Problem:** spójność, którą udowodniłem jednorazowo przy odzyskiwaniu (sidecar = archiwum, manifest = payload, Czytanka w ZIP-ie = `reading/v1/`), nie była niczym pilnowana. Kolejna przebudowa mogła ją cicho zepsuć.
- **Działanie:** nowy `tests/test_patch_artifacts.py` (9 testów, ~1,7 s) czyta wyłącznie archiwa i pliki repo, bez uruchamiania jakiegokolwiek kodu z ZIP-ów:
  - sidecar `.sha256` zgadza się z bajtami obu ZIP-ów;
  - żaden ZIP nie zawiera assetów gry (`.rpgmvp`, `.rpgmvo`, `.exe`, `.dll`, audio itd.);
  - `translations_sha256`, `fingerprints_sha256` i `translation_coverage_sha256` z manifestu zgadzają się z payloadem, który ZIP faktycznie zawiera;
  - kopie w `translation/reports/` są identyczne z payloadem (fingerprinty i pokrycie po bajtach, manifest po polach);
  - 238 fingerprintów to poprawne SHA-256, a liczba wierszy w `translations.jsonl` i ich unikalność zgadzają się z manifestem;
  - manifest jasno deklaruje `runtime_tested: false`, `game_files_included: false` i `pending_untranslated_record_count: 0`;
  - **wszystkie 4 399 wpisów Czytanki jest bajt w bajt równe plikom z `reading/v1/`**, a epizodów jest 4 394.
- **Wynik:** `python3 -m unittest discover -s games/the-genesis-order/tests -q` → **69/69 OK**. Testy pinują teraz nie tylko liczby korpusu (427 partii, 45 229/39 926/131/5 172 w teście scalania), ale też to, że opublikowane paczki odpowiadają zawartości Git.

## 2026-10-29 (wieczór) — decyzje właściciela: R-01, R-02, R-07, R-08, R-09 + przebudowa obu paczek

- **Decyzje wykonane:** R-01 (tytuł gry zawsze po angielsku), R-02 (`Channel 4` bez zmian — korpus już to spełniał), R-07 (7 placeholderów `Text goes here<br>` z TEST MAP wraca po angielsku), R-08 (`TEXT` z TEST MAP wraca), R-09 (ujednolicenie odmiany imion na `-a`). R-11 (fonty) wstrzymane decyzją właściciela.
- **Bramka pokrycia:** po cofnięciu 9 tłumaczeń audyt zgłosiłby 9 rekordów „unresolved” i builder odmówiłby budowy. Zamiast wyjątku szerokiego dodano w `audit_translation_coverage.py` jawną, wąską funkcję `owner_keep_source()`, która zwraca powód z ID decyzji (`owner_decision_R01_brand_title_kept_in_english`, `…R07…`, `…R08…`). Reguła R-07 działa **tylko** dla `map_name == "TEST MAP"`; cztery testy pilnują, że te wyjątki nie rozlewają się na inne kategorie.
- **R-09 — narzędzie, nie tłumaczenie:** `tools/unify_name_declension.py` odmienia tylko formy rozstrzygalne składniowo (wołacz po przecinku / cała kwestia / początek zdania; dopełniacz po rzeczowniku lub przyimku). Wynik: **383 wystąpienia w 380 rekordach, 148 plików**; 628 form niejednoznacznych zostaje w mianowniku (raport: `translation/reports/declension_r09_report.json`). Idempotencja i brak wpływu na znaczniki `\c[n]` mają testy. Kontrola krzyżowa: to samo narzędzie uruchomione na draftach z `git archive HEAD` daje bajt w bajt bieżący korpus, więc wynik nie zależy od kolejności przebiegów.
- **Czytanka (decyzja właściciela):** `1Hero` → **Mox** (17 032 wystąpienia), kolejne kwestie dialogowe bez pustej linii między sobą, `chronological_script_PL.md` bez linii `<sub>Źródłowe ID…</sub>` (w `episodes/` zostają jako ślad). Ponieważ sandbox nie ma dostępu do `data/` gry (okrojone wyjście sieciowe), builder dostał tryb offline: `--previous-order` i `--locations-index` dziedziczą numerację rozdziałów i indeks 291 lokacji z wydania v1. Efekt: 4 394 rozdziały, 221/291 map, **386 bloków różnicy** względem poprzedniego wydania — wszystkie to odmiana imion, żadna kwestia nie zniknęła.
- **Artefakty:** patch `TGO_PL_translation_patch_POC_v0.1.1.zip` SHA-256 `914e73fa9e9022aabbe9a5fcb5dfef553d6100b6f266e8fde9e256f8344e6789` (3 740 219 B, 39 917 tłumaczeń, 238 fingerprintów — `fingerprints_sha256` bez zmian `22aaa094…`, bo źródła gry się nie zmieniły); Czytanka `TGO_readalong_PL_v1.zip` SHA-256 `74a3b096a07e92de32f6b5ac42e9f297cf4a33adf2db21fdd92359f60ec04c4f`.
- **Odtwarzalność:** nowy test w `tests/test_merge_translation_batches.py` scala drafty z Git i porównuje SHA-256 payloadu z manifestem → `d90191df69ca4194b6d59071ce6a4a40a3dfa5ac52c5a5b20f5ff9b726a44458`. Testy: **88/88 OK**.
- **Nie zrobiono:** nic nie uruchomiono w Windows ani w grze; R-11 (glify) nadal NIEZNANE i nadal blokuje sens całości.
