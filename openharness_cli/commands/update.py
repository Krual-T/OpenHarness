from __future__ import annotations

import subprocess
from enum import StrEnum
from pathlib import Path

import typer

from ..core import load_yaml, write_yaml


class UpdateMode(StrEnum):
    PULL = "pull"
    FORCE_SYNC = "force-sync"


def _project_settings_path(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "settings.yaml").resolve()


def update(
    force_sync: bool = typer.Option(False, "--force-sync", help="Discard local changes and reset to upstream branch"),
    mode: str | None = typer.Option(None, "--mode", help="Override saved default update mode (pull / force-sync)"),
    set_default_mode: str | None = typer.Option(None, "--set-default-mode", help="Save default update mode and exit (pull / force-sync)"),
) -> None:
    """Update the OpenHarness clone and refresh the installed CLI tool."""
    repo_root = Path(__file__).resolve().parents[1]

    if set_default_mode:
        m = UpdateMode(str(set_default_mode))
        settings_path = _project_settings_path(repo_root)
        data = load_yaml(settings_path) if settings_path.exists() else {}
        update_settings = data.setdefault("update", {})
        if not isinstance(update_settings, dict):
            print(f"ERROR: `update` settings must be a mapping in {settings_path}")
            raise typer.Exit(code=1)
        update_settings["default_mode"] = m.value
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(settings_path, data)
        print(f"Default update mode set to `{m.value}` in {settings_path}")
        return

    # Resolve update mode
    if force_sync:
        update_mode = UpdateMode.FORCE_SYNC
    elif mode is not None:
        update_mode = UpdateMode(str(mode))
    else:
        settings_path = _project_settings_path(repo_root)
        if settings_path.exists():
            data = load_yaml(settings_path)
            configured = (data.get("update") or {}).get("default_mode")
            if configured:
                try:
                    update_mode = UpdateMode(str(configured).strip())
                except ValueError:
                    print(
                        f"ERROR: invalid default update mode `{configured}` in {settings_path}; "
                        f"expected `pull` or `force-sync`"
                    )
                    raise typer.Exit(code=1)
            else:
                update_mode = UpdateMode.PULL
        else:
            update_mode = UpdateMode.PULL

    if update_mode is UpdateMode.FORCE_SYNC:
        for command_parts in (["git", "fetch", "--prune"], ["git", "reset", "--hard", "@{u}"]):
            sync_result = subprocess.run(command_parts, cwd=repo_root).returncode
            if sync_result != 0:
                print(f"ERROR: force sync failed at `{' '.join(command_parts)}`; refusing to continue with tool upgrade.")
                raise typer.Exit(code=1)
        print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    elif update_mode is UpdateMode.PULL:
        git_pull_result = subprocess.run(["git", "pull"], cwd=repo_root).returncode
        if git_pull_result != 0:
            print("ERROR: git pull failed; refusing to continue with tool upgrade.")
            raise typer.Exit(code=1)

    upgrade_result = subprocess.run(["uv", "tool", "upgrade", "openharness"], cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade openharness` failed.")
        raise typer.Exit(code=1)
    print(f"Updated OpenHarness from {repo_root}")
