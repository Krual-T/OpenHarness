from __future__ import annotations

import argparse
import json
from pathlib import Path

from .constants import ACTIVE_STATUSES, VERIFYABLE_STATUSES
from .lifecycle import (
    _archive_task_package,
    _build_transition_candidate,
    _check_archive_preconditions,
    _ensure_transition_allowed,
    _record_verification_artifact,
    _save_package_status,
    describe_stage,
)
from .models import TaskScaffoldRequest
from .repository import (
    _utc_timestamp,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    humanize_task_name,
    load_manifest,
    resolve_task_package,
    summarize_task_package,
)
from .validation import validate_task_package
from . import lifecycle


def cmd_bootstrap(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_task_packages(repo_root, manifest)
    if not args.all:
        packages = [package for package in packages if package.status_name in ACTIVE_STATUSES]
    if args.json:
        print(
            json.dumps(
                {
                    "repo": str(repo_root),
                    "manifest": str(manifest.path),
                    "task_packages_root": str(manifest.task_packages_root),
                    "archived_task_packages_root": str(manifest.archived_task_packages_root),
                    "task_packages": [
                        {
                            "id": package.task_id,
                            "name": package.name,
                            "title": package.title,
                            "status": package.status_name,
                            "summary": package.summary,
                            "owner": package.owner,
                            "root": str(package.root),
                            "required_commands": list(package.required_commands),
                            "required_scenarios": list(package.required_scenarios),
                            **describe_stage(package),
                        }
                        for package in packages
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    print(f"Harness manifest: {manifest.path}")
    print(f"Task package root: {manifest.task_packages_root}")
    if not packages:
        print("No matching task packages found.")
        return 0
    print("Active task packages:" if not args.all else "Task packages:")
    for package in packages:
        stage = describe_stage(package)
        print(f"- {summarize_task_package(package)}")
        print(f"  current stage: `{stage['current_stage']}` - {stage['current_stage_description']}")
        print(f"  next stage: `{stage['next_stage']}`" if stage["next_stage"] else "  next stage: none")
        print(f"  next step: {stage['next_step']}")
        if package.required_commands:
            print(f"  verify commands: {', '.join(package.required_commands)}")
        if package.required_scenarios:
            print(f"  scenarios: {', '.join(package.required_scenarios)}")
    return 0


def cmd_check_tasks(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_task_packages(repo_root, manifest)
    errors: list[str] = []
    if not packages:
        errors.append(
            f"no task packages found under {manifest.task_packages_root} or {manifest.archived_task_packages_root}"
        )
    duplicate_task_ids = find_duplicate_task_ids(packages)
    for task_id, duplicates in sorted(duplicate_task_ids.items()):
        roots = ", ".join(str(package.root) for package in duplicates)
        errors.append(f"duplicate task id `{task_id}` found in: {roots}")
    for package in packages:
        errors.extend(validate_task_package(package))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Validated {len(packages)} task package(s) under "
        f"{manifest.task_packages_root} and {manifest.archived_task_packages_root}"
    )
    return 0


def cmd_new_task(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    legacy_task_id = str(getattr(args, "legacy_task_id", "") or "").strip()
    legacy_title = str(getattr(args, "legacy_title", "") or "").strip()
    explicit_task_id = str(getattr(args, "task_id", "") or "").strip()
    explicit_title = str(getattr(args, "title", "") or "").strip()
    auto_id = bool(getattr(args, "auto_id", False))

    if auto_id and (explicit_task_id or legacy_task_id):
        print("ERROR: `--auto-id` cannot be combined with an explicit task id")
        return 1

    task_id = explicit_task_id or legacy_task_id
    if auto_id:
        task_id = allocate_next_task_id(repo_root)
    if not task_id:
        print("ERROR: new-task requires either an explicit task id or `--auto-id`")
        return 1

    title = explicit_title or legacy_title or humanize_task_name(args.task_name)
    task_root = create_task_package(
        TaskScaffoldRequest(
            repo_root=repo_root,
            task_name=args.task_name,
            task_id=task_id,
            title=title,
            owner=args.owner,
            summary=args.summary,
            status=args.status,
        )
    )
    print(f"Created task package: {task_root}")
    print(f"Task id: {task_id}")
    print(f"Title: {title}")
    return 0


def cmd_transition(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    try:
        package = resolve_task_package(repo_root, args.task, manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    transition_errors = _ensure_transition_allowed(package, args.target_status)
    if transition_errors:
        for error in transition_errors:
            print(f"ERROR: {error}")
        return 1
    if args.target_status == package.status_name:
        print(f"{package.task_id} already in `{package.status_name}`")
        return 0
    if args.target_status == "archived":
        precondition_errors = _check_archive_preconditions(package)
        if precondition_errors:
            for error in precondition_errors:
                print(f"ERROR: {error}")
            return 1
        archived_ok, detail = _archive_task_package(package)
        if not archived_ok:
            print(f"ERROR: {detail}")
            return 1
        print(f"Archived task package: {package.task_id} -> {manifest.archived_task_packages_root / package.name}")
        if detail:
            print(detail)
        return 0

    candidate = _build_transition_candidate(package, args.target_status)
    errors = validate_task_package(candidate)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    _save_package_status(package, candidate.status)
    print(f"Transitioned {package.task_id} from `{package.status_name}` to `{args.target_status}`")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_task_packages(repo_root, manifest)
    errors: list[str] = []
    if not packages:
        errors.append(
            f"no task packages found under {manifest.task_packages_root} or {manifest.archived_task_packages_root}"
        )
    for package in packages:
        errors.extend(validate_task_package(package))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if getattr(args, "check_tasks_only", False):
        return 0
    if args.design:
        packages = [package for package in packages if package.name == args.design or package.task_id == args.design]
    else:
        packages = [package for package in packages if package.status_name in VERIFYABLE_STATUSES]
    if not packages:
        print("No matching task packages to verify.")
        return 0
    saw_insufficient_verification = False
    for package in packages:
        print(f"== Verifying {package.task_id} {package.title} ==")
        started_at = _utc_timestamp()
        command_results: list[dict[str, object]] = []
        overall_result = "passed"
        for command in package.required_commands:
            exit_code = lifecycle._run_command(repo_root, command)
            command_results.append({"command": command, "exit_code": exit_code})
            if exit_code != 0:
                overall_result = "failed"
                artifact_path = _record_verification_artifact(
                    package,
                    started_at=started_at,
                    finished_at=_utc_timestamp(),
                    overall_result=overall_result,
                    command_results=command_results,
                )
                print(f"Recorded verification artifact: {artifact_path}")
                return 1
        if package.required_scenarios:
            print(
                "Declared manual scenarios "
                f"(not executed automatically by this CLI): {', '.join(package.required_scenarios)}"
            )
        if not package.required_commands and not package.required_scenarios:
            print(
                "ERROR: insufficient verification for "
                f"{package.task_id} {package.title}: "
                "No command-backed verification or manual scenarios declared."
            )
            overall_result = "insufficient_verification"
            saw_insufficient_verification = True
        artifact_path = _record_verification_artifact(
            package,
            started_at=started_at,
            finished_at=_utc_timestamp(),
            overall_result=overall_result,
            command_results=command_results,
        )
        print(f"Recorded verification artifact: {artifact_path}")
    if saw_insufficient_verification:
        return 1
    return 0
