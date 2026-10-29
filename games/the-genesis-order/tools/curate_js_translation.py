#!/usr/bin/env python3
"""Promote explicitly reviewed TGO JS candidates into private translation JSONL.

The checked-in decision file contains candidate IDs and content-free evidence,
not game strings. Source text is read only from ignored google_drive/ files.
No JavaScript is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from export_translation import REPO_ROOT, SOURCE_ROOT, record

DECISIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "js_review_decisions.json"
DEFAULT_CANDIDATES = SOURCE_ROOT / "translation" / "review-v2" / "js_text_candidates.jsonl"
DEFAULT_OUT = SOURCE_ROOT / "translation" / "export-v1" / "reviewed_js_ui.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_candidates(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise ValueError(f"Invalid candidate record at {path}:{line_no}")
            if row["id"] in result:
                raise ValueError(f"Duplicate candidate ID: {row['id']}")
            result[row["id"]] = row
    return result


def curate(candidates_path: Path, output_path: Path, decisions_path: Path = DECISIONS_PATH) -> dict[str, Any]:
    policy = json.loads(decisions_path.read_text(encoding="utf-8"))
    if policy.get("schema") != "tgo-js-review-decisions-v1":
        raise ValueError("Unsupported JS review decision schema")
    decisions = policy.get("decisions")
    deferred = policy.get("deferred", {})
    excluded = policy.get("excluded", {})
    exclusion_reasons = policy.get("exclusion_reasons", {})
    if (not isinstance(decisions, dict) or not decisions or not isinstance(deferred, dict)
            or not isinstance(excluded, dict) or not isinstance(exclusion_reasons, dict)):
        raise ValueError("JS review decision file has no valid disposition maps")
    candidates = load_candidates(candidates_path)
    dispositions = [set(decisions), set(deferred), set(excluded)]
    unknown = sorted(set.union(*dispositions) - candidates.keys())
    if unknown:
        raise ValueError(f"Reviewed candidate IDs absent from scan: {unknown[:5]}")
    for i, left in enumerate(dispositions):
        for right in dispositions[i + 1:]:
            overlap = left & right
            if overlap:
                raise ValueError(f"Candidate has conflicting review dispositions: {sorted(overlap)[:5]}")
    if any(not isinstance(reason, str) or not reason.strip() for reason in deferred.values()):
        raise ValueError("Deferred review entries require content-free reasons")
    if any(not isinstance(code, str) or code not in exclusion_reasons for code in excluded.values()):
        raise ValueError("Excluded review entries require a defined content-free reason code")

    rows = []
    source_hashes: dict[str, str] = {}
    for candidate_id, candidate in candidates.items():
        source = candidate.get("source", {})
        rel = source.get("file")
        if not isinstance(rel, str) or source.get("locator", {}).get("file") != rel:
            raise ValueError(f"Invalid source locator for candidate {candidate_id}")
        source_path = (SOURCE_ROOT / rel).resolve()
        if SOURCE_ROOT.resolve() not in source_path.parents:
            raise ValueError(f"Unsafe source path for candidate {candidate_id}")
        current_hash = sha256(source_path)
        if current_hash != source.get("sha256"):
            raise ValueError(f"Candidate source hash is stale for {candidate_id}")
        if rel in source_hashes and source_hashes[rel] != current_hash:
            raise ValueError(f"Candidate records disagree on source hash for {rel}")
        source_hashes[rel] = current_hash

    unreviewed_ids = candidates.keys() - set.union(*dispositions)

    for candidate_id, decision in decisions.items():
        candidate = candidates[candidate_id]
        source = candidate.get("source", {})
        locator = source.get("locator", {})
        rel = source.get("file")
        current_hash = source_hashes[rel]
        if candidate.get("classification") != "unreviewed_candidate_not_translation":
            raise ValueError(f"Input candidate is unexpectedly pre-classified: {candidate_id}")
        if decision.get("classification") != "confirmed_ui_text":
            raise ValueError(f"Unsupported promotion decision for {candidate_id}")
        if not isinstance(candidate.get("source_text"), str) or not candidate["source_text"].strip():
            raise ValueError(f"Reviewed candidate has no source text: {candidate_id}")
        if candidate.get("category") == "js_display_literal_candidate":
            if candidate.get("context", {}).get("plugin_status") not in {"enabled", "engine_source"}:
                raise ValueError(f"Static UI literal is not from an enabled plugin/engine source: {candidate_id}")
        if candidate.get("category") == "plugin_parameter_candidate":
            if candidate.get("context", {}).get("plugin_status") != "enabled":
                raise ValueError(f"Plugin parameter is not active: {candidate_id}")

        canonical_category = decision["category"]
        context = dict(candidate.get("context") or {})
        context.update({"review_candidate_id": candidate_id, "review_evidence": decision["reason"]})
        if decision.get("translation_policy") is not None:
            if decision["translation_policy"] != "keep_source_value":
                raise ValueError(f"Unsupported translation policy for {candidate_id}")
            context["translation_policy"] = decision["translation_policy"]
        structure = {
            "candidate_kind": candidate["category"],
            "source_locator_kind": "static_js_string" if "char_offset" in locator else "plugin_parameter_json_string",
            "source_literal_kind": (candidate.get("context") or {}).get("literal_kind")
                                  if "char_offset" in locator else "json_string",
        }
        rows.append(record(
            category=canonical_category,
            status="confirmed_ui_text",
            text=candidate["source_text"],
            source_file=rel,
            source_hash=current_hash,
            locator=locator,
            context=context,
            structure=structure,
        ))

    rows.sort(key=lambda row: (row["source"]["file"], row["id"]))
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Canonical UI record IDs are not unique")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp = output_path.with_name(output_path.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, output_path)
    manifest = {
        "schema": "tgo-reviewed-js-ui-export-v1",
        "records": len(rows),
        "candidate_count": len(candidates),
        "confirmed_ui_candidates": len(decisions),
        "excluded_candidates": len(excluded),
        "excluded_reason_counts": dict(sorted(Counter(excluded.values()).items())),
        "deferred_candidates": len(deferred),
        "unreviewed_candidates": len(unreviewed_ids),
        "complete_for_candidate_scan": not unreviewed_ids,
        "source_files": len(source_hashes),
        "categories": dict(sorted(Counter(row["category"] for row in rows).items())),
        "source_file_hashes": dict(sorted(source_hashes.items())),
        "output_sha256": sha256(output_path),
        "output_file": output_path.name,
        "review_policy_schema": policy["schema"],
        "review_scope": policy.get("review_scope", {}),
    }
    manifest_path = output_path.with_name(output_path.stem + "_manifest.json")
    temporary_manifest = manifest_path.with_name(manifest_path.name + ".tmp")
    with temporary_manifest.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary_manifest, manifest_path)
    return {
        "records": len(rows),
        "candidate_count": len(candidates),
        "confirmed_ui_candidates": len(decisions),
        "excluded_candidates": len(excluded),
        "deferred_candidates": len(deferred),
        "unreviewed_candidates": len(unreviewed_ids),
        "source_files": len(source_hashes),
        "categories": manifest["categories"],
        "output_sha256": manifest["output_sha256"],
        "output_path": str(output_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--decisions", type=Path, default=DECISIONS_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    private_root = (REPO_ROOT / "google_drive").resolve()
    output = args.out.resolve()
    if output != private_root and private_root not in output.parents:
        raise ValueError("Refusing to write source text outside ignored google_drive/")
    report = curate(args.candidates, output, args.decisions)
    print(
        "Candidate dispositions: "
        f"{report['candidate_count']} total; {report['confirmed_ui_candidates']} confirmed UI; "
        f"{report['excluded_candidates']} excluded by content-free rule; "
        f"{report['deferred_candidates']} deferred; {report['unreviewed_candidates']} unreviewed."
    )
    print(f"Reviewed UI records: {report['records']}; source files hash-verified: {report['source_files']}")
    print(f"Categories: {json.dumps(report['categories'], sort_keys=True)}")
    print("Source strings are written only under ignored google_drive/; JavaScript was not executed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
