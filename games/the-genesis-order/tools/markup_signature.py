#!/usr/bin/env python3
"""Proposed v2 markup signature for TGO, with a read-only impact report.

The immutable v1 signature (``export_translation.TOKEN_RE``) treats every
backslash word as a tag together with an optional bracketed argument. A
no-argument toggle such as ``\\fb`` written directly before the visible text is
therefore captured as ``\\fbCraft`` (tag glued to the first word) instead of
``\\fb``. Any Polish wording then fails the token comparison in
``apply_translation.validate_record``, so those records cannot be translated at
all while the v1 signature is enforced.

This module only *measures* the problem and offers an explicit alternative
tokenizer. It never writes to the canonical export and never relaxes
``validate_record``; switching the project to v2 requires an owner decision (see
``docs/ADR.md``, ADR 002).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from export_translation import EXTRA_CONTROL_RE, TOKEN_RE

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EXPORT = REPO_ROOT / "games/the-genesis-order/translation/export-v1"

# Tags that take no argument. Each one must be listed explicitly: the fix is a
# decision about the engine's markup, not a heuristic on arbitrary text.
NO_ARGUMENT_TAGS = ("\\fb",)

TOKEN_V2_RE = re.compile(
    "|".join(re.escape(tag) for tag in NO_ARGUMENT_TAGS) + "|" + TOKEN_RE.pattern
)


def tokens_v2(text: str) -> list[str]:
    """Markup tokens with no-argument tags kept separate from the following word."""
    return TOKEN_V2_RE.findall(text)


def preserves_v2_signature(source: str, translation: str) -> bool:
    """True when the translation keeps every v2 token and control sequence."""
    return (tokens_v2(translation) == tokens_v2(source)
            and EXTRA_CONTROL_RE.findall(translation) == EXTRA_CONTROL_RE.findall(source))


def load_canonical(path: Path) -> list[dict[str, Any]]:
    paths = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    if not paths:
        raise FileNotFoundError(f"No canonical JSONL found at {path}")
    rows: list[dict[str, Any]] = []
    for file in paths:
        with file.open(encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def signature_impact(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare the stored (v1) signature with the proposed v2 signature."""
    changed = []
    for row in rows:
        source = row["source_text"]
        if tokens_v2(source) != row["markup_tokens"]:
            changed.append({
                "id": row["id"],
                "category": row["category"],
                "source_text": source,
                "v1_tokens": row["markup_tokens"],
                "v2_tokens": tokens_v2(source),
            })
    return {
        "records": len(rows),
        "v1_v2_identical": len(rows) - len(changed),
        "changed_records": len(changed),
        "changed_ids": sorted(item["id"] for item in changed),
        "changed_examples": changed[:5],
        "changed_categories": sorted({item["category"] for item in changed}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, default=DEFAULT_EXPORT)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report = signature_impact(load_canonical(args.canonical))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({key: report[key] for key in
                      ("records", "v1_v2_identical", "changed_records",
                       "changed_categories", "changed_ids")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
