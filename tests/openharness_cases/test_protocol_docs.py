from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from .common import REPO_ROOT, SKILL_ROOT, openharness


LIVE_REPO_SKILLS = [
    "using-openharness",
]

STATE_SKILLS = [
    "brainstorming",
    "detailed-design",
    "exploring-solution-space",
    "finishing-a-development-branch",
    "implementing",
    "verification-designing",
    "verifying",
]

IMPLICIT_SKILLS = {
    "using-openharness",
}

EXPLICIT_ONLY_SKILLS: set[str] = set()

STATE_SKILLS_IMPLICIT: set[str] = set()

STATE_SKILLS_EXPLICIT = {
    "brainstorming",
    "detailed-design",
    "exploring-solution-space",
    "finishing-a-development-branch",
    "implementing",
    "verification-designing",
    "verifying",
}

STATES_BASE = "skills/using-openharness/states"


def _load_skill_metadata(skill_name: str, base: str = "skills") -> dict:
    metadata_path = REPO_ROOT / base / skill_name / "agents" / "openai.yaml"
    data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_openharness_repo_self_tests_live_under_top_level_tests() -> None:
    assert (REPO_ROOT / "tests" / "test_openharness.py").exists()
    assert (REPO_ROOT / "tests" / "openharness_cases" / "test_cli_workflows.py").exists()
    assert not (REPO_ROOT / "skills" / "using-openharness" / "tests" / "test_openharness.py").exists()


def test_openharness_legacy_script_entrypoint_is_removed() -> None:
    assert not (REPO_ROOT / "skills" / "using-openharness" / "scripts" / "openharness.py").exists()


def _all_skill_triples():
    """Return (skill_name, base_path, expected_implicit) for every live skill."""
    triples: list[tuple[str, str, bool]] = []
    for name in LIVE_REPO_SKILLS:
        triples.append((name, "skills", name in IMPLICIT_SKILLS))
    for name in STATE_SKILLS:
        triples.append((name, STATES_BASE, name in STATE_SKILLS_IMPLICIT))
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

    for skill_name in STATE_SKILLS_IMPLICIT:
        metadata = _load_skill_metadata(skill_name, STATES_BASE)
        assert metadata["policy"]["allow_implicit_invocation"] is True

    for skill_name in EXPLICIT_ONLY_SKILLS:
        metadata = _load_skill_metadata(skill_name)
        assert metadata["policy"]["allow_implicit_invocation"] is False

    for skill_name in STATE_SKILLS_EXPLICIT:
        metadata = _load_skill_metadata(skill_name, STATES_BASE)
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
    parser = openharness.build_parser()
    choices = parser._subparsers._group_actions[0].choices  # type: ignore[attr-defined]
    assert set(choices) == {
        "bootstrap",
        "check-tasks",
        "writing-guide",
        "init",
        "new-task",
        "rwp",
        "task-package",
        "transition",
        "update",
    }


@pytest.mark.skip(reason="openharness in tests = openharness_cli.main; public symbols like discover_task_packages live in openharness_cli, not main")
def test_openharness_script_uses_task_package_naming_in_public_symbols() -> None:
    assert hasattr(openharness, "TaskPackage")
    assert hasattr(openharness, "TaskScaffoldRequest")
    assert hasattr(openharness, "discover_task_packages")
    assert hasattr(openharness, "validate_task_package")
    assert hasattr(openharness, "create_task_package")
    assert hasattr(openharness, "summarize_task_package")
    assert hasattr(openharness, "slugify_task_name")
    assert hasattr(openharness, "cmd_check_tasks")
    assert hasattr(openharness, "cmd_init")
    assert hasattr(openharness, "cmd_new_task")
    assert not hasattr(openharness, "DesignPackage")
    assert not hasattr(openharness, "DesignScaffoldRequest")
    assert not hasattr(openharness, "discover_design_packages")
    assert not hasattr(openharness, "validate_design_package")
    assert not hasattr(openharness, "create_design_package")
    assert not hasattr(openharness, "summarize_design_package")
    assert not hasattr(openharness, "slugify_design_name")
    assert not hasattr(openharness, "cmd_check_designs")
    assert not hasattr(openharness, "cmd_new_design")


