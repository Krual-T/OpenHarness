from __future__ import annotations

import argparse
from pathlib import Path

from ..repository import discover_task_packages, find_duplicate_task_ids, load_config
from ..validate import validate_task_package


def cmd_check_tasks(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        config = load_config(repo_root)
        packages = discover_task_packages(repo_root, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errors: list[str] = []
    if not packages:
        errors.append(f"no task packages found under {config.task_packages_root} or {config.archived_task_packages_root}")
    duplicate_task_ids = find_duplicate_task_ids(packages)
    for task_id, duplicates in sorted(duplicate_task_ids.items()):
        roots = ", ".join(str(p.root) for p in duplicates)
        errors.append(f"duplicate task id `{task_id}` found in: {roots}")
    for p in packages:
        errors.extend(validate_task_package(p))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {len(packages)} task package(s) under {config.task_packages_root} and {config.archived_task_packages_root}")
    return 0
