from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

import typer

from ..core import (
    discover_runtime_workflow_packages,
    resolve_runtime_workflow_package,
    resolve_runtime_workflow_script,
)

rwp_app = typer.Typer(help="Discover and run Runtime Workflow Packages.")


@rwp_app.command(name="list")
def rwp_list(ctx: typer.Context) -> None:
    """List Runtime Workflow Package summaries."""
    hx = ctx.obj
    try:
        packages = discover_runtime_workflow_packages()
    except ValueError as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)
    if not packages:
        print("No runtime workflow packages found.")
        return
    for p in packages:
        rel_root = p.root.relative_to(hx.repo_root)
        print(f"- {p.name} - {p.description}")
        print(f"  path: {rel_root}")


@rwp_app.command(name="show")
def rwp_show(
    workflow: str = typer.Argument(...),
) -> None:
    """Show a Runtime Workflow Package workflow.md."""
    try:
        pkg = resolve_runtime_workflow_package(workflow)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)
    print(pkg.workflow_path.read_text(encoding="utf-8"), end="")


@rwp_app.command(name="run")
def rwp_run(
    ctx: typer.Context,
    workflow: str = typer.Argument(...),
    script: str = typer.Argument(...),
    script_args: list[str] = typer.Argument(default_factory=list),
) -> None:
    """Run an explicit Python script from a Runtime Workflow Package."""
    hx = ctx.obj
    try:
        script_path = resolve_runtime_workflow_script(workflow, script)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        raise typer.Exit(code=1)
    runtime_api_root = Path(__file__).resolve().parents[1]
    pythonpath = os.pathsep.join([
        str(runtime_api_root),
        *([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []),
    ])
    os.environ["PYTHONPATH"] = pythonpath
    cmd_parts = ["uv", "run", "python", str(script_path), *list(script_args)]
    print(f"$ {shlex.join(cmd_parts)}")
    completed = subprocess.run(cmd_parts, cwd=hx.repo_root)
    raise typer.Exit(code=completed.returncode)
