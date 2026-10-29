#!/usr/bin/env python3
"""Build a branch-aware Polish reading script from static TGO data and drafts.

The output is a reader's edition, not a recovered canonical playthrough. Map
order is based on the first potential reachability from the observed start map;
conditions are not executed and optional scenes may be out of strict chronology.
No game JavaScript is executed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
import zipfile
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from merge_translation_batches import merge_batches

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
CANONICAL = TRANSLATION / "export-v1"
DRAFTS = TRANSLATION / "drafts"
SOURCE_ROOT = ROOT.parents[1] / "google_drive" / "tgo_source"
DEFAULT_OUTPUT = ROOT / "reading" / "v1"
DEFAULT_ZIP = ROOT / "translation" / "packages" / "TGO_readalong_PL_v1.zip"

# Imię bohatera widoczne w Czytance (decyzja właściciela 2026-10-29).
# W grze pozostaje placeholder `1Hero` podstawiany w runtime — to nie jest
# tłumaczenie tekstu gry, tylko sposób prezentacji skryptu.
HERO_NAME = "Mox"

SPEAKERS = {
    "Mc": HERO_NAME, "Ad": "Andrea", "Ar": "Arianna", "Bo": "Bobby",
    "Br": "Brian", "Ca": "Carol", "Ch": "Chloe", "Da": "David",
    "Du": "Duncan", "El": "Ella", "Er": "Erica", "Hn": "Hannah",
    "He": "Heather", "Jo": "Jon", "Ju": "Judy", "Ki": "Kimberly",
    "La": "Larry", "Li": "Lillian", "Me": "Melissa", "Ho": "Zakapturzona postać",
    "Ne": "Nellie", "Ta": "Tasha", "Hr": "Henry", "Di": "Diana",
    "Ob": "Funkcjonariusz B", "Ml": "Madalyn", "Se": "Ochrona",
    "Pl": "Paul", "H1": "Oprych 1", "H2": "Oprych 2",
    "Oa": "Funkcjonariusz A", "Oc": "Funkcjonariusz C",
    "Hw": "Kobieta-popleczniczka", "D1": "Demon 1", "D2": "Demon 2", "D3": "Demon 3",
    "Mo": "Wzmocniony sługa", "Dj": "Demon Judy", "Gn": "Drab",
    "Al": "Alia", "Ll": "Lilith", "Ev": "Evie", "Dm": "Daemalius",
    "Jd": "Sędzia", "Lw": "Prawnik", "Am": "Amulet H.",
    "Si": "Simon", "Sm": "Smithfield", "NPC": "Postać niezależna",
}
UNKNOWN_SPEAKER_PREFIXES = {"Bn", "Ha", "Ba", "Ec", "Ma"}

CATEGORY_ORDER = {
    "custom_dialogue": 0,
    "native_message": 1,
    "phone_text": 2,
    "arianna_hint": 3,
    "image_caption": 4,
    "ui_choice": 5,
    "choice_option": 6,
}
NARRATIVE_CATEGORIES = set(CATEGORY_ORDER)
HTML_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]*>")
VARIABLE_RE = re.compile(r"\\([VNP])\[(\d+)\]", re.IGNORECASE)
ICON_RE = re.compile(r"\\i\[(\d+)\]", re.IGNORECASE)
STYLE_ESCAPE_RE = re.compile(
    r"\\(?:fn(?:<[^>]*>)?|fb|fi|fs\[\d+\]|c\[\d+\]|ow\[\d+\]|ta\[\d+\]|"
    r"w\[\d+\]|\^|!|\||\.|>|<|\$)", re.IGNORECASE
)
CONTROL_ESCAPE_RE = re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?(?:<[^>]*>)?", re.IGNORECASE)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def row_translation(row: dict[str, Any]) -> str:
    value = row.get("translation")
    return value if isinstance(value, str) and value.strip() else row.get("source_text", "")


def clean_reading_text(value: str) -> str:
    text = HTML_BREAK_RE.sub("\n", value)
    text = VARIABLE_RE.sub(
        lambda m: {"V": f"[wartość zmiennej {m.group(2)}]",
                   "N": f"[imię aktora {m.group(2)}]",
                   "P": f"[członek drużyny {m.group(2)}]"}[m.group(1).upper()], text
    )
    text = ICON_RE.sub(lambda m: f"[ikona {m.group(1)}]", text)
    text = STYLE_ESCAPE_RE.sub("", text)
    text = CONTROL_ESCAPE_RE.sub("", text)
    text = HTML_TAG_RE.sub("", text)
    text = text.replace("\\\\", "\\")
    text = "\n".join(part.strip() for part in text.splitlines())
    return re.sub(r"[ \t]+", " ", text).strip()


def hero_text(value: str) -> str:
    """Show the hero's real name instead of the game's ``1Hero`` placeholder."""
    return value.replace("1Hero", HERO_NAME)


def source_map_paths(source_root: Path) -> dict[int, Path]:
    paths: dict[int, Path] = {}
    for path in source_root.glob("Map*.json"):
        match = re.fullmatch(r"Map(\d{3})\.json", path.name)
        if match:
            paths[int(match.group(1))] = path
    return paths


def load_map_and_common(source_root: Path) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], dict[int, dict[str, Any]]]:
    map_paths = source_map_paths(source_root)
    maps = {map_id: read_json(path) for map_id, path in map_paths.items()}
    common_path = source_root / "CommonEvents.json"
    common_rows = read_json(common_path)
    common = {row["id"]: row for row in common_rows if isinstance(row, dict) and row.get("id")}
    infos_rows = read_json(source_root / "MapInfos.json")
    infos = {row["id"]: row for row in infos_rows if isinstance(row, dict) and row.get("id")}
    return maps, common, infos


def commands_in_event_pages(map_doc: dict[str, Any]):
    for event in map_doc.get("events") or []:
        if not isinstance(event, dict):
            continue
        for page_number, page in enumerate(event.get("pages") or [], 1):
            if isinstance(page, dict):
                yield event, page_number, page.get("list") or []


def direct_common_calls(commands: list[dict[str, Any]]) -> list[tuple[int, int]]:
    calls = []
    for command_index, command in enumerate(commands):
        if isinstance(command, dict) and command.get("code") == 117:
            params = command.get("parameters") or []
            if params and isinstance(params[0], int):
                calls.append((command_index, params[0]))
    return calls


def transfer_targets(commands: list[dict[str, Any]]) -> list[int]:
    targets = []
    for command in commands:
        if not isinstance(command, dict) or command.get("code") != 201:
            continue
        params = command.get("parameters") or []
        if len(params) > 1 and params[0] == 0 and isinstance(params[1], int):
            targets.append(params[1])
    return targets


def common_call_graph(common: dict[int, dict[str, Any]]) -> tuple[dict[int, list[int]], dict[int, set[int]]]:
    calls: dict[int, list[int]] = {}
    direct_transfers: dict[int, set[int]] = {}
    for common_id, event in common.items():
        commands = event.get("list") or []
        calls[common_id] = [child for _, child in direct_common_calls(commands) if child in common]
        direct_transfers[common_id] = set(transfer_targets(commands))
    transfers: dict[int, set[int]] = {}
    for start in common:
        seen: set[int] = set()
        pending = [start]
        reached: set[int] = set()
        while pending:
            current = pending.pop()
            if current in seen or current not in common:
                continue
            seen.add(current)
            reached.update(direct_transfers.get(current, set()))
            pending.extend(calls.get(current, []))
        transfers[start] = reached
    return calls, transfers


def map_graph(maps: dict[int, dict[str, Any]], common: dict[int, dict[str, Any]]) -> dict[int, set[int]]:
    graph: dict[int, set[int]] = defaultdict(set)
    _, common_transfers = common_call_graph(common)
    for map_id, map_doc in maps.items():
        for _, _, commands in commands_in_event_pages(map_doc):
            graph[map_id].update(transfer_targets(commands))
            for _, common_id in direct_common_calls(commands):
                graph[map_id].update(common_transfers.get(common_id, set()))
    return graph


def map_ranks(maps: dict[int, dict[str, Any]], common: dict[int, dict[str, Any]],
              infos: dict[int, dict[str, Any]], start_map: int) -> tuple[dict[int, int], dict[int, set[int]], dict[int, int]]:
    graph = map_graph(maps, common)
    distance = {start_map: 0}
    queue = deque([start_map])
    while queue:
        current = queue.popleft()
        for target in sorted(graph.get(current, set())):
            if target in maps and target not in distance:
                distance[target] = distance[current] + 1
                queue.append(target)
    tie_sorted = sorted(maps, key=lambda mid: (
        distance.get(mid, 1_000_000), infos.get(mid, {}).get("order", 1_000_000), mid
    ))
    return {mid: index for index, mid in enumerate(tie_sorted)}, graph, distance


def first_common_call_order(maps: dict[int, dict[str, Any]], common: dict[int, dict[str, Any]],
                            infos: dict[int, dict[str, Any]], map_rank: dict[int, int]) -> dict[int, tuple[int, ...]]:
    import heapq

    call_graph, _ = common_call_graph(common)
    queue: list[tuple[tuple[int, ...], int]] = []
    for map_id in sorted(maps, key=lambda mid: map_rank[mid]):
        map_doc = maps[map_id]
        for event, page_number, commands in sorted(
            commands_in_event_pages(map_doc), key=lambda item: (item[0].get("id", 0), item[1])
        ):
            for command_index, common_id in direct_common_calls(commands):
                key = (map_rank[map_id], infos.get(map_id, {}).get("order", 0), map_id,
                       event.get("id", 0), page_number, command_index, 0, -1, common_id)
                heapq.heappush(queue, (key, common_id))

    order: dict[int, tuple[int, ...]] = {}
    while queue:
        key, common_id = heapq.heappop(queue)
        if common_id not in common or (common_id in order and order[common_id] <= key):
            continue
        order[common_id] = key
        depth = key[6]
        for child_index, child_id in enumerate(call_graph.get(common_id, [])):
            child_key = key[:6] + (depth + 1, child_index, child_id)
            if child_id not in order or child_key < order[child_id]:
                heapq.heappush(queue, (child_key, child_id))
    return order


def event_key(row: dict[str, Any]) -> tuple[str, int | None, int | None, int | None]:
    context = row.get("context") or {}
    source_kind = context.get("source_kind") or "common_event"
    if source_kind == "map":
        return ("map", context.get("map_id"), context.get("event_id"), context.get("page_number"))
    return ("common_event", None, context.get("event_id"), None)


def choice_tables(rows: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[tuple[str, int], str]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    label_by_group_index: dict[tuple[str, int], str] = {}
    for row in rows:
        if row.get("category") not in {"choice_option", "ui_choice"}:
            continue
        context = row.get("context") or {}
        structure = row.get("structure") or {}
        group = context.get("choice_group_id") or structure.get("choice_group_id")
        index = context.get("choice_index", structure.get("option_index"))
        if not isinstance(group, str) or not isinstance(index, int):
            continue
        groups[group].append(row)
        label_by_group_index[(group, index)] = clean_reading_text(row_translation(row))
    for group in groups:
        groups[group].sort(key=lambda row: (
            (row.get("context") or {}).get("choice_index", (row.get("structure") or {}).get("option_index", 0)),
            row.get("id", ""),
        ))
    return groups, label_by_group_index


def format_condition(parameters: list[Any], switches: list[str], variables: list[str]) -> str:
    if not parameters:
        return "warunek RPG Maker"
    kind = parameters[0]
    if kind == 0 and len(parameters) >= 3:
        sid, enabled = parameters[1], bool(parameters[2])
        name = switches[sid] if isinstance(sid, int) and sid < len(switches) and switches[sid] else f"#{sid}"
        return f"{name}: {'włączony' if enabled else 'wyłączony'}"
    if kind == 1 and len(parameters) >= 5:
        vid, operand_type, operand, op = parameters[1:5]
        name = variables[vid] if isinstance(vid, int) and vid < len(variables) and variables[vid] else f"#{vid}"
        ops = {0: "=", 1: "≥", 2: "≤", 3: ">", 4: "<", 5: "≠"}
        right = f"zmienna #{operand}" if operand_type else str(operand)
        return f"{name} {ops.get(op, '?')} {right}"
    if kind == 2 and len(parameters) >= 2:
        enabled = parameters[2] if len(parameters) >= 3 else True
        return f"przełącznik lokalny {parameters[1]}: {'włączony' if enabled else 'wyłączony'}"
    if kind == 3:
        return "warunek licznika czasu"
    labels = {4: "warunek aktora", 5: "warunek przeciwnika", 6: "warunek postaci", 7: "warunek pieniędzy",
              8: "warunek przedmiotu", 9: "warunek broni", 10: "warunek zbroi", 11: "warunek przycisku",
              12: "warunek skryptowy"}
    return f"{labels.get(kind, 'warunek RPG Maker')} {parameters[1:]}"


def branch_labels(row: dict[str, Any], label_by_group_index: dict[tuple[str, int], str],
                  switches: list[str], variables: list[str]) -> str:
    parts = []
    context = row.get("context") or {}
    for branch in context.get("branch_path") or []:
        if branch.get("kind") == "choice_branch":
            group, index = branch.get("choice_group_id"), branch.get("option_index")
            label = label_by_group_index.get((group, index), clean_reading_text(branch.get("branch_label", "")))
            if label:
                parts.append(f"wybór «{label}»")
        elif branch.get("kind") == "condition":
            parts.append(format_condition(branch.get("parameters") or [], switches, variables))
        elif branch.get("kind") == "else":
            parts.append("gałąź alternatywna")
    return " → ".join(parts)


def page_condition_notes(context: dict[str, Any], switches: list[str], variables: list[str]) -> list[str]:
    cond = context.get("page_conditions") or {}
    notes = []
    for key, name_list, label in (("switch1Id", switches, "przełącznik"), ("switch2Id", switches, "przełącznik")):
        if cond.get(key + "Valid"):
            idx = cond.get(key)
            name = name_list[idx] if isinstance(idx, int) and idx < len(name_list) and name_list[idx] else f"#{idx}"
            notes.append(f"{label} {name} musi być włączony")
    if cond.get("selfSwitchValid"):
        notes.append(f"przełącznik lokalny {cond.get('selfSwitchCh')} musi być włączony")
    if cond.get("variableValid"):
        idx = cond.get("variableId")
        name = variables[idx] if isinstance(idx, int) and idx < len(variables) and variables[idx] else f"#{idx}"
        notes.append(f"warunek zmiennej {name} (wartość {cond.get('variableValue')})")
    if cond.get("itemValid"):
        notes.append(f"wymaga przedmiotu #{cond.get('itemId')}")
    if cond.get("actorValid"):
        notes.append(f"wymaga aktora #{cond.get('actorId')}")
    return notes


def speaker_for(row: dict[str, Any]) -> tuple[str, str]:
    context = row.get("context") or {}
    if row.get("category") == "custom_dialogue":
        header = str(context.get("custom_header") or "")
        if header == "I can’t be wasting time" and context.get("map_id") == 3 and context.get("event_id") in range(1, 17):
            return HERO_NAME, "header:niekanoniczny; przypisanie z kontekstu sceny początkowej"
        if header == "NPC":
            return "Postać niezależna", "jawny kod NPC"
        match = re.match(r"^@?([A-Z][a-z]|[A-Z]\d)", header)
        if match:
            prefix = match.group(1)
            if prefix in SPEAKERS:
                return SPEAKERS[prefix], f"kod mówcy {prefix}"
            return f"Mówca nieustalony ({prefix})", f"nieznany kod {prefix}"
        return "Mówca nieustalony", "brak rozpoznawalnego kodu mówcy"
    speaker = context.get("speaker")
    if speaker:
        return str(speaker), "speaker z eksportu"
    header = context.get("message_header") or {}
    face = header.get("faceName")
    if face:
        return str(face), "faceName z okna wiadomości"
    return "Narrator / mówca nieustalony", "brak jawnego mówcy w źródle"


def display_group(group: list[dict[str, Any]]) -> str:
    options = [clean_reading_text(row_translation(row)) for row in group]
    options = [value for value in options if value]
    if not options:
        return ""
    lines = ["**Wybór gracza:**"]
    lines.extend(f"- {option}" for option in options)
    return "\n".join(lines)


def render_episode(key: tuple[str, int | None, int | None, int | None],
                   rows: list[dict[str, Any]],
                   choice_groups: dict[str, list[dict[str, Any]]],
                   labels: dict[tuple[str, int], str],
                   switches: list[str], variables: list[str],
                   map_name: str = "", common_name: str = "") -> tuple[str, dict[str, Any]]:
    """Render one episode as Markdown blocks.

    Kwestie dialogowe idą jedna pod drugą (twarde złamanie wiersza zamiast
    pustej linii między nimi), żeby skrypt dał się czytać jak scenariusz.
    Bloki strukturalne — warunki, ścieżki, wybory, podpisy — nadal są
    oddzielone pustą linią, bo tego wymaga Markdown.
    """
    kind, map_id, event_id, page_number = key
    title = (f"Mapa {map_id:03d} — {map_name}" if kind == "map" and isinstance(map_id, int)
             else f"Common Event {event_id:03d} — {common_name}")
    if kind == "map":
        title += f" / event {event_id}"
        if page_number is not None:
            title += f" / strona {page_number}"
    blocks: list[str] = [f"## {title}"]
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            blocks.append("\n".join(paragraph))
            paragraph.clear()

    context = (rows[0].get("context") or {}) if rows else {}
    notes = page_condition_notes(context, switches, variables)
    if notes:
        blocks.append("> **Warunek strony:** " + "; ".join(notes) + ".")

    last_branch = object()
    printed_groups: set[str] = set()
    included = 0
    unknown_speakers: list[str] = []
    speaker_counts: Counter[str] = Counter()
    for row in sorted(rows, key=lambda r: (
        ((r.get("context") or {}).get("command_index")
         if (r.get("context") or {}).get("command_index") is not None
         else (r.get("source", {}).get("locator", {}).get("command_index", 0))),
        CATEGORY_ORDER.get(r.get("category", ""), 99), r.get("id", ""),
    )):
        category = row.get("category")
        context = row.get("context") or {}
        branch = branch_labels(row, labels, switches, variables)
        if branch != last_branch:
            if branch:
                flush()
                blocks.append(f"> **Ścieżka warunkowa:** {branch}.")
            last_branch = branch
        if category in {"choice_option", "ui_choice"}:
            group_id = context.get("choice_group_id") or (row.get("structure") or {}).get("choice_group_id")
            if isinstance(group_id, str) and group_id not in printed_groups:
                block = display_group(choice_groups.get(group_id, [row]))
                if block:
                    flush()
                    blocks.append(block)
                    included += 1
                    printed_groups.add(group_id)
            continue

        text = hero_text(clean_reading_text(row_translation(row)))
        if not text:
            continue
        if category == "image_caption":
            flush()
            blocks.append(f"*〔Podpis widoczny przy obrazie: {text}〕*")
            included += 1
            continue
        if category == "arianna_hint":
            flush()
            blocks.append(f"*〔Wskazówka: {text}〕*")
            included += 1
            continue
        speaker, _basis = speaker_for(row)
        speaker_counts[speaker] += 1
        if "nieustalony" in speaker.casefold():
            unknown_speakers.append(row.get("id", ""))
        for part in text.split("\n"):
            if part:
                paragraph.append(f"**{speaker}:** {part}  ")
        included += 1
    if included == 0:
        return "", {"included": 0, "unknown_speakers": [], "speaker_counts": {}}
    flush()
    return "\n\n".join(blocks), {
        "included": included, "unknown_speakers": unknown_speakers,
        "speaker_counts": dict(speaker_counts),
    }


def _source_note(source_ids: str) -> str:
    """Traceability footer kept in episode files, dropped from the full script."""
    return f"<sub>Źródłowe ID (przykłady): {source_ids}</sub>"


def character_index(speaker_counts: Counter[str]) -> str:
    lines = ["# Indeks postaci i mówców — PL", "",
             "Zestawienie wynika wyłącznie z jawnych nagłówków/etykiet mówcy w rekordach. Liczba oznacza widoczne kwestie w Czytance, nie unikalne linie fabularne.", ""]
    if not speaker_counts:
        lines.append("Brak jawnie rozpoznanych mówców.")
    else:
        for name, count in sorted(speaker_counts.items(), key=lambda item: (item[0].casefold(), item[0])):
            note = " — etykieta nieustalona; nie przypisano jej postaci" if "nieustalony" in name.casefold() else ""
            lines.append(f"- **{name}** — {count} kwestii{note}.")
    return "\n".join(lines) + "\n"


def location_index(maps: dict[int, dict[str, Any]], infos: dict[int, dict[str, Any]],
                   map_rank: dict[int, int], map_distance: dict[int, int],
                   map_names: dict[int, dict[str, Any]], episode_counts: Counter[int]) -> str:
    lines = ["# Indeks lokacji — PL", "",
             "Nazwy pochodzą z przetłumaczonych etykiet map; w razie ich braku użyto źródłowej nazwy MapInfos. Osiągalność jest statyczna i nie uwzględnia warunków/runtime.", ""]
    for map_id in sorted(maps, key=lambda mid: map_rank[mid]):
        row = map_names.get(map_id)
        name = clean_reading_text(row_translation(row)) if row else ""
        name = name or clean_reading_text((infos.get(map_id) or {}).get("name", "")) or "(bez nazwy)"
        distance = map_distance.get(map_id)
        reachability = f"potencjalnie osiągalna, BFS {distance}" if distance is not None else "poza grafem osiągalności od startu"
        lines.append(f"- **Mapa {map_id:03d} — {name}** — {reachability}; epizodów: {episode_counts.get(map_id, 0)}.")
    return "\n".join(lines) + "\n"


def load_previous_order(path: Path | None) -> dict[tuple[str, int, int, int], dict[str, str]]:
    """Wczytaj wiersze z wcześniejszego `reading_order.tsv`.

    Źródła gry nie są w repozytorium, więc pełne przeliczenie grafu osiągalności
    dałoby inną (nie gorszą, ale inną) numerację rozdziałów. Tryb offline
    zachowuje numerację i metadane opublikowane w `reading/v1`, żeby nowe
    wydanie różniło się wyłącznie poprawkami redakcyjnymi.
    """
    if path is None or not path.is_file():
        return {}
    rows: dict[tuple[str, int, int, int], dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for record in csv.DictReader(stream, delimiter="\t"):
            if not record.get("sequence"):
                continue
            key = (record.get("kind", ""), int(record.get("map_id") or 0),
                   int(record.get("event_id") or 0), int(record.get("page_number") or 0))
            rows[key] = record
    return rows


def previous_locations_index(path: Path | None) -> tuple[str, int, int] | None:
    """Wczytaj opublikowany indeks lokacji i policz mapy (wszystkie/osiągalne).

    Indeks lokacji wymaga nazw i kolejności map z `MapInfos.json` oraz grafu
    transferów; tych danych nie ma w repozytorium. Nowe wydanie dziedziczy więc
    indeks z poprzedniego, a liczby w README bierzemy z niego samego.
    """
    if path is None or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.startswith("- **Mapa ")]
    reachable = sum(1 for line in lines if "potencjalnie osiągalna" in line)
    return text, len(lines), reachable


def build(source_root: Path, output: Path, zip_path: Path,
          previous_order: Path | None = None,
          locations_index: Path | None = None) -> dict[str, Any]:
    source_root = source_root.resolve()
    output = output.resolve()
    zip_path = zip_path.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite reading output: {output}")
    if zip_path.exists():
        raise FileExistsError(f"Refusing to overwrite reading ZIP: {zip_path}")
    if not (source_root / "MapInfos.json").is_file() or not (source_root / "CommonEvents.json").is_file():
        raise FileNotFoundError(f"Expected extracted static TGO source data in {source_root}")

    maps, common, infos = load_map_and_common(source_root)
    system = read_json(source_root / "System.json")
    switches = system.get("switches") or []
    variables = system.get("variables") or []
    start_map = system.get("startMapId", 38)
    map_rank, graph, map_distance = map_ranks(maps, common, infos, start_map)
    common_order = first_common_call_order(maps, common, infos, map_rank)

    with tempfile.TemporaryDirectory(prefix=".readalong-merge-", dir=TRANSLATION) as work_name:
        merged = Path(work_name) / "merged.jsonl"
        merge_report = merge_batches(CANONICAL, sorted(DRAFTS.rglob("*.jsonl")), merged, TRANSLATION)
        rows = [json.loads(line) for line in merged.read_text(encoding="utf-8").splitlines() if line.strip()]

    choice_groups, label_by_group_index = choice_tables(rows)
    grouped: dict[tuple[str, int | None, int | None, int | None], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("category") not in NARRATIVE_CATEGORIES:
            continue
        if row.get("category") in {"choice_option", "ui_choice"}:
            # Keep every player choice; they may encode story branches or useful menus.
            pass
        grouped[event_key(row)].append(row)

    map_names = {
        (row.get("context") or {}).get("map_id"): row for row in rows
        if row.get("category") == "map_label" and isinstance((row.get("context") or {}).get("map_id"), int)
    }
    episodes: list[tuple[tuple[Any, ...], tuple[str, int | None, int | None, int | None], str]] = []
    unknown_speaker_ids: set[str] = set()
    speaker_counts: Counter[str] = Counter()
    for key, event_rows in grouped.items():
        kind, map_id, event_id, page_number = key
        if kind == "map":
            rank = map_rank.get(map_id, 1_000_000)
            info = infos.get(map_id, {})
            event_sort = (rank, info.get("order", 1_000_000), map_id or 0, event_id or 0, page_number or 0, 0)
            map_row = map_names.get(map_id)
            name = clean_reading_text(row_translation(map_row)) if map_row else info.get("name", "")
            content, stats = render_episode(key, event_rows, choice_groups, label_by_group_index,
                                            switches, variables, map_name=name)
            unknown_speaker_ids.update(stats["unknown_speakers"])
            speaker_counts.update(stats["speaker_counts"])
            certainty = "map-first-potential-reach-order"
        else:
            first = common_order.get(event_id, (2_000_000, 2_000_000, event_id or 0, 0, 0, 0))
            rank = first[0] if first else 2_000_000
            common_name = (common.get(event_id) or {}).get("name", "")
            call_map = first[2] if len(first) > 2 and isinstance(first[2], int) else None
            call_map_rank = map_rank.get(call_map, 1_000_000) if call_map is not None else 1_000_000
            event_sort = (call_map_rank, first[1] if len(first) > 1 else 1_000_000,
                          call_map or 0, first[3] if len(first) > 3 else 0,
                          first[5] if len(first) > 5 else 0, event_id or 0)
            content, stats = render_episode(key, event_rows, choice_groups, label_by_group_index,
                                            switches, variables, common_name=common_name)
            unknown_speaker_ids.update(stats["unknown_speakers"])
            speaker_counts.update(stats["speaker_counts"])
            certainty = "first-static-common-event-call"
        if content:
            episodes.append((event_sort, key, content))

    episodes.sort(key=lambda item: item[0])
    previous = load_previous_order(previous_order)
    if previous:
        fallback = max((int(row["sequence"]) for row in previous.values()), default=0) + 1
        episodes.sort(key=lambda item: (int(previous.get(
            (item[1][0], item[1][1] or 0, item[1][2] or 0, item[1][3] or 0),
            {"sequence": fallback})["sequence"]), item[0]))
    output.mkdir(parents=True)
    episode_dir = output / "episodes"
    episode_dir.mkdir()
    order_rows = []
    full_script = [
        "# The Genesis Order — Czytanka PL (kolejność statycznie przybliżona)", "",
        "> To reader’s edition z zachowanymi warunkami i wyborami. Nie jest kanoniczną linią czasu: mapy uporządkowano według najwcześniejszej potencjalnej osiągalności od mapy startowej, bez wykonania warunków, przełączników ani danych runtime. Warianty mogą wystąpić w różnej kolejności albo nie wystąpić w jednym przejściu.", "",
    ]
    file_manifest = []
    for sequence, (sort_key, key, content) in enumerate(episodes, 1):
        kind, map_id, event_id, page_number = key
        filename = (f"{sequence:04d}_map{map_id:03d}_event{event_id:03d}_page{page_number:02d}.md"
                    if kind == "map" else f"{sequence:04d}_common_event{event_id:03d}.md")
        episode_path = episode_dir / filename
        source_note = _source_note(", ".join(row["id"] for row in grouped[key][:8]))
        episode_path.write_text(content + "\n\n" + source_note + "\n", encoding="utf-8", newline="\n")
        title = f"Map {map_id} event {event_id} page {page_number}" if kind == "map" else f"Common Event {event_id} {(common.get(event_id) or {}).get('name', '')}"
        inherited = previous.get((kind, map_id or 0, event_id or 0, page_number or 0)) or {}
        order_rows.append({
            "sequence": sequence, "episode": filename, "kind": kind,
            "map_id": map_id or "", "event_id": event_id or "", "page_number": page_number or "",
            "map_rank": inherited.get("map_rank") if inherited else (map_rank.get(map_id, "") if map_id is not None else ""),
            "chronology_basis": inherited.get("chronology_basis") if inherited else (
                "first potential map reachability; condition evaluation omitted" if kind == "map"
                else "first statically observed common-event call; conditional call order uncertain"),
            "title": (inherited.get("title") if inherited else "") or title,
        })
        full_script.extend([content, "\n---\n"])
        file_manifest.append(filename)

    order_path = output / "reading_order.tsv"
    with order_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(order_rows[0].keys()) if order_rows else ["sequence", "episode"],
                                delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(order_rows)
    full_script_path = output / "chronological_script_PL.md"
    full_script_path.write_text("\n".join(full_script), encoding="utf-8", newline="\n")
    episode_counts = Counter(key[1] for _, key, _ in episodes if key[0] == "map" and key[1] is not None)
    (output / "index_characters_PL.md").write_text(character_index(speaker_counts), encoding="utf-8", newline="\n")
    inherited_index = previous_locations_index(locations_index)
    if inherited_index is not None:
        index_text, total_maps, inherited_reachable = inherited_index
        (output / "index_locations_PL.md").write_text(index_text, encoding="utf-8", newline="\n")
        reachable = inherited_reachable
    else:
        (output / "index_locations_PL.md").write_text(
            location_index(maps, infos, map_rank, map_distance, map_names, episode_counts),
            encoding="utf-8", newline="\n",
        )
        reachable = len(map_distance)
        total_maps = len(maps)
    common_scene_count = sum(1 for _, key, _ in episodes if key[0] == "common_event")
    map_scene_count = sum(1 for _, key, _ in episodes if key[0] == "map")

    inheritance_note = ""
    if inherited_index is not None:
        inheritance_note = ("- Numeracja rozdziałów i indeks lokacji są dziedziczone z wydania v1: źródła gry nie są "
                            "przechowywane w repozytorium, więc grafu osiągalności ani nazw map nie przelicza się od zera. "
                            "Treść kwestii pochodzi w całości z bieżącego korpusu tłumaczeń.\n")
    readme = f"""# Czytanka TGO PL — wydanie robocze v1

