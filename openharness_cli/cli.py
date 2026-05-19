
from pathlib import Path

import typer

from .harness_context import HarnessContext, find_harness_root
from .commands.update import update
from .commands.task_package import task_app
from .commands.rwp import rwp_app

app = typer.Typer(
    name="openharness",
    help="Openharness repository workflow CLI.",
)


@app.callback()
def main(ctx: typer.Context, repo: str = typer.Option(".", "--repo", help="Repository root")):
    hx = HarnessContext(find_harness_root(Path(repo))).activate()
    ctx.obj = hx


try:
    from .commands.init_cmd import init
except ModuleNotFoundError:
    def init(ctx: typer.Context, **kwargs):  # noqa: E306
        print("ERROR: missing dependencies, run `openharness update` first", flush=True)
        raise typer.Exit(code=1)


app.command()(init)
app.command()(update)
app.add_typer(task_app, name="task-package")
app.add_typer(rwp_app, name="rwp")
