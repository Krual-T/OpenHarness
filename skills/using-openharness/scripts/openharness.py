#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re

import yaml

ACTIVE_STATUSES = {"proposed", "requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying"}
VERIFYABLE_STATUSES = {"in_progress", "verifying"}
REQUIRED_TASK_PACKAGE_FILES = (
    "README.md",
    "STATUS.yaml",
    "01-requirements.md",
    "02-overview-design.md",
    "03-detailed-design.md",
    "05-verification.md",
    "06-evidence.md",
)
REQUIRED_STATUS_KEYS = (
    "id",
    "title",
    "status",
    "summary",
    "owner",
    "created_at",
    "updated_at",
    "done_criteria",
    "verification",
)
VERIFICATION_RESULT_VALUES = {"passed", "failed", "insufficient_verification"}

PLACEHOLDER_BULLET_RE = re.compile(r"^[-*]\s*$")
PLACEHOLDER_NUMBERED_RE = re.compile(r"^\d+\.\s*$")
LABEL_ONLY_RE = re.compile(r"^[-*]\s+[^:]+:\s*$")

STATUS_SECTION_REQUIREMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "requirements_ready": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
    ),
    "overview_ready": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
        ("02-overview-design.md", "## System Boundary"),
        ("02-overview-design.md", "## Proposed Structure"),
        ("02-overview-design.md", "## Key Flows"),
        ("02-overview-design.md", "## Trade-offs"),
        ("02-overview-design.md", "## Overview Reflection"),
    ),
    "detailed_ready": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
        ("02-overview-design.md", "## System Boundary"),
        ("02-overview-design.md", "## Proposed Structure"),
        ("02-overview-design.md", "## Key Flows"),
        ("02-overview-design.md", "## Trade-offs"),
        ("02-overview-design.md", "## Overview Reflection"),
        ("03-detailed-design.md", "## Runtime Verification Plan"),
        ("03-detailed-design.md", "## Files Added Or Changed"),
        ("03-detailed-design.md", "## Interfaces"),
        ("03-detailed-design.md", "## Error Handling"),
        ("03-detailed-design.md", "## Detailed Reflection"),
    ),
    "verifying": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
        ("02-overview-design.md", "## System Boundary"),
        ("02-overview-design.md", "## Proposed Structure"),
        ("02-overview-design.md", "## Key Flows"),
        ("02-overview-design.md", "## Trade-offs"),
        ("02-overview-design.md", "## Overview Reflection"),
        ("03-detailed-design.md", "## Runtime Verification Plan"),
        ("03-detailed-design.md", "## Files Added Or Changed"),
        ("03-detailed-design.md", "## Interfaces"),
        ("03-detailed-design.md", "## Error Handling"),
        ("03-detailed-design.md", "## Detailed Reflection"),
    ),
    "archived": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
        ("02-overview-design.md", "## System Boundary"),
        ("02-overview-design.md", "## Proposed Structure"),
        ("02-overview-design.md", "## Key Flows"),
        ("02-overview-design.md", "## Trade-offs"),
        ("02-overview-design.md", "## Overview Reflection"),
        ("03-detailed-design.md", "## Runtime Verification Plan"),
        ("03-detailed-design.md", "## Files Added Or Changed"),
        ("03-detailed-design.md", "## Interfaces"),
        ("03-detailed-design.md", "## Error Handling"),
        ("03-detailed-design.md", "## Detailed Reflection"),
        ("06-evidence.md", "## Files"),
        ("06-evidence.md", "## Commands"),
        ("06-evidence.md", "## Residual Risks"),
    ),
}

STATUS_LABEL_REQUIREMENTS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "verifying": (
        ("05-verification.md", "## Verification Path", "Planned Path"),
        ("05-verification.md", "## Verification Path", "Executed Path"),
        ("05-verification.md", "## Latest Result", ""),
    ),
    "archived": (
        ("05-verification.md", "## Verification Path", "Planned Path"),
        ("05-verification.md", "## Verification Path", "Executed Path"),
        ("05-verification.md", "## Latest Result", ""),
    ),
}


