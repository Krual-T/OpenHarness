from __future__ import annotations

from .common import (
    Path,
    ALL_DESIGN_FILES,
    REPO_ROOT,
    argparse,
    json,
    load_config,
    openharness,
    pytest,
    validate_task_package,
    discover_task_packages,
)


def test_bootstrap_reports_yaml_quote_hint_for_invalid_status_yaml(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "bad-yaml").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "bad-yaml"
    for name in ALL_DESIGN_FILES:
        if name != "task-info.yaml":
            (root / name).write_text("x\n", encoding="utf-8")
    (root / "task-info.yaml").write_text(
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

    result = openharness.cmd_task_package_list(argparse.Namespace(repo=str(repo_root), json=True, all=False))

    captured = capsys.readouterr()
    assert result == 1
    assert "wrap the whole sentence in double quotes" in captured.out
    assert 'summary: "`02-overview-design.md` guidance: fix quoting"' in captured.out


def test_bootstrap_reports_stage_guidance_in_text_output(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_designed\n"
        "    - overview_designed\n"
        "    - detailed_designed\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in ALL_DESIGN_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "task-info.yaml").write_text(
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

    result = openharness.cmd_task_package_list(argparse.Namespace(repo=str(repo_root), json=False, all=False))

    captured = capsys.readouterr()
    assert result == 0
    assert "Harness manifest:" not in captured.out
    assert "Task package root:" not in captured.out
    assert "current stage:" in captured.out
    assert "next stage:" in captured.out
    assert "next step:" in captured.out
    assert "`overview_designing`" in captured.out


def test_bootstrap_reports_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_designed\n"
        "    - overview_designed\n"
        "    - detailed_designed\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in ALL_DESIGN_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "task-info.yaml").write_text(
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

    result = openharness.cmd_task_package_list(argparse.Namespace(repo=str(repo_root), json=False, all=False))

    captured = capsys.readouterr()
    assert result == 0
    assert "author entry:" in captured.out
    assert "author-entry.md" in captured.out


def test_init_parser_accepts_repo_argument() -> None:
    parser = openharness.build_parser()

    args = parser.parse_args(["init", "--repo", "/tmp/example-repo"])

    assert args.handler == openharness.cmd_init
    assert args.repo == "/tmp/example-repo"


def test_init_creates_harness_gitignore_that_ignores_everything(
    tmp_path: Path, capsys
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    result = openharness.cmd_init(argparse.Namespace(repo=str(repo_root)))

    captured = capsys.readouterr()
    assert result == 0
    assert (repo_root / ".harness" / ".gitignore").read_text(encoding="utf-8") == "*\n"
    assert str(repo_root / ".harness") in captured.out


def test_bootstrap_json_includes_author_entry_when_present(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    references_root = repo_root / "skills" / "using-openharness" / "references"
    references_root.mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "visible-stage").mkdir(parents=True)
    (references_root / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_designed\n"
        "    - overview_designed\n"
        "    - detailed_designed\n"
        "    - in_progress\n"
        "    - verifying\n"
        "    - archived\n",
        encoding="utf-8",
    )
    (references_root / "author-entry.md").write_text("# Author Entry\n", encoding="utf-8")
    root = repo_root / "docs" / "task-packages" / "visible-stage"
    for name in ALL_DESIGN_FILES:
        (root / name).write_text("# x\n", encoding="utf-8")
    (root / "task-info.yaml").write_text(
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

    result = openharness.cmd_task_package_list(argparse.Namespace(repo=str(repo_root), json=True, all=False))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["author_entry"]["path"].endswith("author-entry.md")


def test_validate_design_package_rejects_overview_designed_without_reflection(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references").mkdir(parents=True)
    (repo_root / "docs" / "task-packages" / "overview-no-reflection").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n"
        "workflow:\n"
        "  default_status_flow:\n"
        "    - proposed\n"
        "    - requirements_designed\n"
        "    - overview_designed\n"
        "    - detailed_designed\n"
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
    (root / "verification_design.md").write_text("x\n", encoding="utf-8")
    (root / "evidence.md").write_text("x\n", encoding="utf-8")
    (root / "task-info.yaml").write_text(
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

    manifest = load_config(repo_root)
    package = discover_task_packages(repo_root, manifest)[0]
    errors = validate_task_package(package)

    assert any("overview_designed requires non-placeholder content" in error for error in errors)
    assert any("## Overview Reflection" in error for error in errors)
