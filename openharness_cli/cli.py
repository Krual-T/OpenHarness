from __future__ import annotations

import argparse


class _HelpFormatter(argparse.RawDescriptionHelpFormatter):
    pass


def build_parser(
    *,
    cmd_bootstrap,
    cmd_check_tasks,
    cmd_new_task,
    cmd_transition,
    cmd_verify,
    cmd_update,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Openharness repository workflow CLI.",
        epilog=(
            "Examples:\n"
            "  openharness bootstrap\n"
            "  openharness check-tasks\n"
            "  openharness update"
        ),
        formatter_class=_HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Inspect project harness entrypoints and task packages.",
        description="Inspect project harness entrypoints and task packages.",
        epilog=(
            "Example:\n"
            "  openharness bootstrap\n"
            "  openharness bootstrap --json\n"
            "  openharness bootstrap --all"
        ),
        formatter_class=_HelpFormatter,
    )
    bootstrap_parser.add_argument("--repo", default=".", help="Repository root")
    bootstrap_parser.add_argument("--json", action="store_true", help="Print JSON output")
    bootstrap_parser.add_argument("--all", action="store_true", help="Include non-active task packages")
    bootstrap_parser.set_defaults(handler=cmd_bootstrap)

    check_parser = subparsers.add_parser(
        "check-tasks",
        help="Validate repository task packages against harness protocol.",
        description="Validate repository task packages against harness protocol.",
        epilog=(
            "Example:\n"
            "  openharness check-tasks\n"
            "  openharness check-tasks --repo /path/to/repo"
        ),
        formatter_class=_HelpFormatter,
    )
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=cmd_check_tasks)

    new_design_parser = subparsers.add_parser(
        "new-task",
        help="Create a new task package from harness templates.",
        description="Create a new task package from harness templates.",
        epilog=(
            "Example:\n"
            "  openharness new-task feature-name --auto-id --title \"Feature Title\"\n"
            "  openharness new-task feature-name --task-id OH-999 --title \"Feature Title\""
        ),
        formatter_class=_HelpFormatter,
    )
    new_design_parser.add_argument("task_name", help="Directory slug or human-readable task name")
    new_design_parser.add_argument("--task-id", default="", help="Stable task id; omit with `--auto-id` to allocate one")
    new_design_parser.add_argument("--title", default="", help="Human-readable task title")
    new_design_parser.add_argument("--auto-id", action="store_true", help="Allocate the next stable task id automatically")
    new_design_parser.add_argument("--owner", default="unassigned", help="Initial owner")
    new_design_parser.add_argument("--summary", default="", help="Short summary")
    new_design_parser.add_argument("--status", default="proposed", help="Initial status")
    new_design_parser.add_argument("--repo", default=".", help="Repository root")
    new_design_parser.set_defaults(handler=cmd_new_task)

    transition_parser = subparsers.add_parser(
        "transition",
        help="Move a task package to a legal workflow status.",
        description="Move a task package to a legal workflow status.",
        epilog=(
            "Example:\n"
            "  openharness transition my-task requirements_ready\n"
            "  openharness transition OH-027 archived"
        ),
        formatter_class=_HelpFormatter,
    )
    transition_parser.add_argument("task", help="Task package name or task id")
    transition_parser.add_argument("target_status", help="Target workflow status")
    transition_parser.add_argument("--repo", default=".", help="Repository root")
    transition_parser.set_defaults(handler=cmd_transition)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Run harness verification for one task package or all active packages.",
        description="Run harness verification for one task package or all active packages.",
        epilog=(
            "Example:\n"
            "  openharness verify\n"
            "  openharness verify my-task\n"
            "  openharness verify --check-tasks-only"
        ),
        formatter_class=_HelpFormatter,
    )
    verify_parser.add_argument("design", nargs="?", default="", help="Task package name or task id")
    verify_parser.add_argument("--repo", default=".", help="Repository root")
    verify_parser.add_argument("--check-tasks-only", action="store_true", help="Only validate task package protocol")
    verify_parser.set_defaults(handler=cmd_verify)

    update_parser = subparsers.add_parser(
        "update",
        help="Update the OpenHarness clone and refresh the installed CLI tool.",
        description="Update the OpenHarness clone and refresh the installed CLI tool.",
        epilog=(
            "This command runs `git pull` in the OpenHarness source clone first, then\n"
            "refreshes the installed CLI tool with `uv tool upgrade openharness`.\n\n"
            "Example:\n"
            "  openharness update"
        ),
        formatter_class=_HelpFormatter,
    )
    update_parser.set_defaults(handler=cmd_update)

    return parser
