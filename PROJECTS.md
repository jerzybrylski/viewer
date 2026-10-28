# Projekty i kandydaci

Każda visual novel ma własny katalog `games/<slug>/`. Statusy opisują wyłącznie dowody dostępne dla danego wydania; nie oznaczają, że właściciel wybrał już tytuł do tłumaczenia.

| Tytuł | Slug | Status | Następny krok |
|---|---|---|---|
| The Genesis Order | [`the-genesis-order`](games/the-genesis-order/README.md) | **RPG Maker MV 1.6.1 i fonty potwierdzone; pełne liczenie tekstów w toku** | Przygotować porównywalne liczniki zakresu oraz próbkę branch-aware Czytanki dla TGO i Being a DIK. |
| Being a DIK | [`being-a-dik`](games/being-a-dik/README.md) | **Wstępna analiza: technicznie osiągalne; kandydat niezatwierdzony** | Przed tłumaczeniem zdekompilować i policzyć treści, przygotować próbkę branch-aware Czytanki, a potem porównać zakres z TGO. |

## Dodanie kolejnego tytułu

1. Skopiuj strukturę opisaną w [`docs/PROJECT_TEMPLATE.md`](docs/PROJECT_TEMPLATE.md) do nowego `games/<slug>/`.
2. Ustal platformę, wydanie, język źródłowy i stan praw dostępu bez zakładania silnika.
3. Zapisz osobny status, fakty/hipotezy, dziennik eksperymentów, środowisko i zasady tłumaczenia tytułu.
4. Dodaj tytuł do tabeli dopiero po przygotowaniu jego README i AGENTS.
