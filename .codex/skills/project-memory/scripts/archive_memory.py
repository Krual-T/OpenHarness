#!/usr/bin/env python3
"""Archive, deprecate, or invalidate a repo-local memory object."""

from __future__ import annotations

import argparse
from pathlib import Path

from project_memory_lib import archive_memory_object, find_repo_root, supported_memory_kinds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive or deprecate a project-memory object.")
    parser.add_argument("object_id", help="Memory object id to archive")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--kind", choices=supported_memory_kinds(), default=None, help="Object kind when id is ambiguous")
    parser.add_argument(
        "--status",
        choices=("archived", "deprecated", "invalid"),
        default="archived",
        help="Inactive status to assign",
    )
    parser.add_argument("--reason", required=True, help="Why this object is being archived or deprecated")
    parser.add_argument("--archived-by", default="codex", help="Who archived this object")
    parser.add_argument("--superseded-by", default="", help="Replacement object id")
    parser.add_argument("--note", default="", help="Optional note appended to the object")
    parser.add_argument(
        "--move-aliases-to-superseded",
        action="store_true",
        help="Move current aliases to the superseding object",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    archived_path, replacement_path = archive_memory_object(
        repo_root,
        args.object_id,
        kind=args.kind,
        status=args.status,
        reason=args.reason,
        archived_by=args.archived_by,
        superseded_by=args.superseded_by,
        note=args.note,
        move_aliases_to_superseded=args.move_aliases_to_superseded,
    )
    print(f"Updated memory object: {archived_path.relative_to(repo_root)}")
    if replacement_path is not None:
        print(f"Moved aliases into: {replacement_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
