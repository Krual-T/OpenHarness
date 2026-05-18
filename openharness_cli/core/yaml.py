
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(
            f"failed to parse YAML at {path}. "
            "If a task-info.yaml sentence contains backticks or other YAML-sensitive punctuation, "
            'wrap the whole sentence in double quotes, for example: '
            'summary: "`02-overview-design.md` guidance: fix quoting"'
        ) from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML object at {path} must be a mapping")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
