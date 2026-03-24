from __future__ import annotations

import argparse


def build_parser(
    *,
    cmd_bootstrap,
    cmd_check_tasks,
    cmd_new_task,
    cmd_transition,
    cmd_verify,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Openharness repository workflow CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Inspect project harness entrypoints and task packages.")
    bootstrap_parser.add_argument("--repo", default=".", help="Repository root")
    bootstrap_parser.add_argument("--json", action="store_true", help="Print JSON output")
    bootstrap_parser.add_argument("--all", action="store_true", help="Include non-active task packages")
    bootstrap_parser.set_defaults(handler=cmd_bootstrap)

    check_parser = subparsers.add_parser(
        "check-tasks",
        help="Validate repository task packages against harness protocol.",
    )
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=cmd_check_tasks)

    new_design_parser = subparsers.add_parser(
        "new-task",
        help="Create a new task package from harness templates.",
    )
    new_design_parser.add_argument("task_name", help="Directory slug or human-readable task name")
    new_design_parser.add_argument("legacy_task_id", nargs="?", help="Stable task id, such as OR-016")
    new_design_parser.add_argument("legacy_title", nargs="?", help="Human-readable task title")
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
    )
    transition_parser.add_argument("task", help="Task package name or task id")
    transition_parser.add_argument("target_status", help="Target workflow status")
    transition_parser.add_argument("--repo", default=".", help="Repository root")
    transition_parser.set_defaults(handler=cmd_transition)

    verify_parser = subparsers.add_parser("verify", help="Run harness verification for one task package or all active packages.")
    verify_parser.add_argument("design", nargs="?", default="", help="Task package name or task id")
    verify_parser.add_argument("--repo", default=".", help="Repository root")
    verify_parser.add_argument("--check-tasks-only", action="store_true", help="Only validate task package protocol")
    verify_parser.set_defaults(handler=cmd_verify)

    return parser
