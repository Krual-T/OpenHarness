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
