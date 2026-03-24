from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constants import REQUIRED_TASK_PACKAGE_FILES


@dataclass(slots=True, frozen=True)
class HarnessManifest:
    repo_root: Path
    path: Path
    raw: dict[str, Any]

    @property
    def task_packages_root(self) -> Path:
        raw_root = str(
            self.raw.get("task_packages_root")
            or self.raw.get("designs_root")
            or "docs/task-packages"
        ).strip() or "docs/task-packages"
        return (self.repo_root / raw_root).resolve()

    @property
    def archived_task_packages_root(self) -> Path:
        raw_root = str(
            self.raw.get("archived_task_packages_root")
            or self.raw.get("archived_designs_root")
            or "docs/archived/task-packages"
        ).strip() or "docs/archived/task-packages"
        return (self.repo_root / raw_root).resolve()

    @property
    def required_design_files(self) -> tuple[str, ...]:
        raw = self.raw.get("required_design_files")
        if not isinstance(raw, list) or not raw:
            return REQUIRED_TASK_PACKAGE_FILES
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def designs_root(self) -> Path:
        return self.task_packages_root

    @property
    def archived_designs_root(self) -> Path:
        return self.archived_task_packages_root

    @property
    def allowed_statuses(self) -> tuple[str, ...]:
        workflow = self.raw.get("workflow")
        if not isinstance(workflow, dict):
            return ()
        raw = workflow.get("default_status_flow")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())


@dataclass(slots=True, frozen=True)
class TaskPackage:
    root: Path
    status: dict[str, Any]
    manifest: HarnessManifest
    documents: dict[str, Path] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def status_name(self) -> str:
        return str(self.status.get("status") or "").strip()

    @property
    def task_id(self) -> str:
        return str(self.status.get("id") or self.root.name).strip()

    @property
    def title(self) -> str:
        return str(self.status.get("title") or self.root.name).strip()

    @property
    def summary(self) -> str:
        return str(self.status.get("summary") or "").strip()

    @property
    def owner(self) -> str:
        return str(self.status.get("owner") or "").strip()

    @property
    def done_criteria(self) -> tuple[str, ...]:
        raw = self.status.get("done_criteria")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def required_commands(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        commands = verification.get("required_commands")
        if not isinstance(commands, list):
            return ()
        return tuple(str(item).strip() for item in commands if str(item).strip())

    @property
    def required_scenarios(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        scenarios = verification.get("required_scenarios")
        if not isinstance(scenarios, list):
            return ()
        return tuple(str(item).strip() for item in scenarios if str(item).strip())

    @property
    def status_path(self) -> Path:
        return self.root / "STATUS.yaml"


@dataclass(slots=True, frozen=True)
class TaskScaffoldRequest:
    repo_root: Path
    task_name: str
    task_id: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: str = "proposed"
