# Lista kontrolna QA i wydania

Odznaczaj tylko testy faktycznie wykonane. Jeśli etap nie dotyczy projektu, oznacz N/D z uzasadnieniem.

## Inwentaryzacja i próbki

- [ ] Platforma, sklep/nośnik i dokładny build zapisane.
- [ ] Pakiet wejściowy działa w docelowym Windowsie; log i ZIP są kompletne.
- [ ] Raport nie zawiera plików gry ani niepotrzebnych danych prywatnych.
- [ ] Lista dalszych próbek jest minimalna, ma uzasadnienie i rozmiar.
- [ ] Każda zwrotka ma nazwę, Drive ID, rozmiar i SHA-256.

## Ekstrakcja i struktura

- [ ] Wyodrębnienie jest deterministyczne i zachowuje nieznane bajty/metadata.
- [ ] Nie zmieniający niczego round-trip odtwarza wejście bajt w bajt albo opisuje wyjątki.
- [ ] Wszystkie rekordy mają stabilny, unikalny identyfikator; zakres i wersja źródła są zapisane.
- [ ] Tokeny, zmienne, kody sterujące i warunki wyboru są zinwentaryzowane.
- [ ] Kontekst sceny, mówiącego, poprzedniej/następnej kwestii oraz route jest potwierdzony lub oznaczony jako nieznany.

## Tekst i pakiet tłumacza

- [ ] Liczba ID i wypełnionych pól zgodna z manifestem.
- [ ] Źródło i oficjalne referencje nie zostały zmienione.
- [ ] Placeholdery i tokeny mają identyczną liczbę, kolejność i składnię.
- [ ] Długość/wiersze/kodowanie mieszczą się w potwierdzonych ograniczeniach.
- [ ] Glosariusz i decyzje redakcyjne zastosowane; pytania są jawne.
- [ ] Korekta językowa obejmuje sens, głos postaci, rodzaj gramatyczny, odmianę i ciągłość wyborów.

## Patch i test w grze

- [ ] Test patcha obejmuje kopię oryginału i możliwość cofnięcia.
- [ ] Patch jest przypięty do wersji bazowej i odmawia pracy na niezgodnych danych.
- [ ] Raport przed/po zawiera hashe i listę zmienionych elementów.
- [ ] Gra uruchamia się na wspieranej platformie/buildzie.
- [ ] Sprawdzono polskie znaki, overflow, dialogi, wybory, powroty, zmienne, zapisy i odczyty.
- [ ] Użytkownik potwierdził test lub dostarczył raport; brak potwierdzenia jest jawnie zapisany.

## Wydanie

- [ ] Paczka zawiera tylko elementy potrzebne do instalacji, bez oryginalnych assetów.
- [ ] Instrukcja podaje wersję, ograniczenia, wymagania, kopię zapasową i cofnięcie.
- [ ] Suma kontrolna paczki oraz test pobrania/rozpakowania zostały sprawdzone.
- [ ] Status jest właściwy: prototyp / test / kandydat / wydane.
