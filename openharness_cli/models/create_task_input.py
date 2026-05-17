from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .task_status import TaskStatus


@dataclass(slots=True, frozen=True)
class CreateTaskInput:
    repo_root: Path
    task_name: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: TaskStatus = TaskStatus.PROPOSING
