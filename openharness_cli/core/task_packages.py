from __future__ import annotations

import contextlib
import fcntl
import json
from pathlib import Path

from ..constants import TASK_ID_RE
from ..harness_context import harness, HarnessContext
from ..models import CreateTaskInput, TaskInfo, TaskPackage, TaskStatus, TaskPackageDocument
from .yaml import load_yaml, write_yaml
from .utils import current_date, get_git_author, slugify_task_name

ALL_DESIGN_FILES: tuple[TaskPackageDocument, ...] = tuple(TaskPackageDocument)


# ═══════════════════════════════════════════════════════════════════════════════
# Discovery
# ═══════════════════════════════════════════════════════════════════════════════

@harness
def discover_task_packages(ctx: HarnessContext) -> list[TaskPackage]:
    _auto_archive_active_packages()
    config = ctx.config
    packages: list[TaskPackage] = []
    roots = [config.task_packages_root]
    if config.archived_task_packages_root != config.task_packages_root:
        roots.append(config.archived_task_packages_root)
    seen: set[Path] = set()
    for task_packages_root in roots:
        if not task_packages_root.exists():
            continue
        for child in sorted(path for path in task_packages_root.iterdir() if path.is_dir()):
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            info_path = TaskPackageDocument.TASK_INFO.path_from(child)
            if not info_path.exists():
                continue
            raw_info = load_yaml(info_path)
            info = TaskInfo.from_dict(raw_info)
            packages.append(TaskPackage(root=child, info=info, config=config))
    return packages


@harness
def resolve_task_package(ctx: HarnessContext, task: str) -> TaskPackage:
    for package in discover_task_packages():
        if package.name == task or package.task_id == task:
            return package
    raise ValueError(f"task package not found: {task}")


def summarize_task_package(package: TaskPackage) -> str:
    summary = package.summary or "(no summary)"
    return f"{package.task_id} [{package.current_status}] {package.title} - {summary}"


def find_duplicate_task_ids(packages: list[TaskPackage]) -> dict[str, list[TaskPackage]]:
    grouped: dict[str, list[TaskPackage]] = {}
    for package in packages:
        grouped.setdefault(package.task_id, []).append(package)
    return {
        task_id: duplicates
        for task_id, duplicates in grouped.items()
        if task_id and len(duplicates) > 1
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Archive
# ═══════════════════════════════════════════════════════════════════════════════

def archive_task_package(package: TaskPackage) -> tuple[bool, str]:
    import shutil
    target_root = package.config.archived_task_packages_root / package.name
    target_root.parent.mkdir(parents=True, exist_ok=True)
    if target_root.exists():
        return False, f"archive target already exists: {target_root}"

    shutil.move(str(package.root), str(target_root))

    info_path = TaskPackageDocument.TASK_INFO.path_from(target_root)
    raw_info = load_yaml(info_path)
    raw_info["status"] = "archived"
    raw_info["updated_at"] = current_date()
    write_yaml(info_path, raw_info)

    return True, ""


@harness
def _auto_archive_active_packages(ctx: HarnessContext) -> None:
    config = ctx.config
    if config.task_packages_root == config.archived_task_packages_root:
        return
    if not config.task_packages_root.exists():
        return

    for child in sorted(path for path in config.task_packages_root.iterdir() if path.is_dir()):
        info_path = child / "task-info.yaml"
        if not info_path.exists():
            continue
        raw_info = load_yaml(info_path)
        if str(raw_info.get("status") or "").strip() != "archived":
            continue
        info = TaskInfo.from_dict(raw_info)
        package = TaskPackage(root=child, info=info, config=config)
        archived_ok, detail = archive_task_package(package)
        if not archived_ok:
            raise ValueError(f"failed to auto-archive task package `{package.task_id}`: {detail}")


# ═══════════════════════════════════════════════════════════════════════════════
# Creation
# ═══════════════════════════════════════════════════════════════════════════════

@harness
def _task_package_lock_path(ctx: HarnessContext) -> Path:
    return ctx.repo_root / ".harness" / "locks" / "new-task.lock"


@harness
@contextlib.contextmanager
def _task_package_creation_lock(ctx: HarnessContext):
    lock_path = _task_package_lock_path()
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@harness
def _resolve_template_root(ctx: HarnessContext) -> Path:
    skill_root = Path(__file__).resolve().parents[1]
    candidates = (
        ctx.repo_root / "skills" / "using-openharness" / "references" / "templates",
        skill_root / "references" / "templates",
    )
    for candidate in candidates:
        if candidate.resolve().exists():
            return candidate.resolve()
    raise FileNotFoundError("template root not found")


@harness
def _create_task_package_unlocked(ctx: HarnessContext, request: CreateTaskInput, task_id: str) -> Path:
    config = ctx.config
    task_name = slugify_task_name(request.task_name)
    task_root = config.task_packages_root / task_name
    if task_root.exists():
        raise FileExistsError(f"task package already exists: {task_root}")

    template_root = _resolve_template_root()
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
        if target_name == TaskPackageDocument.TASK_INFO:
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


@harness
def allocate_next_task_id(ctx: HarnessContext) -> str:
    prefix_counts: dict[str, int] = {}
    max_by_prefix: dict[str, tuple[int, int]] = {}
    for package in discover_task_packages():
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


@harness
def _resolve_owner(ctx: HarnessContext, owner: str) -> str:
    if owner == "unassigned":
        return get_git_author()
    return owner


@harness
def create_task_package(
    ctx: HarnessContext, *, task_name: str, title: str,
    owner: str = "unassigned", summary: str = "", status: str = "proposing",
) -> tuple[Path, str]:
    """Create a new task package with an auto-allocated task ID."""
    owner = _resolve_owner(owner)
    with _task_package_creation_lock():
        task_id = allocate_next_task_id()
        task_root = _create_task_package_unlocked(
            CreateTaskInput(
                task_name=task_name,
                title=title, owner=owner, summary=summary,
                status=TaskStatus(status) if status else TaskStatus.PROPOSING,
            ),
            task_id=task_id,
        )
    return task_root, task_id
