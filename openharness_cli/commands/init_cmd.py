from __future__ import annotations

import typer


def init(
    ctx: typer.Context,
) -> None:
    """Initialize OpenHarness local repository files."""
    hx = ctx.obj
    harness_root = hx.repo_root / ".harness"
    harness_root.mkdir(parents=True, exist_ok=True)
    (harness_root / ".gitignore").write_text("*\n", encoding="utf-8")
    print(f"Initialized OpenHarness local directory: {harness_root}")
