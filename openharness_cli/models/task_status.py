
from enum import StrEnum
from typing import Optional


def parse_status(value: str) -> Optional[TaskStatus]:
    try:
        return TaskStatus(value)
    except ValueError:
        return None


class TaskStatus(StrEnum):
    PROPOSING = ("proposing", "skills/using-openharness/states/brainstorming/instructions.md")
    REQUIREMENTS_DESIGNED = ("requirements_designed", "")
    OVERVIEW_DESIGNING = ("overview_designing", "skills/using-openharness/states/exploring-solution-space/instructions.md")
    OVERVIEW_DESIGNED = ("overview_designed", "")
    DETAILED_DESIGNING = ("detailed_designing", "skills/using-openharness/states/detailed-design/instructions.md")
    DETAILED_DESIGNED = ("detailed_designed", "")
    VERIFICATION_DESIGNING = ("verification_designing", "skills/using-openharness/states/verification-designing/instructions.md")
    VERIFICATION_DESIGNED = ("verification_designed", "")
    IMPLEMENTING = ("implementing", "skills/using-openharness/states/implementing/instructions.md")
    IMPLEMENTED = ("implemented", "")
    VERIFYING = ("verifying", "skills/using-openharness/states/verifying/instructions.md")
    VERIFIED = ("verified", "")
    ARCHIVED = ("archived", "")

    def __new__(cls, value, hook):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.hook = hook
        return obj
