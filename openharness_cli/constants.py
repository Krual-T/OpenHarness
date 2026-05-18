
import re

# ═══════════════════════════════════════════════════════════════════════════════
# Retained constants (still used by validation / repository)
# ═══════════════════════════════════════════════════════════════════════════════

REQUIRED_STATUS_KEYS = (
    "id",
    "title",
    "status",
    "summary",
    "owner",
    "created_at",
    "updated_at",
    "done_criteria",
    "verification",
)

# ── Regex patterns ────────────────────────────────────────────────────────

PLACEHOLDER_BULLET_RE = re.compile(r"^[-*]\s*$")
PLACEHOLDER_NUMBERED_RE = re.compile(r"^\d+\.\s*$")
LABEL_ONLY_RE = re.compile(r"^[-*]\s+[^:]+:\s*$")
TASK_ID_RE = re.compile(r"^([A-Za-z]+)-(\d+)$")
