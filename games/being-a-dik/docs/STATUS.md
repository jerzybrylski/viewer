# Status — Being a DIK

**Stan: kandydat; wstępne badanie techniczne zakończone.** Aktualizacja: 2026-10-28.

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
- Kompletność tekstów z telefonu, feedów, UI i minigier w standardowej ekstrakcji.
- Instalacja i cofnięcie patcha, zgodność z zapisami/osiągnięciami, runtime na komputerze właściciela.
- Zakres Season 2/3 — nie potwierdzono tych plików w przekazanym GOG manifeście.

## Decyzja właściciela

Nie wybrano jeszcze Being a DIK jako pierwszego tytułu. Zalecany pilot po wyborze: Episode 1, następnie automatyczny QA oraz test na kopii gry.
