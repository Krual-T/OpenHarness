from __future__ import annotations

import argparse

from . import commands


class _HelpFormatter(argparse.RawDescriptionHelpFormatter):
    pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Openharness repository workflow CLI.",
        epilog=(
            "Examples:\n"
            "  openharness bootstrap\n"
            "  openharness check-tasks\n"
            "  openharness init\n"
            "  openharness update"
        ),
        formatter_class=_HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser(
        "bootstrap", help="Inspect project harness entrypoints and task packages.",
        description="Inspect project harness entrypoints and task packages.",
        epilog="Example:\n  openharness bootstrap\n  openharness bootstrap --json\n  openharness bootstrap --all",
        formatter_class=_HelpFormatter,
    )
    bootstrap_parser.add_argument("--repo", default=".", help="Repository root")
    bootstrap_parser.add_argument("--json", action="store_true", help="Print JSON output")
    bootstrap_parser.add_argument("--all", action="store_true", help="Include non-active task packages")
    bootstrap_parser.set_defaults(handler=commands.cmd_bootstrap)

    init_parser = subparsers.add_parser(
        "init", help="Initialize OpenHarness local repository files.",
        description="Initialize OpenHarness local repository files.",
        epilog="Example:\n  openharness init\n  openharness init --repo /path/to/repo",
        formatter_class=_HelpFormatter,
    )
    init_parser.add_argument("--repo", default=".", help="Repository root")
    init_parser.set_defaults(handler=commands.cmd_init)

    check_parser = subparsers.add_parser(
        "check-tasks", help="Validate repository task packages against harness protocol.",
        description="Validate repository task packages against harness protocol.",
        epilog="Example:\n  openharness check-tasks\n  openharness check-tasks --repo /path/to/repo",
        formatter_class=_HelpFormatter,
    )
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=commands.cmd_check_tasks)

    new_design_parser = subparsers.add_parser(
        "new-task", help="Create a new task package from harness templates.",
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
    new_design_parser.add_argument("--status", default="proposing", help="Initial status")
    new_design_parser.add_argument("--repo", default=".", help="Repository root")
    new_design_parser.set_defaults(handler=commands.cmd_new_task)

    rwp_parser = subparsers.add_parser(
        "rwp", help="Discover and run Runtime Workflow Packages.",
        description="Discover and run Runtime Workflow Packages.",
        epilog=(
            "Examples:\n"
            "  openharness rwp list\n"
            "  openharness rwp show lark-message-runtime-validation\n"
            "  openharness rwp run lark-message-runtime-validation send_message_smoke.py"
        ),
        formatter_class=_HelpFormatter,
    )
    rwp_parser.add_argument("--repo", default=".", help="Repository root")
    rwp_subparsers = rwp_parser.add_subparsers(dest="rwp_command", required=True)

    rwp_list_parser = rwp_subparsers.add_parser(
        "list", help="List Runtime Workflow Package summaries.",
        description="List Runtime Workflow Package summaries.", formatter_class=_HelpFormatter,
    )
    rwp_list_parser.set_defaults(handler=commands.cmd_rwp)

    rwp_show_parser = rwp_subparsers.add_parser(
        "show", help="Show a Runtime Workflow Package workflow.md.",
        description="Show a Runtime Workflow Package workflow.md.", formatter_class=_HelpFormatter,
    )
    rwp_show_parser.add_argument("workflow", help="Runtime workflow name or directory slug")
    rwp_show_parser.set_defaults(handler=commands.cmd_rwp)

    rwp_run_parser = rwp_subparsers.add_parser(
        "run", help="Run an explicit Python script from a Runtime Workflow Package.",
        description="Run an explicit Python script from a Runtime Workflow Package.", formatter_class=_HelpFormatter,
    )
    rwp_run_parser.add_argument("workflow", help="Runtime workflow name or directory slug")
    rwp_run_parser.add_argument("script", help="Python script under the workflow scripts directory")
    rwp_run_parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments forwarded to the script")
    rwp_run_parser.set_defaults(handler=commands.cmd_rwp)

    transition_parser = subparsers.add_parser(
        "transition", help="Move a task package to a legal workflow status.",
        description="Move a task package to a legal workflow status.",
        epilog=(
            "Example:\n"
            "  openharness transition my-task requirements_designed\n"
            "  openharness transition OH-027 archived"
        ),
        formatter_class=_HelpFormatter,
    )
    transition_parser.add_argument("task", help="Task package name or task id")
    transition_parser.add_argument("target_status", help="Target workflow status")
    transition_parser.add_argument("--repo", default=".", help="Repository root")
    transition_parser.set_defaults(handler=commands.cmd_transition)

    verify_parser = subparsers.add_parser(
        "verify", help="Run harness verification for one task package or all active packages.",
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
    verify_parser.set_defaults(handler=commands.cmd_verify)

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
        formatter_class=_HelpFormatter,
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

    writing_guide_parser = subparsers.add_parser(
        "writing-guide", help="Discover and read task-package writing guides.",
        description="List or read the writing guide documents for task packages.",
        epilog="Example:\n  openharness writing-guide\n  openharness writing-guide read requirements",
        formatter_class=_HelpFormatter,
    )
    writing_guide_parser.add_argument("--repo", default=".", help="Repository root")
    writing_guide_subparsers = writing_guide_parser.add_subparsers(dest="writing_guide_command")

    writing_guide_list_parser = writing_guide_subparsers.add_parser(
        "list", help="List available writing guides.",
        description="List available writing guides.", formatter_class=_HelpFormatter,
    )
    writing_guide_list_parser.set_defaults(handler=commands.cmd_writing_guide)

    writing_guide_read_parser = writing_guide_subparsers.add_parser(
        "read", help="Read a writing guide.",
        description="Read a writing guide by name.", formatter_class=_HelpFormatter,
    )
    writing_guide_read_parser.add_argument(
        "name",
        choices=("requirements", "overview", "detailed", "verification", "evidence", "author-entry"),
        help="Writing guide name",
    )
    writing_guide_read_parser.set_defaults(handler=commands.cmd_writing_guide)

    # Default to list when no subcommand given
    writing_guide_parser.set_defaults(handler=commands.cmd_writing_guide, writing_guide_command="list")

    return parser
