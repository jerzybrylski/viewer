# Audyt pokrycia draftów — The Genesis Order

> Plik generowany przez `tools/audit_draft_coverage.py`. Liczby pochodzą wyłącznie z kanonicznego eksportu i plików `translation/drafts/` (rekurencyjnie). Etykiety kubełków są dowodem, nie decyzją tłumaczeniową.

## Podsumowanie

- Rekordy kanoniczne: **45 229**.
- Pliki draftów: **425**, wierszy: **45 742**.
- Unikalne ID z niepustym tłumaczeniem: **39 821**.
- Puste rekordy ogółem: **5 408**, w tym **131** chronionych `keep_source_value` i **5 277** do rozstrzygnięcia.
- Konflikty niepustych wariantów: **40**.
- Tłumaczenia identyczne ze źródłem w kategorii prozatorskiej: **616**.

## Kubełki pustych rekordów

| Kubełek | Rekordy | Znaczenie |
|---|---:|---|
| `blocked_by_signature` | 94 | sygnatura v1 skleja tag `\fb` z pierwszym słowem (ADR 002) |
| `command` | 3 742 | komendy `custom_dialogue` zaczynające się od `/` — sterowanie, nie proza |
| `credits_roster` | 234 | listy nazw wspierających — nazw nie tłumaczymy |
| `identifier` | 7 | kody, liczby i krótkie markery |
| `markup_only` | 1 072 | po usunięciu tokenów nie zostaje żadna litera |
| `needs_review` | 30 | realny tekst bez tłumaczenia — wymaga decyzji i draftu |
| `proper_name` | 91 | imiona postaci, nazwy przedmiotów, podpisy galerii |
| `protected` | 131 | `keep_source_value` — wartość musi zostać bez zmian |
| `template_placeholder` | 7 | wypełniacz szablonu mapy testowej |

## Pokrycie według kategorii

| Kategoria | Rekordy | Z tłumaczeniem | Puste |
|---|---:|---:|---:|
| `arianna_hint` | 705 | 705 | 0 |
| `choice_option` | 1 930 | 1 416 | 514 |
| `credits` | 239 | 2 | 237 |
| `custom_dialogue` | 38 638 | 34 714 | 3 924 |
| `database.actors.name` | 28 | 0 | 28 |
| `database.items.name` | 477 | 475 | 2 |
| `image_caption` | 134 | 66 | 68 |
| `item_found_label` | 649 | 648 | 1 |
| `map_label` | 291 | 290 | 1 |
| `native_message` | 1 122 | 692 | 430 |
| `phone_contact_ui` | 378 | 352 | 26 |
| `phone_text` | 30 | 26 | 4 |
| `system.armorTypes` | 6 | 6 | 0 |
| `system.currencyUnit` | 1 | 0 | 1 |
| `system.elements` | 9 | 9 | 0 |
| `system.equipTypes` | 5 | 5 | 0 |
| `system.gameTitle` | 1 | 0 | 1 |
| `system.skillTypes` | 2 | 2 | 0 |
| `system.terms` | 95 | 95 | 0 |
| `system.weaponTypes` | 12 | 12 | 0 |
| `ui.engine_static` | 4 | 4 | 0 |
| `ui.plugin_parameter` | 9 | 9 | 0 |
| `ui.plugin_static` | 22 | 19 | 3 |
| `ui.variable_value` | 262 | 107 | 155 |
| `ui_choice` | 180 | 167 | 13 |

## Rekordy `needs_review` (30)

| ID | Kategoria | Źródło | Zdarzenie |
|---|---|---|---|
| `tgo:choice_unclassified:0c859be5334ca162935e` | `choice_option` | \c[17]\v[328]\c[27]Carol | EV018 |
| `tgo:choice_unclassified:1a4893ed1666550f97f3` | `choice_option` | \c[17]\v[322]\c[27]Melissa  | EV018 |
| `tgo:choice_unclassified:2471e8f0ddd8e1ad838c` | `choice_option` | \c[17]\v[328]\c[27]Carol | EV097 |
| `tgo:choice_unclassified:2a177fcff8696e92f009` | `choice_option` | \c[17]\v[329]\c[27]Erica | EV018 |
| `tgo:choice_unclassified:4681a4c39d523b713165` | `choice_option` | \c[17]\v[329]\c[27]Erica | EV097 |
| `tgo:choice_unclassified:6392a246c2c309e49ead` | `choice_option` | \c[17]\v[327]\c[27]Lillian | EV018 |
| `tgo:choice_unclassified:63cc1667a8769acc4fb1` | `choice_option` | \c[17]\v[326]\c[27]Judy | EV018 |
| `tgo:choice_unclassified:71823edb268eb9e2f2c2` | `choice_option` | \c[17]\v[324]\c[27]Chloe | EV018 |
| `tgo:choice_unclassified:76825db0d780ce4434a1` | `choice_option` | \c[17]\v[327]\c[27]Lillian | EV097 |
| `tgo:choice_unclassified:8a59aee48d8660fd31cd` | `choice_option` | \c[17]\v[332]\c[27]Kimberly | EV097 |
| `tgo:choice_unclassified:8bbcb679269c95fdc6d8` | `choice_option` | \c[17]\v[322]\c[27]Melissa  | EV097 |
| `tgo:choice_unclassified:9871bc2b3feed1bfd57b` | `choice_option` | \c[17]\v[325]\c[27]Hannah | EV018 |
| `tgo:choice_unclassified:98d53a2494d6ba7b5a58` | `choice_option` | \c[17]\v[332]\c[27]Kimberly | EV018 |
| `tgo:choice_unclassified:9ce6a07072eecd9939f2` | `choice_option` | \c[17]\v[326]\c[27]Judy | EV097 |
| `tgo:choice_unclassified:ac2e2a39c0b2af4f8f56` | `choice_option` | \c[17]\v[331]\c[27]Nellie | EV097 |
| `tgo:choice_unclassified:ac3152822a86230a7a6b` | `choice_option` | \c[17]\v[324]\c[27]Chloe | EV097 |
| `tgo:choice_unclassified:c9ceb3f430ab9ba33041` | `choice_option` | \c[17]\v[330]\c[27]Ella | EV018 |
| `tgo:choice_unclassified:d2313e4bf3d6fe4e7835` | `choice_option` | \c[17]\v[333]\c[27]Andrea | EV018 |
| `tgo:choice_unclassified:d4f52fd6efe4f5979f68` | `choice_option` | \c[17]\v[331]\c[27]Nellie | EV018 |
| `tgo:choice_unclassified:d729963ab810995685d7` | `choice_option` | \c[17]\v[333]\c[27]Andrea | EV097 |
| `tgo:choice_unclassified:d798e20b7631150275b1` | `choice_option` | \c[17]\v[323]\c[27]Heather | EV097 |
| `tgo:choice_unclassified:de0ad8e17c280fbf34e1` | `choice_option` | \c[17]\v[323]\c[27]Heather | EV018 |
| `tgo:choice_unclassified:deebf0775b9840245dbc` | `choice_option` | \c[17]\v[330]\c[27]Ella | EV097 |
| `tgo:choice_unclassified:ebcc55ec8d129b55be3d` | `choice_option` | \c[17]\v[325]\c[27]Hannah | EV097 |
| `tgo:map_label:95c1550fdebfe6c2f140` | `map_label` | WoNoChurch |  |
| `tgo:native_message_unclassified:7260eb2826e225c5cb07` | `native_message` | <center><br><br>Madalyn. | SCN - Chloe Flashback |
| `tgo:native_message_unclassified:7f56b2ebd8ae356257bf` | `native_message` | Morgan #142 | EV034 |
| `tgo:phone_contact_ui:c4d223c2fdc3b48773f7` | `phone_contact_ui` | Morgan. | PHONE - Select Item |
| `tgo:phone_contact_ui:ed360055b018450dcc38` | `phone_contact_ui` | Amulet K. | PHONE - Select Item |
| `tgo:system.gameTitle:5546cb9d6b2245f37473` | `system.gameTitle` | The Genesis Order |  |

## Konflikty niepustych wariantów (40)

