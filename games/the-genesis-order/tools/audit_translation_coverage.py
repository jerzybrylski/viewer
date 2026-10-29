#!/usr/bin/env python3
"""Audit untranslated TGO records without generating or altering translations.

Only source values with a reviewed non-linguistic, proper-name, numeric,
renderer, or protected-value rationale are considered complete without a new
translation. Any other blank translation remains an unresolved item.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from merge_translation_batches import merge_batches

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
DEFAULT_CANONICAL = TRANSLATION / "export-v1"
DEFAULT_DRAFTS = TRANSLATION / "drafts"
DEFAULT_OUTPUT = TRANSLATION / "reports" / "coverage_audit_v1.json"

CONTROL_OR_EMOTE_VALUES = {
    "...", "…", "… ", "/appreciate", "/comeback", "/curse", "/excited",
    "/fail", "/find", "/finduseful", "/greet", "/greetback", "/investigate",
    "/locked", "/order", "/shock", "/shocked", "/show", "/showsolve",
    "/solve", "/success", "/success.", "/thanks", "/toomuch", "/worried",
    "/worry", "/worthless",
}
CHARACTER_NAMES = {
    "Andrea", "Arianna", "Carol", "Chloe", "Ella", "Erica", "Hannah",
    "Heather", "Judy", "Kimberly", "Lillian", "Melissa", "Nellie",
}
ACTOR_NAMES = CHARACTER_NAMES | {"William"}
UI_NAME_VALUES = CHARACTER_NAMES
IMAGE_NAMES = CHARACTER_NAMES | {"Frogger"}
RENDERER_ESCAPE_RE = re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?")
PUNCTUATION_ESCAPE_RE = re.compile(r"\\[\^!|><{}.$]")
HTML_TAG_RE = re.compile(r"<[^>]*>")
ONLY_CONTROL_RE = re.compile(r"^(?:\\[A-Za-z]+(?:\[[^\]]*\])?|[\s.,#%$0-9!?…•>\-]*)+$")
MONEY_RE = re.compile(r"\$[0-9][0-9,]*(?:\.[0-9]+)?")


def visible_residue(text: str) -> str:
    text = RENDERER_ESCAPE_RE.sub("", text)
    text = PUNCTUATION_ESCAPE_RE.sub("", text)
    return HTML_TAG_RE.sub("", text).strip()


def _preserved(reason: str) -> tuple[str, str]:
    return ("source_preserved", reason)


# Decyzje właściciela z 2026-10-29, zapisane jako jawne wyjątki od tłumaczenia.
# Każdy wpis ma ID decyzji w docs/EDITORIAL_DECISIONS.md; bez niego nie wolno
# dopisać tu kolejnej wartości (bramka ma pozostać wąska).
OWNER_KEEP_SOURCE = (
    # R-01: tytuł gry zostaje jako nazwa marki.
    ("system.gameTitle", "The Genesis Order", "owner_decision_R01_brand_title_kept_in_english"),
    # R-08: literał kanału telefonu na mapie testowej.
    ("phone_text", "TEXT", "owner_decision_R08_test_map_stub_kept_in_english"),
)


def owner_keep_source(row: dict[str, Any]) -> str | None:
    """Return the recorded owner decision for a value kept in English, if any."""
    category = row.get("category")
    source = row.get("source_text") or ""
    context = row.get("context") or {}
    for rule_category, rule_source, reason in OWNER_KEEP_SOURCE:
        if category == rule_category and source == rule_source:
            return reason
    # R-07: wypełniacze widoczne tylko na TEST MAP (EV001) zostają po angielsku.
    if (category == "native_message" and source.startswith("Text goes here")
            and context.get("map_name") == "TEST MAP"):
        return "owner_decision_R07_test_map_placeholder_kept_in_english"
    return None


def classify_untranslated(row: dict[str, Any]) -> tuple[str, str] | None:
    """Return disposition and explanation for an intentionally unchanged value."""
    context = row.get("context") or {}
    category = row.get("category")
    source = row.get("source_text", "")
    residue = visible_residue(source)

    if context.get("translation_policy") == "keep_source_value":
        return _preserved("explicit_keep_source_value_policy")
    owner_decision = owner_keep_source(row)
    if owner_decision:
        return _preserved(owner_decision)
    if category == "custom_dialogue" and source in CONTROL_OR_EMOTE_VALUES:
        return _preserved("custom_dialogue_emote_or_pause_control")
    if category == "choice_option":
        if not residue or residue.isdecimal() or MONEY_RE.fullmatch(residue):
            return _preserved("numeric_or_runtime_choice_value")
        if residue in CHARACTER_NAMES:
            return _preserved("character_name_in_choice")
        if (residue in {"U", "L", "C", "S"}
                and context.get("map_id") == 17 and context.get("event_id") == 68):
            return _preserved("single_letter_quiz_answer")
    if category == "native_message":
        if not residue or residue.isdecimal():
            return _preserved("renderer_control_or_numeric_message_fragment")
        if MONEY_RE.fullmatch(residue):
            return _preserved("displayed_amount")
        if residue in {"Madalyn.", "Morgan #142"}:
            return _preserved("proper_name_or_name_with_identifier")
    if category == "credits":
        if row.get("source", {}).get("file") == "data/Credits.txt":
            return _preserved("supporter_handle_or_credit_attribution")
    if category == "database.actors.name":
        if residue in ACTOR_NAMES or re.fullmatch(r"[0-9%]+", residue):
            return _preserved("proper_name_or_actor_slot_marker")
    if category == "database.items.name" and residue == "Arianna":
        return _preserved("character_name_used_as_item_label")
    if category == "image_caption" and residue in IMAGE_NAMES:
        return _preserved("character_or_media_title_caption")
    if category == "phone_contact_ui":
        if not residue or residue.isdecimal():
            return _preserved("phone_renderer_control_or_year")
        if residue in {"Amulet K.", "Morgan."}:
            return _preserved("phone_contact_name")
    if category == "phone_text" and not residue:
        return _preserved("phone_renderer_control")
    if category == "ui.variable_value":
        if (not residue or residue in UI_NAME_VALUES or residue == "???"
                or MONEY_RE.fullmatch(residue)):
            return _preserved("symbol_amount_or_character_name_variable")
    if category == "ui_choice" and not residue:
        return _preserved("runtime_variable_choice_value")
    if category == "ui.plugin_static" and context.get("translation_policy") == "keep_source_value":
        return _preserved("runtime_connection_mode_operand")
    if category == "item_found_label" and source == "ECU":
        return _preserved("technical_acronym")
    if category == "system.currencyUnit" and source == "G":
        return _preserved("currency_abbreviation")
    return None


def _iter_drafts(drafts: Path) -> list[Path]:
    return sorted(drafts.rglob("*.jsonl"))


def audit_translation(canonical: Path = DEFAULT_CANONICAL,
                      drafts: Path = DEFAULT_DRAFTS) -> dict[str, Any]:
    canonical = canonical.resolve()
    drafts = drafts.resolve()
    with tempfile.TemporaryDirectory(prefix=".coverage-audit-", dir=TRANSLATION) as tmp:
        merged = Path(tmp) / "merged.jsonl"
        merge_report = merge_batches(canonical, _iter_drafts(drafts), merged, TRANSLATION)
        reasons: Counter[str] = Counter()
        by_category: Counter[str] = Counter()
        protected_by_category: Counter[str] = Counter()
        examples: dict[str, list[dict[str, str]]] = defaultdict(list)
        unresolved: list[dict[str, str]] = []
        for line in merged.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("translation", "").strip():
                continue
            category = row.get("category", "unknown")
            classified = classify_untranslated(row)
            if classified is None:
                unresolved.append({
                    "id": row["id"], "category": category,
                    "source_text": row.get("source_text", ""),
                })
                continue
            disposition, reason = classified
            if disposition != "source_preserved":
                unresolved.append({
                    "id": row["id"], "category": category,
                    "source_text": row.get("source_text", ""),
                })
                continue
            reasons[reason] += 1
            if reason == "explicit_keep_source_value_policy":
                protected_by_category[category] += 1
            else:
                by_category[category] += 1
            if len(examples[reason]) < 3:
                examples[reason].append({"id": row["id"], "source_text": row.get("source_text", "")})

        translated = merge_report["with_translation"]
        protected = merge_report["protected"]
        nonlocalized = sum(reasons.values()) - protected
        return {
            "schema": "tgo-translation-coverage-audit-v1",
            "status": "complete" if not unresolved else "incomplete",
            "canonical_record_count": merge_report["records"],
            "translated_record_count": translated,
            "explicitly_protected_record_count": protected,
            "source_preserved_nonlocalized_record_count": nonlocalized,
            "unresolved_translatable_record_count": len(unresolved),
            "draft_batch_count": len(_iter_drafts(drafts)),
            "source_preserved_by_category": dict(sorted(by_category.items())),
            "explicitly_protected_by_category": dict(sorted(protected_by_category.items())),
            "source_preserved_by_reason": dict(sorted(reasons.items())),
            "reason_examples": dict(sorted(examples.items())),
            "unresolved_records": unresolved,
            "scope_note": (
                "A complete result means every canonical record has a translation, an explicit keep-source policy, "
                "or an audited non-linguistic/proper-name/runtime/renderer rationale. It does not imply runtime "
                "visual QA; image/video-baked text remains excluded by owner decision."
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--drafts", type=Path, default=DEFAULT_DRAFTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit_translation(args.canonical, args.drafts)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k not in {"reason_examples", "unresolved_records"}},
                     ensure_ascii=False, indent=2))
    if report["status"] != "complete":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
