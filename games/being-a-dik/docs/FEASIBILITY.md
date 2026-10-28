# Ocena osiągalności spolszczenia — Being a DIK

**Werdykt (2026-10-28): wysoka osiągalność techniczna; duży, ale dobrze ograniczalny zakres.** Wniosek dotyczy tylko przesłanych plików GOG Season 1. Nie jest obietnicą kompletności ani wynikiem testu patcha.

## Co znaleziono w sieci

- Nie znalazłem wiarygodnego polskiego patcha/spolszczenia. Wyszukiwałem warianty `Being a DIK` + `spolszczenie`, `po polsku`, `Polish translation/patch` oraz wyniki forów i repozytoriów. To ograniczony wynik wyszukiwania, nie dowód, że nigdzie nie istnieje prywatny patch.
- Badana [oficjalna karta Steam dla Season 1](https://store.steampowered.com/sub/382492/) wskazuje język English; plik manifestu GOG przesłany przez użytkownika również deklaruje `en-US`.
- Mocny techniczny prior art: publiczne repo [for-the-plot](https://github.com/Waiyakorn1879/for-the-plot) opisuje działającą fanowską translację Thai dla *Being a DIK*, zaczynając od 2,638 stringów w Episode 1, rozwiniętą do ok. 36 tys. stringów w Episodes 1–8; repo zaznacza też osobny podprojekt dla czatów telefonu oraz dalsze prace nad Season 3. To dowód, że gra i jej tekst są obsługiwalne przez tłumaczeniowy workflow Ren'Py — nie dowód, że dowolny patch działa na wersji z Drive.

## Co potwierdza kopia użytkownika

- `goggame-1181224050.info` identyfikuje **Being a DIK - Season 1**, język English (`en-US`), GOG build ID `55720371802277951` i `BeingADIK.exe`.
- `log.txt` raportuje Windows 10 oraz Ren'Py `7.4.10.2178`; `game/script_version.txt` zawiera `(7, 4, 10)`.
- Cztery zbadane archiwa mają nagłówek `RPA-3.0`, indeksy z kluczem `0x42424242`. Indeksy można odczytać bez uruchamiania kodu gry.
- `scripts.rpa` (9,526,870 B) zawiera 158 indeksowanych plików `.rpyc`, w tym skrypty epizodów, freeroam, telefon (chat, Swyper, Rooster, Brawler, raporty, kontakty), sceny i minigry. To wystarcza do rozpoczęcia statycznej próby ekstrakcji; RPA jest archiwum skompilowanych skryptów, więc będzie potrzebna dekompilacja dopasowana do Ren'Py 7 / Python 2 bytecode.
- Dołączone fonty nie stanowią oczywistej blokady: cmap pięciu fontów (`Museo500`, `Redressed`, `Candara`, `Century Gothic Regular/Bold`) zawiera komplet 18 polskich liter. Niektóre inne fonty gry mają tylko częściowe pokrycie; trzeba ustalić, które style są używane i potwierdzić wynik runtime.
- Próbny test `unrpyc` v2.0.3 zdekompilował dwa wybrane `.rpyc` (krótki skrypt klasy i mały plik odpowiedzi czatu). Jeden przebieg ostrzegł, że plik pochodzi z Ren'Py 7, a narzędzie targetuje Ren'Py 8; dlatego sukces próbek jest dobrym sygnałem, ale nie gwarantuje poprawnego wyniku dla wszystkich 158 skryptów.

## Ryzyka i zakres

1. **Wersja dekompilatora:** `.rpyc` z Ren'Py 7 wymaga obsługi właściwej generacji bytecode; nie należy traktować dekompilacji jak zwykłego tekstu.
2. **Zakres nie jest tylko dialogiem:** treści telefonu, feedów, galerii, raportów, testów i screenów mogą być budowane dynamicznie albo leżeć poza zwykłym say/menu. Prior art dla tego tytułu wskazuje osobne wrappery telefonu.
3. **Zachowanie gry:** zwykły `game/tl/polish/`/filtr runtime jest obiecującą drogą dla Ren'Py, ale nie był jeszcze zbudowany ani przetestowany na tym buildzie.
4. **Wielkość:** nawet istniejący Thai project miał ok. 36 tys. stringów dla Episodes 1–8; pełny tytuł z S3 będzie znaczącym przedsięwzięciem. Mały pilot jest rozsądniejszy niż obietnica od razu kompletnego spolszczenia.
5. **Dane przekazane:** manifest wskazuje Season 1. Nie traktuj tego jako danych Season 1–3.

## Zalecany następny krok, jeśli właściciel wybierze ten tytuł

1. Na kopii `scripts.rpa` zdekompilować całość 158 skryptów narzędziem dobranym do Ren'Py 7, rejestrując błędy i porównując odzyskane struktury; dwa krótkie testy już się powiodły, lecz jeden ostrzegł o wersji Ren'Py.
2. Zrobić mały, niemodyfikujący gry eksport Episode 1: źródło English, label/scena, mówiący, wybory, wszystkie tokeny i osobno treści UI/telefon.
3. Zbudować pojedynczy testowy polski string lub minimalny native translation patch i poprosić właściciela o test w jego kopii gry.
4. Dopiero potem policzyć pełny zakres Season 1 i podjąć decyzję o Season 2/3.
