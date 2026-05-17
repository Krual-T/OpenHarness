from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any

from .constants import DEFAULT_STATUS_FLOW, GATE_STATUSES, MECHANICAL_STATUS_FLOW, STATE_SKILL_HOOKS
from .models import TaskPackage
from .repository import _current_date, _load_yaml, _write_yaml


def _package_status_flow(package: TaskPackage) -> tuple[str, ...]:
    if package.task_type == "mechanical":
        return MECHANICAL_STATUS_FLOW
    return DEFAULT_STATUS_FLOW


def _save_package_status(package: TaskPackage, status: dict[str, Any]) -> TaskPackage:
    _write_yaml(package.status_path, status)
    return TaskPackage(root=package.root, status=status, config=package.config, documents=package.documents)


def _status_description(status: str) -> str:
    descriptions = {
        "proposing": "Converging requirements — 01-requirements.md is not yet ready.",
        "requirements_designed": "Requirements converged; auto-advancing to next active state.",
        "overview_designing": "Exploring and drafting overview design.",
        "overview_designed": "Overview design complete; auto-advancing to detailed design.",
        "detailed_designing": "Drafting detailed design and implementation plan.",
        "detailed_designed": "Detailed design complete; auto-advancing to verification design.",
        "verification_designing": "Designing verification strategy (TDD red phase).",
        "verification_designed": "Verification strategy complete; auto-advancing to implementation.",
        "implementing": "Implementing against the verification plan (TDD green + refactor).",
        "implemented": "Implementation complete; auto-advancing to verification execution.",
        "verifying": "Executing verification and collecting evidence.",
        "verified": "Verification complete; auto-advancing to archived.",
        "archived": "Verification passed; package is archived and no longer active.",
    }
    return descriptions.get(status, "Unknown workflow stage.")


def _next_status(status: str, status_flow: tuple[str, ...]) -> str:
    if status not in status_flow:
        return ""
    index = status_flow.index(status)
    if index >= len(status_flow) - 1:
        return ""
    return status_flow[index + 1]


def _next_step(package: TaskPackage) -> str:
    status_flow = _package_status_flow(package)
    if package.task_type == "mechanical":
        steps = {
            "proposing": (
                "Converge requirements, determine task_type and verify_by, "
                "write `01-requirements.md`, then transition to `requirements_designed`."
            ),
            "requirements_designed": "Auto-advancing to `verification_designing`.",
            "verification_designing": (
                "Design verification strategy, write `verification_design.md`, "
                "then transition to `verification_designed`."
            ),
            "verification_designed": "Auto-advancing to `implementing`.",
            "implementing": (
                "Implement to pass verification, then transition to `implemented`."
            ),
            "implemented": "Auto-advancing to `verifying`.",
            "verifying": (
                "Execute verification and write `evidence.md`, "
                "then transition to `verified`."
            ),
            "verified": "Auto-advancing to `archived`.",
            "archived": "No next step. The package is complete and archived.",
        }
    else:
        steps = {
            "proposing": (
                "Converge requirements, determine task_type and verify_by, "
                "write `01-requirements.md`, then transition to `requirements_designed`."
            ),
            "requirements_designed": "Auto-advancing to `overview_designing`.",
            "overview_designing": (
                "Complete overview design and reflection, "
                "then transition to `overview_designed`."
            ),
            "overview_designed": "Auto-advancing to `detailed_designing`.",
            "detailed_designing": (
                "Complete detailed design, close design challenges, "
                "then transition to `detailed_designed`."
            ),
            "detailed_designed": "Auto-advancing to `verification_designing`.",
            "verification_designing": (
                "Design verification strategy, write `verification_design.md`, "
                "then transition to `verification_designed`."
            ),
            "verification_designed": "Auto-advancing to `implementing`.",
            "implementing": (
                "Implement to pass verification, then transition to `implemented`."
            ),
            "implemented": "Auto-advancing to `verifying`.",
            "verifying": (
                "Execute verification and write `evidence.md`, "
                "then transition to `verified`."
            ),
            "verified": "Auto-advancing to `archived`.",
            "archived": "No next step. The package is complete and archived.",
        }
    return steps.get(package.status_name, "No next step available.")


def describe_stage(package: TaskPackage) -> dict[str, str]:
    status_flow = _package_status_flow(package)
    return {
        "current_stage": package.status_name,
        "current_stage_description": _status_description(package.status_name),
        "next_stage": _next_status(package.status_name, status_flow),
        "next_step": _next_step(package),
    }


