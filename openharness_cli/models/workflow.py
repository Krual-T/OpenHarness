
from dataclasses import dataclass
from typing import Callable, Optional

from .task_status import TaskStatus
from .task_package_document import TaskPackageDocument


@dataclass(frozen=True)
class Workflow:
    name: str
    status_sequence: tuple[TaskStatus, ...]
    gate_next: dict[TaskStatus, TaskStatus]
    gate_preconditions: dict[TaskStatus, Callable[..., list[str]]]
    file_additions: dict[TaskStatus, tuple[TaskPackageDocument, ...]]
    working_files: dict[TaskStatus, tuple[TaskPackageDocument, ...]]
    section_specs: dict[TaskPackageDocument, tuple[tuple[TaskPackageDocument, str], ...]]
    descriptions: dict[TaskStatus, str]
    next_steps: dict[TaskStatus, str]

    @property
    def gate_statuses(self) -> frozenset[TaskStatus]:
        return frozenset(self.gate_next)

    @property
    def active_statuses(self) -> frozenset[TaskStatus]:
        return frozenset(
            s for s in self.status_sequence
            if s not in self.gate_next and s != TaskStatus.ARCHIVED
        )

    def next_status(self, current: TaskStatus) -> Optional[TaskStatus]:
        if current not in self.status_sequence:
            return None
        idx = self.status_sequence.index(current)
        if idx >= len(self.status_sequence) - 1:
            return None
        return self.status_sequence[idx + 1]

    def required_files(self, status: TaskStatus) -> tuple[TaskPackageDocument, ...]:
        base = TaskPackageDocument.base_files()
        accumulated = list(base)
        for s in self.status_sequence:
            accumulated.extend(self.file_additions.get(s, ()))
            if s == status:
                break
        return tuple(accumulated)

    def scaffold_files(self, status: TaskStatus) -> tuple[TaskPackageDocument, ...]:
        docs = list(self.required_files(status))
        docs.extend(self.working_files.get(status, ()))
        return tuple(dict.fromkeys(docs))

    def section_requirements(self, status: TaskStatus) -> tuple[tuple[TaskPackageDocument, str], ...]:
        sections: list[tuple[TaskPackageDocument, str]] = []
        accumulated_files: set[TaskPackageDocument] = set()
        for s in self.status_sequence:
            for f in self.file_additions.get(s, ()):
                accumulated_files.add(f)
                if f in self.section_specs:
                    sections.extend(self.section_specs[f])
            if s == status:
                break
        return tuple(sections)

    def resolve_gate(self, package: object, target: TaskStatus) -> tuple[Optional[TaskStatus], list[str]]:
        next_s = self.gate_next.get(target)
        if next_s is None:
            return None, []
        precond = self.gate_preconditions.get(target)
        if precond is not None:
            errors = precond(package)
            if errors:
                return None, errors
        return next_s, []
