# Wspólny workflow lokalizacji VN

Proces iteracyjny. Każdy etap kończy się małym, weryfikowalnym wynikiem; nie przechodzimy do ekstrakcji ani modyfikacji plików na podstawie przypuszczeń.

## 0. Ustalenie kopii i zakresu

Zapisz tytuł, platformę, sklep/nośnik, numer wersji/build, język oryginalnego tekstu, języki oficjalne, stan aktualizacji/DLC i to, co użytkownik chce przetłumaczyć. Nie pobieraj gry. W razie niepewności pozostaw pole jako nieznane.

## 1. Inwentaryzacja bez kopiowania gry

Dostarcz użytkownikowi mały pakiet BAT + skrypt, który:

- działa lokalnie na wybranym folderze instalacyjnym i nie modyfikuje gry;
- raportuje względne ścieżki, rozmiary, rozszerzenia oraz przydatne metadane;
- nie czyta ani nie wysyła treści wszystkich plików, zapisów z profilu użytkownika ani danych spoza instalacji;
- zapisuje na pulpicie wynikowy raport ZIP i log; opisuje dokładnie, co użytkownik ma umieścić na Drive.

Po otrzymaniu raportu sprawdź kompletność, wersję/identyfikatory, strukturę katalogów, sumy rozmiarów i rozszerzenia. Wynik inwentaryzacji to wskazówka, nie dowód, że plik zawiera tłumaczalny tekst.

## 2. Rozpoznanie formatu i minimalna próbka

Na podstawie raportu sformułuj konkretne pytania techniczne: które pliki są archiwami, gdzie tekst, jak zachować kolejność i identyfikatory, jakiego kodowania używa gra, jak działają dialogi/wybory, czy zasób jest kompresowany lub szyfrowany. Każdą hipotezę testuj na najmniejszej próbce.

Dla użytkownika przygotuj **drugi, celowany pakiet** BAT + PS1: zawiera jawną listę ścieżek, kopiuje tylko wybrane pliki do nowego katalogu i pakuje je wraz z manifestem rozmiarów/SHA-256 oraz logiem. Skrypt ma przerwać z czytelnym błędem przy braku lub niezgodności pliku; nie może modyfikować źródeł. Zanim wyślesz pakiet, sprawdź listę i przewidywany rozmiar. Odbieraj ZIP przez Drive i zapisuj jego ID, nazwę, rozmiar oraz hash.

Nie żądaj od użytkownika całej gry, jeśli pojedynczy zasób wystarcza. Gdy plik jest zbyt duży lub zawiera dane wrażliwe, podziel analizę albo poproś o bezpieczny raport lokalny.

## 3. Ekstrakcja i model tekstu

Najpierw zrób kopię wejścia w wyłączonym z Git katalogu `local/`; oblicz SHA-256. Oryginał pozostaje niezmieniony. Udowodnij odwracalność ekstrakcji na próbce i zachowaj surowe bajty przed dekodowaniem.

Każdy rekord do tłumaczenia powinien mieć, o ile dane pozwalają: stabilny ID, wersję i ścieżkę źródła, offset/klucz/ID zasobu, tekst źródłowy, kontekst sceny, mówcę, gałąź/warunek, poprzedni/następny kontekst, widoczne znaczniki, stan i uwagi. Nierozpoznane opcodes lub placeholdery oznaczaj, nie usuwaj. Weryfikuj, czy wybory prowadzą do właściwych następnych scen i czy tekst UI w grafice nie jest poza zakresem.

## 4. Pakiet tłumacza i redakcja

Oddziel tekst źródłowy i ewentualne oficjalne referencje od pustego pola polskiego. Ustal sposób zwrotu, identyfikatory niezmienne, format tokenów, grupowanie porcjami, reguły łamania wierszy oraz jawne limity. Limity wyznaczaj z rzeczywistej struktury/renderera lub pomiaru — nie przenoś ich z innej gry.

Tłumacz porcjami z glosariuszem i opisem tonu. W każdym zwrocie sprawdź kompletność ID, brak zmian źródła i referencji, tokeny, placeholdery, długości, polskie znaki oraz duplikaty. Zachowuj niepewności i pytania redakcyjne, nie rozwiązuj ich przez zgadywanie.

## 5. Zapis / patch

Dopiero po zrozumieniu formatu wybierz wdrożenie: mod loader, loose-file override, patch binarny, repack zasobu, narzędzie innego typu. Opisz wspierane wersje gry. Najpierw zbuduj testowy patch z jednym małym zasobem; waliduj hash, długość/strukturę, ścieżki, kopię zapasową i cofnięcie. Nigdy nie pakuj oryginalnych plików gry do repozytorium ani do ogólnej dystrybucji.

## 6. QA i dostawa

Testuj automatycznie: ekstrakcję/odbudowę bez zmian, poprawność schematu, kompletność tłumaczeń, kontrolne sumy, tokeny i limity; porównuj z oryginałem. Następnie poproś użytkownika o test na wskazanej platformie i wersji: uruchomienie, sceny, wybory, zmienne/formatowanie, wyświetlanie polskich znaków, overflow, audio oraz zapis/odczyt. Zapisuj raport, zrzuty tylko z wyraźną zgodą użytkownika, błędy i status cofnięcia.

Wydanie nazywaj gotowym dopiero wtedy, gdy znana jest wspierana wersja, test in-game przeszedł, patch jest odwracalny, a instrukcja wymienia ograniczenia. W przeciwnym razie oznacz rezultat jako proof-of-concept, test lub paczkę tłumacza.

## Wymiana przez Drive

- Repo przechowuje kod narzędzi, dokumentację, testy i zaakceptowane dane tłumaczeniowe.
- Drive służy do transferu małych raportów/wybranych zasobów między użytkownikiem a agentem.
- W dzienniku konkretnego tytułu zapisuj nazwy, Drive file ID, rozmiary, SHA-256 i zakres przekazanych plików. Nie publikuj otwartych linków ani uprawnień publicznych bez zgody użytkownika.
