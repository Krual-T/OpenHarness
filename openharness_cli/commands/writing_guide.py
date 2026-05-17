from __future__ import annotations

import argparse
from pathlib import Path


_GUIDANCE_MAP: dict[str, str] = {
    "requirements": "skills/using-openharness/references/templates/task-package.01-requirements.md",
    "overview": "skills/using-openharness/references/templates/task-package.02-overview-design.md",
    "detailed": "skills/using-openharness/references/templates/task-package.03-detailed-design.md",
    "verification": "skills/using-openharness/references/templates/task-package.verification_design.md",
    "evidence": "skills/using-openharness/references/templates/task-package.evidence.md",
    "author-entry": "skills/using-openharness/references/author-entry.md",
}


def _resolve_writing_guide_path(repo_root: Path, name: str) -> Path | None:
    relative = _GUIDANCE_MAP.get(name)
    if not relative:
        return None
    path = (repo_root / relative).resolve()
    return path if path.exists() else None


def cmd_writing_guide(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    command = getattr(args, "writing_guide_command", "list")

    if command == "read":
        path = _resolve_writing_guide_path(repo_root, args.name)
        if path is None:
            print(f"ERROR: unknown or missing writing guide `{args.name}`")
            return 1
        print(path.read_text(encoding="utf-8"), end="")
        return 0

    print("Available writing guides:")
    for name, relative in _GUIDANCE_MAP.items():
        path = repo_root / relative
        exists_icon = "✓" if path.exists() else "✗"
        print(f"  {exists_icon} {name:<15} -> {relative}")
    print(f"\nRead one with: openharness writing-guide read <name>")
    return 0
