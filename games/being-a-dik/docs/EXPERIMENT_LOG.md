# Dziennik analizy — Being a DIK

> **Aktualna decyzja właściciela:** wcześniejsze wzmianki o pozostawianiu tekstów lub tłumaczeń poza Git opisują ówczesny stan, nie obowiązującą zasadę. Wszystkie tekstowe dane projektu, narzędzia i robocze tłumaczenia śledzimy w Git; poza Git pozostają binarne assety gry.

## 2026-10-28 — rekonesans web + Drive

### Źródła z Drive

Folder Drive `Game`, ID `1ENcu9eNt8wOO3LpggviZBgX5T016sJ1I`.

| Plik | Drive file ID | Rozmiar | SHA-256 |
|---|---|---:|---|
| `goggame-1181224050.info` | `1gMOIoqluPTi9yvm_O9yDP_QTU9rFiPRT` | 770 B | `ee44ec2b7b009a8322e2f1e850cf6c56ef6500d099d29845f976043846a8f87c` |
| `scripts.rpa` | `1zFJC2idWh6R1OV2cZLG4R2ByFazVU69w` | 9,526,870 B | `c9ba7ef3801f482df157afc39a662c7c0e0cbf6455e74657ecc8b2f46d24d86f` |
| `archive.rpa` | `1guC-9meTGRHhcNArL1VssyESUQvQN0vM` | 16,645,751 B | `a5a7c02d35de61089b7cc2e868562ce65ef82819da936925727b8558dc82e0bf` |
| `gallery.rpa` | `1HJQdHvAjr0WIwJJtkVEM3CF7ruL26rRi` | 6,605,109 B | `58f22ee18bff357f26f943d3d2f0b99528d2530009c0e014dc14bbf8681b4927` |
| `patch_v042.rpa` | `1yMOH_6q-d5cB9P5cyWxZp9WNOTa4xOtZ` | 14,849,201 B | `cba35dfae18b5d82a373f4ffb40a969a199cf99242e015b274a026af090e0fc3` |
| `script_version.txt` | `186KJzmVSwP77v1YYN79H3DjLarclcUtL` | 10 B | tekst odczytany przez Drive: `(7, 4, 10)` |
| `log.txt` | `15X6y-xxLzMvGKmBUXpO8I-FaiCk3zkLk` | 1,564 B | odczyt tekstu Drive, opisany w `ENVIRONMENT.md` |

RPA/fonty pobrano do wyłączonego z Git katalogu tymczasowego `google_drive/`. Nie uruchamiano plików gry ani skryptów z archiwów.

### Metoda i wyniki

- Odczytano nagłówki RPA-3.0 i indeksy; potwierdzono 158 `.rpyc` w `scripts.rpa` oraz podział wpisów archiwów w `TECHNICAL_FINDINGS.md`.
- RPA indeksy są pickle; przed deserializacją zweryfikowano listę opcode'ów przeciw bezpiecznej allowliście ograniczonej do prymitywnych struktur/typów. Nie było opcode'ów `GLOBAL`, `REDUCE` ani podobnych; kod gry nie został wykonany.
- Dokładne wyszukanie Drive `name='script_version.txt'` oraz ponowne `get_file` potwierdziły, że ID `186KJzmVSwP77v1YYN79H3DjLarclcUtL` należy do `script_version.txt`; właściwy plik `BeingADIK.sh` ma inne ID.
- Odczytano GOG manifest i potwierdzono Season 1 / English / build ID `55720371802277951`.
- Sprawdzono Unicode cmap fontów przez FontTools 4.68.0: 5/10 fontów ma komplet 18 PL liter; pozostałe cmapy są niepełne.
- Wyszukano warianty tytułu + spolszczenie/Polish translation na webie; nie znaleziono wiarygodnego PL patcha. To ograniczony rekonesans, nie dowód nieistnienia.
- Sklonowano i przejrzano `Waiyakorn1879/for-the-plot`, commit `879b9b863032a09e6a27cdca67c6582a573e3819`, tylko dokumentację i profile techniczne. Nie uruchamiano jego tłumaczeń ani nie kopiowano treści.
- W `/tmp` wyekstrahowano dwa wybrane `.rpyc` z `scripts.rpa` i sprawdzono parser `unrpyc` v2.0.3, Git HEAD `3ae8334ed71a05535927dcc559663d3aca51215b`: `math_test2.rpyc` oraz mały skrypt chat odpowiedzi. Oba zakończyły się statusem successful decompilation; w raporcie dla pierwszego narzędzie ostrzegło o Ren'Py 7 wobec Ren'Py 8 targetu tej gałęzi. Nie wypisywano treści gry do repozytorium.

### Ograniczenia wyniku

To test dwóch skryptów, nie całego zestawu 158 `.rpyc`; nie policzono unikalnych tekstów, nie zbudowano ani nie uruchomiono patcha. Cmap nie potwierdza renderowania. Nie było testu w Windowsowej kopii użytkownika.

## 2026-10-28 — pełny statyczny census skryptów Season 1

- `scripts.rpa` pobrano do ignorowanego `google_drive/scripts.rpa`; SHA-256 `c9ba7ef3801f482df157afc39a662c7c0e0cbf6455e74657ecc8b2f46d24d86f`. `unrpa` wyodrębnił 158 `.rpyc`; `unrpyc` v2.0.3 zdekompilował wszystkie 158/158. 133 pliki wygenerowały ostrzeżenie zgodności Ren’Py 7/8, zero błędów dekompilacji.
- Przejście po AST policzyło 16 669 węzłów `Say` (16 510 z jawnym mówiącym, 159 bez mówiącego), 14 650 różnych surowych tekstów, 521 `menu` i 1 266 tekstowych opcji (776 różnych etykiet). Każda gałąź w skompilowanym AST została policzona statycznie, bez ewaluowania warunków.
- Dodatkowa analiza AST bloków Python w telefonie: 487 stałych/wzorcowych wpisów wiadomości i feedu (439 unikalnych wzorców; 424 literalne, 63 formatowane) oraz 400 wariantów odpowiedzi gracza w tablicach telefonu/Swypera (386 unikalnych etykiet). 23 dopisania dynamiczne odnotowano, ale nie liczono ich jako odrębnego tekstu źródłowego.
- Zapisano `docs/COUNT_REPORT.md`; zakres UI, podpisów profili, wszystkich ekranów telefonu i tekstów generowanych wyłącznie w runtime pozostaje osobny. Nie uruchamiano gry ani jej kodu i nie budowano patcha.