def _build_transition_candidate(package: TaskPackage, target_status: str) -> TaskPackage:
    candidate_status = copy.deepcopy(package.status)
    candidate_status["status"] = target_status
    candidate_status["updated_at"] = _current_date()
    return TaskPackage(root=package.root, status=candidate_status, config=package.config, documents=package.documents)


def _ensure_transition_allowed(package: TaskPackage, target_status: str) -> list[str]:
    status_flow = _package_status_flow(package)
    if target_status not in status_flow:
        return [f"unknown target status `{target_status}`; expected one of: {', '.join(status_flow)}"]
    if package.status_name == "archived":
        return [f"cannot transition archived package `{package.task_id}` out of `archived`"]
    if target_status == package.status_name:
        return []
    current_index = status_flow.index(package.status_name)
    target_index = status_flow.index(target_status)
    if target_index > current_index + 1:
        return [
            f"cannot skip forward from `{package.status_name}` to `{target_status}`; "
            f"next legal forward status is `{status_flow[current_index + 1]}`"
        ]
    if target_status == "archived" and package.status_name != "verified":
        return ["can only transition to `archived` from `verified`"]
    return []


# ── Hook: CLI outputs skill file content for the new state ──────────────────

def _output_state_hook(repo_root: Path, state: str) -> None:
    """Read and print the skill file for *state* so the Agent receives instructions inline."""
    relative = STATE_SKILL_HOOKS.get(state)
    if not relative:
        return
    skill_path = repo_root / relative
    if not skill_path.exists():
        print(f"[hook] skill file not found: {relative}", flush=True)
        return
    print(f"--- BEGIN: {relative} ---", flush=True)
    print(skill_path.read_text(encoding="utf-8"), flush=True)
    print(f"--- END: {relative} ---", flush=True)


# ── Gate auto-advance ──────────────────────────────────────────────────────

def _resolve_gate_transition(package: TaskPackage, target_status: str) -> tuple[str | None, list[str]]:
    """If *target_status* is a gate, check preconditions and return the next real state.

    Returns (next_state, [])  → caller should re-target to *next_state*.
    Returns (None, errors)    → precondition failure; caller should abort.
    Returns (None, [])        → *target_status* is not a gate; proceed normally.
    """
    if target_status not in GATE_STATUSES:
        return None, []

    if target_status == "requirements_designed":
        if not package.task_type:
            return None, [
                "task_type 未确认。请向用户提议分类（mechanical / standard development / protocol/architecture）"
                "并写入 STATUS.yaml.collaboration.task_type"
            ]
        if not package.verify_by:
            return None, [
                "verify_by 未确定。请确定验证策略（unit_test / qualitative / rwp）"
                "并写入 STATUS.yaml.verification.verify_by"
            ]
        if package.task_type == "mechanical":
            return "verification_designing", []
        return "overview_designing", []

    if target_status == "overview_designed":
        return "detailed_designing", []

    if target_status == "detailed_designed":
        return "verification_designing", []

    if target_status == "verification_designed":
        return "implementing", []

    if target_status == "implemented":
        return "verifying", []

    if target_status == "verified":
        evidence_path = package.root / "evidence.md"
        if not evidence_path.exists():
            return None, ["证据文件 evidence.md 不存在，请先写入验证证据。"]
        if not evidence_path.read_text(encoding="utf-8").strip():
            return None, ["证据文件 evidence.md 内容为空，请先写入验证证据。"]
        return "archived", []

    return None, []


# ── Archive ─────────────────────────────────────────────────────────────────

def _check_archive_preconditions(package: TaskPackage) -> list[str]:
    """Archiving requires evidence.md to exist and be non-empty."""
    evidence_path = package.root / "evidence.md"
    if not evidence_path.exists():
        return ["archiving requires evidence.md to exist"]
    if not evidence_path.read_text(encoding="utf-8").strip():
        return ["archiving requires evidence.md to be non-empty"]
    return []


def _archive_task_package(package: TaskPackage) -> tuple[bool, str]:
    target_root = package.config.archived_task_packages_root / package.name
    target_root.parent.mkdir(parents=True, exist_ok=True)
    if target_root.exists():
        return False, f"archive target already exists: {target_root}"

    shutil.move(str(package.root), str(target_root))

    status_path = target_root / "STATUS.yaml"
    status = _load_yaml(status_path)
    status["status"] = "archived"
    status["updated_at"] = _current_date()
    _write_yaml(status_path, status)

    return True, ""
