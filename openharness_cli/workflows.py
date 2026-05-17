from __future__ import annotations

from .domain import TaskStatus, TaskType, Workflow, _FILE_SECTION_REQUIREMENTS  # noqa: F401 — used by Workflow.section_requirements


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

def _check_requirements_gate(package: object) -> list[str]:
    errors: list[str] = []
    task_type = getattr(package, "task_type", "")
    verify_by = getattr(package, "verify_by", "")
    if not task_type:
        errors.append(
            "task_type is not confirmed. "
            "Propose a classification (mechanical / standard development / protocol/architecture) "
            "and write it to task-info.yaml collaboration.task_type"
        )
    if not verify_by:
        errors.append(
            "verify_by is not determined. "
            "Determine the verification strategy (unit_test / qualitative / rwp) "
            "and write it to task-info.yaml verification.verify_by"
        )
    return errors


def _check_verified_gate(package: object) -> list[str]:
    root = getattr(package, "root", None)
    if root is None:
        return ["cannot verify: package has no root"]
    from pathlib import Path
    evidence_path = Path(root) / "evidence.md"
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
    descriptions=DESCRIPTIONS,
    next_steps=MECHANICAL_NEXT_STEPS,
)


def workflow_for(task_type: TaskType | str | None) -> Workflow:
    if task_type is None:
        return STANDARD_WORKFLOW
    if isinstance(task_type, str):
        if task_type == TaskType.MECHANICAL.value:
            return MECHANICAL_WORKFLOW
        return STANDARD_WORKFLOW
    if task_type == TaskType.MECHANICAL:
        return MECHANICAL_WORKFLOW
    return STANDARD_WORKFLOW
