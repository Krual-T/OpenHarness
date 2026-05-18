
import json
import importlib.metadata
import subprocess
from enum import StrEnum
from pathlib import Path
from urllib.parse import unquote, urlparse

import typer

from ..core import load_yaml, write_yaml


class UpdateMode(StrEnum):
    PULL = "pull"
    FORCE_SYNC = "force-sync"


def _project_settings_path(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "settings.yaml").resolve()


def _openharness_source_root() -> Path:
    direct_url = _source_root_from_installed_metadata()
    if direct_url is not None:
        return direct_url

    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        if (parent / ".git").exists() and (parent / "pyproject.toml").exists():
            return parent

    return module_path.parents[2]


def _source_root_from_installed_metadata() -> Path | None:
    try:
        distribution = importlib.metadata.distribution("openharness")
    except importlib.metadata.PackageNotFoundError:
        return None

    direct_url_text = distribution.read_text("direct_url.json")
    if not direct_url_text:
        return None

    try:
        direct_url = json.loads(direct_url_text)
    except json.JSONDecodeError:
        return None

    url = direct_url.get("url")
    if not isinstance(url, str):
        return None

    parsed = urlparse(url)
    if parsed.scheme != "file":
        return None

    return Path(unquote(parsed.path)).resolve()


def update(
    force_sync: bool = typer.Option(False, "--force-sync", help="Discard local changes and reset to upstream branch"),
    mode: str | None = typer.Option(None, "--mode", help="Override saved default update mode (pull / force-sync)"),
    set_default_mode: str | None = typer.Option(None, "--set-default-mode", help="Save default update mode and exit (pull / force-sync)"),
) -> None:
    """Update the OpenHarness clone and refresh the installed CLI tool."""
    repo_root = _openharness_source_root()

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

    upgrade_result = subprocess.run(["uv", "tool", "upgrade", "--reinstall", "openharness"], cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade --reinstall openharness` failed.")
        raise typer.Exit(code=1)
    print(f"Updated OpenHarness from {repo_root}")
