
from pathlib import Path
import yaml

from .common import REPO_ROOT, SKILL_ROOT, openharness

LIVE_REPO_SKILLS = [
    "using-openharness",
]

IMPLICIT_SKILLS = {
    "using-openharness",
}

EXPLICIT_ONLY_SKILLS: set[str] = set()

def _load_skill_metadata(skill_name: str, base: str = "skills") -> dict:
    metadata_path = REPO_ROOT / base / skill_name / "agents" / "openai.yaml"
    data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data

def test_openharness_repo_self_tests_live_under_top_level_tests() -> None:
    assert (REPO_ROOT / "tests" / "openharness_cases" / "test_cli_workflows.py").exists()
    assert not (REPO_ROOT / "skills" / "using-openharness" / "tests" / "test_openharness.py").exists()

def test_openharness_legacy_script_entrypoint_is_removed() -> None:
    assert not (REPO_ROOT / "skills" / "using-openharness" / "scripts" / "openharness.py").exists()

def _all_skill_triples():
    """Return (skill_name, base_path, expected_implicit) for every live skill.

    State skills no longer ship agents/openai.yaml — that metadata is only
    required for live repo skills.
    """
    triples: list[tuple[str, str, bool]] = []
    for name in LIVE_REPO_SKILLS:
        triples.append((name, "skills", name in IMPLICIT_SKILLS))
    return triples

def test_live_repo_skills_all_ship_openai_metadata() -> None:
    for skill_name, base, _ in _all_skill_triples():
        metadata_path = REPO_ROOT / base / skill_name / "agents" / "openai.yaml"
        assert metadata_path.exists(), f"{skill_name} is missing agents/openai.yaml"

def test_skill_openai_metadata_declares_implicit_invocation_policy() -> None:
    for skill_name, base, _ in _all_skill_triples():
        metadata = _load_skill_metadata(skill_name, base)
        policy = metadata.get("policy")
        assert isinstance(policy, dict), f"{skill_name} metadata must define policy"
        assert isinstance(
            policy.get("allow_implicit_invocation"), bool
        ), f"{skill_name} metadata must define boolean policy.allow_implicit_invocation"

def test_skill_openai_metadata_uses_repo_implicit_invocation_split() -> None:
    for skill_name in IMPLICIT_SKILLS:
        metadata = _load_skill_metadata(skill_name)
        assert metadata["policy"]["allow_implicit_invocation"] is True

    for skill_name in EXPLICIT_ONLY_SKILLS:
        metadata = _load_skill_metadata(skill_name)
        assert metadata["policy"]["allow_implicit_invocation"] is False

def test_skill_openai_metadata_uses_official_tool_dependency_shape() -> None:
    for skill_name, base, _ in _all_skill_triples():
        metadata = _load_skill_metadata(skill_name, base)
        dependencies = metadata.get("dependencies")
        if dependencies is None:
            continue

        assert isinstance(dependencies, dict), f"{skill_name} dependencies must be a mapping"
        tools = dependencies.get("tools")
        assert isinstance(tools, list), f"{skill_name} dependencies.tools must be a list"

        for tool in tools:
            assert isinstance(tool, dict), f"{skill_name} tool dependency must be an object"
            assert tool.get("type") == "mcp", (
                f"{skill_name} only uses officially documented MCP dependencies"
            )
            assert isinstance(tool.get("value"), str) and tool["value"], (
                f"{skill_name} MCP dependency must define non-empty value"
            )

def test_openharness_single_cli_supports_all_subcommands() -> None:
    from typer.testing import CliRunner
    from openharness_cli.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert "init" in result.stdout
    assert "update" in result.stdout
    assert "task-package" in result.stdout
    assert "rwp" in result.stdout
    # Ensure removed commands are not present
    assert "check-tasks" not in result.stdout
    assert "transition" not in result.stdout

def test_cli_commands_resolve() -> None:
    from typer.testing import CliRunner
    from openharness_cli.cli import app

    runner = CliRunner()
    # init
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    # update
    result = runner.invoke(app, ["update", "--help"])
    assert result.exit_code == 0
    # task-package
    result = runner.invoke(app, ["task-package", "--help"])
    assert result.exit_code == 0
    # task-package new
    result = runner.invoke(app, ["task-package", "new", "--help"])
    assert result.exit_code == 0
    assert "--owner" not in result.stdout
    # task-package transition
    result = runner.invoke(app, ["task-package", "transition", "--help"])
    assert result.exit_code == 0
    # rwp
    result = runner.invoke(app, ["rwp", "--help"])
    assert result.exit_code == 0

def test_agents_md_routes_repo_skill_usage_through_openharness() -> None:
    agents_path = REPO_ROOT / "AGENTS.md"
    text = agents_path.read_text(encoding="utf-8")
    assert "仓库地图" in text
    assert "using-openharness" in text

def test_install_doc_describes_global_openharness_command_install_and_upgrade() -> None:
    text = (REPO_ROOT / "INSTALL.md").read_text(encoding="utf-8")
    assert "uv tool install --editable" in text
    assert "openharness task-package list" in text
    assert "已有安装" in text or "existing" in text

