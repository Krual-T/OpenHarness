
import contextlib
import fcntl
import json
from pathlib import Path

from ..constants import TASK_ID_RE
from ..harness_context import harness, HarnessContext
from ..models import CreateTaskInput, TaskInfo, TaskPackage, TaskStatus, TaskPackageDocument
from ..workflows import workflow_for
from .yaml import load_yaml, write_yaml
from .utils import current_date, get_git_author, slugify_task_name

ALL_DESIGN_FILES: tuple[TaskPackageDocument, ...] = tuple(TaskPackageDocument)


# ═══════════════════════════════════════════════════════════════════════════════
# Discovery
# ═══════════════════════════════════════════════════════════════════════════════

@harness
def discover_task_packages(ctx: HarnessContext) -> list[TaskPackage]:
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
    if package.root.exists():
        try:
            package.root.rmdir()
        except OSError:
            return False, f"archive source still exists after move: {package.root}"

    info_path = TaskPackageDocument.TASK_INFO.path_from(target_root)
    raw_info = load_yaml(info_path)
    raw_info["status"] = "archived"
    raw_info["updated_at"] = current_date()
    _rewrite_archived_package_paths(raw_info, package)
    write_yaml(info_path, raw_info)

    return True, ""


def _rewrite_archived_package_paths(raw_info: dict, package: TaskPackage) -> None:
    active_prefix = str(package.config.task_packages_root.relative_to(package.config.repo_root) / package.name)
    archived_prefix = str(package.config.archived_task_packages_root.relative_to(package.config.repo_root) / package.name)

    def rewrite(value):
        if isinstance(value, str):
            if value == active_prefix:
                return archived_prefix
            if value.startswith(f"{active_prefix}/"):
                return f"{archived_prefix}/{value[len(active_prefix) + 1:]}"
            return value
        if isinstance(value, list):
            return [rewrite(item) for item in value]
        if isinstance(value, dict):
            return {key: rewrite(item) for key, item in value.items()}
        return value

    for key, value in list(raw_info.items()):
        raw_info[key] = rewrite(value)


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
            print(f"WARNING: failed to auto-archive task package `{package.task_id}`: {detail}", flush=True)


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
    pkg_root = Path(__file__).resolve().parents[2]
    relative = "skills/using-openharness/references/templates"
    candidates = (
        ctx.repo_root / relative,
        pkg_root / relative,
        ctx.repo_root / ".claude" / "skills" / relative,
        ctx.repo_root / ".codex" / "skills" / relative,
        ctx.repo_root / ".codex" / "skills" / "openharness" / relative,
        ctx.repo_root / ".agents" / "skills" / relative,
        ctx.repo_root / ".agents" / "skills" / "openharness" / relative,
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
        "<TASK_ID>": task_id,
        "<DESIGN_ID>": task_id,
        "<TITLE>": request.title,
        "<DESIGN_NAME>": task_name,
        "<OWNER>": request.owner,
        "<STATUS>": request.status.value,
        "<SUMMARY>": request.summary or f"描述《{request.title}》的目标和要求。",
        "<DATE>": current_date(),
    }
    task_root.mkdir(parents=True, exist_ok=False)
    for doc in workflow_for(None).scaffold_files(request.status):
        _create_task_package_document(template_root, task_root, doc, replacements)
    return task_root


def _create_task_package_document(
    template_root: Path,
    task_root: Path,
    doc: TaskPackageDocument,
    replacements: dict[str, str],
) -> None:
    template = template_root / f"task-package.{doc.value}"
    if not template.exists():
        raise FileNotFoundError(f"template not found: {template}")
    target_path = doc.path_from(task_root)
    if target_path.exists():
        return
    content = template.read_text(encoding="utf-8")
    template_replacements = dict(replacements)
    if doc == TaskPackageDocument.TASK_INFO:
        template_replacements.update({
            "<TASK_ID>": json.dumps(replacements["<TASK_ID>"], ensure_ascii=False),
            "<DESIGN_ID>": json.dumps(replacements["<DESIGN_ID>"], ensure_ascii=False),
            "<TITLE>": json.dumps(replacements["<TITLE>"], ensure_ascii=False),
            "<OWNER>": json.dumps(replacements["<OWNER>"], ensure_ascii=False),
            "<STATUS>": json.dumps(replacements["<STATUS>"], ensure_ascii=False),
            "<SUMMARY>": json.dumps(replacements["<SUMMARY>"], ensure_ascii=False),
            "<DATE>": json.dumps("YYYY-MM-DD", ensure_ascii=False),
        })
    for source, target in template_replacements.items():
        content = content.replace(source, target)
    target_path.write_text(content, encoding="utf-8")


@harness
def ensure_task_package_stage_files(ctx: HarnessContext, package: TaskPackage) -> None:
    docs = package.workflow.scaffold_files(package.info.status)
    missing_docs = [doc for doc in docs if not doc.path_from(package.root).exists()]
    if not missing_docs:
        return
    template_root = _resolve_template_root()
    replacements = {
        "<TASK_ID>": package.task_id,
        "<DESIGN_ID>": package.task_id,
        "<TITLE>": package.title,
        "<DESIGN_NAME>": package.name,
        "<OWNER>": package.owner,
        "<STATUS>": package.current_status,
        "<SUMMARY>": package.summary,
        "<DATE>": "YYYY-MM-DD",
    }
    for doc in missing_docs:
        _create_task_package_document(template_root, package.root, doc, replacements)


@harness
def allocate_next_task_id(ctx: HarnessContext) -> str:
    max_number = 0
    max_width = 0
    for package in discover_task_packages():
        match = TASK_ID_RE.match(package.task_id)
        if not match:
            continue
        prefix, raw_number = match.groups()
        if prefix != "TASK":
            continue
        number = int(raw_number)
        width = len(raw_number)
        if number > max_number:
            max_number = number
            max_width = width
        elif number == max_number and width > max_width:
            max_width = width

    next_number = max_number + 1
    return f"TASK-{next_number:0{max(max_width, 3)}d}"


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
