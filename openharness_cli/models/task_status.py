
from enum import StrEnum
from typing import Optional


def parse_status(value: str) -> Optional[TaskStatus]:
    try:
        return TaskStatus(value)
    except ValueError:
        return None


class TaskStatus(StrEnum):
    PROPOSING = ("proposing", "skills/using-openharness/states/brainstorming/SKILL.md")
    REQUIREMENTS_DESIGNED = ("requirements_designed", "")
    OVERVIEW_DESIGNING = ("overview_designing", "skills/using-openharness/states/exploring-solution-space/SKILL.md")
    OVERVIEW_DESIGNED = ("overview_designed", "")
    DETAILED_DESIGNING = ("detailed_designing", "skills/using-openharness/states/detailed-design/SKILL.md")
    DETAILED_DESIGNED = ("detailed_designed", "")
    VERIFICATION_DESIGNING = ("verification_designing", "skills/using-openharness/states/verification-designing/SKILL.md")
    VERIFICATION_DESIGNED = ("verification_designed", "")
    IMPLEMENTING = ("implementing", "skills/using-openharness/states/implementing/SKILL.md")
    IMPLEMENTED = ("implemented", "")
    VERIFYING = ("verifying", "skills/using-openharness/states/verifying/SKILL.md")
    VERIFIED = ("verified", "")
    ARCHIVED = ("archived", "")

    def __new__(cls, value, hook):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.hook = hook
        return obj