## Jak czytać

- Zacznij od `chronological_script_PL.md` (pełny tekst). Wersje rozdziałów są osobno w `episodes/`, `reading_order.tsv` podaje kolejność i podstawę sortowania, a `index_characters_PL.md` i `index_locations_PL.md` są indeksami mówców i lokacji.
- Każda kwestia ma jawnego mówcę, gdy można go statycznie odczytać z kodu nagłówka; nierozpoznane nagłówki są oznaczone, nie zgadywane.
- **Ścieżka warunkowa** zachowuje wybory i warunki z kontekstu eventu. Wybory są listowane w miejscu polecenia. Mówca, etykiety i dialog pochodzą ze scalonych tłumaczeń; wartości kontrolne i nazwy własne pozostają źródłowe.
- Wartości `\\V[n]`, `\\N[n]` i `\\P[n]` są oznaczane jako zmienna, imię aktora lub członek drużyny; `\\I[n]` jako ikona. Niepewne wartości nie są zgadywane.

## Ważne ograniczenie chronologii

Kolejność jest **przybliżona i statyczna**, nie kanoniczna: początkowa kolejność map to BFS po bezpośrednich transferach RPG Maker i rozpoznanych wywołaniach Common Events z mapy startowej {start_map}. Warunki, przełączniki, zmienne, wybory oraz runtime nie są wykonywane. **{reachable}/{total_maps}** map ma potencjalną ścieżkę od startu w tym grafie; pozostałe są na końcu w kolejności edytora. Common Events sortujemy po pierwszym znalezionym wywołaniu, a nie po gwarantowanej kolejności rozgrywki. Sceny opcjonalne/ponownie odtwarzane mogą mieć inne miejsce; nie traktuj ich sąsiedztwa jako jednej rozgrywki.

