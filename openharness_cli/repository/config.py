from __future__ import annotations

from pathlib import Path

from ..models import HarnessConfig


def load_config(repo_root: Path) -> HarnessConfig:
    return HarnessConfig(repo_root=Path(repo_root).resolve())
