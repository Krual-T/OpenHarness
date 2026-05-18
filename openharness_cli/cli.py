from __future__ import annotations

from pathlib import Path

import typer

from .harness_context import HarnessContext
from .commands.init_cmd import init
from .commands.update import update
from .commands.task_package import task_app
from .commands.rwp import rwp_app

app = typer.Typer(
    name="openharness",
    help="Openharness repository workflow CLI.",
)


@app.callback()
def main(ctx: typer.Context, repo: str = typer.Option(".", "--repo", help="Repository root")):
    hx = HarnessContext(Path(repo).resolve()).activate()
    ctx.obj = hx


app.command()(init)
app.command()(update)
app.add_typer(task_app, name="task-package")
app.add_typer(rwp_app, name="rwp")
