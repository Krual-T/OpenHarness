
from dataclasses import dataclass, field
from typing import Any, Optional

from .task_status import TaskStatus, parse_status
from .collaboration_info import CollaborationInfo
from .verification_info import VerificationInfo


@dataclass
class TaskInfo:
    id: str
    title: str
    status: TaskStatus
    summary: str
    owner: str
    created_at: str
    updated_at: str
    entrypoints: tuple[str, ...] = ()
    collaboration: Optional[CollaborationInfo] = None
    verification: Optional[VerificationInfo] = None
    _raw_status: Optional[str] = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @property
    def status_value(self) -> str:
        if self._raw_status is not None:
            return self._raw_status
        return self.status.value

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskInfo:
        raw = dict(d)

        status_raw = str(raw.pop("status", "")).strip()
        _raw_status: Optional[str] = None
        if status_raw:
            parsed = parse_status(status_raw)
            if parsed is None:
                status = TaskStatus.PROPOSING
                _raw_status = status_raw
            else:
                status = parsed
        else:
            status = TaskStatus.PROPOSING

        collab_raw = raw.pop("collaboration", None)
        collaboration = CollaborationInfo.from_dict(collab_raw) if isinstance(collab_raw, dict) else None

        verif_raw = raw.pop("verification", None)
        verification = VerificationInfo.from_dict(verif_raw) if isinstance(verif_raw, dict) else None

        ep_raw = raw.pop("entrypoints", None)
        entrypoints: tuple[str, ...] = ()
        if isinstance(ep_raw, list):
            entrypoints = tuple(str(item).strip() for item in ep_raw if str(item).strip())

        return cls(
            id=str(raw.pop("id", "")).strip(),
            title=str(raw.pop("title", "")).strip(),
            status=status,
            summary=str(raw.pop("summary", "")).strip(),
            owner=str(raw.pop("owner", "")).strip(),
            created_at=str(raw.pop("created_at", "")).strip(),
            updated_at=str(raw.pop("updated_at", "")).strip(),
            entrypoints=entrypoints,
            collaboration=collaboration,
            verification=verification,
            _raw_status=_raw_status,
            _extra=raw,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        result["id"] = self.id
        result["title"] = self.title
        result["status"] = self.status_value
        result["summary"] = self.summary
        result["owner"] = self.owner
        result["created_at"] = self.created_at
        result["updated_at"] = self.updated_at
        if self.entrypoints:
            result["entrypoints"] = list(self.entrypoints)
        if self.collaboration is not None:
            result["collaboration"] = self.collaboration.to_dict()
        if self.verification is not None:
            result["verification"] = self.verification.to_dict()
        for k, v in self._extra.items():
            result[k] = v
        return result
