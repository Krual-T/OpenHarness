#!/usr/bin/env python3
"""Save or update a repo-local workflow under .project-memory/."""

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
    save_workflow,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a validated project-memory workflow.")
    parser.add_argument("workflow_id", help="Stable workflow identifier")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--title", default="", help="Workflow title")
    parser.add_argument("--summary", default="", help="Workflow summary")
    parser.add_argument("--alias", action="append", default=[], help="Prompt variant for this workflow")
    parser.add_argument("--tag", action="append", default=[], help="Workflow tag")
    parser.add_argument("--step", action="append", default=[], help="Workflow step")
    parser.add_argument("--entrypoint", action="append", default=[], help="Entrypoint file or symbol")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence file path")
    parser.add_argument("--note", action="append", default=[], help="Free-form note")
    parser.add_argument("--status", default="", help="Stored status override")
    parser.add_argument("--confidence", type=float, default=None, help="Confidence score override")
    parser.add_argument("--owner", default="", help="Owning team or person")
    parser.add_argument("--branch", default="", help="Scope branch override")
    parser.add_argument("--review-after", default="", help="Date after which this workflow should be reviewed")
    parser.add_argument("--valid-until", default="", help="Date after which this workflow is no longer trusted")
    parser.add_argument("--verified-commit", default="", help="Verified commit override")
    parser.add_argument(
        "--allow-alias-reassign",
        action="store_true",
        help="Allow aliases to move from another object to this workflow",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    ensure_memory_layout(repo_root)
    existing = load_memory_object(repo_root, "workflow", args.workflow_id)
    title = args.title.strip() or str(existing.get("title", "")).strip()
    if not title:
        raise ProjectMemoryError("--title is required when creating a new workflow")

    branch = args.branch.strip() or str((existing.get("scope") or {}).get("branch", "")).strip()
    if not branch:
        branch = current_branch(repo_root)
    verified_commit = args.verified_commit.strip() or str(existing.get("last_verified_commit", "")).strip()
    if not verified_commit:
        verified_commit = current_commit(repo_root)

    workflow: dict[str, Any] = dict(existing)
    workflow["id"] = args.workflow_id
    workflow["title"] = title
    workflow["summary"] = args.summary.strip() or str(existing.get("summary", "")).strip()
    workflow["intent_aliases"] = merge_string_lists(existing.get("intent_aliases"), args.alias)
    workflow["tags"] = merge_string_lists(existing.get("tags"), args.tag)
    workflow["steps"] = merge_string_lists(existing.get("steps"), args.step)
    workflow["entrypoints"] = merge_string_lists(existing.get("entrypoints"), args.entrypoint)
    workflow["notes"] = merge_string_lists(existing.get("notes"), args.note)
    workflow["evidence"] = [
        *[
            item
            for item in existing.get("evidence") or []
            if isinstance(item, dict) and str(item.get("path", "")).strip()
        ],
        *[{"path": item, "kind": "file"} for item in args.evidence if item.strip()],
    ]
    workflow["scope"] = {
        "repo": repo_root.name,
        "branch": branch,
    }
    if args.owner.strip():
        workflow["owner"] = args.owner.strip()
    elif existing.get("owner"):
        workflow["owner"] = str(existing["owner"]).strip()
    workflow["status"] = args.status.strip() or str(existing.get("status", "reviewed"))
    workflow["confidence"] = (
        float(args.confidence)
        if args.confidence is not None
        else float(existing.get("confidence", 0.8))
    )
    workflow["review_after"] = args.review_after.strip() or str(existing.get("review_after", "")).strip()
    workflow["valid_until"] = args.valid_until.strip() or str(existing.get("valid_until", "")).strip()
    workflow["last_verified_commit"] = verified_commit
    workflow["created_at"] = str(existing.get("created_at", "")).strip() or utc_now_iso()
    workflow["updated_at"] = utc_now_iso()

    saved_path = save_workflow(
        repo_root,
        workflow,
        allow_alias_reassign=args.allow_alias_reassign,
    )
    print(f"Saved workflow: {saved_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
