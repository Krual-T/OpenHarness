from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .task_type import TaskType
from .design_review_mode import DesignReviewMode


@dataclass
class CollaborationInfo:
    task_type: Optional[TaskType] = None
    design_review_mode: Optional[DesignReviewMode] = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Optional[dict[str, Any]]) -> CollaborationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        task_type_raw = str(raw.pop("task_type", "")).strip()
        drm_raw = str(raw.pop("design_review_mode", "")).strip()
        task_type = None
        design_review_mode = None
        if task_type_raw:
            try:
                task_type = TaskType(task_type_raw)
            except ValueError:
                pass
        if drm_raw:
            try:
                design_review_mode = DesignReviewMode(drm_raw)
            except ValueError:
                pass
        return cls(task_type=task_type, design_review_mode=design_review_mode, _extra=raw)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.task_type is not None:
            result["task_type"] = self.task_type.value
        if self.design_review_mode is not None:
            result["design_review_mode"] = self.design_review_mode.value
        return result
