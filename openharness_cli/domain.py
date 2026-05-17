from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Callable


# ═══════════════════════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════════════════════

class TaskStatus(StrEnum):
    PROPOSING = ("proposing", "skills/using-openharness/states/brainstorming/SKILL.md")
    REQUIREMENTS_DESIGNED = ("requirements_designed", "")
    OVERVIEW_DESIGNING = ("overview_designing", "skills/using-openharness/states/exploring-solution-space/SKILL.md")
    OVERVIEW_DESIGNED = ("overview_designed", "")
    DETAILED_DESIGNING = ("detailed_designing", "skills/using-openharness/states/detailed-design/SKILL.md")
    DETAILED_DESIGNED = ("detailed_designed", "")
    VERIFICATION_DESIGNING = ("verification_designing", "skills/using-openharness/states/verification-designing/SKILL.md")
    VERIFICATION_DESIGNED = ("verification_designed", "")
    IMPLEMENTING = ("implementing", "skills/using-openharness/states/implementing/SKILL.md")
    IMPLEMENTED = ("implemented", "")
    VERIFYING = ("verifying", "skills/using-openharness/states/verifying/SKILL.md")
    VERIFIED = ("verified", "")
    ARCHIVED = ("archived", "skills/using-openharness/states/finishing-a-development-branch/SKILL.md")

    def __new__(cls, value, hook):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.hook = hook
        return obj


class TaskType(StrEnum):
    MECHANICAL = "mechanical"
    STANDARD = "standard development"
    PROTOCOL = "protocol/architecture"


class VerifyBy(StrEnum):
    UNIT_TEST = "unit_test"
    QUALITATIVE = "qualitative"
    RWP = "rwp"


class DesignReviewMode(StrEnum):
    STEPWISE = "stepwise"
    AUTO = "auto"


