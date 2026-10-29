# Undercover with Nora

Projekt rozpoznania tekstu dla przekazanej kopii **v1.0.0**. Potwierdzono **Ren'Py 8.3.3.24111502** i archiwum **RPA-3.0**. Pełny statyczny licznik tekstu dialogowego z dostarczonych skryptów jest w [`docs/COUNT_REPORT.md`](docs/COUNT_REPORT.md).

## Wynik w skrócie

- **15 036 wystąpień dialogu** w skryptach odcinków 1–10 i wspólnym `script.rpy`.
- **13 344 różne literalne treści** po prostym deduplikowaniu identycznych zapisów; to nie zastępuje licznika wystąpień z kontekstem.
- Dodatkowo **54 bloki `menu` i 121 tekstowych opcji** w skryptach odcinków — liczone osobno od dialogów.
- 23/23 skompilowane skrypty z jedynego `01001110.rpa` udało się statycznie zdekompilować; nie uruchamiano gry ani kodu gry.

Licznik obejmuje wszystkie gałęzie zapisane w skryptach kopii, także te wzajemnie wykluczające się podczas jednego przejścia. „Linia” oznacza tu pojedynczą instrukcję dialogową silnika, nie wiersz po zawinięciu tekstu w oknie. UI, ekrany, przyciski, osiągnięcia i inne niedialogowe stringi nie są wliczone.

## Dokumentacja

- [Raport licznika](docs/COUNT_REPORT.md)
- [Status](docs/STATUS.md)
- [Ustalenia techniczne](docs/TECHNICAL_FINDINGS.md)
- [Dziennik eksperymentów](docs/EXPERIMENT_LOG.md)
- [Środowisko i zakres kopii](ENVIRONMENT.md)
- [Instrukcje dla agentów](AGENTS.md)

Tłumaczenie ani patch nie zostały rozpoczęte. Projekt pozostaje kandydatem; ten raport opisuje tylko zbadany build v1.0.0.
