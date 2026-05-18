from __future__ import annotations

from dataclasses import dataclass

from .task_status import TaskStatus


@dataclass(slots=True, frozen=True)
class CreateTaskInput:
    task_name: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: TaskStatus = TaskStatus.PROPOSING
