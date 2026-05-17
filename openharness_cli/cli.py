from __future__ import annotations

import typer

from .commands.init_cmd import init
from .commands.update import update
from .commands.task_package import task_app
from .commands.rwp import rwp_app

app = typer.Typer(
    name="openharness",
    help="Openharness repository workflow CLI.",
)
app.command()(init)
app.command()(update)
app.add_typer(task_app, name="task-package")
app.add_typer(rwp_app, name="rwp")