# ═══════════════════════════════════════════════════════════════════════════════
# Typed status data model
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CollaborationInfo:
    task_type: str | None = None
    design_review_mode: str | None = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> CollaborationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        return cls(
            task_type=str(raw.pop("task_type", "")).strip() or None,
            design_review_mode=str(raw.pop("design_review_mode", "")).strip() or None,
            _extra=raw,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.task_type is not None:
            result["task_type"] = self.task_type
        if self.design_review_mode is not None:
            result["design_review_mode"] = self.design_review_mode
        return result


@dataclass
class VerificationInfo:
    verify_by: str | None = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> VerificationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        return cls(
            verify_by=str(raw.pop("verify_by", "")).strip() or None,
            _extra=raw,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.verify_by is not None:
            result["verify_by"] = self.verify_by
        return result


@dataclass
class TaskInfo:
    id: str
    title: str
    status: TaskStatus
    summary: str
    owner: str
    created_at: str
    updated_at: str
    done_criteria: tuple[str, ...] = ()
    entrypoints: tuple[str, ...] = ()
    collaboration: CollaborationInfo | None = None
    verification: VerificationInfo | None = None
    _raw_status: str | None = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @property
    def status_value(self) -> str:
        if self._raw_status is not None:
            return self._raw_status
        return self.status.value

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskInfo:
        raw = dict(d)

        status_raw = str(raw.pop("status", "")).strip()
        _raw_status: str | None = None
        if status_raw:
            try:
                status = TaskStatus(status_raw)
            except ValueError:
                status = TaskStatus.PROPOSING
                _raw_status = status_raw
        else:
            status = TaskStatus.PROPOSING

        collab_raw = raw.pop("collaboration", None)
        collaboration = CollaborationInfo.from_dict(collab_raw) if isinstance(collab_raw, dict) else None

        verif_raw = raw.pop("verification", None)
        verification = VerificationInfo.from_dict(verif_raw) if isinstance(verif_raw, dict) else None

        done_raw = raw.pop("done_criteria", None)
        done_criteria: tuple[str, ...] = ()
        if isinstance(done_raw, list):
            done_criteria = tuple(str(item).strip() for item in done_raw if str(item).strip())

        ep_raw = raw.pop("entrypoints", None)
        entrypoints: tuple[str, ...] = ()
        if isinstance(ep_raw, list):
            entrypoints = tuple(str(item).strip() for item in ep_raw if str(item).strip())

        return cls(
            id=str(raw.pop("id", "")).strip(),
            title=str(raw.pop("title", "")).strip(),
            status=status,
            summary=str(raw.pop("summary", "")).strip(),
            owner=str(raw.pop("owner", "")).strip(),
            created_at=str(raw.pop("created_at", "")).strip(),
            updated_at=str(raw.pop("updated_at", "")).strip(),
            done_criteria=done_criteria,
            entrypoints=entrypoints,
            collaboration=collaboration,
            verification=verification,
            _raw_status=_raw_status,
            _extra=raw,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        result["id"] = self.id
        result["title"] = self.title
        result["status"] = self.status_value
        result["summary"] = self.summary
        result["owner"] = self.owner
        result["created_at"] = self.created_at
        result["updated_at"] = self.updated_at
        if self.done_criteria:
            result["done_criteria"] = list(self.done_criteria)
        if self.entrypoints:
            result["entrypoints"] = list(self.entrypoints)
        if self.collaboration is not None:
            result["collaboration"] = self.collaboration.to_dict()
        if self.verification is not None:
            result["verification"] = self.verification.to_dict()
        for k, v in self._extra.items():
            result[k] = v
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# Per-file section requirements — used to compute cumulative section_requirements
# ═══════════════════════════════════════════════════════════════════════════════

_FILE_SECTION_REQUIREMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "01-requirements.md": (
        ("01-requirements.md", "## Goal"),
        ("01-requirements.md", "## Problem Statement"),
        ("01-requirements.md", "## Required Outcomes"),
        ("01-requirements.md", "## Constraints"),
    ),
    "02-overview-design.md": (
        ("02-overview-design.md", "## System Boundary"),
        ("02-overview-design.md", "## Proposed Structure"),
        ("02-overview-design.md", "## Key Flows"),
        ("02-overview-design.md", "## Stage Gates"),
        ("02-overview-design.md", "## Trade-offs"),
        ("02-overview-design.md", "## Overview Reflection"),
    ),
    "03-detailed-design.md": (
        ("03-detailed-design.md", "## Runtime Verification Plan"),
        ("03-detailed-design.md", "## Files Added Or Changed"),
        ("03-detailed-design.md", "## Interfaces"),
        ("03-detailed-design.md", "## Module Internals"),
        ("03-detailed-design.md", "## Data Semantics"),
        ("03-detailed-design.md", "## Decision Closure"),
        ("03-detailed-design.md", "## Error Handling"),
        ("03-detailed-design.md", "## Migration Notes"),
        ("03-detailed-design.md", "## Detailed Reflection"),
    ),
    "verification_design.md": (
        ("verification_design.md", "## Verification Path"),
        ("verification_design.md", "## Required Commands"),
        ("verification_design.md", "## Expected Outcomes"),
        ("verification_design.md", "## Traceability"),
        ("verification_design.md", "## Risk Acceptance"),
    ),
    "evidence.md": (
        ("evidence.md", "## Verification Result"),
        ("evidence.md", "## Files"),
        ("evidence.md", "## Residual Risks"),
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# Workflow — state machine definition for a task-package pipeline
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Workflow:
    name: str
    status_sequence: tuple[TaskStatus, ...]
    gate_next: dict[TaskStatus, TaskStatus]
    gate_preconditions: dict[TaskStatus, Callable[..., list[str]]]
    file_additions: dict[TaskStatus, tuple[str, ...]]
    descriptions: dict[TaskStatus, str]
    next_steps: dict[TaskStatus, str]

    @property
    def gate_statuses(self) -> frozenset[TaskStatus]:
        return frozenset(self.gate_next)

    @property
    def active_statuses(self) -> frozenset[TaskStatus]:
        return frozenset(
            s for s in self.status_sequence
            if s not in self.gate_next and s != TaskStatus.ARCHIVED
        )

    def next_status(self, current: TaskStatus) -> TaskStatus | None:
        if current not in self.status_sequence:
            return None
        idx = self.status_sequence.index(current)
        if idx >= len(self.status_sequence) - 1:
            return None
        return self.status_sequence[idx + 1]

    def required_files(self, status: TaskStatus) -> tuple[str, ...]:
        base = ("README.md", "task-info.yaml")
        accumulated = list(base)
        for s in self.status_sequence:
            accumulated.extend(self.file_additions.get(s, ()))
            if s == status:
                break
        return tuple(accumulated)

    def section_requirements(self, status: TaskStatus) -> tuple[tuple[str, str], ...]:
        """Cumulative section requirements up to *status*, computed from file_additions."""
        sections: list[tuple[str, str]] = [("README.md", "## Overview")]
        accumulated_files: set[str] = set()
        for s in self.status_sequence:
            for f in self.file_additions.get(s, ()):
                accumulated_files.add(f)
                if f in _FILE_SECTION_REQUIREMENTS:
                    sections.extend(_FILE_SECTION_REQUIREMENTS[f])
            if s == status:
                break
        return tuple(sections)

    def resolve_gate(self, package: object, target: TaskStatus) -> tuple[TaskStatus | None, list[str]]:
        next_s = self.gate_next.get(target)
        if next_s is None:
            return None, []
        precond = self.gate_preconditions.get(target)
        if precond is not None:
            errors = precond(package)
            if errors:
                return None, errors
        return next_s, []

