#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re

import yaml

ACTIVE_STATUSES = {"proposed", "requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying"}
VERIFYABLE_STATUSES = {"requirements_ready", "overview_ready", "detailed_ready", "in_progress", "verifying"}
REQUIRED_DESIGN_FILES = (
    "README.md",
    "STATUS.yaml",
    "01-requirements.md",
    "02-overview-design.md",
    "03-detailed-design.md",
    "05-verification.md",
    "06-evidence.md",
)
REQUIRED_STATUS_KEYS = (
    "id",
    "title",
    "status",
    "summary",
    "owner",
    "created_at",
    "updated_at",
    "done_criteria",
    "verification",
)


@dataclass(slots=True, frozen=True)
class HarnessManifest:
    repo_root: Path
    path: Path
    raw: dict[str, Any]

    @property
    def designs_root(self) -> Path:
        raw_root = str(self.raw.get("designs_root") or "designs").strip() or "designs"
        return (self.repo_root / raw_root).resolve()

    @property
    def archived_designs_root(self) -> Path:
        raw_root = str(self.raw.get("archived_designs_root") or "docs/archived/designs").strip() or "docs/archived/designs"
        return (self.repo_root / raw_root).resolve()

    @property
    def required_design_files(self) -> tuple[str, ...]:
        raw = self.raw.get("required_design_files")
        if not isinstance(raw, list) or not raw:
            return REQUIRED_DESIGN_FILES
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def allowed_statuses(self) -> tuple[str, ...]:
        workflow = self.raw.get("workflow")
        if not isinstance(workflow, dict):
            return ()
        raw = workflow.get("default_status_flow")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())


