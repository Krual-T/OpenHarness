from typing import Optional, Union

from .models import TaskPackage, TaskPackageDocument, TaskStatus, TaskType, Workflow


# ═══════════════════════════════════════════════════════════════════════════════
# Per-file section requirements — used by Workflow.section_requirements()
# ═══════════════════════════════════════════════════════════════════════════════

_FILE_SECTION_REQUIREMENTS = TaskPackageDocument.section_specs()


# ═══════════════════════════════════════════════════════════════════════════════
# Stage descriptions
# ═══════════════════════════════════════════════════════════════════════════════

DESCRIPTIONS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: f"Converging requirements — {TaskPackageDocument.REQUIREMENTS.value} is not yet ready.",
    TaskStatus.REQUIREMENTS_DESIGNED: "Requirements converged; auto-advancing to next active state.",
    TaskStatus.OVERVIEW_DESIGNING: "Exploring and drafting overview design.",
    TaskStatus.OVERVIEW_DESIGNED: "Overview design complete; auto-advancing to detailed design.",
    TaskStatus.DETAILED_DESIGNING: "Drafting detailed design.",
    TaskStatus.DETAILED_DESIGNED: "Detailed design complete; auto-advancing to planning.",
    TaskStatus.PLANNING: "Drafting implementation plan and verification design.",
    TaskStatus.PLANNED: "Plan complete; auto-advancing to implementation.",
    TaskStatus.IMPLEMENTING: "Implementing against the plan.",
    TaskStatus.IMPLEMENTED: "Implementation complete; auto-advancing to verification execution.",
    TaskStatus.VERIFYING: "Executing verification and collecting evidence.",
    TaskStatus.VERIFIED: "Verification complete; auto-advancing to archived.",
    TaskStatus.ARCHIVED: "Verification passed; package is archived and no longer active.",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Per-state next-step instructions
# ═══════════════════════════════════════════════════════════════════════════════

_PROPOSING_STEP = (
    "Converge requirements, determine task_type, verification method, and RWP setting, "
    f"write `{TaskPackageDocument.REQUIREMENTS.value}`, then transition to `requirements_designed`."
)

_IMPLEMENT_STEP = "Implement to pass the plan, then transition to `implemented`."

_VERIFY_STEP = (
    f"Execute verification and write `{TaskPackageDocument.EVIDENCE.value}`, "
    "then transition to `verified`."
)

MECHANICAL_NEXT_STEPS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: _PROPOSING_STEP,
    TaskStatus.REQUIREMENTS_DESIGNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: _IMPLEMENT_STEP,
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: _VERIFY_STEP,
    TaskStatus.VERIFIED: "Auto-advancing to `archived`.",
    TaskStatus.ARCHIVED: "No next step. The package is complete and archived.",
}

STANDARD_NEXT_STEPS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: _PROPOSING_STEP,
    TaskStatus.REQUIREMENTS_DESIGNED: "Auto-advancing to `planning`.",
    TaskStatus.PLANNING: (
        f"Write `{TaskPackageDocument.PLAN.value}` with implementation steps and verification design, "
        "then transition to `planned`."
    ),
    TaskStatus.PLANNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: _IMPLEMENT_STEP,
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: _VERIFY_STEP,
    TaskStatus.VERIFIED: "Auto-advancing to `archived`.",
    TaskStatus.ARCHIVED: "No next step. The package is complete and archived.",
}

