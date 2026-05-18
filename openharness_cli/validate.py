
from pathlib import Path
from typing import Optional

from .constants import (
    LABEL_ONLY_RE,
    PLACEHOLDER_BULLET_RE,
    PLACEHOLDER_NUMBERED_RE,
    REQUIRED_STATUS_KEYS,
)
from .models import DesignReviewMode, TaskPackage, TaskStatus, TaskType, VerifyBy, TaskPackageDocument


def _extract_markdown_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    target = heading.strip()
    start: Optional[int] = None
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
    wf = package.workflow
    status = package.info.status

    required_files = wf.required_files(status)

    for doc in required_files:
        if not doc.path_from(package.root).exists():
            errors.append(f"missing required file for `{package.current_status}`: {doc.path_from(package.root)}")
    for key in REQUIRED_STATUS_KEYS:
        value = package.info.to_dict().get(key)
        if value in (None, "", []):
            errors.append(f"missing required key `{key}` in {TaskPackageDocument.TASK_INFO.path_from(package.root)}")

    # Validate task_type if present
    if package.task_type and package.task_type not in {t.value for t in TaskType}:
        errors.append(
            f"unknown collaboration.task_type `{package.task_type}` in {TaskPackageDocument.TASK_INFO.path_from(package.root)}; "
            f"expected one of: {', '.join(sorted(t.value for t in TaskType))}"
        )

    # Validate design_review_mode if present
    design_review_mode = package.design_review_mode
    if design_review_mode and design_review_mode not in {drm.value for drm in DesignReviewMode}:
        errors.append(
            f"unknown collaboration.design_review_mode `{design_review_mode}` in {TaskPackageDocument.TASK_INFO.path_from(package.root)}; "
            f"expected `stepwise` or `auto`"
        )

    # Validate verify_by if present
    if package.verify_by and package.verify_by not in {v.value for v in VerifyBy}:
        errors.append(
            f"unknown verification.verify_by `{package.verify_by}` in {TaskPackageDocument.TASK_INFO.path_from(package.root)}; "
            f"expected one of: {', '.join(sorted(v.value for v in VerifyBy))}"
        )

    verification = package.info.to_dict().get("verification")
    if verification is not None and not isinstance(verification, dict):
        errors.append(f"`verification` must be a mapping in {TaskPackageDocument.TASK_INFO.path_from(package.root)}")

    valid_status_values = {s.value for s in wf.status_sequence}
    if package.current_status not in valid_status_values:
        errors.append(
            f"unknown status `{package.current_status}` in {TaskPackageDocument.TASK_INFO.path_from(package.root)}; "
            f"expected one of: {', '.join(sorted(valid_status_values))}"
        )
    if package.current_status == "archived":
        if package.root.resolve().parent != package.config.archived_task_packages_root:
            errors.append(
                f"archived package must live under {package.config.archived_task_packages_root}: {package.root}"
            )
    elif package.root.resolve().parent == package.config.archived_task_packages_root:
        errors.append(
            f"non-archived package must not live under {package.config.archived_task_packages_root}: {package.root}"
        )
    if package.current_status != "archived":
        for doc, heading in wf.section_requirements(status):
            path = doc.path_from(package.root)
            if not _section_has_meaningful_content(path, heading):
                errors.append(
                    f"{package.current_status} requires non-placeholder content for `{heading}` in {path}"
                )
    return errors