| ID | Źródło | Warianty |
|---|---|---|
| `tgo:map_label:01152277af5c79d430fe` | Foyer | `inventory-names-01.jsonl` → Hol<br>`inventory-names-02.jsonl` → Hol wejściowy<br>`map-labels-01.jsonl` → Hol wejściowy |
| `tgo:map_label:0f8dc604fab5140669d6` | Storage Room | `inventory-names-01.jsonl` → Pomieszczenie magazynowe<br>`inventory-names-02.jsonl` → Składzik<br>`map-labels-01.jsonl` → Składzik |
| `tgo:map_label:0fc3f5e97bda05cf0c6b` | Storage | `inventory-names-01.jsonl` → Schowek<br>`inventory-names-02.jsonl` → Magazyn<br>`map-labels-01.jsonl` → Magazyn |
| `tgo:map_label:1827eb9c397129b3fb28` | Secret Room | `inventory-names-01.jsonl` → Tajny pokój<br>`inventory-names-02.jsonl` → Tajne pomieszczenie<br>`map-labels-01.jsonl` → Tajne pomieszczenie |
| `tgo:map_label:1afd1c49d31ace03b815` | Dock | `inventory-names-01.jsonl` → Doki<br>`inventory-names-02.jsonl` → Pomost<br>`map-labels-01.jsonl` → Pomost |
| `tgo:map_label:277fccf5044f182b1909` | NorthMostCreek | `inventory-names-01.jsonl` → Najbardziej na północ wysunięty strumień<br>`inventory-names-02.jsonl` → Najbardziej wysunięty na północ strumień<br>`map-labels-01.jsonl` → Najbardziej wysunięty na północ strumień |
| `tgo:map_label:35444eb111fb7f66b9d6` | Entryway | `inventory-names-01.jsonl` → Przedpokój<br>`inventory-names-02.jsonl` → Przedsionek<br>`map-labels-01.jsonl` → Przedsionek |
| `tgo:map_label:3960d37d97a5fd59ee4d` | Cumshot Game | `inventory-names-01.jsonl` → Gra w wytrysk<br>`inventory-names-02.jsonl` → Gra w cumshoty<br>`map-labels-01.jsonl` → Gra w cumshoty |
| `tgo:map_label:408e7a1f207ce002ca09` | Storage | `inventory-names-01.jsonl` → Schowek<br>`inventory-names-02.jsonl` → Magazyn<br>`map-labels-01.jsonl` → Magazyn |
| `tgo:map_label:4c29c55252c10d706708` | PRE TITLE | `inventory-names-01.jsonl` → PRZED TYTUŁEM<br>`inventory-names-02.jsonl` → PRZED EKRANEM TYTUŁOWYM<br>`map-labels-01.jsonl` → PRZED EKRANEM TYTUŁOWYM |
| `tgo:map_label:5a930990f1caadb3b111` | Changing Room | `inventory-names-01.jsonl` → Przebieralnia<br>`inventory-names-02.jsonl` → Szatnia<br>`map-labels-01.jsonl` → Szatnia |
| `tgo:map_label:623675ba05d689effe6c` | Storage | `inventory-names-01.jsonl` → Schowek<br>`inventory-names-02.jsonl` → Magazyn<br>`map-labels-01.jsonl` → Magazyn |
| `tgo:map_label:63542e1174a6f0719600` | Ellas Entry | `inventory-names-01.jsonl` → Wejście do Elli<br>`inventory-names-02.jsonl` → Wejście Elli<br>`map-labels-01.jsonl` → Wejście Elli |
| `tgo:map_label:6480db9f0707b21d19a0` | North Main Entry | `inventory-names-01.jsonl` → Północne główne wejście<br>`inventory-names-02.jsonl` → Główne wejście od północy<br>`map-labels-01.jsonl` → Główne wejście od północy |
| `tgo:map_label:64d773f024c1586789d9` | Channel 4 | `inventory-names-01.jsonl` → Kanał 4<br>`inventory-names-02.jsonl` → Channel 4<br>`map-labels-01.jsonl` → Channel 4 |
| `tgo:map_label:6e5f017fc0f7e7e1338b` | Lobby | `inventory-names-01.jsonl` → Hol wejściowy<br>`inventory-names-02.jsonl` → Hol<br>`map-labels-01.jsonl` → Hol |
| `tgo:map_label:72f427d7aa5e2726bb74` | Int Room 2 | `inventory-names-01.jsonl` → Wewnętrzny pokój 2<br>`inventory-names-02.jsonl` → Pomieszczenie wewnętrzne 2<br>`map-labels-01.jsonl` → Pomieszczenie wewnętrzne 2 |
| `tgo:map_label:7b5057bbcb6d0707f659` | 2nd Story West Room | `inventory-names-01.jsonl` → Pokój na zachodzie drugiego piętra<br>`inventory-names-02.jsonl` → 2. piętro — pokój zachodni<br>`map-labels-01.jsonl` → 2. piętro — pokój zachodni |
| `tgo:map_label:7c497c9e72e11dcda3a9` | Lake West | `inventory-names-01.jsonl` → Zachodnia część jeziora<br>`inventory-names-02.jsonl` → Zachód jeziora<br>`map-labels-01.jsonl` → Zachód jeziora |
| `tgo:map_label:8d356ab9adfb2853795d` | Melissa Condo Entry | `inventory-names-01.jsonl` → Wejście do mieszkania Melissy<br>`inventory-names-02.jsonl` → Wejście do apartamentu Melissy<br>`map-labels-01.jsonl` → Wejście do apartamentu Melissy |
| `tgo:map_label:9129b6fc70624ae2d481` | Bunk Room | `inventory-names-01.jsonl` → Pokój z łóżkami piętrowymi<br>`inventory-names-02.jsonl` → Pokój w bunkrze<br>`map-labels-01.jsonl` → Pokój w bunkrze |
| `tgo:map_label:92646d6974da2e30334b` | Courtyard West | `inventory-names-01.jsonl` → Zachodni dziedziniec<br>`inventory-names-02.jsonl` → Zachodnia część dziedzińca<br>`map-labels-01.jsonl` → Zachodnia część dziedzińca |
| `tgo:map_label:a65f6a3c5653e6c502ba` | Junkroom | `inventory-names-01.jsonl` → Pokój na graty<br>`inventory-names-02.jsonl` → Pokój rupieci<br>`map-labels-01.jsonl` → Pokój rupieci |
| `tgo:map_label:ad57e0911e756d39f488` | Media Room | `inventory-names-01.jsonl` → Pokój multimedialny<br>`inventory-names-02.jsonl` → Sala multimedialna<br>`map-labels-01.jsonl` → Sala multimedialna |
| `tgo:map_label:c33eba4cf3f995a3f14d` | Bunker Mid | `inventory-names-01.jsonl` → Środek bunkra<br>`inventory-names-02.jsonl` → Środkowa część bunkra<br>`map-labels-01.jsonl` → Środkowa część bunkra |
| `tgo:map_label:c35e2ec728732a6ba60f` | Lake North | `inventory-names-01.jsonl` → Północna część jeziora<br>`inventory-names-02.jsonl` → Północ jeziora<br>`map-labels-01.jsonl` → Północ jeziora |
| `tgo:map_label:c7211a087debc125b701` | Middle South | `inventory-names-01.jsonl` → Południowy środek<br>`inventory-names-02.jsonl` → Południowa część środka<br>`map-labels-01.jsonl` → Południowa część środka |
| `tgo:map_label:cdceec71dff308c21513` | 2nd Stroy Right | `inventory-names-01.jsonl` → Drugie piętro — prawa strona<br>`inventory-names-02.jsonl` → 2. piętro — prawa strona<br>`map-labels-01.jsonl` → 2. piętro — prawa strona |
| `tgo:map_label:cee3d9917845d8210c1b` | 2nd Story Left | `inventory-names-01.jsonl` → Drugie piętro — lewa strona<br>`inventory-names-02.jsonl` → 2. piętro — lewa strona<br>`map-labels-01.jsonl` → 2. piętro — lewa strona |
| `tgo:map_label:d5f7c54e27bd85c4c1d1` | Foyer | `inventory-names-01.jsonl` → Hol<br>`inventory-names-02.jsonl` → Hol wejściowy<br>`map-labels-01.jsonl` → Hol wejściowy |
| `tgo:map_label:da319999be623fcc063c` | Above Entry West | `inventory-names-01.jsonl` → Na zachód od wejścia, piętro wyżej<br>`inventory-names-02.jsonl` → Na zachód nad wejściem<br>`map-labels-01.jsonl` → Na zachód nad wejściem |
| `tgo:map_label:dee5d8c5a4150a25c83e` | Front Rubble | `inventory-names-01.jsonl` → Gruz przed wejściem<br>`inventory-names-02.jsonl` → Gruzy przed wejściem<br>`map-labels-01.jsonl` → Gruzy przed wejściem |
| `tgo:map_label:dfc842de395765e3b776` | Strip Center | `inventory-names-01.jsonl` → Pasaż handlowy<br>`inventory-names-02.jsonl` → Centrum handlowe<br>`map-labels-01.jsonl` → Centrum handlowe |
| `tgo:map_label:e8c435817646928dd9d9` | Lake South | `inventory-names-01.jsonl` → Południowa część jeziora<br>`inventory-names-02.jsonl` → Południe jeziora<br>`map-labels-01.jsonl` → Południe jeziora |
| `tgo:map_label:e8fba1a9118c43241e4f` | Mels Kitchen | `inventory-names-01.jsonl` → Kuchnia Mel<br>`inventory-names-02.jsonl` → Kuchnia Meli<br>`map-labels-01.jsonl` → Kuchnia Meli |
| `tgo:map_label:e94d009d9401f37e888e` | MC Home | `inventory-names-01.jsonl` → Dom głównego bohatera<br>`inventory-names-02.jsonl` → Dom bohatera<br>`map-labels-01.jsonl` → Dom bohatera |
| `tgo:map_label:f02ca14d1078913582db` | Mels Bedroom | `inventory-names-01.jsonl` → Sypialnia Mel<br>`inventory-names-02.jsonl` → Sypialnia Meli<br>`map-labels-01.jsonl` → Sypialnia Meli |
| `tgo:map_label:f76d5f6e996173b96434` | Entryway | `inventory-names-01.jsonl` → Przedpokój<br>`inventory-names-02.jsonl` → Przedsionek<br>`map-labels-01.jsonl` → Przedsionek |
| `tgo:map_label:fc9c6af951bf2da2c415` | Police Station | `inventory-names-01.jsonl` → Komisariat<br>`inventory-names-02.jsonl` → Komisariat policji<br>`map-labels-01.jsonl` → Komisariat policji |
| `tgo:map_label:fd18931dc4e26846ee6f` | Condos | `inventory-names-01.jsonl` → Mieszkania<br>`inventory-names-02.jsonl` → Apartamentowce<br>`map-labels-01.jsonl` → Apartamentowce |

## Tłumaczenia identyczne ze źródłem (616)

