#!/usr/bin/env python3
"""Query repo-local memory objects stored under .project-memory/."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from project_memory_lib import (
    DEFAULT_MIN_CONFIDENCE,
    DEFAULT_MIN_SCORE,
    find_repo_root,
    parse_memory_kinds,
    query_memory_objects,
    sync_index,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query repo-local project memory objects.")
    parser.add_argument("query", help="Question, alias, or phrase to search")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--kind", action="append", default=[], help="Limit to one or more kinds")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results")
    parser.add_argument(
        "--include-unusable",
        action="store_true",
        help="Include stale, review-due, low-confidence, and low-score matches",
    )
    parser.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE, help="Minimum reuse score")
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=DEFAULT_MIN_CONFIDENCE,
        help="Minimum confidence required for reuse",
    )
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def type_specific_lines(memory_object: dict) -> list[str]:
    kind = memory_object.get("kind", "workflow")
    if kind == "workflow":
        steps = ", ".join(memory_object.get("steps") or []) or "-"
        return [f"steps: {steps}"]
    if kind == "fact":
        statement = memory_object.get("statement", "-")
        applies_to = ", ".join(memory_object.get("applies_to") or []) or "-"
        return [f"statement: {statement}", f"applies_to: {applies_to}"]
    if kind == "decision":
        decision = memory_object.get("decision", "-")
        rationale = memory_object.get("rationale", "-")
        revisit_when = ", ".join(memory_object.get("revisit_when") or []) or "-"
        return [f"decision: {decision}", f"rationale: {rationale}", f"revisit_when: {revisit_when}"]
    return []


def render_text(matches: list[dict], repo_root: Path) -> None:
    if not matches:
        print("No matching memory objects found.")
        return
    for index, match in enumerate(matches, start=1):
        memory_object = match["object"]
        title = memory_object.get("title", "-")
        summary = memory_object.get("summary", "-")
        aliases = ", ".join(memory_object.get("intent_aliases") or []) or "-"
        evidence = ", ".join(item["path"] for item in memory_object.get("evidence") or []) or "-"
        file_path = Path(memory_object["_path"]).resolve().relative_to(repo_root.resolve())
        stale_text = ", ".join(match["stale_reasons"]) or "-"
        reasons = ", ".join(match["match_reasons"]) or "-"
        blockers = ", ".join(match["reuse_blockers"]) or "-"
        print(
            f"{index}. [{memory_object['kind']}] {memory_object['id']} score={match['score']} "
            f"status={match['effective_status']} reusable={match['reusable']} file={file_path.as_posix()}"
        )
        print(f"   title: {title}")
        print(f"   summary: {summary}")
        print(f"   aliases: {aliases}")
        for line in type_specific_lines(memory_object):
            print(f"   {line}")
        print(f"   evidence: {evidence}")
        print(f"   stale_reasons: {stale_text}")
        print(f"   match_reasons: {reasons}")
        print(f"   reuse_blockers: {blockers}")


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    kinds = parse_memory_kinds(args.kind)
    sync_index(repo_root)
    matches = query_memory_objects(
        repo_root,
        args.query,
        limit=args.limit,
        kinds=kinds,
        include_unusable=args.include_unusable,
        min_score=args.min_score,
        min_confidence=args.min_confidence,
    )
    if not matches and not args.include_unusable:
        blocked = query_memory_objects(
            repo_root,
            args.query,
            limit=args.limit,
            kinds=kinds,
            include_unusable=True,
            min_score=args.min_score,
            min_confidence=args.min_confidence,
        )
        if blocked:
            if args.as_json:
                print(
                    json.dumps(
                        {
                            "matches": [],
                            "blocked_candidate_count": len(blocked),
                            "message": "No reusable memory objects found. Rerun with --include-unusable to inspect blocked candidates.",
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                return
            print(
                f"No reusable memory objects found. {len(blocked)} blocked candidates exist; "
                "rerun with --include-unusable to inspect them."
            )
            return
    if args.as_json:
        payload = []
        for match in matches:
            memory_object = dict(match["object"])
            memory_object["_path"] = str(Path(memory_object["_path"]).resolve())
            payload.append(
                {
                    "object": memory_object,
                    "score": match["score"],
                    "effective_status": match["effective_status"],
                    "base_status": match["base_status"],
                    "reusable": match["reusable"],
                    "reuse_blockers": match["reuse_blockers"],
                    "stale_reasons": match["stale_reasons"],
                    "match_reasons": match["match_reasons"],
                }
            )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    render_text(matches, repo_root)


if __name__ == "__main__":
    main()
