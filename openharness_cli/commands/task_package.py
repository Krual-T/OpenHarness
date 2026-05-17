from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from ..models import CreateTaskInput, TaskStatus
from ..workflows import ACTIVE_STATUSES
from ..display import describe_stage, output_state_hook
from ..repository import (
    create_task_package, create_task_package_with_auto_id,
    discover_task_packages, humanize_task_name,
    summarize_task_package,
)

def cmd_task_package_list(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        packages = discover_task_packages(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    author_entry_path = repo_root / "skills" / "using-openharness" / "references" / "author-entry.md"
    author_entry: Optional[dict[str, str]] = None
    if author_entry_path.exists():
        author_entry = {"path": str(author_entry_path), "summary": "Chinese-first author entry for task-package writing guidance."}
    if not args.all:
        packages = [p for p in packages if p.current_status in ACTIVE_STATUSES]
    if args.json:
        cfg = packages[0].config if packages else None
        task_packages_root = str(cfg.task_packages_root) if cfg else str(repo_root / "docs" / "task-packages")
        archived_root = str(cfg.archived_task_packages_root) if cfg else str(repo_root / "docs" / "archived" / "task-packages")
        payload = {
            "repo": str(repo_root),
            "task_packages_root": task_packages_root,
            "archived_task_packages_root": archived_root,
            "task_packages": [
                {
                    "id": p.task_id, "name": p.name, "title": p.title,
                    "status": p.current_status, "summary": p.summary,
                    "owner": p.owner, "root": str(p.root),
                    **describe_stage(p),
                }
                for p in packages
            ],
        }
        if author_entry is not None:
            payload["author_entry"] = author_entry
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if author_entry is not None:
        print(f"author entry: {author_entry['path']}")
    if not packages:
        print("No matching task packages found.")
        return 0
    print("Active task packages:" if not args.all else "Task packages:")
    for p in packages:
        stage = describe_stage(p)
        print(f"- {summarize_task_package(p)}")
        print(f"  current stage: `{stage['current_stage']}` - {stage['current_stage_description']}")
        print(f"  next stage: `{stage['next_stage']}`" if stage["next_stage"] else "  next stage: none")
        print(f"  next step: {stage['next_step']}")

    proposing = [p for p in packages if p.current_status == "proposing"]
    if proposing:
        print("\n" + "=" * 60, flush=True)
        for p in proposing:
            print(f"\n## Task: {p.task_id} {p.title}", flush=True)
            output_state_hook(repo_root, "proposing")
            req_path = p.root / "01-requirements.md"
            if req_path.exists():
                print(f"\n--- Current 01-requirements.md ({p.task_id}) ---", flush=True)
                print(req_path.read_text(encoding="utf-8"), flush=True)
                print(f"--- END: 01-requirements.md ({p.task_id}) ---", flush=True)

    return 0


def cmd_task_package_new(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    explicit_task_id = str(getattr(args, "task_id", "") or "").strip()
    explicit_title = str(getattr(args, "title", "") or "").strip()
    auto_id = bool(getattr(args, "auto_id", False))
    if auto_id and explicit_task_id:
        print("ERROR: `--auto-id` cannot be combined with an explicit task id")
        return 1
    task_id = explicit_task_id
    if not task_id and not auto_id:
        print("ERROR: new-task requires either an explicit task id or `--auto-id`")
        return 1
    owner = args.owner
    title = explicit_title or humanize_task_name(args.task_name)
    try:
        if auto_id:
            task_root, task_id = create_task_package_with_auto_id(
                repo_root=repo_root, task_name=args.task_name, title=title,
                owner=owner, summary=args.summary, status=args.status,
            )
        else:
            task_root = create_task_package(
                CreateTaskInput(
                    repo_root=repo_root, task_name=args.task_name, task_id=task_id,
                    title=title, owner=owner, summary=args.summary,
                    status=TaskStatus(args.status) if args.status else TaskStatus.PROPOSING,
                )
            )
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Created task package: {task_root}")
    print(f"Task id: {task_id}")
    print(f"Title: {title}")
    print(f"Current status: {args.status}")
    output_state_hook(repo_root, args.status if args.status in ACTIVE_STATUSES else "proposing")
    print(f"\n完成后执行：openharness transition {task_id} requirements_designed")
    return 0
