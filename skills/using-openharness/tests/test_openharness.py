from __future__ import annotations

import argparse
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import openharness
from openharness import (
    ACTIVE_STATUSES,
    DesignScaffoldRequest,
    REQUIRED_TASK_PACKAGE_FILES,
    create_design_package,
    discover_design_packages,
    load_manifest,
    slugify_design_name,
    summarize_design_package,
    validate_design_package,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_manifest_points_to_task_package_roots() -> None:
    manifest = load_manifest(REPO_ROOT)
    assert manifest.task_packages_root == REPO_ROOT / "docs" / "task-packages"
    assert manifest.archived_task_packages_root == REPO_ROOT / "docs" / "archived" / "task-packages"


def test_self_hosting_design_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_design_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "self-hosting-bootstrap")
    assert package.design_id == "OH-001"
    assert package.status_name == "archived"
    assert "Self-Hosting Bootstrap" in summarize_design_package(package)


def test_workflow_redesign_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_design_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "workflow-redesign")
    assert package.design_id == "OH-002"
    assert package.status_name == "archived"
    assert "Workflow Redesign" in summarize_design_package(package)


def test_reflective_design_review_package_is_discoverable() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_design_packages(REPO_ROOT, manifest)
    package = next(package for package in packages if package.name == "reflective-design-review")
    assert package.design_id == "OH-003"
    assert package.status_name == "archived"
    assert "Reflective Design Review" in summarize_design_package(package)


def test_active_statuses_do_not_include_archived() -> None:
    assert "in_progress" in ACTIVE_STATUSES
    assert "archived" not in ACTIVE_STATUSES


def test_design_packages_validate_cleanly() -> None:
    manifest = load_manifest(REPO_ROOT)
    packages = discover_design_packages(REPO_ROOT, manifest)
    errors = [error for package in packages for error in validate_design_package(package)]
    assert errors == []


def test_load_manifest_prefers_repo_local_skills_layout(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    assert manifest.path == (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml")


def test_validate_design_package_rejects_unknown_status_and_missing_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "broken").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
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
    package = discover_design_packages(repo_root, manifest)[0]
    errors = validate_design_package(package)

    assert any("unknown status" in error for error in errors)
    assert any("missing referenced path" in error for error in errors)


def test_validate_design_package_rejects_archived_status_in_active_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "wrong-place").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    package = discover_design_packages(repo_root, manifest)[0]
    errors = validate_design_package(package)
    assert any("archived package must live under" in error for error in errors)


def test_validate_design_package_rejects_verifying_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "verifying-empty").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    package = discover_design_packages(repo_root, manifest)[0]
    errors = validate_design_package(package)

    assert any("verifying status requires at least one verification path" in error for error in errors)


def test_validate_design_package_rejects_archived_without_verification_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archived-empty").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    package = discover_design_packages(repo_root, manifest)[0]
    errors = validate_design_package(package)

    assert any("archived status requires at least one verification path" in error for error in errors)


def test_slugify_design_name_normalizes_human_text() -> None:
    assert slugify_design_name("Harness Replay Flow") == "harness-replay-flow"


def test_create_design_package_from_templates(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\ndesigns_root: docs/task-packages\narchived_designs_root: docs/archived/task-packages\nrequired_design_files:\n"
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

    design_root = create_design_package(
        DesignScaffoldRequest(
            repo_root=repo_root,
            design_name="Harness Replay",
            design_id="OH-016",
            title="Harness Replay",
            owner="codex",
            summary="Replay scenarios.",
        )
    )

    assert design_root == repo_root / "docs" / "task-packages" / "harness-replay"
    assert (design_root / "README.md").read_text(encoding="utf-8") == "# OH-016 Harness Replay\n"
    assert not (design_root / "04-implementation-plan.md").exists()
    assert "summary: Replay scenarios." in (design_root / "STATUS.yaml").read_text(encoding="utf-8")


def test_key_repo_skills_are_vendored_locally() -> None:
    expected = [
        "using-openharness",
        "exploring-solution-space",
        "using-git-worktrees",
        "writing-plans",
        "executing-plans",
        "verification-before-completion",
        "systematic-debugging",
        "finishing-a-development-branch",
    ]
    for name in expected:
        path = REPO_ROOT / "skills" / name
        assert path.is_dir()
        assert (path / "SKILL.md").exists()


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
    assert set(choices) == {"bootstrap", "check-designs", "check-tasks", "new-design", "new-task", "verify"}


def test_task_package_aliases_share_legacy_handlers() -> None:
    parser = openharness.build_parser()
    assert parser.parse_args(["check-tasks"]).handler == openharness.cmd_check_designs
    assert parser.parse_args(["check-designs"]).handler == openharness.cmd_check_designs
    assert parser.parse_args(["new-task", "name", "OH-999", "Title"]).handler == openharness.cmd_new_design
    assert parser.parse_args(["new-design", "name", "OH-999", "Title"]).handler == openharness.cmd_new_design


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


def test_optional_execution_skills_are_not_described_as_core_protocol() -> None:
    for path in [
        REPO_ROOT / "skills" / "writing-plans" / "SKILL.md",
        REPO_ROOT / "skills" / "executing-plans" / "SKILL.md",
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

    assert "## Runtime Verification Plan" in detailed
    assert "Verification Path" in detailed
    assert "Fallback Path" in detailed
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
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
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
        argparse.Namespace(repo=str(repo_root), design="manual-only", check_designs_only=False)
    )

    captured = capsys.readouterr()
    assert result == 0
    assert calls == []
    assert "Declared manual scenarios" in captured.out
    assert "not executed automatically" in captured.out


def test_verify_rejects_packages_with_no_declared_verification_path(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "no-verification").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    for name in REQUIRED_TASK_PACKAGE_FILES:
        (root / name).write_text("x\n", encoding="utf-8")
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
        argparse.Namespace(repo=str(repo_root), design="no-verification", check_designs_only=False)
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
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
        for file_name in REQUIRED_TASK_PACKAGE_FILES:
            (root / file_name).write_text("x\n", encoding="utf-8")
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
        argparse.Namespace(repo=str(repo_root), design="", check_designs_only=False)
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
        "designs_root: docs/task-packages\n"
        "archived_designs_root: docs/archived/task-packages\n"
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
    for file_name in REQUIRED_TASK_PACKAGE_FILES:
        (root / file_name).write_text("x\n", encoding="utf-8")
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
        argparse.Namespace(repo=str(repo_root), design="early-target", check_designs_only=False)
    )

    capsys.readouterr()
    assert result == 0
    assert calls == ["echo targeted"]
