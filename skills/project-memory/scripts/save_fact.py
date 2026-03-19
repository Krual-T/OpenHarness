#!/usr/bin/env python3
"""Save or update a repo-local fact under .project-memory/."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from project_memory_lib import (
    ProjectMemoryError,
    current_branch,
    current_commit,
    ensure_memory_layout,
    find_repo_root,
    load_memory_object,
    merge_string_lists,
    save_fact,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a validated project-memory fact.")
    parser.add_argument("fact_id", help="Stable fact identifier")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--title", default="", help="Fact title")
    parser.add_argument("--summary", default="", help="Fact summary")
    parser.add_argument("--statement", default="", help="Canonical fact statement")
    parser.add_argument("--details", default="", help="Additional fact details")
    parser.add_argument("--alias", action="append", default=[], help="Prompt variant for this fact")
    parser.add_argument("--tag", action="append", default=[], help="Fact tag")
    parser.add_argument("--applies-to", action="append", default=[], help="Scope or subsystem this fact applies to")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence file path")
    parser.add_argument("--note", action="append", default=[], help="Free-form note")
    parser.add_argument("--status", default="", help="Stored status override")
    parser.add_argument("--confidence", type=float, default=None, help="Confidence score override")
    parser.add_argument("--owner", default="", help="Owning team or person")
    parser.add_argument("--branch", default="", help="Scope branch override")
    parser.add_argument("--review-after", default="", help="Date after which this fact should be reviewed")
    parser.add_argument("--valid-until", default="", help="Date after which this fact is no longer trusted")
    parser.add_argument("--verified-commit", default="", help="Verified commit override")
    parser.add_argument(
        "--allow-alias-reassign",
        action="store_true",
        help="Allow aliases to move from another object to this fact",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    ensure_memory_layout(repo_root)
    existing = load_memory_object(repo_root, "fact", args.fact_id)
    title = args.title.strip() or str(existing.get("title", "")).strip()
    if not title:
        raise ProjectMemoryError("--title is required when creating a new fact")

    branch = args.branch.strip() or str((existing.get("scope") or {}).get("branch", "")).strip()
    if not branch:
        branch = current_branch(repo_root)
    verified_commit = args.verified_commit.strip() or str(existing.get("last_verified_commit", "")).strip()
    if not verified_commit:
        verified_commit = current_commit(repo_root)

    fact: dict[str, Any] = dict(existing)
    fact["id"] = args.fact_id
    fact["title"] = title
    fact["summary"] = args.summary.strip() or str(existing.get("summary", "")).strip()
    fact["statement"] = args.statement.strip() or str(existing.get("statement", "")).strip()
    fact["details"] = args.details.strip() or str(existing.get("details", "")).strip()
    fact["intent_aliases"] = merge_string_lists(existing.get("intent_aliases"), args.alias)
    fact["tags"] = merge_string_lists(existing.get("tags"), args.tag)
    fact["applies_to"] = merge_string_lists(existing.get("applies_to"), args.applies_to)
    fact["notes"] = merge_string_lists(existing.get("notes"), args.note)
    fact["evidence"] = [
        *[
            item
            for item in existing.get("evidence") or []
            if isinstance(item, dict) and str(item.get("path", "")).strip()
        ],
        *[{"path": item, "kind": "file"} for item in args.evidence if item.strip()],
    ]
    fact["scope"] = {
        "repo": repo_root.name,
        "branch": branch,
    }
    if args.owner.strip():
        fact["owner"] = args.owner.strip()
    elif existing.get("owner"):
        fact["owner"] = str(existing["owner"]).strip()
    fact["status"] = args.status.strip() or str(existing.get("status", "reviewed"))
    fact["confidence"] = (
        float(args.confidence)
        if args.confidence is not None
        else float(existing.get("confidence", 0.8))
    )
    fact["review_after"] = args.review_after.strip() or str(existing.get("review_after", "")).strip()
    fact["valid_until"] = args.valid_until.strip() or str(existing.get("valid_until", "")).strip()
    fact["last_verified_commit"] = verified_commit
    fact["created_at"] = str(existing.get("created_at", "")).strip() or utc_now_iso()
    fact["updated_at"] = utc_now_iso()

    saved_path = save_fact(repo_root, fact, allow_alias_reassign=args.allow_alias_reassign)
    print(f"Saved fact: {saved_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
