from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import openharness
from openharness import (
    ACTIVE_STATUSES,
    TaskScaffoldRequest,
    REQUIRED_TASK_PACKAGE_FILES,
    create_task_package,
    discover_task_packages,
    find_duplicate_task_ids,
    load_manifest,
    slugify_task_name,
    summarize_task_package,
    validate_task_package,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_manifest_points_to_task_package_roots() -> None:
    manifest = load_manifest(REPO_ROOT)
    assert manifest.task_packages_root == REPO_ROOT / "docs" / "task-packages"
    assert manifest.archived_task_packages_root == REPO_ROOT / "docs" / "archived" / "task-packages"


def test_self_hosting_design_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "self-hosting-bootstrap")
    assert package.task_id == "OH-001"
    assert package.status_name == "archived"
    assert "Self-Hosting Bootstrap" in summarize_task_package(package)


def test_workflow_redesign_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "workflow-redesign")
    assert package.task_id == "OH-002"
    assert package.status_name == "archived"
    assert "Workflow Redesign" in summarize_task_package(package)


def test_reflective_design_review_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "reflective-design-review")
    assert package.task_id == "OH-003"
    assert package.status_name == "archived"
    assert "Reflective Design Review" in summarize_task_package(package)


def test_active_statuses_do_not_include_archived() -> None:
    assert "in_progress" in ACTIVE_STATUSES
    assert "archived" not in ACTIVE_STATUSES


def test_design_packages_validate_cleanly() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_task_packages(REPO_ROOT, manifest)
    assert find_duplicate_task_ids(packages) == {}
    errors = [error for package in packages for error in validate_task_package(package)]
    assert errors == []


def test_find_duplicate_task_ids_reports_conflicts(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )

    first = repo_root / "docs" / "task-packages" / "one"
    second = repo_root / "docs" / "archived" / "task-packages" / "two"
    for root, status in ((first, "proposed"), (second, "archived")):
        root.mkdir(parents=True)
        for name in REQUIRED_TASK_PACKAGE_FILES:
            (root / name).write_text("# x\n", encoding="utf-8")
        (root / "STATUS.yaml").write_text(
            "id: OH-999\n"
            "title: Duplicate\n"
            f"status: {status}\n"
            "summary: dup\n"
            "owner: codex\n"
            "created_at: 2026-03-23\n"
            "updated_at: 2026-03-23\n"
            "done_criteria:\n"
            "  - x\n"
            "verification:\n"
            "  required_commands:\n"
            "    - uv run pytest\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    manifest = load_manifest(repo_root)
    packages = discover_task_packages(repo_root, manifest)
    duplicates = find_duplicate_task_ids(packages)

    assert set(duplicates) == {"OH-999"}
    assert {package.name for package in duplicates["OH-999"]} == {"one", "two"}


def test_load_manifest_prefers_repo_local_skills_layout(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    assert manifest.path == (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml")


def test_validate_task_package_rejects_unknown_status_and_missing_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "broken").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "broken"
    for name in (
        "README.md",
        "01-requirements.md",
        "02-overview-design.md",
        "03-detailed-design.md",
        "05-verification.md",
        "06-evidence.md",
    ):
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Broken Package\n"
        "status: invalid_status\n"
        "summary: bad\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "entrypoints:\n"
        "  - docs/task-packages/broken/README.md\n"
        "  - docs/task-packages/broken/missing.md\n"
        "verification:\n"
        "  required_commands: []\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/task-packages/broken/06-evidence.md\n"
        "    - docs/task-packages/broken/nope.md\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("unknown status" in error for error in errors)
    assert any("missing referenced path" in error for error in errors)


def test_validate_task_package_rejects_archived_status_in_active_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "wrong-place").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "wrong-place"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Wrong Place\n"
        "status: archived\n"
        "summary: bad\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n",
        encoding="utf-8",
    )
    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)
    assert any("archived package must live under" in error for error in errors)


def test_validate_task_package_rejects_verifying_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "verifying-empty").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "verifying-empty"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-901\n"
        "title: Verifying Empty\n"
        "status: verifying\n"
        "summary: missing verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("verifying status requires at least one verification path" in error for error in errors)


