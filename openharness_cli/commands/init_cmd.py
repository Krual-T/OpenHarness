from __future__ import annotations

from pathlib import Path

import typer


def init(
    repo: str = typer.Option(".", "--repo", help="Repository root"),
) -> None:
    """Initialize OpenHarness local repository files."""
    repo_root = Path(repo).resolve()
    harness_root = repo_root / ".harness"
    harness_root.mkdir(parents=True, exist_ok=True)
    (harness_root / ".gitignore").write_text("*\n", encoding="utf-8")
    print(f"Initialized OpenHarness local directory: {harness_root}")
