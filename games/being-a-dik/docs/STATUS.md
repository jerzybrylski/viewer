# Status — Being a DIK

**Stan: kandydat; pełny statyczny census archiwum `scripts.rpa` dla Season 1 gotowy, przed tłumaczeniem wymagane porównanie i osobna inwentaryzacja UI.** Aktualizacja: 2026-10-28.

## Wniosek

Tłumaczenie polskie jest **technicznie osiągalne z wysokim prawdopodobieństwem** dla przesłanej kopii Season 1: to Ren'Py 7.4.10, skrypty znajdują się w standardowych archiwach RPA-3.0, a publiczne repo opisuje workflow dla tej samej gry (deklaracja autora, niezależnie niezweryfikowana). Polska lokalizacja nie jest oficjalnie wykazana na Steam/GOG w zbadanych metadanych, a wiarygodnego gotowego spolszczenia nie znaleziono.

## Potwierdzone

- GOG manifest: Season 1 / English `en-US`, build ID `55720371802277951`.
- Silnik: Ren'Py `7.4.10.2178` według przesłanego logu.
- `scripts.rpa` indeksuje 158 skompilowanych `.rpyc` plików; dwa próbne pliki zostały zdekompilowane przez `unrpyc` v2.0.3, choć jeden test zgłosił ostrzeżenie wersji Ren'Py.
- Pięć dołączonych fontów ma glify Unicode dla wszystkich polskich znaków; część pozostałych fontów ich nie ma.
- Publiczne repo `for-the-plot` deklaruje przykład fanowskiej translacji Thai dla *Being a DIK* (Episodes 1–8) i osobny zakres czatów telefonu. To deklaracja autora, nie niezależnie odtworzony patch; tłumaczenie nie jest źródłem dla PL.

## Nieznane / niezweryfikowane

- Czy folder zawiera wszystkie pliki Season 1 i dokładnie jaki jest content revision poza GOG build ID.
- Ekstrakcja i dekompilacja każdego skryptu z tej kopii; liczba unikalnych tekstów do polskiego przekładu.
- Przypisania fontów do poszczególnych stylów, renderowanie polskich liter i długości w oknach.
- Kompletność etykiet i opisów GUI/ekranów telefonu, profili i części tekstów UI/minigier; census wiadomości i wyborów telefonicznych jest dostępny osobno w raporcie.
- Instalacja i cofnięcie patcha, zgodność z zapisami/osiągnięciami, runtime na komputerze właściciela.
- Zakres Season 2/3 — nie potwierdzono tych plików w przekazanym GOG manifeście.

## Następny etap przed tłumaczeniem

Właściciel chce najpierw porównywalnego licznika dialogów/wyborów dla Being a DIK i TGO oraz Czytanek z oznaczeniem scen, mówiących i wyborów. Dla BAD gotowy jest pełny census wszystkich 158 skryptów; TGO wymaga jeszcze dostarczenia pełnego pakietu tekstowych JSON-ów, by przetworzyć 291 map. Należy zachować odgałęzienia i warunki, a nie sprowadzać grę do jednej kanonicznej ścieżki. Nie rozpoczęto tłumaczenia. Being a DIK nie został wybrany jako pierwszy tytuł.
