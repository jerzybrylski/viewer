# Dziennik eksperymentów — The Genesis Order

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
- Konfiguracja aktywnego `YEP_LoadCustomFonts` wskazuje 10 nazw plików w `www/fonts/`; inwentarz wykazał 11 fontów. Folder `www/fonts/` nie znajduje się w przesłanym `www` (w Drive są tylko `data` i `js`).
- Nie uruchamiano JS, gry ani runtime; JSON parsowano statycznie. Nie skopiowano żadnego assetu do Git.
- **Następny krok:** użytkownik dosyła wyłącznie fonty `.ttf`/`.otf` z `www/fonts/`; następnie pełniejszy eksport tekstów może być budowany z JSON-ów bez pobierania mediów.
