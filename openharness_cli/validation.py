from __future__ import annotations

from pathlib import Path

from .constants import (
    LABEL_ONLY_RE,
    PLACEHOLDER_BULLET_RE,
    PLACEHOLDER_NUMBERED_RE,
    REQUIRED_STATUS_KEYS,
    STATUS_LABEL_REQUIREMENTS,
    STATUS_SECTION_REQUIREMENTS,
    VERIFICATION_RESULT_VALUES,
)
from .models import TaskPackage


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


def _referenced_path_exists(package: TaskPackage, raw_path: object) -> bool:
    repo_root = package.manifest.repo_root
    normalized = str(raw_path)
    direct_path = (repo_root / normalized).resolve()
    if direct_path.exists():
        return True
    if package.status_name != "archived":
        return False
    legacy_path = (repo_root / "docs" / "archived" / "legacy" / normalized).resolve()
    return legacy_path.exists()


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
            if not _referenced_path_exists(package, last_run_artifact):
                errors.append(
                    f"missing referenced path `{last_run_artifact}` in {package.root / 'STATUS.yaml'}"
                )

    for key in ("entrypoints",):
        raw_paths = package.status.get(key)
        if isinstance(raw_paths, list):
            for raw_path in raw_paths:
                if not _referenced_path_exists(package, raw_path):
                    errors.append(f"missing referenced path `{raw_path}` in {package.root / 'STATUS.yaml'}")

    if isinstance(evidence, dict):
        for group in ("docs", "code", "tests"):
            raw_paths = evidence.get(group)
            if isinstance(raw_paths, list):
                for raw_path in raw_paths:
                    if not _referenced_path_exists(package, raw_path):
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
