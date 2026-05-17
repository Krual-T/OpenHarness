from __future__ import annotations

from .constants import (
    REQUIRED_STATUS_KEYS,
    TASK_ID_RE,
)
from .domain import (
    DesignReviewMode,
    TaskInfo,
    TaskStatus,
    TaskType,
    VerifyBy,
    Workflow,
)
from .workflows import (
    STANDARD_WORKFLOW,
    MECHANICAL_WORKFLOW,
    workflow_for,
)
from .models import (
    HarnessConfig,
    RuntimeWorkflowPackage,
    TaskPackage,
    CreateTaskInput,
)
from .repository import (
    ALL_DESIGN_FILES,
    allocate_next_task_id,
    create_task_package,
    create_task_package_with_auto_id,
    discover_task_packages,
    find_duplicate_task_ids,
    humanize_task_name,
    load_config,
    resolve_task_package,
    slugify_task_name,
    summarize_task_package,
)
from .display import describe_stage, output_state_hook
from .workflow import execute_transition
from .validate import validate_task_package
from .cli import build_parser
from .main import main

# Backward-compatible computed constants
_ACTIVE = STANDARD_WORKFLOW.active_statuses | MECHANICAL_WORKFLOW.active_statuses
ACTIVE_STATUSES = frozenset(s.value for s in _ACTIVE)
GATE_STATUSES = frozenset(s.value for s in STANDARD_WORKFLOW.gate_statuses | MECHANICAL_WORKFLOW.gate_statuses)

__all__ = [
    # Domain types
    "TaskStatus", "TaskType", "VerifyBy", "DesignReviewMode",
    "Workflow", "TaskInfo",
    "STANDARD_WORKFLOW", "MECHANICAL_WORKFLOW", "workflow_for",
    # Backward-compat
    "ACTIVE_STATUSES", "GATE_STATUSES",
    # Models
    "HarnessConfig", "TaskPackage", "CreateTaskInput", "RuntimeWorkflowPackage",
    # Constants
    "ALL_DESIGN_FILES", "REQUIRED_STATUS_KEYS", "TASK_ID_RE",
    # Repository (public API)
    "load_config", "discover_task_packages", "find_duplicate_task_ids",
    "resolve_task_package", "summarize_task_package",
    "allocate_next_task_id", "create_task_package", "create_task_package_with_auto_id",
    "humanize_task_name", "slugify_task_name",
    # Validation
    "validate_task_package",
    # CLI
    "build_parser", "main",
]
