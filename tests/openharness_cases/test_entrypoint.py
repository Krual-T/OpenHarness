from __future__ import annotations

import pytest

from pathlib import Path
import tomllib

from .common import openharness


def test_entrypoint_re_exports_package_main_and_parser() -> None:
    package_root = Path(__file__).resolve().parents[2] / "openharness_cli"
    assert package_root.is_dir()
    assert hasattr(openharness, "main")
    assert hasattr(openharness, "app")


def test_pyproject_exposes_openharness_console_script() -> None:
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("openharness") == "openharness_cli.main:main"


def test_parser_help_includes_top_level_description() -> None:
    from typer.testing import CliRunner
    from openharness_cli.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert "Openharness repository workflow CLI." in result.stdout
    assert "update" in result.stdout
    assert "Update" in result.stdout

    result = runner.invoke(app, ["update", "--help"])
    assert "Update the OpenHarness clone and refresh the installed CLI tool." in result.stdout
    assert "--force-sync" in result.stdout
    assert "Discard local changes" in result.stdout