def test_validate_task_package_rejects_archived_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-empty").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "archived" / "task-packages" / "archived-empty"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-902\n"
        "title: Archived Empty\n"
        "status: archived\n"
        "summary: archived without verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("archived status requires at least one verification path" in error for error in errors)


def test_slugify_task_name_normalizes_human_text() -> None:
    assert slugify_task_name("Harness Replay Flow") == "harness-replay-flow"


def test_create_task_package_from_templates(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\ntask_packages_root: docs/task-packages\narchived_task_packages_root: docs/archived/task-packages\nrequired_design_files:\n"
        "  - README.md\n  - STATUS.yaml\n  - 01-requirements.md\n  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n  - 05-verification.md\n  - 06-evidence.md\n",
        encoding="utf-8",
    )
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    for file_name, content in {
        "task-package.README.md": "# <DESIGN_ID> <TITLE>\n",
        "task-package.STATUS.yaml": "id: <DESIGN_ID>\ntitle: <TITLE>\nstatus: <STATUS>\nsummary: <SUMMARY>\nowner: <OWNER>\ncreated_at: <DATE>\nupdated_at: <DATE>\ndone_criteria:\n  - x\nverification:\n  required_commands: []\n",
        "task-package.01-requirements.md": "req\n",
        "task-package.02-overview-design.md": "overview\n",
        "task-package.03-detailed-design.md": "detail\n",
        "task-package.05-verification.md": "verify\n",
        "task-package.06-evidence.md": "evidence\n",
    }.items():
        (template_root / file_name).write_text(content, encoding="utf-8")

    task_root = create_task_package(
        TaskScaffoldRequest(
            repo_root=repo_root,
            task_name="Harness Replay",
            task_id="OH-016",
            title="Harness Replay",
            owner="codex",
            summary="Replay scenarios.",
        )
    )

    assert task_root == repo_root / "docs" / "task-packages" / "harness-replay"
    assert (task_root / "README.md").read_text(encoding="utf-8") == "# OH-016 Harness Replay\n"
    assert not (task_root / "04-implementation-plan.md").exists()
    assert "summary: Replay scenarios." in (task_root / "STATUS.yaml").read_text(encoding="utf-8")


def test_key_repo_skills_are_vendored_locally() -> None:
    expected = [
        "using-openharness",
        "exploring-solution-space",
        "using-git-worktrees",
        "verification-before-completion",
        "systematic-debugging",
        "finishing-a-development-branch",
    ]
    for name in expected:
        path = REPO_ROOT / "skills" / name
        assert path.is_dir()
        assert (path / "SKILL.md").exists()


def test_retired_skills_are_not_shipped_live() -> None:
    for name in ["executing-plans", "writing-plans", "writing-skills"]:
        assert not (REPO_ROOT / "skills" / name).exists()


def test_openharness_skill_owns_supporting_scripts_and_templates() -> None:
    skill_root = REPO_ROOT / "skills" / "using-openharness"
    assert SKILL_ROOT == skill_root
    assert (skill_root / "scripts" / "openharness.py").exists()
    assert (skill_root / "tests" / "test_openharness.py").exists()
    assert (skill_root / "references" / "manifest.yaml").exists()
    assert (skill_root / "references" / "templates" / "task-package.README.md").exists()
    assert (skill_root / "references" / "templates" / "task-package.STATUS.yaml").exists()
    assert not (skill_root / "references" / "templates" / "task-package.04-implementation-plan.md").exists()


def test_openharness_single_cli_supports_all_subcommands() -> None:
    parser = openharness.build_parser()
    choices = parser._subparsers._group_actions[0].choices  # type: ignore[attr-defined]
    assert set(choices) == {"bootstrap", "check-tasks", "new-task", "transition", "verify"}