def test_task_package_commands_use_current_handlers_only() -> None:
    from openharness_cli import commands as cmd
    parser = openharness.build_parser()
    assert parser.parse_args(["check-tasks"]).handler == cmd.cmd_check_tasks
    assert parser.parse_args(["init"]).handler == cmd.cmd_init
    assert (
        parser.parse_args(["new-task", "name", "--task-id", "OH-999", "--title", "Title"]).handler
        == cmd.cmd_task_package_new
    )
    assert parser.parse_args(["rwp", "list"]).handler == cmd.cmd_rwp
    assert parser.parse_args(["transition", "name", "requirements_designed"]).handler == cmd.cmd_transition
    assert parser.parse_args(["update"]).handler == cmd.cmd_update


def test_new_task_rejects_legacy_positional_task_id_and_title() -> None:
    parser = openharness.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["new-task", "name", "OH-999", "Title"])








@pytest.mark.skip(reason="subagent-driven-development and requesting-code-review moved to tmp/ backup")
def test_optional_execution_skills_are_not_described_as_core_protocol() -> None:
    for path in [
        REPO_ROOT / "tmp" / "skills-backup" / "subagent-driven-development" / "SKILL.md",
        REPO_ROOT / "tmp" / "skills-backup" / "requesting-code-review" / "SKILL.md",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "04-implementation-plan.md" not in text






def test_readme_describes_plug_and_play_harness_and_python_pytest_floor() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "plug-and-play" in readme
    assert "Python-first" in readme
    assert "`uv run pytest` is the default automated verification floor for testable code behavior" in readme
    assert "not the only valid evidence path" in readme
    assert "object-appropriate verification" in readme


@pytest.mark.skip(reason="reference docs reorganized")
def test_runtime_reference_docs_use_existing_sibling_paths() -> None:
    expected_paths = {
        REPO_ROOT / "skills" / "using-openharness" / "references" / "runtime-capability-contract.md": [
            "runtime-workflow-packages.md",
        ],
        REPO_ROOT / "skills" / "using-openharness" / "references" / "state-routing-table.md": [
            "cli-reference.md",
        ],
    }

    for doc_path, relative_targets in expected_paths.items():
        text = doc_path.read_text(encoding="utf-8")
        for relative_target in relative_targets:
            assert f"`{relative_target}`" in text, f"{doc_path} must reference {relative_target}"
            resolved_path = doc_path.parent / Path(relative_target)
            assert resolved_path.exists(), f"{doc_path} points to missing sibling file {resolved_path}"


@pytest.mark.skip(reason="systematic-debugging moved to tmp/ backup")
def test_systematic_debugging_docs_do_not_advertise_retired_path() -> None:
    retired_path = "skills/debugging/systematic-debugging"
    allowed_path = "skills/systematic-debugging"
    doc_paths = [
        REPO_ROOT / "tmp" / "skills-backup" / "systematic-debugging" / "test-academic.md",
        REPO_ROOT / "tmp" / "skills-backup" / "systematic-debugging" / "test-pressure-1.md",
        REPO_ROOT / "tmp" / "skills-backup" / "systematic-debugging" / "test-pressure-2.md",
        REPO_ROOT / "tmp" / "skills-backup" / "systematic-debugging" / "test-pressure-3.md",
        REPO_ROOT / "tmp" / "skills-backup" / "systematic-debugging" / "CREATION-LOG.md",
    ]

    for doc_path in doc_paths:
        text = doc_path.read_text(encoding="utf-8")
        assert retired_path not in text, f"{doc_path} still references retired skill path"
        assert allowed_path in text, f"{doc_path} should reference the live skill path"


def test_readme_describes_runtime_capability_contract() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Runtime Workflow Package" in readme
    assert "openharness rwp list" in readme
    assert ".harness/rwp/workflows" in readme
    assert "03-detailed-design.md" in readme


def test_agents_md_routes_repo_skill_usage_through_openharness() -> None:
    agents_path = REPO_ROOT / "AGENTS.md"
    text = agents_path.read_text(encoding="utf-8")
    assert "仓库地图" in text
    assert "using-openharness" in text


def test_install_doc_describes_global_openharness_command_install_and_upgrade() -> None:
    text = (REPO_ROOT / "INSTALL.codex.md").read_text(encoding="utf-8")
    assert "uv tool install --editable" in text
    assert "openharness task-package list" in text
    assert "已安装" in text or "existing" in text


def test_install_doc_mentions_openharness_update() -> None:
    text = (REPO_ROOT / "INSTALL.codex.md").read_text(encoding="utf-8")
    assert "openharness update" in text










@pytest.mark.skip(reason="state-routing-table.md moved to tmp; routing now inline in SKILL.md + CLI hooks")
def test_state_routing_table_includes_all_workflow_stages() -> None:
    text = (REPO_ROOT / "tmp" / "skills-backup" / "references" / "state-routing-table.md").read_text(
        encoding="utf-8"
    )
    assert "## 标准流程" in text
    assert "## 机械流程" in text
    assert "## 实现阶段说明" in text
    assert "## 回退与异常" in text
    assert "`proposing`" in text
    assert "`archived`" in text
    assert "`verification_designing`" in text
    assert "`verified`" in text










def test_design_package_templates_include_verification_path_sections() -> None:
    overview = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.02-overview-design.md"
    ).read_text(encoding="utf-8")
    detailed = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.03-detailed-design.md"
    ).read_text(encoding="utf-8")
    verification = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.verification_design.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.evidence.md"
    ).read_text(encoding="utf-8")

    assert "## Overview Reflection" in overview
    assert "模块" in overview
    assert "接口" in overview
    assert "数据" in overview
    assert "PlantUML" in overview
    assert "## Runtime Verification Plan" in detailed
    assert "Verification Path" in detailed
    assert "Fallback Path" in detailed
    assert "## Detailed Reflection" in detailed
    assert "模块内部" in detailed
    assert "数据语义" in detailed
    assert "异常" in detailed
    assert "PlantUML" in detailed
    assert "## Stage Gates" in overview
    assert "## Stage Gates" in detailed
    assert "## Decision Closure" in detailed
    assert "## Traceability" in verification
    assert "## Risk Acceptance" in verification
    assert "## Verification Path" in verification
    assert "Executed Path" in verification
    assert "## Verification Result" in evidence
    assert "## Residual Risks" in evidence



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
    assert "03-detailed-design.md" in text
    assert "verification_design.md" in text
    assert "evidence.md" in text
    assert "## Routing Contract" in text
    assert "openharness rwp list" in text
    assert "openharness rwp show" in text
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
    assert "openharness rwp show" in text
    assert "openharness rwp run" in text
    assert "03-detailed-design.md" in text
    assert "verification_design.md" in text
    assert "evidence.md" in text


