from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .constants import DEFAULT_STATUS_FLOW, MECHANICAL_STATUS_FLOW
from .models import TaskPackage
from .repository import _current_date, _load_yaml, _utc_now, _write_yaml


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
        "requirements_designed": "Requirements are converged; ready to explore solutions.",
        "overview_designing": "Exploring and drafting overview design.",
        "overview_designed": "Overview design is coherent; ready for detailed design.",
        "detailed_designing": "Drafting detailed design and implementation plan.",
        "detailed_designed": "Detailed design is ready; implementation can start.",
        "implementing": "Implementation is in progress against the task-package contract.",
        "implemented": "Implementation is complete; ready to gather verification evidence.",
        "verifying": "Running verification and recording evidence.",
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
                "Converge requirements, write `01-requirements.md`, "
                "then transition to `requirements_designed`."
            ),
            "requirements_designed": (
                "Start implementation, then transition to `implementing`."
            ),
            "implementing": (
                "Finish implementation, then transition to `verifying` "
                "when ready for verification."
            ),
            "verifying": (
                "Complete verification and record passing evidence, "
                "then transition to `archived`."
            ),
            "archived": "No next step. The package is complete and archived.",
        }
    else:
        steps = {
            "proposing": (
                "Converge requirements, write `01-requirements.md`, "
                "then transition to `requirements_designed`."
            ),
            "requirements_designed": (
                "Run exploration, draft `02-overview-design.md`, "
                "and transition to `overview_designing`."
            ),
            "overview_designing": (
                "Complete overview design and reflection, "
                "then transition to `overview_designed`."
            ),
            "overview_designed": (
                "Draft `03-detailed-design.md`, "
                "and transition to `detailed_designing`."
            ),
            "detailed_designing": (
                "Complete detailed design, close design challenges, "
                "then transition to `detailed_designed`."
            ),
            "detailed_designed": (
                "Start implementation, then transition to `implementing`."
            ),
            "implementing": (
                "Finish implementation, then transition to `implemented` "
                "when ready for verification."
            ),
            "implemented": (
                "Run declared verification, refresh `04-verification.md` and `05-evidence.md`, "
                "then transition to `verifying`."
            ),
            "verifying": (
                "Complete verification and record passing evidence, "
                "then transition to `archived`."
            ),
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
    if target_status == "archived" and package.status_name != "verifying":
        return ["can only transition to `archived` from `verifying`"]
    return []


def _latest_verification_artifact_path(package: TaskPackage) -> Path | None:
    verification = package.status.get("verification")
    if not isinstance(verification, dict):
        return None
    raw = str(verification.get("last_run_artifact") or "").strip()
    if not raw:
        return None
    return (package.config.repo_root / raw).resolve()


def _check_archive_preconditions(package: TaskPackage) -> list[str]:
    errors: list[str] = []
    artifact_path = _latest_verification_artifact_path(package)
    if artifact_path is None or not artifact_path.exists():
        errors.append("archiving requires an existing latest verification artifact")
        return errors
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    if artifact.get("overall_result") != "passed":
        errors.append("archiving requires the latest verification artifact result to be `passed`")
    if artifact.get("task_id") != package.task_id:
        errors.append("latest verification artifact does not match the task package id")
    return errors


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


def _record_verification_artifact(
    package: TaskPackage,
    *,
    started_at: str,
    finished_at: str,
    overall_result: str,
    command_results: list[dict[str, Any]],
) -> Path:
    run_id = _utc_now().strftime("%Y%m%dT%H%M%S%fZ")
    artifact_root = package.config.repo_root / ".harness" / "artifacts" / package.task_id / "verification-runs"
    artifact_root.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_root / f"{run_id}.json"
    artifact = {
        "run_id": run_id,
        "task_id": package.task_id,
        "task_name": package.name,
        "title": package.title,
        "status_at_run": package.status_name,
        "started_at": started_at,
        "finished_at": finished_at,
        "required_commands_snapshot": list(package.required_commands),
        "required_scenarios_snapshot": list(package.required_scenarios),
        "command_results": command_results,
        "overall_result": overall_result,
    }
    artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest_path = artifact_root / "latest.json"
    latest_path.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")

    status = copy.deepcopy(package.status)
    verification = status.setdefault("verification", {})
    if isinstance(verification, dict):
        verification["last_run_at"] = finished_at
        verification["last_run_result"] = overall_result
        verification["last_run_artifact"] = str(artifact_path.relative_to(package.config.repo_root))
    status["updated_at"] = _current_date()
    _save_package_status(package, status)
    return artifact_path


def _run_command(repo_root: Path, command: str) -> int:
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True, cwd=repo_root)
    return completed.returncode
