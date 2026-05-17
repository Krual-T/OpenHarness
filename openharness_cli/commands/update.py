from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from ..repository import _load_yaml, _write_yaml

UPDATE_MODES = {"pull", "force-sync"}


def _openharness_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _project_settings_path(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "settings.yaml").resolve()


def _load_project_settings(repo_root: Path) -> dict[str, object]:
    path = _project_settings_path(repo_root)
    if not path.exists():
        return {}
    return _load_yaml(path)


def _save_project_settings(repo_root: Path, settings: dict[str, object]) -> None:
    path = _project_settings_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_yaml(path, settings)


def _set_default_update_mode(repo_root: Path, mode: str) -> None:
    settings = _load_project_settings(repo_root)
    update_settings = settings.setdefault("update", {})
    if not isinstance(update_settings, dict):
        raise ValueError(f"`update` settings must be a mapping in {_project_settings_path(repo_root)}")
    update_settings["default_mode"] = mode
    _save_project_settings(repo_root, settings)


def _configured_update_mode(repo_root: Path) -> str:
    settings = _load_project_settings(repo_root)
    update_settings = settings.get("update") or {}
    if not isinstance(update_settings, dict):
        raise ValueError(f"`update` settings must be a mapping in {_project_settings_path(repo_root)}")
    mode = str(update_settings.get("default_mode") or "").strip()
    if not mode:
        return "pull"
    if mode not in UPDATE_MODES:
        raise ValueError(
            f"invalid default update mode `{mode}` in {_project_settings_path(repo_root)}; "
            f"expected `pull` or `force-sync`"
        )
    return mode


def _resolve_update_mode(args: argparse.Namespace, repo_root: Path) -> str:
    if getattr(args, "force_sync", False):
        return "force-sync"
    mode = getattr(args, "mode", None)
    if mode:
        return str(mode)
    return _configured_update_mode(repo_root)


def cmd_update(args: argparse.Namespace) -> int:
    repo_root = _openharness_repo_root()
    default_mode = getattr(args, "set_default_mode", None)
    if default_mode:
        mode = str(default_mode)
        if mode not in UPDATE_MODES:
            print(f"ERROR: invalid mode `{mode}`; expected `pull` or `force-sync`.")
            return 1
        try:
            _set_default_update_mode(repo_root, mode)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Default update mode set to `{mode}` in {_project_settings_path(repo_root)}")
        return 0

    try:
        update_mode = _resolve_update_mode(args, repo_root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if update_mode == "force-sync":
        for command_parts in (["git", "fetch", "--prune"], ["git", "reset", "--hard", "@{u}"]):
            sync_result = subprocess.run(command_parts, cwd=repo_root).returncode
            if sync_result != 0:
                print(f"ERROR: force sync failed at `{' '.join(command_parts)}`; refusing to continue with tool upgrade.")
                return 1
        print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    elif update_mode == "pull":
        git_pull_result = subprocess.run(["git", "pull"], cwd=repo_root).returncode
        if git_pull_result != 0:
            print("ERROR: git pull failed; refusing to continue with tool upgrade.")
            return 1
    else:
        print(f"ERROR: invalid update mode `{update_mode}`; expected `pull` or `force-sync`.")
        return 1

    upgrade_result = subprocess.run(["uv", "tool", "upgrade", "openharness"], cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade openharness` failed.")
        return 1
    print(f"Updated OpenHarness from {repo_root}")
    return 0
