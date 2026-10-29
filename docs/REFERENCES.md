# Źródła praktyk workflow

Podstawą organizacji są sprawdzone procesy z projektów dostępnych w repozytorium [szybkoiwyraznie-rgb/mtgcrawler](https://github.com/szybkoiwyraznie-rgb/mtgcrawler). Inspekcja źródeł została wykonana na commicie [`d3e0f97a3fc68f6d9c76f62efa439f920bce02b7`](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/commit/d3e0f97a3fc68f6d9c76f62efa439f920bce02b7) z 2026-10-27. Przejrzane materiały:

- [instrukcje repozytorium](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/AGENTS.md) — separacja projektów, prywatne dane lokalne, jawne fakty/hipotezy, logi testów;
- [SRW OE: workflow tłumaczenia](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-oe-translation/docs/TRANSLATION_WORKFLOW.md) — czytelny, edytowalny eksport, oddzielne etapy tłumaczenia/aplikacji i jawne granice zakresu;
- [SRW OE: wytyczne tłumaczenia](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-oe-translation/docs/TRANSLATION_GUIDELINES.md) oraz [polityka](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-oe-translation/docs/TRANSLATION_POLICY.md) — techniczne ograniczenia wyznaczane per rodzaj tekstu, kontekst/mówca, stabilne identyfikatory i źródła terminologii;
- [SRW OE: metoda](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-oe-translation/docs/METHOD.md) — najpierw korzystać z dowodów, a nie powtarzać niepotrzebne eksperymenty;
- [SRW Y: instrukcje projektu](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-y-translation/AGENTS.md) i [README](https://github.com/szybkoiwyraznie-rgb/mtgcrawler/blob/main/srw-y-translation/README.md) — raporty lokalne, minimalne zbiory wejściowe, hashe/Drive IDs, bogaty kontekst i jawny status niezweryfikowanych testów.

## Dodatkowy punkt odniesienia dla Ren'Py / Being a DIK

Przy badaniu Ren'Py sprawdzono także [Waiyakorn1879/for-the-plot](https://github.com/Waiyakorn1879/for-the-plot), commit [`879b9b863032a09e6a27cdca67c6582a573e3819`](https://github.com/Waiyakorn1879/for-the-plot/commit/879b9b863032a09e6a27cdca67c6582a573e3819). Repo opisuje pipeline Ren'Py oraz przykład profilu dla *Being a DIK* → Thai. To wiedza techniczna, nie źródło polskiego przekładu. **Nie kopiujemy** tłumaczenia, przykładów ani game-specific danych — korzystamy z dokumentacji o formacie, ekstrakcji i QA tylko jako z technicznego prior art.

Do lokalnego testu parsowania skompilowanych skryptów użyto [CensoredUsername/unrpyc](https://github.com/CensoredUsername/unrpyc), v2.0.3, Git HEAD `3ae8334ed71a05535927dcc559663d3aca51215b`. Dwa wybrane skrypty zakończyły dekompilację pomyślnie; jeden wynik zawierał ostrzeżenie o Ren'Py 7. Szczegóły i ograniczenie próby zapisano w raporcie Being a DIK.

## Co przenosimy

- iteracyjne BAT/PowerShell → ZIP → Drive dla wejść z Windowsa;
- zaczynanie od spisu/rozmiarów, później zbieranie ściśle wskazanych plików;
- separację jednego tytułu od drugiego i rejestrowanie pochodzenia; zasady przechowywania w Git określa bieżąca decyzja właściciela;
- pakiety tłumacza ze stabilnymi ID, kontekstem, tokenami i limitem tylko wtedy, gdy jest potwierdzony;
- osobny glosariusz, walidatory, testy, dziennik eksperymentów i bezpieczny etap aplikacji patcha.

## Czego nie przenosimy automatycznie

Repozytorium SRW obejmuje konkretne gry, platformy, silniki, pliki, kodowania i decyzje redakcyjne. Żaden szczegół techniczny ani limit z SRW nie jest domyślnie prawdziwy dla VN. Narzędzia mogą być adaptowane po inspekcji i zgodzie, ale nigdy nie kopiujemy do tego repo danych gry ani tekstów z innego tłumaczenia.
