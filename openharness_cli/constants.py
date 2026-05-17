from __future__ import annotations

import re

# All _designed / verified states are gate states: CLI auto-advances through them
# after checking required fields / documents.
DEFAULT_STATUS_FLOW = (
    "proposing",
    "requirements_designed",
    "overview_designing",
    "overview_designed",
    "detailed_designing",
    "detailed_designed",
    "verification_designing",
    "verification_designed",
    "implementing",
    "implemented",
    "verifying",
    "verified",
    "archived",
)

ACTIVE_STATUSES = {
    "proposing",
    "overview_designing",
    "detailed_designing",
    "verification_designing",
    "implementing",
    "verifying",
}

GATE_STATUSES = {
    "requirements_designed",
    "overview_designed",
    "detailed_designed",
    "verification_designed",
    "implemented",
    "verified",
}

REQUIRED_TASK_PACKAGE_FILES = (
    "README.md",
    "STATUS.yaml",
    "01-requirements.md",
    "02-overview-design.md",
    "03-detailed-design.md",
    "verification_design.md",
    "evidence.md",
)

# Mechanical tasks use a shorter status flow, skipping overview/detailed design.
MECHANICAL_STATUS_FLOW = (
    "proposing",
    "requirements_designed",
    "verification_designing",
    "verification_designed",
    "implementing",
    "implemented",
    "verifying",
    "verified",
    "archived",
)

_FILE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "requirements_designed": ("01-requirements.md",),
    "overview_designed": ("02-overview-design.md",),
    "detailed_designed": ("03-detailed-design.md",),
    "verification_designed": ("verification_design.md",),
    "verified": ("evidence.md",),
}

_MECHANICAL_FILE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "requirements_designed": ("01-requirements.md",),
    "verification_designed": ("verification_design.md",),
    "verified": ("evidence.md",),
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
VERIFY_BY_VALUES = {"unit_test", "qualitative", "rwp"}

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

_SECTION_REQS_VERIFICATION = _SECTION_REQS_DETAILED + (
    ("verification_design.md", "## Verification Path"),
    ("verification_design.md", "## Required Commands"),
    ("verification_design.md", "## Expected Outcomes"),
    ("verification_design.md", "## Traceability"),
    ("verification_design.md", "## Risk Acceptance"),
)

_SECTION_REQS_VERIFIED = _SECTION_REQS_VERIFICATION + (
    ("evidence.md", "## Verification Result"),
    ("evidence.md", "## Files"),
    ("evidence.md", "## Residual Risks"),
)

# Mechanical tasks skip overview/detailed design.
_SECTION_REQS_VERIFICATION_MECHANICAL = _SECTION_REQS_BASE + (
    ("verification_design.md", "## Verification Path"),
    ("verification_design.md", "## Required Commands"),
    ("verification_design.md", "## Expected Outcomes"),
    ("verification_design.md", "## Traceability"),
    ("verification_design.md", "## Risk Acceptance"),
)

_SECTION_REQS_VERIFIED_MECHANICAL = _SECTION_REQS_VERIFICATION_MECHANICAL + (
    ("evidence.md", "## Verification Result"),
    ("evidence.md", "## Files"),
    ("evidence.md", "## Residual Risks"),
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
    "verification_designing": _SECTION_REQS_DETAILED,
    "verification_designed": _SECTION_REQS_VERIFICATION,
    "implementing": _SECTION_REQS_VERIFICATION,
    "verifying": _SECTION_REQS_VERIFICATION,
    "verified": _SECTION_REQS_VERIFIED,
    "archived": _SECTION_REQS_VERIFIED,
}

MECHANICAL_STATUS_SECTION_REQUIREMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "proposing": (
        ("README.md", "## Overview"),
    ),
    "requirements_designed": _SECTION_REQS_BASE,
    "verification_designing": _SECTION_REQS_BASE,
    "verification_designed": _SECTION_REQS_VERIFICATION_MECHANICAL,
    "implementing": _SECTION_REQS_VERIFICATION_MECHANICAL,
    "verifying": _SECTION_REQS_VERIFICATION_MECHANICAL,
    "verified": _SECTION_REQS_VERIFIED_MECHANICAL,
    "archived": _SECTION_REQS_VERIFIED_MECHANICAL,
}

# Hook mapping: active state → skill file read and output by CLI on transition.
STATE_SKILL_HOOKS: dict[str, str] = {
    "proposing":               "skills/using-openharness/states/brainstorming/SKILL.md",
    "overview_designing":      "skills/using-openharness/states/exploring-solution-space/SKILL.md",
    "detailed_designing":      "skills/using-openharness/states/detailed-design/SKILL.md",
    "verification_designing":  "skills/using-openharness/states/verification-designing/SKILL.md",
    "implementing":            "skills/using-openharness/states/implementing/SKILL.md",
    "verifying":               "skills/using-openharness/states/verifying/SKILL.md",
    "archived":                "skills/using-openharness/states/finishing-a-development-branch/SKILL.md",
}