def test_openharness_script_uses_task_package_naming_in_public_symbols() -> None:
    assert hasattr(openharness, "TaskPackage")
    assert hasattr(openharness, "TaskScaffoldRequest")
    assert hasattr(openharness, "discover_task_packages")
    assert hasattr(openharness, "validate_task_package")
    assert hasattr(openharness, "create_task_package")
    assert hasattr(openharness, "summarize_task_package")
    assert hasattr(openharness, "slugify_task_name")
    assert hasattr(openharness, "cmd_check_tasks")
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
    parser = openharness.build_parser()
    assert parser.parse_args(["check-tasks"]).handler == openharness.cmd_check_tasks
    assert parser.parse_args(["new-task", "name", "OH-999", "Title"]).handler == openharness.cmd_new_task
    assert parser.parse_args(["transition", "name", "requirements_ready"]).handler == openharness.cmd_transition


def test_openharness_skill_is_repo_entry_skill() -> None:
    skill_path = REPO_ROOT / "skills" / "using-openharness" / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    assert "`using-openharness` is the first repository workflow skill to check" in text
    assert "including clarifying questions" in text
    assert "only repository entry skill" in text
    assert "exploring-solution-space" in text
    assert "runtime verification" in text
    assert "reflection pass" in text
    assert "bounded subagent discussion" in text


def test_skill_hub_declares_no_parallel_entry_skill() -> None:
    hub_path = REPO_ROOT / "skills" / "using-openharness" / "references" / "skill-hub.md"
    text = hub_path.read_text(encoding="utf-8")
    assert "repository entry skill" in text
    assert "Do not keep a separate repository entry layer beside `openharness`." in text
    assert "`exploring-solution-space`" in text
    assert "reflection" in text


def test_skill_hub_uses_protocol_status_plus_stage_model() -> None:
    hub_path = REPO_ROOT / "skills" / "using-openharness" / "references" / "skill-hub.md"
    text = hub_path.read_text(encoding="utf-8")
    assert "## Protocol Status" in text
    assert "### Core Protocol Skills" in text
    assert "### Optional Helper Skills" in text
    assert "### Imported Generic Skills" in text
    assert "## Workflow Stages And Triggers" in text
    assert "### Entry And Routing" in text
    assert "### Requirements Convergence" in text
    assert "### Exploration And Architecture" in text
    assert "### Implementation Execution" in text
    assert "### Debugging And Repair" in text
    assert "### Verification And Closure" in text
    assert "### Repository Memory And Maintenance" in text


def test_optional_execution_skills_are_not_described_as_core_protocol() -> None:
    for path in [
        REPO_ROOT / "skills" / "subagent-driven-development" / "SKILL.md",
        REPO_ROOT / "skills" / "requesting-code-review" / "SKILL.md",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "04-implementation-plan.md" not in text


def test_exploration_skill_requires_reflection_before_design_is_ready() -> None:
    text = (REPO_ROOT / "skills" / "exploring-solution-space" / "SKILL.md").read_text(encoding="utf-8")
    assert "02-overview-design.md" in text
    assert "03-detailed-design.md" in text
    assert "primary output" in text
    assert "Only after `02-overview-design.md` is coherent" in text
    assert "reflection" in text
    assert "subagent" in text


def test_docs_describe_reflective_design_loop() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "reflection" in readme
    assert "reflection" in agents
    assert "subagent" in readme or "子智能体" in agents


def test_readme_describes_plug_and_play_harness_and_python_pytest_floor() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "plug-and-play" in readme
    assert "Python-first" in readme
    assert "`uv run pytest` is the default minimum automated verification floor" in readme
    assert "project-specific runtime verification" in readme


def test_agents_md_routes_repo_skill_usage_through_openharness() -> None:
    agents_path = REPO_ROOT / "AGENTS.md"
    text = agents_path.read_text(encoding="utf-8")
    assert "`using-openharness` 视为本仓库的默认入口技能" in text
    assert "先经过 `using-openharness` 做 skill routing" in text
    assert "探索" in text


def test_brainstorming_defaults_to_autonomous_continuation() -> None:
    text = (REPO_ROOT / "skills" / "brainstorming" / "SKILL.md").read_text(encoding="utf-8")
    assert "continue automatically by default" in text
    assert "Only stop for user review if one of these is true" in text
    assert "do not create unnecessary approval pauses" in text


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
        / "task-package.05-verification.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.06-evidence.md"
    ).read_text(encoding="utf-8")

    assert "## Overview Reflection" in overview
    assert "## Runtime Verification Plan" in detailed
    assert "Verification Path" in detailed
    assert "Fallback Path" in detailed
    assert "## Detailed Reflection" in detailed
    assert "## Verification Path" in verification
    assert "Executed Path" in verification
    assert "## Residual Risks" in evidence
    assert "Manual Steps" in evidence


