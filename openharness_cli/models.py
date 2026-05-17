from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .domain import Workflow, TaskInfo, TaskStatus
from .workflows import workflow_for


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
    info: TaskInfo
    config: HarnessConfig
    documents: dict[str, Path] = field(default_factory=dict)

    @property
    def workflow(self) -> Workflow:
        return workflow_for(self.task_type or None)

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def current_status(self) -> str:
        return self.info.status_value

    @property
    def task_id(self) -> str:
        return self.info.id or self.root.name

    @property
    def title(self) -> str:
        return self.info.title or self.root.name

    @property
    def summary(self) -> str:
        return self.info.summary

    @property
    def owner(self) -> str:
        return self.info.owner

    @property
    def done_criteria(self) -> tuple[str, ...]:
        return self.info.done_criteria

    @property
    def verify_by(self) -> str:
        v = self.info.verification
        return v.verify_by if v and v.verify_by else ""

    @property
    def task_type(self) -> str:
        c = self.info.collaboration
        return c.task_type if c and c.task_type else ""

    @property
    def design_review_mode(self) -> str:
        c = self.info.collaboration
        return c.design_review_mode if c and c.design_review_mode else ""

    @property
    def info_path(self) -> Path:
        return self.root / "task-info.yaml"


@dataclass(slots=True, frozen=True)
class CreateTaskInput:
    repo_root: Path
    task_name: str
    task_id: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: TaskStatus = TaskStatus.PROPOSING


@dataclass(slots=True, frozen=True)
class RuntimeWorkflowPackage:
    root: Path
    workflow_path: Path
    name: str
    description: str
