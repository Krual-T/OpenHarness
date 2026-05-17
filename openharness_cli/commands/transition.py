from __future__ import annotations

import argparse
from pathlib import Path

from ..display import output_state_hook
from ..workflow import execute_transition
from ..repository import load_config, resolve_task_package
from ..validate import validate_task_package


def cmd_transition(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        config = load_config(repo_root)
        package = resolve_task_package(repo_root, args.task, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    updated, errors = execute_transition(package, args.target_status)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if updated is not None:
        validation_errors = validate_task_package(updated)
        if validation_errors:
            for error in validation_errors:
                print(f"ERROR: {error}")
            return 1
        target = updated.current_status
        print(f"Transitioned {package.task_id} from `{package.current_status}` to `{target}`")
        output_state_hook(repo_root, target)
    elif args.target_status == "archived":
        print(f"Archived task package: {package.task_id} -> {config.archived_task_packages_root / package.name}")
        output_state_hook(repo_root, "archived")
    else:
        print(f"{package.task_id} already in `{package.current_status}`")
    return 0