| ID | Kategoria | Plik | Tekst |
|---|---|---|---|
| `tgo:choice_unclassified:1224b5d8777280d3737b` | `choice_option` | `choice-ui-01.jsonl` | Anal |
| `tgo:choice_unclassified:1b8903deae198c61c36f` | `choice_option` | `choice-ui-01.jsonl` | Anal |
| `tgo:choice_unclassified:a3636dc9ba778079e553` | `choice_option` | `choice-ui-01.jsonl` | Demon |
| `tgo:custom_dialogue:01eadb6b0292564ad530` | `custom_dialogue` | `custom-dialogue-common-event-385-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:0d6969c99cc6b464b0e4` | `custom_dialogue` | `custom-dialogue-common-event-350-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:2974fcc843cc6c753cff` | `custom_dialogue` | `custom-dialogue-common-event-387-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:29c9b7ba7637f702ce55` | `custom_dialogue` | `custom-dialogue-common-event-390-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:360f08d4235170c32cc8` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:4cc06bf9b76e99fa4469` | `custom_dialogue` | `custom-dialogue-common-event-483-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:5bada381bbd7451eb0b6` | `custom_dialogue` | `custom-dialogue-common-event-427-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:69f9d96a02fd54e4d0ef` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:6ae39955167fa0c06662` | `custom_dialogue` | `custom-dialogue-common-event-433-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:6db4215dd0ac79e16c35` | `custom_dialogue` | `custom-dialogue-map55-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:70675a478474a22eadb5` | `custom_dialogue` | `custom-dialogue-common-event-452-02.jsonl` | 1Hero! |
| `tgo:custom_dialogue:766b354d88443d2a7868` | `custom_dialogue` | `custom-dialogue-map202-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:80a9443b9f3b9d338f54` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | 1Hero! |
| `tgo:custom_dialogue:8169f520545ffc3a2549` | `custom_dialogue` | `custom-dialogue-common-event-411-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:888e11be826a732c4aac` | `custom_dialogue` | `custom-dialogue-map120-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:9125c1ca719e4700d3c5` | `custom_dialogue` | `custom-dialogue-common-event-493-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:9373bed0048d2ea37db3` | `custom_dialogue` | `custom-dialogue-map55-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:94429df84c37652e4311` | `custom_dialogue` | `custom-dialogue-common-event-457-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:94ca9da8d604cf7465e3` | `custom_dialogue` | `custom-dialogue-common-event-443-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:98bc71355327cb1f2812` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:a3f3c543863931b653df` | `custom_dialogue` | `custom-dialogue-map277-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:a9382cf401289d416625` | `custom_dialogue` | `custom-dialogue-common-event-451-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:b61506f6aa31a76545b8` | `custom_dialogue` | `custom-dialogue-map116-event-4-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:b74ea6e45982df64ab4a` | `custom_dialogue` | `custom-dialogue-map76-kimura-home-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:b86b6c6c43fb5fc61b3a` | `custom_dialogue` | `custom-dialogue-map116-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:c523e9bd6d641eb72a25` | `custom_dialogue` | `custom-dialogue-map11-gym-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:c63356030b6405010d12` | `custom_dialogue` | `custom-dialogue-map291-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:c6fccf66a3db9823f9cc` | `custom_dialogue` | `custom-dialogue-common-event-385-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:cb014023b157dd578dc8` | `custom_dialogue` | `custom-dialogue-map3-event-39-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:cc774452396dc6e2c550` | `custom_dialogue` | `custom-dialogue-common-event-495-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:cff07ebf8a1546105717` | `custom_dialogue` | `custom-dialogue-map82-channel4-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:d0f188e6ec077e725d5a` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | 1Hero! |
| `tgo:custom_dialogue:e74270af8104cc5bc5db` | `custom_dialogue` | `custom-dialogue-common-event-433-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:e8a569182fe8a7440a66` | `custom_dialogue` | `custom-dialogue-map20-event-61-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:edde9a2c5ba04d0cc667` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:f063215e012785d6119a` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 1Hero! |
| `tgo:custom_dialogue:f1a86035228a735ee16f` | `custom_dialogue` | `custom-dialogue-common-event-349-02.jsonl` | 1Hero! |
| `tgo:custom_dialogue:faea3ccef58cafccd202` | `custom_dialogue` | `custom-dialogue-map200-followups-01.jsonl` | 1Hero! |
| `tgo:custom_dialogue:1bb8aa166831037d61f8` | `custom_dialogue` | `custom-dialogue-map43-followups-01.jsonl` | 1Hero!  |
| `tgo:custom_dialogue:87a074c6036bc5c35f57` | `custom_dialogue` | `custom-dialogue-map32-station-followups-01.jsonl` | 1Hero!  |
| `tgo:custom_dialogue:6ad6db74d0a99ef12501` | `custom_dialogue` | `custom-dialogue-map149-followups-01.jsonl` | 1Hero!... |
| `tgo:custom_dialogue:032e616cdb2addd19b0b` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:03af8d66b4dd9549717d` | `custom_dialogue` | `custom-dialogue-map23-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:0c1873ba148980f5e924` | `custom_dialogue` | `custom-dialogue-common-event-354-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:184b88c5283ca0566ea3` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:223acd21f7c5258a91ea` | `custom_dialogue` | `custom-dialogue-common-event-358-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:38129e557c112f64be82` | `custom_dialogue` | `custom-dialogue-map20-church-event-48-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:38fb4778aa3e41262322` | `custom_dialogue` | `custom-dialogue-common-event-470-02.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:5f26d7ec14f8851a1888` | `custom_dialogue` | `custom-dialogue-map119-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:68bf7160d49cf7f8bc48` | `custom_dialogue` | `custom-dialogue-map63-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:6fe7e7647b985dee694d` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-02.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:718aba6dd4784909d91e` | `custom_dialogue` | `custom-dialogue-common-event-428-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:7567379d6f9fc3a761fc` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:77c4ec68d3cb5a2c92f3` | `custom_dialogue` | `custom-dialogue-map60-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:77c7f5ea6b71f3191c2a` | `custom_dialogue` | `custom-dialogue-map35-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:7cad19237a244b295911` | `custom_dialogue` | `custom-dialogue-common-event-342-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:8504ae654d6745687847` | `custom_dialogue` | `custom-dialogue-common-event-383-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:8d3fa412d636d7309bdc` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:937a25ecbc4fb3f12851` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:93a90ac50832d99673dc` | `custom_dialogue` | `custom-dialogue-map183-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:b0f52cacadcee6b51fc9` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:c46462f3f8ff45b0c781` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:cfb5aa56c134a96df74c` | `custom_dialogue` | `custom-dialogue-map51-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:d2151c0129a43513ee17` | `custom_dialogue` | `custom-dialogue-common-event-375-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:dc11dd6a583ceb4edd09` | `custom_dialogue` | `custom-dialogue-map79-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:de9b3921551b7e48f620` | `custom_dialogue` | `custom-dialogue-map204-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:e7d97ab7827747c4e2fe` | `custom_dialogue` | `custom-dialogue-common-event-326-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:f1e4ccab09a0c97c06b2` | `custom_dialogue` | `custom-dialogue-map107-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:f402246d4030084a024c` | `custom_dialogue` | `custom-dialogue-common-event-453-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:f8dca472550a0d9176b3` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:f9130bcd3d068ec30344` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:fb047ea2147210ef9ff4` | `custom_dialogue` | `custom-dialogue-common-event-428-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:fb53c89a570fcf566374` | `custom_dialogue` | `custom-dialogue-map204-followups-01.jsonl` | 1Hero!? |
| `tgo:custom_dialogue:b2a9cc470f66f1bad736` | `custom_dialogue` | `custom-dialogue-map87-mansion-ambush-followups-01.jsonl` | 1Hero!?  |
| `tgo:custom_dialogue:eba8439afbe86934caac` | `custom_dialogue` | `custom-dialogue-map6-church-followups-01.jsonl` | 1Hero!?... |
| `tgo:custom_dialogue:fe88f0b3c57d6c1c2633` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | 1Hero!?... |
| `tgo:custom_dialogue:8adb77daeaf9c965d831` | `custom_dialogue` | `custom-dialogue-map17-followups-01.jsonl` | 1Hero. |
| `tgo:custom_dialogue:da7989a0d9db6dd2b52c` | `custom_dialogue` | `custom-dialogue-map26-mansion-followups-01.jsonl` | 1Hero. |
| `tgo:custom_dialogue:0ef633f0fff373cbc24a` | `custom_dialogue` | `custom-dialogue-map73-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:1c5015af8ad11787629a` | `custom_dialogue` | `custom-dialogue-scene-judy-masturbate-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:1d38edf3214f8efe0e3c` | `custom_dialogue` | `custom-dialogue-map116-event-89-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:1f9c2b663bc09f732d06` | `custom_dialogue` | `custom-dialogue-map18-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:20f2a69c34e79fd527e1` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:27ee7db2ae2987f90047` | `custom_dialogue` | `custom-dialogue-map31-event-15-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:2f212b519db7c788b3f5` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:3619f19b603fe898c99d` | `custom_dialogue` | `custom-dialogue-map81-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:3d0c55727a8d63c94528` | `custom_dialogue` | `custom-dialogue-map124-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:42b20ea2cdc8376135ab` | `custom_dialogue` | `custom-dialogue-map99-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:4e4cddd6a1435f2e3bdd` | `custom_dialogue` | `custom-dialogue-map76-kimura-home-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:5ace855ad2f43084ff31` | `custom_dialogue` | `custom-dialogue-map56-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:65f7faeed6c653b4328b` | `custom_dialogue` | `custom-dialogue-map6-church-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:69a6a9d11fc1c71c5e7b` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:6f23ce18c456af3403a1` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 1Hero? |
| `tgo:custom_dialogue:7d4b119bb4d053999c55` | `custom_dialogue` | `custom-dialogue-map27-housewarming-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:7fb3576d94b421e063f2` | `custom_dialogue` | `custom-dialogue-common-event-390-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:a581b95a0ee971273f19` | `custom_dialogue` | `custom-dialogue-map30-dicks-restaurant-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:aa661798ffef90adb65c` | `custom_dialogue` | `custom-dialogue-common-event-445-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:ab75d65e8e7b1d5346ab` | `custom_dialogue` | `custom-dialogue-map5-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:b3c4d71212dd78d9efab` | `custom_dialogue` | `custom-dialogue-common-event-381-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:bd9c0a7e1c504f208b47` | `custom_dialogue` | `custom-dialogue-map21-chapel-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:bfbc5de1904e0752f3e5` | `custom_dialogue` | `custom-dialogue-common-event-381-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:c09719d9747c11ea2836` | `custom_dialogue` | `custom-dialogue-map20-foyer-heather-arianna-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:c1f1c8a7c0344a488bec` | `custom_dialogue` | `custom-dialogue-map23-followups-02.jsonl` | 1Hero? |
| `tgo:custom_dialogue:d28c995cdcb5f6214b8a` | `custom_dialogue` | `custom-dialogue-map4-apartments-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:d6db78c4746fea901c71` | `custom_dialogue` | `custom-dialogue-map3-event-22-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:ddd19d13e4cae6034316` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 1Hero? |
| `tgo:custom_dialogue:f119ce2cfe2938d34743` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | 1Hero? |
| `tgo:custom_dialogue:8cd419c153dd3898af56` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | 1Hero?! |
| `tgo:custom_dialogue:cf48a278a5c59410f465` | `custom_dialogue` | `custom-dialogue-common-event-418-01.jsonl` | 1Hero?... |
| `tgo:custom_dialogue:02ef09acf482c7b7b885` | `custom_dialogue` | `custom-dialogue-common-event-452-02.jsonl` | 1Hero… |
| `tgo:custom_dialogue:0bfd778cc95e743168db` | `custom_dialogue` | `custom-dialogue-map22-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:19b85e5eae4f3480fa85` | `custom_dialogue` | `custom-dialogue-scene-judy-masturbate-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:49f580b0a3cd3e06b542` | `custom_dialogue` | `custom-dialogue-map15-warehouse-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:4f4c34a30b04ed327c77` | `custom_dialogue` | `custom-dialogue-map24-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:882b340521cb5d7edd60` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:9c6e110afe4671217e98` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:a139c2cc23709b12d61a` | `custom_dialogue` | `custom-dialogue-map9-event-114-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:c43aa4900c5b0f9ddb52` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:cca652c703e3614d3ec6` | `custom_dialogue` | `custom-dialogue-common-event-388-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:d2d01e4e7bd6b8984941` | `custom_dialogue` | `custom-dialogue-map82-channel4-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:d492548323a979d6ef4a` | `custom_dialogue` | `custom-dialogue-common-event-433-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:f2c0f3e856ad91b16d81` | `custom_dialogue` | `custom-dialogue-map19-followups-01.jsonl` | 1Hero… |
| `tgo:custom_dialogue:c3b4d477d6f9fbf49087` | `custom_dialogue` | `custom-dialogue-map200-followups-01.jsonl` | Adios, Daemalius. |
| `tgo:custom_dialogue:3beb11581295efe3e29f` | `custom_dialogue` | `custom-dialogue-common-event-383-01.jsonl` | Aghuha… |
| `tgo:custom_dialogue:58dfd1bd4a395504c0ca` | `custom_dialogue` | `custom-dialogue-common-event-477-01.jsonl` | Ahahaha! |
| `tgo:custom_dialogue:38125a3ae5071be552ad` | `custom_dialogue` | `custom-dialogue-map31-event-25-01.jsonl` | Alia! |
| `tgo:custom_dialogue:2ff811cf456784e9c2bb` | `custom_dialogue` | `custom-dialogue-common-event-npc-barks-followups-01.jsonl` | Amulet K? |
| `tgo:custom_dialogue:76278966a55936fb496a` | `custom_dialogue` | `custom-dialogue-map20-church-event-48-01.jsonl` | Amulet? |
| `tgo:custom_dialogue:09882bdf66bdd60073fa` | `custom_dialogue` | `custom-dialogue-map200-followups-01.jsonl` | Andrea! |
| `tgo:custom_dialogue:40c05b2348415403bb3f` | `custom_dialogue` | `custom-dialogue-common-event-365-01.jsonl` | Andrea! |
| `tgo:custom_dialogue:8bb0bf9bd182c6792b53` | `custom_dialogue` | `custom-dialogue-common-event-431-01.jsonl` | Andrea! |
| `tgo:custom_dialogue:43c4c4dcfd4c88bf85ec` | `custom_dialogue` | `custom-dialogue-map32-station-followups-01.jsonl` | Andrea!? |
| `tgo:custom_dialogue:b4bdc7d09788f96721ca` | `custom_dialogue` | `custom-dialogue-common-event-394-01.jsonl` | Andrea!? |
| `tgo:custom_dialogue:0659477c1b3bb7ad3538` | `custom_dialogue` | `custom-dialogue-map144-library-followups-01.jsonl` | Andrea? |
| `tgo:custom_dialogue:40ff63a624f8cbb383be` | `custom_dialogue` | `custom-dialogue-scene-andrea-kim-3some-01.jsonl` | Andrea? |
| `tgo:custom_dialogue:4ec497d0812f80d117fe` | `custom_dialogue` | `custom-dialogue-scene-andrea-kim-3some-01.jsonl` | Andrea? |
| `tgo:custom_dialogue:530300f2be8912c67719` | `custom_dialogue` | `custom-dialogue-scene-andrea-nellie-tub-01.jsonl` | Andrea? |
| `tgo:custom_dialogue:4853a61bc414391353b0` | `custom_dialogue` | `custom-dialogue-map34-commissioner-followups-01.jsonl` | Argh!! |
| `tgo:custom_dialogue:3852fd4d0d31952b5ae1` | `custom_dialogue` | `custom-dialogue-map121-followups-01.jsonl` | Arianna! |
| `tgo:custom_dialogue:3d4ffc52f921c8a24312` | `custom_dialogue` | `custom-dialogue-map102-followups-01.jsonl` | Arianna! |
| `tgo:custom_dialogue:df200d33fa33406fa956` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-01.jsonl` | Arianna! |
| `tgo:custom_dialogue:e1b46684821ebce27f38` | `custom_dialogue` | `custom-dialogue-map56-followups-01.jsonl` | Arianna! |
| `tgo:custom_dialogue:f140df92a123a01b9c1e` | `custom_dialogue` | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | Arianna! |
| `tgo:custom_dialogue:3e45f88d2ffa44919edd` | `custom_dialogue` | `custom-dialogue-scene-orgy-01.jsonl` | Arianna!? |
| `tgo:custom_dialogue:699e696bd8a2186d981f` | `custom_dialogue` | `custom-dialogue-map183-followups-01.jsonl` | Arianna? |
| `tgo:custom_dialogue:9f4b1c0d400593245796` | `custom_dialogue` | `custom-dialogue-map82-channel4-followups-01.jsonl` | Arianna? |
| `tgo:custom_dialogue:96eea1c231782bdbe9c3` | `custom_dialogue` | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | Arianna?... |
| `tgo:custom_dialogue:b7cf6ff220a882bffcb8` | `custom_dialogue` | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | Arianna?... |
| `tgo:custom_dialogue:186e894170549e9954fd` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Awww! |
| `tgo:custom_dialogue:470003882010603fc22d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Awww! |
| `tgo:custom_dialogue:6e7073746da5ec76c2c7` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Awww! |
| `tgo:custom_dialogue:1f478aaf3eb7eff770fd` | `custom_dialogue` | `custom-dialogue-map12-arianna-followups-01.jsonl` | Awwwwwwww!!! |
| `tgo:custom_dialogue:1841dfc388d588e9ca5a` | `custom_dialogue` | `custom-dialogue-map240-followups-01.jsonl` | Big Man. |
| `tgo:custom_dialogue:1afcb1cd20760ec24a80` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-02.jsonl` | Bingo! |
| `tgo:custom_dialogue:0a134102bf7475e69e5d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Bingo. |
| `tgo:custom_dialogue:0a82083fc784c2b6a84f` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Bingo. |
| `tgo:custom_dialogue:7bbe703681033db3f65d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Bingo. |
| `tgo:custom_dialogue:9c3d6f8bcd24d55a2714` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Bingo. |
| `tgo:custom_dialogue:fa2130c51d26b067bd2d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Bingo. |
| `tgo:custom_dialogue:b9bf37b49f8107ccda48` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | Bobby! |
| `tgo:custom_dialogue:bf6b4245af9577ad1ee2` | `custom_dialogue` | `custom-dialogue-map6-church-followups-01.jsonl` | Bobby!? |
| `tgo:custom_dialogue:1cd3d6b2e7b9996cc8b4` | `custom_dialogue` | `custom-dialogue-map53-followups-01.jsonl` | Brian!? |
| `tgo:custom_dialogue:5121a10fea51379841dc` | `custom_dialogue` | `custom-dialogue-common-event-348-01.jsonl` | Canmore. |
| `tgo:custom_dialogue:0a591f7f18d956d2dc5c` | `custom_dialogue` | `custom-dialogue-map86-followups-01.jsonl` | Canmore? |
| `tgo:custom_dialogue:ebac62ebf98fc19dfac4` | `custom_dialogue` | `custom-dialogue-map126-followups-01.jsonl` | Canmore? |
| `tgo:custom_dialogue:bc7555b48bfffd734c58` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Canmore? Rinaldi? |
| `tgo:custom_dialogue:967d1fd1cdb14ac58144` | `custom_dialogue` | `custom-dialogue-map78-channel4-kimura-followups-01.jsonl` | Canmore… |
| `tgo:custom_dialogue:0b039d5bad3752d6f193` | `custom_dialogue` | `custom-dialogue-common-event-380-01.jsonl` | Carol! |
| `tgo:custom_dialogue:44b846807951c87fac53` | `custom_dialogue` | `custom-dialogue-map48-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:5252f46af747d2782183` | `custom_dialogue` | `custom-dialogue-common-event-380-01.jsonl` | Carol! |
| `tgo:custom_dialogue:526cb9ab76c43d4992db` | `custom_dialogue` | `custom-dialogue-map101-heather-sleepover-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:7048b1da372ca71c1c2c` | `custom_dialogue` | `custom-dialogue-common-event-436-01.jsonl` | Carol! |
| `tgo:custom_dialogue:8610e377d8903ed2fe1d` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:9f773caa43a9efe83369` | `custom_dialogue` | `custom-dialogue-common-event-392-01.jsonl` | Carol! |
| `tgo:custom_dialogue:a1c2a1c282246deb317a` | `custom_dialogue` | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl` | Carol! |
| `tgo:custom_dialogue:a514c0ba4a58e2e94fac` | `custom_dialogue` | `custom-dialogue-common-event-362-01.jsonl` | Carol! |
| `tgo:custom_dialogue:ab6324ccae05a3b33e07` | `custom_dialogue` | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl` | Carol! |
| `tgo:custom_dialogue:b2925d9829adbcc3cfaa` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:bfd586db7dbb12979ddc` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Carol! |
| `tgo:custom_dialogue:d22d98e449d4d3b9f095` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:d4ac13a66ae67cbc0370` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Carol! |
| `tgo:custom_dialogue:e52c4c332c1e4da8e2ef` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:ee841dcdfa22cc39a8ca` | `custom_dialogue` | `custom-dialogue-common-event-436-01.jsonl` | Carol! |
| `tgo:custom_dialogue:eee2a3e495f3e690a61e` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Carol! |
| `tgo:custom_dialogue:f7898446daf1d926956d` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:fcdb69a702dd8450d3ec` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Carol! |
| `tgo:custom_dialogue:1040c41da29ec75d6a29` | `custom_dialogue` | `custom-dialogue-common-event-442-01.jsonl` | Carol! Heather!... |
| `tgo:custom_dialogue:385734d7deb0923232a5` | `custom_dialogue` | `custom-dialogue-common-event-380-01.jsonl` | Carol!... |
| `tgo:custom_dialogue:0301c53c553d9a146492` | `custom_dialogue` | `custom-dialogue-common-event-327-01.jsonl` | Carol!? |
| `tgo:custom_dialogue:7cbef62bea8df7f55ecc` | `custom_dialogue` | `custom-dialogue-map63-followups-01.jsonl` | Carol!? |
| `tgo:custom_dialogue:82b49400799c224f4672` | `custom_dialogue` | `custom-dialogue-map102-followups-01.jsonl` | Carol!? |
| `tgo:custom_dialogue:c86df0cf677cf3ca962a` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Carol!? |
| `tgo:custom_dialogue:2652eaa80818890c2b7f` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Carol? |
| `tgo:custom_dialogue:456a431f96671c6759f0` | `custom_dialogue` | `custom-dialogue-common-event-331-01.jsonl` | Carol? |
| `tgo:custom_dialogue:b8c1e363d7d500a9aa39` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Carol? |
| `tgo:custom_dialogue:cc1f660ea79091a5aed9` | `custom_dialogue` | `custom-dialogue-map9-event-114-01.jsonl` | Carol? |
| `tgo:custom_dialogue:ff5cf86bda4d45e95aab` | `custom_dialogue` | `custom-dialogue-common-event-392-01.jsonl` | Carol? |
| `tgo:custom_dialogue:e48b6111d7ddb81f5e1e` | `custom_dialogue` | `custom-dialogue-common-event-346-01.jsonl` | Carol?! |
| `tgo:custom_dialogue:093bc9b649d0e7b2a31e` | `custom_dialogue` | `custom-dialogue-map23-followups-02.jsonl` | Carol… |
| `tgo:custom_dialogue:504da5661403aad1d795` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Carol… |
| `tgo:custom_dialogue:7b613d3248b957783076` | `custom_dialogue` | `custom-dialogue-common-event-380-01.jsonl` | Carol… |
| `tgo:custom_dialogue:abead9d24ff64191f245` | `custom_dialogue` | `custom-dialogue-map47-followups-01.jsonl` | Carol… |
| `tgo:custom_dialogue:dc954868f41ed5a0d78a` | `custom_dialogue` | `custom-dialogue-common-event-346-01.jsonl` | Carol… |
| `tgo:custom_dialogue:743015584a278388f0b6` | `custom_dialogue` | `custom-dialogue-map24-followups-01.jsonl` | Channel 4. |
| `tgo:custom_dialogue:99f8a61503b2506918e8` | `custom_dialogue` | `custom-dialogue-map70-followups-01.jsonl` | Charles Wilkes. |
| `tgo:custom_dialogue:7183f4b4df2889f0c455` | `custom_dialogue` | `custom-dialogue-map24-followups-05.jsonl` | Chloe! |
| `tgo:custom_dialogue:b1336bcd0e59c2e37e3d` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Chloe! |
| `tgo:custom_dialogue:d31fbbb47b43358cfa76` | `custom_dialogue` | `custom-dialogue-scene-ella-judy-pool-01.jsonl` | Chloe! |
| `tgo:custom_dialogue:2e13cd3285cc2ff2519a` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | Chloe!? |
| `tgo:custom_dialogue:37b4b41aecfdbb3cd0f6` | `custom_dialogue` | `custom-dialogue-map96-followups-01.jsonl` | Chloe!? |
| `tgo:custom_dialogue:83ea5c2df25293e5d08f` | `custom_dialogue` | `custom-dialogue-map134-followups-01.jsonl` | Chloe!? 1Hero!? |
| `tgo:custom_dialogue:21e9afcdcad9f4682cce` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Chloe!? Larry!? |
| `tgo:custom_dialogue:010e86e8c0127cfb3f7e` | `custom_dialogue` | `custom-dialogue-map21-chapel-followups-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:8299f9222e945ad678b2` | `custom_dialogue` | `custom-dialogue-common-event-342-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:d5fce96c1f467061ddff` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:d62b9669788c50f5c169` | `custom_dialogue` | `custom-dialogue-common-event-399-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:d74234ee931f9ead6503` | `custom_dialogue` | `custom-dialogue-common-event-412-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:fd192111348a22623b2c` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | Chloe? |
| `tgo:custom_dialogue:6f2c85e0b0bf59ba0bae` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | Chloe… |
| `tgo:custom_dialogue:ea3a130ec7c0aaa143e2` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Daemalius! |
| `tgo:custom_dialogue:0ffd98105466acd4588b` | `custom_dialogue` | `custom-dialogue-map3-event-39-01.jsonl` | Damalius… |
| `tgo:custom_dialogue:7d86ea0c307d2568978b` | `custom_dialogue` | `custom-dialogue-map15-warehouse-followups-01.jsonl` | David? |
| `tgo:custom_dialogue:9d0b9d2f6c3c4cef6a84` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Diana! |
| `tgo:custom_dialogue:9a259a36f30a5ac6fc06` | `custom_dialogue` | `custom-dialogue-map114-followups-01.jsonl` | Diana!? |
| `tgo:custom_dialogue:976984114441f1c9acf6` | `custom_dialogue` | `custom-dialogue-map99-followups-01.jsonl` | Diana? |
| `tgo:custom_dialogue:dd1913429a460eb5a51d` | `custom_dialogue` | `custom-dialogue-map70-followups-01.jsonl` | Diana? |
| `tgo:custom_dialogue:82ed2407fd0bb8183c29` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | Diana? Henry? |
| `tgo:custom_dialogue:2fa35322cbcad3cd3224` | `custom_dialogue` | `custom-dialogue-map19-followups-01.jsonl` | Duncan Helmer? |
| `tgo:custom_dialogue:0881c711cc41191a543d` | `custom_dialogue` | `custom-dialogue-map202-followups-01.jsonl` | Duncan! |
| `tgo:custom_dialogue:ba8d1702f13df7a65671` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Duncan! |
| `tgo:custom_dialogue:0b46c34ba008a56b3440` | `custom_dialogue` | `custom-dialogue-map77-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:0e683a3390a88e57fa51` | `custom_dialogue` | `custom-dialogue-map202-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:1480455140ae2951f7b9` | `custom_dialogue` | `custom-dialogue-common-event-446-01.jsonl` | Ella! |
| `tgo:custom_dialogue:158141565c837b071359` | `custom_dialogue` | `custom-dialogue-map132-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:2205ad27f2c58f9dca0f` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Ella! |
| `tgo:custom_dialogue:2a5b5e1deb6e2c5afc91` | `custom_dialogue` | `custom-dialogue-map24-followups-02.jsonl` | Ella! |
| `tgo:custom_dialogue:2e4362e93b27df2d424f` | `custom_dialogue` | `custom-dialogue-map5-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:47a74bdcfb44b1a80492` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Ella! |
| `tgo:custom_dialogue:48f2bc35063586484afe` | `custom_dialogue` | `custom-dialogue-common-event-446-01.jsonl` | Ella! |
| `tgo:custom_dialogue:4fec248fe9f1b3e2f379` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Ella! |
| `tgo:custom_dialogue:57b9af158c94fd367b06` | `custom_dialogue` | `custom-dialogue-map51-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:b09fccff96db8c24ab36` | `custom_dialogue` | `custom-dialogue-scene-chloe-ella-drinks-01.jsonl` | Ella! |
| `tgo:custom_dialogue:baf4fe5fe25c037b0a9e` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:d3c88e5ac67b8d50aaad` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Ella! |
| `tgo:custom_dialogue:e0400b55b32ca62fc37e` | `custom_dialogue` | `custom-dialogue-map116-event-4-01.jsonl` | Ella! |
| `tgo:custom_dialogue:e4a09342253825a596e6` | `custom_dialogue` | `custom-dialogue-common-event-344-01.jsonl` | Ella! |
| `tgo:custom_dialogue:ecb3ddbdf2a57513cc88` | `custom_dialogue` | `custom-dialogue-map4-apartments-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:f96889784332ceb5814a` | `custom_dialogue` | `custom-dialogue-map11-gym-followups-01.jsonl` | Ella! |
| `tgo:custom_dialogue:37f8f5532236d240eee5` | `custom_dialogue` | `custom-dialogue-map172-followups-01.jsonl` | Ella!? |
| `tgo:custom_dialogue:517d618a8639c3c5b9a3` | `custom_dialogue` | `custom-dialogue-map45-followups-01.jsonl` | Ella!? |
| `tgo:custom_dialogue:8ca893dd4e9e544c654f` | `custom_dialogue` | `custom-dialogue-map107-followups-01.jsonl` | Ella!? |
| `tgo:custom_dialogue:a289f8c9af8567779552` | `custom_dialogue` | `custom-dialogue-map159-followups-01.jsonl` | Ella!? |
| `tgo:custom_dialogue:e39623cdd5fdba3b03a9` | `custom_dialogue` | `custom-dialogue-map200-followups-01.jsonl` | Ella!? |
| `tgo:custom_dialogue:1e9953a7a4848b236d1a` | `custom_dialogue` | `custom-dialogue-map201-finale-followups-01.jsonl` | Ella? |
| `tgo:custom_dialogue:5486ea09f3525d0c02a0` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | Ella? |
| `tgo:custom_dialogue:71c4e98514dad495635d` | `custom_dialogue` | `custom-dialogue-map4-apartments-followups-01.jsonl` | Ella? |
| `tgo:custom_dialogue:75061c5a6b9972547895` | `custom_dialogue` | `custom-dialogue-scene-hannah-ella-carol-01.jsonl` | Ella? |
| `tgo:custom_dialogue:974f3155d5c0dd630a18` | `custom_dialogue` | `custom-dialogue-common-event-325-01.jsonl` | Ella? |
| `tgo:custom_dialogue:2b2e34a299c0bbdac942` | `custom_dialogue` | `custom-dialogue-map51-followups-01.jsonl` | Ella… |
| `tgo:custom_dialogue:44079bfda050f7a81b03` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Ella… |
| `tgo:custom_dialogue:aadeedeefeaf25d793a0` | `custom_dialogue` | `custom-dialogue-map6-church-followups-02.jsonl` | Ella…? |
| `tgo:custom_dialogue:c909b6ce9ca2c303470e` | `custom_dialogue` | `custom-dialogue-map32-station-followups-01.jsonl` | Erica Abraham? |
| `tgo:custom_dialogue:7ac7c414b6cc24b3a42a` | `custom_dialogue` | `custom-dialogue-scene-hannah-erica-contest-01.jsonl` | Erica! |
| `tgo:custom_dialogue:7c63fff85736d9ed79d4` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | Erica! |
| `tgo:custom_dialogue:f40cea1b2bd2c375730f` | `custom_dialogue` | `custom-dialogue-common-event-375-01.jsonl` | Erica! |
| `tgo:custom_dialogue:03dee726428c682397e6` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | Erica!? |
| `tgo:custom_dialogue:352cab96b4ed8f8224a4` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | Erica!? |
| `tgo:custom_dialogue:6ed8c4bf3b9f87b2ff3c` | `custom_dialogue` | `custom-dialogue-map19-followups-01.jsonl` | Erica!? |
| `tgo:custom_dialogue:f1fc59b61b26974266c9` | `custom_dialogue` | `custom-dialogue-map3-event-31-01.jsonl` | Erica!? |
| `tgo:custom_dialogue:0083a643c0b64aee1acf` | `custom_dialogue` | `custom-dialogue-map183-followups-01.jsonl` | Erica? |
| `tgo:custom_dialogue:178195f323d1c134c578` | `custom_dialogue` | `custom-dialogue-common-event-316-02.jsonl` | Erica? |
| `tgo:custom_dialogue:48059e2c3ecd2e3cd41f` | `custom_dialogue` | `custom-dialogue-map55-followups-02.jsonl` | Erica? |
| `tgo:custom_dialogue:bd20b1956641fdc270cf` | `custom_dialogue` | `custom-dialogue-common-event-456-02.jsonl` | Erica? |
| `tgo:custom_dialogue:cb30f76ffa916268e896` | `custom_dialogue` | `custom-dialogue-map17-followups-01.jsonl` | Erica? |
| `tgo:custom_dialogue:d1615f5d50c38de5f482` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Erica? |
| `tgo:custom_dialogue:fbdc9bf5071d2696befb` | `custom_dialogue` | `custom-dialogue-map114-followups-01.jsonl` | Erica? |
| `tgo:custom_dialogue:d1262db2a580bba7c176` | `custom_dialogue` | `custom-dialogue-scene-erica-sex-01.jsonl` | Erica?... |
| `tgo:custom_dialogue:1e2626c28bbdc25f7fea` | `custom_dialogue` | `custom-dialogue-map94-church-followups-01.jsonl` | Erica… |
| `tgo:custom_dialogue:9285d9bc20172f9515e6` | `custom_dialogue` | `custom-dialogue-map52-ella-chloe-followups-01.jsonl` | Erica…  |
| `tgo:custom_dialogue:95ef10bbcaed7495a8fa` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | Evie! |
| `tgo:custom_dialogue:cb00b3e0c86e1a2af819` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | Evie! |
| `tgo:custom_dialogue:c4ab40f21642638a4b8c` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Fluffy! |
| `tgo:custom_dialogue:0559134be233f31e5c39` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Fluffy? |
| `tgo:custom_dialogue:fe64d8b5ab078fcb94c1` | `custom_dialogue` | `custom-dialogue-common-event-346-01.jsonl` | Ha! Ha! Ha! Ha! |
| `tgo:custom_dialogue:81de50fc48adb522b3d3` | `custom_dialogue` | `custom-dialogue-map30-dicks-restaurant-followups-01.jsonl` | Haha |
| `tgo:custom_dialogue:daf0888baba6d61054f2` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Haha! |
| `tgo:custom_dialogue:079390dbac672137388b` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Haha. |
| `tgo:custom_dialogue:1d668985473720bab9a0` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Haha. |
| `tgo:custom_dialogue:8859e8d07d94d5e53f5d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Haha. |
| `tgo:custom_dialogue:e179ea9c1661811750e1` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Haha. |
| `tgo:custom_dialogue:0499bea8456cbee1334a` | `custom_dialogue` | `custom-dialogue-map31-event-15-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:21c3ffeea8a4d7e89ec2` | `custom_dialogue` | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:26cdbf7bfb3a0e0717c6` | `custom_dialogue` | `custom-dialogue-map53-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:3459b55c9d065346ad40` | `custom_dialogue` | `custom-dialogue-map31-alia-treasure-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:4828c638fb74c1f72d7e` | `custom_dialogue` | `custom-dialogue-map23-followups-04.jsonl` | Hahaha! |
| `tgo:custom_dialogue:4f0ad247d6de61b7dceb` | `custom_dialogue` | `custom-dialogue-map202-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:520a22b1c732caff6c5e` | `custom_dialogue` | `custom-dialogue-map31-event-15-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:5ce93f9d8c4a592fc299` | `custom_dialogue` | `custom-dialogue-map27-housewarming-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:64eba278e14f27055690` | `custom_dialogue` | `custom-dialogue-map59-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:8bfdffd1e655e01eea7e` | `custom_dialogue` | `custom-dialogue-map276-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:8f47c78f5bf36e292313` | `custom_dialogue` | `custom-dialogue-map101-heather-sleepover-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:bdc480ee5c50360b2b36` | `custom_dialogue` | `custom-dialogue-map101-heather-sleepover-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:c86d836eb10eafc6bc76` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:ce7ff794ecdd942d68c7` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Hahaha! |
| `tgo:custom_dialogue:ceabd7a3a58c80b78557` | `custom_dialogue` | `custom-dialogue-map206-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:d9b9f05119c95022bf69` | `custom_dialogue` | `custom-dialogue-map32-station-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:e0007f0f66d81d03ea67` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Hahaha! |
| `tgo:custom_dialogue:ad473c5c4fc4dd8fcf9d` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | Hahaha!... |
| `tgo:custom_dialogue:144108790f52c76f5bac` | `custom_dialogue` | `custom-dialogue-map55-followups-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:32b0a8200d1409207bf2` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:38da316c46246f0878d1` | `custom_dialogue` | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:59077c9ec2bede23d78a` | `custom_dialogue` | `custom-dialogue-common-event-477-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:5b1ef69ef24aec87aaac` | `custom_dialogue` | `custom-dialogue-map31-alia-quest-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:7d8bd95cd1f51f5054c9` | `custom_dialogue` | `custom-dialogue-map48-followups-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:c4bcae64bd0965aba56d` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:d54a58c9674f61df50c4` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Hahaha. |
| `tgo:custom_dialogue:ed555f2978afff5ce405` | `custom_dialogue` | `custom-dialogue-map257-followups-01.jsonl` | Hahaha. |
| `tgo:custom_dialogue:1f181f5d35a52355576f` | `custom_dialogue` | `custom-dialogue-scene-hannah-erica-contest-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:2a19e0cd2d32bd5c9b96` | `custom_dialogue` | `custom-dialogue-map31-followups-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:3629be81ac971323a0e1` | `custom_dialogue` | `custom-dialogue-common-event-456-02.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:9b6d42fee7dd1f428165` | `custom_dialogue` | `custom-dialogue-scene-hannah-erica-contest-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:a20ec516ace00ff21ef8` | `custom_dialogue` | `custom-dialogue-common-event-378-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:a40f52f7d2c687f19fa1` | `custom_dialogue` | `custom-dialogue-map47-followups-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:b4a31ae3bbcac6c8ec35` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:c5be49a60b6d70707cbd` | `custom_dialogue` | `custom-dialogue-map48-followups-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:f12d702f01cb223595eb` | `custom_dialogue` | `custom-dialogue-common-event-378-01.jsonl` | Hahahaha! |
| `tgo:custom_dialogue:06cdeae0a60e08ce7014` | `custom_dialogue` | `custom-dialogue-map48-followups-01.jsonl` | Hahahaha. |
| `tgo:custom_dialogue:de541ccfd48df7468948` | `custom_dialogue` | `custom-dialogue-map52-ella-chloe-followups-01.jsonl` | Hahahaha. |
| `tgo:custom_dialogue:7abf023cd8891848af09` | `custom_dialogue` | `custom-dialogue-common-event-495-01.jsonl` | Hahahahaha! |
| `tgo:custom_dialogue:19d640edd0fb05642280` | `custom_dialogue` | `custom-dialogue-map149-followups-01.jsonl` | Hahahahahahahaha! |
| `tgo:custom_dialogue:e849f8107b31bec40f82` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | Hahahahahahahahahaha! |
| `tgo:custom_dialogue:7875a20056a06503ce45` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | Hannah Ray! |
| `tgo:custom_dialogue:80906d980bd9464808d8` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | Hannah Ray! |
| `tgo:custom_dialogue:006ea6bb717867b71c1a` | `custom_dialogue` | `custom-dialogue-common-event-391-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:024590041ddc728d18f8` | `custom_dialogue` | `custom-dialogue-common-event-326-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:08e2cfd700ddd64d3b88` | `custom_dialogue` | `custom-dialogue-common-event-430-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:165ecbb728fbc9ff3b56` | `custom_dialogue` | `custom-dialogue-common-event-342-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:2850fa464709bc5a9de2` | `custom_dialogue` | `custom-dialogue-common-event-358-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:2b61e0dcbbdcb34e7018` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Hannah! |
| `tgo:custom_dialogue:2f9edfd6f0f5032bf2e7` | `custom_dialogue` | `custom-dialogue-common-event-304-02.jsonl` | Hannah! |
| `tgo:custom_dialogue:3c5024ecf51a419ff408` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Hannah! |
| `tgo:custom_dialogue:3cbc5943f58deedb2995` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Hannah! |
| `tgo:custom_dialogue:3dc15aa2d32ce65bdd3f` | `custom_dialogue` | `custom-dialogue-map153-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:3e82ef4af2f9e34d7270` | `custom_dialogue` | `custom-dialogue-map105-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:462e010ae6b4f45e2d80` | `custom_dialogue` | `custom-dialogue-map201-finale-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:4e54c16db388bd3ee72b` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:5cba84506d72e5d0c9ab` | `custom_dialogue` | `custom-dialogue-map116-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:6830a086dde1ac5d7277` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:888bcd0d73f25aec4a3d` | `custom_dialogue` | `custom-dialogue-common-event-375-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:89ac3b2a672030c9d131` | `custom_dialogue` | `custom-dialogue-map41-followups-02.jsonl` | Hannah! |
| `tgo:custom_dialogue:8ac53a9aa4f6e7e21535` | `custom_dialogue` | `custom-dialogue-map24-followups-02.jsonl` | Hannah! |
| `tgo:custom_dialogue:908fac5dc12b378c0844` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:9605ca1e6968fb7643fa` | `custom_dialogue` | `custom-dialogue-common-event-455-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:9773de8e072a4c72e473` | `custom_dialogue` | `custom-dialogue-map121-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:9b4ffb92a98c1b53c77e` | `custom_dialogue` | `custom-dialogue-common-event-358-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:9f6721141ffa27c25994` | `custom_dialogue` | `custom-dialogue-map6-church-followups-02.jsonl` | Hannah! |
| `tgo:custom_dialogue:a0e001bcef853f88bd90` | `custom_dialogue` | `custom-dialogue-common-event-430-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:a296050688cca6cc1638` | `custom_dialogue` | `custom-dialogue-common-event-342-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:a76efaea55fc72e2ffd0` | `custom_dialogue` | `custom-dialogue-map203-courtroom-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:b68921ff9b256034178d` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:b856e1bd3fdf31963b14` | `custom_dialogue` | `custom-dialogue-map9-event-124-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:bbc383e351bdf910644a` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:c3fbfa4b41c9fd3465fb` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:c8f67f54562b8ab1caa0` | `custom_dialogue` | `custom-dialogue-map25-dinner-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:ccd3c126bdfc8e353245` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:d0b881ae942ea6238a86` | `custom_dialogue` | `custom-dialogue-map23-followups-04.jsonl` | Hannah! |
| `tgo:custom_dialogue:e36c23d9daa388b8c23f` | `custom_dialogue` | `custom-dialogue-map13-strip-center-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:e7257597d838ce550e05` | `custom_dialogue` | `custom-dialogue-map201-finale-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:e9cd19fac6a7228c0e24` | `custom_dialogue` | `custom-dialogue-common-event-358-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:ea2db01fd26a7a3f8067` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:ea7d5531e55ba12e717b` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:fea4843879dca9a340e3` | `custom_dialogue` | `custom-dialogue-map16-heather-home-followups-01.jsonl` | Hannah! |
| `tgo:custom_dialogue:777e04a085e65972d23f` | `custom_dialogue` | `custom-dialogue-common-event-435-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:83d37e8dcd12477db44c` | `custom_dialogue` | `custom-dialogue-common-event-315-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:92de50198cb260eaa396` | `custom_dialogue` | `custom-dialogue-common-event-411-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:dc4ddd897b447951421c` | `custom_dialogue` | `custom-dialogue-map107-followups-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:ddd841895378d099fe3d` | `custom_dialogue` | `custom-dialogue-map153-followups-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:e9fa7f1f9513589c129e` | `custom_dialogue` | `custom-dialogue-map140-followups-01.jsonl` | Hannah!? |
| `tgo:custom_dialogue:3d96bcdedb50b1451813` | `custom_dialogue` | `custom-dialogue-map23-followups-02.jsonl` | Hannah. |
| `tgo:custom_dialogue:1aee6991da39fc1a75b4` | `custom_dialogue` | `custom-dialogue-common-event-315-01.jsonl` | Hannah? |
| `tgo:custom_dialogue:57fa30fbc77a5d1acc81` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Hannah? |
| `tgo:custom_dialogue:60ac8efec6a638dc85b7` | `custom_dialogue` | `custom-dialogue-common-event-392-01.jsonl` | Hannah? |
| `tgo:custom_dialogue:94d891a4d6ee248ec5dc` | `custom_dialogue` | `custom-dialogue-map23-event-44-01.jsonl` | Hannah? |
| `tgo:custom_dialogue:e74df6c92d1ed2e3943f` | `custom_dialogue` | `custom-dialogue-map12-arianna-followups-01.jsonl` | Hannah? |
| `tgo:custom_dialogue:cdf1e55066ada6c60e3a` | `custom_dialogue` | `custom-dialogue-map41-followups-02.jsonl` | Hannah?... Alia?... |
| `tgo:custom_dialogue:3217b1cfce0838243a34` | `custom_dialogue` | `custom-dialogue-common-event-455-01.jsonl` | Hannah… |
| `tgo:custom_dialogue:33e6bf875a203a7ea5ea` | `custom_dialogue` | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl` | Hannah… |
| `tgo:custom_dialogue:17ac348341e93563eeba` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | Harem? |
| `tgo:custom_dialogue:3d3481005ff0f9a29677` | `custom_dialogue` | `custom-dialogue-common-event-380-01.jsonl` | Heather! |
| `tgo:custom_dialogue:414176c9c24e61021f40` | `custom_dialogue` | `custom-dialogue-common-event-456-02.jsonl` | Heather! |
| `tgo:custom_dialogue:4c5fc8d7a907dfd97125` | `custom_dialogue` | `custom-dialogue-map31-event-15-01.jsonl` | Heather! |
| `tgo:custom_dialogue:d380df3b4b145f239a2a` | `custom_dialogue` | `custom-dialogue-map24-followups-03.jsonl` | Heather! |
| `tgo:custom_dialogue:f97031a8ccbedcdbe0cf` | `custom_dialogue` | `custom-dialogue-common-event-341-01.jsonl` | Heather! |
| `tgo:custom_dialogue:471a95f184a1c8a15776` | `custom_dialogue` | `custom-dialogue-common-event-373-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:4f79f99d5d40a57e133d` | `custom_dialogue` | `custom-dialogue-common-event-314-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:571eb43e14b536453623` | `custom_dialogue` | `custom-dialogue-common-event-327-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:6e9eb9ad105b4609d304` | `custom_dialogue` | `custom-dialogue-common-event-362-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:7d7ded0103901c4025e9` | `custom_dialogue` | `custom-dialogue-map54-backyard-followups-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:c26fe3e6e27699a2e6c0` | `custom_dialogue` | `custom-dialogue-common-event-341-01.jsonl` | Heather!? |
| `tgo:custom_dialogue:007dad2a7ecb6a7f922d` | `custom_dialogue` | `custom-dialogue-map18-followups-01.jsonl` | Heather? |
| `tgo:custom_dialogue:30f5e106d72659a222b6` | `custom_dialogue` | `custom-dialogue-common-event-430-01.jsonl` | Heather? |
| `tgo:custom_dialogue:68875fa5b6ad5ead65f9` | `custom_dialogue` | `custom-dialogue-common-event-357-01.jsonl` | Heather? |
| `tgo:custom_dialogue:91b38d620f6a3d47285d` | `custom_dialogue` | `custom-dialogue-map132-followups-01.jsonl` | Heather? |
| `tgo:custom_dialogue:a1c62eb540b74bc72f62` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | Heather? |
| `tgo:custom_dialogue:4539435f2826f74b7d7c` | `custom_dialogue` | `custom-dialogue-map73-followups-01.jsonl` | Heather… |
| `tgo:custom_dialogue:ef3dfff3d6d785b0871c` | `custom_dialogue` | `custom-dialogue-map24-followups-03.jsonl` | Heather… |
| `tgo:custom_dialogue:4459e44182b91762c5b3` | `custom_dialogue` | `custom-dialogue-map7-followups-01.jsonl` | Heh. |
| `tgo:custom_dialogue:ed48fb5bf51cf6d2a587` | `custom_dialogue` | `custom-dialogue-common-event-443-01.jsonl` | Heh… |
| `tgo:custom_dialogue:de029cf453605785c20b` | `custom_dialogue` | `custom-dialogue-map205-followups-01.jsonl` | Henry? |
| `tgo:custom_dialogue:05a449709d57abf267f2` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:168a077501d93450f57a` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:6153ba0fb10987f6ea25` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:db950e09616d1fbbd79d` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:e6281d7252d61ff11ac9` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:fd02f6e0567198bda716` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm. |
| `tgo:custom_dialogue:1cd6e5c36d98a32efbd1` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm… |
| `tgo:custom_dialogue:71739cbcfb8bcaeb06ba` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm… |
| `tgo:custom_dialogue:a5ce764b551ed0566a8e` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm… |
| `tgo:custom_dialogue:bb188b4aa1f283e89898` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm… |
| `tgo:custom_dialogue:cd15200d41c642f8d0b2` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmm… |
| `tgo:custom_dialogue:ef264b8df33c45035606` | `custom_dialogue` | `custom-dialogue-map114-followups-01.jsonl` | Hmm… Lorenzo D. Scott. |
| `tgo:custom_dialogue:2c89d476ad615761f9ed` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmph. |
| `tgo:custom_dialogue:3ed9380b384765ad3cdb` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmph. |
| `tgo:custom_dialogue:4aa3ae39a2683232b469` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmph. |
| `tgo:custom_dialogue:e5c77d64040a41807b48` | `custom_dialogue` | `custom-dialogue-repeated-01.jsonl` | Hmph. |
| `tgo:custom_dialogue:e694a0525d550d111c9e` | `custom_dialogue` | `custom-dialogue-map18-followups-01.jsonl` | Jon!? |
| `tgo:custom_dialogue:417917d4bd28fa12717e` | `custom_dialogue` | `custom-dialogue-common-event-418-01.jsonl` | Judy! |
| `tgo:custom_dialogue:6d8ccdd69da01cd8046c` | `custom_dialogue` | `custom-dialogue-common-event-483-01.jsonl` | Judy! |
| `tgo:custom_dialogue:9c3e4e53e04c94e8596d` | `custom_dialogue` | `custom-dialogue-map55-followups-01.jsonl` | Judy! |
| `tgo:custom_dialogue:d4715bc3b293c22442e3` | `custom_dialogue` | `custom-dialogue-map49-church-attic-followups-01.jsonl` | Judy! |
| `tgo:custom_dialogue:ecb1ab1c8dfff57d6132` | `custom_dialogue` | `custom-dialogue-map41-followups-01.jsonl` | Judy! |
| `tgo:custom_dialogue:1f458af393bb3b3a90af` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-02.jsonl` | Judy!? |
| `tgo:custom_dialogue:ea659988fa0a63e3829a` | `custom_dialogue` | `custom-dialogue-map23-followups-01.jsonl` | Judy!? |
| `tgo:custom_dialogue:17c293e27337110e87ef` | `custom_dialogue` | `custom-dialogue-scene-chloe-judy-masturbation-01.jsonl` | Judy? |
| `tgo:custom_dialogue:55fb59c461690a79a500` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | Judy? |
| `tgo:custom_dialogue:a429bba0216868e5790b` | `custom_dialogue` | `custom-dialogue-common-event-433-01.jsonl` | Judy? |
| `tgo:custom_dialogue:dda5309488f8922b4fad` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Judy? |
| `tgo:custom_dialogue:e6febf08facb4f93f6a8` | `custom_dialogue` | `custom-dialogue-common-event-395-01.jsonl` | Judy? |
| `tgo:custom_dialogue:4444b2f3d063957a4d7f` | `custom_dialogue` | `custom-dialogue-map21-chapel-followups-01.jsonl` | Judy… |
| `tgo:custom_dialogue:7c068f56735c2ea1137e` | `custom_dialogue` | `custom-dialogue-common-event-257-01.jsonl` | Ketchup. |
| `tgo:custom_dialogue:1715b62f8b4e4210857b` | `custom_dialogue` | `custom-dialogue-map116-event-89-01.jsonl` | Kimberly! |
| `tgo:custom_dialogue:1ac2ae4be8447a0ea53f` | `custom_dialogue` | `custom-dialogue-map116-followups-03.jsonl` | Kimberly! |
| `tgo:custom_dialogue:4f291071eee6a1dfc374` | `custom_dialogue` | `custom-dialogue-common-event-376-01.jsonl` | Kimberly! |
| `tgo:custom_dialogue:64ae8f5f2bc8e251b1dd` | `custom_dialogue` | `custom-dialogue-map157-hell-followups-01.jsonl` | Kimberly! |
| `tgo:custom_dialogue:30a8655c10b7ebd9a12b` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-01.jsonl` | Kimberly!? |
| `tgo:custom_dialogue:ad8f0872fa29216f30bc` | `custom_dialogue` | `custom-dialogue-map98-followups-01.jsonl` | Kimberly!? |
| `tgo:custom_dialogue:8d8d4a2a914a5fcd39ca` | `custom_dialogue` | `custom-dialogue-map61-gym-followups-01.jsonl` | Kimberly?! |
| `tgo:custom_dialogue:40b7e8511e1535c9d29d` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Kirk!? |
| `tgo:custom_dialogue:d0902dcefd9563ef3e91` | `custom_dialogue` | `custom-dialogue-map158-followups-01.jsonl` | Kirk? |
| `tgo:custom_dialogue:0c6c8252523258a9cb1f` | `custom_dialogue` | `custom-dialogue-map183-followups-01.jsonl` | Lilith! |
| `tgo:custom_dialogue:4b4aa2e080a6da13d267` | `custom_dialogue` | `custom-dialogue-common-event-440-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:58e976a473c0f09ac516` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Lillian! |
| `tgo:custom_dialogue:742c4feecab4f6550824` | `custom_dialogue` | `custom-dialogue-map116-event-4-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:9e6d58082f3e506c7a9e` | `custom_dialogue` | `custom-dialogue-common-event-316-02.jsonl` | Lillian! |
| `tgo:custom_dialogue:a19e7b4ec92042c7cbea` | `custom_dialogue` | `custom-dialogue-map108-followups-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:a3d1f762174695229288` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:a5cc6dda2ba1bc99fcb9` | `custom_dialogue` | `custom-dialogue-map200-followups-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:cc2690d2de604ab06c33` | `custom_dialogue` | `custom-dialogue-common-event-403-01.jsonl` | Lillian! |
| `tgo:custom_dialogue:d9689779b07a84075614` | `custom_dialogue` | `custom-dialogue-scene-kimberly-lillian-chapel-01.jsonl` | Lillian!? Kimberly!? |
| `tgo:custom_dialogue:d497c56d67a2aaeafe78` | `custom_dialogue` | `custom-dialogue-map128-followups-01.jsonl` | Lillian. |
| `tgo:custom_dialogue:09f3527de8e578c46019` | `custom_dialogue` | `custom-dialogue-common-event-story-followups-04.jsonl` | Lillian? |
| `tgo:custom_dialogue:2ead27c6e6236c3ccbab` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Lillian? |
| `tgo:custom_dialogue:6c7b7a5a311c00157706` | `custom_dialogue` | `custom-dialogue-common-event-388-01.jsonl` | Lillian? |
| `tgo:custom_dialogue:999f3f93ff4683ffe75d` | `custom_dialogue` | `custom-dialogue-map151-hell-followups-02.jsonl` | Lillian? |
| `tgo:custom_dialogue:a248e4dfa882f1832772` | `custom_dialogue` | `custom-dialogue-common-event-443-01.jsonl` | Lillian? |
| `tgo:custom_dialogue:bd14576607dc185b5bd9` | `custom_dialogue` | `custom-dialogue-common-event-374-01.jsonl` | Lillian? |
| `tgo:custom_dialogue:022afeefb2dcc1c17ec4` | `custom_dialogue` | `custom-dialogue-map201-finale-followups-01.jsonl` | Lillian… |
| `tgo:custom_dialogue:18cec6d601c0f01f5fa5` | `custom_dialogue` | `custom-dialogue-map11-gym-followups-01.jsonl` | Lustagram? |
| `tgo:custom_dialogue:37ac7b6ea03c6b2f455d` | `custom_dialogue` | `custom-dialogue-map149-followups-01.jsonl` | Madalyn! |
| `tgo:custom_dialogue:3a3a641df2098d02c0c0` | `custom_dialogue` | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | Madalyn! |
| `tgo:custom_dialogue:4ae87cfc2a13af99af48` | `custom_dialogue` | `custom-dialogue-common-event-431-01.jsonl` | Madalyn! |
| `tgo:custom_dialogue:92a261998d840ff820ea` | `custom_dialogue` | `custom-dialogue-map20-church-event-58-01.jsonl` | Madalyn! |
| `tgo:custom_dialogue:50cc0fe05dc924e3bb10` | `custom_dialogue` | `custom-dialogue-scene-dinner-01.jsonl` | Madalyn? |
| `tgo:custom_dialogue:65862f3c4477ee8475d4` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | Madalyn? |
| `tgo:custom_dialogue:591b766316d01bbfab45` | `custom_dialogue` | `custom-dialogue-common-event-305-01.jsonl` | Madalyn?... |
| `tgo:custom_dialogue:6f8fb55a55b467235a3b` | `custom_dialogue` | `custom-dialogue-common-event-409-01.jsonl` | Melissa! |
| `tgo:custom_dialogue:fe6bf2a22ae40a3f8696` | `custom_dialogue` | `custom-dialogue-map19-followups-01.jsonl` | Melissa! |
| `tgo:custom_dialogue:5811c8e452c93d54bf8d` | `custom_dialogue` | `custom-dialogue-common-event-441-01.jsonl` | Melissa? |
| `tgo:custom_dialogue:707026ddc66f288692eb` | `custom_dialogue` | `custom-dialogue-common-event-356-01.jsonl` | Melissa? |
| `tgo:custom_dialogue:98b0d6c83d78cbbfde00` | `custom_dialogue` | `custom-dialogue-map78-channel4-kimura-followups-01.jsonl` | Melissa? |
| `tgo:custom_dialogue:b004d617d6ba7a23c32f` | `custom_dialogue` | `custom-dialogue-map15-warehouse-followups-01.jsonl` | Melissa? |
| `tgo:custom_dialogue:f839b06f1a201131c7f0` | `custom_dialogue` | `custom-dialogue-map20-church-event-58-01.jsonl` | Melissa? |
| `tgo:custom_dialogue:030ba790ddccf0fc16aa` | `custom_dialogue` | `custom-dialogue-common-event-477-01.jsonl` | Mmm! |
| `tgo:custom_dialogue:0330b8830fad6b7ca711` | `custom_dialogue` | `custom-dialogue-scene-orgy-01.jsonl` | Mmm! |
| `tgo:custom_dialogue:77659fa26183a5cf2b34` | `custom_dialogue` | `custom-dialogue-common-event-477-01.jsonl` | Mmm! |
| `tgo:custom_dialogue:6ce7883e549691d4d2b9` | `custom_dialogue` | `custom-dialogue-common-event-482-01.jsonl` | Mmm. |
| `tgo:custom_dialogue:8806f1ffd789a6f52fbe` | `custom_dialogue` | `custom-dialogue-common-event-477-01.jsonl` | Mmm. |
| `tgo:custom_dialogue:03727a3a1b6b0b6d464a` | `custom_dialogue` | `custom-dialogue-common-event-388-01.jsonl` | Mmmf! |
| `tgo:custom_dialogue:87b2cbde171d9cd7881a` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Mmmm! |
| `tgo:custom_dialogue:2a58f28643e2a61ee6f1` | `custom_dialogue` | `custom-dialogue-common-event-455-01.jsonl` | Mmmmm! |
| `tgo:custom_dialogue:7647695a312e6b8206b0` | `custom_dialogue` | `custom-dialogue-common-event-366-01.jsonl` | Mmmmm! |
| `tgo:custom_dialogue:b6c6cea9ec9888ea0481` | `custom_dialogue` | `custom-dialogue-common-event-366-01.jsonl` | Mmmmm! |
| `tgo:custom_dialogue:ce162b839ba8a3ea3591` | `custom_dialogue` | `custom-dialogue-common-event-346-01.jsonl` | Mmmmm. |
| `tgo:custom_dialogue:09920f27439eb04f72a1` | `custom_dialogue` | `custom-dialogue-common-event-398-01.jsonl` | Mmmm… |
| `tgo:custom_dialogue:9a0df33ff93a22851308` | `custom_dialogue` | `custom-dialogue-common-event-381-01.jsonl` | Mmmm… |
| `tgo:custom_dialogue:0dabd3339374d331f83e` | `custom_dialogue` | `custom-dialogue-common-event-366-01.jsonl` | Mmm… |
| `tgo:custom_dialogue:5534c4b8924b91aa2221` | `custom_dialogue` | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | Mmm… |
| `tgo:custom_dialogue:bcdccc8ec09fb95b4ad5` | `custom_dialogue` | `custom-dialogue-common-event-474-01.jsonl` | Mmm… |
| `tgo:custom_dialogue:70b50b76593eb1e21788` | `custom_dialogue` | `custom-dialogue-common-event-426-01.jsonl` | Mmph! |
| `tgo:custom_dialogue:bbd74e8a19545179053f` | `custom_dialogue` | `custom-dialogue-common-event-442-01.jsonl` | Mmph! |
| `tgo:custom_dialogue:cd763009c90c92624d22` | `custom_dialogue` | `custom-dialogue-common-event-409-01.jsonl` | Nellie Cole. |
| `tgo:custom_dialogue:14584f6487e2ab2ad67a` | `custom_dialogue` | `custom-dialogue-scene-andrea-nellie-tub-01.jsonl` | Nellie! |
| `tgo:custom_dialogue:408a3ce21e3dbf288ed9` | `custom_dialogue` | `custom-dialogue-map106-followups-01.jsonl` | Nellie! |
| `tgo:custom_dialogue:60d00a4be053d88e594d` | `custom_dialogue` | `custom-dialogue-common-event-438-01.jsonl` | Nellie! |
| `tgo:custom_dialogue:c5bad263952b6cc5f919` | `custom_dialogue` | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | Nellie! |
| `tgo:custom_dialogue:d1f44167b1fb1732b040` | `custom_dialogue` | `custom-dialogue-common-event-387-01.jsonl` | Nellie! |
| `tgo:custom_dialogue:eb9b3344d528f140f2a0` | `custom_dialogue` | `custom-dialogue-common-event-384-02.jsonl` | Nellie! |
| `tgo:custom_dialogue:0531aafbf28f935a41aa` | `custom_dialogue` | `custom-dialogue-map20-foyer-heather-arianna-01.jsonl` | Nellie!? |
| `tgo:custom_dialogue:3f7094b63ec37c696294` | `custom_dialogue` | `custom-dialogue-map31-event-15-01.jsonl` | Nellie!? |
| `tgo:custom_dialogue:6c647258981df1522b30` | `custom_dialogue` | `custom-dialogue-map53-followups-01.jsonl` | Nellie!? |
| `tgo:custom_dialogue:7229b7f9f19f2aa31386` | `custom_dialogue` | `custom-dialogue-map20-foyer-heather-arianna-01.jsonl` | Nellie!? |
| `tgo:custom_dialogue:8a26b229f65cf7fe15cd` | `custom_dialogue` | `custom-dialogue-map15-warehouse-followups-01.jsonl` | Nellie!? |
| `tgo:custom_dialogue:e0207d6fbc5e954415d4` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-02.jsonl` | Nellie!? |
| `tgo:custom_dialogue:e06a4f1b5b398102e630` | `custom_dialogue` | `custom-dialogue-map44-mansion-followups-02.jsonl` | Nellie!?... |
| `tgo:custom_dialogue:276082b98a5588b645bc` | `custom_dialogue` | `custom-dialogue-map31-diana-investigation-01.jsonl` | Nellie. |
| `tgo:custom_dialogue:6c5ceaf01028249a32f2` | `custom_dialogue` | `custom-dialogue-map108-followups-01.jsonl` | Nellie? |
| `tgo:custom_dialogue:ce135437b78e90d774ae` | `custom_dialogue` | `custom-dialogue-map202-followups-01.jsonl` | Nellie… |
| `tgo:custom_dialogue:8271c521183d29e9e745` | `custom_dialogue` | `custom-dialogue-scene-judy-masturbate-01.jsonl` | Ooooooo… |
| `tgo:custom_dialogue:118051bb9ca49614e6c0` | `custom_dialogue` | `custom-dialogue-map98-followups-01.jsonl` | Paul? |
| `tgo:custom_dialogue:20a29497f95a4f3be896` | `custom_dialogue` | `custom-dialogue-common-event-373-01.jsonl` | Psst! 1Hero! |
| `tgo:custom_dialogue:a2185cc9f75bb1246216` | `custom_dialogue` | `custom-dialogue-map98-followups-01.jsonl` | Psst! 1Hero! |
| `tgo:custom_dialogue:138d4ec821c31d33d43d` | `custom_dialogue` | `custom-dialogue-map141-warehouse-followups-01.jsonl` | Santiva! |
| `tgo:custom_dialogue:c7cf3f96b0ad0813a4ba` | `custom_dialogue` | `custom-dialogue-map82-channel4-followups-01.jsonl` | Simon! |
| `tgo:custom_dialogue:1af5ecc4c3477ec61bfa` | `custom_dialogue` | `custom-dialogue-map15-warehouse-followups-01.jsonl` | Tasha Cole. |
| `tgo:custom_dialogue:5c40016c2fdb34d7023c` | `custom_dialogue` | `custom-dialogue-map31-tasha-inquiry-01.jsonl` | Tasha! |
| `tgo:custom_dialogue:e4a6a32324bf6b94b113` | `custom_dialogue` | `custom-dialogue-map150-followups-01.jsonl` | Tasha! |
| `tgo:custom_dialogue:38ff6ef119c3b6ed36a3` | `custom_dialogue` | `custom-dialogue-map20-event-89-01.jsonl` | Tasha? |
| `tgo:custom_dialogue:5e123677f8e9dc7b9ee1` | `custom_dialogue` | `custom-dialogue-map94-church-followups-01.jsonl` | Tasha? |
| `tgo:custom_dialogue:832829e8bb766ea83780` | `custom_dialogue` | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | Tasha? |
| `tgo:custom_dialogue:dd2c24f5caecef131fcf` | `custom_dialogue` | `custom-dialogue-map11-gym-followups-01.jsonl` | Tasha? |
| `tgo:custom_dialogue:ec300f3926c4fb7964d7` | `custom_dialogue` | `custom-dialogue-map20-event-89-01.jsonl` | Tasha? |
| `tgo:custom_dialogue:ef31fc4d83493219317a` | `custom_dialogue` | `custom-dialogue-map201-finale-followups-01.jsonl` | Tasha… |
| `tgo:custom_dialogue:36939580192af4f40211` | `custom_dialogue` | `custom-dialogue-common-event-411-01.jsonl` | Ugh!... |
| `tgo:custom_dialogue:557c4b4fa8944cf83a6f` | `custom_dialogue` | `custom-dialogue-map20-foyer-heather-arianna-01.jsonl` | … Tasha. |
| `tgo:custom_dialogue:8fdbda3f10fce31d6b4f` | `custom_dialogue` | `custom-dialogue-common-event-364-01.jsonl` | …Judy? |
| `tgo:item_found_label:83c72d9eaac323b63984` | `item_found_label` | `inventory-names-01.jsonl` | Angelcraft |
| `tgo:item_found_label:83c72d9eaac323b63984` | `item_found_label` | `inventory-names-02.jsonl` | Angelcraft |
| `tgo:item_found_label:d15e4ae441c0b291176a` | `item_found_label` | `inventory-names-01.jsonl` | Cheeseburger |
| `tgo:item_found_label:d15e4ae441c0b291176a` | `item_found_label` | `inventory-names-02.jsonl` | Cheeseburger |
| `tgo:item_found_label:183a533a7659b36d1785` | `item_found_label` | `inventory-names-01.jsonl` | Detonator |
| `tgo:item_found_label:183a533a7659b36d1785` | `item_found_label` | `inventory-names-02.jsonl` | Detonator |
| `tgo:item_found_label:067c0fc96aade1c2cc5f` | `item_found_label` | `inventory-names-01.jsonl` | Dildo |
| `tgo:item_found_label:067c0fc96aade1c2cc5f` | `item_found_label` | `inventory-names-02.jsonl` | Dildo |
| `tgo:item_found_label:f348d6fb1cb4f73be7bd` | `item_found_label` | `inventory-names-01.jsonl` | Hamburger |
| `tgo:item_found_label:f348d6fb1cb4f73be7bd` | `item_found_label` | `inventory-names-02.jsonl` | Hamburger |
| `tgo:map_label:bd7c99d21121302c58a1` | `map_label` | `inventory-names-02.jsonl` | Casula Plus |
| `tgo:map_label:bd7c99d21121302c58a1` | `map_label` | `map-labels-01.jsonl` | Casula Plus |
| `tgo:map_label:64d773f024c1586789d9` | `map_label` | `inventory-names-02.jsonl` | Channel 4 |
| `tgo:map_label:64d773f024c1586789d9` | `map_label` | `map-labels-01.jsonl` | Channel 4 |
| `tgo:map_label:6e31a1e38fc48deebd62` | `map_label` | `inventory-names-01.jsonl` | START |
| `tgo:map_label:6e31a1e38fc48deebd62` | `map_label` | `inventory-names-02.jsonl` | START |
| `tgo:map_label:6e31a1e38fc48deebd62` | `map_label` | `map-labels-01.jsonl` | START |
| `tgo:map_label:6a09133ce8abafdf18d3` | `map_label` | `inventory-names-02.jsonl` | Studio |
| `tgo:map_label:6a09133ce8abafdf18d3` | `map_label` | `map-labels-01.jsonl` | Studio |
| `tgo:map_label:9ae9abcb093fb31cef87` | `map_label` | `inventory-names-02.jsonl` | TEST |
| `tgo:map_label:9ae9abcb093fb31cef87` | `map_label` | `map-labels-01.jsonl` | TEST |
| `tgo:map_label:a4227009332364e857cb` | `map_label` | `inventory-names-01.jsonl` | Test |
| `tgo:map_label:a4227009332364e857cb` | `map_label` | `inventory-names-02.jsonl` | Test |
| `tgo:map_label:a4227009332364e857cb` | `map_label` | `map-labels-01.jsonl` | Test |
| `tgo:native_message_unclassified:38040532e832a83ea51d` | `native_message` | `native-messages-01.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:38040532e832a83ea51d` | `native_message` | `native-messages-02.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:38040532e832a83ea51d` | `native_message` | `native-messages-03.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:9c4e260625025fd72c52` | `native_message` | `native-messages-01.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:9c4e260625025fd72c52` | `native_message` | `native-messages-02.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:9c4e260625025fd72c52` | `native_message` | `native-messages-03.jsonl` | <br>\c[27]NLT-Media.com/share\c[0] |
| `tgo:native_message_unclassified:bb7cd910bddb4fa76316` | `native_message` | `native-messages-02.jsonl` | <center><br><br>Hahahahahaha! |
| `tgo:native_message_unclassified:bb7cd910bddb4fa76316` | `native_message` | `native-messages-03.jsonl` | <center><br><br>Hahahahahaha! |
| `tgo:native_message_unclassified:87d68ec14c19a3d09366` | `native_message` | `native-messages-01.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:87d68ec14c19a3d09366` | `native_message` | `native-messages-02.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:87d68ec14c19a3d09366` | `native_message` | `native-messages-03.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:8d582d8ab0d2bf6b1059` | `native_message` | `native-messages-01.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:8d582d8ab0d2bf6b1059` | `native_message` | `native-messages-02.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:8d582d8ab0d2bf6b1059` | `native_message` | `native-messages-03.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:e33751608cacb6707cc6` | `native_message` | `native-messages-01.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:e33751608cacb6707cc6` | `native_message` | `native-messages-02.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:e33751608cacb6707cc6` | `native_message` | `native-messages-03.jsonl` | Cheeseburger |
| `tgo:native_message_unclassified:44d2a5a04982943c30d0` | `native_message` | `native-messages-01.jsonl` | Detonator |
| `tgo:native_message_unclassified:44d2a5a04982943c30d0` | `native_message` | `native-messages-02.jsonl` | Detonator |
| `tgo:native_message_unclassified:44d2a5a04982943c30d0` | `native_message` | `native-messages-03.jsonl` | Detonator |
| `tgo:native_message_unclassified:d3ce5e1714bb030bf823` | `native_message` | `native-messages-01.jsonl` | Detonator |
| `tgo:native_message_unclassified:d3ce5e1714bb030bf823` | `native_message` | `native-messages-02.jsonl` | Detonator |
| `tgo:native_message_unclassified:d3ce5e1714bb030bf823` | `native_message` | `native-messages-03.jsonl` | Detonator |
| `tgo:native_message_unclassified:dbcb065bdf4428ac60aa` | `native_message` | `native-messages-01.jsonl` | Detonator |
| `tgo:native_message_unclassified:dbcb065bdf4428ac60aa` | `native_message` | `native-messages-02.jsonl` | Detonator |
| `tgo:native_message_unclassified:dbcb065bdf4428ac60aa` | `native_message` | `native-messages-03.jsonl` | Detonator |
| `tgo:native_message_unclassified:76257e1625de26a5f085` | `native_message` | `native-messages-01.jsonl` | Hamburger |
| `tgo:native_message_unclassified:76257e1625de26a5f085` | `native_message` | `native-messages-02.jsonl` | Hamburger |
| `tgo:native_message_unclassified:76257e1625de26a5f085` | `native_message` | `native-messages-03.jsonl` | Hamburger |
| `tgo:native_message_unclassified:9c0ed759226505d97727` | `native_message` | `native-messages-01.jsonl` | Hamburger |
| `tgo:native_message_unclassified:9c0ed759226505d97727` | `native_message` | `native-messages-02.jsonl` | Hamburger |
| `tgo:native_message_unclassified:9c0ed759226505d97727` | `native_message` | `native-messages-03.jsonl` | Hamburger |
| `tgo:native_message_unclassified:eaf81580e9b5443814d0` | `native_message` | `native-messages-01.jsonl` | Hamburger |
| `tgo:native_message_unclassified:eaf81580e9b5443814d0` | `native_message` | `native-messages-02.jsonl` | Hamburger |
| `tgo:native_message_unclassified:eaf81580e9b5443814d0` | `native_message` | `native-messages-03.jsonl` | Hamburger |
| `tgo:native_message_unclassified:9a84c2616ffb0847d74b` | `native_message` | `native-messages-02.jsonl` | Reliquiae<br>\fb |
| `tgo:native_message_unclassified:9a84c2616ffb0847d74b` | `native_message` | `native-messages-03.jsonl` | Reliquiae<br>\fb |
| `tgo:phone_contact_ui:1adece89b5f79984b18d` | `phone_contact_ui` | `phone-contact-ui-01.jsonl` | M. Deluna:<br> |
| `tgo:phone_contact_ui:1adece89b5f79984b18d` | `phone_contact_ui` | `phone-contact-ui-02.jsonl` | M. Deluna:<br> |
| `tgo:phone_contact_ui:3fd868291fbf530a7d22` | `phone_contact_ui` | `phone-contact-ui-01.jsonl` | M. Deluna:<br> |
| `tgo:phone_contact_ui:3fd868291fbf530a7d22` | `phone_contact_ui` | `phone-contact-ui-02.jsonl` | M. Deluna:<br> |
| `tgo:phone_contact_ui:f2ba9d2e8fdc629a93ed` | `phone_contact_ui` | `phone-contact-ui-01.jsonl` | M. Deluna:<br> |
| `tgo:phone_contact_ui:f2ba9d2e8fdc629a93ed` | `phone_contact_ui` | `phone-contact-ui-02.jsonl` | M. Deluna:<br> |
| `tgo:system.terms:1c630f8bff93eef9db10` | `system.terms` | `ui-01/system_terms.jsonl` | EXP |
| `tgo:system.terms:25da5e30ca7b2d49dd49` | `system.terms` | `ui-01/system_terms.jsonl` | EXP |
| `tgo:system.terms:56a984a7cb4d516c8654` | `system.terms` | `ui-01/system_terms.jsonl` | Status |
| `tgo:ui.plugin_parameter:cff774686e8c003e9c41` | `ui.plugin_parameter` | `ui-01/ui_plugin_parameter.jsonl` | Lovense Remote |
| `tgo:ui.plugin_parameter:b85d5efdb5f3cdd0d63d` | `ui.plugin_parameter` | `ui-01/ui_plugin_parameter.jsonl` | NLT-Media.com |
| `tgo:ui_choice:7a84642d3172dc2b20a0` | `ui_choice` | `choice-ui-01.jsonl` | Country |
| `tgo:ui_choice:13db3bedc0ef10eb397a` | `ui_choice` | `choice-ui-01.jsonl` | Demon |
| `tgo:ui_choice:2a832e28ed49c0fa5eb9` | `ui_choice` | `choice-ui-01.jsonl` | Ketchup |
| `tgo:ui_choice:60d767e6db092b571332` | `ui_choice` | `choice-ui-01.jsonl` | Ketchup |
| `tgo:ui_choice:f7b73aa9f21f1499408b` | `ui_choice` | `choice-ui-01.jsonl` | Ketchup |
| `tgo:ui_choice:a68c474ba07530997bed` | `ui_choice` | `choice-ui-01.jsonl` | Noir |

## Odtworzenie

```bash
python3 games/the-genesis-order/tools/audit_draft_coverage.py \
  --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md
```
