from __future__ import annotations

import contextlib
import fcntl
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .constants import REQUIRED_TASK_PACKAGE_FILES, TASK_ID_RE
from .models import HarnessManifest, RuntimeWorkflowPackage, TaskPackage, TaskScaffoldRequest


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(
            f"failed to parse YAML at {path}. "
            "If a STATUS.yaml sentence contains backticks or other YAML-sensitive punctuation, "
            'wrap the whole sentence in double quotes, for example: '
            'summary: "`02-overview-design.md` guidance: fix quoting"'
        ) from exc
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


def _rwp_root(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "rwp").resolve()


def _rwp_workflows_root(repo_root: Path) -> Path:
    return _rwp_root(repo_root) / "workflows"


def _load_workflow_metadata(workflow_path: Path) -> dict[str, Any]:
    text = workflow_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"workflow metadata header missing in {workflow_path}")
    end_index = text.find("\n---", 4)
    if end_index == -1:
        raise ValueError(f"workflow metadata header not closed in {workflow_path}")
    metadata_text = text[4:end_index]
    try:
        data = yaml.safe_load(metadata_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"failed to parse workflow metadata at {workflow_path}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"workflow metadata at {workflow_path} must be a mapping")
    name = str(data.get("name") or "").strip()
    description = str(data.get("description") or "").strip()
    if not name or not description:
        raise ValueError(f"workflow metadata at {workflow_path} requires `name` and `description`")
    return {"name": name, "description": description}


def discover_runtime_workflow_packages(repo_root: Path) -> list[RuntimeWorkflowPackage]:
    workflows_root = _rwp_workflows_root(repo_root)
    if not workflows_root.exists():
        return []
    packages: list[RuntimeWorkflowPackage] = []
    for child in sorted(path for path in workflows_root.iterdir() if path.is_dir()):
        workflow_path = child / "workflow.md"
        if not workflow_path.exists():
            continue
        metadata = _load_workflow_metadata(workflow_path)
        packages.append(
            RuntimeWorkflowPackage(
                root=child,
                workflow_path=workflow_path,
                name=metadata["name"],
                description=metadata["description"],
            )
        )
    return packages


def resolve_runtime_workflow_package(repo_root: Path, workflow: str) -> RuntimeWorkflowPackage:
    matches = [
        package
        for package in discover_runtime_workflow_packages(repo_root)
        if package.name == workflow or package.root.name == workflow
    ]
    if not matches:
        raise ValueError(f"runtime workflow package not found: {workflow}")
    if len(matches) > 1:
        roots = ", ".join(str(package.root) for package in matches)
        raise ValueError(f"runtime workflow package `{workflow}` is ambiguous: {roots}")
    return matches[0]


def resolve_runtime_workflow_script(repo_root: Path, workflow: str, script: str) -> Path:
    script_name = str(script or "").strip()
    if not script_name:
        raise ValueError("rwp run requires an explicit script name")
    if "/" in script_name or "\\" in script_name:
        raise ValueError("rwp script name must refer to a file directly under `scripts/`")
    if not script_name.endswith(".py"):
        raise ValueError("rwp run only supports `.py` scripts")
    package = resolve_runtime_workflow_package(repo_root, workflow)
    script_path = package.root / "scripts" / script_name
    if not script_path.exists() or not script_path.is_file():
        raise ValueError(f"rwp script not found: {script_name}")
    return script_path


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


def _duplicate_task_id_exists(
    repo_root: Path,
    task_id: str,
    manifest: HarnessManifest | None = None,
) -> bool:
    current_manifest = manifest or load_manifest(repo_root)
    return any(package.task_id == task_id for package in discover_task_packages(repo_root, current_manifest))


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


def _create_task_package_unlocked(
    request: TaskScaffoldRequest,
    manifest: HarnessManifest | None = None,
) -> Path:
    current_manifest = manifest or load_manifest(request.repo_root)
    task_name = slugify_task_name(request.task_name)
    task_root = current_manifest.task_packages_root / task_name
    if task_root.exists():
        raise FileExistsError(f"task package already exists: {task_root}")
    if _duplicate_task_id_exists(request.repo_root, request.task_id, current_manifest):
        raise ValueError(f"duplicate task id `{request.task_id}` already exists")
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
        template_replacements = dict(replacements)
        if target_name == "STATUS.yaml":
            template_replacements.update(
                {
                    "<DESIGN_ID>": json.dumps(request.task_id, ensure_ascii=False),
                    "<TITLE>": json.dumps(request.title, ensure_ascii=False),
                    "<OWNER>": json.dumps(request.owner, ensure_ascii=False),
                    "<STATUS>": json.dumps(request.status, ensure_ascii=False),
                    "<SUMMARY>": json.dumps(
                        request.summary or f"Describe the goal of {request.title}.",
                        ensure_ascii=False,
                    ),
                    "<DATE>": json.dumps("YYYY-MM-DD", ensure_ascii=False),
                }
            )
        for source, target in template_replacements.items():
            content = content.replace(source, target)
        (task_root / target_name).write_text(content, encoding="utf-8")
    return task_root


def create_task_package(request: TaskScaffoldRequest) -> Path:
    manifest = load_manifest(request.repo_root)
    with _task_package_creation_lock(request.repo_root):
        return _create_task_package_unlocked(request, manifest)


def create_task_package_with_auto_id(
    *,
    repo_root: Path,
    task_name: str,
    title: str,
    owner: str = "unassigned",
    summary: str = "",
    status: str = "proposed",
) -> tuple[Path, str]:
    manifest = load_manifest(repo_root)
    with _task_package_creation_lock(repo_root):
        task_id = allocate_next_task_id(repo_root, manifest)
        task_root = _create_task_package_unlocked(
            TaskScaffoldRequest(
                repo_root=repo_root,
                task_name=task_name,
                task_id=task_id,
                title=title,
                owner=owner,
                summary=summary,
                status=status,
            ),
            manifest,
        )
    return task_root, task_id
