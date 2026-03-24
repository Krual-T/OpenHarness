from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pytest

SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
TESTS_ROOT = SKILL_ROOT / "tests"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

import openharness
from openharness import (
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


REPO_ROOT = Path(__file__).resolve().parents[4]
