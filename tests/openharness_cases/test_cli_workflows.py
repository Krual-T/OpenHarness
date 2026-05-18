
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
        "summary: `02-overview-design.md` guidance: fix quoting\n"
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
    assert 'summary: "`02-overview-design.md` guidance: fix quoting"' in result.stdout


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
    TaskPackageDocument.README.path_from(root).write_text("# Overview No Reflection\n", encoding="utf-8")
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