@pytest.mark.skip(reason="writing guidance refactored to templates only")
def test_task_package_writing_guidance_references_define_stage_contracts() -> None:
    expected: dict[str, tuple[str, str]] = {
        "requirements-writing-guidance.md": (
            "skills/brainstorming/references", "01-requirements.md"
        ),
        "overview-design-writing-guidance.md": (
            "skills/exploring-solution-space/references", "02-overview-design.md"
        ),
        "detailed-design-writing-guidance.md": (
            "skills/exploring-solution-space/references", "03-detailed-design.md"
        ),
        "verification-writing-guidance.md": (
            "skills/verification-before-completion/references", "verification_design.md"
        ),
        "evidence-writing-guidance.md": (
            "skills/verification-before-completion/references", "evidence.md"
        ),
    }

    old_root = REPO_ROOT / "skills" / "using-openharness" / "references"
    assert not (old_root / "task-package-writing-guide.md").exists()
    # Old locations should be cleaned up
    for filename in expected:
        assert not (old_root / filename).exists(), f"{filename} should have moved from using-openharness"

    for filename, (rel_dir, target_doc) in expected.items():
        path = REPO_ROOT / rel_dir / filename
        text = path.read_text(encoding="utf-8")
        assert target_doc in text
        assert "Questions This Document Must Answer" in text
        assert "Section Mapping" in text
        assert "Boundary With Adjacent Documents" in text
        assert "Common Failure Modes" in text
        assert "Minimum Acceptable Shape" in text
        assert "Exit Check" in text

    requirements = (REPO_ROOT / "skills/brainstorming/references/requirements-writing-guidance.md").read_text(encoding="utf-8")
    assert "acceptance criteria" in requirements
    assert "cost cap" in requirements
    assert "counterexample" in requirements

    overview = (REPO_ROOT / "skills/exploring-solution-space/references/overview-design-writing-guidance.md").read_text(encoding="utf-8")
    assert "key failure modes" in overview
    assert "challenge closure" in overview
    assert "Stage Gates" in overview
    assert "模块" in overview
    assert "接口" in overview
    assert "数据" in overview
    assert "PlantUML" in overview

    detailed = (REPO_ROOT / "skills/exploring-solution-space/references/detailed-design-writing-guidance.md").read_text(encoding="utf-8")
    assert "observability" in detailed
    assert "testing-first" in detailed
    assert "Runtime Verification Plan" in detailed
    assert "模块内部" in detailed
    assert "数据语义" in detailed
    assert "异常" in detailed
    assert "PlantUML" in detailed

    verification = (REPO_ROOT / "skills/verification-before-completion/references/verification-writing-guidance.md").read_text(encoding="utf-8")
    assert "fresh" in verification
    assert "Required Commands" in verification
    assert "Expected Outcomes" in verification
    assert "Latest Result" in verification

    evidence = (REPO_ROOT / "skills/verification-before-completion/references/evidence-writing-guidance.md").read_text(encoding="utf-8")
    assert "final verification command" in evidence
    assert "Artifact Paths" in evidence
    assert "Manual Steps" in evidence




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
    assert "03-detailed-design.md" in text
    assert "verification_design.md" in text
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


