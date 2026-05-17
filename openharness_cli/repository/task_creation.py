from __future__ import annotations

import contextlib
import fcntl
import json
from pathlib import Path

from ..constants import TASK_ID_RE
from ..models import CreateTaskInput, TaskStatus
from .config import load_config
from .task_packages import discover_task_packages
from .utils import get_git_author, slugify_task_name


def _task_package_lock_path(repo_root: Path) -> Path:
    return repo_root / ".harness" / "locks" / "new-task.lock"


@contextlib.contextmanager
def _task_package_creation_lock(repo_root: Path):
    lock_path = _task_package_lock_path(repo_root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _resolve_template_root(repo_root: Path) -> Path:
    skill_root = Path(__file__).resolve().parents[1]
    candidates = (
        repo_root / "skills" / "using-openharness" / "references" / "templates",
        skill_root / "references" / "templates",
    )
    for candidate in candidates:
        if candidate.resolve().exists():
            return candidate.resolve()
    raise FileNotFoundError("template root not found")


def _create_task_package_unlocked(request: CreateTaskInput, task_id: str) -> Path:
    current_config = load_config(request.repo_root)
    task_name = slugify_task_name(request.task_name)
    task_root = current_config.task_packages_root / task_name
    if task_root.exists():
        raise FileExistsError(f"task package already exists: {task_root}")

    template_root = _resolve_template_root(request.repo_root)
    replacements = {
        "<DESIGN_ID>": task_id,
        "<TITLE>": request.title,
        "<DESIGN_NAME>": task_name,
        "<OWNER>": request.owner,
        "<STATUS>": request.status.value,
        "<SUMMARY>": request.summary or f"Describe the goal of {request.title}.",
        "<DATE>": "YYYY-MM-DD",
    }
    task_root.mkdir(parents=True, exist_ok=False)
    for template in sorted(template_root.glob("task-package.*")):
        target_name = template.name.removeprefix("task-package.")
        content = template.read_text(encoding="utf-8")
        template_replacements = dict(replacements)
        if target_name == "task-info.yaml":
            template_replacements.update({
                "<DESIGN_ID>": json.dumps(task_id, ensure_ascii=False),
                "<TITLE>": json.dumps(request.title, ensure_ascii=False),
                "<OWNER>": json.dumps(request.owner, ensure_ascii=False),
                "<STATUS>": json.dumps(request.status.value, ensure_ascii=False),
                "<SUMMARY>": json.dumps(request.summary or f"Describe the goal of {request.title}.", ensure_ascii=False),
                "<DATE>": json.dumps("YYYY-MM-DD", ensure_ascii=False),
            })
        for source, target in template_replacements.items():
            content = content.replace(source, target)
        (task_root / target_name).write_text(content, encoding="utf-8")
    return task_root


def allocate_next_task_id(repo_root: Path) -> str:
    prefix_counts: dict[str, int] = {}
    max_by_prefix: dict[str, tuple[int, int]] = {}
    for package in discover_task_packages(repo_root):
        match = TASK_ID_RE.match(package.task_id)
        if not match:
            continue
        prefix, raw_number = match.groups()
        number = int(raw_number)
        width = len(raw_number)
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        previous = max_by_prefix.get(prefix)
        if previous is None or number > previous[0]:
            max_by_prefix[prefix] = (number, width)
        elif number == previous[0] and width > previous[1]:
            max_by_prefix[prefix] = (number, width)

    if not max_by_prefix:
        return "TASK-001"
    prefix = max(prefix_counts.items(), key=lambda item: (item[1], item[0]))[0]
    max_number, width = max_by_prefix[prefix]
    next_number = max_number + 1
    return f"{prefix}-{next_number:0{max(width, 3)}d}"


def _resolve_owner(repo_root: Path, owner: str) -> str:
    if owner == "unassigned":
        return get_git_author(repo_root)
    return owner


def create_task_package(
    *, repo_root: Path, task_name: str, title: str,
    owner: str = "unassigned", summary: str = "", status: str = "proposing",
) -> tuple[Path, str]:
    """Create a new task package with an auto-allocated task ID."""
    owner = _resolve_owner(repo_root, owner)
    with _task_package_creation_lock(repo_root):
        task_id = allocate_next_task_id(repo_root)
        task_root = _create_task_package_unlocked(
            CreateTaskInput(
                repo_root=repo_root, task_name=task_name,
                title=title, owner=owner, summary=summary,
                status=TaskStatus(status) if status else TaskStatus.PROPOSING,
            ),
            task_id=task_id,
        )
    return task_root, task_id
