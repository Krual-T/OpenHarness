from __future__ import annotations

from pathlib import Path

from ..domain import TaskInfo
from ..models import HarnessConfig, TaskPackage
from .config import load_config, _resolve_config
from .yaml import _load_yaml, _write_yaml
from .utils import _current_date

ALL_DESIGN_FILES = (
    "README.md", "task-info.yaml", "01-requirements.md",
    "02-overview-design.md", "03-detailed-design.md",
    "verification_design.md", "evidence.md",
)


def discover_task_packages(repo_root: Path, config: HarnessConfig | None = None) -> list[TaskPackage]:
    current_config = _resolve_config(repo_root, config)
    _auto_archive_active_packages(current_config)
    packages: list[TaskPackage] = []
    roots = [current_config.task_packages_root]
    if current_config.archived_task_packages_root != current_config.task_packages_root:
        roots.append(current_config.archived_task_packages_root)
    seen: set[Path] = set()
    for task_packages_root in roots:
        if not task_packages_root.exists():
            continue
        for child in sorted(path for path in task_packages_root.iterdir() if path.is_dir()):
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            info_path = child / "task-info.yaml"
            if not info_path.exists():
                continue
            raw_info = _load_yaml(info_path)
            info = TaskInfo.from_dict(raw_info)
            documents = {name: child / name for name in ALL_DESIGN_FILES}
            packages.append(TaskPackage(root=child, info=info, config=current_config, documents=documents))
    return packages


def _archive_task_package(package: TaskPackage) -> tuple[bool, str]:
    import shutil
    target_root = package.config.archived_task_packages_root / package.name
    target_root.parent.mkdir(parents=True, exist_ok=True)
    if target_root.exists():
        return False, f"archive target already exists: {target_root}"

    shutil.move(str(package.root), str(target_root))

    info_path = target_root / "task-info.yaml"
    raw_info = _load_yaml(info_path)
    raw_info["status"] = "archived"
    raw_info["updated_at"] = _current_date()
    _write_yaml(info_path, raw_info)

    return True, ""


def _auto_archive_active_packages(config: HarnessConfig) -> None:
    if config.task_packages_root == config.archived_task_packages_root:
        return
    if not config.task_packages_root.exists():
        return

    for child in sorted(path for path in config.task_packages_root.iterdir() if path.is_dir()):
        info_path = child / "task-info.yaml"
        if not info_path.exists():
            continue
        raw_info = _load_yaml(info_path)
        if str(raw_info.get("status") or "").strip() != "archived":
            continue
        info = TaskInfo.from_dict(raw_info)
        package = TaskPackage(
            root=child, info=info, config=config,
            documents={name: child / name for name in ALL_DESIGN_FILES},
        )
        archived_ok, detail = _archive_task_package(package)
        if not archived_ok:
            raise ValueError(f"failed to auto-archive task package `{package.task_id}`: {detail}")


def find_duplicate_task_ids(packages: list[TaskPackage]) -> dict[str, list[TaskPackage]]:
    grouped: dict[str, list[TaskPackage]] = {}
    for package in packages:
        grouped.setdefault(package.task_id, []).append(package)
    return {
        task_id: duplicates
        for task_id, duplicates in grouped.items()
        if task_id and len(duplicates) > 1
    }


def resolve_task_package(repo_root: Path, task: str, config: HarnessConfig | None = None) -> TaskPackage:
    current_config = _resolve_config(repo_root, config)
    for package in discover_task_packages(repo_root, current_config):
        if package.name == task or package.task_id == task:
            return package
    raise ValueError(f"task package not found: {task}")


def summarize_task_package(package: TaskPackage) -> str:
    summary = package.summary or "(no summary)"
    return f"{package.task_id} [{package.current_status}] {package.title} - {summary}"
