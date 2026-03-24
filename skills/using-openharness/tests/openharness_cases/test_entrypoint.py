from __future__ import annotations

from pathlib import Path

import openharness


def test_entrypoint_re_exports_package_main_and_parser() -> None:
    package_root = Path(openharness.__file__).resolve().parent / "openharness_cli"
    assert package_root.is_dir()
    assert hasattr(openharness, "main")
    assert hasattr(openharness, "build_parser")
