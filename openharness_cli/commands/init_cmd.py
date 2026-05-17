from __future__ import annotations

import argparse
from pathlib import Path


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    harness_root = repo_root / ".harness"
    harness_root.mkdir(parents=True, exist_ok=True)
    (harness_root / ".gitignore").write_text("*\n", encoding="utf-8")
    print(f"Initialized OpenHarness local directory: {harness_root}")
    return 0
