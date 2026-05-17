from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path

from ..repository import (
    discover_runtime_workflow_packages,
    resolve_runtime_workflow_package,
    resolve_runtime_workflow_script,
)


def cmd_rwp_list(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        packages = discover_runtime_workflow_packages(repo_root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    if not packages:
        print("No runtime workflow packages found.")
        return 0
    for p in packages:
        rel_root = p.root.relative_to(repo_root)
        print(f"- {p.name} - {p.description}")
        print(f"  path: {rel_root}")
    return 0


def cmd_rwp_show(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        pkg = resolve_runtime_workflow_package(repo_root, args.workflow)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(pkg.workflow_path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_rwp_run(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    try:
        script_path = resolve_runtime_workflow_script(repo_root, args.workflow, args.script)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    runtime_api_root = Path(__file__).resolve().parents[1]
    pythonpath = os.pathsep.join([
        str(runtime_api_root),
        *([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []),
    ])
    os.environ["PYTHONPATH"] = pythonpath
    cmd_parts = ["uv", "run", "python", str(script_path), *list(args.script_args)]
    print(f"$ {shlex.join(cmd_parts)}")
    completed = subprocess.run(cmd_parts, cwd=repo_root)
    return completed.returncode
