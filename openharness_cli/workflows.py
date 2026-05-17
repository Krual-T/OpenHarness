from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from .models import TaskStatus, TaskType, Workflow

if TYPE_CHECKING:
    from .models import TaskPackage


# ═══════════════════════════════════════════════════════════════════════════════
# Per-file section requirements — used by Workflow.section_requirements()
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
# Stage descriptions
# ═══════════════════════════════════════════════════════════════════════════════

DESCRIPTIONS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: "Converging requirements — 01-requirements.md is not yet ready.",
    TaskStatus.REQUIREMENTS_DESIGNED: "Requirements converged; auto-advancing to next active state.",
    TaskStatus.OVERVIEW_DESIGNING: "Exploring and drafting overview design.",
    TaskStatus.OVERVIEW_DESIGNED: "Overview design complete; auto-advancing to detailed design.",
    TaskStatus.DETAILED_DESIGNING: "Drafting detailed design and implementation plan.",
    TaskStatus.DETAILED_DESIGNED: "Detailed design complete; auto-advancing to verification design.",
    TaskStatus.VERIFICATION_DESIGNING: "Designing verification strategy (TDD red phase).",
    TaskStatus.VERIFICATION_DESIGNED: "Verification strategy complete; auto-advancing to implementation.",
    TaskStatus.IMPLEMENTING: "Implementing against the verification plan (TDD green + refactor).",
    TaskStatus.IMPLEMENTED: "Implementation complete; auto-advancing to verification execution.",
    TaskStatus.VERIFYING: "Executing verification and collecting evidence.",
    TaskStatus.VERIFIED: "Verification complete; auto-advancing to archived.",
    TaskStatus.ARCHIVED: "Verification passed; package is archived and no longer active.",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Per-state next-step instructions
# ═══════════════════════════════════════════════════════════════════════════════

_PROPOSING_STEP = (
    "Converge requirements, determine task_type and verify_by, "
    "write `01-requirements.md`, then transition to `requirements_designed`."
)

STANDARD_NEXT_STEPS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: _PROPOSING_STEP,
    TaskStatus.REQUIREMENTS_DESIGNED: "Auto-advancing to `overview_designing`.",
    TaskStatus.OVERVIEW_DESIGNING: (
        "Complete overview design and reflection, "
        "then transition to `overview_designed`."
    ),
    TaskStatus.OVERVIEW_DESIGNED: "Auto-advancing to `detailed_designing`.",
    TaskStatus.DETAILED_DESIGNING: (
        "Complete detailed design, close design challenges, "
        "then transition to `detailed_designed`."
    ),
    TaskStatus.DETAILED_DESIGNED: "Auto-advancing to `verification_designing`.",
    TaskStatus.VERIFICATION_DESIGNING: (
        "Design verification strategy, write `verification_design.md`, "
        "then transition to `verification_designed`."
    ),
    TaskStatus.VERIFICATION_DESIGNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: (
        "Implement to pass verification, then transition to `implemented`."
    ),
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: (
        "Execute verification and write `evidence.md`, "
        "then transition to `verified`."
    ),
    TaskStatus.VERIFIED: "Auto-advancing to `archived`.",
    TaskStatus.ARCHIVED: "No next step. The package is complete and archived.",
}

MECHANICAL_NEXT_STEPS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: _PROPOSING_STEP,
    TaskStatus.REQUIREMENTS_DESIGNED: "Auto-advancing to `verification_designing`.",
    TaskStatus.VERIFICATION_DESIGNING: (
        "Design verification strategy, write `verification_design.md`, "
        "then transition to `verification_designed`."
    ),
    TaskStatus.VERIFICATION_DESIGNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: (
        "Implement to pass verification, then transition to `implemented`."
    ),
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: (
        "Execute verification and write `evidence.md`, "
        "then transition to `verified`."
    ),
    TaskStatus.VERIFIED: "Auto-advancing to `archived`.",
    TaskStatus.ARCHIVED: "No next step. The package is complete and archived.",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Gate precondition functions
# ═══════════════════════════════════════════════════════════════════════════════

def _check_requirements_gate(package: TaskPackage) -> list[str]:
    errors: list[str] = []
    if not package.task_type:
        errors.append(
            "task_type is not confirmed. "
            "Propose a classification (mechanical / standard development / protocol/architecture) "
            "and write it to task-info.yaml collaboration.task_type"
        )
    if not package.verify_by:
        errors.append(
            "verify_by is not determined. "
            "Determine the verification strategy (unit_test / qualitative / rwp) "
            "and write it to task-info.yaml verification.verify_by"
        )
    return errors


