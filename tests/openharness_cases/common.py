from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

import pytest

openharness = importlib.import_module("openharness_cli.main")
from openharness_cli import (
    ACTIVE_STATUSES,
    TaskScaffoldRequest,
    REQUIRED_TASK_PACKAGE_FILES,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    load_manifest,
    slugify_task_name,
    summarize_task_package,
    validate_task_package,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills" / "using-openharness"
