from __future__ import annotations

from pathlib import Path

from ..models import HarnessConfig


def load_config(repo_root: Path) -> HarnessConfig:
    return HarnessConfig(repo_root=Path(repo_root).resolve())


def _resolve_config(repo_root: Path, config: HarnessConfig | None = None) -> HarnessConfig:
    if isinstance(config, HarnessConfig):
        return config
    return load_config(repo_root)
