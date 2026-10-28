# Szablon nowego projektu VN

Skopiuj ten układ i zastąp `<slug>` oraz `<tytuł>`. Usuń sekcje, które nie pasują, ale nie kasuj rozróżnienia faktów, hipotez i niewiadomych.

```text
games/<slug>/
├── README.md
├── AGENTS.md
├── ENVIRONMENT.md
├── docs/
│   ├── STATUS.md
│   ├── TECHNICAL_FINDINGS.md
│   ├── EXPERIMENT_LOG.md
│   ├── TRANSLATION_POLICY.md
│   └── GLOSSARY.md
├── tools/                 # tylko narzędzia dla tego tytułu
└── local/                 # wyłączone z Git: wejścia, ekstrakty i zwrotki
```

## README.md

- tytuł, platforma, sklep/nośnik i potwierdzony build;
- cel tłumaczenia, status i najbliższy krok;
- krótki workflow, bez niepotwierdzonych szczegółów technicznych;
- linki do statusu, ustaleń, eksperymentów i zasad.

## AGENTS.md

- pliki, które trzeba przeczytać na początku sesji;
- fakty i decyzje właściciela, których nie wolno ponownie zgadywać;
- szczegóły konkretnej wersji gry, prywatnych wejść i Drive ID;
- blokady, otwarte pytania, testy i ograniczenia. Nie kopiuj notatek z innego tytułu.

## Status i dowody

`STATUS.md` używa etykiet **POTWIERDZONE**, **HIPOTEZA**, **NIEZNANE**, **NIEZWERYFIKOWANE**. `TECHNICAL_FINDINGS.md` zapisuje wyniki pomiarów, a `EXPERIMENT_LOG.md` każdą próbę: data, wersja, wejścia (nazwy/rozmiary/hashe/Drive ID), narzędzie i wersja, dokładne polecenie, wynik, ograniczenia, następny krok.

## Pierwsze pytania

Platforma? Źródło zakupu/nośnik? Wersja/build i DLC? Język tekstu źródłowego? Który zakres (dialogi, UI, grafiki, dodatki)? Czy użytkownik chce patch, mod czy na razie pakiet do tłumaczenia? Pozostaw nieznane, jeśli nie ustalono.
