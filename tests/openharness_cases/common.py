from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

openharness = importlib.import_module("openharness_cli.main")
from openharness_cli import (
    ACTIVE_STATUSES,
    ALL_DESIGN_FILES,
    CreateTaskInput,
    HarnessConfig,
    HarnessContext,
    TaskPackageDocument,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    slugify_task_name,
    summarize_task_package,
    validate_task_package,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills" / "using-openharness"


def setup_harness(repo_root: Path) -> HarnessContext:
    """Activate a HarnessContext for tests that call @harness-decorated functions."""
    return HarnessContext(repo_root).activate()
