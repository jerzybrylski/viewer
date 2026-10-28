# Projekty i kandydaci

Każda visual novel ma własny katalog `games/<slug>/`. Statusy opisują wyłącznie dowody dostępne dla danego wydania; nie oznaczają, że właściciel wybrał już tytuł do tłumaczenia.

| Tytuł | Slug | Status | Następny krok |
|---|---|---|---|
| The Genesis Order | [`the-genesis-order`](games/the-genesis-order/README.md) | **Pełny census dialogów i wyborów z 291 map / 500 common events gotowy; UI/dynamika osobno** | Przejrzeć komendy skryptowe/pluginowe, sprawdzić font fallback i przygotować branch-aware Czytankę. |
| Being a DIK | [`being-a-dik`](games/being-a-dik/README.md) | **Pełny statyczny census 158 skryptów `scripts.rpa` (Season 1) gotowy; kandydat niezatwierdzony** | Osobno zinwentaryzować UI/pozostałe teksty telefonu, przygotować branch-aware Czytankę i porównać zakresy. |
| Undercover with Nora | [`undercover-with-nora`](games/undercover-with-nora/README.md) | **Statyczny licznik dialogów gotowy dla przesłanej kopii v1.0.0; kandydat niezatwierdzony** | Osobno zinwentaryzować UI/screeny, a w razie wyboru przygotować branch-aware Czytankę i QA zakresu. |

## Dodanie kolejnego tytułu

1. Skopiuj strukturę opisaną w [`docs/PROJECT_TEMPLATE.md`](docs/PROJECT_TEMPLATE.md) do nowego `games/<slug>/`.
2. Ustal platformę, wydanie, język źródłowy i stan praw dostępu bez zakładania silnika.
3. Zapisz osobny status, fakty/hipotezy, dziennik eksperymentów, środowisko i zasady tłumaczenia tytułu.
4. Dodaj tytuł do tabeli dopiero po przygotowaniu jego README i AGENTS.
