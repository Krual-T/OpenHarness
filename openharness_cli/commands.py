from __future__ import annotations

import argparse
import json
import os
import shlex
from pathlib import Path

from .constants import ACTIVE_STATUSES
from .lifecycle import (
    _archive_task_package,
    _build_transition_candidate,
    _check_archive_preconditions,
    _ensure_transition_allowed,
    _output_state_hook,
    _resolve_gate_transition,
    _save_package_status,
    describe_stage,
)
from .models import TaskScaffoldRequest
from .repository import (
    _load_yaml, _utc_timestamp, _write_yaml,
    create_task_package, create_task_package_with_auto_id,
    discover_runtime_workflow_packages, discover_task_packages,
    find_duplicate_task_ids, get_git_author, humanize_task_name, load_config,
    resolve_runtime_workflow_package, resolve_runtime_workflow_script,
    resolve_task_package, summarize_task_package,
)
from .validation import validate_task_package

UPDATE_MODES = {"pull", "force-sync"}


def _openharness_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _project_settings_path(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "settings.yaml").resolve()


def _load_project_settings(repo_root: Path) -> dict[str, object]:
    path = _project_settings_path(repo_root)
    if not path.exists():
        return {}
    return _load_yaml(path)


def _save_project_settings(repo_root: Path, settings: dict[str, object]) -> None:
    path = _project_settings_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_yaml(path, settings)


def _set_default_update_mode(repo_root: Path, mode: str) -> None:
    settings = _load_project_settings(repo_root)
    update_settings = settings.setdefault("update", {})
    if not isinstance(update_settings, dict):
        raise ValueError(f"`update` settings must be a mapping in {_project_settings_path(repo_root)}")
    update_settings["default_mode"] = mode
    _save_project_settings(repo_root, settings)


def _configured_update_mode(repo_root: Path) -> str:
    settings = _load_project_settings(repo_root)
    update_settings = settings.get("update") or {}
    if not isinstance(update_settings, dict):
        raise ValueError(f"`update` settings must be a mapping in {_project_settings_path(repo_root)}")
    mode = str(update_settings.get("default_mode") or "").strip()
    if not mode:
        return "pull"
    if mode not in UPDATE_MODES:
        raise ValueError(
            f"invalid default update mode `{mode}` in {_project_settings_path(repo_root)}; "
            f"expected `pull` or `force-sync`"
        )
    return mode


def _resolve_update_mode(args: argparse.Namespace, repo_root: Path) -> str:
    if getattr(args, "force_sync", False):
        return "force-sync"
    mode = getattr(args, "mode", None)
    if mode:
        return str(mode)
    return _configured_update_mode(repo_root)


def _author_entry_info(repo_root: Path) -> dict[str, str] | None:
    author_entry = repo_root / "skills" / "using-openharness" / "references" / "author-entry.md"
    if not author_entry.exists():
        return None
    return {"path": str(author_entry), "summary": "Chinese-first author entry for task-package writing guidance."}


# ── task-package list ───────────────────────────────────────────────────────

def cmd_task_package_list(args: argparse.Namespace) -> int:
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

    # For proposing tasks, also output brainstorming skill + current 01 content
    proposing = [p for p in packages if p.status_name == "proposing"]
    if proposing:
        print("\n" + "=" * 60, flush=True)
        for p in proposing:
            print(f"\n## Task: {p.task_id} {p.title}", flush=True)
            _output_state_hook(repo_root, "proposing")
            req_path = p.root / "01-requirements.md"
            if req_path.exists():
                print(f"\n--- Current 01-requirements.md ({p.task_id}) ---", flush=True)
                print(req_path.read_text(encoding="utf-8"), flush=True)
                print(f"--- END: 01-requirements.md ({p.task_id}) ---", flush=True)

    return 0


# ── task-package new ────────────────────────────────────────────────────────

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
    if owner == "unassigned":
        owner = get_git_author(repo_root)
    title = explicit_title or humanize_task_name(args.task_name)
    try:
        if auto_id:
            task_root, task_id = create_task_package_with_auto_id(
                repo_root=repo_root, task_name=args.task_name, title=title,
                owner=owner, summary=args.summary, status=args.status,
            )
        else:
            task_root = create_task_package(
                TaskScaffoldRequest(
                    repo_root=repo_root, task_name=args.task_name, task_id=task_id,
                    title=title, owner=owner, summary=args.summary, status=args.status,
                )
            )
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Created task package: {task_root}")
    print(f"Task id: {task_id}")
    print(f"Title: {title}")
    print(f"Current status: {args.status}")
    # Output brainstorming instructions inline (O3)
    _output_state_hook(repo_root, args.status if args.status in ACTIVE_STATUSES else "proposing")
    print(f"\n完成后执行：openharness transition {task_id} requirements_designed")
    return 0