def test_install_doc_mentions_openharness_update() -> None:
    text = (REPO_ROOT / "INSTALL.md").read_text(encoding="utf-8")
    assert "openharness update" in text

def test_design_package_templates_include_verification_path_sections() -> None:
    overview = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.overview-design.md"
    ).read_text(encoding="utf-8")
    detailed = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.detailed-design.md"
    ).read_text(encoding="utf-8")
    verification = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.verification-design.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.evidence.md"
    ).read_text(encoding="utf-8")

    assert "## 反思" in overview
    assert "模块" in overview
    assert "接口" in overview
    assert "数据" in overview
    assert "## 可观察性与验证准备" in detailed
    assert "Verification Path" not in detailed
    assert "Fallback Path" not in detailed
    assert "## 反思" in detailed
    assert "模块内部" in detailed
    assert "数据语义" in detailed
    assert "异常" in detailed
    assert "## 阶段门禁" in overview
    assert "## 阶段门禁" in detailed
    assert "## 决策闭合" in detailed
    assert "## 可追溯性" in verification
    assert "## 风险接受" in verification
    assert "## 验证路径" in verification
    assert "## 审核交接包" in verification
    assert "### 审核矩阵" in verification
    assert "Fallback Path" not in verification
    assert "## 验证结果" in evidence
    assert "### 审核交接包摘要" in evidence
    assert "### 发现处理" in evidence
    assert "## 残余风险" in evidence

def test_runtime_capability_reference_defines_declaration_shape_and_writeback() -> None:
    text = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "runtime-capability-contract.md"
    ).read_text(encoding="utf-8")

    assert "## Capability Layers" in text
    assert "core protocol" in text
    assert "Runtime Workflow Package" in text
    assert "## Declaration Shape" in text
    assert ".harness/rwp/workflows" in text
    assert "prerequisites" in text
    assert "scripts/" in text
    assert "runtime observation" in text
    assert "success criteria" in text
    assert "failure evidence" in text
    assert "detailed-design.md" in text
    assert "verification-design.md" in text
    assert "evidence.md" in text
    assert "## Routing Contract" in text
    assert "openharness rwp list" in text
    assert "openharness rwp view" in text
    assert "openharness rwp run" in text
    assert "runtime-workflow-packages.md" in text

def test_runtime_workflow_package_reference_defines_minimum_contents_and_selection_flow() -> None:
    text = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "runtime-workflow-packages.md"
    ).read_text(encoding="utf-8")

    assert "# Runtime Workflow Packages" in text
    assert "## Package Shape" in text
    assert ".harness/rwp/workflows" in text
    assert "workflow.md" in text
    assert "name" in text
    assert "description" in text
    assert "prerequisites" in text
    assert "scripts/" in text
    assert "runtime observation" in text
    assert "success criteria" in text
    assert "failure evidence" in text
    assert "## Selection Flow" in text
    assert "subagent" in text
    assert "openharness rwp list" in text
    assert "openharness rwp view" in text
    assert "openharness rwp run" in text
    assert "detailed-design.md" in text
    assert "verification-design.md" in text
    assert "evidence.md" in text

def test_runtime_workflow_package_template_provides_adoption_shape() -> None:
    text = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "runtime-workflow-package.workflow.md"
    ).read_text(encoding="utf-8")

    assert "name: <RWP_NAME>" in text
    assert "description: <DESCRIPTION>" in text
    assert "# Runtime Workflow Package" in text
    assert "## Scripts" in text
    assert "## Runtime Observation" in text
    assert "## Success Criteria" in text
    assert "## Failure Evidence" in text
    assert "detailed-design.md" in text
    assert "verification-design.md" in text
    assert "evidence.md" in text

def test_runtime_workflow_package_reference_defines_env_and_logger_boundaries() -> None:
    text = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "runtime-workflow-packages.md"
    ).read_text(encoding="utf-8")

    assert ".harness/.env" in text
    assert ".harness/rwp/.env" in text
    assert "from openharness.rwp import get_logger" in text
    assert "libs/" in text
    assert "logs/" in text
    assert "OpenHarness does not define workflow-specific script names" in text

def test_task_package_templates_default_to_chinese_narrative_and_headings() -> None:
    requirements = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.requirements.md"
    ).read_text(encoding="utf-8")
    overview = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.overview-design.md"
    ).read_text(encoding="utf-8")
    detailed = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.detailed-design.md"
    ).read_text(encoding="utf-8")
    verification = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.verification-design.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.evidence.md"
    ).read_text(encoding="utf-8")

    for text in (requirements, overview, detailed, verification, evidence):
        assert "正文默认使用中文" in text
        assert "章节标题使用中文" in text
        assert "YAML 键名" in text

    assert "## 目标" in requirements
    assert "## 推荐结构" in overview
    assert "## 可观察性与验证准备" in detailed
    assert "## 验证路径" in verification
    assert "## 审核交接包" in verification
    assert "### 审核矩阵" in verification
    assert "### 审核交接包摘要" in evidence
    assert "## 残余风险" in evidence