def test_design_package_templates_include_status_guidance() -> None:
    readme = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.README.md"
    ).read_text(encoding="utf-8")
    status = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.STATUS.yaml"
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
        / "task-package.05-verification.md"
    ).read_text(encoding="utf-8")

    assert "Status should match the highest workflow checkpoint" in readme
    assert "requirements_ready -> overview_ready -> detailed_ready" in status
    assert "Move to `in_progress` only when detailed design is concrete enough to execute." in detailed
    assert "Use `verifying` only when implementation is complete enough" in verification


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
        / "task-package.05-verification.md"
    ).read_text(encoding="utf-8")
    evidence = (
        REPO_ROOT
        / "skills"
        / "using-openharness"
        / "references"
        / "templates"
        / "task-package.06-evidence.md"
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


def test_repo_protocol_documents_task_package_language_policy() -> None:
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    openharness_skill = (REPO_ROOT / "skills" / "using-openharness" / "SKILL.md").read_text(encoding="utf-8")

    assert "task package 的 Markdown 正文默认使用中文" in agents
    assert "章节标题、命令、状态值、YAML 键名、文件名与路径保持英文" in agents
    assert "task-package Markdown narrative should be Chinese-first" in openharness_skill
    assert "section titles, commands, status values, YAML keys, file names, and paths stay English" in openharness_skill


def test_verification_skill_distinguishes_manual_and_insufficient_paths() -> None:
    text = (REPO_ROOT / "skills" / "verification-before-completion" / "SKILL.md").read_text(encoding="utf-8")
    assert "manual runtime verification" in text
    assert "insufficient verification" in text
    assert "blocked completion state" in text


def test_workflow_skills_include_status_guidance() -> None:
    openharness_text = (REPO_ROOT / "skills" / "using-openharness" / "SKILL.md").read_text(encoding="utf-8")
    exploration_text = (REPO_ROOT / "skills" / "exploring-solution-space" / "SKILL.md").read_text(encoding="utf-8")

    assert "`overview_ready`" in exploration_text
    assert "`detailed_ready`" in exploration_text
    assert "`in_progress`" in openharness_text
    assert "`verifying`" in openharness_text
    assert "`archived`" in openharness_text


def test_verify_reports_declared_manual_scenarios_without_claiming_execution(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "manual-only").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "manual-only"
    (root / "README.md").write_text("# Manual Only\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-999\n"
        "title: Manual Only\n"
        "status: requirements_ready\n"
        "summary: manual verification only\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios:\n"
        "    - Open the app and confirm the banner text changes.\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="manual-only", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    assert result == 0
    assert calls == []
    assert "Declared manual scenarios" in captured.out
    assert "not executed automatically" in captured.out


def test_transition_rejects_skipped_forward_moves(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "skip-me").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "skip-me"
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-950\n"
        "title: Skip Me\n"
        "status: proposed\n"
        "summary: transition skip coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_transition(
        argparse.Namespace(repo=str(repo_root), task="skip-me", target_status="overview_ready")
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "next legal forward status is `requirements_ready`" in captured.out
    assert "status: proposed" in (root / "STATUS.yaml").read_text(encoding="utf-8")


def test_verify_records_artifact_and_status_metadata(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "artifact-run").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "artifact-run"
    (root / "README.md").write_text("# Artifact Run\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "05-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: x\n"
        "- Executed Path: y\n"
        "- Path Notes: z\n\n"
        "## Required Commands\n- echo ok\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "06-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- none\n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- a\n\n"
        "## Commands\n- echo ok\n\n"
        "## Follow-ups\n- none\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-951\n"
        "title: Artifact Run\n"
        "status: in_progress\n"
        "summary: verify artifact coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo ok\n"
        "  required_scenarios: []\n"
        "  last_run_at: \"\"\n"
        "  last_run_result: \"\"\n"
        "  last_run_artifact: \"\"\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="artifact-run", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    status = openharness._load_yaml(root / "STATUS.yaml")
    artifact_rel = status["verification"]["last_run_artifact"]
    artifact_path = repo_root / artifact_rel
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

    assert result == 0
    assert calls == ["echo ok"]
    assert "Recorded verification artifact" in captured.out
    assert artifact_path.exists()
    assert (artifact_path.parent / "latest.json").exists()
    assert status["verification"]["last_run_result"] == "passed"
    assert status["verification"]["last_run_at"]
    assert artifact["task_id"] == "OH-951"
    assert artifact["overall_result"] == "passed"
    assert artifact["package_fingerprint"]
    assert artifact["required_commands_snapshot"] == ["echo ok"]
    assert artifact["command_results"][0]["command"] == "echo ok"
    assert artifact["command_results"][0]["exit_code"] == 0


def test_transition_to_archived_moves_package_and_rewrites_paths(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "archive-me").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "archive-me"
    (root / "README.md").write_text("# Archive Me\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "05-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: docs/task-packages/archive-me/03-detailed-design.md\n"
        "- Executed Path: docs/task-packages/archive-me/05-verification.md\n"
        "- Path Notes: ok\n\n"
        "## Required Commands\n- echo ok\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "06-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- none\n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- docs/task-packages/archive-me/README.md\n\n"
        "## Commands\n- echo ok\n\n"
        "## Follow-ups\n- none\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-952\n"
        "title: Archive Me\n"
        "status: verifying\n"
        "summary: archive transition coverage\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "entrypoints:\n"
        "  - docs/task-packages/archive-me/README.md\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo ok\n"
        "  required_scenarios: []\n"
        "  last_run_at: \"\"\n"
        "  last_run_result: \"\"\n"
        "  last_run_artifact: \"\"\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/task-packages/archive-me/05-verification.md\n"
        "    - docs/task-packages/archive-me/06-evidence.md\n"
        "  code: []\n"
        "  tests: []\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(openharness, "_run_command", lambda repo, command: 0)

    verify_result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="archive-me", check_tasks_only=False)
    )
    assert verify_result == 0

    result = openharness.cmd_transition(
        argparse.Namespace(repo=str(repo_root), task="archive-me", target_status="archived")
    )

    captured = capsys.readouterr()
    archived_root = repo_root / "docs" / "archived" / "task-packages" / "archive-me"

    assert result == 0
    assert "Archived task package" in captured.out
    assert not root.exists()
    assert archived_root.exists()
    archived_status = (archived_root / "STATUS.yaml").read_text(encoding="utf-8")
    archived_verification = (archived_root / "05-verification.md").read_text(encoding="utf-8")
    archived_evidence = (archived_root / "06-evidence.md").read_text(encoding="utf-8")
    assert "status: archived" in archived_status
    assert "docs/archived/task-packages/archive-me/README.md" in archived_status
    assert "docs/archived/task-packages/archive-me/05-verification.md" in archived_status
    assert "docs/archived/task-packages/archive-me/03-detailed-design.md" in archived_verification
    assert "docs/archived/task-packages/archive-me/README.md" in archived_evidence


def test_verify_rejects_packages_with_no_declared_verification_path(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "no-verification").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "no-verification"
    (root / "README.md").write_text("# No Verification\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-998\n"
        "title: No Verification\n"
        "status: requirements_ready\n"
        "summary: missing verification path\n"
        "owner: codex\n"
        "created_at: 2026-03-20\n"
        "updated_at: 2026-03-20\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="no-verification", check_tasks_only=False)
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "insufficient verification" in captured.out
    assert "No command-backed verification or manual scenarios declared" in captured.out


def test_verify_defaults_to_later_stage_statuses_only(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )

    def write_package(name: str, status: str, command: str) -> None:
        root = repo_root / "docs" / "task-packages" / name
        root.mkdir(parents=True)
        (root / "README.md").write_text(f"# {name}\n", encoding="utf-8")
        (root / "01-requirements.md").write_text(
            "# Requirements\n\n"
            "## Goal\nA\n\n"
            "## Problem Statement\nB\n\n"
            "## Required Outcomes\n1. C\n\n"
            "## Non-Goals\n- D\n\n"
            "## Constraints\n- E\n",
            encoding="utf-8",
        )
        if status in {"overview_ready", "detailed_ready", "in_progress", "verifying", "archived"}:
            (root / "02-overview-design.md").write_text(
                "# Overview Design\n\n"
                "## System Boundary\nA\n\n"
                "## Proposed Structure\nB\n\n"
                "## Key Flows\nC\n\n"
                "## Trade-offs\nD\n\n"
                "## Overview Reflection\nE\n",
                encoding="utf-8",
            )
        else:
            (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
        if status in {"detailed_ready", "in_progress", "verifying", "archived"}:
            (root / "03-detailed-design.md").write_text(
                "# Detailed Design\n\n"
                "## Runtime Verification Plan\n"
                "- Verification Path:\n  - x\n"
                "- Fallback Path:\n  - y\n"
                "- Planned Evidence:\n  - z\n\n"
                "## Files Added Or Changed\n- a\n\n"
                "## Interfaces\nb\n\n"
                "## Error Handling\nc\n\n"
                "## Migration Notes\nd\n\n"
                "## Detailed Reflection\ne\n",
                encoding="utf-8",
            )
        else:
            (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
        if status in {"verifying", "archived"}:
            (root / "05-verification.md").write_text(
                "# Verification\n\n"
                "## Verification Path\n"
                "- Planned Path: x\n"
                "- Executed Path: y\n"
                "- Path Notes: z\n\n"
                "## Required Commands\n- cmd\n\n"
                "## Expected Outcomes\n- ok\n\n"
                "## Latest Result\n- pass\n",
                encoding="utf-8",
            )
        else:
            (root / "05-verification.md").write_text("x\n", encoding="utf-8")
        (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
        (root / "STATUS.yaml").write_text(
            f"id: {name.upper()}\n"
            f"title: {name}\n"
            f"status: {status}\n"
            "summary: status coverage\n"
            "owner: codex\n"
            "created_at: 2026-03-21\n"
            "updated_at: 2026-03-21\n"
            "done_criteria:\n"
            "  - x\n"
            "verification:\n"
            "  required_commands:\n"
            f"    - {command}\n"
            "  required_scenarios: []\n",
            encoding="utf-8",
        )

    write_package("requirements", "requirements_ready", "echo requirements")
    write_package("detailed", "detailed_ready", "echo detailed")
    write_package("progress", "in_progress", "echo progress")
    write_package("verifying", "verifying", "echo verifying")

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="", check_tasks_only=False)
    )

    capsys.readouterr()
    assert result == 0
    assert calls == ["echo progress", "echo verifying"]


def test_verify_allows_explicit_package_target_before_in_progress(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "early-target"
    root.mkdir(parents=True)
    (root / "README.md").write_text("# Early Target\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Migration Notes\nd\n\n"
        "## Detailed Reflection\ne\n",
        encoding="utf-8",
    )
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-777\n"
        "title: Early Target\n"
        "status: detailed_ready\n"
        "summary: explicit verify target\n"
        "owner: codex\n"
        "created_at: 2026-03-21\n"
        "updated_at: 2026-03-21\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - echo targeted\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    calls: list[str] = []

    def fake_run(repo: Path, command: str) -> int:
        calls.append(command)
        return 0

    monkeypatch.setattr(openharness, "_run_command", fake_run)

    result = openharness.cmd_verify(
        argparse.Namespace(repo=str(repo_root), design="early-target", check_tasks_only=False)
    )

    capsys.readouterr()
    assert result == 0
    assert calls == ["echo targeted"]


def test_validate_design_package_rejects_requirements_ready_with_placeholder_requirements(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "placeholder-reqs").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "placeholder-reqs"
    (root / "README.md").write_text("# Placeholder Reqs\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\n\n"
        "## Problem Statement\n\n"
        "## Required Outcomes\n"
        "1. \n\n"
        "## Non-Goals\n"
        "- \n\n"
        "## Constraints\n"
        "- \n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text("x\n", encoding="utf-8")
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-903\n"
        "title: Placeholder Reqs\n"
        "status: requirements_ready\n"
        "summary: requirements shell only\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("requirements_ready requires non-placeholder content" in error for error in errors)


def test_validate_design_package_rejects_overview_ready_without_reflection(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "overview-no-reflection").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "overview-no-reflection"
    (root / "README.md").write_text("# Overview No Reflection\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text("x\n", encoding="utf-8")
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-904\n"
        "title: Overview No Reflection\n"
        "status: overview_ready\n"
        "summary: overview missing reflection\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("overview_ready requires non-placeholder content" in error for error in errors)
    assert any("## Overview Reflection" in error for error in errors)


def test_validate_design_package_rejects_archived_without_evidence_anchors(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-thin-evidence").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "archived" / "task-packages" / "archived-thin-evidence"
    (root / "README.md").write_text("# Archived Thin Evidence\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Detailed Reflection\nd\n",
        encoding="utf-8",
    )
    (root / "05-verification.md").write_text(
        "# Verification\n\n"
        "## Verification Path\n"
        "- Planned Path: x\n"
        "- Executed Path: y\n"
        "- Path Notes: z\n\n"
        "## Required Commands\n- cmd\n\n"
        "## Expected Outcomes\n- ok\n\n"
        "## Latest Result\n- pass\n",
        encoding="utf-8",
    )
    (root / "06-evidence.md").write_text(
        "# Evidence\n\n"
        "## Residual Risks\n- \n\n"
        "## Manual Steps\n- none\n\n"
        "## Files\n- \n\n"
        "## Commands\n- \n\n"
        "## Follow-ups\n- later\n",
        encoding="utf-8",
    )
    (root / "STATUS.yaml").write_text(
        "id: OH-905\n"
        "title: Archived Thin Evidence\n"
        "status: archived\n"
        "summary: archived without evidence anchors\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands:\n"
        "    - uv run pytest\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("archived requires non-placeholder content" in error for error in errors)


def test_validate_design_package_accepts_detailed_ready_with_filled_semantic_anchors(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "detailed-solid").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - STATUS.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - 05-verification.md\n"
        "  - 06-evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_ready\n"
        "    - overview_ready\n"
        "    - detailed_ready\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "detailed-solid"
    (root / "README.md").write_text("# Detailed Solid\n", encoding="utf-8")
    (root / "01-requirements.md").write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    (root / "02-overview-design.md").write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n\n"
        "## Overview Reflection\nE\n",
        encoding="utf-8",
    )
    (root / "03-detailed-design.md").write_text(
        "# Detailed Design\n\n"
        "## Runtime Verification Plan\n"
        "- Verification Path:\n  - x\n"
        "- Fallback Path:\n  - y\n"
        "- Planned Evidence:\n  - z\n\n"
        "## Files Added Or Changed\n- a\n\n"
        "## Interfaces\nb\n\n"
        "## Error Handling\nc\n\n"
        "## Detailed Reflection\nd\n",
        encoding="utf-8",
    )
    (root / "05-verification.md").write_text("x\n", encoding="utf-8")
    (root / "06-evidence.md").write_text("x\n", encoding="utf-8")
    (root / "STATUS.yaml").write_text(
        "id: OH-906\n"
        "title: Detailed Solid\n"
        "status: detailed_ready\n"
        "summary: detailed anchors filled\n"
        "owner: codex\n"
        "created_at: 2026-03-22\n"
        "updated_at: 2026-03-22\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]

    assert validate_task_package(package) == []
