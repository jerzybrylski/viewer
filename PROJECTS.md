# Projekty i kandydaci

Każda visual novel ma własny katalog `games/<slug>/`. Statusy opisują wyłącznie dowody dostępne dla danego wydania; nie oznaczają, że właściciel wybrał już tytuł do tłumaczenia.

| Tytuł | Slug | Status | Następny krok |
|---|---|---|---|
| The Genesis Order | [`the-genesis-order`](games/the-genesis-order/README.md) | **Inwentaryzacja odebrana; źródło kopii do potwierdzenia** | Po potwierdzeniu legalnej kopii przygotować pakiet #2: minimalny, wskazany zestaw JS/JSON bez mediów i bez modyfikacji gry. |
| Being a DIK | [`being-a-dik`](games/being-a-dik/README.md) | **Wstępna analiza: technicznie osiągalne; kandydat niezatwierdzony** | Ustalić, czy wybieramy ten tytuł i czy początkowym zakresem ma być Season 1 (dostępny w aktualnych plikach Drive), czy szersza całość. |

## Dodanie kolejnego tytułu

1. Skopiuj strukturę opisaną w [`docs/PROJECT_TEMPLATE.md`](docs/PROJECT_TEMPLATE.md) do nowego `games/<slug>/`.
2. Ustal platformę, wydanie, język źródłowy i stan praw dostępu bez zakładania silnika.
3. Zapisz osobny status, fakty/hipotezy, dziennik eksperymentów, środowisko i zasady tłumaczenia tytułu.
4. Dodaj tytuł do tabeli dopiero po przygotowaniu jego README i AGENTS.
