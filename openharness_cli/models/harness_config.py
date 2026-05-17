from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class HarnessConfig:
    repo_root: Path

    @property
    def task_packages_root(self) -> Path:
        return self.repo_root / "docs" / "task-packages"

    @property
    def archived_task_packages_root(self) -> Path:
        return self.repo_root / "docs" / "archived" / "task-packages"
