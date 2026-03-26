from __future__ import annotations

from pathlib import Path
import tomllib

from .common import openharness


def test_entrypoint_re_exports_package_main_and_parser() -> None:
    package_root = Path(__file__).resolve().parents[4] / "openharness_cli"
    assert package_root.is_dir()
    assert hasattr(openharness, "main")
    assert hasattr(openharness, "build_parser")


def test_pyproject_exposes_openharness_console_script() -> None:
    pyproject_path = Path(__file__).resolve().parents[4] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("openharness") == "openharness_cli.main:main"


def test_parser_help_includes_overview_and_update_behavior() -> None:
    parser = openharness.build_parser()
    top_level_help = parser.format_help()
    update_help = parser._subparsers._group_actions[0].choices["update"].format_help()  # type: ignore[attr-defined]
    bootstrap_help = parser._subparsers._group_actions[0].choices["bootstrap"].format_help()  # type: ignore[attr-defined]

    assert "Openharness repository workflow CLI." in top_level_help
    assert "update              Update the OpenHarness clone" in top_level_help
    assert "Update the OpenHarness clone and refresh the installed CLI tool." in update_help
    assert "git pull" in update_help
    assert "uv tool upgrade openharness" in update_help
    assert "Inspect project harness entrypoints and task packages." in bootstrap_help
    assert "Example:" in bootstrap_help
