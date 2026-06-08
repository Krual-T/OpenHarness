
from dataclasses import dataclass
from pathlib import Path

from .harness_config import HarnessConfig
from .task_info import TaskInfo
from .task_package_document import TaskPackageDocument
from .workflow import Workflow


@dataclass(slots=True, frozen=True)
class TaskPackage:
    root: Path
    info: TaskInfo
    config: HarnessConfig

    @property
    def workflow(self) -> Workflow:
        from ..workflows import workflow_for
        return workflow_for(self.task_type or None)

    @property
    def documents(self) -> dict[TaskPackageDocument, Path]:
        return {d: d.path_from(self.root) for d in TaskPackageDocument}

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
    def verification_method(self) -> str:
        v = self.info.verification
        return v.method.value if v and v.method else ""

    @property
    def raw_verification_method(self) -> str:
        v = self.info.verification
        return v.raw_method if v else ""

    @property
    def rwp_enabled(self) -> str:
        v = self.info.verification
        if not v or v.rwp.enabled is None:
            return ""
        return "true" if v.rwp.enabled else "false"

    @property
    def rwp_reason(self) -> str:
        v = self.info.verification
        return v.rwp.reason if v else ""

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
        return TaskPackageDocument.TASK_INFO.path_from(self.root)
