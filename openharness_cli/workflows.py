
from typing import Optional, Union

from .models import TaskPackage, TaskStatus, TaskType, Workflow, TaskPackageDocument


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
    "Converge requirements, determine task_type, verification method, and RWP setting, "
    f"write `{TaskPackageDocument.REQUIREMENTS.value}`, then transition to `requirements_designed`."
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
        f"Design verification strategy, write `{TaskPackageDocument.VERIFICATION_DESIGN.value}`, "
        "then transition to `verification_designed`."
    ),
    TaskStatus.VERIFICATION_DESIGNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: (
        "Implement to pass verification, then transition to `implemented`."
    ),
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: (
        f"Execute verification and write `{TaskPackageDocument.EVIDENCE.value}`, "
        "then transition to `verified`."
    ),
    TaskStatus.VERIFIED: "Auto-advancing to `archived`.",
    TaskStatus.ARCHIVED: "No next step. The package is complete and archived.",
}

MECHANICAL_NEXT_STEPS: dict[TaskStatus, str] = {
    TaskStatus.PROPOSING: _PROPOSING_STEP,
    TaskStatus.REQUIREMENTS_DESIGNED: "Auto-advancing to `verification_designing`.",
    TaskStatus.VERIFICATION_DESIGNING: (
        f"Design verification strategy, write `{TaskPackageDocument.VERIFICATION_DESIGN.value}`, "
        "then transition to `verification_designed`."
    ),
    TaskStatus.VERIFICATION_DESIGNED: "Auto-advancing to `implementing`.",
    TaskStatus.IMPLEMENTING: (
        "Implement to pass verification, then transition to `implemented`."
    ),
    TaskStatus.IMPLEMENTED: "Auto-advancing to `verifying`.",
    TaskStatus.VERIFYING: (
        f"Execute verification and write `{TaskPackageDocument.EVIDENCE.value}`, "
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
        TaskStatus.REQUIREMENTS_DESIGNED: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.OVERVIEW_DESIGNED: (TaskPackageDocument.OVERVIEW_DESIGN,),
        TaskStatus.DETAILED_DESIGNED: (TaskPackageDocument.DETAILED_DESIGN,),
        TaskStatus.VERIFICATION_DESIGNED: (TaskPackageDocument.VERIFICATION_DESIGN,),
        TaskStatus.VERIFIED: (TaskPackageDocument.EVIDENCE,),
    },
    working_files={
        TaskStatus.PROPOSING: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.OVERVIEW_DESIGNING: (TaskPackageDocument.OVERVIEW_DESIGN,),
        TaskStatus.DETAILED_DESIGNING: (TaskPackageDocument.DETAILED_DESIGN,),
        TaskStatus.VERIFICATION_DESIGNING: (TaskPackageDocument.VERIFICATION_DESIGN,),
        TaskStatus.VERIFYING: (TaskPackageDocument.EVIDENCE,),
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
        TaskStatus.REQUIREMENTS_DESIGNED: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.VERIFICATION_DESIGNED: (TaskPackageDocument.VERIFICATION_DESIGN,),
        TaskStatus.VERIFIED: (TaskPackageDocument.EVIDENCE,),
    },
    working_files={
        TaskStatus.PROPOSING: (TaskPackageDocument.REQUIREMENTS,),
        TaskStatus.VERIFICATION_DESIGNING: (TaskPackageDocument.VERIFICATION_DESIGN,),
        TaskStatus.VERIFYING: (TaskPackageDocument.EVIDENCE,),
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
