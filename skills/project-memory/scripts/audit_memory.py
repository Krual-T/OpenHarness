#!/usr/bin/env python3
"""Audit repo-local memory objects for stale data, schema issues, and collisions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from project_memory_lib import audit_memory_objects, find_repo_root, parse_memory_kinds


SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit project-memory objects for common failure modes.")
    parser.add_argument("--repo-root", type=Path, default=None, help="Override repo root")
    parser.add_argument("--kind", action="append", default=[], help="Only audit one or more kinds")
    parser.add_argument(
        "--fail-on",
        choices=("none", "low", "medium", "high"),
        default="none",
        help="Exit non-zero when findings at or above this severity exist",
    )
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    kinds = parse_memory_kinds(args.kind)
    findings = audit_memory_objects(repo_root, kinds=kinds)
    if args.as_json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("No audit findings.")
        for finding in findings:
            details = ", ".join(finding.get("details") or []) or "-"
            print(
                f"[{finding['severity']}] [{finding['kind']}] {finding['id']} issue={finding['issue']}"
            )
            print(f"  details: {details}")

    if args.fail_on != "none":
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[item["severity"]] >= threshold for item in findings):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
