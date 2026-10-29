# Projekty i kandydaci

Każda visual novel ma własny katalog `games/<slug>/`. Statusy opisują dowody dostępne dla danego wydania. Właściciel wybrał The Genesis Order do rozpoczęcia pełnego workflow lokalizacji; pozostałe tytuły nadal są niezapoczętymi kandydatami.

| Tytuł | Slug | Status | Następny krok |
|---|---|---|---|
| The Genesis Order | [`the-genesis-order`](games/the-genesis-order/README.md) | **Wybrany projekt; statyczny eksport 45 229 rekordów i znane powierzchnie zweryfikowane** | Uzyskać akceptację zakresu/semantycznych niepewności, ustalić politykę tłumaczenia i rozpocząć tłumaczenie; ZIP i patcher później. |
| Being a DIK | [`being-a-dik`](games/being-a-dik/README.md) | **Pełny statyczny census 158 skryptów `scripts.rpa` (Season 1) gotowy; kandydat niezatwierdzony** | Osobno zinwentaryzować UI/pozostałe teksty telefonu, przygotować branch-aware Czytankę i porównać zakresy. |
| Undercover with Nora | [`undercover-with-nora`](games/undercover-with-nora/README.md) | **Statyczny licznik dialogów gotowy dla przesłanej kopii v1.0.0; kandydat niezatwierdzony** | Osobno zinwentaryzować UI/screeny, a w razie wyboru przygotować branch-aware Czytankę i QA zakresu. |

## Dodanie kolejnego tytułu

1. Skopiuj strukturę opisaną w [`docs/PROJECT_TEMPLATE.md`](docs/PROJECT_TEMPLATE.md) do nowego `games/<slug>/`.
2. Ustal platformę, wydanie, język źródłowy i stan praw dostępu bez zakładania silnika.
3. Zapisz osobny status, fakty/hipotezy, dziennik eksperymentów, środowisko i zasady tłumaczenia tytułu.
4. Dodaj tytuł do tabeli dopiero po przygotowaniu jego README i AGENTS.