@dataclass(slots=True, frozen=True)
class HarnessManifest:
    repo_root: Path
    path: Path
    raw: dict[str, Any]

    @property
    def task_packages_root(self) -> Path:
        raw_root = str(
            self.raw.get("task_packages_root")
            or self.raw.get("designs_root")
            or "docs/task-packages"
        ).strip() or "docs/task-packages"
        return (self.repo_root / raw_root).resolve()

    @property
    def archived_task_packages_root(self) -> Path:
        raw_root = str(
            self.raw.get("archived_task_packages_root")
            or self.raw.get("archived_designs_root")
            or "docs/archived/task-packages"
        ).strip() or "docs/archived/task-packages"
        return (self.repo_root / raw_root).resolve()

    @property
    def required_design_files(self) -> tuple[str, ...]:
        raw = self.raw.get("required_design_files")
        if not isinstance(raw, list) or not raw:
            return REQUIRED_TASK_PACKAGE_FILES
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def designs_root(self) -> Path:
        return self.task_packages_root

    @property
    def archived_designs_root(self) -> Path:
        return self.archived_task_packages_root

    @property
    def allowed_statuses(self) -> tuple[str, ...]:
        workflow = self.raw.get("workflow")
        if not isinstance(workflow, dict):
            return ()
        raw = workflow.get("default_status_flow")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())


