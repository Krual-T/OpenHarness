from __future__ import annotations

from typing import Optional

from .cli import build_parser
from .commands import (
    cmd_check_tasks, cmd_init, cmd_rwp_list, cmd_rwp_show, cmd_rwp_run,
    cmd_task_package_list, cmd_task_package_new,
    cmd_transition, cmd_update,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)
