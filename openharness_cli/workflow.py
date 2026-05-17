from __future__ import annotations

import dataclasses

from .domain import TaskStatus
from .models import TaskPackage
from .repository import _archive_task_package, _current_date, _write_yaml


# ═══════════════════════════════════════════════════════════════════════════════
# Status persistence
# ═══════════════════════════════════════════════════════════════════════════════

def _save_package_status(package: TaskPackage, info) -> TaskPackage:
    _write_yaml(package.info_path, info.to_dict())
    return TaskPackage(root=package.root, info=info, config=package.config, documents=package.documents)


# ═══════════════════════════════════════════════════════════════════════════════
# Internal transition helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _build_transition_candidate(package: TaskPackage, target_status: str) -> TaskPackage:
    try:
        target = TaskStatus(target_status)
    except ValueError:
        target = TaskStatus.PROPOSING
    candidate = dataclasses.replace(
        package.info,
        status=target,
        updated_at=_current_date(),
        _raw_status=None,
    )
    return TaskPackage(root=package.root, info=candidate, config=package.config, documents=package.documents)


def _ensure_transition_allowed(package: TaskPackage, target_status: str) -> list[str]:
    wf = package.workflow
    sequence_values = {s.value for s in wf.status_sequence}
    if target_status not in sequence_values:
        return [
            f"unknown target status `{target_status}`; "
            f"expected one of: {', '.join(s.value for s in wf.status_sequence)}"
        ]
    if package.current_status == "archived":
        return [f"cannot transition archived package `{package.task_id}` out of `archived`"]
    if target_status == package.current_status:
        return []

    current = package.info.status
    target = TaskStatus(target_status) if target_status in {s.value for s in TaskStatus} else TaskStatus.PROPOSING

    try:
        current_index = wf.status_sequence.index(current)
        target_index = wf.status_sequence.index(target)
    except ValueError:
        return [f"unknown status in transition from `{current}` to `{target}`"]

    if target_index > current_index + 1:
        next_s = wf.status_sequence[current_index + 1]
        return [
            f"cannot skip forward from `{package.current_status}` to `{target_status}`; "
            f"next legal forward status is `{next_s.value}`"
        ]
    if target_status == "archived" and package.current_status != "verified":
        return ["can only transition to `archived` from `verified`"]
    return []


def _resolve_gate_transition(package: TaskPackage, target_status: str) -> tuple[str | None, list[str]]:
    try:
        target = TaskStatus(target_status)
    except ValueError:
        return None, []

    next_s, errors = package.workflow.resolve_gate(package, target)
    if errors:
        return None, errors
    if next_s is not None:
        return next_s.value, []
    return None, []


# ═══════════════════════════════════════════════════════════════════════════════
# Public entry point
# ═══════════════════════════════════════════════════════════════════════════════

def execute_transition(package: TaskPackage, target_status: str) -> tuple[TaskPackage | None, list[str]]:
    """Attempt to transition *package* to *target_status*.

    Returns (updated_package, []) on success.
    Returns (None, errors) on failure.
    """
    errors = _ensure_transition_allowed(package, target_status)
    if errors:
        return None, errors

    if target_status == package.current_status:
        return package, []

    # Archive
    if target_status == "archived":
        _, gate_errors = package.workflow.resolve_gate(package, TaskStatus.VERIFIED)
        if gate_errors:
            return None, gate_errors
        archived_ok, detail = _archive_task_package(package)
        if not archived_ok:
            return None, [detail]
        return None, []

    # Save the transition to the target state first
    candidate = _build_transition_candidate(package, target_status)
    updated = _save_package_status(package, candidate.info)

    # Then check if the new state is a gate that should auto-advance
    gate_next, gate_errors = _resolve_gate_transition(updated, target_status)
    if gate_errors:
        return None, gate_errors
    if gate_next is not None:
        return execute_transition(updated, gate_next)

    return updated, []