def _check_verified_gate(package: TaskPackage) -> list[str]:
    evidence_path = package.root / "evidence.md"
    if not evidence_path.exists():
        return ["evidence.md does not exist; write verification evidence first."]
    if not evidence_path.read_text(encoding="utf-8").strip():
        return ["evidence.md is empty; write verification evidence first."]
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# Concrete Workflow instances
# ═══════════════════════════════════════════════════════════════════════════════

STANDARD_WORKFLOW = Workflow(
    name="standard",
    status_sequence=(
        TaskStatus.PROPOSING,
        TaskStatus.REQUIREMENTS_DESIGNED,
        TaskStatus.OVERVIEW_DESIGNING,
        TaskStatus.OVERVIEW_DESIGNED,
        TaskStatus.DETAILED_DESIGNING,
        TaskStatus.DETAILED_DESIGNED,
        TaskStatus.VERIFICATION_DESIGNING,
        TaskStatus.VERIFICATION_DESIGNED,
        TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED,
        TaskStatus.VERIFYING,
        TaskStatus.VERIFIED,
        TaskStatus.ARCHIVED,
    ),
    gate_next={
        TaskStatus.REQUIREMENTS_DESIGNED: TaskStatus.OVERVIEW_DESIGNING,
        TaskStatus.OVERVIEW_DESIGNED: TaskStatus.DETAILED_DESIGNING,
        TaskStatus.DETAILED_DESIGNED: TaskStatus.VERIFICATION_DESIGNING,
        TaskStatus.VERIFICATION_DESIGNED: TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED: TaskStatus.VERIFYING,
        TaskStatus.VERIFIED: TaskStatus.ARCHIVED,
    },
    gate_preconditions={
        TaskStatus.REQUIREMENTS_DESIGNED: _check_requirements_gate,
        TaskStatus.VERIFIED: _check_verified_gate,
    },
    file_additions={
        TaskStatus.REQUIREMENTS_DESIGNED: ("01-requirements.md",),
        TaskStatus.OVERVIEW_DESIGNED: ("02-overview-design.md",),
        TaskStatus.DETAILED_DESIGNED: ("03-detailed-design.md",),
        TaskStatus.VERIFICATION_DESIGNED: ("verification_design.md",),
        TaskStatus.VERIFIED: ("evidence.md",),
    },
    section_specs=_FILE_SECTION_REQUIREMENTS,
    descriptions=DESCRIPTIONS,
    next_steps=STANDARD_NEXT_STEPS,
)

MECHANICAL_WORKFLOW = Workflow(
    name="mechanical",
    status_sequence=(
        TaskStatus.PROPOSING,
        TaskStatus.REQUIREMENTS_DESIGNED,
        TaskStatus.VERIFICATION_DESIGNING,
        TaskStatus.VERIFICATION_DESIGNED,
        TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED,
        TaskStatus.VERIFYING,
        TaskStatus.VERIFIED,
        TaskStatus.ARCHIVED,
    ),
    gate_next={
        TaskStatus.REQUIREMENTS_DESIGNED: TaskStatus.VERIFICATION_DESIGNING,
        TaskStatus.VERIFICATION_DESIGNED: TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED: TaskStatus.VERIFYING,
        TaskStatus.VERIFIED: TaskStatus.ARCHIVED,
    },
    gate_preconditions={
        TaskStatus.REQUIREMENTS_DESIGNED: _check_requirements_gate,
        TaskStatus.VERIFIED: _check_verified_gate,
    },
    file_additions={
        TaskStatus.REQUIREMENTS_DESIGNED: ("01-requirements.md",),
        TaskStatus.VERIFICATION_DESIGNED: ("verification_design.md",),
        TaskStatus.VERIFIED: ("evidence.md",),
    },
    section_specs=_FILE_SECTION_REQUIREMENTS,
    descriptions=DESCRIPTIONS,
    next_steps=MECHANICAL_NEXT_STEPS,
)


ACTIVE_STATUSES = frozenset(
    s.value for s in STANDARD_WORKFLOW.active_statuses | MECHANICAL_WORKFLOW.active_statuses
)

GATE_STATUSES = frozenset(
    s.value for s in STANDARD_WORKFLOW.gate_statuses | MECHANICAL_WORKFLOW.gate_statuses
)


def workflow_for(task_type: Optional[Union[TaskType, str]]) -> Workflow:
    if task_type is None:
        return STANDARD_WORKFLOW
    if isinstance(task_type, str):
        if task_type == TaskType.MECHANICAL.value:
            return MECHANICAL_WORKFLOW
        return STANDARD_WORKFLOW
    if task_type == TaskType.MECHANICAL:
        return MECHANICAL_WORKFLOW
    return STANDARD_WORKFLOW
