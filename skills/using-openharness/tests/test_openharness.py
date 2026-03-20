from __future__ import annotations

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
    REQUIRED_DESIGN_FILES,
    create_design_package,
    discover_design_packages,
    load_manifest,
    slugify_design_name,
    summarize_design_package,
    validate_design_package,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_manifest_points_to_designs_root() -> None:
    manifest = load_manifest(REPO_ROOT)
    assert manifest.designs_root == REPO_ROOT / "docs" / "designs"
    assert manifest.archived_designs_root == REPO_ROOT / "docs" / "archived" / "designs"


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
        "designs_root: docs/designs\n"
        "archived_designs_root: docs/archived/designs\n",
        encoding="utf-8",
    )

    manifest = load_manifest(repo_root)
    assert manifest.path == (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml")


def test_validate_design_package_rejects_unknown_status_and_missing_paths(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "designs" / "broken").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/designs\n"
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
    root = repo_root / "docs" / "designs" / "broken"
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
        "  - docs/designs/broken/README.md\n"
        "  - docs/designs/broken/missing.md\n"
        "verification:\n"
        "  required_commands: []\n"
        "evidence:\n"
        "  docs:\n"
        "    - docs/designs/broken/06-evidence.md\n"
        "    - docs/designs/broken/nope.md\n",
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
    (repo_root / "docs" / "designs" / "wrong-place").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "designs_root: docs/designs\n"
        "archived_designs_root: docs/archived/designs\n"
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
    root = repo_root / "docs" / "designs" / "wrong-place"
    for name in REQUIRED_DESIGN_FILES:
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


def test_slugify_design_name_normalizes_human_text() -> None:
    assert slugify_design_name("Harness Replay Flow") == "harness-replay-flow"


def test_create_design_package_from_templates(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "designs").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\ndesigns_root: docs/designs\narchived_designs_root: docs/archived/designs\nrequired_design_files:\n"
        "  - README.md\n  - STATUS.yaml\n  - 01-requirements.md\n  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n  - 05-verification.md\n  - 06-evidence.md\n",
        encoding="utf-8",
    )
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    for file_name, content in {
        "design-package.README.md": "# <DESIGN_ID> <TITLE>\n",
        "design-package.STATUS.yaml": "id: <DESIGN_ID>\ntitle: <TITLE>\nstatus: <STATUS>\nsummary: <SUMMARY>\nowner: <OWNER>\ncreated_at: <DATE>\nupdated_at: <DATE>\ndone_criteria:\n  - x\nverification:\n  required_commands: []\n",
        "design-package.01-requirements.md": "req\n",
        "design-package.02-overview-design.md": "overview\n",
        "design-package.03-detailed-design.md": "detail\n",
        "design-package.05-verification.md": "verify\n",
        "design-package.06-evidence.md": "evidence\n",
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

    assert design_root == repo_root / "docs" / "designs" / "harness-replay"
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
    assert (skill_root / "references" / "templates" / "design-package.README.md").exists()
    assert (skill_root / "references" / "templates" / "design-package.STATUS.yaml").exists()
    assert not (skill_root / "references" / "templates" / "design-package.04-implementation-plan.md").exists()


def test_openharness_single_cli_supports_all_subcommands() -> None:
    parser = openharness.build_parser()
    choices = parser._subparsers._group_actions[0].choices  # type: ignore[attr-defined]
    assert set(choices) == {"bootstrap", "check-designs", "new-design", "verify"}


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
