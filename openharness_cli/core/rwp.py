
from pathlib import Path
from typing import Any

import yaml

from ..harness_context import harness, HarnessContext
from ..models import RuntimeWorkflowPackage


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
    workflows_root = ctx.config.rwp_workflows_root
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


_WORKFLOW_TEMPLATE = """\
---
name: {name}
description: {description}
---

# Runtime Workflow Package

## Purpose
说明这个 RWP 验证什么真实运行时行为。一两句话说清楚：验证什么系统/服务/流程的什么行为。

## When To Use
说明什么类型的任务应考虑使用这个 workflow。

## Prerequisites
列出运行脚本需要的所有前置条件：
- 环境变量
- 账号/权限
- 服务状态
- 测试数据

## Scripts
说明 `scripts/` 下每个脚本的作用和用法。

## Runtime Observation
说明运行后应观察什么来判定结果：
- 日志输出
- API 响应
- 数据库/外部系统状态变化
- trace、截图等外部证据

## Success Criteria
说明什么条件成立时判定通过。用可验证的事实表述。

## Failure Evidence
说明失败时必须保存什么证据以便排查。
产物写入 `.harness/rwp/logs/` 目录。

## Limitations
说明这个 workflow 不覆盖什么。

## Writeback Guidance
- `detailed-design.md`: 写入被选中的 workflow、脚本、前置条件、预期观察和降级路径。
- `plan.md`: 写入计划执行命令、预期结果、运行时观察方式和阻塞回退。
- `evidence.md`: 写入产物路径、外部记录、人工步骤、残余风险和后续事项。
"""


def _validate_workflow_name(name: str) -> str:
    name = str(name).strip()
    if not name:
        raise ValueError("workflow name is required")
    if "/" in name or "\\" in name:
        raise ValueError("workflow name must not contain path separators")
    return name


@harness
def create_runtime_workflow_package(
    ctx: HarnessContext, name: str, description: str
) -> RuntimeWorkflowPackage:
    name = _validate_workflow_name(name)
    description = str(description).strip()
    if not description:
        raise ValueError("workflow description is required")
    workflows_root = ctx.config.rwp_workflows_root
    package_root = workflows_root / name
    if package_root.exists():
        raise ValueError(f"workflow already exists: {name}")
    scripts_dir = package_root / "scripts"
    scripts_dir.mkdir(parents=True)
    workflow_path = package_root / "workflow.md"
    workflow_path.write_text(
        _WORKFLOW_TEMPLATE.format(name=name, description=description),
        encoding="utf-8",
    )
    return RuntimeWorkflowPackage(
        root=package_root,
        workflow_path=workflow_path,
        name=name,
        description=description,
    )


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
