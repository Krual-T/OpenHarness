#!/usr/bin/env python3
"""Check whether stored project-memory objects are stale."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from project_memory_lib import (
    evaluate_memory_object_status,
    find_repo_root,
    load_memory_objects,
    parse_memory_kinds,
    rebuild_index,
    save_memory_object,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether project-memory objects went stale.")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--id", default="", help="Only inspect one memory object id")
    parser.add_argument("--kind", action="append", default=[], help="Only inspect one or more kinds")
    parser.add_argument("--write-status", action="store_true", help="Persist computed status back to YAML")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    kinds = parse_memory_kinds(args.kind)
    memory_objects = load_memory_objects(repo_root, kinds=kinds)
    rows: list[dict] = []
    for memory_object in memory_objects:
        if args.id and memory_object.get("id") != args.id:
            continue
        status, reasons = evaluate_memory_object_status(memory_object, repo_root)
        rows.append(
            {
                "id": memory_object.get("id"),
                "kind": memory_object.get("kind"),
                "title": memory_object.get("title"),
                "status": status,
                "reasons": reasons,
                "file": str(Path(memory_object["_path"]).resolve().relative_to(repo_root.resolve())),
            }
        )
        if args.write_status:
            updated_object = dict(memory_object)
            updated_object["health_status"] = status
            updated_object["health_checked_at"] = utc_now_iso()
            updated_object["updated_at"] = utc_now_iso()
            if reasons:
                updated_object["stale_reasons"] = reasons
            else:
                updated_object.pop("stale_reasons", None)
            save_memory_object(repo_root, updated_object)
    rebuild_index(repo_root)
    if args.as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("No memory objects found.")
        return
    for row in rows:
        reasons = ", ".join(row["reasons"]) or "-"
        print(f"[{row['kind']}] {row['id']} status={row['status']} file={row['file']}")
        print(f"  title: {row['title']}")
        print(f"  reasons: {reasons}")


if __name__ == "__main__":
    main()
