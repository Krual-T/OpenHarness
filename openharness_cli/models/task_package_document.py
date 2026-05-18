from __future__ import annotations

from enum import StrEnum
from pathlib import Path


class TaskPackageDocument(StrEnum):
    README = ("README.md", True, ("## Overview",))
    TASK_INFO = ("task-info.yaml", True, ())
    REQUIREMENTS = ("01-requirements.md", False, (
        "## Goal", "## Problem Statement", "## Required Outcomes", "## Constraints",
    ))
    OVERVIEW_DESIGN = ("02-overview-design.md", False, (
        "## System Boundary", "## Proposed Structure", "## Key Flows",
        "## Stage Gates", "## Trade-offs", "## Overview Reflection",
    ))
    DETAILED_DESIGN = ("03-detailed-design.md", False, (
        "## Runtime Verification Plan", "## Files Added Or Changed",
        "## Interfaces", "## Module Internals", "## Data Semantics",
        "## Decision Closure", "## Error Handling", "## Migration Notes",
        "## Detailed Reflection",
    ))
    VERIFICATION_DESIGN = ("verification_design.md", False, (
        "## Verification Path", "## Required Commands", "## Expected Outcomes",
        "## Traceability", "## Risk Acceptance",
    ))
    EVIDENCE = ("evidence.md", False, (
        "## Verification Result", "## Files", "## Residual Risks",
    ))

    def __new__(cls, filename: str, is_base: bool, sections: tuple[str, ...]):
        obj = str.__new__(cls, filename)
        obj._value_ = filename
        obj.is_base = is_base
        obj.sections = sections
        return obj

    def path_from(self, root: Path) -> Path:
        return root / self.value

    @classmethod
    def base_files(cls) -> tuple[TaskPackageDocument, ...]:
        return tuple(d for d in cls if d.is_base)

    @classmethod
    def section_specs(cls) -> dict[TaskPackageDocument, tuple[tuple[TaskPackageDocument, str], ...]]:
        return {
            d: tuple((d, h) for h in d.sections)
            for d in cls
            if d.sections
        }
