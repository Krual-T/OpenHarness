#!/usr/bin/env python3
"""Save or update a repo-local decision under .project-memory/."""

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
    save_decision,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a validated project-memory decision.")
    parser.add_argument("decision_id", help="Stable decision identifier")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--title", default="", help="Decision title")
    parser.add_argument("--summary", default="", help="Decision summary")
    parser.add_argument("--question", default="", help="Decision question")
    parser.add_argument("--decision", default="", help="Chosen decision")
    parser.add_argument("--rationale", default="", help="Decision rationale")
    parser.add_argument("--alias", action="append", default=[], help="Prompt variant for this decision")
    parser.add_argument("--tag", action="append", default=[], help="Decision tag")
    parser.add_argument("--alternative", action="append", default=[], help="Considered alternative")
    parser.add_argument("--consequence", action="append", default=[], help="Known consequence")
    parser.add_argument("--revisit-when", action="append", default=[], help="Condition that should trigger re-evaluation")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence file path")
    parser.add_argument("--note", action="append", default=[], help="Free-form note")
    parser.add_argument("--status", default="", help="Stored status override")
    parser.add_argument("--confidence", type=float, default=None, help="Confidence score override")
    parser.add_argument("--owner", default="", help="Owning team or person")
    parser.add_argument("--branch", default="", help="Scope branch override")
    parser.add_argument("--review-after", default="", help="Date after which this decision should be reviewed")
    parser.add_argument("--valid-until", default="", help="Date after which this decision is no longer trusted")
    parser.add_argument("--superseded-by", default="", help="Decision id that supersedes this one")
    parser.add_argument("--verified-commit", default="", help="Verified commit override")
    parser.add_argument(
        "--allow-alias-reassign",
        action="store_true",
        help="Allow aliases to move from another object to this decision",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    ensure_memory_layout(repo_root)
    existing = load_memory_object(repo_root, "decision", args.decision_id)
    title = args.title.strip() or str(existing.get("title", "")).strip()
    if not title:
        raise ProjectMemoryError("--title is required when creating a new decision")

    branch = args.branch.strip() or str((existing.get("scope") or {}).get("branch", "")).strip()
    if not branch:
        branch = current_branch(repo_root)
    verified_commit = args.verified_commit.strip() or str(existing.get("last_verified_commit", "")).strip()
    if not verified_commit:
        verified_commit = current_commit(repo_root)

    decision: dict[str, Any] = dict(existing)
    decision["id"] = args.decision_id
    decision["title"] = title
    decision["summary"] = args.summary.strip() or str(existing.get("summary", "")).strip()
    decision["question"] = args.question.strip() or str(existing.get("question", "")).strip()
    decision["decision"] = args.decision.strip() or str(existing.get("decision", "")).strip()
    decision["rationale"] = args.rationale.strip() or str(existing.get("rationale", "")).strip()
    decision["intent_aliases"] = merge_string_lists(existing.get("intent_aliases"), args.alias)
    decision["tags"] = merge_string_lists(existing.get("tags"), args.tag)
    decision["alternatives"] = merge_string_lists(existing.get("alternatives"), args.alternative)
    decision["consequences"] = merge_string_lists(existing.get("consequences"), args.consequence)
    decision["revisit_when"] = merge_string_lists(existing.get("revisit_when"), args.revisit_when)
    decision["notes"] = merge_string_lists(existing.get("notes"), args.note)
    decision["evidence"] = [
        *[
            item
            for item in existing.get("evidence") or []
            if isinstance(item, dict) and str(item.get("path", "")).strip()
        ],
        *[{"path": item, "kind": "file"} for item in args.evidence if item.strip()],
    ]
    decision["scope"] = {
        "repo": repo_root.name,
        "branch": branch,
    }
    if args.owner.strip():
        decision["owner"] = args.owner.strip()
    elif existing.get("owner"):
        decision["owner"] = str(existing["owner"]).strip()
    decision["status"] = args.status.strip() or str(existing.get("status", "reviewed"))
    decision["confidence"] = (
        float(args.confidence)
        if args.confidence is not None
        else float(existing.get("confidence", 0.8))
    )
    decision["review_after"] = args.review_after.strip() or str(existing.get("review_after", "")).strip()
    decision["valid_until"] = args.valid_until.strip() or str(existing.get("valid_until", "")).strip()
    decision["superseded_by"] = args.superseded_by.strip() or str(existing.get("superseded_by", "")).strip()
    decision["last_verified_commit"] = verified_commit
    decision["created_at"] = str(existing.get("created_at", "")).strip() or utc_now_iso()
    decision["updated_at"] = utc_now_iso()

    saved_path = save_decision(
        repo_root,
        decision,
        allow_alias_reassign=args.allow_alias_reassign,
    )
    print(f"Saved decision: {saved_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