STRUCTURAL_NEXT_STEPS: dict[TaskStatus, str] = {
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
    TaskStatus.DETAILED_DESIGNED: "Auto-advancing to `planning`.",
    TaskStatus.PLANNING: (
        f"Write `{TaskPackageDocument.PLAN.value}` with implementation steps and verification design, "
        "then transition to `planned`."
    ),
    TaskStatus.PLANNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: _IMPLEMENT_STEP,
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: _VERIFY_STEP,
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
            "Propose a classification (mechanical / standard / structural) "
            "and write it to task-info.yaml collaboration.task_type"
        )
    if not package.verification_method:
        errors.append(
            "verification method is not determined. "
            "Determine the verification method (unit_test / qualitative) "
            "and write it to task-info.yaml verification.method"
        )
    if not package.rwp_enabled:
        errors.append(
            "RWP setting is not confirmed. "
            "Confirm whether runtime workflow evidence is enabled "
            "and write it to task-info.yaml verification.rwp.enabled"
        )
    if package.rwp_enabled and not package.rwp_reason:
        errors.append(
            "RWP reason is not documented. "
            "Write the reason to task-info.yaml verification.rwp.reason"
        )
    return errors


def _check_verified_gate(package: TaskPackage) -> list[str]:
    evidence_path = TaskPackageDocument.EVIDENCE.path_from(package.root)
    if not evidence_path.exists():
        return [f"{TaskPackageDocument.EVIDENCE.value} does not exist; write verification evidence first."]
    if not evidence_path.read_text(encoding="utf-8").strip():
        return [f"{TaskPackageDocument.EVIDENCE.value} is empty; write verification evidence first."]
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# Concrete Workflow instances
# ═══════════════════════════════════════════════════════════════════════════════

MECHANICAL_WORKFLOW = Workflow(
    name="mechanical",
    status_sequence=(
        TaskStatus.PROPOSING,
        TaskStatus.REQUIREMENTS_DESIGNED,
        TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED,
        TaskStatus.VERIFYING,
        TaskStatus.VERIFIED,
        TaskStatus.ARCHIVED,
    ),
    gate_next={
        TaskStatus.REQUIREMENTS_DESIGNED: TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED: TaskStatus.VERIFYING,
        TaskStatus.VERIFIED: TaskStatus.ARCHIVED,
    },
    gate_preconditions={
        TaskStatus.REQUIREMENTS_DESIGNED: _check_requirements_gate,
        TaskStatus.VERIFIED: _check_verified_gate,
    },
    file_additions={
        TaskStatus.REQUIREMENTS_DESIGNED: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.VERIFIED: (TaskPackageDocument.EVIDENCE,),
    },
    working_files={
        TaskStatus.PROPOSING: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.VERIFYING: (TaskPackageDocument.EVIDENCE,),
    },
    section_specs=_FILE_SECTION_REQUIREMENTS,
    descriptions=DESCRIPTIONS,
    next_steps=MECHANICAL_NEXT_STEPS,
)

STANDARD_WORKFLOW = Workflow(
    name="standard",
    status_sequence=(
        TaskStatus.PROPOSING,
        TaskStatus.REQUIREMENTS_DESIGNED,
        TaskStatus.PLANNING,
        TaskStatus.PLANNED,
        TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED,
        TaskStatus.VERIFYING,
        TaskStatus.VERIFIED,
        TaskStatus.ARCHIVED,
    ),
    gate_next={
        TaskStatus.REQUIREMENTS_DESIGNED: TaskStatus.PLANNING,
        TaskStatus.PLANNED: TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED: TaskStatus.VERIFYING,
        TaskStatus.VERIFIED: TaskStatus.ARCHIVED,
    },
    gate_preconditions={
        TaskStatus.REQUIREMENTS_DESIGNED: _check_requirements_gate,
        TaskStatus.VERIFIED: _check_verified_gate,
    },
    file_additions={
        TaskStatus.REQUIREMENTS_DESIGNED: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.PLANNED: (TaskPackageDocument.PLAN,),
        TaskStatus.VERIFIED: (TaskPackageDocument.EVIDENCE,),
    },
    working_files={
        TaskStatus.PROPOSING: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.PLANNING: (TaskPackageDocument.PLAN,),
        TaskStatus.VERIFYING: (TaskPackageDocument.EVIDENCE,),
    },
    section_specs=_FILE_SECTION_REQUIREMENTS,
    descriptions=DESCRIPTIONS,
    next_steps=STANDARD_NEXT_STEPS,
)

