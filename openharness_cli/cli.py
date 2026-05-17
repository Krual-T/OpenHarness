from __future__ import annotations

import argparse

from . import commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Openharness repository workflow CLI.",
        epilog=(
            "Examples:\n"
            "  openharness task-package list\n"
            "  openharness task-package new feature-name --auto-id\n"
            "  openharness check-tasks\n"
            "  openharness init\n"
            "  openharness update"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── task-package ──────────────────────────────────────────────────
    task_package_parser = subparsers.add_parser(
        "task-package", help="Manage task packages.",
        description="List or create task packages.",
        epilog=(
            "Examples:\n"
            "  openharness task-package list\n"
            "  openharness task-package list --json\n"
            "  openharness task-package new feature-name --auto-id"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    task_package_parser.add_argument("--repo", default=".", help="Repository root")
    tp_subparsers = task_package_parser.add_subparsers(dest="tp_command", required=True)

    tp_list_parser = tp_subparsers.add_parser(
        "list", help="List task packages.",
        description="List active task packages with current status and next steps.",
        epilog="Example:\n  openharness task-package list\n  openharness task-package list --json\n  openharness task-package list --all",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    tp_list_parser.add_argument("--json", action="store_true", help="Print JSON output")
    tp_list_parser.add_argument("--all", action="store_true", help="Include archived task packages")
    tp_list_parser.set_defaults(handler=commands.cmd_task_package_list)

    tp_new_parser = tp_subparsers.add_parser(
        "new", help="Create a new task package from harness templates.",
        description="Create a new task package from harness templates.",
        epilog=(
            "Example:\n"
            "  openharness task-package new feature-name --auto-id --title \"Feature Title\"\n"
            "  openharness task-package new feature-name --task-id OH-999 --title \"Feature Title\""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    tp_new_parser.add_argument("task_name", help="Directory slug or human-readable task name")
    tp_new_parser.add_argument("--task-id", default="", help="Stable task id; omit with `--auto-id` to allocate one")
    tp_new_parser.add_argument("--title", default="", help="Human-readable task title")
    tp_new_parser.add_argument("--auto-id", action="store_true", help="Allocate the next stable task id automatically")
    tp_new_parser.add_argument("--owner", default="unassigned", help="Initial owner (defaults to git config user.name if not specified)")
    tp_new_parser.add_argument("--summary", default="", help="Short summary")
    tp_new_parser.add_argument("--status", default="proposing", help="Initial status")
    tp_new_parser.set_defaults(handler=commands.cmd_task_package_new)

    # ── init ──────────────────────────────────────────────────────────
    init_parser = subparsers.add_parser(
        "init", help="Initialize OpenHarness local repository files.",
        description="Initialize OpenHarness local repository files.",
        epilog="Example:\n  openharness init\n  openharness init --repo /path/to/repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    init_parser.add_argument("--repo", default=".", help="Repository root")
    init_parser.set_defaults(handler=commands.cmd_init)

    # ── check-tasks ───────────────────────────────────────────────────
    check_parser = subparsers.add_parser(
        "check-tasks", help="Validate repository task packages against harness protocol.",
        description="Validate repository task packages against harness protocol.",
        epilog="Example:\n  openharness check-tasks\n  openharness check-tasks --repo /path/to/repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=commands.cmd_check_tasks)

    # ── rwp ───────────────────────────────────────────────────────────
    rwp_parser = subparsers.add_parser(
        "rwp", help="Discover and run Runtime Workflow Packages.",
        description="Discover and run Runtime Workflow Packages.",
        epilog=(
            "Examples:\n"
            "  openharness rwp list\n"
            "  openharness rwp show lark-message-runtime-validation\n"
            "  openharness rwp run lark-message-runtime-validation send_message_smoke.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rwp_parser.add_argument("--repo", default=".", help="Repository root")
    rwp_subparsers = rwp_parser.add_subparsers(dest="rwp_command", required=True)

    rwp_list_parser = rwp_subparsers.add_parser(
        "list", help="List Runtime Workflow Package summaries.",
        description="List Runtime Workflow Package summaries.", formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rwp_list_parser.set_defaults(handler=commands.cmd_rwp)

    rwp_show_parser = rwp_subparsers.add_parser(
        "show", help="Show a Runtime Workflow Package workflow.md.",
        description="Show a Runtime Workflow Package workflow.md.", formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rwp_show_parser.add_argument("workflow", help="Runtime workflow name or directory slug")
    rwp_show_parser.set_defaults(handler=commands.cmd_rwp)

    rwp_run_parser = rwp_subparsers.add_parser(
        "run", help="Run an explicit Python script from a Runtime Workflow Package.",
        description="Run an explicit Python script from a Runtime Workflow Package.", formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rwp_run_parser.add_argument("workflow", help="Runtime workflow name or directory slug")
    rwp_run_parser.add_argument("script", help="Python script under the workflow scripts directory")
    rwp_run_parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments forwarded to the script")
    rwp_run_parser.set_defaults(handler=commands.cmd_rwp)

    # ── transition ────────────────────────────────────────────────────
    transition_parser = subparsers.add_parser(
        "transition", help="Move a task package to a legal workflow status.",
        description="Move a task package to a legal workflow status.",
        epilog=(
            "Example:\n"
            "  openharness transition my-task requirements_designed\n"
            "  openharness transition OH-027 verification_designing"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    transition_parser.add_argument("task", help="Task package name or task id")
    transition_parser.add_argument("target_status", help="Target workflow status")
    transition_parser.add_argument("--repo", default=".", help="Repository root")
    transition_parser.set_defaults(handler=commands.cmd_transition)

    # ── update ────────────────────────────────────────────────────────
    update_parser = subparsers.add_parser(
        "update", help="Update the OpenHarness clone and refresh the installed CLI tool.",
        description="Update the OpenHarness clone and refresh the installed CLI tool.",
        epilog=(
            "This command runs `git pull` in the OpenHarness source clone first, then\n"
            "refreshes the installed CLI tool with `uv tool upgrade openharness`.\n"
            "Use `--force-sync` only when you explicitly want to discard local changes\n"
            "in the OpenHarness source clone and reset it to its upstream branch.\n\n"
            "Example:\n"
            "  openharness update\n"
            "  openharness update --force-sync"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    update_parser.add_argument(
        "--force-sync", action="store_true",
        help="Discard local changes in the OpenHarness source clone and reset it to its upstream branch.",
    )
    update_parser.add_argument(
        "--mode", choices=("pull", "force-sync"),
        help="Use one update mode for this run, overriding the saved default mode.",
    )
    update_parser.add_argument(
        "--set-default-mode", choices=("pull", "force-sync"),
        help="Save the default update mode and exit without running update.",
    )
    update_parser.set_defaults(handler=commands.cmd_update)


    return parser
