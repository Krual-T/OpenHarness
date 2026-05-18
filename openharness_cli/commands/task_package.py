
import json

import typer

from ..display import describe_stage, output_state_hook
from ..core import (
    create_task_package,
    discover_task_packages,
    humanize_task_name,
    resolve_task_package,
    summarize_task_package,
)
from ..core.task_packages import _auto_archive_active_packages
from ..transition_engine import execute_transition
from ..validate import validate_task_package
from ..workflows import ACTIVE_STATUSES

task_app = typer.Typer(help="Manage task packages.")


@task_app.command(name="list")
def list_packages(
    ctx: typer.Context,
    as_json: bool = typer.Option(False, "--json", help="Print JSON output"),
    show_all: bool = typer.Option(False, "--all", help="Include archived task packages"),
) -> None:
    """List task packages with current status and next steps."""
    hx = ctx.obj
    try:
        packages = discover_task_packages()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)

    author_entry_path = hx.repo_root / "skills" / "using-openharness" / "references" / "author-entry.md"
    author_entry: dict | None = None
    if author_entry_path.exists():
        author_entry = {"path": str(author_entry_path), "summary": "Chinese-first author entry for task-package writing guidance."}

    if not show_all:
        packages = [p for p in packages if p.current_status in ACTIVE_STATUSES]

    if as_json:
        cfg = packages[0].config if packages else None
        task_packages_root = str(cfg.task_packages_root) if cfg else str(hx.repo_root / "docs" / "task-packages")
        archived_root = str(cfg.archived_task_packages_root) if cfg else str(hx.repo_root / "docs" / "archived" / "task-packages")
        payload = {
            "repo": str(hx.repo_root),
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
        return

    if author_entry is not None:
        print(f"author entry: {author_entry['path']}")
    if not packages:
        print("No matching task packages found.")
        return

    print("Active task packages:" if not show_all else "Task packages:")
    for p in packages:
        stage = describe_stage(p)
        print(f"- {summarize_task_package(p)}")
        print(f"  current stage: `{stage['current_stage']}` - {stage['current_stage_description']}")
        print(f"  next stage: `{stage['next_stage']}`" if stage["next_stage"] else "  next stage: none")
        print(f"  next step: {stage['next_step']}")


@task_app.command(name="view")
def view_package(
    task: str = typer.Argument(..., help="Task package name or task id"),
) -> None:
    """Show task package details and inject the current stage's skill instructions."""
    try:
        package = resolve_task_package(task)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)

    stage = describe_stage(package)
    print(f"Task: {package.task_id} {package.title}")
    print(f"Owner: {package.owner}")
    print(f"Status: `{stage['current_stage']}` — {stage['current_stage_description']}")
    print(f"Next: `{stage['next_stage']}` — {stage['next_step']}" if stage["next_stage"] else f"Next: none")
    output_state_hook(package.current_status)


@task_app.command(name="new")
def new_package(
    task_name: str = typer.Argument(..., help="Directory slug or human-readable task name"),
    title: str = typer.Option("", "--title", help="Human-readable task title"),
    owner: str = typer.Option("unassigned", "--owner", help="Initial owner"),
    summary: str = typer.Option("", "--summary", help="Short summary"),
    status: str = typer.Option("proposing", "--status", help="Initial status"),
) -> None:
    """Create a new task package with an auto-allocated task ID."""
    human_title = title or humanize_task_name(task_name)
    try:
        task_root, task_id = create_task_package(
            task_name=task_name,
            title=human_title,
            owner=owner,
            summary=summary,
            status=status,
        )
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)

    print(f"Created task package: {task_root}")
    print(f"Task id: {task_id}")
    print(f"Title: {human_title}")
    print(f"Current status: {status}")
    output_state_hook(status if status in ACTIVE_STATUSES else "proposing")
    print(f"\n完成后执行：openharness task-package transition {task_id} requirements_designed")


@task_app.command(name="transition")
def transition(
    task: str = typer.Argument(..., help="Task package name or task id"),
    target_status: str = typer.Argument(..., help="Target workflow status"),
) -> None:
    """Move a task package to a legal workflow status."""
    _auto_archive_active_packages()
    try:
        package = resolve_task_package(task)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)

    result, errors = execute_transition(package, target_status)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise typer.Exit(code=1)

    if result.package is not None:
        updated = result.package
        validation_errors = validate_task_package(updated)
        if validation_errors:
            for error in validation_errors:
                print(f"ERROR: {error}")
            raise typer.Exit(code=1)
        target = updated.current_status
        print(f"Transitioned {package.task_id} from `{package.current_status}` to `{target}`")
        output_state_hook(target)
    elif result.archived_path is not None:
        print(f"Archived task package: {package.task_id} -> {result.archived_path}")
        output_state_hook("archived")
    else:
        print(f"{package.task_id} already in `{package.current_status}`")
