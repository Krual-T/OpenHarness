
from .common import (
    Path,
    ALL_DESIGN_FILES,
    REPO_ROOT,
    TaskPackageDocument,
    json,
    pytest,
    setup_harness,
    validate_task_package,
    discover_task_packages,
)
from typer.testing import CliRunner
from openharness_cli.cli import app

runner = CliRunner()


def test_bootstrap_reports_yaml_quote_hint_for_invalid_status_yaml(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "bad-yaml").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "bad-yaml"
    for doc in ALL_DESIGN_FILES:
        if doc != TaskPackageDocument.TASK_INFO:
            doc.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-998\n"
        "title: Bad YAML\n"
        "status: proposed\n"
        "summary: `overview-design.md` guidance: fix quoting\n"
        "owner: codex\n"
        "created_at: 2026-03-30\n"
        "updated_at: 2026-03-30\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list", "--json"])
    assert result.exit_code == 1
    assert "wrap the whole sentence in double quotes" in result.stdout
    assert 'summary: "`overview-design.md` guidance: fix quoting"' in result.stdout


def test_bootstrap_reports_stage_guidance_in_text_output(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-960\n"
        "title: Visible Stage\n"
        "status: overview_designing\n"
        "summary: stage guidance\n"
        "owner: codex\n"
        "created_at: 2026-03-24\n"
        "updated_at: 2026-03-24\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list"])
    assert result.exit_code == 0
    assert "Harness manifest:" not in result.stdout
    assert "Task package root:" not in result.stdout
    assert "current stage:" in result.stdout
    assert "next stage:" in result.stdout
    assert "next step:" in result.stdout
    assert "`overview_designing`" in result.stdout


def test_task_package_view_injects_current_stage_skill(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    state_root = repo_root / "skills" / "using-openharness" / "states" / "exploring-solution-space"
    state_root.mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (state_root / "SKILL.md").write_text("# Overview Stage\n\nUse overview guidance.\n", encoding="utf-8")
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-964\n"
        "title: Visible Stage View\n"
        "status: overview_designing\n"
        "summary: stage view\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "view", "visible-stage"])

    assert result.exit_code == 0
    assert "Task: OH-964 Visible Stage View" in result.stdout
    assert "Status: `overview_designing`" in result.stdout
    assert "--- BEGIN: skills/using-openharness/states/exploring-solution-space/SKILL.md ---" in result.stdout
    assert "# Overview Stage" in result.stdout


def test_transition_verified_reports_auto_archive(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "ready-to-archive").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "ready-to-archive"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text(
        "# Evidence\n\n## Verification Result\npassed\n",
        encoding="utf-8",
    )
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-966\n"
        "title: Ready To Archive\n"
        "status: verifying\n"
        "summary: auto archive message\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "done_criteria:\n"
        "  - x\n"
        "entrypoints:\n"
        "  - docs/task-packages/ready-to-archive/requirements.md\n"
        "verification:\n"
        "  verify_by: qualitative\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "ready-to-archive", "verified"],
    )

    assert result.exit_code == 0
    assert "Archived task package: OH-966" in result.stdout
    assert "already in `verifying`" not in result.stdout
    assert not root.exists()
    archived_info = repo_root / "docs" / "archived" / "task-packages" / "ready-to-archive" / "task-info.yaml"
    assert archived_info.exists()
    archived_text = archived_info.read_text(encoding="utf-8")
    assert "docs/archived/task-packages/ready-to-archive/requirements.md" in archived_text
    assert "README.md" not in archived_text


def test_transition_verified_keeps_source_status_when_archive_target_exists(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "archive-conflict").mkdir(parents=True)
    (repo_root / "docs" / "archived" / "task-packages" / "archive-conflict").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "archive-conflict"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text(
        "# Evidence\n\n## Verification Result\npassed\n",
        encoding="utf-8",
    )
    info_path = TaskPackageDocument.TASK_INFO.path_from(root)
    info_path.write_text(
        "id: OH-967\n"
        "title: Archive Conflict\n"
        "status: verifying\n"
        "summary: archive conflict\n"
        "owner: codex\n"
        "created_at: 2026-05-18\n"
        "updated_at: 2026-05-18\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  verify_by: qualitative\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--repo", str(repo_root), "task-package", "transition", "archive-conflict", "verified"],
    )

    assert result.exit_code == 1
    assert "archive target already exists" in result.stdout
    assert root.exists()
    assert "status: verifying" in info_path.read_text(encoding="utf-8")


def test_bootstrap_reports_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-962\n"
        "title: Visible Stage Author Entry\n"
        "status: proposing\n"
        "summary: author entry surface\n"
        "owner: codex\n"
        "created_at: 2026-03-27\n"
        "updated_at: 2026-03-27\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list"])
    assert result.exit_code == 0
    assert "author entry:" in result.stdout
    assert "author-entry.md" in result.stdout


def test_init_parser_accepts_repo_argument() -> None:
    result = runner.invoke(app, ["--repo", "/tmp/example-repo", "init"])
    assert result.exit_code == 0


def test_init_creates_harness_gitignore_that_ignores_everything(
    tmp_path: Path, capsys
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    result = runner.invoke(app, ["--repo", str(repo_root), "init"])
    captured = capsys.readouterr()
    assert result.exit_code == 0
    assert (repo_root / ".harness" / ".gitignore").read_text(encoding="utf-8") == "*\n"
    assert str(repo_root / ".harness") in result.stdout


def test_bootstrap_json_includes_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for doc in ALL_DESIGN_FILES:
        doc.path_from(root).write_text("# x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-963\n"
        "title: Visible Stage Json Author Entry\n"
        "status: detailed_designed\n"
        "summary: author entry json\n"
        "owner: codex\n"
        "created_at: 2026-03-27\n"
        "updated_at: 2026-03-27\n"
        "done_criteria:\n"
        "  - x\n"
        "verification:\n"
        "  required_commands: []\n"
        "  required_scenarios: []\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--repo", str(repo_root), "task-package", "list", "--json"])
    payload = json.loads(result.stdout)
    assert result.exit_code == 0
    assert payload["author_entry"]["path"].endswith("author-entry.md")


def test_validate_design_package_rejects_overview_designed_without_reflection(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "overview-no-reflection").mkdir(parents=True)
    root = repo_root / "docs" / "task-packages" / "overview-no-reflection"
    TaskPackageDocument.REQUIREMENTS.path_from(root).write_text(
        "# Requirements\n\n"
        "## Goal\nA\n\n"
        "## Problem Statement\nB\n\n"
        "## Required Outcomes\n1. C\n\n"
        "## Non-Goals\n- D\n\n"
        "## Constraints\n- E\n",
        encoding="utf-8",
    )
    TaskPackageDocument.OVERVIEW_DESIGN.path_from(root).write_text(
        "# Overview Design\n\n"
        "## System Boundary\nA\n\n"
        "## Proposed Structure\nB\n\n"
        "## Key Flows\nC\n\n"
        "## Trade-offs\nD\n",
        encoding="utf-8",
    )
    TaskPackageDocument.DETAILED_DESIGN.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.VERIFICATION_DESIGN.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.EVIDENCE.path_from(root).write_text("x\n", encoding="utf-8")
    TaskPackageDocument.TASK_INFO.path_from(root).write_text(
        "id: OH-904\n"
        "title: Overview No Reflection\n"
        "status: overview_designed\n"
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

    setup_harness(repo_root)
    package = discover_task_packages()[0]
    errors = validate_task_package(package)

    assert any("overview_designed requires non-placeholder content" in error for error in errors)
    assert any("## Overview Reflection" in error for error in errors)
