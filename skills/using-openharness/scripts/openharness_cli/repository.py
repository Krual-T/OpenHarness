from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .constants import REQUIRED_TASK_PACKAGE_FILES, TASK_ID_RE
from .models import HarnessManifest, TaskPackage, TaskScaffoldRequest


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML object at {path} must be a mapping")
    return data


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def load_manifest(repo_root: Path) -> HarnessManifest:
    skill_root = Path(__file__).resolve().parents[1]
    candidates = (
        repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml",
        repo_root / "skills" / "using-openharness" / "manifest.yaml",
        repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "references" / "manifest.yaml",
        repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "manifest.yaml",
        repo_root / ".harness" / "manifest.yaml",
        skill_root / "references" / "manifest.yaml",
        skill_root / "manifest.yaml",
    )
    for candidate in candidates:
        manifest_path = candidate.resolve()
        if manifest_path.exists():
            return HarnessManifest(repo_root=repo_root, path=manifest_path, raw=_load_yaml(manifest_path))
    raise FileNotFoundError(
        "Harness manifest not found. Checked: "
        + ", ".join(str(candidate) for candidate in candidates)
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_timestamp() -> str:
    return _utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def _current_date() -> str:
    return _utc_now().date().isoformat()


def discover_task_packages(repo_root: Path, manifest: HarnessManifest | None = None) -> list[TaskPackage]:
    current_manifest = manifest or load_manifest(repo_root)
    packages: list[TaskPackage] = []
    roots = [current_manifest.task_packages_root]
    if current_manifest.archived_task_packages_root != current_manifest.task_packages_root:
        roots.append(current_manifest.archived_task_packages_root)
    seen: set[Path] = set()
    for task_packages_root in roots:
        if not task_packages_root.exists():
            continue
        for child in sorted(path for path in task_packages_root.iterdir() if path.is_dir()):
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            status_path = child / "STATUS.yaml"
            if not status_path.exists():
                continue
            status = _load_yaml(status_path)
            documents = {name: child / name for name in current_manifest.required_design_files}
            packages.append(TaskPackage(root=child, status=status, manifest=current_manifest, documents=documents))
    return packages


def find_duplicate_task_ids(packages: list[TaskPackage]) -> dict[str, list[TaskPackage]]:
    grouped: dict[str, list[TaskPackage]] = {}
    for package in packages:
        grouped.setdefault(package.task_id, []).append(package)
    return {
        task_id: duplicates
        for task_id, duplicates in grouped.items()
        if task_id and len(duplicates) > 1
    }


def resolve_task_package(repo_root: Path, task: str, manifest: HarnessManifest | None = None) -> TaskPackage:
    current_manifest = manifest or load_manifest(repo_root)
    for package in discover_task_packages(repo_root, current_manifest):
        if package.name == task or package.task_id == task:
            return package
    raise ValueError(f"task package not found: {task}")


def summarize_task_package(package: TaskPackage) -> str:
    summary = package.summary or "(no summary)"
    return f"{package.task_id} [{package.status_name}] {package.title} - {summary}"


def slugify_task_name(raw_name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", raw_name.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("task name must contain at least one ASCII letter or number")
    return cleaned


def humanize_task_name(task_name: str) -> str:
    slug = slugify_task_name(task_name)
    return " ".join(part.capitalize() for part in slug.split("-"))


def allocate_next_task_id(repo_root: Path, manifest: HarnessManifest | None = None) -> str:
    current_manifest = manifest or load_manifest(repo_root)
    prefix_counts: dict[str, int] = {}
    max_by_prefix: dict[str, tuple[int, int]] = {}
    for package in discover_task_packages(repo_root, current_manifest):
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


def create_task_package(request: TaskScaffoldRequest) -> Path:
    manifest = load_manifest(request.repo_root)
    task_name = slugify_task_name(request.task_name)
    task_root = manifest.task_packages_root / task_name
    if task_root.exists():
        raise FileExistsError(f"task package already exists: {task_root}")
    skill_root = Path(__file__).resolve().parents[1]
    template_root = request.repo_root / "skills" / "using-openharness" / "references" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / "skills" / "using-openharness" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "references" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "templates"
    if not template_root.exists():
        template_root = skill_root / "references" / "templates"
    if not template_root.exists():
        template_root = skill_root / "templates"
    replacements = {
        "<DESIGN_ID>": request.task_id,
        "<TITLE>": request.title,
        "<DESIGN_NAME>": task_name,
        "<OWNER>": request.owner,
        "<STATUS>": request.status,
        "<SUMMARY>": request.summary or f"Describe the goal of {request.title}.",
        "<DATE>": "YYYY-MM-DD",
    }
    task_root.mkdir(parents=True, exist_ok=False)
    for template in sorted(template_root.glob("task-package.*")):
        target_name = template.name.removeprefix("task-package.")
        content = template.read_text(encoding="utf-8")
        for source, target in replacements.items():
            content = content.replace(source, target)
        (task_root / target_name).write_text(content, encoding="utf-8")
    return task_root
