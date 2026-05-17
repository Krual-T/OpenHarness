from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from .harness_config import HarnessConfig
from .task_info import TaskInfo

if TYPE_CHECKING:
    from .workflow import Workflow


@dataclass(slots=True, frozen=True)
class TaskPackage:
    root: Path
    info: TaskInfo
    config: HarnessConfig
    documents: dict[str, Path] = field(default_factory=dict)

    @property
    def workflow(self) -> Workflow:
        from ..workflows import workflow_for
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
        return v.verify_by.value if v and v.verify_by else ""

    @property
    def task_type(self) -> str:
        c = self.info.collaboration
        return c.task_type.value if c and c.task_type else ""

    @property
    def design_review_mode(self) -> str:
        c = self.info.collaboration
        return c.design_review_mode.value if c and c.design_review_mode else ""

    @property
    def info_path(self) -> Path:
        return self.root / "task-info.yaml"
