# Wspólna polityka tłumaczenia

Zasady wspólne dla projektów VN. Decyzje specyficzne dla gry (język źródłowy, ton, konwencje, nazwy i format) zapisuj w `games/<slug>/docs/TRANSLATION_POLICY.md`.

## Źródło i wierność

- Źródłem jest tekst z dokładnie zidentyfikowanej wersji gry, nie tekst znaleziony w fanowskim patchu.
- Inny oficjalny język jest referencją pomocniczą. Jeśli rozbiega się ze źródłem, oznacz rozbieżność i rozstrzygaj z kontekstu oraz decyzji projektu.
- Nie kopiuj gotowych fanowskich tłumaczeń. Nie przedstawiaj MT ani surowego szkicu modelu jako przekładu finalnego; każda propozycja automatyczna wymaga pełnej redakcji i weryfikacji względem źródła.
- Zachowuj sens sceny, intencję, humor, podtekst, rejestr, głos postaci i relacje. Brak kontekstu oznacz pytaniem zamiast konfabulować.

## Pakiet i kontekst

- Źródło, identyfikatory i oficjalne referencje są tylko do odczytu. Pole `PL` jest jedynym polem do wypełniania, chyba że instrukcja projektu mówi inaczej.
- Każdy tekst ma stabilny klucz powiązany z konkretnym buildem. Zachowuj pełny kontekst dostępny: nazwę sceny, route/warunek, mówiącego, portret, sąsiednie kwestie, etykietę wyboru i znaczniki.
- Mówcę, płeć, kolejność scen i relacje potwierdzaj przez dane gry. Nie wyprowadzaj ich wyłącznie z tonu pojedynczego zdania.
- Używaj jednego glosariusza na tytuł. Zapisuj formę oryginalną, polski odpowiednik, odmianę, źródło i status decyzji. Dopuszczaj warianty, jeśli zależą od mówcy lub kontekstu.

## Język polski

- Stosuj poprawną polską interpunkcję, diakrytyki i odmianę; nie zamieniaj ą/ę/ł/ń/ó/ś/ź/ż na ASCII.
- Ustalaj reguły zapisu imion, zaimków, form grzecznościowych, onomatopei, cenzury i terminów kulturowych osobno dla gry.
- Nie spłaszczaj różnic stylu postaci. Uwzględniaj rodzaj gramatyczny i ciągłość wyborów/zmiennych.
- Zachowuj oryginalne łamanie wierszy tylko jeśli wymaga tego format. Jeżeli tekst może rosnąć, nie skracaj go na podstawie arbitralnego limitu; jeżeli ma twardy budżet, licz go zgodnie z regułą gry.

## Znaczniki i techniczne ograniczenia

- Nie tłumacz, nie usuwaj ani nie przestawiaj placeholderów, zmiennych, tagów formatowania, kodów sterujących ani identyfikatorów. Ich dokładne zasady określa projekt.
- Wyjściowy tekst musi mieścić się w potwierdzonym budżecie kodowania/renderowania. Długość bajtowa, liczba znaków i szerokość wizualna są różnymi miarami.
- Błędy tokenów, brakujące ID, niepoprawna kolejność lub nierozpoznany znacznik blokują import; nie poprawiaj ich po cichu.

## Status redakcyjny

Stosuj statusy co najmniej: `do tłumaczenia`, `wersja robocza`, `do korekty`, `zaakceptowane`, `wstrzymane / pytanie`. Zachowuj autora/recenzenta i notę zmiany, gdy workflow to obsługuje. „Zaakceptowane” nie oznacza jeszcze „działa w grze”.
