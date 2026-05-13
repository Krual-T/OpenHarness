from __future__ import annotations

from .cli import build_parser
from .commands import (
    cmd_bootstrap, cmd_check_tasks, cmd_init, cmd_new_task,
    cmd_rwp, cmd_transition, cmd_update, cmd_verify,
)
from .lifecycle import _run_command  # noqa: F401 — test monkeypatch
from .models import TaskPackage, TaskScaffoldRequest  # noqa: F401 — test compat
from .repository import _load_yaml  # noqa: F401 — test compat


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)
