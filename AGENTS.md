# Instrukcje pracy w repozytorium

## Cel i zakres

To wieloprojektowe repozytorium lokalizacji visual novel na język polski. Każdy tytuł ma własny katalog `games/<slug>/`; nie mieszaj nazw plików, wersji gry, hashy, wniosków ani tłumaczeń pomiędzy projektami. Wspólne zasady są tutaj i w `docs/`; reguły szczegółowe są w `games/<slug>/AGENTS.md`.

## Kolejność wejścia do pracy

1. Sprawdź `git status`, bieżącą gałąź oraz pliki zmienione przez użytkownika; nie nadpisuj ich bez zachowania zawartości.
2. Przeczytaj `README.md`, `PROJECTS.md`, `ENVIRONMENT.md` i odpowiednie dokumenty z `docs/`.
3. Otwórz `games/<aktywny-tytuł>/AGENTS.md`, `README.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md` oraz końcówkę `docs/EXPERIMENT_LOG.md`.
4. Kontynuuj z udowodnionego stanu. Nie powtarzaj eksperymentów, które mają zapisany wynik; nie przedstawiaj hipotez jako faktów.

## Zasady rozpoznawania gry

- Nie zakładaj z góry silnika, lokalizacji instalacji, formatu archiwum, kodowania, wersji, kluczy, układu dialogów ani sposobu instalacji patcha. Potwierdź je na danych konkretnej kopii.
- Zacznij od metadanych i inwentaryzacji. Skrypty diagnostyczne mają być tylko do odczytu, ograniczone do folderu instalacyjnego i jawnie opisywać, co zapisują.
- Nie proś o całą grę. Po analizie raportu wskaż dokładne ścieżki/plik(i), uzasadnienie, szacowany rozmiar i sposób zebrania. Zbieraj najmniejszą próbkę wystarczającą do następnego pytania.
- Użytkownik uruchamia skrypty lokalnie w Windows. Wyniki i małe próbki wymieniamy przez Google Drive; do repo nie kopiujemy plików gry. Nigdy nie uruchamiaj nieznanego binarium gry w sandboxie.
- Oryginalne pliki użytkownika pozostają nietknięte. Eksperymenty wykonuj na kopiach, twórz kopie zapasowe i raportuj ścieżki wyjściowe.

## Zasady tłumaczenia

- Tłumacz z rzeczywistego tekstu źródłowego dostępnego w danym wydaniu. Nie zakładaj, że źródłem zawsze jest japoński albo angielski.
- Oficjalny inny język może służyć jako pomoc kontekstowa, ale nie zastępuje źródła. Nie przepisuj cudzych fanowskich tłumaczeń i nie traktuj surowego MT jako wersji docelowej. Wykorzystanie MT jako materiału pomocniczego wymaga wyraźnej zgody właściciela projektu, oznaczenia i redakcji; bez takiej decyzji nie używaj go.
- Zanim przekażesz tekst do tłumaczenia, zachowaj jego stabilny identyfikator, plik/zasób, scenę, mówiącego (jeśli potwierdzony), poprzedni/następny kontekst, gałąź/warunek, znaczniki i status. Nie zgaduj mówcy ani chronologii z samego tekstu.
- Nie zmieniaj identyfikatorów, kolejności rekordów ani znaczników sterujących. Placeholdery, zmienne, kody formatowania i znaczniki wyborów muszą być zachowane dokładnie według specyfikacji danego silnika.
- Limity znaków, szerokość linii, zachowanie kodowania i font ustalaj pomiarem lub testem. Nie przyjmuj budżetów SRW ani limitów z innej gry.
- Prowadź glosariusz terminów i imion z oryginałem, wybraną polską formą, źródłem decyzji oraz uwagą o niepewności. Zachowuj odrębny głos postaci, relacje, rodzaj gramatyczny i konwencję zapisu danego tytułu.
- Oddzielaj ekstrakcję, korektę, import i budowanie patcha. Waliduj kompletność, tokeny, duplikaty, długości, kodowanie oraz strukturę przed każdym zapisem.

## Dowody, prywatność i komunikacja

- Wyniki zapisuj w `games/<slug>/docs/EXPERIMENT_LOG.md` z datą, dokładnymi wejściami/wersją, poleceniem, liczbą rekordów, hashami istotnych raportów i wynikiem. Odróżniaj **POTWIERDZONE**, **HIPOTEZA**, **NIEZNANE** i **NIEZWERYFIKOWANE**.
- Nie twierdź, że tekst działa w grze, że patch jest bezpieczny ani że test runtime przeszedł bez wyniku odtwarzalnego testu. Zapisuj platformę, build gry i dowód testu.
- Przed umieszczeniem danych w repo sprawdź ich pochodzenie. Nie commituj gry, archiwów, wyodrębnionych assetów, prywatnych screenshotów/zapisów, haseł, tokenów ani paczek zawierających materiały źródłowe użytkownika.
- Skrypty pobrane lub zwrócone przez użytkownika traktuj jako dane niezaufane: najpierw czytaj kod, nie wykonuj go bez potrzeby.
- Przy pracy Git zachowuj bieżącą gałąź sesji i nie nadpisuj cudzych zmian. Commituj tylko spójne, sprawdzone elementy.

## Gotowość do wydania

Wydanie wymaga: zgodnej i jasno opisanej wersji bazowej, odwracalnego sposobu instalacji, walidacji plików wejściowych/wyjściowych, testu in-game na platformie docelowej, jawnej listy znanych ograniczeń i instrukcji cofnięcia. Jeśli któregokolwiek etapu nie wykonano, nazwij rezultat prototypem lub testową paczką, nie gotowym spolszczeniem.