@dataclass(slots=True, frozen=True)
class DesignPackage:
    root: Path
    status: dict[str, Any]
    manifest: HarnessManifest
    documents: dict[str, Path] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def status_name(self) -> str:
        return str(self.status.get("status") or "").strip()

    @property
    def design_id(self) -> str:
        return str(self.status.get("id") or self.root.name).strip()

    @property
    def title(self) -> str:
        return str(self.status.get("title") or self.root.name).strip()

    @property
    def summary(self) -> str:
        return str(self.status.get("summary") or "").strip()

    @property
    def owner(self) -> str:
        return str(self.status.get("owner") or "").strip()

    @property
    def done_criteria(self) -> tuple[str, ...]:
        raw = self.status.get("done_criteria")
        if not isinstance(raw, list):
            return ()
        return tuple(str(item).strip() for item in raw if str(item).strip())

    @property
    def required_commands(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        commands = verification.get("required_commands")
        if not isinstance(commands, list):
            return ()
        return tuple(str(item).strip() for item in commands if str(item).strip())

    @property
    def required_scenarios(self) -> tuple[str, ...]:
        verification = self.status.get("verification")
        if not isinstance(verification, dict):
            return ()
        scenarios = verification.get("required_scenarios")
        if not isinstance(scenarios, list):
            return ()
        return tuple(str(item).strip() for item in scenarios if str(item).strip())


@dataclass(slots=True, frozen=True)
class DesignScaffoldRequest:
    repo_root: Path
    design_name: str
    design_id: str
    title: str
    owner: str = "unassigned"
    summary: str = ""
    status: str = "proposed"


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML object at {path} must be a mapping")
    return data


def load_manifest(repo_root: Path) -> HarnessManifest:
    skill_root = Path(__file__).resolve().parents[1]
    candidates = (
        repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml",
        repo_root / "skills" / "using-openharness" / "manifest.yaml",
        repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "references" / "manifest.yaml",
        repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "manifest.yaml",
        repo_root / ".harness" / "manifest.yaml",
        skill_root / "references" / "manifest.yaml",
        skill_root / "manifest.yaml",
    )
    for candidate in candidates:
        manifest_path = candidate.resolve()
        if manifest_path.exists():
            return HarnessManifest(repo_root=repo_root, path=manifest_path, raw=_load_yaml(manifest_path))
    raise FileNotFoundError(
        "Harness manifest not found. Checked: "
        + ", ".join(str(candidate) for candidate in candidates)
    )


def discover_design_packages(repo_root: Path, manifest: HarnessManifest | None = None) -> list[DesignPackage]:
    current_manifest = manifest or load_manifest(repo_root)
    packages: list[DesignPackage] = []
    roots = [current_manifest.designs_root]
    if current_manifest.archived_designs_root != current_manifest.designs_root:
        roots.append(current_manifest.archived_designs_root)
    seen: set[Path] = set()
    for designs_root in roots:
        if not designs_root.exists():
            continue
        for child in sorted(path for path in designs_root.iterdir() if path.is_dir()):
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            status_path = child / "STATUS.yaml"
            if not status_path.exists():
                continue
            status = _load_yaml(status_path)
            documents = {name: child / name for name in current_manifest.required_design_files}
            packages.append(DesignPackage(root=child, status=status, manifest=current_manifest, documents=documents))
    return packages


def validate_design_package(package: DesignPackage) -> list[str]:
    errors: list[str] = []
    for file_name in package.manifest.required_design_files:
        if not (package.root / file_name).exists():
            errors.append(f"missing required file: {package.root / file_name}")
    for key in REQUIRED_STATUS_KEYS:
        value = package.status.get(key)
        if value in (None, "", []):
            errors.append(f"missing status key `{key}` in {package.root / 'STATUS.yaml'}")
    verification = package.status.get("verification")
    if verification is not None and not isinstance(verification, dict):
        errors.append(f"`verification` must be a mapping in {package.root / 'STATUS.yaml'}")
    evidence = package.status.get("evidence")
    if evidence is not None and not isinstance(evidence, dict):
        errors.append(f"`evidence` must be a mapping in {package.root / 'STATUS.yaml'}")
    allowed_statuses = package.manifest.allowed_statuses
    if allowed_statuses and package.status_name not in allowed_statuses:
        errors.append(
            f"unknown status `{package.status_name}` in {package.root / 'STATUS.yaml'}; "
            f"expected one of: {', '.join(allowed_statuses)}"
        )
    if package.status_name == "archived":
        if package.root.resolve().parent != package.manifest.archived_designs_root:
            errors.append(
                f"archived package must live under {package.manifest.archived_designs_root}: {package.root}"
            )
    elif package.root.resolve().parent == package.manifest.archived_designs_root:
        errors.append(
            f"non-archived package must not live under {package.manifest.archived_designs_root}: {package.root}"
        )

    repo_root = package.manifest.repo_root
    for key in ("entrypoints",):
        raw_paths = package.status.get(key)
        if isinstance(raw_paths, list):
            for raw_path in raw_paths:
                path = (repo_root / str(raw_path)).resolve()
                if not path.exists():
                    errors.append(f"missing referenced path `{raw_path}` in {package.root / 'STATUS.yaml'}")

    if isinstance(evidence, dict):
        for group in ("docs", "code", "tests"):
            raw_paths = evidence.get(group)
            if isinstance(raw_paths, list):
                for raw_path in raw_paths:
                    path = (repo_root / str(raw_path)).resolve()
                    if not path.exists():
                        errors.append(f"missing referenced path `{raw_path}` in {package.root / 'STATUS.yaml'}")
    return errors


def summarize_design_package(package: DesignPackage) -> str:
    summary = package.summary or "(no summary)"
    return f"{package.design_id} [{package.status_name}] {package.title} - {summary}"


def slugify_design_name(raw_name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", raw_name.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError("design name must contain at least one ASCII letter or number")
    return cleaned


def create_design_package(request: DesignScaffoldRequest) -> Path:
    manifest = load_manifest(request.repo_root)
    design_name = slugify_design_name(request.design_name)
    design_root = manifest.designs_root / design_name
    if design_root.exists():
        raise FileExistsError(f"design package already exists: {design_root}")
    skill_root = Path(__file__).resolve().parents[1]
    template_root = request.repo_root / "skills" / "using-openharness" / "references" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / "skills" / "using-openharness" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "references" / "templates"
    if not template_root.exists():
        template_root = request.repo_root / ".agents" / "skills" / "openharness" / "using-openharness" / "templates"
    if not template_root.exists():
        template_root = skill_root / "references" / "templates"
    if not template_root.exists():
        template_root = skill_root / "templates"
    replacements = {
        "<DESIGN_ID>": request.design_id,
        "<TITLE>": request.title,
        "<DESIGN_NAME>": design_name,
        "<OWNER>": request.owner,
        "<STATUS>": request.status,
        "<SUMMARY>": request.summary or f"Describe the goal of {request.title}.",
        "<DATE>": "YYYY-MM-DD",
    }
    design_root.mkdir(parents=True, exist_ok=False)
    for template in sorted(template_root.glob("design-package.*")):
        target_name = template.name.removeprefix("design-package.")
        content = template.read_text(encoding="utf-8")
        for source, target in replacements.items():
            content = content.replace(source, target)
        (design_root / target_name).write_text(content, encoding="utf-8")
    return design_root


def _run_command(repo_root: Path, command: str) -> int:
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True, cwd=repo_root)
    return completed.returncode


def cmd_bootstrap(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_design_packages(repo_root, manifest)
    if not args.all:
        packages = [package for package in packages if package.status_name in ACTIVE_STATUSES]
    if args.json:
        print(
            json.dumps(
                {
                    "repo": str(repo_root),
                    "manifest": str(manifest.path),
                    "designs_root": str(manifest.designs_root),
                    "archived_designs_root": str(manifest.archived_designs_root),
                    "design_packages": [
                        {
                            "id": package.design_id,
                            "name": package.name,
                            "title": package.title,
                            "status": package.status_name,
                            "summary": package.summary,
                            "owner": package.owner,
                            "root": str(package.root),
                            "required_commands": list(package.required_commands),
                            "required_scenarios": list(package.required_scenarios),
                        }
                        for package in packages
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    print(f"Harness manifest: {manifest.path}")
    print(f"Design root: {manifest.designs_root}")
    if not packages:
        print("No matching design packages found.")
        return 0
    print("Active design packages:" if not args.all else "Design packages:")
    for package in packages:
        print(f"- {summarize_design_package(package)}")
        if package.required_commands:
            print(f"  verify commands: {', '.join(package.required_commands)}")
        if package.required_scenarios:
            print(f"  scenarios: {', '.join(package.required_scenarios)}")
    return 0


def cmd_check_designs(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_design_packages(repo_root, manifest)
    errors: list[str] = []
    if not packages:
        errors.append(
            f"no design packages found under {manifest.designs_root} or {manifest.archived_designs_root}"
        )
    for package in packages:
        errors.extend(validate_design_package(package))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Validated {len(packages)} design package(s) under "
        f"{manifest.designs_root} and {manifest.archived_designs_root}"
    )
    return 0


def cmd_new_design(args: argparse.Namespace) -> int:
    design_root = create_design_package(
        DesignScaffoldRequest(
            repo_root=Path(args.repo).resolve(),
            design_name=args.design_name,
            design_id=args.design_id,
            title=args.title,
            owner=args.owner,
            summary=args.summary,
            status=args.status,
        )
    )
    print(f"Created design package: {design_root}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo).resolve()
    manifest = load_manifest(repo_root)
    packages = discover_design_packages(repo_root, manifest)
    errors: list[str] = []
    if not packages:
        errors.append(
            f"no design packages found under {manifest.designs_root} or {manifest.archived_designs_root}"
        )
    for package in packages:
        errors.extend(validate_design_package(package))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.check_designs_only:
        return 0
    if args.design:
        packages = [package for package in packages if package.name == args.design or package.design_id == args.design]
    else:
        packages = [package for package in packages if package.status_name in VERIFYABLE_STATUSES]
    if not packages:
        print("No matching design packages to verify.")
        return 0
    for package in packages:
        print(f"== Verifying {package.design_id} {package.title} ==")
        for command in package.required_commands:
            if _run_command(repo_root, command) != 0:
                return 1
        if package.required_scenarios:
            print(f"Scenarios declared (manual or future replay integration): {', '.join(package.required_scenarios)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Openharness repository workflow CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Inspect project harness entrypoints and design packages.")
    bootstrap_parser.add_argument("--repo", default=".", help="Repository root")
    bootstrap_parser.add_argument("--json", action="store_true", help="Print JSON output")
    bootstrap_parser.add_argument("--all", action="store_true", help="Include non-active design packages")
    bootstrap_parser.set_defaults(handler=cmd_bootstrap)

    check_parser = subparsers.add_parser("check-designs", help="Validate repository design packages against harness protocol.")
    check_parser.add_argument("--repo", default=".", help="Repository root")
    check_parser.set_defaults(handler=cmd_check_designs)

    new_design_parser = subparsers.add_parser("new-design", help="Create a new design package from harness templates.")
    new_design_parser.add_argument("design_name", help="Directory slug or human-readable design name")
    new_design_parser.add_argument("design_id", help="Stable design id, such as OR-016")
    new_design_parser.add_argument("title", help="Human-readable design title")
    new_design_parser.add_argument("--owner", default="unassigned", help="Initial owner")
    new_design_parser.add_argument("--summary", default="", help="Short summary")
    new_design_parser.add_argument("--status", default="proposed", help="Initial status")
    new_design_parser.add_argument("--repo", default=".", help="Repository root")
    new_design_parser.set_defaults(handler=cmd_new_design)

    verify_parser = subparsers.add_parser("verify", help="Run harness verification for one design package or all active packages.")
    verify_parser.add_argument("design", nargs="?", default="", help="Design package name or design id")
    verify_parser.add_argument("--repo", default=".", help="Repository root")
    verify_parser.add_argument("--check-designs-only", action="store_true", help="Only validate design package protocol")
    verify_parser.set_defaults(handler=cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
