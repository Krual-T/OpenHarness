from __future__ import annotations

from .cli import build_parser
from .commands import (
    cmd_check_tasks, cmd_init, cmd_rwp,
    cmd_task_package_list, cmd_task_package_new,
    cmd_transition, cmd_update,
)
from .models import TaskPackage, CreateTaskInput  # noqa: F401 — test compat
from .repository import _load_yaml  # noqa: F401 — test compat


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)
