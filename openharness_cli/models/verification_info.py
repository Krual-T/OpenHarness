
from dataclasses import dataclass, field
from typing import Any, Optional

from .verify_by import VerifyBy


@dataclass
class VerificationInfo:
    verify_by: Optional[VerifyBy] = None
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Optional[dict[str, Any]]) -> VerificationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        vb_raw = str(raw.pop("verify_by", "")).strip()
        verify_by = None
        if vb_raw:
            try:
                verify_by = VerifyBy(vb_raw)
            except ValueError:
                pass
        return cls(verify_by=verify_by, _extra=raw)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.verify_by is not None:
            result["verify_by"] = self.verify_by.value
        return result
