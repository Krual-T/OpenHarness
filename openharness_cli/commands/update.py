from __future__ import annotations

import argparse
import subprocess
from enum import StrEnum
from pathlib import Path

from ..repository import load_yaml, write_yaml


class UpdateMode(StrEnum):
    PULL = "pull"
    FORCE_SYNC = "force-sync"


def _project_settings_path(repo_root: Path) -> Path:
    return (repo_root / ".harness" / "settings.yaml").resolve()


def cmd_update(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[1]

    default_mode = getattr(args, "set_default_mode", None)
    if default_mode:
        mode = UpdateMode(str(default_mode))
        settings_path = _project_settings_path(repo_root)
        data = load_yaml(settings_path) if settings_path.exists() else {}
        update_settings = data.setdefault("update", {})
        if not isinstance(update_settings, dict):
            print(f"ERROR: `update` settings must be a mapping in {settings_path}")
            return 1
        update_settings["default_mode"] = mode.value
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(settings_path, data)
        print(f"Default update mode set to `{mode.value}` in {settings_path}")
        return 0

    # Resolve update mode
    if getattr(args, "force_sync", False):
        update_mode = UpdateMode.FORCE_SYNC
    elif getattr(args, "mode", None):
        update_mode = UpdateMode(str(args.mode))
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
                    return 1
            else:
                update_mode = UpdateMode.PULL
        else:
            update_mode = UpdateMode.PULL

    if update_mode is UpdateMode.FORCE_SYNC:
        for command_parts in (["git", "fetch", "--prune"], ["git", "reset", "--hard", "@{u}"]):
            sync_result = subprocess.run(command_parts, cwd=repo_root).returncode
            if sync_result != 0:
                print(f"ERROR: force sync failed at `{' '.join(command_parts)}`; refusing to continue with tool upgrade.")
                return 1
        print(f"Force-synchronized OpenHarness source clone from {repo_root}")
    elif update_mode is UpdateMode.PULL:
        git_pull_result = subprocess.run(["git", "pull"], cwd=repo_root).returncode
        if git_pull_result != 0:
            print("ERROR: git pull failed; refusing to continue with tool upgrade.")
            return 1

    upgrade_result = subprocess.run(["uv", "tool", "upgrade", "openharness"], cwd=repo_root).returncode
    if upgrade_result != 0:
        print("ERROR: `uv tool upgrade openharness` failed.")
        return 1
    print(f"Updated OpenHarness from {repo_root}")
    return 0