@dataclass(slots=True, frozen=True)
class TaskPackage:
    root: Path
    status: dict[str, Any]
    manifest: HarnessManifest
    documents: dict[str, Path] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def status_name(self) -> str:
        return str(self.status.get("status") or "").strip()

    @property
    def task_id(self) -> str:
        return str(self.status.get("id") or self.root.name).strip()

    @property
    def title(self) -> str:
        return str(self.status.get("title") or self.root.name).strip()

    @property
    def summary(self) -> str:
        return str(self.status.get("summary") or "").strip()

    @property
    def owner(self) -> str:
        return str(self.status.get("owner") or "").strip()

    @property
    def done_criteria(self) -> tuple[str, ...]:
        raw = self.status.get("done_criteria")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def required_commands(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        commands = verification.get("required_commands")
        if not isinstance(commands, list):
            return ()
        return tuple(str(item).strip() for item in commands if str(item).strip())

    @property
    def required_scenarios(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        scenarios = verification.get("required_scenarios")
        if not isinstance(scenarios, list):
            return ()
        return tuple(str(item).strip() for item in scenarios if str(item).strip())

    @property
    def status_path(self) -> Path:
        return self.root / "STATUS.yaml"


@dataclass(slots=True, frozen=True)
class TaskScaffoldRequest:
    repo_root: Path
    task_name: str
    task_id: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: str = "proposed"


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


def _extract_markdown_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    target = heading.strip()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def _has_meaningful_markdown_content(text: str) -> bool:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if PLACEHOLDER_BULLET_RE.match(line):
            continue
        if PLACEHOLDER_NUMBERED_RE.match(line):
            continue
        if LABEL_ONLY_RE.match(line):
            continue
        return True
    return False


def _section_has_meaningful_content(path: Path, heading: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    section = _extract_markdown_section(text, heading)
    if not section:
        return False
    return _has_meaningful_markdown_content(section)


def _label_has_meaningful_content(path: Path, section_heading: str, label: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    section = _extract_markdown_section(text, section_heading)
    if not section:
        return False
    if not label:
        return _has_meaningful_markdown_content(section)

    lines = section.splitlines()
    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if not stripped.startswith("- "):
            continue
        body = stripped[2:]
        if not body.startswith(f"{label}:"):
            continue
        tail = body[len(label) + 1 :].strip()
        if tail:
            return True
        nested_lines: list[str] = []
        for nested in lines[index + 1 :]:
            if not nested.strip():
                continue
            if nested.startswith("- "):
                break
            if nested.startswith("## "):
                break
            nested_lines.append(nested)
        return _has_meaningful_markdown_content("\n".join(nested_lines))
    return False


def validate_task_package(package: TaskPackage) -> list[str]:
    errors: list[str] = []
    repo_root = package.manifest.repo_root
    for file_name in package.manifest.required_design_files:
        if not (package.root / file_name).exists():
            errors.append(f"missing required file: {package.root / file_name}")
    for key in REQUIRED_STATUS_KEYS:
        value = package.status.get(key)
        if value in (None, "", []):
            errors.append(f"missing status key `{key}` in {package.root / 'STATUS.yaml'}")
    verification = package.status.get("verification")
    if verification is not None and not isinstance(verification, dict):
        errors.append(f"`verification` must be a mapping in {package.root / 'STATUS.yaml'}")
    evidence = package.status.get("evidence")
    if evidence is not None and not isinstance(evidence, dict):
        errors.append(f"`evidence` must be a mapping in {package.root / 'STATUS.yaml'}")
    allowed_statuses = package.manifest.allowed_statuses
    if allowed_statuses and package.status_name not in allowed_statuses:
        errors.append(
            f"unknown status `{package.status_name}` in {package.root / 'STATUS.yaml'}; "
            f"expected one of: {', '.join(allowed_statuses)}"
        )
    if package.status_name == "archived":
        if package.root.resolve().parent != package.manifest.archived_task_packages_root:
            errors.append(
                f"archived package must live under {package.manifest.archived_task_packages_root}: {package.root}"
            )
    elif package.root.resolve().parent == package.manifest.archived_task_packages_root:
        errors.append(
            f"non-archived package must not live under {package.manifest.archived_task_packages_root}: {package.root}"
        )
    if package.status_name == "verifying" and not package.required_commands and not package.required_scenarios:
        errors.append(
            f"verifying status requires at least one verification path in {package.root / 'STATUS.yaml'}"
        )
    if package.status_name == "archived" and not package.required_commands and not package.required_scenarios:
        errors.append(
            f"archived status requires at least one verification path in {package.root / 'STATUS.yaml'}"
        )
    if isinstance(verification, dict):
        last_run_result = str(verification.get("last_run_result") or "").strip()
        if last_run_result and last_run_result not in VERIFICATION_RESULT_VALUES:
            errors.append(
                f"unknown verification.last_run_result `{last_run_result}` in {package.root / 'STATUS.yaml'}"
            )
        last_run_artifact = str(verification.get("last_run_artifact") or "").strip()
        if last_run_artifact:
            artifact_path = (repo_root / last_run_artifact).resolve()
            if not artifact_path.exists():
                errors.append(
                    f"missing referenced path `{last_run_artifact}` in {package.root / 'STATUS.yaml'}"
                )

    for key in ("entrypoints",):
        raw_paths = package.status.get(key)
        if isinstance(raw_paths, list):
            for raw_path in raw_paths:
                path = (repo_root / str(raw_path)).resolve()
                if not path.exists():
                    errors.append(f"missing referenced path `{raw_path}` in {package.root / 'STATUS.yaml'}")

    if isinstance(evidence, dict):
        for group in ("docs", "code", "tests"):
            raw_paths = evidence.get(group)
            if isinstance(raw_paths, list):
                for raw_path in raw_paths:
                    path = (repo_root / str(raw_path)).resolve()
                    if not path.exists():
                        errors.append(f"missing referenced path `{raw_path}` in {package.root / 'STATUS.yaml'}")

    for file_name, heading in STATUS_SECTION_REQUIREMENTS.get(package.status_name, ()):
        path = package.root / file_name
        if not _section_has_meaningful_content(path, heading):
            errors.append(
                f"{package.status_name} requires non-placeholder content for `{heading}` in {path}"
            )
    for file_name, section_heading, label in STATUS_LABEL_REQUIREMENTS.get(package.status_name, ()):
        path = package.root / file_name
        if not _label_has_meaningful_content(path, section_heading, label):
            anchor = f"`{section_heading}`" if not label else f"`{label}` inside `{section_heading}`"
            errors.append(
                f"{package.status_name} requires non-placeholder content for {anchor} in {path}"
            )
    return errors


def summarize_task_package(package: TaskPackage) -> str:
    summary = package.summary or "(no summary)"
    return f"{package.task_id} [{package.status_name}] {package.title} - {summary}"


def slugify_task_name(raw_name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", raw_name.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("task name must contain at least one ASCII letter or number")
    return cleaned


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


def _normalize_status_for_fingerprint(status: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(status)
    normalized.pop("updated_at", None)
    normalized.pop("status", None)
    verification = normalized.get("verification")
    if isinstance(verification, dict):
        verification.pop("last_run_at", None)
        verification.pop("last_run_result", None)
        verification.pop("last_run_artifact", None)
    return normalized


def compute_task_package_fingerprint(package: TaskPackage) -> str:
    payload: dict[str, Any] = {"documents": {}}
    for file_name in package.manifest.required_design_files:
        path = package.root / file_name
        if file_name == "STATUS.yaml" and path.exists():
            payload["documents"][file_name] = _normalize_status_for_fingerprint(_load_yaml(path))
            continue
        payload["documents"][file_name] = path.read_text(encoding="utf-8") if path.exists() else None
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _save_package_status(package: TaskPackage, status: dict[str, Any]) -> TaskPackage:
    _write_yaml(package.status_path, status)
    return TaskPackage(root=package.root, status=status, manifest=package.manifest, documents=package.documents)


def _status_flow(manifest: HarnessManifest) -> tuple[str, ...]:
    if manifest.allowed_statuses:
        return manifest.allowed_statuses
    return ("proposed", "requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying", "archived")


def _build_transition_candidate(package: TaskPackage, target_status: str) -> TaskPackage:
    candidate_status = copy.deepcopy(package.status)
    candidate_status["status"] = target_status
    candidate_status["updated_at"] = _current_date()
    return TaskPackage(root=package.root, status=candidate_status, manifest=package.manifest, documents=package.documents)


def _ensure_transition_allowed(package: TaskPackage, target_status: str) -> list[str]:
    flow = _status_flow(package.manifest)
    if target_status not in flow:
        return [f"unknown target status `{target_status}`; expected one of: {', '.join(flow)}"]
    if package.status_name == "archived":
        return [f"cannot transition archived package `{package.task_id}` out of `archived`"]
    if target_status == package.status_name:
        return []
    current_index = flow.index(package.status_name)
    target_index = flow.index(target_status)
    if target_index > current_index + 1:
        return [
            f"cannot skip forward from `{package.status_name}` to `{target_status}`; "
            f"next legal forward status is `{flow[current_index + 1]}`"
        ]
    if target_status == "archived" and package.status_name != "verifying":
        return ["can only transition to `archived` from `verifying`"]
    return []


def _latest_verification_artifact_path(package: TaskPackage) -> Path | None:
    verification = package.status.get("verification")
    if not isinstance(verification, dict):
        return None
    raw = str(verification.get("last_run_artifact") or "").strip()
    if not raw:
        return None
    return (package.manifest.repo_root / raw).resolve()


def _check_archive_preconditions(package: TaskPackage) -> list[str]:
    errors: list[str] = []
    artifact_path = _latest_verification_artifact_path(package)
    if artifact_path is None or not artifact_path.exists():
        errors.append("archiving requires an existing latest verification artifact")
        return errors
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    if artifact.get("overall_result") != "passed":
        errors.append("archiving requires the latest verification artifact result to be `passed`")
    if artifact.get("task_id") != package.task_id:
        errors.append("latest verification artifact does not match the task package id")
    current_fingerprint = compute_task_package_fingerprint(package)
    if artifact.get("package_fingerprint") != current_fingerprint:
        errors.append("latest verification artifact does not match the current task-package content")
    return errors


def _replace_package_prefix(text: str, package_name: str, archived: bool) -> str:
    active_prefix = f"docs/task-packages/{package_name}/"
    archived_prefix = f"docs/archived/task-packages/{package_name}/"
    if archived:
        return text.replace(active_prefix, archived_prefix)
    return text.replace(archived_prefix, active_prefix)


def _scan_repo_references(repo_root: Path, needle: str, ignore_roots: tuple[Path, ...]) -> list[Path]:
    hits: list[Path] = []
    ignore_resolved = {path.resolve() for path in ignore_roots if path.exists()}
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        if any(parent in ignore_resolved for parent in resolved.parents):
            continue
        if ".git" in resolved.parts:
            continue
        try:
            if needle in path.read_text(encoding="utf-8"):
                hits.append(path)
        except UnicodeDecodeError:
            continue
    return sorted(hits)


def _prepare_archived_copy(package: TaskPackage, temp_root: Path) -> TaskPackage:
    shutil.copytree(package.root, temp_root)
    for file_name in package.manifest.required_design_files:
        path = temp_root / file_name
        if not path.exists():
            continue
        if file_name == "STATUS.yaml":
            status = _load_yaml(path)
            status["status"] = "archived"
            status["updated_at"] = _current_date()
            _write_yaml(path, status)
            rewritten = _replace_package_prefix(path.read_text(encoding="utf-8"), package.name, archived=True)
            path.write_text(rewritten, encoding="utf-8")
            continue
        rewritten = _replace_package_prefix(path.read_text(encoding="utf-8"), package.name, archived=True)
        path.write_text(rewritten, encoding="utf-8")
    status = _load_yaml(temp_root / "STATUS.yaml")
    return TaskPackage(
        root=temp_root,
        status=status,
        manifest=package.manifest,
        documents={name: temp_root / name for name in package.manifest.required_design_files},
    )


def _archive_task_package(package: TaskPackage) -> tuple[bool, str]:
    target_root = package.manifest.archived_task_packages_root / package.name
    temp_root = package.manifest.archived_task_packages_root / f".{package.name}.tmp-archive"
    backup_root = package.manifest.task_packages_root / f".{package.name}.archive-backup"
    target_root.parent.mkdir(parents=True, exist_ok=True)
    if target_root.exists():
        return False, f"archive target already exists: {target_root}"
    if temp_root.exists():
        shutil.rmtree(temp_root)
    if backup_root.exists():
        shutil.rmtree(backup_root)
    _prepare_archived_copy(package, temp_root)
    try:
        package.root.rename(backup_root)
        temp_root.rename(target_root)
        archived_status = _load_yaml(target_root / "STATUS.yaml")
        archived_package = TaskPackage(
            root=target_root,
            status=archived_status,
            manifest=package.manifest,
            documents={name: target_root / name for name in package.manifest.required_design_files},
        )
        errors = validate_task_package(archived_package)
        if errors:
            invalid_root = package.manifest.archived_task_packages_root / f".{package.name}.invalid-archive"
            if invalid_root.exists():
                shutil.rmtree(invalid_root)
            target_root.rename(invalid_root)
            backup_root.rename(package.root)
            shutil.rmtree(invalid_root)
            return False, "\n".join(errors)
        shutil.rmtree(backup_root)
    except Exception as exc:
        if target_root.exists() and not package.root.exists():
            try:
                target_root.rename(package.root)
            except Exception:
                pass
        if backup_root.exists() and not package.root.exists():
            backup_root.rename(package.root)
        if temp_root.exists():
            shutil.rmtree(temp_root)
        return False, f"failed to archive package transactionally: {exc}"
    lingering = _scan_repo_references(
        package.manifest.repo_root,
        f"docs/task-packages/{package.name}/",
        ignore_roots=(target_root,),
    )
    if lingering:
        return True, "remaining repository references:\n" + "\n".join(str(path) for path in lingering)
    return True, ""


def _record_verification_artifact(
    package: TaskPackage,
    *,
    started_at: str,
    finished_at: str,
    overall_result: str,
    command_results: list[dict[str, Any]],
) -> Path:
    run_id = _utc_now().strftime("%Y%m%dT%H%M%S%fZ")
    artifact_root = package.manifest.repo_root / ".harness" / "artifacts" / package.task_id / "verification-runs"
    artifact_root.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_root / f"{run_id}.json"
    artifact = {
        "run_id": run_id,
        "task_id": package.task_id,
        "task_name": package.name,
        "title": package.title,
        "status_at_run": package.status_name,
        "started_at": started_at,
        "finished_at": finished_at,
        "package_fingerprint": compute_task_package_fingerprint(package),
        "required_commands_snapshot": list(package.required_commands),
        "required_scenarios_snapshot": list(package.required_scenarios),
        "command_results": command_results,
        "overall_result": overall_result,
    }
    artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest_path = artifact_root / "latest.json"
    latest_path.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")

    status = copy.deepcopy(package.status)
    verification = status.setdefault("verification", {})
    if isinstance(verification, dict):
        verification["last_run_at"] = finished_at
        verification["last_run_result"] = overall_result
        verification["last_run_artifact"] = str(artifact_path.relative_to(package.manifest.repo_root))
    status["updated_at"] = _current_date()
    _save_package_status(package, status)
    return artifact_path


def _run_command(repo_root: Path, command: str) -> int:
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True, cwd=repo_root)
    return completed.returncode


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
        print(f"- {summarize_task_package(package)}")
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
    task_root = create_task_package(
        TaskScaffoldRequest(
            repo_root=Path(args.repo).resolve(),
            task_name=args.task_name,
            task_id=args.task_id,
            title=args.title,
            owner=args.owner,
            summary=args.summary,
            status=args.status,
        )
    )
    print(f"Created task package: {task_root}")
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
        command_results: list[dict[str, Any]] = []
        overall_result = "passed"
        for command in package.required_commands:
            exit_code = _run_command(repo_root, command)
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Openharness repository workflow CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Inspect project harness entrypoints and task packages.")
    bootstrap_parser.add_argument("--repo", default=".", help="Repository root")
    bootstrap_parser.add_argument("--json", action="store_true", help="Print JSON output")
    bootstrap_parser.add_argument("--all", action="store_true", help="Include non-active task packages")
    bootstrap_parser.set_defaults(handler=cmd_bootstrap)

    check_parser = subparsers.add_parser(
        "check-tasks",
        help="Validate repository task packages against harness protocol.",
    )
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=cmd_check_tasks)

    new_design_parser = subparsers.add_parser(
        "new-task",
        help="Create a new task package from harness templates.",
    )
    new_design_parser.add_argument("task_name", help="Directory slug or human-readable task name")
    new_design_parser.add_argument("task_id", help="Stable task id, such as OR-016")
    new_design_parser.add_argument("title", help="Human-readable task title")
    new_design_parser.add_argument("--owner", default="unassigned", help="Initial owner")
    new_design_parser.add_argument("--summary", default="", help="Short summary")
    new_design_parser.add_argument("--status", default="proposed", help="Initial status")
    new_design_parser.add_argument("--repo", default=".", help="Repository root")
    new_design_parser.set_defaults(handler=cmd_new_task)

    transition_parser = subparsers.add_parser(
        "transition",
        help="Move a task package to a legal workflow status.",
    )
    transition_parser.add_argument("task", help="Task package name or task id")
    transition_parser.add_argument("target_status", help="Target workflow status")
    transition_parser.add_argument("--repo", default=".", help="Repository root")
    transition_parser.set_defaults(handler=cmd_transition)

    verify_parser = subparsers.add_parser("verify", help="Run harness verification for one task package or all active packages.")
    verify_parser.add_argument("design", nargs="?", default="", help="Task package name or task id")
    verify_parser.add_argument("--repo", default=".", help="Repository root")
    verify_parser.add_argument("--check-tasks-only", action="store_true", help="Only validate task package protocol")
    verify_parser.set_defaults(handler=cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
