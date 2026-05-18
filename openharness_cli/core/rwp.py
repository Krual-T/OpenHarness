
from pathlib import Path
from typing import Any

import yaml

from ..harness_context import harness, HarnessContext
from ..models import RuntimeWorkflowPackage


@harness
def _rwp_root(ctx: HarnessContext) -> Path:
    return (ctx.repo_root / ".harness" / "rwp").resolve()


@harness
def _rwp_workflows_root(ctx: HarnessContext) -> Path:
    return _rwp_root() / "workflows"


def _load_workflow_metadata(workflow_path: Path) -> dict[str, Any]:
    text = workflow_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"workflow metadata header missing in {workflow_path}")
    end_index = text.find("\n---", 4)
    if end_index == -1:
        raise ValueError(f"workflow metadata header not closed in {workflow_path}")
    metadata_text = text[4:end_index]
    try:
        data = yaml.safe_load(metadata_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"failed to parse workflow metadata at {workflow_path}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"workflow metadata at {workflow_path} must be a mapping")
    name = str(data.get("name") or "").strip()
    description = str(data.get("description") or "").strip()
    if not name or not description:
        raise ValueError(f"workflow metadata at {workflow_path} requires `name` and `description`")
    return {"name": name, "description": description}


@harness
def discover_runtime_workflow_packages(ctx: HarnessContext) -> list[RuntimeWorkflowPackage]:
    workflows_root = _rwp_workflows_root()
    if not workflows_root.exists():
        return []
    packages: list[RuntimeWorkflowPackage] = []
    for child in sorted(path for path in workflows_root.iterdir() if path.is_dir()):
        workflow_path = child / "workflow.md"
        if not workflow_path.exists():
            continue
        metadata = _load_workflow_metadata(workflow_path)
        packages.append(
            RuntimeWorkflowPackage(
                root=child, workflow_path=workflow_path,
                name=metadata["name"], description=metadata["description"],
            )
        )
    return packages


@harness
def resolve_runtime_workflow_package(ctx: HarnessContext, workflow: str) -> RuntimeWorkflowPackage:
    matches = [
        p for p in discover_runtime_workflow_packages()
        if p.name == workflow or p.root.name == workflow
    ]
    if not matches:
        raise ValueError(f"runtime workflow package not found: {workflow}")
    if len(matches) > 1:
        roots = ", ".join(str(p.root) for p in matches)
        raise ValueError(f"runtime workflow package `{workflow}` is ambiguous: {roots}")
    return matches[0]


@harness
def resolve_runtime_workflow_script(ctx: HarnessContext, workflow: str, script: str) -> Path:
    script_name = str(script or "").strip()
    if not script_name:
        raise ValueError("rwp run requires an explicit script name")
    if "/" in script_name or "\\" in script_name:
        raise ValueError("rwp script name must refer to a file directly under `scripts/`")
    if not script_name.endswith(".py"):
        raise ValueError("rwp run only supports `.py` scripts")
    package = resolve_runtime_workflow_package(workflow)
    script_path = package.root / "scripts" / script_name
    if not script_path.exists() or not script_path.is_file():
        raise ValueError(f"rwp script not found: {script_name}")
    return script_path
