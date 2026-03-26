from __future__ import annotations

from .constants import (
    ACTIVE_STATUSES,
    REQUIRED_TASK_PACKAGE_FILES,
    VERIFYABLE_STATUSES,
)
from .models import HarnessManifest, TaskPackage, TaskScaffoldRequest
from .repository import (
    _current_date,
    _load_yaml,
    _utc_now,
    _utc_timestamp,
    _write_yaml,
    allocate_next_task_id,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    humanize_task_name,
    load_manifest,
    resolve_task_package,
    slugify_task_name,
    summarize_task_package,
)
from .validation import validate_task_package
from . import lifecycle
from .cli import build_parser as _build_parser
from .commands import (
    cmd_bootstrap as _cmd_bootstrap,
    cmd_check_tasks as _cmd_check_tasks,
    cmd_new_task as _cmd_new_task,
    cmd_transition as _cmd_transition,
    cmd_verify as _cmd_verify,
)


_run_command = lifecycle._run_command


def cmd_bootstrap(args):
    return _cmd_bootstrap(args)


def cmd_check_tasks(args):
    return _cmd_check_tasks(args)


def cmd_new_task(args):
    return _cmd_new_task(args)


def cmd_transition(args):
    return _cmd_transition(args)


def cmd_verify(args):
    lifecycle._run_command = globals()["_run_command"]
    return _cmd_verify(args)


def build_parser():
    return _build_parser(
        cmd_bootstrap=cmd_bootstrap,
        cmd_check_tasks=cmd_check_tasks,
        cmd_new_task=cmd_new_task,
        cmd_transition=cmd_transition,
        cmd_verify=cmd_verify,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)