# ── transition ──────────────────────────────────────────────────────────────

def cmd_transition(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        config = load_config(repo_root)
        package = resolve_task_package(repo_root, args.task, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    target_status = args.target_status
    transition_errors = _ensure_transition_allowed(package, target_status)
    if transition_errors:
        for error in transition_errors:
            print(f"ERROR: {error}")
        return 1

    if target_status == package.status_name:
        print(f"{package.task_id} already in `{package.status_name}`")
        return 0

    # Gate auto-advance: resolve gate target to actual next state
    gate_next, gate_errors = _resolve_gate_transition(package, target_status)
    if gate_errors:
        for error in gate_errors:
            print(f"ERROR: {error}")
        return 1
    if gate_next is not None:
        print(f"Gate `{target_status}` → auto-advancing to `{gate_next}`")
        # Recurse with the resolved target
        args.target_status = gate_next
        return cmd_transition(args)

    if target_status == "archived":
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
        _output_state_hook(repo_root, "archived")
        return 0

    candidate = _build_transition_candidate(package, target_status)
    errors = validate_task_package(candidate)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    _save_package_status(package, candidate.status)
    print(f"Transitioned {package.task_id} from `{package.status_name}` to `{target_status}`")
    # Output the skill file for the new state (hook)
    _output_state_hook(repo_root, target_status)
    return 0


# ── check-tasks ─────────────────────────────────────────────────────────────

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
            import subprocess
            print(f"$ {command_line}")
            completed = subprocess.run(command_line, shell=True, cwd=repo_root)
            return completed.returncode
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"ERROR: unknown rwp command `{command}`")
    return 1


# ── writing-guide ───────────────────────────────────────────────────────────

_GUIDANCE_MAP: dict[str, str] = {
    "requirements": "skills/using-openharness/references/templates/task-package.01-requirements.md",
    "overview": "skills/using-openharness/references/templates/task-package.02-overview-design.md",
    "detailed": "skills/using-openharness/references/templates/task-package.03-detailed-design.md",
    "verification": "skills/using-openharness/references/templates/task-package.verification_design.md",
    "evidence": "skills/using-openharness/references/templates/task-package.evidence.md",
    "author-entry": "skills/using-openharness/references/author-entry.md",
}


def _resolve_writing_guide_path(repo_root: Path, name: str) -> Path | None:
    relative = _GUIDANCE_MAP.get(name)
    if not relative:
        return None
    path = (repo_root / relative).resolve()
    return path if path.exists() else None


def cmd_writing_guide(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    command = getattr(args, "writing_guide_command", "list")

    if command == "read":
        path = _resolve_writing_guide_path(repo_root, args.name)
        if path is None:
            print(f"ERROR: unknown or missing writing guide `{args.name}`")
            return 1
        print(path.read_text(encoding="utf-8"), end="")
        return 0

    # list (default)
    print("Available writing guides:")
    for name, relative in _GUIDANCE_MAP.items():
        path = repo_root / relative
        exists_icon = "✓" if path.exists() else "✗"
        print(f"  {exists_icon} {name:<15} -> {relative}")
    print(f"\nRead one with: openharness writing-guide read <name>")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    import subprocess
    repo_root = _openharness_repo_root()
    default_mode = getattr(args, "set_default_mode", None)
    if default_mode:
        mode = str(default_mode)
        if mode not in UPDATE_MODES:
            print(f"ERROR: invalid mode `{mode}`; expected `pull` or `force-sync`.")
            return 1
        try:
            _set_default_update_mode(repo_root, mode)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Default update mode set to `{mode}` in {_project_settings_path(repo_root)}")
        return 0

    try:
        update_mode = _resolve_update_mode(args, repo_root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if update_mode == "force-sync":
        for command in ("git fetch --prune", "git reset --hard '@{u}'"):
            sync_result = subprocess.run(command, shell=True, cwd=repo_root).returncode
            if sync_result != 0:
                print(f"ERROR: force sync failed at `{command}`; refusing to continue with tool upgrade.")
                return 1
        print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    elif update_mode == "pull":
        git_pull_result = subprocess.run("git pull", shell=True, cwd=repo_root).returncode
        if git_pull_result != 0:
            print("ERROR: git pull failed; refusing to continue with tool upgrade.")
            return 1
    else:
        print(f"ERROR: invalid update mode `{update_mode}`; expected `pull` or `force-sync`.")
        return 1

    upgrade_result = subprocess.run("uv tool upgrade openharness", shell=True, cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade openharness` failed.")
        return 1
    print(f"Updated OpenHarness from {repo_root}")
    return 0
