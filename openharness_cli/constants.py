from __future__ import annotations

import re

DEFAULT_STATUS_FLOW = (
    "proposing",
    "requirements_designed",
    "overview_designing",
    "overview_designed",
    "detailed_designing",
    "detailed_designed",
    "implementing",
    "implemented",
    "verifying",
    "archived",
)

ACTIVE_STATUSES = {
    "proposing",
    "requirements_designed",
    "overview_designing",
    "overview_designed",
    "detailed_designing",
    "detailed_designed",
    "implementing",
    "implemented",
    "verifying",
}
VERIFYABLE_STATUSES = {"implementing", "implemented", "verifying"}
REQUIRED_TASK_PACKAGE_FILES = (
    "README.md",
    "STATUS.yaml",
    "01-requirements.md",
    "02-overview-design.md",
    "03-detailed-design.md",
    "04-verification.md",
    "05-evidence.md",
)

# Mechanical tasks use a shorter status flow, skipping overview/detailed design stages.
MECHANICAL_STATUS_FLOW = (
    "proposing",
    "requirements_designed",
    "implementing",
    "verifying",
    "archived",
)

_FILE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "requirements_designed": ("01-requirements.md",),
    "overview_designed": ("02-overview-design.md",),
    "detailed_designed": ("03-detailed-design.md",),
    "verifying": ("04-verification.md",),
    "archived": ("05-evidence.md",),
}

_MECHANICAL_FILE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "requirements_designed": ("01-requirements.md",),
    "implementing": (),
    "verifying": ("04-verification.md",),
    "archived": ("05-evidence.md",),
}


def _build_status_required_files() -> dict[str, tuple[str, ...]]:
    base = ("README.md", "STATUS.yaml")
    result: dict[str, tuple[str, ...]] = {}
    accumulated = list(base)
    for status in DEFAULT_STATUS_FLOW:
        accumulated.extend(_FILE_ADDITIONS.get(status, ()))
        result[status] = tuple(accumulated)
    return result


def _build_mechanical_status_required_files() -> dict[str, tuple[str, ...]]:
    base = ("README.md", "STATUS.yaml")
    result: dict[str, tuple[str, ...]] = {}
    accumulated = list(base)
    for status in MECHANICAL_STATUS_FLOW:
        accumulated.extend(_MECHANICAL_FILE_ADDITIONS.get(status, ()))
        result[status] = tuple(accumulated)
    return result


STATUS_REQUIRED_FILES = _build_status_required_files()
MECHANICAL_STATUS_REQUIRED_FILES = _build_mechanical_status_required_files()
del _build_status_required_files, _build_mechanical_status_required_files, _FILE_ADDITIONS, _MECHANICAL_FILE_ADDITIONS

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

TASK_TYPE_VALUES = {"mechanical", "standard development", "protocol/architecture"}
VERIFICATION_RESULT_VALUES = {"passed", "failed", "insufficient_verification"}

PLACEHOLDER_BULLET_RE = re.compile(r"^[-*]\s*$")
PLACEHOLDER_NUMBERED_RE = re.compile(r"^\d+\.\s*$")
LABEL_ONLY_RE = re.compile(r"^[-*]\s+[^:]+:\s*$")
TASK_ID_RE = re.compile(r"^([A-Za-z]+)-(\d+)$")

_SECTION_REQS_BASE = (
    ("01-requirements.md", "## Goal"),
    ("01-requirements.md", "## Problem Statement"),
    ("01-requirements.md", "## Required Outcomes"),
    ("01-requirements.md", "## Constraints"),
)

_SECTION_REQS_OVERVIEW = _SECTION_REQS_BASE + (
    ("02-overview-design.md", "## System Boundary"),
    ("02-overview-design.md", "## Proposed Structure"),
    ("02-overview-design.md", "## Key Flows"),
    ("02-overview-design.md", "## Stage Gates"),
    ("02-overview-design.md", "## Trade-offs"),
    ("02-overview-design.md", "## Overview Reflection"),
)

_SECTION_REQS_DETAILED = _SECTION_REQS_OVERVIEW + (
    ("03-detailed-design.md", "## Runtime Verification Plan"),
    ("03-detailed-design.md", "## Files Added Or Changed"),
    ("03-detailed-design.md", "## Interfaces"),
    ("03-detailed-design.md", "## Module Internals"),
    ("03-detailed-design.md", "## Data Semantics"),
    ("03-detailed-design.md", "## Decision Closure"),
    ("03-detailed-design.md", "## Error Handling"),
    ("03-detailed-design.md", "## Migration Notes"),
    ("03-detailed-design.md", "## Detailed Reflection"),
)

_SECTION_REQS_ARCHIVED = _SECTION_REQS_DETAILED + (
    ("05-evidence.md", "## Files"),
    ("05-evidence.md", "## Commands"),
    ("05-evidence.md", "## Residual Risks"),
)

# Mechanical tasks skip overview/detailed design; evidence sections still required.
_SECTION_REQS_ARCHIVED_MECHANICAL = _SECTION_REQS_BASE + (
    ("05-evidence.md", "## Files"),
    ("05-evidence.md", "## Commands"),
    ("05-evidence.md", "## Residual Risks"),
)

STATUS_SECTION_REQUIREMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "proposing": (
        ("README.md", "## Overview"),
    ),
    "requirements_designed": _SECTION_REQS_BASE,
    "overview_designing": _SECTION_REQS_BASE,
    "overview_designed": _SECTION_REQS_OVERVIEW,
    "detailed_designing": _SECTION_REQS_OVERVIEW,
    "detailed_designed": _SECTION_REQS_DETAILED,
    "implementing": _SECTION_REQS_DETAILED,
    "implemented": _SECTION_REQS_DETAILED,
    "verifying": _SECTION_REQS_DETAILED,
    "archived": _SECTION_REQS_ARCHIVED,
}

MECHANICAL_STATUS_SECTION_REQUIREMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "proposing": (
        ("README.md", "## Overview"),
    ),
    "requirements_designed": _SECTION_REQS_BASE,
    "implementing": _SECTION_REQS_BASE,
    "verifying": _SECTION_REQS_BASE,
    "archived": _SECTION_REQS_ARCHIVED_MECHANICAL,
}

_STATUS_LABEL_BASE = (
    ("04-verification.md", "## Verification Path", "Planned Path"),
    ("04-verification.md", "## Verification Path", "Executed Path"),
    ("04-verification.md", "## Latest Result", ""),
)

STATUS_LABEL_REQUIREMENTS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "verifying": _STATUS_LABEL_BASE,
    "archived": _STATUS_LABEL_BASE,
}

MECHANICAL_STATUS_LABEL_REQUIREMENTS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "verifying": _STATUS_LABEL_BASE,
    "archived": _STATUS_LABEL_BASE,
}
