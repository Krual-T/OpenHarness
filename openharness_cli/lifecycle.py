from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .models import HarnessManifest, TaskPackage
from .repository import _current_date, _load_yaml, _utc_now, _write_yaml
from .validation import validate_task_package


def _normalize_status_for_fingerprint(status: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(status)
    normalized.pop("updated_at", None)
    normalized.pop("status", None)
    verification = normalized.get("verification")
    if isinstance(verification, dict):
        verification.pop("last_run_at", None)
        verification.pop("last_run_result", None)
        verification.pop("last_run_artifact", None)
    return normalized


def compute_task_package_fingerprint(package: TaskPackage) -> str:
    payload: dict[str, Any] = {"documents": {}}
    for file_name in package.manifest.required_design_files:
        path = package.root / file_name
        if file_name == "STATUS.yaml" and path.exists():
            payload["documents"][file_name] = _normalize_status_for_fingerprint(_load_yaml(path))
            continue
        payload["documents"][file_name] = path.read_text(encoding="utf-8") if path.exists() else None
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _save_package_status(package: TaskPackage, status: dict[str, Any]) -> TaskPackage:
    _write_yaml(package.status_path, status)
    return TaskPackage(root=package.root, status=status, manifest=package.manifest, documents=package.documents)


def _status_flow(manifest: HarnessManifest) -> tuple[str, ...]:
    if manifest.allowed_statuses:
        return manifest.allowed_statuses
    return ("proposed", "requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying", "archived")


def _status_description(status: str) -> str:
    descriptions = {
        "proposed": "Task package exists, but requirements are not ready yet.",
        "requirements_ready": "Requirements are converged and the work is ready for exploration.",
        "overview_ready": "Overview design is coherent and the work is ready for detailed design.",
        "detailed_ready": "Detailed design is ready and implementation can start against the package.",
        "in_progress": "Implementation is underway against the current task-package contract.",
        "verifying": "Implementation is complete enough to gather fresh verification evidence.",
        "archived": "Implementation and verification are complete, and the package is no longer active.",
    }
    return descriptions.get(status, "Unknown workflow stage.")


def _next_status(manifest: HarnessManifest, status: str) -> str:
    flow = _status_flow(manifest)
    if status not in flow:
        return ""
    index = flow.index(status)
    if index >= len(flow) - 1:
        return ""
    return flow[index + 1]


def _next_step(package: TaskPackage) -> str:
    steps = {
        "proposed": (
            "Finish requirements convergence, write `01-requirements.md`, "
            "then transition to `requirements_ready`."
        ),
        "requirements_ready": (
            "Run exploration, write `02-overview-design.md`, and transition to `overview_ready`."
        ),
        "overview_ready": (
            "Write `03-detailed-design.md`, close detailed-design challenges, "
            "and transition to `detailed_ready`."
        ),
        "detailed_ready": (
            "Start implementation against the package, then transition to `in_progress` "
            "once execution actually begins."
        ),
        "in_progress": (
            "Finish implementation, update verification and evidence planning, "
            "and transition to `verifying` when fresh evidence can be gathered."
        ),
        "verifying": (
            "Run declared verification, refresh `04-verification.md` and `05-evidence.md`, "
            "then transition to `archived` after passing evidence is recorded."
        ),
        "archived": "No next step. The package is complete and archived.",
    }
    return steps.get(package.status_name, "No next step available.")


def describe_stage(package: TaskPackage) -> dict[str, str]:
    return {
        "current_stage": package.status_name,
        "current_stage_description": _status_description(package.status_name),
        "next_stage": _next_status(package.manifest, package.status_name),
        "next_step": _next_step(package),
    }


def _build_transition_candidate(package: TaskPackage, target_status: str) -> TaskPackage:
    candidate_status = copy.deepcopy(package.status)
    candidate_status["status"] = target_status
    candidate_status["updated_at"] = _current_date()
    return TaskPackage(root=package.root, status=candidate_status, manifest=package.manifest, documents=package.documents)


def _ensure_transition_allowed(package: TaskPackage, target_status: str) -> list[str]:
    flow = _status_flow(package.manifest)
    if target_status not in flow:
        return [f"unknown target status `{target_status}`; expected one of: {', '.join(flow)}"]
    if package.status_name == "archived":
        return [f"cannot transition archived package `{package.task_id}` out of `archived`"]
    if target_status == package.status_name:
        return []
    current_index = flow.index(package.status_name)
    target_index = flow.index(target_status)
    if target_index > current_index + 1:
        return [
            f"cannot skip forward from `{package.status_name}` to `{target_status}`; "
            f"next legal forward status is `{flow[current_index + 1]}`"
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
    return (package.manifest.repo_root / raw).resolve()


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
    current_fingerprint = compute_task_package_fingerprint(package)
    if artifact.get("package_fingerprint") != current_fingerprint:
        errors.append("latest verification artifact does not match the current task-package content")
    return errors


def _replace_package_prefix(text: str, package_name: str, archived: bool) -> str:
    active_prefix = f"docs/task-packages/{package_name}/"
    archived_prefix = f"docs/archived/task-packages/{package_name}/"
    if archived:
        return text.replace(active_prefix, archived_prefix)
    return text.replace(archived_prefix, active_prefix)


def _scan_repo_references(repo_root: Path, needle: str, ignore_roots: tuple[Path, ...]) -> list[Path]:
    hits: list[Path] = []
    ignore_resolved = {path.resolve() for path in ignore_roots if path.exists()}
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        if any(parent in ignore_resolved for parent in resolved.parents):
            continue
        if ".git" in resolved.parts:
            continue
        try:
            if needle in path.read_text(encoding="utf-8"):
                hits.append(path)
        except UnicodeDecodeError:
            continue
    return sorted(hits)


def _prepare_archived_copy(package: TaskPackage, temp_root: Path) -> TaskPackage:
    shutil.copytree(package.root, temp_root)
    for file_name in package.manifest.required_design_files:
        path = temp_root / file_name
        if not path.exists():
            continue
        if file_name == "STATUS.yaml":
            status = _load_yaml(path)
            status["status"] = "archived"
            status["updated_at"] = _current_date()
            _write_yaml(path, status)
            rewritten = _replace_package_prefix(path.read_text(encoding="utf-8"), package.name, archived=True)
            path.write_text(rewritten, encoding="utf-8")
            continue
        rewritten = _replace_package_prefix(path.read_text(encoding="utf-8"), package.name, archived=True)
        path.write_text(rewritten, encoding="utf-8")
    status = _load_yaml(temp_root / "STATUS.yaml")
    return TaskPackage(
        root=temp_root,
        status=status,
        manifest=package.manifest,
        documents={name: temp_root / name for name in package.manifest.required_design_files},
    )


def _archive_task_package(package: TaskPackage) -> tuple[bool, str]:
    target_root = package.manifest.archived_task_packages_root / package.name
    temp_root = package.manifest.archived_task_packages_root / f".{package.name}.tmp-archive"
    backup_root = package.manifest.task_packages_root / f".{package.name}.archive-backup"
    target_root.parent.mkdir(parents=True, exist_ok=True)
    if target_root.exists():
        return False, f"archive target already exists: {target_root}"
    if temp_root.exists():
        shutil.rmtree(temp_root)
    if backup_root.exists():
        shutil.rmtree(backup_root)
    _prepare_archived_copy(package, temp_root)
    try:
        package.root.rename(backup_root)
        temp_root.rename(target_root)
        archived_status = _load_yaml(target_root / "STATUS.yaml")
        archived_package = TaskPackage(
            root=target_root,
            status=archived_status,
            manifest=package.manifest,
            documents={name: target_root / name for name in package.manifest.required_design_files},
        )
        errors = validate_task_package(archived_package)
        if errors:
            invalid_root = package.manifest.archived_task_packages_root / f".{package.name}.invalid-archive"
            if invalid_root.exists():
                shutil.rmtree(invalid_root)
            target_root.rename(invalid_root)
            backup_root.rename(package.root)
            shutil.rmtree(invalid_root)
            return False, "\n".join(errors)
        shutil.rmtree(backup_root)
    except Exception as exc:
        if target_root.exists() and not package.root.exists():
            try:
                target_root.rename(package.root)
            except Exception:
                pass
        if backup_root.exists() and not package.root.exists():
            backup_root.rename(package.root)
        if temp_root.exists():
            shutil.rmtree(temp_root)
        return False, f"failed to archive package transactionally: {exc}"
    lingering = _scan_repo_references(
        package.manifest.repo_root,
        f"docs/task-packages/{package.name}/",
        ignore_roots=(target_root,),
    )
    if lingering:
        return True, "remaining repository references:\n" + "\n".join(str(path) for path in lingering)
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
    artifact_root = package.manifest.repo_root / ".harness" / "artifacts" / package.task_id / "verification-runs"
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
        "package_fingerprint": compute_task_package_fingerprint(package),
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
        verification["last_run_artifact"] = str(artifact_path.relative_to(package.manifest.repo_root))
    status["updated_at"] = _current_date()
    _save_package_status(package, status)
    return artifact_path


def _run_command(repo_root: Path, command: str) -> int:
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True, cwd=repo_root)
    return completed.returncode
