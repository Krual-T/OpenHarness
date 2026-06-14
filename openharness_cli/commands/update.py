
import json
import importlib.metadata
import subprocess
from enum import StrEnum
from pathlib import Path
from urllib.parse import unquote, urlparse

import typer

from ..core import load_yaml, write_yaml


class UpdateMode(StrEnum):
    FORCE_SYNC = "force-sync"
    DEV_SOURCE = "dev-source"


SYNC_RETRY_ATTEMPTS = 3
OUTPUT_SNIPPET_LIMIT = 2000


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


def _snippet(value: str | None) -> str:
    if not value:
        return "(empty)"
    stripped = value.strip()
    if len(stripped) <= OUTPUT_SNIPPET_LIMIT:
        return stripped
    return f"{stripped[:OUTPUT_SNIPPET_LIMIT]}... [truncated]"


def _run_sync_command(command_parts: list[str], repo_root: Path) -> bool:
    command_display = " ".join(command_parts)
    for attempt in range(1, SYNC_RETRY_ATTEMPTS + 1):
        result = subprocess.run(
            command_parts,
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True

        print(
            f"Attempt {attempt}/{SYNC_RETRY_ATTEMPTS} failed for `{command_display}` "
            f"in {repo_root} (exit {result.returncode})."
        )
        print(f"stdout: {_snippet(result.stdout)}")
        print(f"stderr: {_snippet(result.stderr)}")
    return False


def _head_commit(repo_root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()

    print(f"ERROR: failed to read git HEAD in {repo_root} (exit {result.returncode}).")
    print(f"stdout: {_snippet(result.stdout)}")
    print(f"stderr: {_snippet(result.stderr)}")
    return None


def _parse_update_mode(value: str) -> UpdateMode:
    try:
        return UpdateMode(str(value).strip())
    except ValueError:
        print(f"ERROR: invalid update mode `{value}`; expected `force-sync` or `dev-source`")
        raise typer.Exit(code=1)


def _force_sync(repo_root: Path) -> bool:
    before_head = _head_commit(repo_root)
    if before_head is None:
        raise typer.Exit(code=1)

    for command_parts in (["git", "fetch", "--prune"], ["git", "reset", "--hard", "@{u}"]):
        if not _run_sync_command(command_parts, repo_root):
            print(
                f"ERROR: force sync failed at `{' '.join(command_parts)}` after "
                f"{SYNC_RETRY_ATTEMPTS} attempts; refusing to continue with tool upgrade."
            )
            raise typer.Exit(code=1)

    after_head = _head_commit(repo_root)
    if after_head is None:
        raise typer.Exit(code=1)

    print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    return before_head != after_head


def update(
    force_sync: bool = typer.Option(False, "--force-sync", help="Discard local changes and reset the managed source clone to upstream"),
    mode: str | None = typer.Option(None, "--mode", help="Override saved default update mode (force-sync / dev-source)"),
    set_default_mode: str | None = typer.Option(None, "--set-default-mode", help="Save default update mode and exit (force-sync / dev-source)"),
) -> None:
    """Update the OpenHarness clone and refresh the installed CLI tool."""
    repo_root = _openharness_source_root()

    if set_default_mode:
        m = _parse_update_mode(set_default_mode)
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

    if force_sync:
        update_mode = UpdateMode.FORCE_SYNC
    elif mode is not None:
        update_mode = _parse_update_mode(mode)
    else:
        settings_path = _project_settings_path(repo_root)
        if settings_path.exists():
            data = load_yaml(settings_path)
            configured = (data.get("update") or {}).get("default_mode")
            if configured:
                update_mode = _parse_update_mode(str(configured))
            else:
                update_mode = UpdateMode.FORCE_SYNC
        else:
            update_mode = UpdateMode.FORCE_SYNC

    source_changed = True
    if update_mode is UpdateMode.FORCE_SYNC:
        source_changed = _force_sync(repo_root)

    if not source_changed:
        print(f"OpenHarness is already at latest code in {repo_root}")
        return

    upgrade_result = subprocess.run(["uv", "tool", "upgrade", "--reinstall", "openharness"], cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade --reinstall openharness` failed.")
        raise typer.Exit(code=1)
    if update_mode is UpdateMode.DEV_SOURCE:
        print(f"Reinstalled OpenHarness from local dev source {repo_root}")
    else:
        print(f"Updated OpenHarness from {repo_root}")