STRUCTURAL_WORKFLOW = Workflow(
    name="structural",
    status_sequence=(
        TaskStatus.PROPOSING,
        TaskStatus.REQUIREMENTS_DESIGNED,
        TaskStatus.OVERVIEW_DESIGNING,
        TaskStatus.OVERVIEW_DESIGNED,
        TaskStatus.DETAILED_DESIGNING,
        TaskStatus.DETAILED_DESIGNED,
        TaskStatus.PLANNING,
        TaskStatus.PLANNED,
        TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED,
        TaskStatus.VERIFYING,
        TaskStatus.VERIFIED,
        TaskStatus.ARCHIVED,
    ),
    gate_next={
        TaskStatus.REQUIREMENTS_DESIGNED: TaskStatus.OVERVIEW_DESIGNING,
        TaskStatus.OVERVIEW_DESIGNED: TaskStatus.DETAILED_DESIGNING,
        TaskStatus.DETAILED_DESIGNED: TaskStatus.PLANNING,
        TaskStatus.PLANNED: TaskStatus.IMPLEMENTING,
        TaskStatus.IMPLEMENTED: TaskStatus.VERIFYING,
        TaskStatus.VERIFIED: TaskStatus.ARCHIVED,
    },
    gate_preconditions={
        TaskStatus.REQUIREMENTS_DESIGNED: _check_requirements_gate,
        TaskStatus.VERIFIED: _check_verified_gate,
    },
    file_additions={
        TaskStatus.REQUIREMENTS_DESIGNED: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.OVERVIEW_DESIGNED: (TaskPackageDocument.OVERVIEW_DESIGN,),
        TaskStatus.DETAILED_DESIGNED: (TaskPackageDocument.DETAILED_DESIGN,),
        TaskStatus.PLANNED: (TaskPackageDocument.PLAN,),
        TaskStatus.VERIFIED: (TaskPackageDocument.EVIDENCE,),
    },
    working_files={
        TaskStatus.PROPOSING: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.OVERVIEW_DESIGNING: (TaskPackageDocument.OVERVIEW_DESIGN,),
        TaskStatus.DETAILED_DESIGNING: (TaskPackageDocument.DETAILED_DESIGN,),
        TaskStatus.PLANNING: (TaskPackageDocument.PLAN,),
        TaskStatus.VERIFYING: (TaskPackageDocument.EVIDENCE,),
    },
    section_specs=_FILE_SECTION_REQUIREMENTS,
    descriptions=DESCRIPTIONS,
    next_steps=STRUCTURAL_NEXT_STEPS,
)


ACTIVE_STATUSES = frozenset(
    s.value
    for s in (
        MECHANICAL_WORKFLOW.active_statuses
        | STANDARD_WORKFLOW.active_statuses
        | STRUCTURAL_WORKFLOW.active_statuses
    )
)

GATE_STATUSES = frozenset(
    s.value
    for s in (
        MECHANICAL_WORKFLOW.gate_statuses
        | STANDARD_WORKFLOW.gate_statuses
        | STRUCTURAL_WORKFLOW.gate_statuses
    )
)


def workflow_for(task_type: Optional[Union[TaskType, str]]) -> Workflow:
    if task_type is None:
        return STANDARD_WORKFLOW
    if isinstance(task_type, str):
        if task_type == TaskType.MECHANICAL.value:
            return MECHANICAL_WORKFLOW
        if task_type == TaskType.STRUCTURAL.value:
            return STRUCTURAL_WORKFLOW
        return STANDARD_WORKFLOW
    if task_type == TaskType.MECHANICAL:
        return MECHANICAL_WORKFLOW
    if task_type == TaskType.STRUCTURAL:
        return STRUCTURAL_WORKFLOW
    return STANDARD_WORKFLOW
