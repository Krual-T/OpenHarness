from __future__ import annotations

import argparse
import json
import os
import shlex
from pathlib import Path

from .constants import ACTIVE_STATUSES, VERIFYABLE_STATUSES
from .lifecycle import (
    _archive_task_package,
    _build_transition_candidate,
    _check_archive_preconditions,
    _ensure_transition_allowed,
    _record_verification_artifact,
    _run_command,
    _save_package_status,
    describe_stage,
)
from .models import TaskScaffoldRequest
from .repository import (
    _utc_timestamp,
    create_task_package, create_task_package_with_auto_id,
    discover_runtime_workflow_packages, discover_task_packages,
    find_duplicate_task_ids, humanize_task_name, load_config,
    resolve_runtime_workflow_package, resolve_runtime_workflow_script,
    resolve_task_package, summarize_task_package,
)
from .validation import validate_task_package

def _openharness_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _author_entry_info(repo_root: Path) -> dict[str, str] | None:
    author_entry = repo_root / "skills" / "using-openharness" / "references" / "author-entry.md"
    if not author_entry.exists():
        return None
    return {"path": str(author_entry), "summary": "Chinese-first author entry for task-package writing guidance."}


def cmd_bootstrap(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        config = load_config(repo_root)
        packages = discover_task_packages(repo_root, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    author_entry = _author_entry_info(repo_root)
    if not args.all:
        packages = [p for p in packages if p.status_name in ACTIVE_STATUSES]
    if args.json:
        payload = {
            "repo": str(repo_root),
            "task_packages_root": str(config.task_packages_root),
            "archived_task_packages_root": str(config.archived_task_packages_root),
            "task_packages": [
                {
                    "id": p.task_id, "name": p.name, "title": p.title,
                    "status": p.status_name, "summary": p.summary,
                    "owner": p.owner, "root": str(p.root),
                    "required_commands": list(p.required_commands),
                    "required_scenarios": list(p.required_scenarios),
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
        if p.required_commands:
            print(f"  verify commands: {', '.join(p.required_commands)}")
        if p.required_scenarios:
            print(f"  scenarios: {', '.join(p.required_scenarios)}")
    return 0


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


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    harness_root = repo_root / ".harness"
    harness_root.mkdir(parents=True, exist_ok=True)
    (harness_root / ".gitignore").write_text("*\n", encoding="utf-8")
    print(f"Initialized OpenHarness local directory: {harness_root}")
    return 0


def cmd_new_task(args: argparse.Namespace) -> int:
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
    title = explicit_title or humanize_task_name(args.task_name)
    try:
        if auto_id:
            task_root, task_id = create_task_package_with_auto_id(
                repo_root=repo_root, task_name=args.task_name, title=title,
                owner=args.owner, summary=args.summary, status=args.status,
            )
        else:
            task_root = create_task_package(
                TaskScaffoldRequest(
                    repo_root=repo_root, task_name=args.task_name, task_id=task_id,
                    title=title, owner=args.owner, summary=args.summary, status=args.status,
                )
            )
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Created task package: {task_root}")
    print(f"Task id: {task_id}")
    print(f"Title: {title}")
    return 0


def cmd_rwp(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    command = args.rwp_command
    try:
        if command == "list":
            packages = discover_runtime_workflow_packages(repo_root)
            if not packages:
                print("No runtime workflow packages found.")
                return 0
            for p in packages:
                rel_root = p.root.relative_to(repo_root)
                print(f"- {p.name} - {p.description}")
                print(f"  path: {rel_root}")
            return 0
        if command == "show":
            pkg = resolve_runtime_workflow_package(repo_root, args.workflow)
            print(pkg.workflow_path.read_text(encoding="utf-8"), end="")
            return 0
        if command == "run":
            script_path = resolve_runtime_workflow_script(repo_root, args.workflow, args.script)
            runtime_api_root = Path(__file__).resolve().parents[1]
            pythonpath = os.pathsep.join([
                str(runtime_api_root),
                *([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []),
            ])
            os.environ["PYTHONPATH"] = pythonpath
            command_line = shlex.join(["uv", "run", "python", str(script_path), *list(args.script_args)])
            return _run_command(repo_root, command_line)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"ERROR: unknown rwp command `{command}`")
    return 1


def cmd_transition(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        config = load_config(repo_root)
        package = resolve_task_package(repo_root, args.task, config)
    except (FileNotFoundError, ValueError) as exc:
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
        print(f"Archived task package: {package.task_id} -> {config.archived_task_packages_root / package.name}")
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
    try:
        config = load_config(repo_root)
        packages = discover_task_packages(repo_root, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errors: list[str] = []
    if not packages:
        errors.append(f"no task packages found under {config.task_packages_root} or {config.archived_task_packages_root}")
    for p in packages:
        errors.extend(validate_task_package(p))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if getattr(args, "check_tasks_only", False):
        return 0
    if args.design:
        packages = [p for p in packages if p.name == args.design or p.task_id == args.design]
    else:
        packages = [p for p in packages if p.status_name in VERIFYABLE_STATUSES]
    if not packages:
        print("No matching task packages to verify.")
        return 0
    saw_insufficient_verification = False
    for p in packages:
        print(f"== Verifying {p.task_id} {p.title} ==")
        started_at = _utc_timestamp()
        command_results: list[dict[str, object]] = []
        overall_result = "passed"
        for command in p.required_commands:
            exit_code = _run_command(repo_root, command)
            command_results.append({"command": command, "exit_code": exit_code})
            if exit_code != 0:
                overall_result = "failed"
                artifact_path = _record_verification_artifact(
                    p, started_at=started_at, finished_at=_utc_timestamp(),
                    overall_result=overall_result, command_results=command_results,
                )
                print(f"Recorded verification artifact: {artifact_path}")
                return 1
        if p.required_scenarios:
            print(f"Declared manual scenarios (not executed automatically by this CLI): {', '.join(p.required_scenarios)}")
        if not p.required_commands and not p.required_scenarios:
            print(f"ERROR: insufficient verification for {p.task_id} {p.title}: No command-backed verification or manual scenarios declared.")
            overall_result = "insufficient_verification"
            saw_insufficient_verification = True
        artifact_path = _record_verification_artifact(
            p, started_at=started_at, finished_at=_utc_timestamp(),
            overall_result=overall_result, command_results=command_results,
        )
        print(f"Recorded verification artifact: {artifact_path}")
    if saw_insufficient_verification:
        return 1
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    repo_root = _openharness_repo_root()
    if getattr(args, "force_sync", False):
        for command in ("git fetch --prune", "git reset --hard '@{u}'"):
            sync_result = _run_command(repo_root, command)
            if sync_result != 0:
                print(f"ERROR: force sync failed at `{command}`; refusing to continue with tool upgrade.")
                return 1
        print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    else:
        git_pull_result = _run_command(repo_root, "git pull")
        if git_pull_result != 0:
            print("ERROR: git pull failed; refusing to continue with tool upgrade.")
            return 1
    upgrade_result = _run_command(repo_root, "uv tool upgrade openharness")
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade openharness` failed.")
        return 1
    print(f"Updated OpenHarness from {repo_root}")
    return 0