To zachowuje ostrzeżenie z przykładowych skryptów SRW: warunkowe/sytuacyjne kwestie nie tworzą jednej, gwarantowanej osi czasu.

## Statyczne źródła i liczby

{inheritance_note}- Korpus: {merge_report['records']:,} kanonicznych rekordów; {merge_report['with_translation']:,} rekordów z tłumaczeniem; nazwy własne, markery, kody i jawnie chronione wartości pozostają bez zmian.
- W tym wydaniu: {map_scene_count} rozdziałów map/event/page i {common_scene_count} rozdziałów Common Events.
- Gry nie uruchamiano. Nie dołączono assetów, mediów, kodu gry ani zapisów.
- Źródłowe ID w plikach pozwalają wrócić do rekordu JSONL. Pełna lista kolejności znajduje się w `reading_order.tsv`.
"""
    (output / "README_PL.md").write_text(readme, encoding="utf-8", newline="\n")

    if not order_rows:
        raise ValueError("No narrative episode was generated")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(zip_path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"ZIP CRC error in {bad}")
    digest = __import__("hashlib").sha256(zip_path.read_bytes()).hexdigest()
    zip_path.with_suffix(zip_path.suffix + ".sha256").write_text(f"{digest}  {zip_path.name}\n", encoding="ascii")
    return {
        "output": str(output), "zip": str(zip_path), "sha256": digest,
        "episodes": len(episodes), "map_episodes": map_scene_count,
        "common_event_episodes": common_scene_count,
        "maps_reachable_from_start": reachable, "total_maps": total_maps,
        "translation_records_merged": merge_report["with_translation"],
        "unknown_speaker_rows": len(unknown_speaker_ids),
        "indexed_speakers": len(speaker_counts),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=SOURCE_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--zip", type=Path, default=DEFAULT_ZIP)
    parser.add_argument("--previous-order", type=Path, default=None,
                        help="poprzedni reading_order.tsv — zachowuje numerację i metadane rozdziałów")
    parser.add_argument("--locations-index", type=Path, default=None,
                        help="poprzedni index_locations_PL.md — użyj, gdy brak danych map gry")
    args = parser.parse_args()
    print(json.dumps(build(args.source_root, args.output, args.zip, args.previous_order,
                           args.locations_index), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
