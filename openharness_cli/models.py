from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True, frozen=True)
class HarnessConfig:
    repo_root: Path

    @property
    def task_packages_root(self) -> Path:
        return self.repo_root / "docs" / "task-packages"

    @property
    def archived_task_packages_root(self) -> Path:
        return self.repo_root / "docs" / "archived" / "task-packages"


@dataclass(slots=True, frozen=True)
class TaskPackage:
    root: Path
    status: dict[str, Any]
    config: HarnessConfig
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
    def task_type(self) -> str:
        collaboration = self.status.get("collaboration")
        if not isinstance(collaboration, dict):
            return ""
        return str(collaboration.get("task_type") or "").strip()

    @property
    def design_review_mode(self) -> str:
        collaboration = self.status.get("collaboration")
        if not isinstance(collaboration, dict):
            return ""
        return str(collaboration.get("design_review_mode") or "").strip()

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
    status: str = "proposing"


@dataclass(slots=True, frozen=True)
class RuntimeWorkflowPackage:
    root: Path
    workflow_path: Path
    name: str
    description: str
