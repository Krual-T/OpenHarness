from __future__ import annotations

import re


ACTIVE_STATUSES = {"proposed", "requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying"}
VERIFYABLE_STATUSES = {"in_progress", "verifying"}
REQUIRED_TASK_PACKAGE_FILES = (
    "README.md",
    "STATUS.yaml",
    "01-requirements.md",
    "02-overview-design.md",
    "03-detailed-design.md",
    "04-verification.md",
    "05-evidence.md",
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
TASK_ID_RE = re.compile(r"^([A-Za-z]+)-(\d+)$")

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
        ("05-evidence.md", "## Files"),
        ("05-evidence.md", "## Commands"),
        ("05-evidence.md", "## Residual Risks"),
    ),
}

STATUS_LABEL_REQUIREMENTS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "verifying": (
        ("04-verification.md", "## Verification Path", "Planned Path"),
        ("04-verification.md", "## Verification Path", "Executed Path"),
        ("04-verification.md", "## Latest Result", ""),
    ),
    "archived": (
        ("04-verification.md", "## Verification Path", "Planned Path"),
        ("04-verification.md", "## Verification Path", "Executed Path"),
        ("04-verification.md", "## Latest Result", ""),
    ),
}
