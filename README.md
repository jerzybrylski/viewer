# Warsztat spolszczania visual novels

Repozytorium do technicznego rozpoznawania, tłumaczenia, testowania i przygotowywania polskich lokalizacji visual novel. Każdy tytuł ma osobny katalog i własne ustalenia — nie zakładamy wspólnego silnika ani formatu.

> **Zasada nadrzędna:** najpierw rozpoznajemy konkretną kopię gry i jej zasoby, dopiero potem wybieramy narzędzia oraz sposób pracy. Nie modyfikujemy instalacji użytkownika podczas inwentaryzacji.

## Projekty i kandydaci

- [The Genesis Order](games/the-genesis-order/README.md) — wybrany projekt lokalizacji; kanoniczny eksport ma 45 229 rekordów JSON, statyczny audyt powierzchni jest zakończony, a ZIP i patcher pozostają wstrzymane do akceptacji pokrycia.
- [Being a DIK](games/being-a-dik/README.md) — wstępna analiza przesłanej edycji Season 1; pełny licznik treści jeszcze niegotowy.
- [Undercover with Nora](games/undercover-with-nora/README.md) — potwierdzono Ren'Py 8.3.3; przygotowano pełny statyczny licznik jawnych dialogów dla przesłanej kopii v1.0.0.
- [Lista projektów i ich status](PROJECTS.md) oraz [porównanie kandydatów](docs/CANDIDATE_COMPARISON.md).

## Sposób pracy

1. **Inwentaryzacja lokalna** — użytkownik uruchamia dostarczony skrypt na swojej kopii. Zbieramy listę plików, rozmiary i metadane; wynik trafia do nas jako mały ZIP przez Google Drive.
2. **Rozpoznanie zasobów** — na podstawie rzeczywistych danych identyfikujemy silnik, archiwa, formaty tekstu, kodowanie, strukturę scen, wybory i ograniczenia renderowania. Nie zgadujemy ścieżek ani narzędzi.
3. **Zbieranie celowane** — prosimy o konkretnie wskazane, minimalne pliki. Dołączamy nowy BAT/PowerShell lub odpowiedni skrypt, który tylko kopiuje wybrane wejścia i raportuje wyniki.
4. **Ekstrakcja i kontekst** — przygotowujemy stabilne identyfikatory tekstów, kontekst sceny, mówiącego, warianty/gałęzie, tokeny i potwierdzone limity.
5. **Tłumaczenie i kontrola** — pracujemy porcjami, ze wspólnym glosariuszem, kontrolą znaczników, spójności głosów, długości oraz kompletności.
6. **Wdrożenie i test** — dopiero po poznaniu formatu wybieramy patch/mod lub inną metodę. Testy w grze opisujemy jako wykonane wyłącznie na podstawie rzeczywistych wyników użytkownika.

Pełne zasady: [workflow](docs/WORKFLOW.md), [polityka tłumaczenia](docs/TRANSLATION_POLICY.md), [higiena danych](docs/DATA_HANDLING.md), [checklista QA](docs/QA_CHECKLIST.md), [szablon nowego tytułu](docs/PROJECT_TEMPLATE.md) i [źródła przeniesionych praktyk](docs/REFERENCES.md).

## Układ repozytorium

```text
games/<slug>/       dokumentacja, narzędzia i tłumaczenie jednego tytułu
tools/folio-viewer/ pomocniczy viewer screenshotów powstały przed zmianą profilu repo
docs/               zasady wspólne dla wszystkich VN-ów
```

Dane gry, pełne instalatory, oryginalne zasoby, zapisy, zrzuty ekranu i zbudowane kopie gry nie trafiają do Git. Dane lokalne są ignorowane przez `.gitignore`; do repo trafiają narzędzia, dokumentacja, jawnie przygotowane dane tłumaczeniowe oraz testy.

## Środowisko

Zobacz [ENVIRONMENT.md](ENVIRONMENT.md). To repo nie narzuca jednego silnika ani globalnego zestawu zależności. Wymagania konkretnego tytułu muszą być zapisane w jego katalogu i poparte testem.

## Wykorzystane doświadczenia

Wspólny proces czerpie z udanych praktyk projektu [mtgcrawler / SRW Y i SRW OE](https://github.com/szybkoiwyraznie-rgb/mtgcrawler): małe, celowane paczki danych; lokalna praca na kopii użytkownika; czytelne pakiety tłumacza; stabilne identyfikatory; osobny glosariusz i dziennik eksperymentów; jawne rozróżnianie faktów, hipotez i niewiadomych; testy strukturalne przed przekazaniem patcha. Szczegóły techniczne SRW są właściwe wyłącznie tamtemu projektowi i nie są automatycznie przenoszone na VN-y.

## Zachowany viewer

[Viewer screenshotów](tools/folio-viewer/README.md) pozostaje pomocniczym narzędziem do oznaczania scen, gałęzi i ilustracji. Nie jest już głównym celem repozytorium.
