from __future__ import annotations

from .constants import (
    REQUIRED_STATUS_KEYS,
    TASK_ID_RE,
)
from .models import (
    CollaborationInfo,
    CreateTaskInput,
    DesignReviewMode,
    HarnessConfig,
    RuntimeWorkflowPackage,
    TaskInfo,
    TaskPackage,
    TaskStatus,
    TaskType,
    VerifyBy,
    VerificationInfo,
    Workflow,
    parse_status,
)
from .workflows import (
    ACTIVE_STATUSES,
    GATE_STATUSES,
    STANDARD_WORKFLOW,
    MECHANICAL_WORKFLOW,
    workflow_for,
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
from .transition_engine import execute_transition
from .validate import validate_task_package
from .cli import build_parser
from .main import main

ALL_STATUS_VALUES = frozenset(s.value for s in TaskStatus)

__all__ = [
    # Domain types
    "TaskStatus", "TaskType", "VerifyBy", "DesignReviewMode",
    "CollaborationInfo", "VerificationInfo",
    "Workflow", "TaskInfo", "parse_status",
    "STANDARD_WORKFLOW", "MECHANICAL_WORKFLOW", "workflow_for",
    # Backward-compat
    "ACTIVE_STATUSES", "GATE_STATUSES", "ALL_STATUS_VALUES",
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
