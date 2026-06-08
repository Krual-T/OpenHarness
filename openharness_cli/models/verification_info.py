
from dataclasses import dataclass, field
from typing import Any, Optional

from .verification_method import VerificationMethod


@dataclass
class RwpVerificationInfo:
    enabled: Optional[bool] = None
    raw_enabled: Any = None
    reason: str = ""
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Optional[dict[str, Any]]) -> RwpVerificationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        enabled_raw = raw.pop("enabled", None)
        enabled = enabled_raw if isinstance(enabled_raw, bool) else None
        reason = str(raw.pop("reason", "")).strip()
        return cls(enabled=enabled, raw_enabled=enabled_raw, reason=reason, _extra=raw)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.enabled is not None:
            result["enabled"] = self.enabled
        if self.reason:
            result["reason"] = self.reason
        return result


@dataclass
class VerificationInfo:
    method: Optional[VerificationMethod] = None
    raw_method: str = ""
    rwp: RwpVerificationInfo = field(default_factory=RwpVerificationInfo)
    _extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Optional[dict[str, Any]]) -> VerificationInfo:
        if d is None:
            return cls()
        raw = dict(d)
        method_raw = str(raw.pop("method", "")).strip()
        method = None
        if method_raw:
            try:
                method = VerificationMethod(method_raw)
            except ValueError:
                pass
        rwp_raw = raw.pop("rwp", None)
        rwp = RwpVerificationInfo.from_dict(rwp_raw) if isinstance(rwp_raw, dict) else RwpVerificationInfo()
        return cls(method=method, raw_method=method_raw, rwp=rwp, _extra=raw)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._extra)
        if self.method is not None:
            result["method"] = self.method.value
        elif self.raw_method:
            result["method"] = self.raw_method
        result["rwp"] = self.rwp.to_dict()
        return result
