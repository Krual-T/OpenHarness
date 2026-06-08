
from .constants import (
    REQUIRED_STATUS_KEYS,
    TASK_ID_RE,
)
from .harness_context import HarnessContext, harness
from .models import (
    AgentType,
    CollaborationInfo,
    CreateTaskInput,
    DesignReviewMode,
    HarnessConfig,
    RuntimeWorkflowPackage,
    TaskInfo,
    TaskPackage,
    TaskPackageDocument,
    TaskStatus,
    TaskType,
    VerificationMethod,
    VerificationInfo,
    Workflow,
    parse_status,
)
from .workflows import (
    ACTIVE_STATUSES,
    STANDARD_WORKFLOW,
    MECHANICAL_WORKFLOW,
    workflow_for,
)
from .core import (
    ALL_DESIGN_FILES,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    humanize_task_name,
    resolve_task_package,
    slugify_task_name,
    summarize_task_package,
)
from .display import describe_stage, output_state_hook
from .transition_engine import execute_transition
from .validate import validate_task_package
from .cli import app

ALL_STATUS_VALUES = frozenset(s.value for s in TaskStatus)

__all__ = [
    # Harness context
    "HarnessContext", "harness",
    # Domain types
    "AgentType",
    "TaskStatus", "TaskType", "VerificationMethod", "DesignReviewMode",
    "CollaborationInfo", "VerificationInfo",
    "Workflow", "TaskInfo", "parse_status",
    "STANDARD_WORKFLOW", "MECHANICAL_WORKFLOW", "workflow_for",
    # Backward-compat
    "ACTIVE_STATUSES", "ALL_STATUS_VALUES",
    # Models
    "HarnessConfig", "TaskPackage", "TaskPackageDocument",
    "CreateTaskInput", "RuntimeWorkflowPackage",
    # Constants
    "ALL_DESIGN_FILES", "REQUIRED_STATUS_KEYS", "TASK_ID_RE",
    # Core (public API)
    "discover_task_packages", "find_duplicate_task_ids",
    "resolve_task_package", "summarize_task_package",
    "allocate_next_task_id", "create_task_package",
    "humanize_task_name", "slugify_task_name",
    # Validation
    "validate_task_package",
    # CLI
    "app",
]