def test_task_package_templates_default_to_chinese_narrative_with_english_anchors() -> None:
    requirements = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.01-requirements.md"
    ).read_text(encoding="utf-8")
    overview = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.02-overview-design.md"
    ).read_text(encoding="utf-8")
    detailed = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.03-detailed-design.md"
    ).read_text(encoding="utf-8")
    verification = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.verification_design.md"
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
        assert "章节标题保留英文" in text
        assert "YAML 键名" in text

    assert "## Goal" in requirements
    assert "## Proposed Structure" in overview
    assert "## Runtime Verification Plan" in detailed
    assert "## Verification Path" in verification
    assert "## Residual Risks" in evidence






@pytest.mark.skip(reason="skills rewritten in Chinese — old English status references removed")
def test_workflow_skills_include_status_guidance() -> None:
    openharness_text = (REPO_ROOT / "skills" / "using-openharness" / "SKILL.md").read_text(encoding="utf-8")
    exploration_text = (REPO_ROOT / "skills" / "exploring-solution-space" / "SKILL.md").read_text(encoding="utf-8")

    assert "`overview_ready`" in exploration_text
    assert "`detailed_ready`" in exploration_text
    assert "`in_progress`" in openharness_text
    assert "`verifying`" in openharness_text
    assert "`archived`" in openharness_text
